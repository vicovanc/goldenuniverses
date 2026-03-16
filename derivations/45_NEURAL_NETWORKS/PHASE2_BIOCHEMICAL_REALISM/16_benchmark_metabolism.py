#!/usr/bin/env python3
"""
Track D2: Benchmark metabolism outputs.
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


def run_benchmark() -> Dict[str, object]:
    c = _load("00_common.py", "_p2_common")
    rep = _load("04_metabolic_redox_engine.py", "_p2_met").run_metabolic()["payload"]
    targets = json.loads(Path(__file__).with_name("reference_targets").joinpath("phase2_reference_targets.json").read_text(encoding="utf-8"))

    # Redo calibration: use an ATP-dominance turnover index on [0,1] that is
    # stable across mechanistic runs and comparable to nominal metabolic fitness.
    atp = float(rep["summary"]["final_atp"])
    nadh = float(rep["summary"]["final_nadh"])
    val = atp / max(atp + nadh, 1e-12)
    nominal = targets["atp_turnover_proxy_nominal"]
    tol = targets["atp_turnover_proxy_tolerance"]
    abs_err = abs(val - nominal)
    passed = abs_err <= tol

    payload = {
        "model": "benchmark_metabolism",
        "config": {"target_nominal": nominal, "target_tolerance": tol},
        "summary": {
            "observed_atp_turnover_proxy": val,
            "abs_error": abs_err,
            "passed": passed,
        },
        "diagnostics": {
            "protocol": "abs_error <= tolerance",
            "observable_definition": "final_atp / (final_atp + final_nadh)",
        },
    }
    out = c.write_report(__file__, payload)
    return {"output": str(out), "payload": payload}


def main() -> None:
    result = run_benchmark()
    print(f"wrote {result['output']}")


if __name__ == "__main__":
    main()
