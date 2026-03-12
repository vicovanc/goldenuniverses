#!/usr/bin/env python3
"""
Trinity necessity probe:
  - pi from lattice-circle pixelation
  - phi from finite bad-approximability score
  - e from discrete compounding convergence
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path


@dataclass
class PiProbeResult:
    max_radius: int
    pi_estimate: float
    abs_error: float
    rel_error: float


@dataclass
class IrrationalScore:
    name: str
    value: float
    finite_bad_approx_score: float


def estimate_pi_from_lattice(max_radius: int = 500) -> PiProbeResult:
    points = 0
    rr = max_radius * max_radius
    for x in range(-max_radius, max_radius + 1):
        xx = x * x
        for y in range(-max_radius, max_radius + 1):
            if xx + y * y <= rr:
                points += 1
    pi_est = points / (max_radius * max_radius)
    abs_err = abs(pi_est - math.pi)
    rel_err = abs_err / math.pi
    return PiProbeResult(max_radius, pi_est, abs_err, rel_err)


def finite_bad_approx_score(alpha: float, q_max: int = 1000) -> float:
    # Larger score means harder to approximate by rationals with small denominators.
    # score = min_{1<=q<=q_max} q * ||q*alpha||, where ||.|| is distance to nearest integer.
    best = float("inf")
    for q in range(1, q_max + 1):
        x = q * alpha
        dist = abs(x - round(x))
        val = q * dist
        if val < best:
            best = val
    return best


def irrational_comparison(q_max: int = 1000) -> list[IrrationalScore]:
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    candidates = {
        "phi": phi,
        "sqrt2": math.sqrt(2.0),
        "sqrt3": math.sqrt(3.0),
        "pi-3": math.pi - 3.0,
        "e-2": math.e - 2.0,
    }
    out: list[IrrationalScore] = []
    for name, value in candidates.items():
        out.append(
            IrrationalScore(
                name=name,
                value=value,
                finite_bad_approx_score=finite_bad_approx_score(value, q_max=q_max),
            )
        )
    out.sort(key=lambda s: s.finite_bad_approx_score, reverse=True)
    return out


def e_compounding_probe(ns: list[int] | None = None) -> list[dict]:
    if ns is None:
        ns = [1, 2, 5, 10, 50, 100, 1000, 10000]
    rows = []
    for n in ns:
        v = (1.0 + 1.0 / n) ** n
        err = abs(v - math.e)
        rows.append(
            {
                "n": n,
                "value": v,
                "abs_error": err,
                "rel_error": err / math.e,
            }
        )
    return rows


def main() -> None:
    pi_probe = estimate_pi_from_lattice(max_radius=500)
    irr_scores = irrational_comparison(q_max=1000)
    e_probe = e_compounding_probe()

    top_name = irr_scores[0].name if irr_scores else None

    report = {
        "pi_pixelation_probe": {
            "max_radius": pi_probe.max_radius,
            "pi_estimate": pi_probe.pi_estimate,
            "abs_error": pi_probe.abs_error,
            "rel_error": pi_probe.rel_error,
        },
        "irrational_bad_approximability_probe": [
            {
                "name": s.name,
                "value": s.value,
                "finite_bad_approx_score": s.finite_bad_approx_score,
            }
            for s in irr_scores
        ],
        "e_compounding_probe": e_probe,
        "interpretation": {
            "pi_signal": "strong" if pi_probe.rel_error < 0.01 else "moderate",
            "phi_signal": (
                "strong_finite_window" if top_name == "phi" else "criterion_dependent"
            ),
            "e_signal": "strong" if e_probe[-1]["rel_error"] < 1e-4 else "moderate",
            "honest_note": (
                "This is structural evidence, not a formal uniqueness theorem. "
                "Pixelation supports continuum constants via convergence behavior."
            ),
        },
    }

    out_path = Path(__file__).with_name("trinity_necessity_report.json")
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("=" * 80)
    print("TRINITY NECESSITY PROBE")
    print("=" * 80)
    print(f"pi estimate (lattice, r={pi_probe.max_radius}): {pi_probe.pi_estimate:.8f}")
    print(f"pi relative error: {pi_probe.rel_error:.3e}")
    print(
        "top finite bad-approximability candidate: "
        f"{top_name} (score={irr_scores[0].finite_bad_approx_score:.6f})"
    )
    print(f"e compounding at n={e_probe[-1]['n']}: {e_probe[-1]['value']:.10f}")
    print(f"e relative error: {e_probe[-1]['rel_error']:.3e}")
    print(f"\nReport written: {out_path}")


if __name__ == "__main__":
    main()

