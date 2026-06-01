"""Tests for topology config validation."""

import pytest

from qkd_odcn.config import validate_config


def test_valid_config_passes() -> None:
    validate_config({"edges": [[1, 2, 1], [2, 3, 2.5]]})


def test_missing_edges_fails() -> None:
    with pytest.raises(ValueError):
        validate_config({})


@pytest.mark.parametrize(
    "config",
    [
        {"edges": [[1, 2]]},
        {"edges": [[1, 2, 3, 4]]},
        {"edges": [["1", 2, 1]]},
        {"edges": [[1, "2", 1]]},
    ],
)
def test_malformed_edge_fails(config: dict) -> None:
    with pytest.raises(ValueError):
        validate_config(config)


@pytest.mark.parametrize("weight", [0, -1])
def test_non_positive_weight_fails(weight: int) -> None:
    with pytest.raises(ValueError):
        validate_config({"edges": [[1, 2, weight]]})


def test_self_loop_fails() -> None:
    with pytest.raises(ValueError):
        validate_config({"edges": [[1, 1, 1]]})
