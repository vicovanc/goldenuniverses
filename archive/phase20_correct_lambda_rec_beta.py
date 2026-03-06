#!/usr/bin/env python3
"""
Golden Universe Theory - Phase 20: CORRECT λ_rec/β from Theory Documents
=========================================================================

CRITICAL DISCOVERY from "GU Couplings and Particles.md" line 5825:

The theory EXPLICITLY states:
  λ_rec/β = e^φ / π² = 0.51097951228960997824303381840723004398203106664718

This is VERY DIFFERENT from our dimensional guess:
  π·e/√φ = 6.714...

Let's test which one is correct!

Also found (line 3808):
  Memory quartic integral uses Beta/Gamma functions
  ∫|ψ_0|^4 ds = κ · (1/√π) · (Γ(a+1/2)/Γ(a))² · Γ(2a)/Γ(2a+1/2)
  where ψ_0(s) = N_0 · sech^a(κs)
  and a = g_e·v/κ (Pöschl-Teller index)

This suggests 'a' is the generation parameter, not our elliptic ν!
"""

from mpmath import mp, mpf, sqrt, pi, e, ellipk, ellipe, exp, gamma
import json

mp.dps = 50

print("=" * 80)
print("PHASE 20: CORRECT λ_rec/β FROM THEORY DOCUMENTS")
print("=" * 80)
print()

φ_mp = (1 + sqrt(5)) / 2
M_P_MeV = mpf('1.22091e+22')
α = mpf('1') / mpf('137.035999177')
η_QED = 1 - α / (2 * pi)

m_e_exp = mpf('0.51099895069')
m_μ_exp = mpf('105.6583755')
m_τ_exp = mpf('1776.86')

print("THEORY DOCUMENT SAYS (line 5825):")
print()

# From theory documents
lambda_rec_over_beta_theory = exp(φ_mp) / (pi ** 2)

print(f"  λ_rec/β = e^φ / π² = {lambda_rec_over_beta_theory}")
print(f"  Value: {float(lambda_rec_over_beta_theory):.6f}")
print()

# Our previous guess
lambda_rec_over_beta_old = (pi * e) / sqrt(φ_mp)

print("OUR PREVIOUS GUESS:")
print(f"  λ_rec/β = π·e/√φ = {lambda_rec_over_beta_old}")
print(f"  Value: {float(lambda_rec_over_beta_old):.6f}")
print()

print(f"RATIO: theory/guess = {float(lambda_rec_over_beta_theory / lambda_rec_over_beta_old):.6f}")
print()

# Winding numbers (from Phase 17)
N_e, p_e, q_e = 111, -41, 70
N_μ, p_μ, q_μ = 100, -37, 63
N_τ, p_τ, q_τ = 94, -37, 57

def calculate_mass_with_lambda(N, p, q, lambda_rec_over_beta):
    """Calculate mass with given λ_rec/β"""
    k_res = N / (φ_mp ** 2)
    k_nearest = round(float(k_res))
    δ = k_res - k_nearest
    y = abs(q + p * φ_mp)
    
    ν = mpf('1')/2 + (δ / (2 * k_res))
    
    K_ν = ellipk(ν)
    E_ν = ellipe(ν)
    g_δ = 1 + δ / pi
    f_geom = g_δ / y
    
    C = lambda_rec_over_beta * (K_ν - E_ν) * f_geom
    geom_supp = (2 * pi) / (φ_mp ** N)
    m = M_P_MeV * geom_supp * C * η_QED
    
    return m, float(C)

# ============================================================================
# TEST ELECTRON with BOTH VALUES
# ============================================================================

print("=" * 80)
print("ELECTRON: Test both λ_rec/β values")
print("=" * 80)
print()

m_e_old, C_e_old = calculate_mass_with_lambda(N_e, p_e, q_e, lambda_rec_over_beta_old)
error_e_old = ((m_e_old - m_e_exp) / m_e_exp) * 100

m_e_theory, C_e_theory = calculate_mass_with_lambda(N_e, p_e, q_e, lambda_rec_over_beta_theory)
error_e_theory = ((m_e_theory - m_e_exp) / m_e_exp) * 100

print(f"With λ_rec/β = π·e/√φ (OUR GUESS):")
print(f"  m_e = {float(m_e_old):.6f} MeV")
print(f"  Error = {float(error_e_old):+.2f}%")
print()

print(f"With λ_rec/β = e^φ/π² (THEORY DOCUMENT):")
print(f"  m_e = {float(m_e_theory):.6f} MeV")
print(f"  Error = {float(error_e_theory):+.2f}%")
print()

if abs(error_e_theory) < abs(error_e_old):
    print("  ✅ THEORY VALUE IS BETTER!")
else:
    print("  ⚠️ OUR GUESS WAS BETTER!")
print()

# ============================================================================
# TEST MUON with BOTH VALUES
# ============================================================================

print("=" * 80)
print("MUON: Test both λ_rec/β values")
print("=" * 80)
print()

m_μ_old, C_μ_old = calculate_mass_with_lambda(N_μ, p_μ, q_μ, lambda_rec_over_beta_old)
error_μ_old = ((m_μ_old - m_μ_exp) / m_μ_exp) * 100

m_μ_theory, C_μ_theory = calculate_mass_with_lambda(N_μ, p_μ, q_μ, lambda_rec_over_beta_theory)
error_μ_theory = ((m_μ_theory - m_μ_exp) / m_μ_exp) * 100

print(f"With λ_rec/β = π·e/√φ (OUR GUESS):")
print(f"  m_μ = {float(m_μ_old):.6f} MeV")
print(f"  Error = {float(error_μ_old):+.2f}%")
print()

