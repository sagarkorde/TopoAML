import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from topoaml.data import ROOT,load,graph_and_times
from topoaml.temporal import historical_neighborhood
from topoaml.topology import filtration


def main():
    f,e=load();g,times=graph_and_times(f,e)
    d=pd.concat([pd.read_csv(p) for p in sorted((ROOT/'data/processed/features_k2_n32_distance').glob('*.csv'))])
    d=d.merge(f[['txId','Time step','class']],on='txId');d=d[d['Time step']<=30]
    fig,axes=plt.subplots(2,2,figsize=(9,7))
    for dim in [0,1]:
        for label,sub in d.groupby('class'):
            columns=[f'p_h{dim}_curve_{i}' for i in range(8)]
            axes[0,dim].plot(np.linspace(0,4,8),sub[columns].mean(),'o-',label='illicit' if label==1 else 'licit')
        axes[0,dim].set(xlabel='Graph distance',ylabel=f'Mean H{dim} Betti count');axes[0,dim].legend()
    for column,label in enumerate([1,2]):
        target=int(d.loc[d['class']==label,'txId'].min())
        h,_=historical_neighborhood(g,times,target,2,32);st=filtration(h,max_nodes=32);st.compute_persistence(homology_coeff_field=2,persistence_dim_max=True)
        ax=axes[1,column];ax.plot([0,4],[0,4],color='gray',lw=1)
        counts=[]
        for dim in [0,1]:
            diagram=st.persistence_intervals_in_dimension(dim);finite=diagram[np.isfinite(diagram[:,1])]
            if len(finite):ax.scatter(finite[:,0],finite[:,1],label=f'H{dim}')
            counts.append(f'H{dim} essential: {np.isinf(diagram[:,1]).sum()}')
        ax.text(.05,.9,'; '.join(counts),transform=ax.transAxes,fontsize=9)
        ax.set(xlim=(-.1,4.1),ylim=(-.1,4.1),xlabel='Birth',ylabel='Finite death',title=f'First training ID in class {label}: {target}')
        handles,_=ax.get_legend_handles_labels()
        if handles:ax.legend()
    fig.tight_layout()
    for ext in ['svg','pdf','png']:fig.savefig(ROOT/f'results/figures/supplementary_persistence.{ext}',dpi=600,bbox_inches='tight')
    plt.close(fig)
    print('Measured training Betti curves and deterministic case diagrams exported')

if __name__=='__main__':main()
