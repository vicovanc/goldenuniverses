#!/usr/bin/env python3
"""
04_pi_in_coupling_hierarchy.py
==============================

The key question: does the coupling hierarchy alpha_EM << alpha_W << alpha_s
correlate with pi^k, or does it come from the RG running via different b_0?

This script:
  1. Computes the exact coupling hierarchy at the QCD scale (~1 GeV)
  2. Tests whether ratios look like pi^k
  3. Shows the actual origin: exponential RG running with different b_0
  4. Demonstrates that any apparent pi^k correlation is coincidental

Reference: 03_pi_in_gauge_loops.py (this script uses its results),
           05_pi_on_omega_torus.py (topological contributions).
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from utils.gu_constants import phi, pi, alpha_EM, alpha_s_MZ

PI = float(pi)
PHI = float(phi)

print("=" * 80)
print("THE COUPLING HIERARCHY: b_0 vs pi^k")
print("Does alpha_EM << alpha_W << alpha_s look like pi^k? No — it's b_0.")
print("=" * 80)

# ============================================================================
# THE COUPLING VALUES
# ============================================================================

print("\n" + "-" * 80)
print("MEASURED COUPLING VALUES (CODATA / PDG)")
print("-" * 80)

alpha_em = 1 / 137.035999084
alpha_w_mz = 1 / 29.587        # SU(2)_L at M_Z (from sin^2(theta_W) and alpha_em)
alpha_s_mz_val = 0.1179         # PDG 2024
sin2_tw = 0.23122               # PDG
M_Z = 91.1876

print(f"  alpha_EM(0)      = 1/137.036 = {alpha_em:.6f}")
print(f"  alpha_EM(M_Z)    = 1/127.9   = {1/127.9:.6f}")
print(f"  alpha_W(M_Z)     = 1/29.6    = {alpha_w_mz:.6f}")
print(f"  alpha_s(M_Z)     = {alpha_s_mz_val:.4f}")
print(f"  sin^2(theta_W)   = {sin2_tw:.5f}")

# ============================================================================
# TEST 1: Do the ratios look like pi^k?
# ============================================================================

print("\n" + "-" * 80)
print("TEST 1: Coupling ratios vs pi^k")
print("-" * 80)

ratios = {
    "alpha_s / alpha_EM(M_Z)": alpha_s_mz_val / (1/127.9),
    "alpha_W / alpha_EM(M_Z)": alpha_w_mz / (1/127.9),
    "alpha_s / alpha_W":       alpha_s_mz_val / alpha_w_mz,
}

print(f"\n  {'Ratio':<30} {'Value':<10} {'pi^1':<10} {'pi^2':<10} {'Closest pi^k'}")
print("  " + "-" * 75)
for name, val in ratios.items():
    k_closest = np.log(val) / np.log(PI)
    print(f"  {name:<30} {val:<10.4f} {PI:<10.4f} {PI**2:<10.4f} pi^{k_closest:.3f}")

print(f"""
  alpha_s/alpha_EM(M_Z) ~ 15.1 vs pi^2 ~ 9.87 — off by 53%
  alpha_W/alpha_EM(M_Z) ~ 4.32 vs pi^1 ~ 3.14 — off by 37%
  alpha_s/alpha_W ~ 3.49 vs pi^1 ~ 3.14 — off by 11%

  The closest match is alpha_s/alpha_W ~ pi^1, but even that is 11% off.
  These are NOT clean powers of pi.
