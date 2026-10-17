"""Historical graph observation; no test labels used in graph construction."""
from collections import deque
import networkx as nx


def snapshot(graph, times, observation_time):
    # Edges assumed observable when both endpoints exist. Coarse steps do not
    # establish within-step causality; this is explicitly a step-close protocol.
    return graph.subgraph(v for v in graph if times[v] <= observation_time).copy()


def historical_neighborhood(graph, times, target, radius=2, max_nodes=64):
    if radius not in (1, 2, 3) or max_nodes < 1:
        raise ValueError("Invalid radius/node bound")
    t = times[target]
    seen, queue = {target}, deque([(target, 0)])
    truncated = False
    while queue:
        u, depth = queue.popleft()
        if depth == radius:
            continue
        neighbors = set(graph.predecessors(u)) | set(graph.successors(u)) if graph.is_directed() else set(graph.neighbors(u))
        eligible = [v for v in sorted(neighbors) if v not in seen and times[v] <= t]
        for v in eligible:
            if len(seen) >= max_nodes:
                truncated = True
                continue
            seen.add(v); queue.append((v, depth + 1))
    return graph.subgraph(seen).copy(), truncated


def split_name(t):
    if not 1 <= t <= 49:
        raise ValueError("Unrecognized observation step")
    return "train" if t <= 30 else "validation" if t <= 39 else "test"
