#!/usr/bin/env python3
"""
Golden Universe Theory - Phase 14C: Verify Generation Jumps
============================================================

From "GU next in line.md":
- ΔN_μ = 11 (electron → muon)
- ΔN_τ = 17 (electron → tau, or muon → tau?)

TEST SPECIFIC EPOCHS:
1. Electron: N_e = 111 ✓ (verified)
2. Muon: N_μ = 111 - 11 = 100
3. Tau: N_τ = 111 - 17 = 94 (direct from electron)
   OR: N_τ = 100 - ΔN = ? (from muon)

Universal scaling: m = M_P × (2π/φ^N) × C × η
"""

from mpmath import mp, mpf, sqrt, pi, e, ellipk, ellipe
import json

mp.dps = 50

print("=" * 80)
print("PHASE 14C: VERIFY GENERATION JUMPS")
print("=" * 80)
print()

φ = (1 + sqrt(5)) / 2
M_P_MeV = mpf('1.22091e+22')
α = mpf('1') / mpf('137.035999177')
η_QED = 1 - α / (2 * pi)
lambda_rec_over_beta_0 = (pi * e) / sqrt(φ)

m_e_exp = mpf('0.51099895069')
m_μ_exp = mpf('105.6583755')
m_τ_exp = mpf('1776.86')

print("From theory document:")
print("  ΔN_μ = 11 (generation 1 → 2)")
print("  ΔN_τ = 17 (generation 1 → 3, or 2 → 3?)")
print()

def find_optimal_winding_systematic(N, k_res):
    """Systematic search for winding numbers"""
    p_center = -(k_res - 1)
    best_w = None
    best_y = float('inf')
    
    for p in range(p_center - 5, p_center + 6):
        q_optimal = -int(p * φ)
        for q_offset in range(-10, 11):
            q = q_optimal + q_offset
            y = abs(q + p * φ)
            if 0.1 < y < best_y:
                best_y = y
                best_w = (p, q)
    
    return best_w

def calculate_mass(N, w_c):
    """Calculate mass from epoch N and winding numbers"""
    p, q = w_c
    k_res = N / (φ ** 2)
    k_nearest = round(float(k_res))
    δ = k_res - k_nearest
    y = abs(q + p * φ)
    ν = mpf('1')/2 + (δ / (2 * k_res))
    
    K_ν = ellipk(ν)
    E_ν = ellipe(ν)
    g_δ = 1 + δ / pi
    f_geom = g_δ / y
    C = lambda_rec_over_beta_0 * (K_ν - E_ν) * f_geom
    geom_supp = (2 * pi) / (φ ** N)
    m = M_P_MeV * geom_supp * C * η_QED
    
    return m, C, float(k_res), float(δ), float(y)

# ============================================================================
# TEST SPECIFIC EPOCHS
# ============================================================================

print("=" * 80)
print("TEST 1: Electron at N=111 (baseline)")
print("=" * 80)
print()

N_e = 111
w_e = (-41, 70)
k_e = N_e / (φ ** 2)
print(f"Electron: N_e = {N_e}")
print(f"  k_e = N_e/φ² = {float(k_e):.4f} (≈ 42)")
print(f"  w_e = {w_e}")

m_e_theory, C_e, k_res_e, δ_e, y_e = calculate_mass(N_e, w_e)
error_e = ((m_e_theory - m_e_exp) / m_e_exp) * 100
print(f"  m_e (theory) = {float(m_e_theory):.6f} MeV")
print(f"  m_e (exp)    = {float(m_e_exp):.6f} MeV")
print(f"  Error        = {float(error_e):+.2f}% ✓")
print()

# ============================================================================
# TEST 2: Muon at N=100 (N_e - 11)
# ============================================================================

print("=" * 80)
print("TEST 2: Muon at N=100 (N_e - ΔN_μ = 111 - 11)")
print("=" * 80)
print()

N_μ_test = N_e - 11  # = 100
k_μ = N_μ_test / (φ ** 2)
k_μ_nearest = round(float(k_μ))
print(f"Muon test: N_μ = {N_μ_test}")
print(f"  k_μ = N_μ/φ² = {float(k_μ):.4f} (nearest = {k_μ_nearest})")