""")

# ============================================================================
# TEST 2: THE ACTUAL ORIGIN — RG running from a single alpha_GUT
# ============================================================================

print("-" * 80)
print("TEST 2: The actual origin — RG running with different b_0")
print("-" * 80)

# SM one-loop beta coefficients (above M_Z, Nf=5 for QCD threshold)
b0_1 = 41.0 / 10.0   # U(1)_Y
b0_2 = -19.0 / 6.0   # SU(2)_L
b0_3 = 7.0            # SU(3)_c with Nf=5

M_GUT = 2e16  # GeV (typical GUT scale)
alpha_GUT = 1 / 40.0  # Approximate unified coupling

print(f"  Assuming unification at M_GUT = {M_GUT:.0e} GeV, alpha_GUT = 1/40 = {alpha_GUT:.4f}")
print(f"  Running DOWN to M_Z = {M_Z:.2f} GeV with 1-loop SM beta functions:")
print()

ln_ratio = np.log(M_Z**2 / M_GUT**2)

alpha_1_mz = alpha_GUT / (1 + b0_1 * alpha_GUT * ln_ratio / (4 * PI))
alpha_2_mz = alpha_GUT / (1 + b0_2 * alpha_GUT * ln_ratio / (4 * PI))
alpha_3_mz = alpha_GUT / (1 + b0_3 * alpha_GUT * ln_ratio / (4 * PI))

# Convert U(1)_Y to EM normalization
alpha_em_mz_pred = alpha_1_mz * 3.0 / 5.0  # GUT normalization factor

print(f"  alpha_1(M_Z) = {alpha_1_mz:.6f}  (1/alpha_1 = {1/alpha_1_mz:.1f})")
print(f"  alpha_2(M_Z) = {alpha_2_mz:.6f}  (1/alpha_2 = {1/alpha_2_mz:.1f})")
print(f"  alpha_3(M_Z) = {alpha_3_mz:.6f}  (1/alpha_3 = {1/alpha_3_mz:.1f})")
print()

print(f"  The hierarchy arises from the SIGN and MAGNITUDE of b_0:")
print(f"    b0_1 = +{b0_1:.1f} (positive) => alpha_1 DECREASES from GUT to M_Z (slower)")
print(f"    b0_2 = {b0_2:.2f} (negative) => alpha_2 INCREASES from GUT to M_Z")
print(f"    b0_3 = +{b0_3:.1f} (positive, largest) => alpha_3 DECREASES fastest")
print()
print(f"  Wait — alpha_3 also decreases? Yes! But it INCREASES going from M_Z DOWN")
print(f"  to low energies (asymptotic freedom). At M_Z it's already ~0.12.")

# ============================================================================
# TEST 3: The exponential structure — is it pi^k or exp(b_0)?
# ============================================================================

print("\n" + "-" * 80)
print("TEST 3: Exponential structure of the hierarchy")
print("-" * 80)

print(f"""
  The one-loop formula can be rewritten:

    1/alpha(M_Z) = 1/alpha_GUT + b_0/(2*pi) * ln(M_GUT/M_Z)

  So the DIFFERENCE in 1/alpha between forces is:

    1/alpha_i - 1/alpha_j = (b0_i - b0_j)/(2*pi) * ln(M_GUT/M_Z)

  The factor 1/(2*pi) is UNIVERSAL, the hierarchy comes from b_0 differences.
""")

L = np.log(M_GUT / M_Z)
print(f"  ln(M_GUT/M_Z) = {L:.2f}")
print(f"  1/(2*pi) * ln(M_GUT/M_Z) = {L/(2*PI):.2f}")
print()

print(f"  {'Pair':<25} {'Delta b_0':<10} {'Delta(1/alpha)':<15} {'Actual'}")
print("  " + "-" * 60)

delta_b_12 = b0_1 - b0_2
delta_b_23 = b0_2 - b0_3
delta_b_13 = b0_1 - b0_3

for name, db in [("U(1)-SU(2)", delta_b_12), ("SU(2)-SU(3)", delta_b_23), ("U(1)-SU(3)", delta_b_13)]:
    delta_inv_alpha = db / (2 * PI) * L
    print(f"  {name:<25} {db:<10.2f} {delta_inv_alpha:<15.2f} (from b_0 alone)")

print(f"""
  The hierarchy 1/alpha_EM >> 1/alpha_W >> 1/alpha_s is ENTIRELY determined
  by the b_0 coefficients (which are group-theory numbers: N_c, N_f, C_2)
  multiplied by the UNIVERSAL factor 1/(2*pi).

  There is no room for, and no need for, a Pattern-k pi^k factor.
