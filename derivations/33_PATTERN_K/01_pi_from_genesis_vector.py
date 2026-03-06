#!/usr/bin/env python3
"""
01_pi_from_genesis_vector.py
============================

Traces where pi FIRST enters the Golden Universe theory.

The Genesis Vector Z_1 = [M_P/(4*sqrt(pi))] * e^(i*2*pi/phi^2) is the
single complex impulse that creates the universe. It contains pi in two
independent places:

  1. MAGNITUDE: |Z_1| = M_P/(4*sqrt(pi))
     Origin: Bekenstein-Hawking entropy of a Planck-scale black hole.
     S_BH = A/(4*l_P^2) = pi*r_s^2/l_P^2. The Planck sphere area is
     4*pi*l_P^2, giving the normalization factor 4*sqrt(pi).

  2. PHASE: arg(Z_1) = 2*pi/phi^2  (the Golden Angle ~ 137.5 degrees)
     Origin: Maximal non-resonant packing of a circle. The unique angle
     that partitions a full turn (2*pi) most irrationally is 2*pi/phi^2.

Reference: Formation document, lines 20, 421-475, 464-475.
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from utils.gu_constants import phi, pi, M_P

PI = float(pi)
PHI = float(phi)
M_P_kg = 2.176434e-8   # Planck mass in kg
M_P_GeV = float(M_P) / 1e3  # GeV
l_P = 1.616255e-35     # Planck length in meters

print("=" * 80)
print("WHERE pi FIRST ENTERS THE GOLDEN UNIVERSE")
print("Tracing pi from the Genesis Vector Z_1")
print("=" * 80)

# ============================================================================
# SOURCE 1: pi IN THE MAGNITUDE — Bekenstein-Hawking entropy
# ============================================================================

print("\n" + "-" * 80)
print("SOURCE 1: pi in |Z_1| = M_P / (4*sqrt(pi))")
print("-" * 80)

print("""
The Planck-scale black hole has Schwarzschild radius r_s = 2*G*M/c^2 = 2*l_P
(for M = M_P). Its horizon area and entropy are:

  A = 4*pi*r_s^2 = 4*pi*(2*l_P)^2 = 16*pi*l_P^2

  S_BH = A / (4*l_P^2) = 4*pi

The pi here is GEOMETRIC — it's the ratio of a sphere's area to the square
of its radius. This is the area of the Planck horizon.

The magnitude of Z_1 is the energy of the smallest stable quantum of
spacetime, normalized by this geometric factor:

  |Z_1| = M_P*c^2 / (4*sqrt(pi))
""")

A_planck = 16 * PI * l_P**2
S_BH = A_planck / (4 * l_P**2)

Z1_magnitude_kg = M_P_kg / (4 * np.sqrt(PI))
Z1_magnitude_GeV = M_P_GeV / (4 * np.sqrt(PI))

print(f"  Planck horizon area:   A = 16*pi*l_P^2 = {A_planck:.4e} m^2")
print(f"  BH entropy:            S_BH = 4*pi = {S_BH:.6f}")
print(f"  |Z_1| = M_P/(4*sqrt(pi)) = {Z1_magnitude_kg:.4e} kg")
print(f"                            = {Z1_magnitude_GeV:.4e} GeV")
print(f"  Fraction of M_P:       {1/(4*np.sqrt(PI)):.6f} = 0.1410...")
print(f"  sqrt(pi) = {np.sqrt(PI):.10f}")

print(f"\n  KEY: The sqrt(pi) here is from the AREA of a sphere (4*pi*r^2).")
print(f"       It would be present in ANY theory with a Planck-scale horizon.")

# ============================================================================
# SOURCE 2: pi IN THE PHASE — Golden Angle
# ============================================================================

print("\n" + "-" * 80)
print("SOURCE 2: pi in arg(Z_1) = 2*pi/phi^2  (Golden Angle)")
print("-" * 80)

print("""
The Golden Angle theta = 2*pi/phi^2 is the unique angle that partitions a
circle most irrationally. It arises from:

  1. A full circle has circumference 2*pi (GEOMETRIC: pi = circumference/diameter)
  2. The golden ratio phi divides it optimally: theta = 2*pi * (1 - 1/phi) = 2*pi/phi^2

