#!/usr/bin/env python3
"""
Phase II-2: Synaptic transmission in GU-inspired effective dynamics.

Includes:
  - electrical coupling proxy (gap-junction like),
  - chemical coupling proxy (release + receptor kernel),
  - delay and efficacy estimation.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Dict, List

from nn_redo_common import augment_report, write_report as write_contract_report

@dataclass
class SynapseConfig:
    dt: float = 0.001
    total_time: float = 1.5
    spike_times_pre: tuple = (0.12, 0.28, 0.44, 0.72, 1.05)
    synaptic_delay: float = 0.004
    tau_rise: float = 0.003
    tau_decay: float = 0.018
    w_electrical: float = 0.35
    w_chemical: float = 0.9
    threshold_post: float = 0.5


def _alpha_kernel(t: float, t0: float, tau_rise: float, tau_decay: float) -> float:
    x = t - t0
    if x <= 0:
        return 0.0
    return math.exp(-x / tau_decay) - math.exp(-x / tau_rise)


def run_synapse(cfg: SynapseConfig) -> Dict[str, object]:
    n_steps = int(cfg.total_time / cfg.dt)
    electrical_trace: List[float] = []
    chemical_trace: List[float] = []
    post_trace: List[float] = []
    rows: List[Dict[str, float]] = []

    first_cross = None
    peak_post = -1e9

    for i in range(n_steps):
        t = i * cfg.dt
        pre_spike_signal = 0.0
        for ts in cfg.spike_times_pre:
            pre_spike_signal += math.exp(-((t - ts) ** 2) / (2.0 * 0.0015**2))

        electrical = cfg.w_electrical * pre_spike_signal
        chemical = 0.0
        for ts in cfg.spike_times_pre:
            chemical += cfg.w_chemical * _alpha_kernel(
                t, ts + cfg.synaptic_delay, cfg.tau_rise, cfg.tau_decay
            )

        post = electrical + chemical
        peak_post = max(peak_post, post)
        if first_cross is None and post >= cfg.threshold_post:
            first_cross = t

        electrical_trace.append(electrical)
        chemical_trace.append(chemical)
        post_trace.append(post)

        if i % max(1, n_steps // 24) == 0:
            rows.append(
                {
                    "t_s": round(t, 6),
                    "electrical_component": round(electrical, 6),
                    "chemical_component": round(chemical, 6),
                    "post_synaptic_signal": round(post, 6),
                }
            )

    mean_elec = sum(electrical_trace) / len(electrical_trace)
    mean_chem = sum(chemical_trace) / len(chemical_trace)
    chem_to_elec = mean_chem / (mean_elec + 1e-12)
    transmission_delay = None
    if first_cross is not None and len(cfg.spike_times_pre) > 0:
        transmission_delay = first_cross - cfg.spike_times_pre[0]

    return {
        "model": "synaptic_transmission",
        "config": {
            **cfg.__dict__,
            "spike_times_pre": list(cfg.spike_times_pre),
        },
        "summary": {
            "peak_post_synaptic_signal": round(peak_post, 6),
            "mean_electrical_component": round(mean_elec, 6),
            "mean_chemical_component": round(mean_chem, 6),
            "chemical_to_electrical_ratio": round(chem_to_elec, 6),
            "first_transmission_delay_s": round(transmission_delay, 6)
            if transmission_delay is not None
            else None,
        },
        "sampled_transmission": rows,
    }


def write_report(report: Dict[str, object]) -> Path:
    payload = augment_report(__file__, report)
    return write_contract_report(__file__, payload)


def main() -> None:
    cfg = SynapseConfig()
    report = run_synapse(cfg)
    out_path = write_report(report)
    s = report["summary"]
    print("Synaptic transmission (GU)")
    print(f"- peak post signal: {s['peak_post_synaptic_signal']}")
    print(f"- chem/elec ratio: {s['chemical_to_electrical_ratio']}")
    print(f"- first delay [s]: {s['first_transmission_delay_s']}")
    print(f"- report: {out_path}")


if __name__ == "__main__":
    main()
