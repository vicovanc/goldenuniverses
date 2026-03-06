#!/usr/bin/env python3
"""
Golden Universe Theory - Phase 18: Generation Normalization Factors
====================================================================

CRITICAL DISCOVERY from "GU next in line.md" lines 1268-1278:

The theory has GENERATION-DEPENDENT normalization factors from kink modes:

  ν_e = 1       → electron (base)
  ν_μ = 3/2     → muon (first excitation)
  ν_τ = 2       → tau (second excitation)

Exact normalization ratios from Beta/Gamma integrals:
  g_μ/g_e = π/4
  g_τ/g_e = 2/3

CORRECTED MASS FORMULA:
  m_e = M_P · (2π/φ^N_e) · C_e · η
  m_μ = M_P · (2π/φ^N_μ) · C_μ · η  where C_μ = C_e · (π/4)
  m_τ = M_P · (2π/φ^N_τ) · C_τ · η  where C_τ = C_e · (2/3)

Let's recalculate!
"""

from mpmath import mp, mpf, sqrt, pi, e, ellipk, ellipe
import json

mp.dps = 50

print("=" * 80)
print("PHASE 18: GENERATION NORMALIZATION FACTORS")
print("=" * 80)
print()

φ_mp = (1 + sqrt(5)) / 2
M_P_MeV = mpf('1.22091e+22')
α = mpf('1') / mpf('137.035999177')
η_QED = 1 - α / (2 * pi)
lambda_rec_over_beta_0 = (pi * e) / sqrt(φ_mp)

m_e_exp = mpf('0.51099895069')
m_μ_exp = mpf('105.6583755')
m_τ_exp = mpf('1776.86')

print("GENERATION FACTORS from kink-mode normalization:")
print(f"  g_μ/g_e = π/4 = {pi/4}")
print(f"  g_τ/g_e = 2/3 = {mpf(2)/3}")
print()

# Generation factors
g_ratio_μ = pi / 4
g_ratio_τ = mpf(2) / 3

print(f"  g_μ/g_e = {float(g_ratio_μ):.6f}")
print(f"  g_τ/g_e = {float(g_ratio_τ):.6f}")
print()

# ============================================================================
# WINDING NUMBERS (from Phase 17 variational minimization)
# ============================================================================

print("Using winding numbers from variational minimization (Phase 17):")
print()

# Electron
N_e = 111
p_e, q_e = -41, 70
print(f"Electron: N={N_e}, (p,q)=({p_e},{q_e})")

# Muon  
N_μ = 100
p_μ, q_μ = -37, 63
print(f"Muon:     N={N_μ}, (p,q)=({p_μ},{q_μ})")

# Tau
N_τ = 94
p_τ, q_τ = -37, 57
print(f"Tau:      N={N_τ}, (p,q)=({p_τ},{q_τ})")
print()

# ============================================================================
# CALCULATE BASE C_e for ELECTRON
# ============================================================================

print("=" * 80)
print("ELECTRON: Calculate base C_e")
print("=" * 80)
print()

k_res_e = N_e / (φ_mp ** 2)
k_nearest_e = round(float(k_res_e))
δ_e = k_res_e - k_nearest_e
y_e = abs(q_e + p_e * φ_mp)
ν_e = mpf('1')/2 + (δ_e / (2 * k_res_e))

K_ν_e = ellipk(ν_e)
E_ν_e = ellipe(ν_e)
g_δ_e = 1 + δ_e / pi
f_geom_e = g_δ_e / y_e

C_e_base = lambda_rec_over_beta_0 * (K_ν_e - E_ν_e) * f_geom_e

geom_supp_e = (2 * pi) / (φ_mp ** N_e)
m_e_theory = M_P_MeV * geom_supp_e * C_e_base * η_QED

error_e = ((m_e_theory - m_e_exp) / m_e_exp) * 100

print(f"C_e (base) = {float(C_e_base):.6f}")
print(f"m_e (theory) = {float(m_e_theory):.6f} MeV")
print(f"m_e (exp)    = {float(m_e_exp):.6f} MeV")
print(f"Error = {float(error_e):+.2f}%")
print()

# ============================================================================
# MUON with GENERATION FACTOR
# ============================================================================

print("=" * 80)
print("MUON: Calculate with generation factor g_μ/g_e = π/4")
print("=" * 80)
print()

