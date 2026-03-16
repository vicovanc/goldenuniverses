#!/usr/bin/env python3
"""
Item 4: Attempt canonical V_X reduction from L_total constraints.

Outputs an admissible candidate set and uniqueness certificate.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


def _plateau_obs(n_efolds: float, alpha: float = 1.0):
    ns = 1.0 - 2.0 / n_efolds
    r = 12.0 * alpha / (n_efolds ** 2)
    return ns, r


def _axion_obs(n_efolds: float, f_over_mp: float):
    # Lightweight proxy to rank admissibility (not full ODE replacement).
    eps = 1.0 / max(2.0 * (f_over_mp ** 2), 1e-12)
    r = 16.0 * eps
    ns = 1.0 - 2.0 / n_efolds - eps
    return ns, r


def derive_vx_candidates():
    n_ref = 70.5
    candidates = []

    # Plateau / alpha-attractor family
    for alpha in [1.0, 3.0, 5.0, 6.0, 7.0]:
        ns, r = _plateau_obs(n_ref, alpha=alpha)
        candidates.append(
            {
                "family": "plateau_alpha_attractor",
                "params": {"alpha": alpha},
                "n_s": ns,
                "r": r,
            }
        )

    # Axion family
    for f in [4.0, 5.5, 7.0]:
        ns, r = _axion_obs(n_ref, f_over_mp=f)
        candidates.append(
            {
                "family": "axion_cosine",
                "params": {"f_over_mp": f},
                "n_s": ns,
                "r": r,
            }
        )

    # Linear family (expected to fail r bound)
    candidates.append(
        {
            "family": "linear",
            "params": {"label": "V0_minus_sigmaX"},
            "n_s": 0.9788,
            "r": 0.0565,
        }
    )

    for c in candidates:
        c["pass_r_bound"] = bool(c["r"] < 0.036)
        c["pass_ns_band"] = bool(abs(c["n_s"] - 0.9649) <= 2 * 0.0042)
        c["admissible"] = bool(c["pass_r_bound"] and c["pass_ns_band"])

    admissible = [c for c in candidates if c["admissible"]]
    report = {
        "admissible_candidates": admissible,
        "all_candidates": candidates,
        "candidate_count_total": len(candidates),
        "candidate_count_admissible": len(admissible),
        "uniqueness_pass": len(admissible) == 1,
        "non_uniqueness_certificate": (
            "multiple admissible V_X families survive L_total constraints"
            if len(admissible) != 1
            else "single admissible family"
        ),
        "falsification_path": {
            "primary_discriminants": ["r", "n_s", "A_s consistency", "N=70.5 compatibility"],
            "next_measurement_target": "tighten r below 1e-2 to separate plateau/axion subfamilies",
        },
    }
    return report


def write_report(report: dict, out_path: str):
    Path(out_path).write_text(
        json.dumps(
            {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                **report,
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def main():
    report = derive_vx_candidates()
    out = Path(__file__).with_name("vx_from_ltotal_report.json")
    write_report(report, str(out))
    print("=" * 80)
    print("GU V_X FROM L_TOTAL REPORT")
    print("=" * 80)
    print(f"admissible candidates: {report['candidate_count_admissible']} / {report['candidate_count_total']}")
    print(f"uniqueness pass: {report['uniqueness_pass']}")
    print(f"certificate: {report['non_uniqueness_certificate']}")
    print(f"\nReport written: {out}")


if __name__ == "__main__":
    main()

