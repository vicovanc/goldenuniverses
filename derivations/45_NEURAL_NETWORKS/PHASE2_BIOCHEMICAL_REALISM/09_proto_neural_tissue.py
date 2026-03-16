#!/usr/bin/env python3
"""
Track B3: Proto-neural tissue excitation thresholds.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Dict, Optional

import numpy as np


def _load(path_name: str, mod_name: str):
    p = Path(__file__).with_name(path_name)
    spec = importlib.util.spec_from_file_location(mod_name, p)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def run_proto_tissue(
    *,
    n: int = 60,
    steps: int = 3000,
    dt: float = 0.005,
    seed_nodes: int = 3,
    coupling: float = 0.18,
    leak: float = 0.07,
    threshold: float = 0.42,
    self_excitation: float = 0.03,
    write_report: bool = True,
) -> Dict[str, object]:
    c = _load("00_common.py", "_p2_common")
    v = np.zeros(n, dtype=float)
    if seed_nodes > 0:
        v[:seed_nodes] = 1.0  # seed stimulus
    activation_count = 0

    for _ in range(steps):
        left = np.roll(v, 1)
        right = np.roll(v, -1)
        drive = coupling * (left + right - 2.0 * v)
        dv = drive - leak * v + self_excitation * (v > threshold)
        v += dt * dv
        v = np.clip(v, 0.0, 1.2)
        activation_count += int(np.sum(v > threshold))

    active_fraction = float(np.mean(v > threshold))
    coherence = float(np.abs(np.mean(np.exp(1j * v))))

    payload = {
        "model": "proto_neural_tissue",
        "config": {
            "n_nodes": n,
            "steps": steps,
            "dt": dt,
            "seed_nodes": seed_nodes,
            "coupling": coupling,
            "leak": leak,
            "threshold": threshold,
            "self_excitation": self_excitation,
        },
        "assumptions": [
            "Diffusive coupling approximates electrotonic spread.",
            "Threshold activity proxy indicates excitable tissue behavior."
        ],
        "units": {"v": "normalized bioelectric state", "time": "s"},
        "parameter_provenance": {"source": "phase2 tissue initialization"},
        "summary": {
            "final_active_fraction": active_fraction,
            "final_coherence": coherence,
            "mean_activation_events_per_step": float(activation_count / steps),
        },
        "diagnostics": {
            "excitable_regime_detected": bool(active_fraction > 0.2),
            "final_state_mean": float(np.mean(v)),
            "final_state_std": float(np.std(v)),
        },
    }
    if write_report:
        out = c.write_report(__file__, payload)
        return {"output": str(out), "payload": payload}
    return {"output": None, "payload": payload}


def main() -> None:
    result = run_proto_tissue()
    print(f"wrote {result['output']}")


if __name__ == "__main__":
    main()
