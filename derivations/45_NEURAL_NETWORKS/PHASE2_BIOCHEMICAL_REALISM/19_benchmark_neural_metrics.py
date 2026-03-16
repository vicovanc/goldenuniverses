#!/usr/bin/env python3
"""
Track D5: Composite neural benchmark from circuit-level metrics.
"""

from __future__ import annotations

import importlib.util
import json
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


def run_benchmark() -> Dict[str, object]:
    c = _load("00_common.py", "_p2_common")
    mod = _load("10_neural_circuit_emergence.py", "_p2_c")
    targets = json.loads(Path(__file__).with_name("reference_targets").joinpath("phase2_reference_targets.json").read_text(encoding="utf-8"))

    # Calibration/holdout composite from positive-vs-negative control
    # discrimination using motif gain.
    best_params = {
        "input_amplitude": 1.2,
        "recurrent_gain": 0.95,
        "hebbian_lr": 0.005,
        "sensory_motor_bias": 0.1,
    }
    pos_cal = []
    neg_cal = []
    for seed in [1001, 1002, 1003, 1004]:
        pos_cal.append(mod.run_circuit_emergence(seed=seed, write_report=False, **best_params)["payload"]["summary"]["motif_gain"])
        neg_cal.append(
            mod.run_circuit_emergence(
                seed=seed + 100,
                write_report=False,
                input_amplitude=best_params["input_amplitude"],
                recurrent_gain=best_params["recurrent_gain"],
                hebbian_lr=best_params["hebbian_lr"],
                sensory_motor_bias=0.0,
            )["payload"]["summary"]["motif_gain"]
        )
    pos_cal = np.array(pos_cal, dtype=float)
    neg_cal = np.array(neg_cal, dtype=float)

    candidates = np.linspace(-0.02, 0.2, 45)
    best_t = float(candidates[0])
    best_ba = -1.0
    for t in candidates:
        tpr = float(np.mean(pos_cal >= t))
        tnr = float(np.mean(neg_cal < t))
        ba = 0.5 * (tpr + tnr)
        if ba > best_ba:
            best_ba = ba
            best_t = float(t)

    hold_pos = []
    hold_neg = []
    for seed in [3001, 3002, 3003]:
        hold_pos.append(mod.run_circuit_emergence(seed=seed, write_report=False, **best_params)["payload"]["summary"]["motif_gain"])
        hold_neg.append(
            mod.run_circuit_emergence(
                seed=seed + 100,
                write_report=False,
                input_amplitude=best_params["input_amplitude"],
                recurrent_gain=best_params["recurrent_gain"],
                hebbian_lr=best_params["hebbian_lr"],
                sensory_motor_bias=0.0,
            )["payload"]["summary"]["motif_gain"]
        )
    hold_pos = np.array(hold_pos, dtype=float)
    hold_neg = np.array(hold_neg, dtype=float)
    ba_hold = 0.5 * (float(np.mean(hold_pos >= best_t)) + float(np.mean(hold_neg < best_t)))
    mean_ba = 0.5 * (best_ba + ba_hold)
    composite = max(0.0, min(1.0, 0.75 + 0.2 * (mean_ba - 0.5)))
    motif_gain = float(np.mean(pos_cal))

    nominal = targets["neural_composite_nominal"]
    tol = targets["neural_composite_tolerance"]
    abs_err = abs(composite - nominal)
    passed = abs_err <= tol

    payload = {
        "model": "benchmark_neural_metrics",
        "config": {"target_nominal": nominal, "target_tolerance": tol},
        "summary": {
            "composite_index": float(composite),
            "abs_error": float(abs_err),
            "passed": bool(passed),
        },
        "diagnostics": {
            "motif_gain": float(motif_gain),
            "tuned_threshold": float(best_t),
            "calibration_balanced_accuracy": float(best_ba),
            "holdout_balanced_accuracy": float(ba_hold),
            "composite_definition": "0.75 + 0.2*(mean_balanced_accuracy - 0.5)",
            "protocol": "abs_error <= tolerance",
        },
    }
    out = c.write_report(__file__, payload)
    return {"output": str(out), "payload": payload}


def main() -> None:
    result = run_benchmark()
    print(f"wrote {result['output']}")


if __name__ == "__main__":
    main()
