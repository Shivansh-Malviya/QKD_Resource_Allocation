"""
Resource allocation heuristics for QKD-ODCN demonstrations.

This module implements a deliberately simplified first-fit strategy. It is not
the full thesis algorithm.
"""

from __future__ import annotations

from typing import Dict, List, Tuple
import networkx as nx

from .connection_request import ConnectionRequest


def _edge_key(graph: nx.Graph | nx.DiGraph, u: int, v: int) -> Tuple[int, int]:
    if isinstance(graph, nx.DiGraph):
        return (u, v)
    return tuple(sorted((u, v)))


def allocate_first_fit(
    graph: nx.Graph | nx.DiGraph,
    requests: List[ConnectionRequest],
    k_sp_dict: Dict[Tuple[int, int], Dict[Tuple[int, ...], float]],
    qsc_capacity: int = 1,
    ts_capacity: int = 1,
) -> None:
    """Allocate requests using a simple first-fit path/resource model."""
    resource_state: Dict[Tuple[int, int], Dict[str, int]] = {}
    for u, v in graph.edges:
        resource_state[_edge_key(graph, u, v)] = {
            "qsc": qsc_capacity,
            "ts": ts_capacity,
        }

    for request in requests:
        candidate_paths = k_sp_dict.get((request.source, request.destination), {})
        allocated = False

        for path_tuple in candidate_paths.keys():
            path = list(path_tuple)
            can_allocate = True

            for u, v in zip(path, path[1:]):
                key = _edge_key(graph, u, v)
                if resource_state[key]["qsc"] < 1 or resource_state[key]["ts"] < 1:
                    can_allocate = False
                    break

            if not can_allocate:
                continue

            for u, v in zip(path, path[1:]):
                key = _edge_key(graph, u, v)
                resource_state[key]["qsc"] -= 1
                resource_state[key]["ts"] -= 1
            request.update_status(
                status="allocated",
                allocated_resources=(1, 1),
                path=path,
            )
            allocated = True
            break

        if not allocated:
            request.update_status(
                status="blocked",
                allocated_resources=(None, None),
                path=None,
            )
