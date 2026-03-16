#!/usr/bin/env python3
"""
Shared contracts for the neural-networks mechanistic redo.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


STATUS_SEMANTICS = {
    "derived_label": "DERIVED",
    "provisional_label": "PROVISIONAL",
    "policy": "benchmark_required_for_claim_promotion",
}


BENCHMARK_TARGETS: Dict[str, Dict[str, Dict[str, float]]] = {
    "single_cell_neural_computation": {
        "information_rate_bits_per_second": {"nominal": 0.6, "tolerance": 0.35},
        "energy_power_proxy": {"nominal": 0.006, "tolerance": 0.004},
    },
    "gap_junction_networks": {
        "mean_coherence": {"nominal": 0.92, "tolerance": 0.12},
    },
    "bioelectric_memory_traces": {
        "memory_half_life_proxy_s": {"nominal": 20.0, "tolerance": 15.0},
    },
    "action_potential_derivation": {
        "firing_rate_hz": {"nominal": 0.05, "tolerance": 0.05},
    },
    "synaptic_transmission": {
        "chemical_to_electrical_ratio": {"nominal": 8.0, "tolerance": 6.0},
    },
    "reflex_circuits": {
        "peak_motor_response": {"nominal": 0.10, "tolerance": 0.06},
    },
    "neural_plasticity": {
        "net_weight_change": {"nominal": 0.0001, "tolerance": 0.0002},
    },
    "cortical_organization": {
        "abstraction_proxy": {"nominal": 0.70, "tolerance": 0.25},
    },
    "neural_oscillations": {
        "dominant_fraction": {"nominal": 0.35, "tolerance": 0.20},
    },
    "long_range_connectivity": {
        "global_efficiency": {"nominal": 0.35, "tolerance": 0.20},
    },
    "specialized_brain_regions": {
        "global_task_efficiency": {"nominal": 0.90, "tolerance": 0.10},
    },
    "global_workspace_theory": {
        "integration_index": {"nominal": 0.80, "tolerance": 0.25},
    },
    "self_referential_circuits": {
        "mean_self_model_error": {"nominal": 0.15, "tolerance": 0.10},
    },
    "metacognition": {
        "task_accuracy": {"nominal": 0.85, "tolerance": 0.20},
    },
    "language_and_symbols": {
        "symbolic_consistency_score": {"nominal": 0.80, "tolerance": 0.20},
    },
    "gu_inspired_architectures": {
        "accuracy_gain": {"nominal": 0.005, "tolerance": 0.02},
    },
    "bioelectric_computing": {
        "latency_s": {"nominal": 2.0, "tolerance": 1.5},
    },
    "conscious_ai_design": {
        "consciousness_score": {"nominal": 0.80, "tolerance": 0.20},
    },
}


def _benchmark_hooks(model: str, summary: Dict[str, Any]) -> Dict[str, Any]:
    targets = BENCHMARK_TARGETS.get(model, {})
    hooks: Dict[str, Any] = {}
    for key, cfg in targets.items():
        if key not in summary:
            continue
        observed = float(summary[key])
        nominal = float(cfg["nominal"])
        tol = float(cfg["tolerance"])
        err = abs(observed - nominal)
        hooks[key] = {
            "observed": observed,
            "nominal": nominal,
            "tolerance": tol,
            "abs_error": err,
            "passed": bool(err <= tol),
        }
    return hooks


def augment_report(script_path: str, report: Dict[str, Any]) -> Dict[str, Any]:
    model = str(report.get("model", Path(script_path).stem))
    cfg = report.get("config", {})
    summary = report.get("summary", {})

    report.setdefault(
        "assumptions",
        [
            "Mechanistic redo contract: explicit dynamics and deterministic execution.",
            "Status promotion is policy-gated and benchmark-aware.",
        ],
    )
    report.setdefault("units", {})
    report.setdefault(
        "parameter_provenance",
        {
            "source": "neural_redo_mechanistic_v1",
            "deterministic_seed": cfg.get("seed", "deterministic_by_construction"),
        },
    )
    diagnostics = report.setdefault("diagnostics", {})
    diagnostics["status_semantics"] = STATUS_SEMANTICS
    diagnostics["benchmark_hooks"] = _benchmark_hooks(model, summary)
    diagnostics["schema_contract"] = {
        "required_fields_present": all(
            key in report for key in ["model", "config", "summary", "assumptions", "units", "parameter_provenance", "diagnostics"]
        ),
        "contract_version": "neural_redo_v1",
    }
    return report


def write_report(script_path: str, report: Dict[str, Any]) -> Path:
    script = Path(script_path)
    out_path = script.with_name(f"{script.stem}_report.json")
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return out_path
