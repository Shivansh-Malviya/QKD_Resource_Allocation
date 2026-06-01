"""
Connection request model for QKD-enabled optical data center networks.

This module defines a compact ``ConnectionRequest`` class and helpers for
generating synthetic connection requests and organising them into priority
queues for allocation simulations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import random
from typing import List, Tuple


@dataclass
class ConnectionRequest:
    """A connection request between two nodes with an associated security level."""

    index: int
    source: int
    destination: int
    security_level: str
    time_slots: int = 1
    status: str = field(default="initialized", init=False)
    allocated_resources: Tuple[int | None, int | None] = field(
        default_factory=lambda: (None, None), init=False
    )
    path: List[int] | None = field(default=None, init=False)

    def update_status(
        self,
        status: str,
        allocated_resources: Tuple[int | None, int | None] | None = None,
        path: List[int] | None = None,
    ) -> None:
        """Update status, resources, and path.

        ``path`` is always assigned. Passing ``path=None`` intentionally clears
        a previously allocated path, which is required when a request becomes
        blocked after an earlier allocation state.
        """
        self.status = status
        if allocated_resources is not None:
            self.allocated_resources = allocated_resources
        self.path = path

    def __repr__(self) -> str:  # pragma: no cover - simple representation
        return (
            f"ConnectionRequest(index={self.index}, source={self.source}, "
            f"destination={self.destination}, security_level={self.security_level}, "
            f"status={self.status}, allocated_resources={self.allocated_resources}, "
            f"path={self.path})"
        )


SECURITY_LEVELS: List[str] = ["high", "medium", "low"]
SECURITY_WEIGHTS = {"high": 5, "medium": 4, "low": 3}


def generate_requests(num_requests: int, num_nodes: int) -> List[ConnectionRequest]:
    """Generate random connection requests over nodes numbered from 1."""
    requests: List[ConnectionRequest] = []
    base = num_requests // len(SECURITY_LEVELS)
    level_pool = SECURITY_LEVELS * base
    for _ in range(num_requests % len(SECURITY_LEVELS)):
        level_pool.append(random.choice(SECURITY_LEVELS))
    random.shuffle(level_pool)

    for i in range(num_requests):
        source = random.randint(1, num_nodes)
        destination = random.randint(1, num_nodes)
        while source == destination:
            destination = random.randint(1, num_nodes)
        security_level = level_pool.pop() if level_pool else random.choice(SECURITY_LEVELS)
        requests.append(
            ConnectionRequest(
                index=i,
                source=source,
                destination=destination,
                security_level=security_level,
                time_slots=1,
            )
        )
    return requests


def create_priority_queue(
    requests: List[ConnectionRequest],
    return_all: bool = False,
) -> List[ConnectionRequest] | Tuple[
    List[ConnectionRequest],
    List[ConnectionRequest],
    List[ConnectionRequest],
    List[ConnectionRequest],
]:
    """Create a high-medium-low security priority queue."""
    high: List[ConnectionRequest] = []
    medium: List[ConnectionRequest] = []
    low: List[ConnectionRequest] = []
    for request in requests:
        if request.security_level == "high":
            high.append(request)
        elif request.security_level == "medium":
            medium.append(request)
        else:
            low.append(request)
    priority_queue = high + medium + low
    if return_all:
        return priority_queue, high, medium, low
    return priority_queue
