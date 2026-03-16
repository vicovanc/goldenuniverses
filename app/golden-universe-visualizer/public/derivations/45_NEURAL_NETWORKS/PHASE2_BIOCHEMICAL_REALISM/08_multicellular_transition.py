#!/usr/bin/env python3
"""
Track B2: Multicellular transition via adhesion + signaling coupling.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Dict

import numpy as np


def _load(path_name: str, mod_name: str):
    p = Path(__file__).with_name(path_name)
    spec = importlib.util.spec_from_file_location(mod_name, p)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def run_transition() -> Dict[str, object]:
    c = _load("00_common.py", "_p2_common")
    rng = np.random.default_rng(808)
    n = 120
    steps = 240
    adhesion = np.clip(rng.normal(0.35, 0.12, size=n), 0.01, 0.95)
    signaling = np.clip(rng.normal(0.30, 0.10, size=n), 0.01, 0.95)
    gap = np.clip(rng.normal(0.20, 0.08, size=n), 0.01, 0.9)

    cluster_index_hist = []
    for _ in range(steps):
        mean_a = float(np.mean(adhesion))
        mean_s = float(np.mean(signaling))
        mean_g = float(np.mean(gap))
        # Cooperative growth with saturation.
        adhesion += 0.02 * (mean_s + 0.5 * mean_g) * (1.0 - adhesion) - 0.005 * adhesion
        signaling += 0.02 * (mean_a + mean_g) * (1.0 - signaling) - 0.006 * signaling
        gap += 0.03 * (mean_a + 0.5 * mean_s) * (1.0 - gap) - 0.007 * gap
        # stochastic perturbations
        adhesion += rng.normal(0, 0.003, size=n)
        signaling += rng.normal(0, 0.003, size=n)
        gap += rng.normal(0, 0.003, size=n)
        adhesion = np.clip(adhesion, 0.0, 1.0)
        signaling = np.clip(signaling, 0.0, 1.0)
        gap = np.clip(gap, 0.0, 1.0)

        cluster_idx = float(np.mean(0.5 * adhesion + 0.3 * signaling + 0.2 * gap))
        cluster_index_hist.append(cluster_idx)

    payload = {
        "model": "multicellular_transition",
        "config": {"n_cells": n, "steps": steps, "seed": 808},
        "assumptions": [
            "Adhesion, signaling, and gap-junction coupling co-evolve under cooperative feedback.",
            "Transition index approximates multicellular integration state."
        ],
        "units": {"traits": "0..1 normalized"},
        "parameter_provenance": {"source": "phase2 transition initialization"},
        "summary": {
            "initial_cluster_index": float(cluster_index_hist[0]),
            "final_cluster_index": float(cluster_index_hist[-1]),
            "cluster_index_gain": float(cluster_index_hist[-1] - cluster_index_hist[0]),
            "final_trait_means": {
                "adhesion": float(np.mean(adhesion)),
                "signaling": float(np.mean(signaling)),
                "gap_coupling": float(np.mean(gap)),
            },
        },
        "diagnostics": {
            "transition_reached_idx_gt_0p55": bool(cluster_index_hist[-1] > 0.55),
            "cluster_index_std_tail": float(np.std(cluster_index_hist[-40:])),
        },
    }
    out = c.write_report(__file__, payload)
    return {"output": str(out), "payload": payload}


def main() -> None:
    result = run_transition()
    print(f"wrote {result['output']}")


if __name__ == "__main__":
    main()
