"""Deterministic tests for simplified first-fit allocation."""

from qkd_odcn.allocation import allocate_first_fit
from qkd_odcn.connection_request import ConnectionRequest
from qkd_odcn.topology import compute_k_sp_all, create_topology


def _request(index: int, source: int = 1, destination: int = 3) -> ConnectionRequest:
    return ConnectionRequest(index, source, destination, "high")


def test_shortest_path_allocates_first() -> None:
    graph = create_topology([(1, 2, 1), (2, 3, 1), (1, 3, 5)])
    k_paths = compute_k_sp_all(graph, k=2)
    request = _request(0)

    allocate_first_fit(graph, [request], k_paths)

    assert request.status == "allocated"
    assert request.allocated_resources == (1, 1)
    assert request.path == [1, 2, 3]


def test_second_request_blocks_when_only_constrained_path_is_available() -> None:
    graph = create_topology([(1, 2, 1), (2, 3, 1), (1, 3, 5)])
    k_paths = compute_k_sp_all(graph, k=1)
    first = _request(0)
    second = _request(1)

    allocate_first_fit(graph, [first, second], k_paths)

    assert first.status == "allocated"
    assert first.path == [1, 2, 3]
    assert second.status == "blocked"
    assert second.allocated_resources == (None, None)
    assert second.path is None


def test_second_request_uses_alternate_path_when_k_permits_it() -> None:
    graph = create_topology([(1, 2, 1), (2, 3, 1), (1, 3, 5)])
    k_paths = compute_k_sp_all(graph, k=2)
    first = _request(0)
    second = _request(1)

    allocate_first_fit(graph, [first, second], k_paths)

    assert first.status == "allocated"
    assert first.path == [1, 2, 3]
    assert second.status == "allocated"
    assert second.allocated_resources == (1, 1)
    assert second.path == [1, 3]


def test_undirected_edge_accounting_is_consistent() -> None:
    graph = create_topology([(1, 2, 1), (2, 3, 1), (1, 3, 5)])
    k_paths = compute_k_sp_all(graph, k=1)
    forward = ConnectionRequest(0, 1, 3, "high")
    reverse = ConnectionRequest(1, 3, 1, "high")

    allocate_first_fit(graph, [forward, reverse], k_paths)

    assert forward.status == "allocated"
    assert forward.path == [1, 2, 3]
    assert reverse.status == "blocked"
    assert reverse.allocated_resources == (None, None)
    assert reverse.path is None
