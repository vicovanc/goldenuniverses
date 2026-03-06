#!/usr/bin/env python3
"""
05_pi_on_omega_torus.py
=======================

Topological contributions from the Omega-torus.

The Omega-field lives on an internal SU(5) torus with angular coordinates
having period 2*pi. We check every place where pi can arise from the torus
topology and ask: does any of them give pi^k for different k?

Sources of pi from the torus:
  1. Angular integrals: int_0^{2*pi} d(theta) = 2*pi per compact dimension
  2. Wilson loops: W = exp(i * oint A) with A over a 2*pi-periodic cycle
  3. Instanton number: Q = (1/(8*pi^2)) * int tr(F*F_tilde)
  4. Casimir energy: E_C ~ pi^(d/2)/Gamma(d/2+1) per compact dimension

Reference: theory-laws.md, lines 7048-7100 (topological term).
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from scipy.special import gamma as gamma_func
from utils.gu_constants import phi, pi, alpha_s_MZ

PI = float(pi)
PHI = float(phi)

print("=" * 80)
print("pi ON THE OMEGA-TORUS")
print("Angular integrals, instantons, Casimir energy")
print("=" * 80)

# ============================================================================
# SOURCE 1: ANGULAR INTEGRALS
# ============================================================================

print("\n" + "-" * 80)
print("SOURCE 1: Angular integrals on the torus")
print("-" * 80)

print("""
  The Omega-torus has rank-4 angular coordinates (for SU(5)):
    theta_1, theta_2, theta_3, theta_4  each in [0, 2*pi)

  Integrating any smooth function over the torus gives:

    int f(theta) d^4(theta) = (2*pi)^4 * <f>

  where <f> is the average value. The (2*pi)^4 is a VOLUME factor.

  For the Omega-field partition function:
    Z = int [D Omega] exp(-S[Omega])

  The torus contribution is a (2*pi)^4 normalization — it's the same
  for ALL sectors of the theory (EM, Weak, Strong, GUT).
""")

torus_vol = (2 * PI)**4
print(f"  Torus volume: (2*pi)^4 = {torus_vol:.2f}")
print(f"  Per dimension: 2*pi = {2*PI:.6f}")
print(f"  This is UNIVERSAL — same for all gauge sectors.")

# ============================================================================
# SOURCE 2: WILSON LOOPS
# ============================================================================

print("\n" + "-" * 80)
print("SOURCE 2: Wilson loops on the torus")
print("-" * 80)

print("""
  A Wilson loop around the k-th cycle of the torus:

    W_k = exp(i * oint_{C_k} A)  where C_k has length 2*pi*R_k

  For winding numbers (p, q) on a 2-torus, the loop encloses:

    W_{p,q} = exp(i * (p*theta_1 + q*theta_2))

  The integers (p, q) determine WHICH representation of the gauge group
  the particle belongs to, but the factor of 2*pi in the angle is the
  SAME for all (p, q). Different winding numbers give different particles,
  NOT different powers of pi.

  Example:
    - Electron: (p,q) = (3,2) or similar on the SU(5) torus
    - Quarks: different (p,q) on the same torus
    - Both see the same 2*pi periodicity
""")

for p, q in [(1,0), (0,1), (1,1), (2,1), (3,2)]:
    phase_at_theta = p * PI/4 + q * PI/3
    print(f"  W({p},{q}) at theta=(pi/4, pi/3): exp(i*{phase_at_theta:.4f}) = "
          f"({np.cos(phase_at_theta):.4f}, {np.sin(phase_at_theta):.4f})")

print(f"\n  The 2*pi periodicity is the same for all (p,q).")
print(f"  No pi^k dependence on the gauge sector.")

# ============================================================================
# SOURCE 3: INSTANTON NUMBER AND ACTION
# ============================================================================

print("\n" + "-" * 80)
print("SOURCE 3: Instanton number and action")
print("-" * 80)

print("""
  From theory-laws.md line 7100, the topological term:

    L_top = -(kappa/(8*pi^2)) * theta_QCD * tr(F * F_tilde)

  The instanton number is:

    Q = (1/(8*pi^2)) * int d^4x tr(F * F_tilde) = integer

  The 8*pi^2 comes from the normalization:
    - In d=4, the unit instanton has action S = 8*pi^2/g^2
    - This is from integrating |F|^2 over R^4 for the BPST instanton
    - Specifically: S = (1/(2g^2)) * int d^4x tr(F^2) = 8*pi^2/g^2

  At the QCD scale where alpha_s = g^2/(4*pi):