# Find winding numbers
w_μ_test = find_optimal_winding_systematic(N_μ_test, k_μ_nearest)
print(f"  w_μ = {w_μ_test}")

m_μ_theory, C_μ, k_res_μ, δ_μ, y_μ = calculate_mass(N_μ_test, w_μ_test)
error_μ = ((m_μ_theory - m_μ_exp) / m_μ_exp) * 100
print(f"  m_μ (theory) = {float(m_μ_theory):.6f} MeV")
print(f"  m_μ (exp)    = {float(m_μ_exp):.6f} MeV")
print(f"  Error        = {float(error_μ):+.2f}%")
print()

# Check mass ratio
mass_ratio_theory = m_μ_theory / m_e_theory
mass_ratio_exp = m_μ_exp / m_e_exp
phi_11 = φ ** 11
print(f"Mass ratio check:")
print(f"  m_μ/m_e (theory) = {float(mass_ratio_theory):.2f}")
print(f"  m_μ/m_e (exp)    = {float(mass_ratio_exp):.2f}")
print(f"  φ^11             = {float(phi_11):.2f}")
print(f"  Ratio match?     = {abs(mass_ratio_theory - phi_11) / phi_11 * 100:.1f}% deviation from φ^11")
print()

# ============================================================================
# TEST 3: Tau at N=94 (N_e - 17)
# ============================================================================

print("=" * 80)
print("TEST 3: Tau at N=94 (N_e - ΔN_τ = 111 - 17)")
print("=" * 80)
print()

N_τ_test = N_e - 17  # = 94
k_τ = N_τ_test / (φ ** 2)
k_τ_nearest = round(float(k_τ))
print(f"Tau test: N_τ = {N_τ_test}")
print(f"  k_τ = N_τ/φ² = {float(k_τ):.4f} (nearest = {k_τ_nearest})")

# Find winding numbers
w_τ_test = find_optimal_winding_systematic(N_τ_test, k_τ_nearest)
print(f"  w_τ = {w_τ_test}")

m_τ_theory, C_τ, k_res_τ, δ_τ, y_τ = calculate_mass(N_τ_test, w_τ_test)
error_τ = ((m_τ_theory - m_τ_exp) / m_τ_exp) * 100
print(f"  m_τ (theory) = {float(m_τ_theory):.6f} MeV")
print(f"  m_τ (exp)    = {float(m_τ_exp):.6f} MeV")
print(f"  Error        = {float(error_τ):+.2f}%")
print()

# Check mass ratio
mass_ratio_τ_e_theory = m_τ_theory / m_e_theory
mass_ratio_τ_e_exp = m_τ_exp / m_e_exp
phi_17 = φ ** 17
print(f"Mass ratio check (τ/e):")
print(f"  m_τ/m_e (theory) = {float(mass_ratio_τ_e_theory):.2f}")
print(f"  m_τ/m_e (exp)    = {float(mass_ratio_τ_e_exp):.2f}")
print(f"  φ^17             = {float(phi_17):.2f}")
print(f"  Ratio match?     = {abs(mass_ratio_τ_e_theory - phi_17) / phi_17 * 100:.1f}% deviation from φ^17")
print()

mass_ratio_τ_μ_theory = m_τ_theory / m_μ_theory
mass_ratio_τ_μ_exp = m_τ_exp / m_μ_exp
phi_6 = φ ** 6  # If tau is from muon with ΔN = 6
print(f"Mass ratio check (τ/μ):")
print(f"  m_τ/m_μ (theory) = {float(mass_ratio_τ_μ_theory):.2f}")
print(f"  m_τ/m_μ (exp)    = {float(mass_ratio_τ_μ_exp):.2f}")
print(f"  φ^6              = {float(phi_6):.2f} (if ΔN_τμ = 6)")
print()

# ============================================================================
# ALTERNATIVE: What if ΔN_τ = 17 is from muon, not electron?
# ============================================================================

