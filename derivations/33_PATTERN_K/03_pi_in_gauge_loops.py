#!/usr/bin/env python3
"""
03_pi_in_gauge_loops.py
=======================

Standard QFT: where pi enters gauge coupling running.

The one-loop beta function for ANY gauge group has the form:
  d_t alpha = -(b_0 / (2*pi)) * alpha^2

The factor 1/(2*pi) = half of 1/(4*pi^2) from the d=4 loop measure.
This is UNIVERSAL — the same for U(1), SU(2), SU(3), SU(5).

The DIFFERENCE between forces comes from b_0 (group theory: N_c, N_f),
not from different powers of pi.

Reference: theory-laws.md, lines 7162-7186 (QCD-4: Beta functions).
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from utils.gu_constants import phi, pi, alpha_EM, alpha_s_MZ

PI = float(pi)

print("=" * 80)
print("pi IN GAUGE COUPLING RUNNING")
print("Standard QFT: 1/(16*pi^2) per loop is UNIVERSAL")
print("=" * 80)

# ============================================================================
# WHERE 1/(16*pi^2) COMES FROM
# ============================================================================

print("\n" + "-" * 80)
print("WHERE 1/(16*pi^2) COMES FROM")
print("-" * 80)

print("""
  In d=4 Euclidean QFT, a one-loop integral has the measure:

    integral d^4p_E / (2*pi)^4  *  (propagator terms)

  The angular part of d^4p_E in 4D is:

    d^4p = p^3 dp * d(Omega_4)
    Omega_4 = 2*pi^2      (surface area of unit 3-sphere)

  So the angular integral gives:
    Omega_4 / (2*pi)^4 = 2*pi^2 / (16*pi^4) = 1/(8*pi^2)

  Combined with the standard vertex/propagator factors, the one-loop
  contribution to the beta function is proportional to:

    1/(16*pi^2)   or equivalently   1/(4*pi)^2
""")

omega_4 = 2 * PI**2
loop_factor = omega_4 / (2*PI)**4

print(f"  Omega_4 = 2*pi^2 = {omega_4:.6f}")
print(f"  (2*pi)^4 = {(2*PI)**4:.4f}")
print(f"  Omega_4/(2*pi)^4 = {loop_factor:.8f}")
print(f"  1/(8*pi^2) = {1/(8*PI**2):.8f}")
print(f"  1/(16*pi^2) = {1/(16*PI**2):.8f}")

# ============================================================================
# THE BETA FUNCTION — SAME pi FOR ALL GAUGE GROUPS
# ============================================================================

print("\n" + "-" * 80)
print("THE BETA FUNCTION — same pi for ALL gauge groups")
print("-" * 80)

print("""
  One-loop beta function (theory-laws.md line 7169):

    d_t g = -(b_0/(16*pi^2)) * g^3

  Equivalently for alpha = g^2/(4*pi):

    d_t alpha = -(b_0/(2*pi)) * alpha^2

  The pi factor is UNIVERSAL. What differs between forces is b_0:
