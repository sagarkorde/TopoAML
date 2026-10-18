"""Descriptive secondary comparisons, task-specific external summary and drift."""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from topoaml.data import ROOT,load,SAFE_FIELDS
from topoaml.evaluation import block_bootstrap


def ensemble_pair(directory,aname,bname,unit='txId',blocks='Time step',repetitions=1000):
    aa=[];bb=[]
    for seed in [11,22,33,44,55]:
        a=directory/f'{aname}_seed{seed}_predictions.csv';b=directory/f'{bname}_seed{seed}_predictions.csv'
        if not a.exists() or not b.exists():continue
        da=pd.read_csv(a,float_precision='round_trip');db=pd.read_csv(b,float_precision='round_trip');assert np.array_equal(da[unit],db[unit])
        aa.append(da.probability.to_numpy());bb.append(db.probability.to_numpy())
    if len(aa)!=5:return None
    grouping=da[blocks] if blocks in da else da[unit]
    report=block_bootstrap(da.y,np.mean(aa,axis=0),np.mean(bb,axis=0),grouping,repetitions=repetitions)
    report.update(comparison=f'{aname} minus {bname}',seeds=5,kind='secondary descriptive; no multiplicity-adjusted superiority claim')
    return report


def main():
    reports=[]
    for a,b in [('xgboost_XSB','xgboost_XS'),('xgboost_XB','xgboost_X'),('random_forest_XSP','random_forest_XS')]:
        result=ensemble_pair(ROOT/'results/tabular',a,b)
        if result:reports.append(result)
    for backbone in ['sage','gat']:
        for a,b in [(f'{backbone}_P_concat',f'{backbone}_none_none'),(f'{backbone}_P_gated',f'{backbone}_P_concat')]:
            result=ensemble_pair(ROOT/'results/graph',a,b)
            if result:reports.append(result)
    (ROOT/'results/E3_secondary_comparisons.json').write_text(json.dumps(reports,indent=2))
    external=[]
    for path in sorted((ROOT/'results/elliptic2').glob('*.json')):
        r=json.loads(path.read_text());external.append({'family':r['family'],'group':r['group'],'seed':r['seed'],**r['test']})
    if external:
        table=pd.DataFrame(external);table.to_csv(ROOT/'results/E5_metrics.csv',index=False)
        summary=table.groupby(['family','group']).average_precision.agg(['mean','std','count']).reset_index()
        summary.to_csv(ROOT/'results/E5_summary.csv',index=False)
        # Subgraphs are the external evaluation units, not Elliptic time steps.
        # Bootstrap individually; source dependence beyond shared-node audit remains.
        from sklearn.metrics import average_precision_score
        rng=np.random.default_rng(2026);external_intervals=[]
        for family in ['random_forest','xgboost']:
            aa=[];bb=[]
            for seed in [11,22,33,44,55]:
                a=pd.read_csv(ROOT/f'results/elliptic2/{family}_SP_seed{seed}_predictions.csv',float_precision='round_trip')
                b=pd.read_csv(ROOT/f'results/elliptic2/{family}_S_seed{seed}_predictions.csv',float_precision='round_trip')
                assert np.array_equal(a.ccId,b.ccId);aa.append(a.probability.to_numpy());bb.append(b.probability.to_numpy())
            pa=np.mean(aa,axis=0);pb=np.mean(bb,axis=0);y=a.y.to_numpy();diff=[]
            positive=np.flatnonzero(y==1);negative=np.flatnonzero(y==0)
            for _ in range(1000):
                idx=np.r_[rng.choice(positive,len(positive),replace=True),rng.choice(negative,len(negative),replace=True)]
                diff.append(average_precision_score(y[idx],pa[idx])-average_precision_score(y[idx],pb[idx]))
            external_intervals.append({'family':family,'delta':float(average_precision_score(y,pa)-average_precision_score(y,pb)),
                                       'ci95':np.quantile(diff,[.025,.975]).tolist(),'scope':'paired stratified subgraph bootstrap; conditional on class counts and fitted models; no shared nodes, broader source dependence unresolved'})
        (ROOT/'results/E5_comparison.json').write_text(json.dumps(external_intervals,indent=2))
    f,_=load();train=f.loc[(f['Time step']<=30)&f['class'].isin([1,2]),SAFE_FIELDS]
    mean=train.mean();std=train.std().replace(0,np.nan)
    drift=[]
    for step,sub in f[(f['Time step']>=40)&f['class'].isin([1,2])].groupby('Time step'):
        shift=((sub[SAFE_FIELDS].mean()-mean)/std).abs()
        drift.append({'time_step':step,'mean_abs_standardized_shift':float(shift.mean()),'positive_prevalence':float((sub['class']==1).mean())})
    pd.DataFrame(drift).to_csv(ROOT/'results/E4_feature_drift.csv',index=False)
    # E1 distributions and diagrams are actual training-set measurements.
    d=pd.concat([pd.read_csv(p) for p in sorted((ROOT/'data/processed/features_k2_n32_distance').glob('*.csv'))])
    d=d.merge(f[['txId','Time step','class']],on='txId');d=d[d['Time step']<=30]
    fig,axes=plt.subplots(1,2,figsize=(9,3))
    for label,sub in d.groupby('class'):
        axes[0].hist(sub.p_h1_life_mean,bins=30,alpha=.45,density=True,label='illicit' if label==1 else 'licit')
        axes[1].hist(sub.s_cycle_rank,bins=30,alpha=.45,density=True,label='illicit' if label==1 else 'licit')
    axes[0].set(xlabel='Mean finite H1 lifetime',ylabel='Training density');axes[1].set(xlabel='Cycle rank',ylabel='Training density')
    axes[0].legend()
    for extension in ['svg','pdf','png']:fig.savefig(ROOT/f'results/figures/training_topology.{extension}',dpi=600,bbox_inches='tight')
    plt.close(fig)
    print('Secondary analyses exported; descriptive comparisons only')

if __name__=='__main__':main()
