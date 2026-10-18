"""Deterministic case perturbations and genuine tree contribution values."""
import json
import joblib
import numpy as np
import pandas as pd
import xgboost as xgb
import networkx as nx
from topoaml.data import ROOT, SAFE_FIELDS, load, graph_and_times
from topoaml.temporal import historical_neighborhood
from topoaml.topology import structural_features, graph_betti, filtration, persistence_features


def main():
    f,e=load();g,times=graph_and_times(f,e); f=f.set_index('txId')
    model_path=ROOT/'results/tabular/xgboost_XSP_seed11.joblib'
    pipe=joblib.load(model_path)
    info=json.loads(model_path.with_suffix('.json').read_text());columns=info['features']
    targets=sorted(f.index[(f['Time step']>=40)&f['class'].isin([1,2])])[:10]
    rows=[];contributions=[]
    for target in targets:
        h,_=historical_neighborhood(g,times,target,2,32)
        alternatives={'observed':h,'remove_first_edge':h.copy()}
        if h.number_of_edges():alternatives['remove_first_edge'].remove_edge(*sorted(h.edges)[0])
        for variant,graph in alternatives.items():
            features={c:f.loc[target,c] for c in SAFE_FIELDS}
            features.update({'s_'+k:v for k,v in structural_features(graph).items()})
            features.update({'p_'+k:v for k,v in persistence_features(filtration(graph,max_nodes=32)).items()})
            frame=pd.DataFrame([features])[columns]
            probability=float(pipe.predict_proba(frame)[0,1])
            rows.append({'txId':target,'variant':variant,'probability':probability,'nodes':len(graph),'edges':graph.number_of_edges(),
                         'label':int(f.loc[target,'class']), 'note':'model sensitivity only; edge removal is not a causal laundering intervention'})
            if variant=='observed':
                transformed=pipe[:-1].transform(frame)
                contribution=pipe[-1].get_booster().predict(xgb.DMatrix(transformed),pred_contribs=True)[0]
                # Imputer appends missing-value indicators; preserve generated names.
                names=pipe[0].get_feature_names_out(columns).tolist()+['bias']
                for name,value in zip(names,contribution):contributions.append({'txId':target,'feature':name,'log_odds_contribution':float(value)})
    pd.DataFrame(rows).to_csv(ROOT/'results/case_perturbations.csv',index=False)
    pd.DataFrame(contributions).to_csv(ROOT/'results/case_tree_contributions.csv',index=False)
    print('10 deterministic test cases analyzed; no case selection by outcome')

if __name__=='__main__':main()