""")

groups = [
    ("U(1)_Y",  "EM",     "41/10",  41/10,   "N/A"),
    ("SU(2)_L", "Weak",   "-19/6",  -19/6,   "N/A"),
    ("SU(3)_c", "Strong", "11-2Nf/3", None,   "Nf-dependent"),
]

print(f"  {'Group':<10} {'Force':<8} {'b_0 formula':<16} {'b_0 (Nf=5)':<12} {'1/(16*pi^2)'}")
print("  " + "-" * 65)
for group, force, formula, b0, note in groups:
    if b0 is None:
        b0_5 = 11 - 2*5/3
        print(f"  {group:<10} {force:<8} {formula:<16} {b0_5:<12.4f} {1/(16*PI**2):.8f}")
    else:
        print(f"  {group:<10} {force:<8} {formula:<16} {b0:<12.4f} {1/(16*PI**2):.8f}")

print(f"\n  NOTE: The column 1/(16*pi^2) = {1/(16*PI**2):.8f} is THE SAME for all rows.")
print(f"        Only b_0 differs. The pi factor does not change with the gauge group.")

# ============================================================================
# RUNNING alpha_s FROM M_Z TO 1 GeV
# ============================================================================

print("\n" + "-" * 80)
print("RUNNING alpha_s: same pi, different b_0")
print("-" * 80)

alpha_s_mz = float(alpha_s_MZ)
M_Z = 91.1876  # GeV

mu_values = [91.19, 50, 20, 10, 5, 3, 2, 1.5, 1.0]
print(f"\n  One-loop alpha_s(mu) = alpha_s(M_Z) / (1 + b_0*alpha_s(M_Z)*ln(mu^2/M_Z^2)/(4*pi))")
print(f"  alpha_s(M_Z) = {alpha_s_mz}")
print(f"\n  {'mu (GeV)':<10} {'Nf':<4} {'b_0':<8} {'alpha_s':<10} {'4*pi*alpha_s':<14} {'pi^2':>8}")
print("  " + "-" * 60)

for mu in mu_values:
    if mu > 4.18:
        Nf = 5
    elif mu > 1.27:
        Nf = 4
    else:
        Nf = 3
    b0 = 11 - 2*Nf/3
    ln_ratio = np.log(mu**2 / M_Z**2)
    alpha_s_mu = alpha_s_mz / (1 + b0 * alpha_s_mz * ln_ratio / (4*PI))
    four_pi_alpha = 4 * PI * alpha_s_mu
    print(f"  {mu:<10.2f} {Nf:<4} {b0:<8.2f} {alpha_s_mu:<10.4f} {four_pi_alpha:<14.4f} {PI**2:>8.4f}")

print(f"\n  At mu ~ 1 GeV: 4*pi*alpha_s ~ 6-7, while pi^2 = {PI**2:.4f}")
print(f"  They're in the same ballpark but NOT equal.")
print(f"  The '~ pi^2' behavior at low energy is a CONSEQUENCE of the running,")
print(f"  not a separate Pattern-2 enhancement.")

# ============================================================================
# KEY TEST: IS pi^2/b_0 SPECIAL?
# ============================================================================

print("\n" + "-" * 80)
print("KEY TEST: Is alpha_s(IR) = pi^2/b_0 derived or coincidental?")
print("-" * 80)

b0_Nf3 = 11 - 2*3/3.0  # = 9
alpha_s_IR_GU = PI**2 / b0_Nf3

print(f"  GU claim: alpha_s(IR) = pi^2/b_0 = {PI**2:.4f}/{b0_Nf3:.0f} = {alpha_s_IR_GU:.4f}")
print(f"  Perturbative 1-loop at 1 GeV: alpha_s ~ 0.5 (above)")
print(f"  Lattice QCD at 1 GeV: alpha_s ~ 0.4-0.5")
print(f"  GU value: {alpha_s_IR_GU:.4f}")
print(f"  Ratio GU/perturbative: ~ {alpha_s_IR_GU/0.5:.2f}")

print(f"""
  The one-loop Landau pole occurs when:
    1 + b_0*alpha_s(M_Z)*ln(mu^2/M_Z^2)/(4*pi) = 0
    ln(mu/M_Z) = -2*pi / (b_0 * alpha_s(M_Z))
    mu_Landau = M_Z * exp(-2*pi / (b_0 * alpha_s(M_Z)))
              = {M_Z:.2f} * exp(-{2*PI/(b0_Nf3*alpha_s_mz):.2f})
              = {M_Z * np.exp(-2*PI/(b0_Nf3*alpha_s_mz)):.4f} GeV

  At the Landau pole, alpha_s -> infinity. Well before that, perturbation
  theory breaks down. The claim alpha_s = pi^2/b_0 = 1.097 is in the
  non-perturbative regime where the one-loop formula is unreliable.

  The value pi^2/9 ≈ 1.097 is:
    - NOT a prediction of standard QCD (perturbation theory fails)
    - NOT derived from L_M in GU (no calculation produces pi^2/b_0)
    - A HYPOTHESIS that happens to give a reasonable IR coupling
""")

# ============================================================================
# DECOMPOSITION: WHAT pi CONTRIBUTES TO COUPLING RUNNING
# ============================================================================

print("-" * 80)
print("DECOMPOSITION: pi in coupling running")
print("-" * 80)

print(f"""
  In the formula alpha(mu) = alpha(mu_0) / (1 + b_0*alpha(mu_0)*ln(mu^2/mu_0^2)/(4*pi)):

  The 4*pi comes from:
    - 2*pi^2 (Omega_4, angular integral in d=4 momentum space)
    - 1/(2*pi)^4 (Fourier transform normalization)
    - Combined: 2*pi^2 / (2*pi)^4 = 1/(8*pi^2)
    - With the gauge vertex factor of 2: gives 1/(16*pi^2) = 1/(4*pi)^2

  This is IDENTICAL for U(1), SU(2), SU(3), SU(5) — it's just the
  geometry of 4D momentum-space integration.

  The force HIERARCHY comes entirely from b_0:
    b_0(U(1)) = 41/10 = 4.1
    b_0(SU(2)) = -19/6 = -3.17  (note: NEGATIVE — coupling grows at low energy!)
    b_0(SU(3), Nf=3) = 9       (positive — asymptotic freedom)

  VERDICT: pi enters gauge running as 1/(16*pi^2), which is UNIVERSAL.
           Different forces differ through b_0, not through different pi^k.
""")

print("=" * 80)
print("DONE: 03_pi_in_gauge_loops.py")
print("=" * 80)
