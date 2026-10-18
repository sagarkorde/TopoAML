import networkx as nx
import numpy as np
from sklearn.impute import SimpleImputer
from topoaml.temporal import historical_neighborhood
from topoaml.topology import filtration,persistence_features


def test_future_edges_cannot_change_historical_topology():
    a=nx.DiGraph([(0,1),(1,2),(0,2)])
    b=a.copy();b.add_edges_from([(2,3),(3,4),(4,0)])
    times={0:1,1:1,2:1,3:9,4:10}
    ha,_=historical_neighborhood(a,times,2)
    hb,_=historical_neighborhood(b,times,2)
    assert set(ha)==set(hb) and set(ha.edges)==set(hb.edges)
    assert persistence_features(filtration(ha))==persistence_features(filtration(hb))


def test_training_only_missing_value_transform():
    train=np.array([[1.],[3.],[np.nan]])
    transform=SimpleImputer(strategy='median').fit(train)
    np.testing.assert_array_equal(transform.statistics_,[2.])
    transform.transform([[1e9],[np.nan]])
    np.testing.assert_array_equal(transform.statistics_,[2.])
