#!/usr/bin/env python3
"""
Generate deterministic sample results for the QKD-ODCN demo.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

import yaml

project_root = Path(__file__).resolve().parents[1]
src_dir = project_root / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from qkd_odcn.allocation import allocate_first_fit
from qkd_odcn.config import validate_config
from qkd_odcn.connection_request import create_priority_queue, generate_requests
from qkd_odcn.metrics import network_security_provision, success_rate
from qkd_odcn.plotting import plot_metric
from qkd_odcn.topology import compute_k_sp_all, create_topology


def run_sweep(
    config_path: str | Path,
    max_cr: int,
    step: int,
    k: int = 3,
    seed: int | None = None,
) -> dict:
    """Run a deterministic request-count sweep and return JSON-ready results."""
    if seed is not None:
        random.seed(seed)

    config_path = Path(config_path)
    with open(config_path, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    validate_config(config)

    graph = create_topology([tuple(edge) for edge in config["edges"]])
    k_shortest = compute_k_sp_all(graph, k=k)

    x_values = []
    srcr_values = []
    nsp_values = []
    allocated_counts = []
    blocked_counts = []

    for num_cr in range(step, max_cr + step, step):
        requests = generate_requests(num_cr, num_nodes=len(graph.nodes))
        queue = create_priority_queue(requests)
        allocate_first_fit(graph, queue, k_shortest)
        x_values.append(num_cr)
        srcr_values.append(success_rate(queue))
        nsp_values.append(network_security_provision(queue))
        allocated_counts.append(sum(1 for request in queue if request.status == "allocated"))
        blocked_counts.append(sum(1 for request in queue if request.status == "blocked"))

    return {
        "config": str(config_path),
        "seed": seed,
        "k": k,
        "max_cr": max_cr,
        "step": step,
        "x_values": x_values,
        "srcr_values": srcr_values,
        "nsp_values": nsp_values,
        "allocated_counts": allocated_counts,
        "blocked_counts": blocked_counts,
        "note": "Generated from a seeded repository demonstration sweep.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate sample SRCR/NSP curves for the QKD-ODCN demo."
    )
    parser.add_argument("--config", type=str, required=True)
    parser.add_argument("--max-cr", type=int, default=50)
    parser.add_argument("--step", type=int, default=5)
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--output-dir", type=str, default="results/figures")
    parser.add_argument("--output-json", type=str, default=None)
    args = parser.parse_args()

    results = run_sweep(
        config_path=args.config,
        max_cr=args.max_cr,
        step=args.step,
        k=args.k,
        seed=args.seed,
    )

    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    srcr_plot_path = Path(args.output_dir) / "srcr_curve.png"
    plot_metric(
        results["x_values"],
        results["srcr_values"],
        xlabel="Number of connection requests",
        ylabel="Success rate (SRCR)",
        title="SRCR vs Number of Requests",
        filename=str(srcr_plot_path),
    )
    print(f"Saved SRCR curve to {srcr_plot_path}")

    nsp_plot_path = Path(args.output_dir) / "nsp_curve.png"
    plot_metric(
        results["x_values"],
        results["nsp_values"],
        xlabel="Number of connection requests",
        ylabel="Network security provision (NSP)",
        title="NSP vs Number of Requests",
        filename=str(nsp_plot_path),
    )
    print(f"Saved NSP curve to {nsp_plot_path}")

    if args.output_json:
        output_json = Path(args.output_json)
        output_json.parent.mkdir(parents=True, exist_ok=True)
        with open(output_json, "w", encoding="utf-8") as file:
            json.dump(results, file, indent=2)
            file.write("\n")
        print(f"Saved results to {output_json}")


if __name__ == "__main__":
    main()
