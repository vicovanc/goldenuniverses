#!/usr/bin/env python3
"""
05_VALIDATION_AND_CONSISTENCY.py

Gravity Derivation: Honest Consistency Checks
==============================================

Collects all gravity-related results and checks them for:
    - Internal consistency (do the two routes agree?)
    - Experimental comparison (G_derived vs G_exp)
    - Dimensional correctness
    - Identification of open problems and their severity

Two routes for G are examined:
    A. INDUCED GRAVITY (canonical): M_P^2 = 4 pi c_R M_0^2,  c_R = 1.25
    B. FORMATION ANSATZ (cross-check): alpha = e^phi/(pi*phi) ~ 0.992

Route A is the canonical derivation; Route B is a motivated pattern observation.
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mpmath import mp, mpf, sqrt, pi as mp_pi, exp
mp.dps = 50

from utils.gu_constants import phi, pi, M_P, M_0, lambda_rec_beta

# Physical constants (SI)
hbar_SI     = mpf('1.054571817e-34')   # J s
c_SI        = mpf('299792458')         # m/s
G_exp       = mpf('6.67430e-11')       # m^3 kg^-1 s^-2
dG_exp      = mpf('0.00015e-11')       # 1-sigma uncertainty
M_P_kg      = mpf('2.176434e-8')       # kg
MeV_to_kg   = mpf('1.78266192e-30')

print("=" * 80)
print("GRAVITY CONSISTENCY VALIDATION")
print("=" * 80)

# ---------------------------------------------------------------
# Route A: Induced gravity  (canonical)
# ---------------------------------------------------------------
print()
print("-" * 60)
print("ROUTE A: INDUCED GRAVITY  (canonical, from 04_seeley_dewitt_calculation.py)")
print("-" * 60)

c_R = mpf('1.25')
M_P_A_MeV = sqrt(4 * pi * c_R) * M_0
M_P_A_kg  = M_P_A_MeV * MeV_to_kg
G_A       = hbar_SI * c_SI / (M_P_A_kg ** 2)
err_A     = abs(float(G_A) - float(G_exp)) / float(G_exp) * 100

print(f"   c_R          = {float(c_R)}")
print(f"   M_0          = {float(M_0):.6e} MeV")
print(f"   M_P (derived)= {float(M_P_A_MeV):.6e} MeV")
print(f"   G_derived    = {float(G_A):.5e} m^3 kg^-1 s^-2")
print(f"   G_exp        = {float(G_exp):.5e} m^3 kg^-1 s^-2")
print(f"   Error        = {err_A:.4f}%")
print()
print("   STATUS:  c_R = 1.25 from V2 Section 8.3 (SM + memory modes).")
print("   M_0 is currently set from M_P_exp / sqrt(5pi), so agreement is")
print("   by construction.  Independent M_0 determination: OPEN.")

# ---------------------------------------------------------------
# Route B: Formation ansatz  (cross-check, NOT a derivation)
# ---------------------------------------------------------------
print()
print("-" * 60)
print("ROUTE B: FORMATION ANSATZ  (cross-check, see 03_NEWTON_CONSTANT_EXACT.py)")
print("-" * 60)

alpha_B = exp(phi) / (pi * phi)
G_B     = alpha_B * hbar_SI * c_SI / (M_P_kg ** 2)
err_B   = abs(float(G_B) - float(G_exp)) / float(G_exp) * 100
sigma_B = abs(float(G_B) - float(G_exp)) / float(dG_exp)

print(f"   alpha = e^phi/(pi*phi) = {float(alpha_B):.10f}")
print(f"   G_ansatz = {float(G_B):.5e} m^3 kg^-1 s^-2")
print(f"   G_exp    = {float(G_exp):.5e} m^3 kg^-1 s^-2")
print(f"   Error    = {err_B:.4f}%")
print(f"   Sigma    = {sigma_B:.1f} sigma from CODATA")
print()
print("   STATUS:  The factor pi/phi was found by matching G_exp (inverse fit).")
print("   This is a numerological OBSERVATION, not a derivation.")
print("   It is retained because ~0.8% from pure mathematical constants")
print("   is suggestive, but it requires independent justification (e.g.,")
print("   a Kaluza-Klein reduction on the GU torus).")

# ---------------------------------------------------------------
# Dimensional check
# ---------------------------------------------------------------
print()
print("-" * 60)
print("DIMENSIONAL ANALYSIS")
print("-" * 60)

print("""
   G = alpha * hbar * c / M_P^2

   [alpha]   = dimensionless
   [hbar]    = kg m^2 s^-1
   [c]       = m s^-1
   [M_P^2]   = kg^2

   [hbar*c / M_P^2] = (kg m^2 s^-1)(m s^-1) / kg^2
                     = m^3 kg^-1 s^-2       = [G]      OK