""")

# ============================================================================
# TEST 4: alpha_s(IR) = pi^2/b_0 — coincidence check
# ============================================================================

print("-" * 80)
print("TEST 4: alpha_s(IR) = pi^2/b_0 — structural or coincidental?")
print("-" * 80)

b0_vals = [(3, 9.0), (4, 25/3), (5, 23/3)]

print(f"\n  If we hypothesize alpha_s(IR, Nf) = pi^2/b_0(Nf):")
print(f"\n  {'Nf':<4} {'b_0':<8} {'pi^2/b_0':<12} {'Lattice QCD':<12} {'Status'}")
print("  " + "-" * 50)
for nf, b0 in b0_vals:
    val = PI**2 / b0
    lattice_approx = {3: "~0.4-0.5", 4: "N/A", 5: "N/A"}
    print(f"  {nf:<4} {b0:<8.2f} {val:<12.4f} {lattice_approx.get(nf, 'N/A'):<12} {'?'}")

print(f"""
  For Nf=3: pi^2/9 = 1.097, but lattice QCD gives alpha_s(~1 GeV) ~ 0.4-0.5
  This is a factor of ~2 discrepancy.

  The formula alpha_s = pi^2/b_0 would mean:
    g_s^2 = 4*pi*alpha_s = 4*pi^3/b_0

  Is there a derivation? Let's check:
    - The IR fixed point of the EXACT beta function (unknown in QCD)
    - The Banks-Zaks fixed point: only exists for 33/2 > Nf > 33/2 - 25/2, i.e. Nf = 9-16
      NOT relevant for physical Nf = 2-3
    - Lattice QCD: no analytical IR fixed point known

  CONCLUSION: pi^2/b_0 is not derived. It's a numerological observation that
  pi^2 ≈ 9.87 ≈ b_0(Nf=3) = 9, making pi^2/b_0 ≈ 1 look "natural" for
  a strong coupling. This is a coincidence, not a derivation.
""")

# ============================================================================
# TEST 5: Could pi^k be the number of loops?
# ============================================================================

print("-" * 80)
print("TEST 5: Could pi^k count loops?")
print("-" * 80)

print(f"""
  Hypothesis: k=0,1,2 counts the NUMBER of essential loop corrections:
    k=0 (EM): tree-level dominant (QED corrections are O(alpha) ~ 0.007)
    k=1 (Weak): one-loop radiative corrections essential (EW precision tests)
    k=2 (QCD): two-loop needed (alpha_s^2 corrections matter)

  Then "pi^k" would be (1/(16*pi^2))^{{-k}} ~ (158)^k ... this grows too fast.

  Or: the effective coupling at scale mu is:
    alpha_eff ~ sum_{{l=0}}^k [b_0*alpha/(2*pi)]^l

  But this is just a truncated perturbation series — the pi is 1/(2*pi)
  from the loop measure, not pi^k.

  VERDICT: The "loop counting" interpretation doesn't produce pi^k either.
""")

# ============================================================================
# FINAL VERDICT
# ============================================================================

print("=" * 80)
print("FINAL VERDICT: COUPLING HIERARCHY")
print("=" * 80)

print(f"""
  The force hierarchy alpha_EM << alpha_W << alpha_s is explained by:

    1. UNIFIED coupling alpha_GUT at M_GUT (GU predicts unification at N=67)
    2. DIFFERENT b_0 coefficients from the gauge group structure:
       - b0_1 = 41/10 (U(1)_Y)
       - b0_2 = -19/6 (SU(2)_L)
       - b0_3 = 11 - 2*Nf/3 (SU(3)_c)
    3. UNIVERSAL factor 1/(2*pi) from the loop measure

  The coupling ratios do NOT match pi^k:
    alpha_s/alpha_W ~ 3.5 vs pi ~ 3.14 (11% off, and not exact)
    alpha_s/alpha_EM ~ 15 vs pi^2 ~ 9.87 (53% off)

  Pattern-k as a "pi^k coupling enhancement" is NOT derived.
  The hierarchy comes from group theory (b_0), not from powers of pi.
""")

print("=" * 80)
print("DONE: 04_pi_in_coupling_hierarchy.py")
print("=" * 80)
