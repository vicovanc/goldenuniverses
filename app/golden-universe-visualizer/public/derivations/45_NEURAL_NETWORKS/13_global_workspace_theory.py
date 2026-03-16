#!/usr/bin/env python3
"""
Phase IV-1: Global workspace theory in a GU-inspired integration model.

Multiple specialist modules compete for broadcast. Conscious access is modeled
as threshold-crossing in shared workspace integration.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Dict, List

import numpy as np

from nn_redo_common import augment_report, write_report as write_contract_report

@dataclass
class WorkspaceConfig:
    n_modules: int = 6
    steps: int = 220
    dt: float = 0.05
    gate_threshold: float = 0.62
    recurrent_gain: float = 0.4
    seed: int = 13


def run_workspace(cfg: WorkspaceConfig) -> Dict[str, object]:
    rng = np.random.default_rng(cfg.seed)
    module_state = np.zeros(cfg.n_modules, dtype=float)
    broadcast = 0.0
    conscious_steps = 0
    rows: List[Dict[str, float]] = []

    for k in range(cfg.steps):
        t = k * cfg.dt
        external = 0.35 + 0.2 * np.sin(0.12 * k + np.arange(cfg.n_modules) * 0.7)
        noise = 0.05 * rng.normal(size=cfg.n_modules)
        module_state = np.tanh(0.7 * module_state + external + noise + cfg.recurrent_gain * broadcast)

        competition = np.max(module_state) - np.mean(module_state)
        broadcast = float(np.clip(np.mean(module_state) + 0.35 * competition, 0.0, 1.2))
        conscious = broadcast >= cfg.gate_threshold
        conscious_steps += int(conscious)

        if k % max(1, cfg.steps // 24) == 0:
            rows.append(
                {
                    "t_s": round(t, 4),
                    "broadcast_level": round(float(broadcast), 6),
                    "module_mean": round(float(np.mean(module_state)), 6),
                    "module_max": round(float(np.max(module_state)), 6),
                    "conscious_access": float(conscious),
                }
            )

    conscious_fraction = conscious_steps / cfg.steps
    integration_index = float(np.mean([r["module_mean"] for r in rows]))

    return {
        "model": "global_workspace_theory",
        "config": cfg.__dict__,
        "summary": {
            "conscious_access_fraction": round(conscious_fraction, 6),
            "integration_index": round(integration_index, 6),
            "final_broadcast_level": round(float(broadcast), 6),
            "gate_threshold": cfg.gate_threshold,
        },
        "canonical_observables": {
            "integration_index": round(integration_index, 6),
            "conscious_access_fraction": round(conscious_fraction, 6),
        },
        "exploratory_metrics": {
            "final_broadcast_level": round(float(broadcast), 6),
        },
        "sampled_workspace_dynamics": rows,
    }


def write_report(report: Dict[str, object]) -> Path:
    payload = augment_report(__file__, report)
    return write_contract_report(__file__, payload)


def main() -> None:
    cfg = WorkspaceConfig()
    report = run_workspace(cfg)
    out_path = write_report(report)
    s = report["summary"]
    print("Global workspace theory (GU)")
    print(f"- conscious access fraction: {s['conscious_access_fraction']}")
    print(f"- integration index: {s['integration_index']}")
    print(f"- report: {out_path}")


if __name__ == "__main__":
    main()
