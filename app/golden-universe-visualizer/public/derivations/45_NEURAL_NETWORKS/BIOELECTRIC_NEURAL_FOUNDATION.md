# Bioelectric Neural Foundation from Golden Universe

## Purpose

This document defines the Phase I computational foundation for neural-network emergence in GU:

- `01_single_cell_neural_computation.py`
- `02_gap_junction_networks.py`
- `03_bioelectric_memory_traces.py`

The focus is a first-principles bridge from cellular bioelectricity to neural computation primitives.

## Canonical GU Starting Point

We use the GU phase-channel coupling in effective form:

- `J_theta^nu = (kappa / 2pi^2) (partial_mu theta) F_tilde^{mu nu}`

Operationally, this appears as:

1. stimulus-driven phase/membrane modulation,
2. memory-feedback stabilization loops,
3. network coupling through gap-junction-like channels.

## Phase I Model Stack

### 1) Single-cell computation

`01_single_cell_neural_computation.py` models chemotaxis as:

- fast signal channel (stimulus -> membrane proxy),
- adaptive memory baseline,
- run/tumble decision gate.

Outputs include:

- decision information rate (bits/s),
- energy-power proxy,
- adaptation behavior over time.

### 2) Gap-junction network dynamics

`02_gap_junction_networks.py` models a coupled ring tissue:

- each node is a bioelectric cell state,
- coupling is controlled by gap-junction strength,
- pacemaker drive seeds coordinated propagation.

Outputs include:

- coherence (synchronization) metrics,
- delay/propagation proxies,
- connectivity-density summary.

### 3) Bioelectric memory traces

`03_bioelectric_memory_traces.py` uses a two-timescale memory model:

- fast Vm state,
- slow gene-expression-like state,
- retention state linking transient dynamics to persistence.

Outputs include:

- post-training retained Vm,
- retrieval score,
- half-life memory proxy.

## Scaling Logic (Cell -> Tissue)

The scaling rule in this phase is:

- single-cell decision loops establish local computation,
- gap-junction coupling creates collective dynamics,
- slow memory channels preserve learned tissue states.

This provides the base computational grammar for later neural-circuit derivations.

## Validation Approach

Phase I validation is designed around measurable proxies:

- information throughput,
- synchronization and delay statistics,
- memory retention after stimulus removal.

The models are deterministic and reproducible. Each script writes a JSON report for downstream phase reuse.

## Limit Boundaries

This phase deliberately does not claim full ion-channel biophysics or complete cortical realism.
It establishes GU-consistent computational primitives that later phases can refine into action potentials, synapses, plasticity, and consciousness-scale architectures.
