#!/usr/bin/env python3
"""
Golden Universe Theory - Phase 21: QED/EW Corrections for Muon and Tau
=======================================================================

From "More Particles Stuff GU.md" lines 747-748:

Mass ratios include QED/EW on-shell corrections:
  m_μ/m_e = [topology] · [running] · [(1 + Δ_μ^QED + Δ_μ^weak) / (1 + Δ_e^QED + Δ_e^weak)]
  
Standard QED corrections (Kinoshita, Cvitanović):
  Δ^QED = -α/π · [3/4 + log(m/m_e) for heavier leptons]
  
Electroweak corrections (Sirlin):
  Δ^weak ≈ α/(4π sin²θ_W) · log(M_Z/m) for m << M_Z
"""

from mpmath import mp, mpf, sqrt, pi, e, ellipk, ellipe, log as mplog
import json

mp.dps = 50

print("=" * 80)
print("PHASE 21: QED/EW CORRECTIONS FOR HEAVIER LEPTONS")
print("=" * 80)
print()

φ_mp = (1 + sqrt(5)) / 2
M_P_MeV = mpf('1.22091e+22')
α = mpf('1') / mpf('137.035999177')
lambda_rec_over_beta_0 = (pi * e) / sqrt(φ_mp)

m_e_exp = mpf('0.51099895069')
m_μ_exp = mpf('105.6583755')
m_τ_exp = mpf('1776.86')

M_Z = mpf('91187.6')  # MeV (Z boson mass)
sin2_theta_W = mpf('0.23122')  # Weinberg angle

print("QED/EW Parameters:")
print(f"  α = 1/137.036")
print(f"  M_Z = {float(M_Z):.1f} MeV")
print(f"  sin²θ_W = {float(sin2_theta_W):.5f}")
print()

# Winding numbers (from Phase 17)
N_e, p_e, q_e = 111, -41, 70
N_μ, p_μ, q_μ = 100, -37, 63
N_τ, p_τ, q_τ = 94, -37, 57

def calculate_QED_correction(m, m_ref):
    """
    QED self-energy + vacuum polarization correction
    
    For electron (reference): Δ_e^QED = -α/(2π)
    For heavier leptons: Additional log(m/m_e) terms
    
    Standard formula (Kinoshita):
      Δ^QED = -α/π · [3/4 + log(M/m)]
    where M is the heavy mass, m is the light mass
    """
    if m <= m_ref:
        # Electron: standard 1-loop
        return -α / (2 * pi)
    else:
        # Heavier leptons: includes large log
        delta_base = -α / pi
        mass_correction = mpf('3')/4 + mplog(m / m_ref)
        return delta_base * mass_correction

def calculate_EW_correction(m):
    """
    Electroweak correction (Sirlin formula)
    
    For m << M_Z:
      Δ^weak ≈ α/(4π·sin²θ_W) · log(M_Z²/m²)
    """
    delta_EW = (α / (4 * pi * sin2_theta_W)) * mplog((M_Z / m)**2)
    return delta_EW

def calculate_mass_with_corrections(N, p, q, apply_QED_EW=False):
    """Calculate mass with optional QED/EW corrections"""
    k_res = N / (φ_mp ** 2)
    k_nearest = round(float(k_res))
    δ = k_res - k_nearest
    y = abs(q + p * φ_mp)
    
    ν = mpf('1')/2 + (δ / (2 * k_res))
    
    K_ν = ellipk(ν)
    E_ν = ellipe(ν)
    g_δ = 1 + δ / pi
    f_geom = g_δ / y
    
    C = lambda_rec_over_beta_0 * (K_ν - E_ν) * f_geom
    geom_supp = (2 * pi) / (φ_mp ** N)
    
    if apply_QED_EW:
        # This is the "bare" mass before corrections
        # We apply corrections as m_phys = m_bare · (1 + Δ^QED + Δ^EW)
        η_QED = 1 - α / (2 * pi)  # Electron correction
        m_bare = M_P_MeV * geom_supp * C * η_QED
        return m_bare, float(C)
    else:
        # Original formula with simple QED
        η_QED = 1 - α / (2 * pi)
        m = M_P_MeV * geom_supp * C * η_QED
        return m, float(C)