k_res_μ = N_μ / (φ_mp ** 2)
k_nearest_μ = round(float(k_res_μ))
δ_μ = k_res_μ - k_nearest_μ
y_μ = abs(q_μ + p_μ * φ_mp)
ν_μ = mpf('1')/2 + (δ_μ / (2 * k_res_μ))

K_ν_μ = ellipk(ν_μ)
E_ν_μ = ellipe(ν_μ)
g_δ_μ = 1 + δ_μ / pi
f_geom_μ = g_δ_μ / y_μ

# Calculate C_μ from geometry (like C_e)
C_μ_geometric = lambda_rec_over_beta_0 * (K_ν_μ - E_ν_μ) * f_geom_μ

print(f"WITHOUT generation factor:")
print(f"  C_μ (geometric) = {float(C_μ_geometric):.6f}")

geom_supp_μ = (2 * pi) / (φ_mp ** N_μ)
m_μ_no_factor = M_P_MeV * geom_supp_μ * C_μ_geometric * η_QED
error_μ_no_factor = ((m_μ_no_factor - m_μ_exp) / m_μ_exp) * 100

print(f"  m_μ (theory) = {float(m_μ_no_factor):.6f} MeV")
print(f"  Error = {float(error_μ_no_factor):+.2f}%")
print()

# WITH generation factor
C_μ_corrected = C_μ_geometric * g_ratio_μ

print(f"WITH generation factor g_μ/g_e = π/4:")
print(f"  C_μ (corrected) = C_μ(geometric) · (π/4) = {float(C_μ_corrected):.6f}")

m_μ_corrected = M_P_MeV * geom_supp_μ * C_μ_corrected * η_QED
error_μ_corrected = ((m_μ_corrected - m_μ_exp) / m_μ_exp) * 100

print(f"  m_μ (theory) = {float(m_μ_corrected):.6f} MeV")
print(f"  m_μ (exp)    = {float(m_μ_exp):.6f} MeV")
print(f"  Error = {float(error_μ_corrected):+.2f}%")
print()

improvement_μ = abs(error_μ_no_factor) - abs(error_μ_corrected)
if improvement_μ > 0:
    print(f"  ✅ Improvement: {float(improvement_μ):.2f} percentage points better!")
else:
    print(f"  ❌ Worse by: {float(-improvement_μ):.2f} percentage points")
print()

# ============================================================================
# TAU with GENERATION FACTOR
# ============================================================================

print("=" * 80)
print("TAU: Calculate with generation factor g_τ/g_e = 2/3")
print("=" * 80)
print()

k_res_τ = N_τ / (φ_mp ** 2)
k_nearest_τ = round(float(k_res_τ))
δ_τ = k_res_τ - k_nearest_τ
y_τ = abs(q_τ + p_τ * φ_mp)
ν_τ = mpf('1')/2 + (δ_τ / (2 * k_res_τ))

K_ν_τ = ellipk(ν_τ)
E_ν_τ = ellipe(ν_τ)
g_δ_τ = 1 + δ_τ / pi
f_geom_τ = g_δ_τ / y_τ

C_τ_geometric = lambda_rec_over_beta_0 * (K_ν_τ - E_ν_τ) * f_geom_τ

print(f"WITHOUT generation factor:")
print(f"  C_τ (geometric) = {float(C_τ_geometric):.6f}")

geom_supp_τ = (2 * pi) / (φ_mp ** N_τ)
m_τ_no_factor = M_P_MeV * geom_supp_τ * C_τ_geometric * η_QED
error_τ_no_factor = ((m_τ_no_factor - m_τ_exp) / m_τ_exp) * 100

print(f"  m_τ (theory) = {float(m_τ_no_factor):.6f} MeV")
print(f"  Error = {float(error_τ_no_factor):+.2f}%")
print()

# WITH generation factor
C_τ_corrected = C_τ_geometric * g_ratio_τ

print(f"WITH generation factor g_τ/g_e = 2/3:")
print(f"  C_τ (corrected) = C_τ(geometric) · (2/3) = {float(C_τ_corrected):.6f}")

m_τ_corrected = M_P_MeV * geom_supp_τ * C_τ_corrected * η_QED
error_τ_corrected = ((m_τ_corrected - m_τ_exp) / m_τ_exp) * 100

