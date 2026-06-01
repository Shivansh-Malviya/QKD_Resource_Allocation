"""Tests for connection request state transitions."""

from qkd_odcn.connection_request import ConnectionRequest


def test_update_status_can_clear_path() -> None:
    request = ConnectionRequest(0, 1, 3, "high")
    request.update_status("allocated", allocated_resources=(1, 1), path=[1, 2, 3])
    assert request.status == "allocated"
    assert request.path == [1, 2, 3]

    request.update_status("blocked", allocated_resources=(None, None), path=None)
    assert request.status == "blocked"
    assert request.path is None
    assert request.allocated_resources == (None, None)
