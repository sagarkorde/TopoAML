from itertools import combinations
import networkx as nx
import numpy as np
import pytest
from topoaml.topology import graph_betti, graph_complex, betti, simplex_tree, filtration, audit_filtration, persistence_features


@pytest.mark.parametrize("g,expected", [
    (nx.Graph(), (0,0,0)), (nx.empty_graph(1), (1,0,0)),
    (nx.empty_graph(3), (3,0,0)), (nx.path_graph(5), (1,0,0)),
    (nx.balanced_tree(2,3), (1,0,0)), (nx.cycle_graph(4), (1,1,0)),
    (nx.disjoint_union(nx.cycle_graph(4), nx.cycle_graph(5)), (2,2,0)),
    (nx.cycle_graph(3), (1,1,0))])
def test_graph_invariants(g, expected):
    assert graph_betti(g) == expected
    assert betti(graph_complex(g)) == expected
    assert len(nx.cycle_basis(g)) == expected[1]


def test_filled_triangle():
    assert betti(graph_complex(nx.complete_graph(3), flag=True)) == (1,0,0)


def test_hollow_and_filled_tetrahedron():
    faces = [(list(s), 0) for s in combinations(range(4), 3)]
    assert betti(simplex_tree(faces)) == (1,0,1)
    assert betti(simplex_tree([([0,1,2,3], 0)])) == (1,0,0)


def test_known_weighted_persistence():
    st = simplex_tree([([0],0),([1],0),([2],0),([0,1],1),([1,2],2),([0,2],3),([0,1,2],4)])
    st.compute_persistence(persistence_dim_max=True)
    np.testing.assert_allclose(st.persistence_intervals_in_dimension(1), [[3,4]])
    assert audit_filtration(st)


def test_dag_with_undirected_cycle():
    g = nx.DiGraph([(0,1),(0,2),(1,3),(2,3)])
    assert nx.is_directed_acyclic_graph(g)
    assert graph_betti(g) == (1,1,0)


@pytest.mark.parametrize("kind", ["distance", "weight", "temporal"])
def test_nestedness(kind):
    st = filtration(nx.cycle_graph(4), kind, dict(enumerate([1,2,3,4])))
    assert audit_filtration(st)
    assert all(np.isfinite(v) for v in persistence_features(st).values())


def test_boundary_squared_zero():
    # Explicit mod-2 cancellation of codimension-2 faces of a tetrahedron.
    for simplex in ([0,1,2], [0,1,2,3]):
        counts = {}
        for face in combinations(simplex, len(simplex)-1):
            for edge in combinations(face, len(face)-1):
                counts[edge] = counts.get(edge, 0) + 1
        assert all(x % 2 == 0 for x in counts.values())
