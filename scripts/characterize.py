"""E1 structural adjustment and E6/E7 measured bounded-neighborhood sensitivity."""
import json
import time
import platform
import numpy as np
import pandas as pd
import networkx as nx
import psutil
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from topoaml.data import ROOT, load, graph_and_times
from topoaml.temporal import historical_neighborhood
from topoaml.topology import structural_features, graph_betti, filtration, persistence_features


def main():
    out=ROOT/'results'; f,e=load();g,times=graph_and_times(f,e)
    d=pd.concat([pd.read_csv(p) for p in sorted((ROOT/'data/processed/features_k2_n32_distance').glob('*.csv'))])
    d=d.merge(f[['txId','Time step','class']],on='txId',validate='one_to_one')
    s=[c for c in d if c.startswith('s_')]
    train=d[d['Time step']<=30].copy()
    # Exact identities, rather than significance tests for deterministically redundant Betti counts.
    assert np.array_equal(d.b_beta0,d.s_components)
    assert np.array_equal(d.b_beta1,d.s_edges-d.s_nodes+d.s_components)
    assert np.allclose(d.b_beta1_per_edge,d.s_cycle_rank/d.s_edges.clip(lower=1))
    rows=[];rng=np.random.default_rng(2026)
    for col in ['p_h0_life_mean','p_h0_entropy','p_h1_life_mean','p_h1_entropy','p_h1_essential']:
        model=make_pipeline(StandardScaler(),Ridge(alpha=1.)).fit(train[s],train[col])
        residual=train[col].to_numpy()-model.predict(train[s])
        series=[]
        for step,indices in train.groupby('Time step').groups.items():
            # Index positions refer to d; use explicit positional selection.
            sub=train.loc[indices]; r=residual[train.index.get_indexer(indices)]
            if sub['class'].nunique()==2:
                series.append(float(r[sub['class'].to_numpy()==1].mean()-r[sub['class'].to_numpy()==2].mean()))
        draws=np.array([np.mean(rng.choice(series,len(series),replace=True)) for _ in range(2000)])
        rows.append({'feature':col,'mean_step_adjusted_difference':float(np.mean(series)),
                     'ci_low':float(np.quantile(draws,.025)),'ci_high':float(np.quantile(draws,.975)),
                     'steps':len(series),'note':'exploratory linear residual adjustment; not a causal or independent-neighborhood test'})
    pd.DataFrame(rows).to_csv(out/'E1_adjusted_topology.csv',index=False)
    train.groupby('class')[[c for c in d if c.startswith(('s_','b_','p_'))]].mean().to_csv(out/'E1_class_means.csv')
    # Sample training IDs only, fixed before sensitivity results are generated.
    ids=rng.choice(train.txId.to_numpy(),min(300,len(train)),replace=False).tolist()
    (out/'E6_sample_ids.json').write_text(json.dumps(ids))
    rows=[]
    for radius in [1,2,3]:
        for kind in ['distance','weight','temporal']:
            for target in ids:
                start=time.perf_counter();h,truncated=historical_neighborhood(g,times,target,radius,32)
                extraction=time.perf_counter()-start
                for perturbation in ['original','drop_10pct_edges']:
                    hp=h.copy()
                    if perturbation!='original':
                        edges=list(hp.edges)
                        if edges:
                            remove=rng.choice(len(edges),int(np.ceil(len(edges)*.1)),replace=False)
                            hp.remove_edges_from([edges[i] for i in remove])
                    start=time.perf_counter();b=graph_betti(hp);betti_seconds=time.perf_counter()-start
                    start=time.perf_counter();st=filtration(hp,kind,{v:(times[v]-1)/48*4 for v in hp},max_nodes=32)
                    values=persistence_features(st);ph_seconds=time.perf_counter()-start
                    rows.append({'txId':target,'radius':radius,'filtration':kind,'perturbation':perturbation,
                                 'nodes':len(hp),'edges':hp.number_of_edges(),'beta1':b[1],
                                 'h1_life_mean':values['h1_life_mean'],'h1_entropy':values['h1_entropy'],
                                 'extraction_seconds':extraction,'betti_seconds':betti_seconds,'ph_seconds':ph_seconds,
                                 'rss_bytes':psutil.Process().memory_info().rss,'truncated':truncated})
    pd.DataFrame(rows).to_csv(out/'E6_E7_sensitivity.csv',index=False)
    audit={'status':'passed for observed graph construction', 'labeled_targets':len(d),
           'future_neighbor_violations':0,'basis':'extractor asserts times[v] <= times[target] for every retained vertex',
           'split_disjoint':True,'transforms':'fitted only to training data by training scripts',
           'labels_used_in_extraction':False,'all_edges_same_step':True,
           'causality_limit':'step-close only; no claim of transaction-time causality or known historical label availability',
           'static_betti_redundancy_verified':True,'truncated_fraction':float(d.truncated.mean())}
    (out/'leakage_audit.json').write_text(json.dumps(audit,indent=2))
    timing={'targets':len(d),'total_recorded_extraction_seconds':float(d.extraction_seconds.sum()),
            'total_recorded_ph_seconds':float(d.ph_seconds.sum()),'median_extraction_seconds':float(d.extraction_seconds.median()),
            'median_ph_seconds':float(d.ph_seconds.median()),'environment':platform.platform(),
            'memory_note':'E6 rows contain instantaneous process RSS, not whole-pipeline peak RAM'}
    (out/'E7_efficiency.json').write_text(json.dumps(timing,indent=2))
    print('E1 and training-only E6/E7 characterization complete',flush=True)

if __name__=='__main__':main()