print("=" * 80)
print("ALTERNATIVE: Tau from muon with ΔN = 17?")
print("=" * 80)
print()

N_τ_alt = N_μ_test - 17  # = 100 - 17 = 83
print(f"If τ is from μ with ΔN=17: N_τ = {N_τ_alt}")

k_τ_alt = N_τ_alt / (φ ** 2)
k_τ_alt_nearest = round(float(k_τ_alt))
print(f"  k_τ = {float(k_τ_alt):.4f} (nearest = {k_τ_alt_nearest})")

w_τ_alt = find_optimal_winding_systematic(N_τ_alt, k_τ_alt_nearest)
print(f"  w_τ = {w_τ_alt}")

m_τ_alt, C_τ_alt, k_res_τ_alt, δ_τ_alt, y_τ_alt = calculate_mass(N_τ_alt, w_τ_alt)
error_τ_alt = ((m_τ_alt - m_τ_exp) / m_τ_exp) * 100
print(f"  m_τ (theory) = {float(m_τ_alt):.6f} MeV")
print(f"  m_τ (exp)    = {float(m_τ_exp):.6f} MeV")
print(f"  Error        = {float(error_τ_alt):+.2f}%")
print()

# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 80)
print("SUMMARY: GENERATION STRUCTURE")
print("=" * 80)
print()

results = [
    ("Electron", N_e, w_e, float(m_e_theory), float(m_e_exp), float(error_e)),
    ("Muon (N=100)", N_μ_test, w_μ_test, float(m_μ_theory), float(m_μ_exp), float(error_μ)),
    ("Tau (N=94)", N_τ_test, w_τ_test, float(m_τ_theory), float(m_τ_exp), float(error_τ)),
    ("Tau alt (N=83)", N_τ_alt, w_τ_alt, float(m_τ_alt), float(m_τ_exp), float(error_τ_alt)),
]

print(f"{'Particle':<20} {'N':<5} {'w_c':<20} {'m_theory (MeV)':<18} {'m_exp (MeV)':<15} {'Error':<10}")
print("-" * 100)

for name, N, w_c, m_th, m_ex, err in results:
    w_str = f"({w_c[0]}, {w_c[1]})"
    print(f"{name:<20} {N:<5} {w_str:<20} {m_th:<18.4f} {m_ex:<15.4f} {err:+.2f}%")

print()
print("CONCLUSION:")
if abs(error_μ) < 5:
    print(f"  ✅ Muon: N=100 works well (error={float(error_μ):.1f}%)")
else:
    print(f"  ❌ Muon: N=100 has large error ({float(error_μ):.1f}%)")

if abs(error_τ) < abs(error_τ_alt):
    print(f"  ✅ Tau: N=94 is better (error={float(error_τ):.1f}% vs {float(error_τ_alt):.1f}%)")
else:
    print(f"  ✅ Tau: N=83 is better (error={float(error_τ_alt):.1f}% vs {float(error_τ):.1f}%)")

print()

# Save results
output = {
    'generation_jumps': {'ΔN_μ': 11, 'ΔN_τ': 17},
    'electron': {'N': N_e, 'w_c': list(w_e), 'm_theory': float(m_e_theory), 'error_%': float(error_e)},
    'muon': {'N': N_μ_test, 'w_c': list(w_μ_test), 'm_theory': float(m_μ_theory), 'error_%': float(error_μ)},
    'tau_option1': {'N': N_τ_test, 'w_c': list(w_τ_test), 'm_theory': float(m_τ_theory), 'error_%': float(error_τ)},
    'tau_option2': {'N': N_τ_alt, 'w_c': list(w_τ_alt), 'm_theory': float(m_τ_alt), 'error_%': float(error_τ_alt)},
}

with open("/Users/Cristiana_1/Documents/Golden Universe/PHASE14C_GENERATION_JUMPS.json", 'w') as f:
    json.dump(output, f, indent=2)

print("Results saved to: PHASE14C_GENERATION_JUMPS.json")
print()
print("=" * 80)
print("PHASE 14C COMPLETE")
print("=" * 80)
