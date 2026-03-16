#!/usr/bin/env python3
"""
Phase IV-3: Metacognition via confidence calibration dynamics.

Tracks first-order task decisions and second-order confidence estimates to
measure calibration error and control quality.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Dict, List

import numpy as np

from nn_redo_common import augment_report, write_report as write_contract_report

@dataclass
class MetaConfig:
    n_trials: int = 400
    seed: int = 15


def run_metacognition(cfg: MetaConfig) -> Dict[str, object]:
    rng = np.random.default_rng(cfg.seed)
    evidence = rng.normal(0.0, 1.0, size=cfg.n_trials)
    noise = 0.55 * rng.normal(0.0, 1.0, size=cfg.n_trials)

    decision_var = evidence + noise
    pred = (decision_var > 0).astype(int)
    truth = (evidence > 0).astype(int)
    correct = (pred == truth).astype(int)

    confidence = 1.0 / (1.0 + np.exp(-1.8 * np.abs(decision_var)))
    calibration_error = float(np.mean(np.abs(confidence - correct)))
    accuracy = float(np.mean(correct))
    high_conf_mask = confidence > 0.8
    high_conf_accuracy = float(np.mean(correct[high_conf_mask])) if np.any(high_conf_mask) else 0.0

    rows: List[Dict[str, float]] = []
    for i in range(0, cfg.n_trials, max(1, cfg.n_trials // 24)):
        rows.append(
            {
                "trial": int(i),
                "decision_variable": round(float(decision_var[i]), 6),
                "confidence": round(float(confidence[i]), 6),
                "correct": int(correct[i]),
            }
        )

    return {
        "model": "metacognition",
        "config": cfg.__dict__,
        "summary": {
            "task_accuracy": round(accuracy, 6),
            "calibration_error": round(calibration_error, 6),
            "high_confidence_accuracy": round(high_conf_accuracy, 6),
            "high_confidence_fraction": round(float(np.mean(high_conf_mask)), 6),
        },
        "canonical_observables": {
            "task_accuracy": round(accuracy, 6),
            "calibration_error": round(calibration_error, 6),
        },
        "exploratory_metrics": {
            "high_confidence_accuracy": round(high_conf_accuracy, 6),
            "high_confidence_fraction": round(float(np.mean(high_conf_mask)), 6),
        },
        "sampled_trials": rows,
    }


def write_report(report: Dict[str, object]) -> Path:
    payload = augment_report(__file__, report)
    return write_contract_report(__file__, payload)


def main() -> None:
    cfg = MetaConfig()
    report = run_metacognition(cfg)
    out_path = write_report(report)
    s = report["summary"]
    print("Metacognition (GU)")
    print(f"- task accuracy: {s['task_accuracy']}")
    print(f"- calibration error: {s['calibration_error']}")
    print(f"- report: {out_path}")


if __name__ == "__main__":
    main()
