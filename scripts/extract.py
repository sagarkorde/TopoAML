"""Resumable bounded target-centered features. No labels passed to extractor."""
import argparse
import json
import time
from pathlib import Path
import pandas as pd
from topoaml.data import ROOT, load, graph_and_times
from topoaml.temporal import historical_neighborhood
from topoaml.topology import structural_features, filtration, persistence_features, graph_betti


def main():
    p=argparse.ArgumentParser(); p.add_argument('--radius',type=int,default=2); p.add_argument('--max-nodes',type=int,default=32)
    p.add_argument('--filtration',choices=['distance','weight','temporal'],default='distance')
    args=p.parse_args()
    f,e=load(); g,times=graph_and_times(f,e)
    directory=ROOT/f'data/processed/features_k{args.radius}_n{args.max_nodes}_{args.filtration}'
    directory.mkdir(parents=True,exist_ok=True)
    targets=f.loc[f['class'].isin([1,2]),'txId'].sort_values().tolist()
    start=time.perf_counter()
    for i in range(0,len(targets),500):
        path=directory/f'{i:06}.csv'
        if path.exists(): continue
        rows=[]
        for target in targets[i:i+500]:
            before=time.perf_counter()
            h,truncated=historical_neighborhood(g,times,target,args.radius,args.max_nodes)
            assert all(times[v]<=times[target] for v in h)
            row={'txId':target,'observation_time':times[target],'truncated':int(truncated)}
            row.update({'s_'+k:v for k,v in structural_features(h).items()})
            b0,b1,_=graph_betti(h)
            row.update(b_beta0=b0,b_beta1=b1,b_beta1_per_edge=b1/max(h.number_of_edges(),1))
            relative_times={v:(times[v]-1)/48*4 for v in h}
            ph_start=time.perf_counter()
            st=filtration(h,args.filtration,relative_times,max_nodes=args.max_nodes)
            row.update({'p_'+k:v for k,v in persistence_features(st).items()})
            row['ph_seconds']=time.perf_counter()-ph_start
            row['extraction_seconds']=time.perf_counter()-before
            rows.append(row)
        temporary=path.with_suffix('.part'); pd.DataFrame(rows).to_csv(temporary,index=False); temporary.replace(path)
        print(f'{min(i+500,len(targets))}/{len(targets)} elapsed={time.perf_counter()-start:.1f}s',flush=True)
    (directory/'config.json').write_text(json.dumps(vars(args),indent=2))

if __name__=='__main__':main()
