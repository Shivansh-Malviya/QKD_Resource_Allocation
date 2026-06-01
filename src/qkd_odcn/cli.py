"""Command-line entry points for qkd_odcn."""

from __future__ import annotations

import argparse
import random
from pathlib import Path

import yaml

from .allocation import allocate_first_fit
from .config import validate_config
from .connection_request import create_priority_queue, generate_requests
from .metrics import network_security_provision, success_rate
from .plotting import plot_topology
from .topology import compute_k_sp_all, create_topology


def main() -> None:
    """Run the sample QKD-ODCN resource-allocation demonstration."""
    parser = argparse.ArgumentParser(
        description="Run a QKD-ODCN resource allocation demonstration."
    )
    parser.add_argument("--config", type=str, required=True)
    parser.add_argument("--num-cr", type=int, default=10)
    parser.add_argument("--k", type=int, default=3)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--output-dir", type=str, default="results/figures")
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    with open(Path(args.config), "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    validate_config(config)

    graph = create_topology([tuple(edge) for edge in config["edges"]])
    k_shortest = compute_k_sp_all(graph, k=args.k)
    requests = generate_requests(args.num_cr, num_nodes=len(graph.nodes))
    queue = create_priority_queue(requests)
    allocate_first_fit(graph, queue, k_shortest)

    print(f"Success rate (SRCR): {success_rate(queue):.2f}")
    print(f"Network security provision (NSP): {network_security_provision(queue):.2f}")

    if args.plot:
        Path(args.output_dir).mkdir(parents=True, exist_ok=True)
        first_allocated = next(
            (request for request in queue if request.status == "allocated" and request.path),
            None,
        )
        output_file = Path(args.output_dir) / "topology_demo.png"
        plot_topology(
            graph,
            path=first_allocated.path if first_allocated else None,
            filename=str(output_file),
        )
        print(f"Saved topology plot to {output_file}")


if __name__ == "__main__":
    main()
