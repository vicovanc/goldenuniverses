#!/usr/bin/env python3
"""
HIGH PRECISION ELECTRON MASS CALCULATION
=========================================

Using 50+ decimal precision to find the exact CODATA value.
We'll systematically check if the 0.17% error is due to:
1. Insufficient decimal precision
2. Missing terms in the formula
3. Incorrect values for derived parameters

Date: 2026-02-11
"""

from mpmath import mp, mpf, sqrt, pi as mp_pi, sin, cos, exp, log

# Set precision to 50 decimal places
mp.dps = 50

print("="*80)
print("HIGH PRECISION ELECTRON MASS CALCULATION")
print("50 Decimal Places Precision")
print("="*80)
print()

# =============================================================================
# FUNDAMENTAL CONSTANTS (50 decimals)
# =============================================================================

print("FUNDAMENTAL CONSTANTS:")
print("-" * 40)

# Golden ratio to 50 decimals
phi = (1 + sqrt(5)) / 2
print(f"φ = {phi}")
print(f"  = {float(phi):.15f} (first 15 decimals)")

# Pi to 50 decimals
pi = mp_pi
print(f"π = {pi}")

# Euler's number
e = mp.e
print(f"e = {e}")

# Physical constants (CODATA 2018/2022)
M_P_MeV = mpf('1.22091000000000000000000000000000000000000000000000e22')  # Planck mass in MeV
print(f"M_P = {M_P_MeV} MeV")

# Target: CODATA electron mass
m_e_CODATA = mpf('0.51099895069')  # MeV (CODATA 2022)
print(f"m_e (CODATA) = {m_e_CODATA} MeV")
print()

# =============================================================================
# THEORY PARAMETERS
# =============================================================================

print("THEORY PARAMETERS:")
print("-" * 40)

# Epoch
N_e = 111
print(f"N_e = {N_e}")

# Calculate φ^111 with high precision
phi_111 = phi**N_e
phi_minus_111 = phi**(-N_e)
print(f"φ^111 = {phi_111}")
print(f"φ^(-111) = {phi_minus_111}")
print()

# =============================================================================
# METHOD 1: CHECK GU_particle_masses.py VALUES
# =============================================================================

print("METHOD 1: Using GU_particle_masses.py exact values")
print("-" * 40)

# These values claim to give EXACT match
nu = mpf('0.8205439660164079')  # From the exact match
C_e = mpf('1.051366998674827')   # From the exact match

# Calculate using theory formula
m_e_theory1 = M_P_MeV * 2 * pi * C_e / phi_111

print(f"ν = {nu}")
print(f"C_e = {C_e}")
print(f"m_e = M_P × 2π × C_e / φ^111")
print(f"    = {m_e_theory1} MeV")
print(f"Error = {abs(m_e_theory1 - m_e_CODATA)} MeV")
print(f"Error % = {100 * abs(m_e_theory1 - m_e_CODATA) / m_e_CODATA}%")
print()

# =============================================================================
# METHOD 2: REVERSE ENGINEER EXACT C_e
# =============================================================================

print("METHOD 2: Reverse engineering exact C_e")
print("-" * 40)

# What C_e do we need for exact match?
C_e_exact = (m_e_CODATA * phi_111) / (M_P_MeV * 2 * pi)
print(f"Required C_e = {C_e_exact}")
print(f"             = {float(C_e_exact):.15f}")

# Verify it gives exact match
m_e_check = M_P_MeV * 2 * pi * C_e_exact / phi_111
print(f"Check: m_e = {m_e_check}")
print(f"Matches CODATA? {abs(m_e_check - m_e_CODATA) < mpf('1e-45')}")
print()

# =============================================================================
# METHOD 3: NLDE PARAMETERS WITH HIGH PRECISION
# =============================================================================

print("METHOD 3: NLDE approach with high precision")
print("-" * 40)

# Current NLDE parameters (need more precision!)
m_bar_star = mpf('4514')  # Needs verification
E_tilde = mpf('-0.882')   # Needs more decimals!

print(f"m̄★ = {m_bar_star}")
print(f"Ẽ = {E_tilde}")
print(f"(1 + Ẽ) = {1 + E_tilde}")

# What X_e gives exact match?
# m_e = m̄★ × X_e × M_P × (1 + Ẽ)
X_e_needed = m_e_CODATA / (m_bar_star * M_P_MeV * (1 + E_tilde))
print(f"X_e needed = {X_e_needed}")
print(f"           = {float(X_e_needed):.6e}")

