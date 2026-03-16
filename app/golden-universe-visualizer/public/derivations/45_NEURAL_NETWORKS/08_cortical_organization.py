#!/usr/bin/env python3
"""
Phase III-1: Cortical organization from hierarchical theta-processing.

Builds a 3-layer feedforward hierarchy and quantifies:
  - layer-wise information compression/expansion,
  - selectivity growth,
  - depth-wise abstraction proxy.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Dict, List

import numpy as np

from nn_redo_common import augment_report, write_report as write_contract_report

@dataclass
class CorticalConfig:
    input_dim: int = 16
    l1_dim: int = 24
    l2_dim: int = 14
    l3_dim: int = 8
    samples: int = 240
    seed: int = 45


def _nonlinear(x: np.ndarray) -> np.ndarray:
    return np.tanh(x)


def run_cortical_model(cfg: CorticalConfig) -> Dict[str, object]:
    rng = np.random.default_rng(cfg.seed)
    x = rng.normal(0.0, 1.0, size=(cfg.samples, cfg.input_dim))

    w1 = rng.normal(0.0, 0.4, size=(cfg.input_dim, cfg.l1_dim))
    w2 = rng.normal(0.0, 0.35, size=(cfg.l1_dim, cfg.l2_dim))
    w3 = rng.normal(0.0, 0.3, size=(cfg.l2_dim, cfg.l3_dim))

    h1 = _nonlinear(x @ w1)
    h2 = _nonlinear(h1 @ w2)
    h3 = _nonlinear(h2 @ w3)

    var_x = float(np.mean(np.var(x, axis=0)))
    var_h1 = float(np.mean(np.var(h1, axis=0)))
    var_h2 = float(np.mean(np.var(h2, axis=0)))
    var_h3 = float(np.mean(np.var(h3, axis=0)))

    # Selectivity proxy: mean absolute activation.
    sel1 = float(np.mean(np.abs(h1)))
    sel2 = float(np.mean(np.abs(h2)))
    sel3 = float(np.mean(np.abs(h3)))

    # Abstraction proxy: depth-weighted reduction in dimensional variance.
    abstraction = (var_x - var_h3) / max(var_x, 1e-9)

    rows: List[Dict[str, float]] = [
        {"layer": 0, "dim": cfg.input_dim, "mean_var": round(var_x, 6), "selectivity": round(float(np.mean(np.abs(x))), 6)},
        {"layer": 1, "dim": cfg.l1_dim, "mean_var": round(var_h1, 6), "selectivity": round(sel1, 6)},
        {"layer": 2, "dim": cfg.l2_dim, "mean_var": round(var_h2, 6), "selectivity": round(sel2, 6)},
        {"layer": 3, "dim": cfg.l3_dim, "mean_var": round(var_h3, 6), "selectivity": round(sel3, 6)},
    ]

    # Sensitivity envelope: perturb depth readout weights around nominal.
    envelope = []
    for scale in [0.9, 1.0, 1.1]:
        h3_p = _nonlinear(h2 @ (scale * w3))
        var_h3_p = float(np.mean(np.var(h3_p, axis=0)))
        abstraction_p = (var_x - var_h3_p) / max(var_x, 1e-9)
        envelope.append({"scale_w3": scale, "abstraction_proxy": round(float(abstraction_p), 6)})

    return {
        "model": "cortical_organization",
        "config": cfg.__dict__,
        "summary": {
            "abstraction_proxy": round(float(abstraction), 6),
            "selectivity_gain_l3_over_l1": round(sel3 / max(sel1, 1e-9), 6),
            "variance_ratio_l3_over_input": round(var_h3 / max(var_x, 1e-9), 6),
        },
        "layer_metrics": rows,
        "diagnostics": {"sensitivity_envelope": envelope},
    }


def write_report(report: Dict[str, object]) -> Path:
    payload = augment_report(__file__, report)
    return write_contract_report(__file__, payload)


def main() -> None:
    cfg = CorticalConfig()
    report = run_cortical_model(cfg)
    out_path = write_report(report)
    s = report["summary"]
    print("Cortical organization (GU)")
    print(f"- abstraction proxy: {s['abstraction_proxy']}")
    print(f"- selectivity gain l3/l1: {s['selectivity_gain_l3_over_l1']}")
    print(f"- report: {out_path}")


if __name__ == "__main__":
    main()