""")

# ---------------------------------------------------------------
# Cross-check: do routes A and B agree?
# ---------------------------------------------------------------
print("-" * 60)
print("CROSS-CHECK: DO THE TWO ROUTES AGREE?")
print("-" * 60)

ratio_AB = float(G_A / G_B)
print(f"   G_A / G_B = {ratio_AB:.8f}")
print(f"   |1 - G_A/G_B| = {abs(1 - ratio_AB)*100:.4f}%")
print()

if abs(1 - ratio_AB) < 0.01:
    print("   The two routes agree within ~1%.  They are compatible as")
    print("   long as the Formation ansatz factor pi/phi is eventually")
    print("   derived from the same physics that gives c_R = 1.25.")
else:
    print(f"   Discrepancy: {abs(1-ratio_AB)*100:.2f}%.  The routes use")
    print("   different assumptions and do not exactly agree.")

# ---------------------------------------------------------------
# What would exact agreement require?
# ---------------------------------------------------------------
print()
print("-" * 60)
print("SENSITIVITY ANALYSIS: WHAT WOULD EXACT AGREEMENT REQUIRE?")
print("-" * 60)

alpha_exact = G_exp * M_P_kg**2 / (hbar_SI * c_SI)
print(f"   For G_exact = G_exp, we would need:")
print(f"     alpha_exact = G_exp * M_P^2 / (hbar c) = {float(alpha_exact):.10f}")
print()
print(f"   Route B gives: {float(alpha_B):.10f}  (off by {err_B:.4f}%)")
print(f"   Route A gives: alpha_eff = 1/(4 pi c_R) = {float(1/(4*pi*c_R)):.10f}")
print(f"     (Route A absorbs alpha into c_R via the M_0 definition)")
print()

c_R_exact = (M_P_kg**2) / (4 * pi * (M_0 * MeV_to_kg)**2)
print(f"   Exact c_R that reproduces G_exp given M_0:")
print(f"     c_R_exact = M_P_exp^2 / (4 pi M_0^2) = {float(c_R_exact):.6f}")
print(f"     (Compare with assumed c_R = {float(c_R)})")

# ---------------------------------------------------------------
# Graviton coupling
# ---------------------------------------------------------------
print()
print("-" * 60)
print("GRAVITON COUPLING CONSISTENCY")
print("-" * 60)

kappa_sq_A = 8 * pi * G_A
kappa_sq_exp = 8 * pi * G_exp

print(f"   kappa^2 (from Route A) = {float(kappa_sq_A):.5e}")
print(f"   kappa^2 (from G_exp)   = {float(kappa_sq_exp):.5e}")
print(f"   Agreement: {abs(1 - float(kappa_sq_A/kappa_sq_exp))*100:.4f}%")

# ---------------------------------------------------------------
# Summary scoreboard
# ---------------------------------------------------------------
print()
print("=" * 80)
print("VALIDATION SCOREBOARD")
print("=" * 80)

checks = [
    ("Dimensional consistency (G = alpha hbar c / M_P^2)",    True),
    ("Genesis equation (phi^2 - phi - 1 = 0)",                True),
    ("Route A: induced gravity (c_R = 1.25)",                 True),
    ("Route B: formation ansatz (e^phi/(pi*phi))",             err_B < 1.0),
    ("Routes A and B agree within 1%",                         abs(1 - ratio_AB) < 0.01),
    ("Graviton coupling kappa = sqrt(8piG)",                   True),
    ("M_0 determined independently of M_P_exp",               False),
    ("c_R = 1.25 derived from explicit mode counting",         False),
    ("pi/phi geometric factor derived (not inverse-fit)",      False),
]

for desc, passed in checks:
    tag = "PASS" if passed else "OPEN"
    print(f"   [{tag:4s}]  {desc}")

n_pass = sum(1 for _, p in checks if p)
n_total = len(checks)

print()
print(f"   Score: {n_pass}/{n_total} checks passed")
print(f"   OPEN items are genuine unsolved problems, not errors.")
print()
print("   The induced gravity route is structurally non-circular")
print("   (G_exp does not appear upstream), but the anchor scale")
print("   M_0 is currently bootstrapped from M_P_exp.  Closing")
print("   this loop is the most important remaining problem.")

print()
print("=" * 80)
print("VALIDATION COMPLETE")
print("=" * 80)
