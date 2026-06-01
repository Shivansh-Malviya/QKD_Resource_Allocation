"""Network topology utilities for QKD-enabled ODCN demonstrations."""

from __future__ import annotations

from typing import Dict, Iterable, List, Tuple
import networkx as nx


def create_topology(edges: Iterable[Tuple[int, int, float]]) -> nx.Graph:
    """Create an undirected weighted graph from ``(u, v, weight)`` edges."""
    graph = nx.Graph()
    graph.add_weighted_edges_from(edges)
    return graph


def create_bi_topology(edges: Iterable[Tuple[int, int, float]]) -> nx.DiGraph:
    """Create a directed weighted graph from ``(u, v, weight)`` edges."""
    graph = nx.DiGraph()
    graph.add_weighted_edges_from(edges)
    return graph


def k_shortest_paths(
    graph: nx.Graph | nx.DiGraph,
    source: int,
    target: int,
    k: int = 3,
) -> List[List[int]]:
    """Return up to ``k`` shortest simple paths between two nodes."""
    try:
        paths = list(
            nx.shortest_simple_paths(
                graph,
                source=source,
                target=target,
                weight="weight",
            )
        )
    except nx.NetworkXNoPath:
        return []
    return paths[:k]


def compute_k_sp_all(
    graph: nx.Graph | nx.DiGraph,
    k: int = 3,
) -> Dict[Tuple[int, int], Dict[Tuple[int, ...], float]]:
    """Compute k-shortest path cost dictionaries for all ordered pairs."""
    path_costs: Dict[Tuple[int, int], Dict[Tuple[int, ...], float]] = {}
    nodes = list(graph.nodes)
    for source in nodes:
        for target in nodes:
            if source == target:
                continue
            costs: Dict[Tuple[int, ...], float] = {}
            for path in k_shortest_paths(graph, source, target, k):
                cost = sum(graph[u][v]["weight"] for u, v in zip(path, path[1:]))
                costs[tuple(path)] = cost
            path_costs[(source, target)] = costs
    return path_costs
