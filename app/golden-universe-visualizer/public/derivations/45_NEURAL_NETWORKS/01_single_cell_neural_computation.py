#!/usr/bin/env python3
"""
Phase I-1: Single-cell neural computation from GU first principles.

This module models E. coli-like chemotaxis as a minimal neural computation
system with:
  - theta-like signal channel (stimulus -> membrane modulation)
  - adaptive memory state (methylation proxy)
  - binary run/tumble decision gate

The goal is not biochemical micro-detail, but a GU-consistent dynamical
prototype that can be measured with information and energy metrics.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Dict, List

from nn_redo_common import augment_report, write_report as write_contract_report

@dataclass
class ChemotaxisConfig:
    dt: float = 0.05
    total_time: float = 120.0
    adaptation_tau: float = 8.0
    gain_signal: float = 1.8
    gain_memory: float = 1.1
    threshold: float = 0.15
    baseline_tumble: float = 0.2
    decision_noise: float = 0.03
    k_bioelectric: float = 0.45


def attractant_profile(t: float) -> float:
    """Piecewise smooth attractant profile with a late pulse."""
    base = 0.3 + 0.2 * math.sin(2.0 * math.pi * t / 60.0)
    pulse = 0.35 * math.exp(-((t - 90.0) ** 2) / (2.0 * 9.0**2))
    return max(0.0, base + pulse)


def run_model(cfg: ChemotaxisConfig) -> Dict[str, object]:
    n_steps = int(cfg.total_time / cfg.dt)

    memory = 0.0
    membrane = 0.0
    run_fraction_sum = 0.0
    energy_sum = 0.0
    entropy_bits_sum = 0.0

    rows: List[Dict[str, float]] = []
    last_run_prob = 0.5

    for i in range(n_steps):
        t = i * cfg.dt
        stim = attractant_profile(t)

        # Adaptive memory tracks long-time average stimulus.
        dmem = (stim - memory) / cfg.adaptation_tau
        memory += cfg.dt * dmem

        # Theta-like processing channel (signal minus adapted baseline).
        theta_drive = cfg.gain_signal * (stim - cfg.gain_memory * memory)
        membrane = membrane + cfg.dt * (cfg.k_bioelectric * theta_drive - 0.5 * membrane)

        decision_variable = membrane - cfg.threshold
        # Deterministic pseudo-noise from signal phase (reproducible).
        det_noise = cfg.decision_noise * math.sin(0.37 * t + 0.9 * stim)
        run_prob = 1.0 / (1.0 + math.exp(-8.0 * (decision_variable + det_noise)))
        tumble_prob = max(0.0, 1.0 - run_prob)
        run_fraction_sum += run_prob

        # Minimal energetic proxy: |signal work| + membrane maintenance.
        energy_step = abs(theta_drive) * 0.02 + abs(membrane) * 0.01
        energy_sum += energy_step * cfg.dt

        # Bernoulli decision entropy (bits).
        p = min(max(run_prob, 1e-9), 1.0 - 1e-9)
        entropy_bits = -(p * math.log2(p) + (1.0 - p) * math.log2(1.0 - p))
        entropy_bits_sum += entropy_bits * cfg.dt

        if i % max(1, n_steps // 24) == 0:
            rows.append(
                {
                    "t_s": round(t, 3),
                    "stimulus": round(stim, 6),
                    "memory_state": round(memory, 6),
                    "membrane_proxy": round(membrane, 6),
                    "run_probability": round(run_prob, 6),
                    "tumble_probability": round(tumble_prob, 6),
                }
            )
        last_run_prob = run_prob

    avg_run_fraction = run_fraction_sum / n_steps
    info_rate_bits_per_s = entropy_bits_sum / cfg.total_time
    power_proxy = energy_sum / cfg.total_time

    return {
        "model": "single_cell_neural_computation",
        "config": cfg.__dict__,
        "summary": {
            "average_run_fraction": round(avg_run_fraction, 6),
            "final_run_probability": round(last_run_prob, 6),
            "information_rate_bits_per_second": round(info_rate_bits_per_s, 6),
            "energy_power_proxy": round(power_proxy, 6),
            "adaptive_memory_timescale_s": cfg.adaptation_tau,
        },
        "sampled_trajectory": rows,
    }


def write_report(report: Dict[str, object]) -> Path:
    payload = augment_report(__file__, report)
    return write_contract_report(__file__, payload)


def main() -> None:
    cfg = ChemotaxisConfig()
    report = run_model(cfg)
    out_path = write_report(report)

    s = report["summary"]
    print("Single-cell neural computation (GU)")
    print(f"- avg run fraction: {s['average_run_fraction']}")
    print(f"- final run probability: {s['final_run_probability']}")
    print(f"- info rate [bits/s]: {s['information_rate_bits_per_second']}")
    print(f"- power proxy: {s['energy_power_proxy']}")
    print(f"- report: {out_path}")


if __name__ == "__main__":
    main()
