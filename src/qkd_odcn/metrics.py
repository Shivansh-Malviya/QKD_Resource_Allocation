"""Metrics for evaluating simplified QKD-ODCN allocation demonstrations."""

from __future__ import annotations

from typing import List

from .connection_request import ConnectionRequest, SECURITY_WEIGHTS


def success_rate(requests: List[ConnectionRequest]) -> float:
    """Return SRCR as allocated requests divided by total requests."""
    if not requests:
        return 0.0
    allocated = sum(1 for request in requests if request.status == "allocated")
    return allocated / len(requests)


def network_security_provision(
    requests: List[ConnectionRequest],
    channel: str = "total",
) -> float:
    """Return a simplified security-weighted allocation fraction.

    The ``channel`` argument is retained for compatibility with older thesis
    code but is ignored in this simplified public implementation.
    """
    if not requests:
        return 0.0
    total_weight = sum(SECURITY_WEIGHTS[request.security_level] for request in requests)
    allocated_weight = sum(
        SECURITY_WEIGHTS[request.security_level]
        for request in requests
        if request.status == "allocated"
    )
    if total_weight == 0:
        return 0.0
    return allocated_weight / total_weight
