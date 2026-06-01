"""Tests for simplified allocation metrics."""

from qkd_odcn.connection_request import ConnectionRequest
from qkd_odcn.metrics import network_security_provision, success_rate


def test_empty_request_list_returns_zero() -> None:
    assert success_rate([]) == 0.0
    assert network_security_provision([]) == 0.0


def test_srcr_is_allocated_divided_by_total() -> None:
    requests = [
        ConnectionRequest(0, 1, 2, "high"),
        ConnectionRequest(1, 1, 2, "medium"),
        ConnectionRequest(2, 1, 2, "low"),
    ]
    requests[0].update_status("allocated", allocated_resources=(1, 1), path=[1, 2])
    requests[1].update_status("blocked", allocated_resources=(None, None), path=None)
    requests[2].update_status("allocated", allocated_resources=(1, 1), path=[1, 2])

    assert success_rate(requests) == 2 / 3


def test_nsp_uses_weights_and_allocated_requests_only() -> None:
    high = ConnectionRequest(0, 1, 2, "high")
    medium = ConnectionRequest(1, 1, 2, "medium")
    low = ConnectionRequest(2, 1, 2, "low")
    high.update_status("allocated", allocated_resources=(1, 1), path=[1, 2])
    medium.update_status("blocked", allocated_resources=(None, None), path=None)
    low.update_status("allocated", allocated_resources=(1, 1), path=[1, 2])

    assert network_security_provision([high, medium, low]) == 8 / 12


def test_nsp_mixed_high_medium_low_hand_computed() -> None:
    requests = [
        ConnectionRequest(0, 1, 2, "high"),
        ConnectionRequest(1, 1, 2, "medium"),
        ConnectionRequest(2, 1, 2, "low"),
        ConnectionRequest(3, 2, 3, "high"),
    ]
    requests[0].update_status("allocated", allocated_resources=(1, 1), path=[1, 2])
    requests[1].update_status("allocated", allocated_resources=(1, 1), path=[1, 2])
    requests[2].update_status("blocked", allocated_resources=(None, None), path=None)
    requests[3].update_status("blocked", allocated_resources=(None, None), path=None)

    # allocated = 5 + 4, total = 5 + 4 + 3 + 5
    assert network_security_provision(requests) == 9 / 17
