# QKD-ODCN Resource Allocation

## Overview

**QKD-ODCN Resource Allocation** presents a compact Python implementation of resource-allocation ideas studied in my BS-MS thesis, **Study and Design of Efficient and Resilient Quantum Key Distribution System**. The project explores how quantum-key resources, security levels, and classical network constraints interact in a QKD-enabled optical data center network model.

The repository is organized as a research prototype around topology construction, connection-request prioritization, path selection, quantum secure channel assignment, and allocation metrics. It also includes selected BB84 and Hamming-code utilities that support the broader QKD simulation context.

## Implemented Components

- Network topology construction and k-shortest-path search with NetworkX.
- A `ConnectionRequest` model with security levels, allocation state, resource assignment, and path tracking.
- Priority-ordered request scheduling across high, medium, and low security classes.
- A first-fit allocation heuristic for quantum secure channel and time-slot resources along candidate paths.
- SRCR and NSP metrics for allocation success and security-weighted provisioning.
- BB84 raw-key, measurement, sifting, and key-error-rate helpers for simulation context.
- Hamming (7,4) encoding and single-bit correction utilities.
- Seeded sample outputs for the six-node demonstration topology.

## Technical Scope

The retained implementation is a research-code prototype, not an operational QKD security stack. The allocator models resource assignment behavior for simulation and comparison; it does not provide deployable cryptographic security guarantees.

Metric coverage is explicit:

- **SRCR**: allocation success rate over connection requests.
- **NSP**: security-weighted allocation fraction.
- **QBER, SKR, TUR, QKU, BP**: thesis-context metrics that are not part of the retained allocation metric layer in this package.

## Repository Structure

```text
QKD_Resource_Allocation/
|-- README.md
|-- LICENSE
|-- CITATION.cff
|-- pyproject.toml
|-- requirements.txt
|-- .github/workflows/ci.yml
|-- src/qkd_odcn/
|-- configs/
|-- scripts/
|-- tests/
`-- results/
```

## Module Map

- `src/qkd_odcn/topology.py`: topology construction and k-shortest-path search.
- `src/qkd_odcn/connection_request.py`: connection-request model and priority queue construction.
- `src/qkd_odcn/allocation.py`: first-fit QSC/time-slot allocation.
- `src/qkd_odcn/metrics.py`: SRCR and simplified NSP metrics.
- `src/qkd_odcn/bb84.py`: BB84 simulation helpers.
- `src/qkd_odcn/hamming.py`: Hamming (7,4) encoding and decoding utilities.
- `src/qkd_odcn/plotting.py`: topology and metric plotting helpers.
- `configs/six_node.yaml`: representative six-node ODCN topology.
- `scripts/run_demo.py`: seeded single-run allocation demonstration.
- `scripts/generate_sample_results.py`: seeded SRCR/NSP sweep used for the retained sample outputs.
- `results/`: representative JSON and figure artifacts.

## Thesis Context

The thesis work studied efficient and resilient QKD system design across simulation settings that included BB84 behavior, error-rate analysis, secure-key behavior, and network resource allocation. This repository focuses on the allocation-facing software layer and selected supporting utilities in a maintainable package layout.

The code is licensed under MIT. Citation metadata is provided in `CITATION.cff`.