print(f"With λ_rec/β = e^φ/π² (THEORY DOCUMENT):")
print(f"  m_μ = {float(m_μ_theory):.6f} MeV")
print(f"  Error = {float(error_μ_theory):+.2f}%")
print()

if abs(error_μ_theory) < abs(error_μ_old):
    print("  ✅ THEORY VALUE IS BETTER!")
    improvement = abs(error_μ_old) - abs(error_μ_theory)
    print(f"  Improvement: {float(improvement):.2f} percentage points!")
else:
    print("  ⚠️ OUR GUESS WAS BETTER!")
print()

# ============================================================================
# TEST TAU with BOTH VALUES
# ============================================================================

print("=" * 80)
print("TAU: Test both λ_rec/β values")
print("=" * 80)
print()

m_τ_old, C_τ_old = calculate_mass_with_lambda(N_τ, p_τ, q_τ, lambda_rec_over_beta_old)
error_τ_old = ((m_τ_old - m_τ_exp) / m_τ_exp) * 100

m_τ_theory, C_τ_theory = calculate_mass_with_lambda(N_τ, p_τ, q_τ, lambda_rec_over_beta_theory)
error_τ_theory = ((m_τ_theory - m_τ_exp) / m_τ_exp) * 100

print(f"With λ_rec/β = π·e/√φ (OUR GUESS):")
print(f"  m_τ = {float(m_τ_old):.6f} MeV")
print(f"  Error = {float(error_τ_old):+.2f}%")
print()

print(f"With λ_rec/β = e^φ/π² (THEORY DOCUMENT):")
print(f"  m_τ = {float(m_τ_theory):.6f} MeV")
print(f"  Error = {float(error_τ_theory):+.2f}%")
print()

if abs(error_τ_theory) < abs(error_τ_old):
    print("  ✅ THEORY VALUE IS BETTER!")
    improvement = abs(error_τ_old) - abs(error_τ_theory)
    print(f"  Improvement: {float(improvement):.2f} percentage points!")
else:
    print("  ⚠️ OUR GUESS WAS BETTER!")
print()

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("=" * 80)
print("SUMMARY: COMPARING λ_rec/β VALUES")
print("=" * 80)
print()

print(f"{'Source':<20} {'Value':<15} {'e Error':<10} {'μ Error':<10} {'τ Error'}")
print("-" * 75)

print(f"{'π·e/√φ (guess)':<20} {float(lambda_rec_over_beta_old):<15.6f} " +
      f"{float(error_e_old):<10.2f} {float(error_μ_old):<10.2f} {float(error_τ_old):.2f}")

print(f"{'e^φ/π² (theory)':<20} {float(lambda_rec_over_beta_theory):<15.6f} " +
      f"{float(error_e_theory):<10.2f} {float(error_μ_theory):<10.2f} {float(error_τ_theory):.2f}")

print()

# Determine winner
errors_old = [abs(float(error_e_old)), abs(float(error_μ_old)), abs(float(error_τ_old))]
errors_theory = [abs(float(error_e_theory)), abs(float(error_μ_theory)), abs(float(error_τ_theory))]

avg_old = sum(errors_old) / len(errors_old)
avg_theory = sum(errors_theory) / len(errors_theory)

print("AVERAGE ABSOLUTE ERROR:")
print(f"  π·e/√φ (guess):  {avg_old:.2f}%")
print(f"  e^φ/π² (theory): {avg_theory:.2f}%")
print()

if avg_theory < avg_old:
    print("🎉 THEORY DOCUMENT VALUE IS CORRECT!")
    print(f"   Improvement: {avg_old - avg_theory:.2f} percentage points average!")
else:
    print("⚠️ OUR GUESS WAS ACTUALLY BETTER")
    print("   This suggests theory doc value might be for different context")

print()

# Check if theory value matches electron exactly
print("NOTE: Theory doc gives λ_rec/β = 0.51097951...")
print(f"      Electron mass (CODATA) = 0.51099895...")
print(f"      These are VERY close! (~0.004% difference)")
print(f"      This might be λ_rec/β in DIFFERENT units or context!")
print()

# Save results
output = {
    'lambda_rec_over_beta': {
        'from_theory_doc': float(lambda_rec_over_beta_theory),
        'our_guess': float(lambda_rec_over_beta_old),
        'ratio': float(lambda_rec_over_beta_theory / lambda_rec_over_beta_old)
    },
    'electron': {
        'with_theory': {
            'm_MeV': float(m_e_theory),
            'error_%': float(error_e_theory)
        },
        'with_guess': {
            'm_MeV': float(m_e_old),
            'error_%': float(error_e_old)
        }
    },
    'muon': {
        'with_theory': {
            'm_MeV': float(m_μ_theory),
            'error_%': float(error_μ_theory)
        },
        'with_guess': {
            'm_MeV': float(m_μ_old),
            'error_%': float(error_μ_old)
        }
    },
    'tau': {
        'with_theory': {
            'm_MeV': float(m_τ_theory),
            'error_%': float(error_τ_theory)
        },
        'with_guess': {
            'm_MeV': float(m_τ_old),
            'error_%': float(error_τ_old)
        }
    },
    'avg_error': {
        'with_theory': avg_theory,
        'with_guess': avg_old
    }
}

with open("/Users/Cristiana_1/Documents/Golden Universe/PHASE20_CORRECT_LAMBDA_REC_BETA.json", 'w') as f:
    json.dump(output, f, indent=2)

print("Results saved to: PHASE20_CORRECT_LAMBDA_REC_BETA.json")
print()
print("=" * 80)
print("PHASE 20 COMPLETE")
print("=" * 80)
