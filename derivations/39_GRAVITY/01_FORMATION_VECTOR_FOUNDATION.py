#!/usr/bin/env python3
"""
01_FORMATION_VECTOR_FOUNDATION.py

Golden Universe Theory: Formation Vector Z_1 and Gravity Context
================================================================

Z_1 = [M_P / (4 sqrt(pi))]  *  exp(i * 2 pi / phi^2)    (Law 15)

KEY CLARIFICATION:
    Z_1 is a CONSEQUENCE of gravity, not a derivation route for G.
    M_P appears in the magnitude of Z_1, and M_P is derived from
    induced gravity (Seeley-DeWitt, see 04_seeley_dewitt_calculation.py).

    The correct dependency order is:
        Omega spectrum  ->  c_R  ->  M_P  ->  Z_1

    Z_1 provides the INITIAL CONDITIONS for the Omega field (phase and
    energy scale) but does not determine G.  G is determined by the
    heat-kernel coefficient c_R from the particle spectrum.

This script computes Z_1 components and their physical interpretation.
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mpmath import mp, mpf, sqrt, pi as mp_pi, exp
mp.dps = 50

from utils.gu_constants import phi, pi, M_P, M_0, lambda_rec_beta

MeV_to_kg = mpf('1.78266192e-30')

print("=" * 80)
print("FORMATION VECTOR Z_1  (Law 15)")
print("=" * 80)
print()
print("Z_1  =  [M_P / (4 sqrt(pi))]  *  exp(i * 2 pi / phi^2)")
print()
print("Dependency order:  Omega spectrum -> c_R -> M_P -> Z_1")
print("Z_1 is a CONSEQUENCE of induced gravity, not a derivation of G.")

# ---------------------------------------------------------------
# Magnitude
# ---------------------------------------------------------------
print()
print("-" * 60)
print("1. MAGNITUDE: |Z_1| = M_P / (4 sqrt(pi))")
print("-" * 60)

Z1_mag_MeV = M_P / (4 * sqrt(pi))
Z1_mag_kg  = Z1_mag_MeV * MeV_to_kg

print(f"   M_P           = {float(M_P):.6e} MeV")
print(f"   4 sqrt(pi)    = {float(4 * sqrt(pi)):.6f}")
print(f"   |Z_1|         = {float(Z1_mag_MeV):.6e} MeV")
print(f"   |Z_1|         = {float(Z1_mag_kg):.6e} kg")
print()
print("   Origin (Formation document):")
print("     Minimal Planck-area White Hole: S = k_B / 4")
print("     Bekenstein-Hawking  =>  |Z_1| = M_P / (4 sqrt(pi))")
print("     pi arises from spherical horizon geometry.")

# ---------------------------------------------------------------
# Phase
# ---------------------------------------------------------------
print()
print("-" * 60)
print("2. PHASE: theta = 2 pi / phi^2  (Golden Angle)")
print("-" * 60)

theta = 2 * pi / (phi**2)

print(f"   phi^2         = {float(phi**2):.10f}")
print(f"   theta         = {float(theta):.10f} rad")
print(f"   theta         = {float(theta * 180 / pi):.6f} deg")
print()
print("   Origin: maximally non-periodic twist (irrational winding).")
print("   Ensures no exact recurrence -> stable complexity.")

# ---------------------------------------------------------------
# Universal memory ratio
# ---------------------------------------------------------------
print()
print("-" * 60)
print("3. UNIVERSAL MEMORY RATIO: e^phi / pi^2")
print("-" * 60)

print(f"   e^phi / pi^2  = {float(lambda_rec_beta):.10f}")
print()
print("   This ratio drives all gauge couplings (Law 32):")
print("     alpha_particle = (e^phi / pi^2) / |q_particle|")
print("   It is NOT a direct graviton coupling.")
print("   Graviton coupling:  kappa = sqrt(8 pi G)  (from induced gravity).")

# ---------------------------------------------------------------
# Initial conditions for Omega
# ---------------------------------------------------------------
print()
print("-" * 60)
print("4. Z_1 AS INITIAL CONDITION FOR OMEGA FIELD")
print("-" * 60)

print(f"   Z_1 seeds the Omega substrate at the Planck epoch:")
print(f"     Re(Z_1) -> initial spatial energy density")
print(f"     Im(Z_1) -> initial phase (Golden Angle)")
print(f"     X_0 = |Re(Z_1)| = initial FRG scale")
print()

X_0 = abs(Z1_mag_MeV * exp(1j * float(theta)).real)
print(f"   X_0 = |Z_1| * |cos(theta)| = {float(X_0):.6e} MeV")
print()
print("   The FRG flow then runs from X_0 downward through 111 epochs")
print("   to the electron scale X_e, with all couplings determined by")
print("   the heat-kernel UV initial conditions (FRG-STEP 2).")

# ---------------------------------------------------------------
# What Z_1 does NOT determine
# ---------------------------------------------------------------
print()
print("-" * 60)
print("5. WHAT Z_1 DOES NOT DETERMINE")
print("-" * 60)

print("""   Z_1 does NOT:
     - Derive Newton's constant G  (that comes from induced gravity)
     - Provide winding numbers for gravity (gravity is not a fermion)
     - Replace the Seeley-DeWitt calculation

   Z_1 DOES:
     - Set the energy scale for the cosmological initial conditions
     - Provide the phase structure for the FRG starting point
     - Encode the thermodynamic origin (S = k_B/4) of the Planck scale
     - Serve as a cross-check: |Z_1| ~ M_P / 7.1 is consistent with
       the induced-gravity relation M_P = sqrt(5 pi) * M_0
""")

print("=" * 80)
print("FORMATION VECTOR FOUNDATION COMPLETE")
print("Next: 02_SPACETIME_GEOMETRY_DERIVATION.py (torus -> spacetime)")
print("=" * 80)
