#!/usr/bin/env python3
"""
02_pi_in_recursion_engine.py
============================

Shows how pi propagates from the Genesis Vector through the recursion engine
U_n = f(U_{n-1}) * e^(i*theta) to the particle mass formula.

The key result: every particle mass contains the SAME factor of 2*pi from
the recursion phase. This factor does NOT depend on the gauge sector (k).

Reference: theory-laws.md, lines 3444-3829 (RC-STEP 1 through RC-STEP 10).
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from utils.gu_constants import phi, pi, M_P, M_0, N_e, N_QCD, N_EW, N_GUT

PI = float(pi)
PHI = float(phi)
M0 = float(M_0)          # MeV
MP = float(M_P)           # MeV

print("=" * 80)
print("pi IN THE RECURSION ENGINE")
print("How 2*pi propagates to the mass formula for ALL particles")
print("=" * 80)

# ============================================================================
# THE RECURSION ENGINE
# ============================================================================

print("\n" + "-" * 80)
print("THE RECURSION ENGINE (Formation doc, Section 4.2)")
print("-" * 80)

print("""
  U_n = f(U_{n-1}) * e^(i*theta)

  where:
    f      = structural transformation (scaling by phi)
    e^(iθ) = Golden Angle rotation, theta = 2*pi/phi^2

  After n steps:
    Total phase:  Theta_n = n * 2*pi/phi^2
    Phase/step:   Delta_theta = 2*pi/phi^2
""")

theta = 2 * PI / PHI**2

print(f"  theta = 2*pi/phi^2 = {theta:.10f} rad")
print(f"  Total phase at n=111: {111 * theta:.4f} rad = {111 * theta / (2*PI):.4f} full turns")
print(f"  Total phase at n=95:  {95 * theta:.4f} rad = {95 * theta / (2*PI):.4f} full turns")
print(f"  Total phase at n=80:  {80 * theta:.4f} rad = {80 * theta / (2*PI):.4f} full turns")

# ============================================================================
# DERIVING omega_target(n)
# ============================================================================

print("\n" + "-" * 80)
print("DERIVING omega_target(n) — theory-laws.md lines 3742-3757")
print("-" * 80)

print("""
  The target frequency for the soliton at epoch n is the phase rate
  of the recursion at that node:

    omega_target(n) = Delta_theta / Delta_t(n)

  where Delta_t(n) ~ phi^n / M_0  (from the X-critical framework).

  So:
    omega_target(n) = (2*pi/phi^2) * (M_0/phi^n) = M_0 * 2*pi * phi^{-(n+2)}

  CRITICAL OBSERVATION: The factor 2*pi appears for ALL n.
  It does NOT depend on which gauge sector is active at epoch n.
""")

def omega_target(n):
    return M0 * 2 * PI * PHI**(-(n + 2))

# ============================================================================
# THE MASS FORMULA — same 2*pi for every particle
# ============================================================================

print("\n" + "-" * 80)
print("THE MASS FORMULA — 2*pi is universal")
print("-" * 80)

print("""
  In the strong-lock limit: E_particle ~ omega_target(n)

  E(n) = M_0 * 2*pi * phi^{-(n+2)}
       = (M_P/sqrt(5*pi)) * 2*pi * phi^{-(n+2)}
       = M_P * (2*pi / sqrt(5*pi)) * phi^{-(n+2)}
       = M_P * (2*sqrt(pi/5)) * phi^{-(n+2)}

  Equivalently, using N = n and the standard form:
  m = M_P * (2*pi * C / phi^N)

  The factor 2*pi is the SAME for:
    - Electron (N=111) — Pattern-0 (EM)
    - Quarks (N=97-110) — confined by Pattern-2 (QCD)
    - W/Z (N~80) — Pattern-1 (EW)
    - GUT particles (N=67) — Pattern-3 (GUT)
""")

particles = [
    ("Electron", N_e, "EM (k=0)"),
    ("Up quark", 110, "QCD (k=2)"),
    ("Down quark", 105, "QCD (k=2)"),
    ("Charm quark", 97, "QCD (k=2)"),
    ("Bottom quark", 89, "QCD/EW (k=2/1)"),
    ("Top quark", 81, "EW (k=1)"),
    ("W/Z scale", 80, "EW (k=1)"),
    ("QCD scale", N_QCD, "QCD (k=2)"),
    ("GUT scale", N_GUT, "GUT (k=3)"),
]

print(f"\n  {'Particle':<16} {'N':>4}  {'omega_target (MeV)':>20}  {'Pattern':>12}  {'2*pi factor'}")
print("  " + "-" * 75)
for name, N, pattern in particles:
    omega = omega_target(N)
    print(f"  {name:<16} {N:>4}  {omega:>20.4f}  {pattern:>12}  2*pi (same)")

# ============================================================================
# DECOMPOSING THE pi CONTENT
# ============================================================================

print("\n" + "-" * 80)
print("DECOMPOSING THE pi CONTENT OF EACH MASS")
print("-" * 80)

print("""
  Each mass formula m(N) = M_0 * 2*pi * phi^{-(N+2)} * C_particle contains:

  1. Factor of 2*pi from the recursion phase (Golden Angle per step)
     — This is the SAME for all particles
     — It comes from theta = 2*pi/phi^2 in U_n

  2. Factor of 1/sqrt(5*pi) from M_0 = M_P/sqrt(5*pi)
     — This is the SAME for all particles
     — It comes from induced gravity: M_P = sqrt(5*pi) * M_0

  3. Factor phi^{-N} from the golden ladder
     — This is DIFFERENT for each particle (different epoch N)
     — It comes from the scaling f in U_n, NOT from pi

  4. Factor C_particle from the soliton structure
     — This is DIFFERENT for each particle
     — For electron: C_e = 1.0550 (from NLDE BVP at nu_topo)
     — For proton: C_mem = 1.2837 (from MIT bag memory integral)

  NOWHERE does a factor pi^k appear that depends on the gauge sector k.
  The ONLY pi factors (2*pi and 1/sqrt(5*pi)) are UNIVERSAL.
""")

# count total powers of pi in the formula
print("  Powers of pi in m = M_P * (2*pi) * phi^{-(N+2)} / sqrt(5*pi) * C:")
print(f"    2*pi contributes: pi^1")
print(f"    1/sqrt(5*pi) contributes: pi^(-1/2)")
print(f"    Net: pi^(1 - 1/2) = pi^(1/2) = sqrt(pi)")
print(f"    sqrt(pi) = {np.sqrt(PI):.10f}")
print(f"    This is the SAME for electron, quarks, W/Z, GUT particles.")

# ============================================================================
# VERDICT
# ============================================================================

print("\n" + "-" * 80)
print("VERDICT")
print("-" * 80)

print("""
  The recursion engine U_n = f(U_{n-1}) * e^(i*2*pi/phi^2) gives:

  1. A UNIVERSAL factor of 2*pi in omega_target(n) for ALL particles
  2. NO mechanism for different powers of pi at different epochs
  3. The force hierarchy (EM vs Weak vs Strong vs GUT) comes from
     DIFFERENT EPOCHS (different N), not from different pi factors

  Pattern-k as "pi^k enhancement" CANNOT originate from the recursion engine.
  The recursion gives ONE factor of 2*pi. Always. For everything.
""")

print("=" * 80)
print("DONE: 02_pi_in_recursion_engine.py")
print("=" * 80)