print(f"  m_τ (theory) = {float(m_τ_corrected):.6f} MeV")
print(f"  m_τ (exp)    = {float(m_τ_exp):.6f} MeV")
print(f"  Error = {float(error_τ_corrected):+.2f}%")
print()

improvement_τ = abs(error_τ_no_factor) - abs(error_τ_corrected)
if improvement_τ > 0:
    print(f"  ✅ Improvement: {float(improvement_τ):.2f} percentage points better!")
else:
    print(f"  ❌ Worse by: {float(-improvement_τ):.2f} percentage points")
print()

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("=" * 80)
print("FINAL SUMMARY: COMPLETE LEPTON SECTOR WITH GENERATION FACTORS")
print("=" * 80)
print()

print(f"{'Particle':<10} {'N':<5} {'(p,q)':<15} {'g/g_e':<10} {'m_theory':<12} {'m_exp':<12} {'Error'}")
print("-" * 90)

print(f"{'Electron':<10} {N_e:<5} {str((p_e,q_e)):<15} {'1.000':<10} " +
      f"{float(m_e_theory):<12.4f} {float(m_e_exp):<12.4f} {float(error_e):+.2f}%")

print(f"{'Muon':<10} {N_μ:<5} {str((p_μ,q_μ)):<15} {'π/4':<10} " +
      f"{float(m_μ_corrected):<12.4f} {float(m_μ_exp):<12.4f} {float(error_μ_corrected):+.2f}%")

print(f"{'Tau':<10} {N_τ:<5} {str((p_τ,q_τ)):<15} {'2/3':<10} " +
      f"{float(m_τ_corrected):<12.4f} {float(m_τ_exp):<12.4f} {float(error_τ_corrected):+.2f}%")

print()

# Check mass ratios
ratio_μe_theory = m_μ_corrected / m_e_theory
ratio_μe_exp = m_μ_exp / m_e_exp
ratio_τe_theory = m_τ_corrected / m_e_theory
ratio_τe_exp = m_τ_exp / m_e_exp

print("Mass ratios:")
print(f"  m_μ/m_e (theory) = {float(ratio_μe_theory):.2f}")
print(f"  m_μ/m_e (exp)    = {float(ratio_μe_exp):.2f}")
print(f"  Error = {float(abs(ratio_μe_theory - ratio_μe_exp)/ratio_μe_exp * 100):.2f}%")
print()
print(f"  m_τ/m_e (theory) = {float(ratio_τe_theory):.2f}")
print(f"  m_τ/m_e (exp)    = {float(ratio_τe_exp):.2f}")
print(f"  Error = {float(abs(ratio_τe_theory - ratio_τe_exp)/ratio_τe_exp * 100):.2f}%")
print()

# Overall grade
errors = [abs(float(error_e)), abs(float(error_μ_corrected)), abs(float(error_τ_corrected))]
max_error = max(errors)
avg_error = sum(errors) / len(errors)

print("=" * 80)
print("THEORY GRADE:")
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
    'generation_factors': {
        'source': 'GU next in line.md lines 1268-1278 (kink-mode ν-ladder)',
        'g_mu_over_g_e': str(g_ratio_μ),
        'g_tau_over_g_e': str(g_ratio_τ)
    },
    'predictions_with_factors': {
        'electron': {
            'N': N_e,
            'winding': (p_e, q_e),
            'generation_factor': 1.0,
            'm_theory_MeV': float(m_e_theory),
            'error_%': float(error_e)
        },
        'muon': {
            'N': N_μ,
            'winding': (p_μ, q_μ),
            'generation_factor': float(g_ratio_μ),
            'm_theory_MeV': float(m_μ_corrected),
            'error_%': float(error_μ_corrected)
        },
        'tau': {
            'N': N_τ,
            'winding': (p_τ, q_τ),
            'generation_factor': float(g_ratio_τ),
            'm_theory_MeV': float(m_τ_corrected),
            'error_%': float(error_τ_corrected)
        }
    },
    'grade': grade,
    'max_error_%': max_error,
    'avg_error_%': avg_error
}

with open("/Users/Cristiana_1/Documents/Golden Universe/PHASE18_GENERATION_FACTORS.json", 'w') as f:
    json.dump(output, f, indent=2)

print("Results saved to: PHASE18_GENERATION_FACTORS.json")
print()
print("=" * 80)
print("PHASE 18 COMPLETE")
print("=" * 80)
