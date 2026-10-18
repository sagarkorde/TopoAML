"""Export actual model comparisons and paired primary uncertainty; no mock values."""
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from topoaml.data import ROOT
from topoaml.evaluation import metrics, block_bootstrap


def save(fig,name):
    directory=ROOT/'results/figures';directory.mkdir(exist_ok=True)
    for suffix in ['svg','pdf','png']:
        fig.savefig(directory/f'{name}.{suffix}',dpi=600,bbox_inches='tight')
    plt.close(fig)


def main():
    records=[]
    for family in ['tabular','graph']:
        for path in sorted((ROOT/f'results/{family}').glob('*.json')):
            r=json.loads(path.read_text())
            if 'test' not in r:continue
            records.append({'name':r['name'],'seed':r['seed'],'family':r.get('family',r.get('backbone')),
                            'group':r.get('group',r.get('topology')+'_'+r.get('fusion')) if 'group' not in r else r['group'],**r['test']})
    table=pd.DataFrame(records);table.to_csv(ROOT/'results/all_model_metrics.csv',index=False)
    summary=table.groupby(['family','group']).average_precision.agg(['mean','std','count']).reset_index()
    summary.to_csv(ROOT/'results/tables_model_summary.csv',index=False)
    a=[];b=[]
    for seed in [11,22,33,44,55]:
        pa=ROOT/f'results/tabular/xgboost_XSP_seed{seed}_predictions.csv'
        pb=ROOT/f'results/tabular/xgboost_XS_seed{seed}_predictions.csv'
        if pa.exists() and pb.exists():
            aa=pd.read_csv(pa,float_precision='round_trip');bb=pd.read_csv(pb,float_precision='round_trip')
            assert np.array_equal(aa.txId,bb.txId)
            a.append(aa.probability.to_numpy());b.append(bb.probability.to_numpy())
    if a:
        # Mean probabilities define a fixed seed ensemble; seed variability is separate.
        report=block_bootstrap(aa.y,np.mean(a,axis=0),np.mean(b,axis=0),aa['Time step'])
        report['seeds']=len(a);report['estimator']='AP difference of equal-weight seed ensembles'
        (ROOT/'results/primary_comparison.json').write_text(json.dumps(report,indent=2))
    fig,ax=plt.subplots(figsize=(8,5))
    for family,sub in summary.groupby('family'):
        ax.errorbar(sub.group,sub['mean'],yerr=sub['std'].fillna(0),marker='o',capsize=3,label=family)
    ax.set_ylabel('Illicit average precision');ax.set_xlabel('Feature configuration');ax.legend();ax.grid(alpha=.2)
    save(fig,'model_comparison')
    if a:
        aa['probability']=np.mean(a,axis=0);temporal=[]
        for step,sub in aa.groupby('Time step'):
            if sub.y.nunique()==2:
                temporal.append({'step':step,'prevalence':sub.y.mean(),**metrics(sub.y,sub.probability)})
        pd.DataFrame(temporal).to_csv(ROOT/'results/E4_temporal.csv',index=False)
        fig,ax=plt.subplots(figsize=(7,3));ax.plot([r['step'] for r in temporal],[r['average_precision'] for r in temporal],'o-')
        ax.set(xlabel='Locked future time step',ylabel='Illicit average precision');ax.grid(alpha=.2);save(fig,'temporal_generalization')
    sensitivity=ROOT/'results/E6_E7_sensitivity.csv'
    if sensitivity.exists():
        d=pd.read_csv(sensitivity);fig,axes=plt.subplots(1,2,figsize=(9,3))
        for kind,sub in d[d.perturbation=='original'].groupby('filtration'):
            means=sub.groupby('radius')[['h1_life_mean','ph_seconds']].mean()
            axes[0].plot(means.index,means.h1_life_mean,'o-',label=kind)
            axes[1].plot(means.index,means.ph_seconds*1000,'o-',label=kind)
        axes[0].set(xlabel='Radius',ylabel='Mean finite H1 lifetime');axes[1].set(xlabel='Radius',ylabel='PH milliseconds / neighborhood')
        axes[0].legend();save(fig,'sensitivity_efficiency')
    print(summary.to_string(index=False))

if __name__=='__main__':main()
