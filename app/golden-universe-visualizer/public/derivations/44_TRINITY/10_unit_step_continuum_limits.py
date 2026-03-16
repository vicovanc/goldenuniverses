#!/usr/bin/env python3
"""
Unit-step -> continuum limit probes for Trinity constants and torus correction.

Tests:
  1) e from multiplicative unit-step compounding: (1 + 1/n)^n
  2) phi from unit-step Fibonacci recursion ratio F_{n+1}/F_n
  3) pi from pixelated lattice-circle counting
  4) torus modular defect from pixelated sampling of sn^2 over one period:
       1 - E/K = m * <sn^2>_period
     and induced electron correction deltaC_e = (1 - E/K)/N_e
"""

from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy import special


def e_compounding_rows(n_values: list[int]) -> list[dict]:
    rows = []
    for n in n_values:
        val = (1.0 + 1.0 / n) ** n
        err = abs(val - math.e)
        rows.append(
            {
                "n": int(n),
                "value": float(val),
                "abs_error": float(err),
                "rel_error": float(err / math.e),
            }
        )
    return rows


def phi_fibonacci_rows(n_values: list[int]) -> list[dict]:
    # Build unit-step recursion F_{k+1}=F_k+F_{k-1}
    n_max = max(n_values)
    f = [0, 1]
    for _ in range(2, n_max + 2):
        f.append(f[-1] + f[-2])

    phi = (1.0 + math.sqrt(5.0)) / 2.0
    rows = []
    for n in n_values:
        ratio = f[n + 1] / f[n]
        err = abs(ratio - phi)
        rows.append(
            {
                "n": int(n),
                "ratio_Fn1_over_Fn": float(ratio),
                "abs_error": float(err),
                "rel_error": float(err / phi),
            }
        )
    return rows


def pi_lattice_rows(r_values: list[int]) -> list[dict]:
    rows = []
    for r in r_values:
        rr = r * r
        points = 0
        for x in range(-r, r + 1):
            xx = x * x
            for y in range(-r, r + 1):
                if xx + y * y <= rr:
                    points += 1
        pi_est = points / (r * r)
        err = abs(pi_est - math.pi)
        rows.append(
            {
                "radius": int(r),
                "pi_estimate": float(pi_est),
                "abs_error": float(err),
                "rel_error": float(err / math.pi),
            }
        )
    return rows


def torus_modular_defect_rows(sample_counts: list[int], m: float, n_e: int = 111) -> dict:
    # scipy.special uses parameter m for ellipk/ellipe and ellipj
    k = special.ellipk(m)
    e = special.ellipe(m)
    defect_exact = 1.0 - e / k
    delta_c_exact = defect_exact / n_e

    rows = []
    for m_samples in sample_counts:
        # one full periodic interval for sn(u|m): [0, 4K]
        u = np.linspace(0.0, 4.0 * k, m_samples, endpoint=False)
        sn, _, _, _ = special.ellipj(u, m)
        avg_sn2 = float(np.mean(sn * sn))
        defect_pix = m * avg_sn2
        delta_c_pix = defect_pix / n_e
        rows.append(
            {
                "samples": int(m_samples),
                "avg_sn2": avg_sn2,
                "defect_pixelated": float(defect_pix),
                "defect_exact": float(defect_exact),
                "defect_abs_error": float(abs(defect_pix - defect_exact)),
                "deltaC_pixelated": float(delta_c_pix),
                "deltaC_exact": float(delta_c_exact),
                "deltaC_abs_error": float(abs(delta_c_pix - delta_c_exact)),
            }
        )

    return {
        "m_parameter": float(m),
        "K_m": float(k),
        "E_m": float(e),
        "defect_exact": float(defect_exact),
        "deltaC_exact": float(delta_c_exact),
        "rows": rows,
    }


def main() -> None:
    # Unit-step ladders
    n_values = [2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987]
    r_values = [20, 50, 100, 200, 400, 800]
    sample_counts = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096]

    # Electron torus anchor used throughout GU docs
    p = -41.0
    q = 70.0
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    q_over_phi = q / phi
    m_torus = abs(q_over_phi) / math.sqrt(p * p + q_over_phi * q_over_phi)  # nu_topo-style parameter

    report = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "e_unit_step_limit": e_compounding_rows([1, 2, 5, 10, 50, 100, 500, 1000, 5000, 10000]),
        "phi_unit_step_limit": phi_fibonacci_rows(n_values),
        "pi_pixelation_limit": pi_lattice_rows(r_values),
        "torus_pixelation_limit": torus_modular_defect_rows(sample_counts, m=m_torus, n_e=111),
    }

    # Compact interpretation flags
    report["interpretation"] = {
        "e_limit_is_clear": report["e_unit_step_limit"][-1]["rel_error"] < 1e-4,
        "phi_limit_is_clear": report["phi_unit_step_limit"][-1]["rel_error"] < 1e-6,
        "pi_limit_is_clear": report["pi_pixelation_limit"][-1]["rel_error"] < 1e-4,
        "torus_deltaC_pixelation_converges": report["torus_pixelation_limit"]["rows"][-1]["deltaC_abs_error"] < 1e-6,
        "honest_note": (
            "Torus correction can be interpreted as continuum-from-pixelation convergence "
            "at the integral-evaluation level, but this does not by itself prove fundamental "
            "spacetime pixelation."
        ),
    }

    out_path = Path(__file__).with_name("10_unit_step_continuum_limits_report.json")
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("=" * 80)
    print("TRINITY UNIT-STEP CONTINUUM LIMITS")
    print("=" * 80)
    print(f"e rel error (last): {report['e_unit_step_limit'][-1]['rel_error']:.3e}")
    print(f"phi rel error (last): {report['phi_unit_step_limit'][-1]['rel_error']:.3e}")
    print(f"pi rel error (last): {report['pi_pixelation_limit'][-1]['rel_error']:.3e}")
    print(f"torus deltaC abs error (last): {report['torus_pixelation_limit']['rows'][-1]['deltaC_abs_error']:.3e}")
    print(f"\nReport written: {out_path}")


if __name__ == "__main__":
    main()

