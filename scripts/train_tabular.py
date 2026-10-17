"""Matched conventional models; model selection never inspects test metrics."""
import json
import time
import argparse
import platform
import importlib.metadata
import joblib
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from topoaml.data import ROOT, SAFE_FIELDS, load
from topoaml.temporal import split_name
from topoaml.evaluation import metrics, choose_threshold


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--seeds',type=int,nargs='+',default=[11,22,33,44,55]); args=parser.parse_args()
    f,_=load()
    paths=sorted((ROOT/'data/processed/features_k2_n32_distance').glob('*.csv'))
    features=pd.concat([pd.read_csv(p) for p in paths],ignore_index=True)
    d=f.merge(features,on='txId',validate='one_to_one').sort_values('txId').reset_index(drop=True)
    if len(d)!=46564:raise ValueError('Incomplete extraction')
    d['split']=d['Time step'].map(split_name); d['y']=(d['class']==1).astype(int)
    groups={'X':SAFE_FIELDS,'XS':SAFE_FIELDS+[c for c in d if c.startswith('s_')],
            'XB':SAFE_FIELDS+[c for c in d if c.startswith('b_')],
            'XSB':SAFE_FIELDS+[c for c in d if c.startswith(('s_','b_'))],
            'XSP':SAFE_FIELDS+[c for c in d if c.startswith(('s_','p_'))]}
    out=ROOT/'results/tabular'; out.mkdir(parents=True,exist_ok=True)
    train=d.split=='train'; val=d.split=='validation'; test=d.split=='test'
    results=[]
    for seed in args.seeds:
        for family in ['logistic','random_forest','xgboost']:
            for group,columns in groups.items():
                name=f'{family}_{group}_seed{seed}'
                summary=out/f'{name}.json'
                if summary.exists():results.append(json.loads(summary.read_text())); continue
                start=time.perf_counter()
                if family=='logistic':
                    model=LogisticRegression(max_iter=2000,class_weight='balanced',random_state=seed)
                elif family=='random_forest':
                    model=RandomForestClassifier(n_estimators=200,max_depth=12,min_samples_leaf=3,class_weight='balanced',n_jobs=6,random_state=seed)
                else:
                    model=XGBClassifier(n_estimators=200,max_depth=4,learning_rate=.05,subsample=.9,colsample_bytree=.9,n_jobs=6,random_state=seed,eval_metric='logloss',tree_method='hist')
                pipe=make_pipeline(SimpleImputer(strategy='median',add_indicator=True),StandardScaler(),model)
                pipe.fit(d.loc[train,columns],d.loc[train,'y'])
                fit_seconds=time.perf_counter()-start
                pv=pipe.predict_proba(d.loc[val,columns])[:,1]
                threshold=choose_threshold(d.loc[val,'y'],pv)
                start=time.perf_counter(); pt=pipe.predict_proba(d.loc[test,columns])[:,1]; inference=time.perf_counter()-start
                row={'name':name,'family':family,'group':group,'seed':seed,'threshold':threshold,
                     'fit_seconds':fit_seconds,'inference_seconds':inference,'features':columns,
                     'validation':metrics(d.loc[val,'y'],pv,threshold),'test':metrics(d.loc[test,'y'],pt,threshold)}
                summary.write_text(json.dumps(row,indent=2)); joblib.dump(pipe,out/f'{name}.joblib')
                pred=d.loc[test,['txId','Time step','y']].copy(); pred['probability']=pt; pred.to_csv(out/f'{name}_predictions.csv',index=False)
                results.append(row); print(name,'done',flush=True)
    table=pd.DataFrame([{'model':r['family'],'features':r['group'],'seed':r['seed'],**r['test']} for r in results])
    table.to_csv(ROOT/'results/model_comparison.csv',index=False)
    environment={'python':platform.python_version(),'platform':platform.platform(),'packages':{p:importlib.metadata.version(p) for p in ['numpy','pandas','scikit-learn','xgboost','torch','torch-geometric','gudhi']}}
    (ROOT/'results/environment.json').write_text(json.dumps(environment,indent=2))

if __name__=='__main__':main()
