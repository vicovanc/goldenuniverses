#!/usr/bin/env python3
"""
18_pattern_k_from_lagrangian.py

Attempts to derive the Pattern-k mechanism (pi^k enhancement for each force)
from the GU Lagrangian L_M = L_Omega + L_X + L_int + L_gauge.

Pattern-k claim:
  - Pattern-0: Electromagnetic (no pi) — U(1) gauge
  - Pattern-1: Weak (pi^1) — SU(2)_L gauge
  - Pattern-2: Strong (pi^2) — SU(3)_c gauge
  - Pattern-3: GUT (pi^3) — SU(5) gauge

Investigates WHERE the factors of pi come from via several hypotheses,
computes coupling hierarchies, compares to experiment, and rates each hypothesis.
"""

import numpy as np
import sys
import os
from math import gamma

# Allow import from derivations/utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.gu_constants import (
    pi,
    phi,
    alpha_EM,
    alpha_GUT,
    alpha_s_MZ,
    pattern_factor,
    PATTERN_EM,
    PATTERN_WEAK,
    PATTERN_STRONG,
    PATTERN_GUT,
)

# Use float(pi) for numerical comparisons
PI = float(pi)


def main():
    print("=" * 72)
    print("PATTERN-k FROM LAGRANGIAN: L_M = L_Omega + L_X + L_int + L_gauge")
    print("=" * 72)

    # Experimental benchmarks (approximate)
    alpha_em_exp = float(alpha_EM)           # ~1/137
    alpha_s_1GeV = 0.5                       # alpha_s(1 GeV) ~ 0.5
    alpha_s_MZ_val = float(alpha_s_MZ)       # ~0.1179
    alpha_gut_exp = float(alpha_GUT)         # ~1/42

    print("\n--- Experimental coupling benchmarks ---")
    print(f"  alpha_EM   ~ {alpha_em_exp:.6f}  (1/137)")
    print(f"  alpha_s(MZ) ~ {alpha_s_MZ_val:.4f}")
    print(f"  alpha_s(1 GeV) ~ {alpha_s_1GeV}")
    print(f"  alpha_GUT  ~ {alpha_gut_exp:.4f}  (1/42)")

    # Test: 4*pi*alpha_s at 1 GeV vs pi^2
    four_pi_alpha_s_1GeV = 4 * PI * alpha_s_1GeV
    pi_sq = PI ** 2
    print(f"\n  Test (Hyp A): 4*pi*alpha_s(1 GeV) = {four_pi_alpha_s_1GeV:.4f}  vs  pi^2 = {pi_sq:.4f}")
    print(f"  Ratio = {four_pi_alpha_s_1GeV / pi_sq:.4f}  (close but not exact)")

    results = {}

    # -------------------------------------------------------------------------
    # HYPOTHESIS A: Loop counting (Casimir invariants)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 72)
    print("HYPOTHESIS A: Loop counting (independent Casimir invariants)")
    print("=" * 72)
    print("  U(1): 0 independent Casimirs beyond charge → k=0")
    print("  SU(2): 1 Casimir (C_2) → k=1")
    print("  SU(3): 2 Casimirs (C_2, C_3) → k=2")
    print("  SU(5): 4 Casimirs, GU reduces effective to 3 → k=3")
    print("  Each gauge loop ~ 1/(4*pi^2) or 1/(16*pi^2)")

    k_A = {0: 0, 1: 1, 2: 2, 3: 3}
    # If effective coupling scales as 1/pi^k (more loops → more suppression?)
    # or as pi^k (pattern enhancement)? GU convention is pattern_factor(k)=pi^k.
    # So alpha_eff might scale like alpha_bare * pi^k (enhancement) or alpha_bare / pi^k.
    # Pattern-k in GU: higher k = stronger pattern factor. So coupling correction could be
    # alpha_k ~ alpha_bare * f(pi^k). Assume we compare ratios.
    pred_em_A = PI ** 0
    pred_weak_A = PI ** 1
    pred_strong_A = PI ** 2
    pred_gut_A = PI ** 3

    # Coupling hierarchy: if alpha ~ g^2/(4*pi), and pattern gives pi^k, then
    # effective g^2 might be modified. Take as hierarchy the ratios of pi^k.
    hierarchy_A = [pred_em_A, pred_weak_A, pred_strong_A, pred_gut_A]
    hierarchy_A = np.array(hierarchy_A) / pred_em_A  # normalize to EM
    print(f"\n  Predicted pattern factors (pi^k): 1, pi, pi^2, pi^3")
    print(f"  As coupling hierarchy (normalized to EM=1): {hierarchy_A}")
    # Does pi^k enter as mass or coupling? In loop counting, pi comes from
    # angular integration in loop momentum → coupling (running coupling).
    results["A"] = {
        "hierarchy": hierarchy_A,
        "mass_or_coupling": "coupling (loop integration)",
        "rating": "PARTIAL",
        "notes": "4*pi*alpha_s(1 GeV) ≈ 6.3 vs pi^2 ≈ 9.87; Casimir count matches k; exact pi^k origin in loops not derived.",
    }
    print(f"  Rating: {results['A']['rating']} — {results['A']['notes']}")

    # -------------------------------------------------------------------------
    # HYPOTHESIS B: Omega-torus angular integration
    # -------------------------------------------------------------------------
    print("\n" + "=" * 72)
    print("HYPOTHESIS B: Omega-torus angular integration")
    print("=" * 72)
    print("  U(1): no non-trivial angular integral → pi^0")
    print("  SU(2): one S^1 (Hopf) → 2*pi → one factor pi")
    print("  SU(3): adjoint orbit S^2×S^1 → two factors")
    print("  SU(5): maximal torus rank 4, but claim k=3 → PROBLEM")

    rank = {0: 0, 1: 1, 2: 2, 3: 4}  # SU(2)=1, SU(3)=2, SU(5)=4
    # If k = rank, then SU(5) would give k=4, not k=3.
    k_B_by_rank = [0, 1, 2, 4]
    k_B_claimed = [0, 1, 2, 3]
    print(f"  rank(SU(n)): k would be 0,1,2,4  vs claimed 0,1,2,3")
    # "Effective pattern" rank - rank(center): SU(5) center Z_5, rank(center)=0 for Lie algebra.
    # So problem remains: rank SU(5)=4.

    pred_em_B = PI ** 0
    pred_weak_B = PI ** 1
    pred_strong_B = PI ** 2
    pred_gut_B = PI ** 3  # claimed, not rank
    hierarchy_B = np.array([pred_em_B, pred_weak_B, pred_strong_B, pred_gut_B]) / pred_em_B
    print(f"  Using claimed k: hierarchy (normalized) = {hierarchy_B}")
    results["B"] = {
        "hierarchy": hierarchy_B,
        "mass_or_coupling": "coupling (volume/angular integration)",
        "rating": "PARTIAL",
        "notes": "Angular integration gives natural pi factors; SU(5) rank=4 vs k=3 is inconsistent unless GU structure removes one dimension.",
    }
    print(f"  Rating: {results['B']['rating']} — {results['B']['notes']}")

    # -------------------------------------------------------------------------
    # HYPOTHESIS C: Topological winding (theta sectors)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 72)
    print("HYPOTHESIS C: Topological winding (kappa from large gauge invariance)")
    print("=" * 72)
    print("  L_top = -sum_a (kappa_a/8*pi^2) theta_a tr(F_a F_tilde_a)")
    print("  k = number of confined/massive theta sectors")
    print("  Below QCD: theta_3 massive → 2 sectors → pi^2")
    print("  Below EW: only theta_EM → 0 sectors → pi^0")

    # Active topological sectors: EM 0, weak 1, strong 2, GUT 3
    k_C = [0, 1, 2, 3]
    pred_C = [PI ** k for k in k_C]
    hierarchy_C = np.array(pred_C) / pred_C[0]
    print(f"  k = active theta sectors: {k_C}")
    print(f"  Hierarchy (normalized): {hierarchy_C}")
    results["C"] = {
        "hierarchy": hierarchy_C,
        "mass_or_coupling": "coupling (theta-term normalization 1/8*pi^2)",
        "rating": "PARTIAL",
        "notes": "Theta sector counting matches k; link from L_top to pi^k enhancement needs explicit derivation.",
    }
    print(f"  Rating: {results['C']['rating']} — {results['C']['notes']}")

    # -------------------------------------------------------------------------
    # HYPOTHESIS D: Casimir energy on the torus
    # -------------------------------------------------------------------------
    print("\n" + "=" * 72)
    print("HYPOTHESIS D: Casimir energy on the Omega-torus")
    print("=" * 72)
    print("  Casimir energy ~ pi^(d/2)/Gamma(d/2+1) * V^(1-d)")
    print("  U(1): 0 extra compact dimensions → pi^0")
    print("  SU(2): 1 extra (Hopf) → pi^1")
    print("  SU(3): 2 extra → pi^2")

    # Effective dimension seen by gauge group
    d_eff = [0, 1, 2, 3]  # EM, weak, strong, GUT
    # Casimir prefactor pi^(d/2)/Gamma(d/2+1): d=0→1, d=1→sqrt(pi), d=2→pi/2, d=3→pi^1.5/...
    casimir_prefactor = lambda d: (PI ** (d / 2)) / gamma(d / 2 + 1) if d >= 0 else 1.0
    pred_D = [casimir_prefactor(d) for d in d_eff]
    hierarchy_D = np.array(pred_D) / pred_D[0]
    print(f"  Effective d: {d_eff}  → Casimir prefactors: {[f'{x:.4f}' for x in pred_D]}")
    print(f"  Hierarchy (normalized): {hierarchy_D}")
    results["D"] = {
        "hierarchy": hierarchy_D,
        "mass_or_coupling": "mass/correction (Casimir energy)",
        "rating": "PARTIAL",
        "notes": "Prefactor is pi^(d/2)/Gamma(...), not pi^d; so pattern is pi^(d/2) with Gamma, not clean pi^k.",
    }
    print(f"  Rating: {results['D']['rating']} — {results['D']['notes']}")

    # -------------------------------------------------------------------------
    # Comparison with experimental coupling hierarchy
    # -------------------------------------------------------------------------
    print("\n" + "=" * 72)
    print("COMPARISON WITH EXPERIMENTAL COUPLING HIERARCHY")
    print("=" * 72)
    # Order of magnitude: alpha_EM ~ 1/137, alpha_W ~ 1/30 (at MZ), alpha_s ~ 0.1-0.5, alpha_GUT ~ 1/42
    # Normalize to alpha_EM = 1.
    alpha_W_approx = 1 / 30  # rough
    exp_hierarchy = np.array([alpha_em_exp, alpha_W_approx, alpha_s_MZ_val, alpha_gut_exp])
    exp_hierarchy = exp_hierarchy / alpha_em_exp
    print(f"  Experimental (alpha_EM, alpha_W~1/30, alpha_s(MZ), alpha_GUT) normalized to EM=1:")
    print(f"  {exp_hierarchy}")

    for label, res in results.items():
        corr = np.corrcoef(res["hierarchy"], exp_hierarchy)[0, 1] if len(res["hierarchy"]) == len(exp_hierarchy) else float("nan")
        print(f"  Hyp {label} correlation with exp: {corr:.4f}")

    # -------------------------------------------------------------------------
    # SUMMARY TABLE
    # -------------------------------------------------------------------------
    print("\n" + "=" * 72)
    print("SUMMARY: Where does pi^k enter? Mass vs coupling? Rating")
    print("=" * 72)
    print(f"  {'Hyp':<4} {'Mass/Coupling':<28} {'Rating':<10} Notes")
    print("  " + "-" * 70)
    for label, res in results.items():
        note = res["notes"]
        print(f"  {label:<4} {res['mass_or_coupling']:<28} {res['rating']:<10} {note[:50]}{'...' if len(note) > 50 else ''}")

    # -------------------------------------------------------------------------
    # CONCLUSION
    # -------------------------------------------------------------------------
    print("\n" + "=" * 72)
    print("CONCLUSION")
    print("=" * 72)
    print("""
  1. Most consistent: Hypothesis A (loop counting) and C (theta sectors) give
     the correct k assignment (0,1,2,3). Hypothesis B fails for SU(5) (rank 4 vs k=3).
     Hypothesis D gives pi^(d/2)/Gamma, not clean pi^k.

  2. Additional derivation needed:
     - From L_M = L_Omega + L_X + L_int + L_gauge, show explicitly which term
       yields the factor pi^k per gauge group (e.g. L_gauge kinetic vs L_int
       vs topological term).
     - Derive why SU(5) effective pattern is k=3 not k=4 (e.g. from GU
       reduction of Casimirs or from one theta sector integrated out).
     - Connect loop 1/(4*pi^2) factors to the *enhancement* pi^k (not
       suppression) if pattern is to increase with k.

  3. Honest assessment: Pattern-k is still POSTULATED, not derived.
     The hypotheses are plausible origins for factors of pi, but none are
     derived from the full GU Lagrangian. The assignment k=0,1,2,3 is
     chosen to match the gauge groups; a first-principles derivation
     from L_M is missing.
""")


if __name__ == "__main__":
    main()
