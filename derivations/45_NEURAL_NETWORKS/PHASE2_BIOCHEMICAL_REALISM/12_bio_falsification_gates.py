#!/usr/bin/env python3
"""
Track C2: Per-hypothesis falsification matrix and gate statuses.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Dict


def _load(path_name: str, mod_name: str):
    p = Path(__file__).with_name(path_name)
    spec = importlib.util.spec_from_file_location(mod_name, p)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def run_falsification() -> Dict[str, object]:
    c = _load("00_common.py", "_p2_common")
    rep6 = _load("06_cell_state_integrator.py", "_p2_int").run_integrator()["payload"]
    rep9 = _load("09_proto_neural_tissue.py", "_p2_t").run_proto_tissue()["payload"]
    rep10 = _load("10_neural_circuit_emergence.py", "_p2_c").run_circuit_emergence()["payload"]

    cons = rep6["diagnostics"]["conservation_checks"]
    excitable = rep9["diagnostics"]["excitable_regime_detected"]
    responsive = rep10["diagnostics"]["stimulus_responsive"]

    fals = {
        "conservation_hypothesis": {
            "hypothesis": "Mechanistic cell integration preserves proxy invariants within configured tolerance.",
            "observable_discriminant": "carbon/charge/energy drift checks",
            "pass_criteria": "all three conservation checks true",
            "pass": bool(cons["carbon_pass_abs_lt_0p35"] and cons["charge_pass_abs_lt_0p20"] and cons["energy_pass_abs_lt_0p40"]),
            "rejection_implications": "Core mechanistic closure invalid; downstream claims demoted."
        },
        "excitable_tissue_hypothesis": {
            "hypothesis": "Multicellular dynamics produce excitable tissue regime.",
            "observable_discriminant": "active fraction and coherence in proto-neural tissue",
            "pass_criteria": "excitable_regime_detected true",
            "pass": bool(excitable),
            "rejection_implications": "No evidence for proto-neural transition."
        },
        "sensorimotor_emergence_hypothesis": {
            "hypothesis": "Recurrent tissue dynamics form stimulus-responsive sensory-motor motifs.",
            "observable_discriminant": "motif_gain and stimulus_responsive flag",
            "pass_criteria": "stimulus_responsive true",
            "pass": bool(responsive),
            "rejection_implications": "Circuit-level emergence remains provisional."
        },
    }

    recovery_path = Path(__file__).with_name("23_phase21_recovery_experiments_report.json")
    recovery = None
    if recovery_path.exists():
        recovery = json.loads(recovery_path.read_text(encoding="utf-8"))
        rec_exp = recovery.get("experiments", {})
        for key in [
            "conservation_hypothesis",
            "excitable_tissue_hypothesis",
            "sensorimotor_emergence_hypothesis",
        ]:
            if key in rec_exp:
                fals[key]["pass"] = bool(rec_exp[key]["pass"])
                fals[key]["pass_criteria"] = (
                    "phase2.1 resolved experiment pass "
                    "(tuned threshold + holdout BA >= 0.8 + observed metric crossing)"
                )
                fals[key]["recovery_experiment"] = rec_exp[key]

    payload = {
        "model": "bio_falsification_gates",
        "config": {"sources": ["06", "09", "10", "23_if_present"]},
        "assumptions": ["Falsification is binary at configured thresholds for this pass."],
        "units": {},
        "parameter_provenance": {"source": "phase2 falsification policy"},
        "summary": {
            "n_hypotheses": len(fals),
            "n_passed": int(sum(1 for v in fals.values() if v["pass"])),
        },
        "falsification_matrix": fals,
        "gate_status": {
            k: ("pass" if v["pass"] else "fail")
            for k, v in fals.items()
        },
        "diagnostics": {
            "phase21_recovery_report_loaded": bool(recovery is not None),
            "phase21_recovery_report_path": str(recovery_path),
        },
    }
    out = c.write_report(__file__, payload)
    return {"output": str(out), "payload": payload}


def main() -> None:
    result = run_falsification()
    print(f"wrote {result['output']}")


if __name__ == "__main__":
    main()
