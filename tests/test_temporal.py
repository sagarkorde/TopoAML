import networkx as nx
from topoaml.temporal import historical_neighborhood, snapshot, split_name


def test_future_neighbor_excluded():
    g = nx.DiGraph([(0,1),(1,2),(0,3),(3,4)])
    times = {0:1,1:2,2:9,3:8,4:10}
    h, _ = historical_neighborhood(g, times, 1, 3)
    assert set(h) == {0,1}
    assert set(snapshot(g,times,2)) == {0,1}


def test_bound_and_split():
    g = nx.DiGraph((0,i) for i in range(1,100))
    h, truncated = historical_neighborhood(g, {i:1 for i in g}, 0, 2, 5)
    assert len(h) == 5 and truncated
    assert [split_name(t) for t in [1,30,31,39,40,49]] == ['train','train','validation','validation','test','test']