""")

alpha_s_vals = [0.3, 0.5, 1.0, 1.097]
print(f"  {'alpha_s':<10} {'g^2':<10} {'S_inst':<15} {'exp(-S)':<15} {'pi^2/b_0?'}")
print("  " + "-" * 65)
for alpha_s in alpha_s_vals:
    g2 = 4 * PI * alpha_s
    S_inst = 8 * PI**2 / g2
    exp_S = np.exp(-S_inst)
    is_gu = " <-- GU" if abs(alpha_s - 1.097) < 0.01 else ""
    print(f"  {alpha_s:<10.3f} {g2:<10.4f} {S_inst:<15.4f} {exp_S:<15.2e}{is_gu}")

print(f"""
  The instanton action S = 8*pi^2/g^2 SUPPRESSES non-perturbative effects.
  At alpha_s ~ 1.097: S ~ 5.7, exp(-S) ~ 0.003

  This is a pi^2 in the DENOMINATOR (suppression), not an enhancement.
  And it's the SAME pi^2 for SU(3) whether k=2 or not.

  For SU(2) instantons: same formula S = 8*pi^2/g_W^2, different g.
  The pi^2 is still 8*pi^2 — not 8*pi^1.
""")

# ============================================================================
# SOURCE 4: CASIMIR ENERGY
# ============================================================================

print("-" * 80)
print("SOURCE 4: Casimir energy on the torus")
print("-" * 80)

print("""
  For a free field on a d-dimensional torus of radius R, the Casimir energy is:

    E_C = -pi^(d/2) / (Gamma(d/2+1) * (2R)^d) * sum_n n^{-d} * (degeneracy factor)

  The pi^(d/2) comes from the volume of a d-dimensional unit ball:
    V_d = pi^(d/2) / Gamma(d/2 + 1)
""")

print(f"  {'d':<4} {'pi^(d/2)':<12} {'Gamma(d/2+1)':<14} {'V_d':<12} {'Ratio'}")
print("  " + "-" * 50)
for d in range(1, 7):
    pi_factor = PI**(d/2)
    gamma_factor = gamma_func(d/2 + 1)
    Vd = pi_factor / gamma_factor
    print(f"  {d:<4} {pi_factor:<12.4f} {gamma_factor:<14.4f} {Vd:<12.4f} pi^{d/2:.1f}")

print(f"""
  For d=4 (our compact torus): pi^2 = {PI**2:.4f}
  For d=2 (a 2-torus): pi^1 = {PI:.4f}

  Could this give pi^k for different sectors?
  - If k=1 (Weak) uses d=2 compact dimensions: pi^1
  - If k=2 (Strong) uses d=4 compact dimensions: pi^2

  BUT: The GU Omega-torus has the SAME dimension for all forces.
  The SU(5) torus has rank 4, and ALL gauge bosons live on it.
  There is no mechanism where different forces see different d.
""")

# ============================================================================
# SOURCE 5: TRACE OVER TORUS MODES
# ============================================================================

print("-" * 80)
print("SOURCE 5: Trace over torus modes (Kaluza-Klein spectrum)")
print("-" * 80)

print("""
  On a compact torus, fields have a discrete KK spectrum:
    m_n = n / R   for n = 0, 1, 2, ...

  The partition function (heat kernel trace):
    Z(t) = sum_n exp(-m_n^2 * t) = sum_n exp(-n^2*t/R^2)

  Using the Jacobi theta function:
    Z(t) = sqrt(pi*R^2/t) * (1 + 2*sum_{n=1} exp(-pi^2*n^2*R^2/t))

  The sqrt(pi) here is from Poisson summation — the Fourier transform
  of a Gaussian. It's the SAME pi as everywhere else.

  For the full SU(5) torus with rank 4:
    Z(t) = (pi*R^2/t)^2 * (1 + ...)

  This gives pi^2 from the rank-4 torus, but it's ALWAYS pi^2 for ALL
  fields on the same torus. Different gauge sectors don't see different
  powers of pi from the KK trace.
""")

# ============================================================================
# SUMMARY TABLE
# ============================================================================

print("=" * 80)
print("SUMMARY: Where pi enters from the Omega-torus")
print("=" * 80)

print(f"""
  {'Source':<30} {'pi factor':<20} {'k-dependent?':<15} {'Status'}
  {'-'*75}
  {'Angular integration':<30} {'(2*pi)^4 = vol':<20} {'No':<15} {'Universal'}
  {'Wilson loops':<30} {'2*pi per cycle':<20} {'No':<15} {'Same for all (p,q)'}
  {'Instanton action':<30} {'8*pi^2/g^2':<20} {'No':<15} {'Universal formula'}
  {'Casimir energy':<30} {'pi^(d/2)':<20} {'No':<15} {'Same d for all forces'}
  {'KK trace':<30} {'pi^(rank/2)':<20} {'No':<15} {'Same torus for all'}

  VERDICT: The Omega-torus produces factors of pi from angular integration,
  instanton normalization, and the heat kernel. ALL of these are UNIVERSAL —
  the same for every gauge sector. There is no mechanism that gives
  DIFFERENT powers of pi for different forces.

  Pattern-k as "pi^k from the torus" is NOT derived.
""")

print("=" * 80)
print("DONE: 05_pi_on_omega_torus.py")
print("=" * 80)