# Compare to claimed X_e
X_e_claimed = mpf('7.85e-26')
print(f"X_e claimed = {X_e_claimed}")
print(f"Ratio = {X_e_needed / X_e_claimed}")
print()

# =============================================================================
# METHOD 4: CHECK SELF-CONSISTENCY
# =============================================================================

print("METHOD 4: Self-consistency check")
print("-" * 40)

# From derive_Xe_corrected.py formula:
# X_e = (2π C_e) / [m̄★ × (1 + Ẽ) × φ^{111}]

X_e_derived = (2 * pi * C_e_exact) / (m_bar_star * (1 + E_tilde) * phi_111)
print(f"X_e (derived) = {X_e_derived}")
print(f"              = {float(X_e_derived):.6e}")

# Check if this is consistent
m_e_final = m_bar_star * X_e_derived * M_P_MeV * (1 + E_tilde)
print(f"Final m_e = {m_e_final}")
print(f"Error = {abs(m_e_final - m_e_CODATA)} MeV")
print(f"Error % = {100 * abs(m_e_final - m_e_CODATA) / m_e_CODATA}%")
print()

# =============================================================================
# INVESTIGATION: WHERE'S THE ERROR?
# =============================================================================

print("="*80)
print("INVESTIGATION: SOURCE OF 0.17% ERROR")
print("="*80)
print()

# Check each component's precision
print("Component precision analysis:")
print("-" * 40)

# 1. Check if m̄★ = 4514 is exact
print("1. m̄★ precision:")
print(f"   Current: {m_bar_star}")
print(f"   Integer? {m_bar_star == int(m_bar_star)}")

# 2. Check Ẽ precision
print("\n2. Ẽ precision:")
print(f"   Current: {E_tilde} (only 3 decimals!)")
print(f"   This could be the issue - need more decimals from NLDE solver")

# 3. Check if we're missing QED corrections
alpha = mpf('0.0072973525693')  # Fine structure constant
eta_QED = 1 - alpha / (2 * pi)
print(f"\n3. QED corrections:")
print(f"   α = {alpha}")
print(f"   η_QED = {eta_QED}")
print(f"   Could multiply by η_QED? {m_e_theory1 * eta_QED}")

# 4. Check for missing factors
print(f"\n4. Possible missing factors:")
print(f"   Current formula: m_e = M_P × 2π C_e / φ^111")
print(f"   Missing a √5/3 factor? {m_e_theory1 * sqrt(mpf('5')/mpf('3'))}")
print(f"   Missing a 2μ factor (μ=0.4192)? {m_e_theory1 * 2 * mpf('0.4192')}")

# =============================================================================
# SOLUTION FINDER
# =============================================================================

print("\n" + "="*80)
print("FINDING THE EXACT SOLUTION")
print("="*80)
print()

# What multiplicative factor do we need?
factor_needed = m_e_CODATA / m_e_theory1
print(f"Factor needed to match CODATA: {factor_needed}")
print(f"                              = {float(factor_needed):.10f}")
print()

# Is this factor close to any known constants?
print("Is this factor close to:")
print(f"  1 - α/(2π) = {eta_QED} ? Ratio = {factor_needed / eta_QED}")
print(f"  1 - α/π = {1 - alpha/pi} ? Ratio = {factor_needed / (1 - alpha/pi)}")
print(f"  cos(π/111) = {cos(pi/111)} ? Ratio = {factor_needed / cos(pi/111)}")
print(f"  sin(π/111) = {sin(pi/111)} ? Ratio = {factor_needed / sin(pi/111)}")
print(f"  111×sin(π/111)/π = {111*sin(pi/111)/pi} ? Ratio = {factor_needed / (111*sin(pi/111)/pi)}")

# =============================================================================
# CONCLUSION
# =============================================================================

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)
print()

print("The 0.17% error is likely due to:")
print("1. Ẽ = -0.882 having insufficient precision (only 3 decimals)")
print("2. Possible missing QED correction factor")
print("3. The NLDE solver may need higher precision")
print()
print("To get EXACT CODATA match, we need ONE of:")
print(f"  • C_e = {C_e_exact:.15f}")
print(f"  • Ẽ more precise than -0.882")
print(f"  • Additional factor of {factor_needed:.10f}")
print()
print("RECOMMENDATION: Re-run NLDE solver with 50 decimal precision")
print("to get precise Ẽ value, which should close the gap.")