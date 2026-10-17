import hashlib
import json
from pathlib import Path
import networkx as nx
import numpy as np
import pandas as pd
from .temporal import split_name

ROOT = Path(__file__).resolve().parents[2]
SAFE_FIELDS = ['total_BTC','fees','size','num_input_addresses','num_output_addresses',
               'in_BTC_min','in_BTC_max','in_BTC_mean','in_BTC_median','in_BTC_total',
               'out_BTC_min','out_BTC_max','out_BTC_mean','out_BTC_median','out_BTC_total']


def load():
    raw = ROOT / 'data/raw/ellipticpp'
    f = pd.read_csv(raw/'txs_features.csv', usecols=['txId','Time step']+SAFE_FIELDS)
    c = pd.read_csv(raw/'txs_classes.csv')
    e = pd.read_csv(raw/'txs_edgelist.csv')
    if f.txId.duplicated().any() or c.txId.duplicated().any():
        raise ValueError('Duplicate IDs')
    f = f.merge(c, on='txId', validate='one_to_one')
    if len(f) != 203769 or len(e) != 234355:
        raise ValueError('Upstream counts changed')
    if set(f['class']) != {1,2,3} or set(f['Time step']) != set(range(1,50)):
        raise ValueError('Labels/times incompatible')
    ids = set(f.txId)
    if not set(e.txId1).union(e.txId2).issubset(ids):
        raise ValueError('Dangling edge')
    # Missing on-chain fields are retained and imputed using training medians.
    if np.isinf(f[SAFE_FIELDS].to_numpy()).any():
        raise ValueError('Infinite predictors')
    return f, e


def graph_and_times(f, e):
    g = nx.DiGraph()
    g.add_nodes_from(f.txId.astype(int))
    g.add_edges_from(e.itertuples(index=False, name=None))
    return g, dict(zip(f.txId, f['Time step']))


def validate_and_freeze():
    f,e=load()
    out=ROOT/'data/processed'; out.mkdir(exist_ok=True,parents=True)
    f['split'] = f['Time step'].map(split_name)
    split=f[['txId','Time step','class','split']].sort_values('txId')
    payload=split.to_csv(index=False).encode()
    path=out/'split_ids.csv'
    if path.exists() and path.read_bytes()!=payload:
        raise ValueError('Frozen partitions would change')
    path.write_bytes(payload)
    g,times=graph_and_times(f,e)
    report={'dataset':'Elliptic++ transaction release', 'samples':len(f),'nodes':len(g),'edges':len(e),
            'labels':f['class'].value_counts().to_dict(), 'missing':int(f.isna().sum().sum()),
            'time_steps':[int(f['Time step'].min()),int(f['Time step'].max())],
            'split_counts':f.groupby(['split','class']).size().unstack(fill_value=0).to_dict(),
            'split_sha256':hashlib.sha256(payload).hexdigest(),'dag':nx.is_directed_acyclic_graph(g),
            'backward_time_edges':sum(times[u]>times[v] for u,v in g.edges),
            'same_step_edges':sum(times[u]==times[v] for u,v in g.edges),
            'feature_policy':SAFE_FIELDS,'limitations':['Opaque and aggregate features excluded; upstream normalization cannot be reconstructed.',
            'Original Elliptic overlap: not an independent replication.','No within-step observation or label-availability timestamps.',
            'Dataset license not verified; raw files excluded from Git.']}
    report['acquisition']=json.loads((ROOT/'data/manifests/acquisition.json').read_text())
    (ROOT/'data/manifests/dataset_manifest.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({k:v for k,v in report.items() if k!='acquisition'},indent=2))
    return f,e
