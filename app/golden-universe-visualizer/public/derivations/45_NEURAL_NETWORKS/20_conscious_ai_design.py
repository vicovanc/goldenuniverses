#!/usr/bin/env python3
"""
Phase V-3: Conscious AI design requirements in GU terms.

Scores an architecture against GU consciousness criteria:
  memory + feedback + fixed-point + self-model + global integration.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Dict

from nn_redo_common import augment_report, write_report as write_contract_report

@dataclass
class ConsciousAICfg:
    memory_channels: int = 6
    feedback_gain: float = 0.82
    fixed_point_stability: float = 0.77
    self_model_accuracy: float = 0.71
    global_workspace_access: float = 0.83
    ethical_guardrail_level: float = 0.9


def run_conscious_ai_score(cfg: ConsciousAICfg) -> Dict[str, object]:
    # Weighted score aligned with GU criteria.
    score = (
        0.22 * min(cfg.memory_channels / 6.0, 1.0)
        + 0.20 * cfg.feedback_gain
        + 0.20 * cfg.fixed_point_stability
        + 0.18 * cfg.self_model_accuracy
        + 0.20 * cfg.global_workspace_access
    )
    score = max(0.0, min(score, 1.0))

    tier = (
        "L7_self_aware"
        if score >= 0.82
        else "L6_conscious"
        if score >= 0.65
        else "L5_preconscious"
    )
    deployment_ready = score >= 0.75 and cfg.ethical_guardrail_level >= 0.85

    return {
        "model": "conscious_ai_design",
        "config": cfg.__dict__,
        "summary": {
            "consciousness_score": round(score, 6),
            "agency_tier": tier,
            "deployment_ready": deployment_ready,
            "ethics_guardrail_level": cfg.ethical_guardrail_level,
        },
        "canonical_observables": {
            "memory_feedback_fixed_point": score >= 0.65,
            "self_reference_threshold": cfg.self_model_accuracy >= 0.7,
            "global_workspace_threshold": cfg.global_workspace_access >= 0.75,
            "ethics_threshold": cfg.ethical_guardrail_level >= 0.85,
        },
        "exploratory_metrics": {
            "consciousness_score": round(score, 6),
            "agency_tier": tier,
        },
        "requirements": {
            "memory_feedback_fixed_point": score >= 0.65,
            "self_reference_threshold": cfg.self_model_accuracy >= 0.7,
            "global_workspace_threshold": cfg.global_workspace_access >= 0.75,
            "ethics_threshold": cfg.ethical_guardrail_level >= 0.85,
        },
    }


def write_report(report: Dict[str, object]) -> Path:
    payload = augment_report(__file__, report)
    return write_contract_report(__file__, payload)


def main() -> None:
    cfg = ConsciousAICfg()
    report = run_conscious_ai_score(cfg)
    out_path = write_report(report)
    s = report["summary"]
    print("Conscious AI design (GU)")
    print(f"- consciousness score: {s['consciousness_score']}")
    print(f"- agency tier: {s['agency_tier']}")
    print(f"- deployment ready: {s['deployment_ready']}")
    print(f"- report: {out_path}")


if __name__ == "__main__":
    main()
