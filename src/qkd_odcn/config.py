"""Configuration validation utilities for QKD-ODCN demos."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any


def validate_config(config: Any) -> None:
    """Validate a topology configuration dictionary.

    The required schema is ``{"edges": [[u, v, weight], ...]}``.
    """
    if not isinstance(config, Mapping):
        raise ValueError("top-level config must be a mapping")
    if "edges" not in config:
        raise ValueError("config must contain an 'edges' entry")
    edges = config["edges"]
    if not isinstance(edges, Sequence) or isinstance(edges, (str, bytes)):
        raise ValueError("'edges' must be a sequence of edge entries")

    for edge in edges:
        if not isinstance(edge, Sequence) or isinstance(edge, (str, bytes)):
            raise ValueError(f"edge {edge!r} must be a sequence")
        if len(edge) != 3:
            raise ValueError(f"edge {edge!r} must have exactly 3 entries")
        source, destination, weight = edge
        if not isinstance(source, int) or not isinstance(destination, int):
            raise ValueError(f"edge {edge!r} source and destination must be ints")
        if source == destination:
            raise ValueError(f"edge {edge!r} must not be a self-loop")
        if not isinstance(weight, (int, float)):
            raise ValueError(f"edge {edge!r} weight must be numeric")
        if weight <= 0:
            raise ValueError(f"edge {edge!r} weight must be positive")
