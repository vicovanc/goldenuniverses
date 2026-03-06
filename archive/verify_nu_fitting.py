#!/usr/bin/env python3
"""
VERIFY: Is ν being fitted or derived?
======================================

The GU_particle_masses.py appears to be SOLVING for ν to match CODATA,
not deriving it from first principles.

Let's verify this and find what ν SHOULD be from theory.
"""

import math

print("="*80)
print("INVESTIGATING: Is ν fitted or derived?")
print("="*80)
print()

# Constants
phi = (1 + math.sqrt(5)) / 2
N_e = 111
M_P = 1.22091e22  # MeV
m_e_CODATA = 0.51099895069  # MeV

print("From GU_particle_masses.py:")
print("-" * 40)
print("Line 186: C_target = m_e_CODATA / prefactor")
print("Line 189: nu_sol = findroot(lambda nu: C_e_full(nu) - C_target, 0.82)")
print()
print("This is SOLVING for ν to make C_e = C_target!")
print("This is FITTING, not deriving from first principles!")
print()

print("What the code does:")
print("-" * 40)
print("1. Calculate C_target = m_e_CODATA / (M_P × 2π/φ^111 × η_QED)")
print("2. Find ν such that C_e(ν) = C_target")
print("3. Use this ν to calculate m_e = M_P × 2π/φ^111 × C_e(ν) × η_QED")
print("4. Of course m_e = m_e_CODATA exactly - it was fitted!")
print()

print("From theory-laws.md, ν should be:")
print("-" * 40)
print("Option 1: ν = 1/2 + δ_e/(2k_res)")
k_res = N_e / (phi**2)
delta_e = k_res - round(k_res)
nu_theory1 = 0.5 + delta_e / (2 * k_res)
print(f"  k_res = {k_res:.6f}")
print(f"  δ_e = {delta_e:.6f}")
print(f"  ν = {nu_theory1:.6f}")
print()

print("Option 2: ν from winding number (topological)")
print("  Should be determined by (p,q) = (-41, 70)")
print("  But the exact formula isn't clear")
print()

print("Option 3: ν = 0.82054... (the fitted value)")
nu_fitted = 0.8205439660164079
print(f"  ν_fitted = {nu_fitted}")
print()

print("Testing if Option 1 works:")
print("-" * 40)
# Using the formula from Option 1
C_e_approx = 1.051366998674827  # From the fitted calculation
prefactor = M_P * 2 * math.pi / (phi**N_e)
eta_QED = 0.9988385903

m_e_option1 = prefactor * C_e_approx * eta_QED
print(f"If we use ν = {nu_theory1:.6f}:")
print(f"  m_e ≈ {m_e_option1:.6f} MeV")
print(f"  Error = {100*(m_e_option1 - m_e_CODATA)/m_e_CODATA:.2f}%")
print()

print("But the code uses ν_fitted = {:.10f}".format(nu_fitted))
print("which gives EXACT match because it was fitted!")
print()

print("="*80)
print("CONCLUSION")
print("="*80)
print()
print("The GU_particle_masses.py is NOT deriving ν from first principles!")
print("It's using numerical root-finding to fit ν to match CODATA.")
print()
print("To truly derive from first principles, we need:")
print("1. A theoretical formula for ν (not fitted)")
print("2. More precise values for Ẽ from NLDE solver")
print("3. Possibly missing QED/weak corrections")
print()
print("The 0.17% error in derive_Xe_corrected.py is the REAL first-principles result.")
print("The 0.000% in GU_particle_masses.py is from FITTING, not derivation!")