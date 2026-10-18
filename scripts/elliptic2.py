"""Independent E5 labeled-subgraph baseline, not full-background GLASS reproduction."""
import hashlib
import json
import zipfile
import time
from pathlib import Path
import requests
import numpy as np
import pandas as pd
import networkx as nx
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from topoaml.data import ROOT
from topoaml.topology import structural_features, graph_betti, filtration, persistence_features
from topoaml.evaluation import metrics, choose_threshold


def main():
    raw=ROOT/'data/raw/elliptic2';raw.mkdir(parents=True,exist_ok=True)
    files=[]
    for name in ['connected_components.csv','nodes.csv','edges.csv']:
        url='https://www.kaggle.com/api/v1/datasets/download/ellipticco/elliptic2-data-set/'+name
        path=raw/name
        if not path.exists():
            response=requests.get(url,timeout=120);response.raise_for_status()
            archive=raw/(name+'.download');archive.write_bytes(response.content)
            with zipfile.ZipFile(archive) as z:
                if z.namelist()!=[name]:raise ValueError('Unexpected archive members')
                z.extract(name,raw)
        files.append({'name':name,'url':url,'sha256':hashlib.file_digest(path.open('rb'),'sha256').hexdigest(),'bytes':path.stat().st_size})
    cc=pd.read_csv(raw/'connected_components.csv');nodes=pd.read_csv(raw/'nodes.csv');edges=pd.read_csv(raw/'edges.csv')
    if not set(['clId','ccId']).issubset(nodes.columns) or not set(['clId1','clId2']).issubset(edges.columns):raise ValueError('Unexpected schema')
    counts=nodes.groupby('clId').ccId.nunique()
    # The source small edge list has no ccId. A unique node-to-component map is
    # required before it can be assigned unambiguously; fail on overlap.
    if (counts>1).any():raise ValueError('Overlapping memberships require a different edge assignment')
    membership=nodes.set_index('clId').ccId.to_dict()
    edgelists={}
    for u,v in edges[['clId1','clId2']].itertuples(index=False,name=None):
        a,b=membership.get(u),membership.get(v)
        if a is not None and a==b:edgelists.setdefault(a,[]).append((u,v))
    # Reproduce actual upstream preprocess_glass.py counter % 10 assignment.
    # This is file-order deterministic, not the random-seed split claimed in README.
    order=nodes.ccId.drop_duplicates().tolist()
    split={c:('train' if (i+1)%10<=7 else 'validation' if (i+1)%10==8 else 'test') for i,c in enumerate(order)}
    manifest={'dataset':'Elliptic2 labeled-subgraph release','source':'https://www.kaggle.com/datasets/ellipticco/elliptic2-data-set',
              'files':files,'subgraphs':len(cc),'memberships':len(nodes),'edges':len(edges),
              'labels':cc.ccLabel.value_counts().to_dict(),'overlap_nodes':int((counts>1).sum()),
              'license':'CC BY-NC-ND 4.0, verified from provider API; raw data not redistributed',
              'version':1,
              'protocol':'actual upstream preprocess_glass.py file-order counter modulo 10',
              'scope':'within-subgraph structural/topology baselines; no full background graph, timestamps or original node attributes',
              'limitations':['Not GLASS/GNNSeg/Sub2vec reproduction','No temporal generalization claim for Elliptic2','Inter-dataset independence of records not established']}
    (ROOT/'data/manifests/elliptic2_manifest.json').write_text(json.dumps(manifest,indent=2))
    processed=ROOT/'data/processed/elliptic2';processed.mkdir(exist_ok=True)
    frame=cc[['ccId','ccLabel']].copy();frame['split']=frame.ccId.map(split)
    payload=frame.to_csv(index=False).encode();lock=processed/'split_ids.csv'
    if lock.exists() and lock.read_bytes()!=payload:raise ValueError('Elliptic2 split mutation')
    lock.write_bytes(payload)
    published=ROOT/'data/splits';published.mkdir(exist_ok=True)
    frame[['ccId','split']].to_csv(published/'elliptic2_ids.csv',index=False)
    manifest['split_sha256']=hashlib.sha256(payload).hexdigest()
    (ROOT/'data/manifests/elliptic2_manifest.json').write_text(json.dumps(manifest,indent=2))
    out=ROOT/'results/elliptic2';out.mkdir(parents=True,exist_ok=True)
    feature_path=processed/'features.csv'
    if not feature_path.exists():
        rows=[];start=time.perf_counter()
        for i,(cid,sub) in enumerate(nodes.groupby('ccId',sort=False)):
            g=nx.Graph();g.add_nodes_from(sub.clId);g.add_edges_from(edgelists.get(cid,[]))
            # The release includes a 296-node subgraph. Preserve whole graphs.
            if len(g)>512:raise ValueError('Subgraph bound exceeded; define a new protocol before evaluation')
            row={'ccId':cid};row.update({'s_'+k:v for k,v in structural_features(g).items()})
            row.update({'p_'+k:v for k,v in persistence_features(filtration(g,max_nodes=512)).items()});rows.append(row)
            if i%10000==0:print('Elliptic2 features',i,'seconds',round(time.perf_counter()-start,1),flush=True)
        pd.DataFrame(rows).to_csv(feature_path,index=False)
    d=frame.merge(pd.read_csv(feature_path),on='ccId',validate='one_to_one')
    if not set(d.ccLabel).issubset({'licit','suspicious','illicit'}):raise ValueError('Unrecognized subgraph labels')
    d['y']=(d.ccLabel!='licit').astype(int)
    train=d.split=='train';val=d.split=='validation';test=d.split=='test'
    for seed in [11,22,33,44,55]:
        for group in ['S','SP']:
            columns=[c for c in d if c.startswith('s_') or (group=='SP' and c.startswith('p_'))]
            for family in ['random_forest','xgboost']:
                name=f'{family}_{group}_seed{seed}'; report=out/f'{name}.json'
                if report.exists():continue
                model=RandomForestClassifier(n_estimators=200,max_depth=12,min_samples_leaf=3,class_weight='balanced',n_jobs=6,random_state=seed) if family=='random_forest' else XGBClassifier(n_estimators=200,max_depth=4,learning_rate=.05,subsample=.9,colsample_bytree=.9,n_jobs=6,random_state=seed,tree_method='hist')
                start=time.perf_counter();pipe=make_pipeline(StandardScaler(),model);pipe.fit(d.loc[train,columns],d.loc[train,'y'])
                pv=pipe.predict_proba(d.loc[val,columns])[:,1];threshold=choose_threshold(d.loc[val,'y'],pv);pt=pipe.predict_proba(d.loc[test,columns])[:,1]
                row={'name':name,'seed':seed,'family':family,'group':group,'threshold':threshold,'test':metrics(d.loc[test,'y'],pt,threshold),'seconds':time.perf_counter()-start}
                report.write_text(json.dumps(row,indent=2))
                pred=d.loc[test,['ccId','y']].copy();pred['probability']=pt;pred.to_csv(out/f'{name}_predictions.csv',index=False)
                import joblib
                joblib.dump(pipe,out/f'{name}.joblib');print('Elliptic2',name,'done',flush=True)

if __name__=='__main__':main()
