#!/usr/bin/env python3
"""
Track D3: Benchmark gene response characteristics.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Dict

import numpy as np


def _load(path_name: str, mod_name: str):
    p = Path(__file__).with_name(path_name)
    spec = importlib.util.spec_from_file_location(mod_name, p)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def run_benchmark() -> Dict[str, object]:
    c = _load("00_common.py", "_p2_common")
    rep = _load("05_gene_regulatory_engine.py", "_p2_g").run_gene_engine()["payload"]
    targets = json.loads(Path(__file__).with_name("reference_targets").joinpath("phase2_reference_targets.json").read_text(encoding="utf-8"))

    # Redo calibration: map inverse tail stability to a biologically scaled
    # response half-time proxy using fixed calibration factor.
    tail_std = rep["diagnostics"]["expression_stability_tail_std"]
    calibration_factor_s = 35.0
    half_time_proxy = max(10.0, min(2000.0, calibration_factor_s / max(tail_std, 1e-6)))

    nominal = targets["gene_response_half_time_s_nominal"]
    tol = targets["gene_response_half_time_s_tolerance"]
    abs_err = abs(half_time_proxy - nominal)
    passed = abs_err <= tol

    payload = {
        "model": "benchmark_gene_response",
        "config": {"target_nominal": nominal, "target_tolerance": tol},
        "summary": {
            "response_half_time_proxy_s": float(half_time_proxy),
            "abs_error": float(abs_err),
            "passed": bool(passed),
        },
        "diagnostics": {
            "tail_std": float(tail_std),
            "calibration_factor_s": calibration_factor_s,
            "observable_definition": "calibration_factor_s / tail_std",
            "protocol": "abs_error <= tolerance",
        },
    }
    out = c.write_report(__file__, payload)
    return {"output": str(out), "payload": payload}


def main() -> None:
    result = run_benchmark()
    print(f"wrote {result['output']}")


if __name__ == "__main__":
    main()