# ============================================================================
# ELECTRON (Reference)
# ============================================================================

print("=" * 80)
print("ELECTRON (Reference)")
print("=" * 80)
print()

m_e_theory, C_e = calculate_mass_with_corrections(N_e, p_e, q_e)
Δ_e_QED = calculate_QED_correction(m_e_theory, m_e_theory)
Δ_e_EW = calculate_EW_correction(m_e_theory)

error_e = ((m_e_theory - m_e_exp) / m_e_exp) * 100

print(f"Bare mass: {float(m_e_theory):.6f} MeV")
print(f"Δ_e^QED: {float(Δ_e_QED):.6f}")
print(f"Δ_e^EW: {float(Δ_e_EW):.6f}")
print(f"Total correction: {float(Δ_e_QED + Δ_e_EW):.6f}")
print(f"Error: {float(error_e):+.2f}%")
print()

# ============================================================================
# MUON with QED/EW Corrections
# ============================================================================

print("=" * 80)
print("MUON: Apply Full QED/EW Corrections")
print("=" * 80)
print()

m_μ_bare, C_μ = calculate_mass_with_corrections(N_μ, p_μ, q_μ)

Δ_μ_QED = calculate_QED_correction(m_μ_bare, m_e_theory)
Δ_μ_EW = calculate_EW_correction(m_μ_bare)

# Apply corrections
m_μ_corrected = m_μ_bare * (1 + Δ_μ_QED + Δ_μ_EW)

error_μ_bare = ((m_μ_bare - m_μ_exp) / m_μ_exp) * 100
error_μ_corrected = ((m_μ_corrected - m_μ_exp) / m_μ_exp) * 100

print(f"Bare mass (before corrections): {float(m_μ_bare):.6f} MeV")
print(f"Δ_μ^QED: {float(Δ_μ_QED):.6f}")
print(f"Δ_μ^EW: {float(Δ_μ_EW):.6f}")
print(f"Total correction factor: {float(1 + Δ_μ_QED + Δ_μ_EW):.6f}")
print(f"Corrected mass: {float(m_μ_corrected):.6f} MeV")
print()
print(f"Error (bare): {float(error_μ_bare):+.2f}%")
print(f"Error (corrected): {float(error_μ_corrected):+.2f}%")
print()

improvement_μ = abs(error_μ_bare) - abs(error_μ_corrected)
if improvement_μ > 0:
    print(f"✅ IMPROVEMENT: {float(improvement_μ):.2f} percentage points!")
else:
    print(f"⚠️ Worse by: {float(-improvement_μ):.2f} percentage points")
print()

# ============================================================================
# TAU with QED/EW Corrections
# ============================================================================

print("=" * 80)
print("TAU: Apply Full QED/EW Corrections")
print("=" * 80)
print()

m_τ_bare, C_τ = calculate_mass_with_corrections(N_τ, p_τ, q_τ)

Δ_τ_QED = calculate_QED_correction(m_τ_bare, m_e_theory)
Δ_τ_EW = calculate_EW_correction(m_τ_bare)

# Apply corrections
m_τ_corrected = m_τ_bare * (1 + Δ_τ_QED + Δ_τ_EW)

error_τ_bare = ((m_τ_bare - m_τ_exp) / m_τ_exp) * 100
error_τ_corrected = ((m_τ_corrected - m_τ_exp) / m_τ_exp) * 100

