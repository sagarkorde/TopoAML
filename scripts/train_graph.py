"""Target-centered mini-batches avoid full-graph future message passing."""
import argparse
import json
import time
import numpy as np
import pandas as pd
import torch
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader
from topoaml.data import ROOT, SAFE_FIELDS, load, graph_and_times
from topoaml.temporal import historical_neighborhood, split_name
from topoaml.models import TopoGraph
from topoaml.evaluation import choose_threshold, metrics


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--epochs',type=int,default=15)
    parser.add_argument('--seeds',type=int,nargs='+',default=[11,22,33,44,55]); parser.add_argument('--batch-size',type=int,default=256)
    parser.add_argument('--families',nargs='+',default=['sage','gat'])
    args=parser.parse_args(); torch.set_num_threads(6)
    f,e=load(); g,times=graph_and_times(f,e); f=f.set_index('txId')
    feature=pd.concat([pd.read_csv(p) for p in sorted((ROOT/'data/processed/features_k2_n32_distance').glob('*.csv'))]).set_index('txId').sort_index()
    if len(feature)!=46564:raise ValueError('Incomplete extraction; finish scripts/extract.py first')
    structural=[c for c in feature if c.startswith('s_')]
    topo={group:[c for c in feature if c.startswith(prefix)] for group,prefix in [('B','b_'),('P','p_')]}
    # Structural center fields enter q; original transaction fields enter message passing.
    feature['split']=[split_name(times[v]) for v in feature.index]
    node_train=f['Time step']<=30
    imputer=SimpleImputer(strategy='median',add_indicator=True).fit(f.loc[node_train,SAFE_FIELDS])
    x=imputer.transform(f[SAFE_FIELDS]); scaler=StandardScaler().fit(x[node_train]); x=scaler.transform(x).astype('float32')
    # Fit structural and topology transforms only on labeled train centers.
    all_cols=structural+topo['B']+topo['P']
    zscaler=StandardScaler().fit(feature.loc[feature.split=='train',all_cols])
    z=pd.DataFrame(zscaler.transform(feature[all_cols]),index=feature.index,columns=all_cols)
    zvalues=z.to_numpy(dtype='float32')
    feature_lookup={v:i for i,v in enumerate(feature.index)}
    structural_indices=[all_cols.index(c) for c in structural]
    topo_indices={group:[all_cols.index(c) for c in columns] for group,columns in topo.items()}
    topology_tensors={group:torch.tensor(zvalues[:,indices],dtype=torch.float32) for group,indices in topo_indices.items()}
    lookup={v:i for i,v in enumerate(f.index)}
    cache={}
    for target in feature.index:
        h,_=historical_neighborhood(g,times,target,2,32)
        nodes=[target]+sorted(set(h)-{target}); mapping={v:i for i,v in enumerate(nodes)}
        # Reciprocal projection is explicit: message passing does not infer fund-flow cycles.
        edges=[(mapping[u],mapping[v]) for u,v in h.edges for u,v in [(u,v),(v,u)]]
        ei=torch.tensor(edges,dtype=torch.long).t().contiguous() if edges else torch.empty((2,0),dtype=torch.long)
        row_index=feature_lookup[target]
        node_x=np.concatenate([x[[lookup[v] for v in nodes]],np.repeat(zvalues[row_index:row_index+1,structural_indices],len(nodes),axis=0)],axis=1)
        cache[target]=Data(x=torch.tensor(node_x,dtype=torch.float32),edge_index=ei,y=torch.tensor([int(f.loc[target,'class']==1)],dtype=torch.float32))
    device='cuda' if torch.cuda.is_available() else 'cpu'
    out=ROOT/'results/graph';out.mkdir(parents=True,exist_ok=True)
    for seed in args.seeds:
        for backbone in args.families:
            for group,fusion in [('none','none'),('B','concat'),('P','concat'),('P','gated')]:
                name=f'{backbone}_{group}_{fusion}_seed{seed}'; report=out/f'{name}.json'
                if report.exists():continue
                torch.manual_seed(seed);np.random.seed(seed)
                cols=topo.get(group,[])
                loaders={}
                for split in ['train','validation','test']:
                    graphs=[]
                    for target in feature.index[feature.split==split]:
                        data=cache[target].clone()
                        index=feature_lookup[target]
                        data.topology=topology_tensors[group][index:index+1] if group in topology_tensors else torch.empty((1,0))
                        graphs.append(data)
                    loaders[split]=DataLoader(graphs,batch_size=args.batch_size,shuffle=split=='train',num_workers=0)
                model=TopoGraph(next(iter(cache.values())).x.shape[1],len(cols),backbone=backbone,fusion=fusion).to(device)
                optimizer=torch.optim.Adam(model.parameters(),lr=.001,weight_decay=.0001)
                best=-1; start=time.perf_counter(); history=[]
                def predict(split):
                    model.eval();ys=[];ps=[]
                    with torch.no_grad():
                        for batch in loaders[split]:
                            batch=batch.to(device); ps.extend(torch.sigmoid(model(batch)).cpu().numpy());ys.extend(batch.y.cpu().numpy())
                    return np.array(ys),np.array(ps)
                for epoch in range(args.epochs):
                    model.train()
                    for batch in loaders['train']:
                        batch=batch.to(device);optimizer.zero_grad()
                        loss=torch.nn.functional.binary_cross_entropy_with_logits(model(batch),batch.y)
                        loss.backward();optimizer.step()
                    yv,pv=predict('validation');score=metrics(yv,pv)['average_precision'];history.append(score)
                    if score>best:
                        best=score;torch.save({'model':model.state_dict(),'epoch':epoch,'seed':seed},out/f'{name}.pt')
                    print(name,epoch,'validation AP',round(score,4),flush=True)
                model.load_state_dict(torch.load(out/f'{name}.pt',weights_only=True)['model'])
                yv,pv=predict('validation');threshold=choose_threshold(yv,pv);yt,pt=predict('test')
                ids=feature.index[feature.split=='test']
                pd.DataFrame({'txId':ids,'Time step':[times[v] for v in ids],'y':yt,'probability':pt}).to_csv(out/f'{name}_predictions.csv',index=False)
                row={'name':name,'seed':seed,'backbone':backbone,'topology':group,'fusion':fusion,'epochs':args.epochs,
                     'validation_history':history,'threshold':threshold,'test':metrics(yt,pt,threshold),
                     'seconds':time.perf_counter()-start,'parameters':sum(p.numel() for p in model.parameters()),'device':device}
                report.write_text(json.dumps(row,indent=2))
                joblib_path=out/f'{name}_transforms.joblib'
                import joblib
                joblib.dump({'imputer':imputer,'scaler':scaler,'topology_scaler':zscaler,'columns':all_cols},joblib_path)

if __name__=='__main__':main()
