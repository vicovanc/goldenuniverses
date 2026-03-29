#!/usr/bin/env python3
"""
Shared contracts and utilities for 46_Instant_Communication.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple


PHI = (1.0 + 5.0 ** 0.5) / 2.0
PI = 3.141592653589793
M_P_MEV = 1.22089e22
ALPHA_EM = 1.0 / 137.035999177
LAMBDA_REC_OVER_BETA = 5.077527e-1  # e^phi / pi^2 (rounded)

STATUS_SEMANTICS = {
    "derived_label": "DERIVED",
    "provisional_label": "PROVISIONAL",
    "constrained_label": "CONSTRAINED",
    "policy": "identifiability_and_falsification_required_for_claim_promotion",
}


BENCHMARK_TARGETS: Dict[str, Dict[str, Dict[str, float]]] = {
    "entanglement_geometry_axioms": {
        "resonance_gate_margin": {"nominal": 0.12, "tolerance": 0.2},
    },
    "memory_channel_equations": {
        "channel_gain_nominal": {"nominal": 0.08, "tolerance": 0.08},
    },
    "topological_activation_conditions": {
        "activation_separation_sigma": {"nominal": 2.0, "tolerance": 1.2},
    },
    "signal_encoding_and_control_knobs": {
        "control_stability_index": {"nominal": 0.7, "tolerance": 0.35},
    },
    "causality_and_guardrail_checks": {
        "guardrail_pass_fraction": {"nominal": 1.0, "tolerance": 0.1},
    },
    "benchmark_scenarios": {
        "active_snr_db": {"nominal": 6.0, "tolerance": 6.0},
    },
    "identifiability_and_falsification": {
        "balanced_accuracy": {"nominal": 0.8, "tolerance": 0.2},
    },
    "phase_diagram_and_operating_regions": {
        "viable_window_fraction": {"nominal": 0.2, "tolerance": 0.2},
    },
}


def resonance_values(n_epoch: int) -> Tuple[int, float]:
    x = n_epoch / (PHI * PHI)
    k_res = int(round(x))
    delta = x - k_res
    return k_res, delta


def benchmark_hooks(model: str, summary: Dict[str, Any]) -> Dict[str, Any]:
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


def with_contract(script_path: str, report: Dict[str, Any]) -> Dict[str, Any]:
    model = str(report.get("model", Path(script_path).stem))
    cfg = report.get("config", {})
    summary = report.get("summary", {})

    report.setdefault(
        "assumptions",
        [
            "Geometric entanglement channel is modeled through phase-memory operators.",
            "Conditional signaling claims are benchmark-gated and falsifiable.",
        ],
    )
    report.setdefault("units", {})
    report.setdefault(
        "parameter_provenance",
        {
            "source": "instant_communication_v1",
            "deterministic_seed": cfg.get("seed", "deterministic_by_construction"),
        },
    )
    diagnostics = report.setdefault("diagnostics", {})
    diagnostics["status_semantics"] = STATUS_SEMANTICS
    diagnostics["benchmark_hooks"] = benchmark_hooks(model, summary)
    diagnostics["schema_contract"] = {
        "required_fields_present": all(
            key in report
            for key in [
                "model",
                "config",
                "summary",
                "assumptions",
                "units",
                "parameter_provenance",
                "diagnostics",
            ]
        ),
        "contract_version": "instant_communication_v1",
    }
    return report


def write_report(script_path: str, report: Dict[str, Any]) -> Path:
    script = Path(script_path)
    out_path = script.with_name(f"{script.stem}_report.json")
    out_path.write_text(json.dumps(with_contract(script_path, report), indent=2), encoding="utf-8")
    return out_path


def mean(values: Iterable[float]) -> float:
    vals = list(values)
    return sum(vals) / len(vals) if vals else 0.0
