#!/usr/bin/env python3
"""
Track E2: Relabel claims according to Phase 2 gates and benchmarks.
Also writes 22_phase2_final_report.md.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Dict
import json


def _load(path_name: str, mod_name: str):
    p = Path(__file__).with_name(path_name)
    spec = importlib.util.spec_from_file_location(mod_name, p)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def run_relabeling() -> Dict[str, object]:
    c = _load("00_common.py", "_p2_common")
    score = _load("14_bio_scorecard.py", "_p2_s").run_scorecard()["payload"]
    bench15 = _load("15_benchmark_membrane_dynamics.py", "_p2_b15").run_benchmark()["payload"]
    bench16 = _load("16_benchmark_metabolism.py", "_p2_b16").run_benchmark()["payload"]
    bench17 = _load("17_benchmark_gene_response.py", "_p2_b17").run_benchmark()["payload"]
    bench18 = _load("18_benchmark_tissue_excitation.py", "_p2_b18").run_benchmark()["payload"]
    bench19 = _load("19_benchmark_neural_metrics.py", "_p2_b19").run_benchmark()["payload"]
    gap = _load("20_phase1_phase2_gap_audit.py", "_p2_g").run_gap_audit()["payload"]

    benchmark_pass = all(
        [
            bench15["summary"]["passed"],
            bench16["summary"]["passed"],
            bench17["summary"]["passed"],
            bench18["summary"]["passed"],
            bench19["summary"]["passed"],
        ]
    )
    promotion = score["summary"]["promotion_status"]
    if promotion == "derived" and benchmark_pass:
        claim_label = "DERIVED"
    elif promotion in {"derived", "constrained"} and benchmark_pass:
        claim_label = "CONSTRAINED"
    else:
        claim_label = "PROVISIONAL"

    payload = {
        "model": "claim_relabeling",
        "config": {"benchmark_required": True},
        "summary": {
            "phase2_claim_label": claim_label,
            "promotion_status": promotion,
            "benchmark_pass": benchmark_pass,
            "gap_flags": gap["summary"]["n_gaps_flagged"],
        },
        "diagnostics": {
            "benchmark_passes": {
                "membrane": bench15["summary"]["passed"],
                "metabolism": bench16["summary"]["passed"],
                "gene_response": bench17["summary"]["passed"],
                "tissue_excitation": bench18["summary"]["passed"],
                "neural_metrics": bench19["summary"]["passed"],
            }
        },
        "assumptions": ["Claim labels are machine-governed by gates + benchmarks."],
        "units": {},
        "parameter_provenance": {"source": "phase2 scorecard + benchmark reports"},
    }
    out = c.write_report(__file__, payload)

    # Write final markdown contradiction-ledger style report.
    md_path = Path(__file__).with_name("22_phase2_final_report.md")
    md_path.write_text(
        (
            "# Phase 2 Final Report (Mechanistic Biology Closure)\n\n"
            f"- Promotion status: `{promotion}`\n"
            f"- Benchmark suite pass: `{benchmark_pass}`\n"
            f"- Phase 2 claim label: `{claim_label}`\n"
            f"- Gap flags vs Phase 1: `{gap['summary']['n_gaps_flagged']}`\n\n"
            "## Contradiction Ledger\n\n"
            "- If promotion is not `derived`, all downstream narrative claims remain non-derived.\n"
            "- Benchmark failure on any module blocks full closure promotion.\n"
            "- Phase 1 surrogate readiness cannot override Phase 2 mechanistic gate outputs.\n\n"
            "## Module Gate Summary\n\n"
            f"- Identifiability rank: `{score['summary']['identifiability_rank']}/{score['summary']['identifiability_full']}`\n"
            f"- Falsification passed: `{score['summary']['falsification_passed']}/{score['summary']['falsification_total']}`\n"
            f"- Excitable tissue detected: `{score['summary']['excitable_tissue']}`\n"
            f"- Sensorimotor responsive: `{score['summary']['sensorimotor_responsive']}`\n\n"
            "## Rule\n\n"
            "Keep labels strict (`DERIVED`, `CONSTRAINED`, `PROVISIONAL`) and mirror machine outputs in documentation.\n"
        ),
        encoding="utf-8",
    )

    return {"output": str(out), "payload": payload, "final_md": str(md_path)}


def main() -> None:
    result = run_relabeling()
    print(f"wrote {result['output']}")
    print(f"wrote {result['final_md']}")


if __name__ == "__main__":
    main()
