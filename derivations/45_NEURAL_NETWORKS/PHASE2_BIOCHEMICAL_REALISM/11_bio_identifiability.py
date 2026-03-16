#!/usr/bin/env python3
"""
Track C1: Biology identifiability diagnostics (rank, singular spectrum, condition number).
"""

from __future__ import annotations

import importlib.util
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


def _observables(theta: np.ndarray) -> np.ndarray:
    # Compact synthetic map approximating coupled biology observables.
    a, b, c, d, e = theta
    return np.array(
        [
            0.8 * a + 0.2 * b**2 - 0.1 * c,
            np.tanh(0.7 * b + 0.2 * d) + 0.1 * a,
            0.5 * c + 0.4 * e + 0.1 * a * b,
            0.6 * d + 0.2 * c**2 + 0.1 * e,
            np.exp(-0.2 * e) + 0.2 * b,
        ],
        dtype=float,
    )


def run_identifiability() -> Dict[str, object]:
    c = _load("00_common.py", "_p2_common")
    theta0 = np.array([0.5, 0.45, 0.4, 0.35, 0.3], dtype=float)
    j = c.finite_diff_jacobian(_observables, theta0, eps=1e-6)
    u, s, vt = np.linalg.svd(j, full_matrices=False)
    rank = int(np.linalg.matrix_rank(j, tol=1e-8))
    cond = float(s[0] / max(s[-1], 1e-12))

    payload = {
        "model": "bio_identifiability",
        "diagnostic_type": "full_ode_proxy_jacobian",
        "config": {"theta0": theta0.tolist(), "eps": 1e-6},
        "assumptions": [
            "Local identifiability approximated by finite-difference Jacobian around theta0.",
            "Observable map acts as reduced-order proxy for coupled biology dynamics."
        ],
        "units": {"theta": "normalized parameter scale"},
        "parameter_provenance": {"source": "phase2 gate initialization"},
        "summary": {
            "jacobian_rank": rank,
            "jacobian_rank_full": int(j.shape[1]),
            "condition_number": cond,
            "identifiable_full_rank": bool(rank == j.shape[1]),
        },
        "diagnostics": {
            "singular_values": s.tolist(),
            "jacobian": j.tolist(),
        },
    }
    out = c.write_report(__file__, payload)
    return {"output": str(out), "payload": payload}


def main() -> None:
    result = run_identifiability()
    print(f"wrote {result['output']}")


if __name__ == "__main__":
    main()
