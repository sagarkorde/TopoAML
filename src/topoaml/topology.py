"""Explicit graph/flag complexes and causal, nested filtrations over F_2."""
from itertools import combinations
import gudhi
import networkx as nx
import numpy as np


def graph_betti(graph):
    g = nx.Graph(graph)
    g.remove_edges_from(nx.selfloop_edges(g))
    c = nx.number_connected_components(g)
    return c, g.number_of_edges() - len(g) + c, 0


def simplex_tree(simplices):
    st = gudhi.SimplexTree()
    for simplex, value in simplices:
        st.insert(simplex, filtration=float(value))
    st.make_filtration_non_decreasing()
    return st


def betti(st):
    st.compute_persistence(homology_coeff_field=2, persistence_dim_max=True)
    values = st.betti_numbers()
    return tuple((values + [0, 0, 0])[:3])


def graph_complex(graph, flag=False):
    g = nx.convert_node_labels_to_integers(nx.Graph(graph))
    g.remove_edges_from(nx.selfloop_edges(g))
    st = simplex_tree([([v], 0) for v in g] + [(list(e), 0) for e in g.edges])
    if flag:
        # Include dimension 3 so tetrahedra can kill H2.
        st.expansion(3)
    return st


def filtration(graph, kind="distance", node_times=None, max_scale=4.0, max_nodes=128):
    """Undirected filtrations; all edge weights are derived, never transfer values.

    distance: shortest-path Rips, f(edge)=distance, flag extension by max.
    weight: original edges, f(edge)=1/(1+common neighbors), vertices at 0.
    temporal: original edges at max(endpoint observation times), flag extension.
    """
    if len(graph) > max_nodes:
        raise ValueError("Neighborhood exceeds configured complexity bound")
    nodes = sorted(graph.nodes)
    mapping = {v: i for i, v in enumerate(nodes)}
    g = nx.relabel_nodes(nx.Graph(graph), mapping)
    g.remove_edges_from(nx.selfloop_edges(g))
    if kind == "temporal" and node_times is None:
        raise ValueError("Temporal filtration requires node observation times")
    times = {mapping[v]: float(node_times[v]) for v in nodes} if node_times is not None else {}
    st = gudhi.SimplexTree()
    for v in g:
        st.insert([v], filtration=times[v] if kind == "temporal" else 0)
    if kind == "distance":
        for u, lengths in nx.all_pairs_shortest_path_length(g, cutoff=int(max_scale)):
            for v, d in lengths.items():
                if u < v and d <= max_scale:
                    st.insert([u, v], filtration=float(d))
    elif kind in {"weight", "temporal"}:
        for u, v in g.edges:
            value = max(times[u], times[v]) if kind == "temporal" else 1 / (1 + len(list(nx.common_neighbors(g, u, v))))
            st.insert([u, v], filtration=value)
    else:
        raise ValueError(kind)
    # H0 and H1 require faces through dimension 2. H2 is not extracted here.
    st.expansion(2)
    audit_filtration(st)
    return st


def audit_filtration(st):
    values = {tuple(s): a for s, a in st.get_filtration()}
    for s, a in values.items():
        for face in combinations(s, len(s) - 1):
            if face and values[face] > a:
                raise ValueError("Face appears after coface")
    return True


def persistence_features(st, horizon=4.0, bins=8):
    """Fixed grids need no held-out fit. Infinite bars counted separately.

    Finite lifetimes alone enter entropy/images. Essential intervals enter Betti
    curves through the fixed horizon and are never assigned invented deaths.
    """
    st.compute_persistence(homology_coeff_field=2, persistence_dim_max=True)
    out = {}
    for dim in (0, 1):
        diagram = st.persistence_intervals_in_dimension(dim)
        finite = diagram[np.isfinite(diagram[:, 1])] if len(diagram) else np.empty((0, 2))
        lifetimes = finite[:, 1] - finite[:, 0]
        positive = lifetimes[lifetimes > 0]
        probs = positive / positive.sum() if len(positive) else np.array([])
        prefix = f"h{dim}_"
        out.update({prefix + "finite_count": len(positive), prefix + "essential": int(np.isinf(diagram[:, 1]).sum()) if len(diagram) else 0,
                    prefix + "life_mean": float(positive.mean()) if len(positive) else 0.,
                    prefix + "life_max": float(positive.max()) if len(positive) else 0.,
                    prefix + "entropy": float(-(probs * np.log(probs)).sum()) if len(probs) else 0.})
        grid = np.linspace(0, horizon, bins)
        for i, t in enumerate(grid):
            out[prefix + f"curve_{i}"] = int(((diagram[:, 0] <= t) & (diagram[:, 1] > t)).sum()) if len(diagram) else 0
        # Fixed Gaussian persistence image over birth/lifetime coordinates.
        for i, birth in enumerate(np.linspace(0, horizon, 4)):
            for j, life in enumerate(np.linspace(0, horizon, 4)):
                out[prefix + f"image_{i}_{j}"] = float(np.sum(lifetimes * np.exp(-((finite[:, 0] - birth)**2 + (lifetimes - life)**2) / .5)))
    return out


def structural_features(graph):
    g = nx.Graph(graph)
    n, m = len(g), g.number_of_edges()
    b0, b1, _ = graph_betti(g)
    degrees = np.array([d for _, d in g.degree()], dtype=float)
    return {"nodes": n, "edges": m, "components": b0, "density": nx.density(g),
            "degree_mean": float(degrees.mean()) if n else 0., "degree_std": float(degrees.std()) if n else 0.,
            "degree_max": float(degrees.max()) if n else 0., "triangles": sum(nx.triangles(g).values()) / 3,
            "clustering": nx.average_clustering(g) if n else 0., "cycle_rank": b1}