This ensures the recursion engine U_n = f(U_{n-1}) * e^(i*theta) is
maximally non-resonant — no finite number of steps brings the phase back
to its starting point.
""")

theta_golden = 2 * PI / PHI**2
theta_degrees = theta_golden * 180 / PI

print(f"  Golden Angle:  theta = 2*pi/phi^2 = {theta_golden:.10f} rad")
print(f"                       = {theta_degrees:.6f} degrees")
print(f"  phi^2 = {PHI**2:.10f}")
print(f"  2*pi  = {2*PI:.10f}")
print(f"  1/phi = {1/PHI:.10f} (complement: 1 - 1/phi = {1 - 1/PHI:.10f})")
print(f"  Check: 2*pi*(1 - 1/phi) = {2*PI*(1-1/PHI):.10f} = theta? {np.isclose(2*PI*(1-1/PHI), theta_golden)}")

# ============================================================================
# SOURCE ANALYSIS: Two independent geometric origins
# ============================================================================

print("\n" + "-" * 80)
print("ANALYSIS: Two independent geometric origins of pi")
print("-" * 80)

print("""
pi enters Z_1 from two DISTINCT geometric facts:

  1. MAGNITUDE: pi = (area of circle) / r^2
     This is Euclidean geometry in 2D. The horizon area 4*pi*r^2 uses
     the same pi. It enters ANY theory with spherical symmetry.

  2. PHASE: pi = (half-circumference) / r
     The full turn 2*pi partitions the unit circle. The Golden Angle
     2*pi/phi^2 uses this. It enters ANY theory with circular phases.

Both sources give the SAME mathematical constant pi because Euclidean
geometry is self-consistent. There is no "Pattern-k" here — just geometry.
""")

# ============================================================================
# THE FULL GENESIS VECTOR
# ============================================================================

print("\n" + "-" * 80)
print("THE FULL GENESIS VECTOR")
print("-" * 80)

Z1_real = Z1_magnitude_kg * np.cos(theta_golden)
Z1_imag = Z1_magnitude_kg * np.sin(theta_golden)

print(f"  Z_1 = [M_P/(4*sqrt(pi))] * e^(i*2*pi/phi^2)")
print(f"       = {Z1_magnitude_kg:.4e} * e^(i*{theta_golden:.6f})")
print(f"       = ({Z1_real:.4e}) + i*({Z1_imag:.4e})  kg")
print(f"  |Z_1| = {Z1_magnitude_kg:.4e} kg")
print(f"  arg(Z_1) = {theta_golden:.6f} rad = {theta_degrees:.2f} degrees")

# ============================================================================
# WHAT THIS MEANS FOR PATTERN-K
# ============================================================================

print("\n" + "-" * 80)
print("IMPLICATIONS FOR PATTERN-K")
print("-" * 80)

print("""
  The Genesis Vector contains exactly ONE factor of sqrt(pi) in the magnitude
  and ONE factor of 2*pi in the phase. These are:

    - The SAME pi (3.14159...)
    - From GEOMETRY (sphere area, circle circumference)
    - UNIVERSAL — they don't depend on which gauge group is active

  There is NO mechanism in Z_1 that gives DIFFERENT powers of pi for
  different forces. The claim "L_eff = L_0 * pi^k" with k=0,1,2,3 for
  EM, Weak, Strong, GUT cannot originate from the Genesis Vector.

  VERDICT: pi enters GU from geometry. It is the same pi everywhere.
           Pattern-k as "pi^k enhancement per force" is NOT sourced here.
""")

print("=" * 80)
print("DONE: 01_pi_from_genesis_vector.py")
print("=" * 80)
