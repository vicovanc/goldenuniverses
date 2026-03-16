#!/usr/bin/env python3
"""
Track E1: Audit gap between Phase 1 surrogate outputs and Phase 2 mechanistic outputs.
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


def run_gap_audit() -> Dict[str, object]:
    c = _load("00_common.py", "_p2_common")
    p1 = Path(__file__).resolve().parents[1]

    p1_mem = json.loads((p1 / "03_bioelectric_memory_traces_report.json").read_text(encoding="utf-8"))
    p1_ws = json.loads((p1 / "13_global_workspace_theory_report.json").read_text(encoding="utf-8"))
    p1_ai = json.loads((p1 / "20_conscious_ai_design_report.json").read_text(encoding="utf-8"))

    p2_int = _load("06_cell_state_integrator.py", "_p2_i").run_integrator()["payload"]
    p2_score = _load("14_bio_scorecard.py", "_p2_s").run_scorecard()["payload"]

    gaps = {
        "memory_retention_shift": p2_int["summary"]["integrated_protein_A"] - p1_mem["summary"]["retained_vm_post_training"],
        "conscious_gate_shift": p2_score["summary"]["promotion_status"] != "derived",
        "ai_claim_vs_mechanistic_gate": p1_ai["summary"]["deployment_ready"] and (p2_score["summary"]["promotion_status"] != "derived"),
        "workspace_vs_mechanistic_consistency": p1_ws["summary"]["conscious_access_fraction"] > 0.9 and p2_score["summary"]["excitable_tissue"],
    }

    payload = {
        "model": "phase1_phase2_gap_audit",
        "config": {"phase1_dir": str(p1)},
        "summary": {
            "n_gaps_flagged": int(sum(1 for v in gaps.values() if bool(v))),
            "promotion_status_phase2": p2_score["summary"]["promotion_status"],
        },
        "diagnostics": gaps,
        "assumptions": [
            "Phase 1 outputs are surrogate-level baselines.",
            "Phase 2 scorecard status is authoritative for mechanistic promotion."
        ],
        "units": {},
        "parameter_provenance": {"source": "phase1 json reports + phase2 scorecard"},
    }
    out = c.write_report(__file__, payload)
    return {"output": str(out), "payload": payload}


def main() -> None:
    result = run_gap_audit()
    print(f"wrote {result['output']}")


if __name__ == "__main__":
    main()
