#!/usr/bin/env python3
"""
DEBUG: Why does Particles v2 formula give different result?
Document claims C_e = 1.64894 gives m_e = 0.51100 MeV (perfect!)
But my calculation gives 0.80238 MeV (57% error)
Let's trace through EXACTLY what the document shows
"""

from mpmath import mp, mpf, sqrt, sin, pi as mp_pi

mp.dps = 50

print("="*80)
print("DEBUG: PARTICLES V2 ELECTRON CALCULATION")
print("="*80)

# From document lines 329-330
M_P = mpf('1.220910e+22')  # Document uses this value
N_e = 111
C_e = mpf('1.64894')

# Epoch constant
phi = (1 + sqrt(5)) / 2
pi_111 = N_e * sin(mp_pi / N_e)
phi_111 = phi

print(f"\n### FROM DOCUMENT (Lines 329-331):")
print(f"M_P c² ≈ {M_P} MeV")
print(f"N_e = {N_e}")
print(f"C_e(n=111) ≈ {C_e}")
print(f"2π_111 ≈ {2*pi_111}")
print(f"φ_111^111 ≈ ? × 10²³")

# Calculate φ^111
phi_111_pow = phi ** N_e
print(f"\nφ_111^111 (calculated) = {phi_111_pow}")
print(f"φ_111^111 (scientific) = {float(phi_111_pow):.6e}")

# Document shows: φ_111^111 ≈ 2.15579 × 10²³
phi_doc = mpf('2.15579e23')
print(f"φ_111^111 (from doc) ≈ {phi_doc}")

# Check which one is correct
print(f"\nMy calculation: {phi_111_pow}")
print(f"Document value: {phi_doc}")
print(f"Ratio: {phi_111_pow / phi_doc}")

# Now calculate m_e both ways
print(f"\n### CALCULATION WITH MY φ^111:")
numerator_my = 2 * pi_111 * C_e
print(f"Numerator: 2π_111 · C_e = {numerator_my}")
m_e_my = M_P * numerator_my / phi_111_pow
print(f"m_e = M_P · (numerator / φ^111) = {m_e_my} MeV")

print(f"\n### CALCULATION WITH DOCUMENT φ^111:")
m_e_doc = M_P * numerator_my / phi_doc
print(f"m_e = M_P · (numerator / φ^111) = {m_e_doc} MeV")

# Check intermediate values from document
print(f"\n### DOCUMENT INTERMEDIATE VALUES (Line 331):")
print(f"Numerator = 2π_111 · 1.64894 ≈ 10.360 (doc)")
print(f"Numerator (calculated) = {numerator_my}")
print(f"Match: {'✅' if abs(numerator_my - 10.360) < 0.001 else '❌'}")

# The document shows: (10.360 / 2.15579×10²³)
intermediate = numerator_my / phi_doc
print(f"\nIntermediate: numerator / φ^111 = {intermediate}")
print(f"Document shows: 4.805×10⁻²³")
print(f"Match: {'✅' if abs(intermediate - mpf('4.805e-23')) < mpf('1e-25') else '❌'}")

# Final calculation
final = M_P * intermediate
print(f"\nFinal: M_P · intermediate = {final} MeV")
print(f"Document claims: 0.51100 MeV")
print(f"CODATA: 0.51099895 MeV")

# AHA! Check if maybe M_P value in document is different
print(f"\n### CHECKING M_P VALUE:")
print(f"I'm using: M_P = {M_P} MeV")
print(f"Standard: M_P = 1.22091×10²² MeV")

# What M_P would give the right answer with their values?
m_e_target = mpf('0.51099895')
M_P_needed = m_e_target / intermediate
print(f"\nM_P needed for correct result: {M_P_needed} MeV")
print(f"M_P needed (scientific): {float(M_P_needed):.6e} MeV")

print("\n" + "="*80)
print("CONCLUSION: Need to find which φ^111 value gives correct result!")
print("="*80)