print(f"Bare mass (before corrections): {float(m_τ_bare):.6f} MeV")
print(f"Δ_τ^QED: {float(Δ_τ_QED):.6f}")
print(f"Δ_τ^EW: {float(Δ_τ_EW):.6f}")
print(f"Total correction factor: {float(1 + Δ_τ_QED + Δ_τ_EW):.6f}")
print(f"Corrected mass: {float(m_τ_corrected):.6f} MeV")
print()
print(f"Error (bare): {float(error_τ_bare):+.2f}%")
print(f"Error (corrected): {float(error_τ_corrected):+.2f}%")
print()

improvement_τ = abs(error_τ_bare) - abs(error_τ_corrected)
if improvement_τ > 0:
    print(f"✅ IMPROVEMENT: {float(improvement_τ):.2f} percentage points!")
else:
    print(f"⚠️ Worse by: {float(-improvement_τ):.2f} percentage points")
print()

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("=" * 80)
print("SUMMARY: QED/EW CORRECTED MASSES")
print("=" * 80)
print()

print(f"{'Particle':<10} {'Bare (MeV)':<15} {'Corrected (MeV)':<15} {'Exp (MeV)':<15} {'Error'}")
print("-" * 75)

print(f"{'Electron':<10} {float(m_e_theory):<15.4f} {float(m_e_theory):<15.4f} " +
      f"{float(m_e_exp):<15.4f} {float(error_e):+.2f}%")

print(f"{'Muon':<10} {float(m_μ_bare):<15.4f} {float(m_μ_corrected):<15.4f} " +
      f"{float(m_μ_exp):<15.4f} {float(error_μ_corrected):+.2f}%")

print(f"{'Tau':<10} {float(m_τ_bare):<15.4f} {float(m_τ_corrected):<15.4f} " +
      f"{float(m_τ_exp):<15.4f} {float(error_τ_corrected):+.2f}%")

print()

# Calculate final grade
errors = [abs(float(error_e)), abs(float(error_μ_corrected)), abs(float(error_τ_corrected))]
max_error = max(errors)
avg_error = sum(errors) / len(errors)

print("THEORY PERFORMANCE:")
print(f"  Max error: {max_error:.2f}%")
print(f"  Avg error: {avg_error:.2f}%")

if max_error < 1:
    grade = "A++"
elif max_error < 5:
    grade = "A+"
elif max_error < 10:
    grade = "A"
elif max_error < 15:
    grade = "A-"
else:
    grade = "B+"

print(f"  Grade: {grade}")
print()

# Save results
output = {
    'QED_EW_parameters': {
        'alpha': float(α),
        'M_Z_MeV': float(M_Z),
        'sin2_theta_W': float(sin2_theta_W)
    },
    'electron': {
        'm_theory_MeV': float(m_e_theory),
        'Delta_QED': float(Δ_e_QED),
        'Delta_EW': float(Δ_e_EW),
        'error_%': float(error_e)
    },
    'muon': {
        'm_bare_MeV': float(m_μ_bare),
        'm_corrected_MeV': float(m_μ_corrected),
        'Delta_QED': float(Δ_μ_QED),
        'Delta_EW': float(Δ_μ_EW),
        'error_bare_%': float(error_μ_bare),
        'error_corrected_%': float(error_μ_corrected),
        'improvement': float(improvement_μ)
    },
    'tau': {
        'm_bare_MeV': float(m_τ_bare),
        'm_corrected_MeV': float(m_τ_corrected),
        'Delta_QED': float(Δ_τ_QED),
        'Delta_EW': float(Δ_τ_EW),
        'error_bare_%': float(error_τ_bare),
        'error_corrected_%': float(error_τ_corrected),
        'improvement': float(improvement_τ)
    },
    'grade': grade,
    'max_error_%': max_error,
    'avg_error_%': avg_error
}

with open("/Users/Cristiana_1/Documents/Golden Universe/PHASE21_QED_EW_CORRECTIONS.json", 'w') as f:
    json.dump(output, f, indent=2)

print("Results saved to: PHASE21_QED_EW_CORRECTIONS.json")
print()
print("=" * 80)
print("PHASE 21 COMPLETE")
print("=" * 80)
