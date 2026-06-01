"""Tests for deterministic sample JSON generation support."""

from scripts.generate_sample_results import run_sweep


def test_run_sweep_returns_required_json_keys() -> None:
    results = run_sweep("configs/six_node.yaml", max_cr=20, step=5, k=3, seed=42)
    required = {
        "config",
        "seed",
        "k",
        "max_cr",
        "step",
        "x_values",
        "srcr_values",
        "nsp_values",
        "allocated_counts",
        "blocked_counts",
        "note",
    }
    assert required <= results.keys()
    assert results["x_values"] == [5, 10, 15, 20]
    assert len(results["srcr_values"]) == 4
    assert len(results["nsp_values"]) == 4
    assert len(results["allocated_counts"]) == 4
    assert len(results["blocked_counts"]) == 4
    assert results["note"] == "Generated from a seeded repository demonstration sweep."
