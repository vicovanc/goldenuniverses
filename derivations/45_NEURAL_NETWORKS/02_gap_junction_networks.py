#!/usr/bin/env python3
"""
Phase I-2: Gap junction network dynamics from GU first principles.

Cells are represented as coupled bioelectric phase/membrane nodes.
Gap junction strength controls synchronization, propagation delay, and
collective decision coherence.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Dict, List

import numpy as np

from nn_redo_common import augment_report, write_report as write_contract_report

@dataclass
class NetworkConfig:
    n_cells: int = 24
    dt: float = 0.02
    total_time: float = 40.0
    coupling_gj: float = 0.18
    leak: float = 0.08
    pacemaker_cells: int = 2
    conduction_speed_proxy: float = 0.12


def _pacemaker_drive(t: float) -> float:
    return 0.8 * math.sin(2.0 * math.pi * t / 1.0)


def _ring_laplacian(n: int) -> np.ndarray:
    l = np.zeros((n, n), dtype=float)
    for i in range(n):
        l[i, i] = 2.0
        l[i, (i - 1) % n] = -1.0
        l[i, (i + 1) % n] = -1.0
    return l


def run_network(cfg: NetworkConfig) -> Dict[str, object]:
    n_steps = int(cfg.total_time / cfg.dt)
    state = np.zeros(cfg.n_cells, dtype=float)
    lap = _ring_laplacian(cfg.n_cells)

    synchrony_samples: List[float] = []
    propagation_samples: List[float] = []
    rows: List[Dict[str, float]] = []

    for i in range(n_steps):
        t = i * cfg.dt
        drive = np.zeros(cfg.n_cells, dtype=float)
        drive[: cfg.pacemaker_cells] = _pacemaker_drive(t)

        # dV/dt = drive - leak*V - g*L*V
        dstate = drive - cfg.leak * state - cfg.coupling_gj * (lap @ state)
        state = state + cfg.dt * dstate

        # Kuramoto-like phase coherence proxy from normalized membrane state.
        phase = np.angle(np.exp(1j * state))
        coh = abs(np.mean(np.exp(1j * phase)))
        synchrony_samples.append(float(coh))

        # Propagation delay proxy from gradient in ring.
        grad = np.abs(np.roll(state, -1) - state)
        mean_grad = float(np.mean(grad))
        delay_proxy = mean_grad / max(cfg.conduction_speed_proxy, 1e-9)
        propagation_samples.append(delay_proxy)

        if i % max(1, n_steps // 20) == 0:
            rows.append(
                {
                    "t_s": round(t, 3),
                    "mean_membrane": round(float(np.mean(state)), 6),
                    "std_membrane": round(float(np.std(state)), 6),
                    "coherence": round(float(coh), 6),
                    "delay_proxy": round(float(delay_proxy), 6),
                }
            )

    coherence_mean = float(np.mean(synchrony_samples))
    coherence_peak = float(np.max(synchrony_samples))
    delay_mean = float(np.mean(propagation_samples))
    connectivity_density = 2.0 / cfg.n_cells  # ring graph degree / N

    return {
        "model": "gap_junction_networks",
        "config": cfg.__dict__,
        "summary": {
            "mean_coherence": round(coherence_mean, 6),
            "peak_coherence": round(coherence_peak, 6),
            "mean_delay_proxy": round(delay_mean, 6),
            "connectivity_density": round(connectivity_density, 6),
            "effective_signal_speed_proxy": round(cfg.conduction_speed_proxy, 6),
        },
        "sampled_network_state": rows,
    }


def write_report(report: Dict[str, object]) -> Path:
    payload = augment_report(__file__, report)
    return write_contract_report(__file__, payload)


def main() -> None:
    cfg = NetworkConfig()
    report = run_network(cfg)
    out_path = write_report(report)
    s = report["summary"]
    print("Gap junction networks (GU)")
    print(f"- mean coherence: {s['mean_coherence']}")
    print(f"- peak coherence: {s['peak_coherence']}")
    print(f"- mean delay proxy: {s['mean_delay_proxy']}")
    print(f"- signal speed proxy: {s['effective_signal_speed_proxy']}")
    print(f"- report: {out_path}")


if __name__ == "__main__":
    main()
