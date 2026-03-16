#!/usr/bin/env python3
"""
Track D1: Benchmark membrane dynamics against reference targets.
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
    rep = _load("03_membrane_transport_engine.py", "_p2_m").run_membrane()["payload"]
    targets = json.loads(Path(__file__).with_name("reference_targets").joinpath("phase2_reference_targets.json").read_text(encoding="utf-8"))

    vm = rep["summary"]["vm_rest_mV"]
    nominal = targets["resting_vm_mV_nominal"]
    tol = targets["resting_vm_mV_tolerance"]
    abs_err = abs(vm - nominal)
    passed = abs_err <= tol

    payload = {
        "model": "benchmark_membrane_dynamics",
        "config": {"target_nominal": nominal, "target_tolerance": tol},
        "summary": {
            "observed_vm_rest_mV": vm,
            "abs_error": abs_err,
            "passed": passed,
        },
        "diagnostics": {"protocol": "abs_error <= tolerance"},
    }
    out = c.write_report(__file__, payload)
    return {"output": str(out), "payload": payload}


def main() -> None:
    result = run_benchmark()
    print(f"wrote {result['output']}")


if __name__ == "__main__":
    main()
