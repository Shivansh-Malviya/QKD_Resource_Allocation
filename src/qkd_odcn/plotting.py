"""Plotting helpers for QKD-ODCN demonstrations."""

from __future__ import annotations

from typing import Iterable, List

import matplotlib.pyplot as plt
import networkx as nx


def plot_topology(
    graph: nx.Graph | nx.DiGraph,
    path: Iterable[int] | None = None,
    filename: str | None = None,
) -> None:
    """Plot a network topology with an optional highlighted path."""
    pos = nx.spring_layout(graph, seed=42)
    nx.draw_networkx_nodes(graph, pos, node_size=300, node_color="lightblue")
    nx.draw_networkx_labels(graph, pos, font_size=8)
    nx.draw_networkx_edges(graph, pos, width=1.5)
    if path is not None:
        path_list = list(path)
        if len(path_list) > 1:
            nx.draw_networkx_edges(
                graph,
                pos,
                edgelist=list(zip(path_list, path_list[1:])),
                width=3,
                edge_color="red",
            )
    plt.axis("off")
    plt.tight_layout()
    if filename:
        plt.savefig(filename, dpi=300)
        plt.close()
    else:
        plt.show()


def plot_metric(
    x: List[float],
    y: List[float],
    xlabel: str,
    ylabel: str,
    title: str,
    filename: str | None = None,
) -> None:
    """Plot and optionally save a simple metric curve."""
    plt.figure()
    plt.plot(x, y, marker="o")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    if filename:
        plt.savefig(filename, dpi=300)
        plt.close()
    else:
        plt.show()
