#!/usr/bin/env python3
"""
Phase IV-2: Self-referential circuits in a GU-inspired loop architecture.

Models a system state and a meta-state that estimates the system itself,
producing a self-model error trajectory.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Dict, List

from nn_redo_common import augment_report, write_report as write_contract_report
import numpy as np


@dataclass
class SelfRefConfig:
    steps: int = 260
    dt: float = 0.04
    system_gain: float = 0.78
    meta_gain: float = 0.66
    self_ref_gain: float = 0.42
    seed: int = 14


def run_self_referential(cfg: SelfRefConfig) -> Dict[str, object]:
    rng = np.random.default_rng(cfg.seed)
    x = 0.0  # system state
    m = 0.0  # meta representation of system
    err_hist: List[float] = []
    rows: List[Dict[str, float]] = []

    for k in range(cfg.steps):
        t = k * cfg.dt
        drive = 0.55 * np.sin(0.09 * k) + 0.1 * rng.normal()
        x = np.tanh(cfg.system_gain * x + drive)
        m = np.tanh(cfg.meta_gain * m + cfg.self_ref_gain * x)
        err = abs(x - m)
        err_hist.append(float(err))

        if k % max(1, cfg.steps // 24) == 0:
            rows.append(
                {
                    "t_s": round(t, 4),
                    "system_state": round(float(x), 6),
                    "meta_state": round(float(m), 6),
                    "self_model_error": round(float(err), 6),
                }
            )

    mean_err = float(np.mean(err_hist))
    final_err = float(err_hist[-1]) if err_hist else 0.0
    convergence_ratio = final_err / max(err_hist[0], 1e-9)

    return {
        "model": "self_referential_circuits",
        "config": cfg.__dict__,
        "summary": {
            "mean_self_model_error": round(mean_err, 6),
            "final_self_model_error": round(final_err, 6),
            "convergence_ratio_final_over_initial": round(convergence_ratio, 6),
            "self_reference_stable": mean_err < 0.35,
        },
        "canonical_observables": {
            "mean_self_model_error": round(mean_err, 6),
            "self_reference_stable": mean_err < 0.35,
        },
        "exploratory_metrics": {
            "convergence_ratio_final_over_initial": round(convergence_ratio, 6),
        },
        "sampled_self_reference": rows,
    }


def write_report(report: Dict[str, object]) -> Path:
    payload = augment_report(__file__, report)
    return write_contract_report(__file__, payload)


def main() -> None:
    cfg = SelfRefConfig()
    report = run_self_referential(cfg)
    out_path = write_report(report)
    s = report["summary"]
    print("Self-referential circuits (GU)")
    print(f"- mean self-model error: {s['mean_self_model_error']}")
    print(f"- final self-model error: {s['final_self_model_error']}")
    print(f"- report: {out_path}")


if __name__ == "__main__":
    main()
