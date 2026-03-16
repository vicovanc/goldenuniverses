#!/usr/bin/env python3
"""
Track C4: Global Phase 2 biology scorecard.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Dict


def _load(path_name: str, mod_name: str):
    p = Path(__file__).with_name(path_name)
    spec = importlib.util.spec_from_file_location(mod_name, p)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def run_scorecard() -> Dict[str, object]:
    c = _load("00_common.py", "_p2_common")
    rep6 = _load("06_cell_state_integrator.py", "_p2_6").run_integrator()["payload"]
    rep8 = _load("08_multicellular_transition.py", "_p2_8").run_transition()["payload"]
    rep9 = _load("09_proto_neural_tissue.py", "_p2_9").run_proto_tissue()["payload"]
    rep10 = _load("10_neural_circuit_emergence.py", "_p2_10").run_circuit_emergence()["payload"]
    rep11 = _load("11_bio_identifiability.py", "_p2_11").run_identifiability()["payload"]
    rep12 = _load("12_bio_falsification_gates.py", "_p2_12").run_falsification()["payload"]
    rep13 = _load("13_bio_promotion_rules.py", "_p2_13").run_promotion()["payload"]

    payload = {
        "model": "bio_scorecard",
        "config": {"scorecard_version": "phase2_v1"},
        "assumptions": ["Scorecard aggregates mechanistic, evolution, and gate outputs."],
        "units": {},
        "parameter_provenance": {"source": "phase2 scorecard aggregation"},
        "summary": {
            "promotion_status": rep13["summary"]["promotion_status"],
            "identifiability_rank": rep11["summary"]["jacobian_rank"],
            "identifiability_full": rep11["summary"]["jacobian_rank_full"],
            "falsification_passed": rep12["summary"]["n_passed"],
            "falsification_total": rep12["summary"]["n_hypotheses"],
            "cluster_gain": rep8["summary"]["cluster_index_gain"],
            # Keep raw baseline observables and resolved gate status separate.
            "excitable_tissue_baseline": rep9["diagnostics"]["excitable_regime_detected"],
            "sensorimotor_responsive_baseline": rep10["diagnostics"]["stimulus_responsive"],
            "excitable_tissue_gate_resolved": rep12["gate_status"]["excitable_tissue_hypothesis"] == "pass",
            "sensorimotor_gate_resolved": rep12["gate_status"]["sensorimotor_emergence_hypothesis"] == "pass",
            # Backward-compatible keys consumed by downstream scripts.
            "excitable_tissue": rep12["gate_status"]["excitable_tissue_hypothesis"] == "pass",
            "sensorimotor_responsive": rep12["gate_status"]["sensorimotor_emergence_hypothesis"] == "pass",
            "phase21_gate_status": rep12["gate_status"],
        },
        "diagnostics": {
            "conservation_checks": rep6["diagnostics"]["conservation_checks"],
            "gate_status": rep13["gate_status"],
        },
    }
    out = c.write_report(__file__, payload)
    return {"output": str(out), "payload": payload}


def main() -> None:
    result = run_scorecard()
    print(f"wrote {result['output']}")


if __name__ == "__main__":
    main()
