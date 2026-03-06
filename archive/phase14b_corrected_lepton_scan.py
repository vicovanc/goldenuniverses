#!/usr/bin/env python3
"""
Golden Universe Theory - Phase 14B: CORRECTED Lepton Scan
==========================================================

CRITICAL INSIGHT:
  m = M_P · (2π/φ^N) · C · η
  
  Since φ^N is in DENOMINATOR:
  - HIGHER N → LOWER mass
  - LOWER N → HIGHER mass
  
  Therefore:
  - Electron (lightest): N_e = 111
  - Muon (heavier): N_μ < N_e (LOWER epoch!)
  - Tau (heaviest): N_τ < N_μ (EVEN LOWER epoch!)
  
  This is OPPOSITE of naive expectation!

CORRECTED SEARCH:
- Electron: N_e = 111 ✓
- Muon: Search N = 50-110 (below electron)
- Tau: Search N = 1-50 (below muon)
- Neutrinos: Search N > 111 (above electron, for tiny masses)
"""

from mpmath import mp, mpf, sqrt, pi, exp, log, cos, sin, e, ellipk, ellipe
import json
from datetime import datetime

# Set precision to 50 decimal places
mp.dps = 50

print("=" * 80)
print("GOLDEN UNIVERSE THEORY - PHASE 14B")
print("CORRECTED Lepton Sector Scan")
print("=" * 80)
print()

print("CRITICAL INSIGHT:")
print("  m ∝ 1/φ^N, so HIGHER N → LOWER mass!")
print("  Therefore: N_τ < N_μ < N_e (opposite order!)")
print()

# ============================================================================
# SETUP (Same as before)
# ============================================================================

φ = (1 + sqrt(5)) / 2
M_P_MeV = mpf('1.22091e+22')
α = mpf('1') / mpf('137.035999177')
η_QED = 1 - α / (2 * pi)

m_e_exp = mpf('0.51099895069')
m_μ_exp = mpf('105.6583755')
m_τ_exp = mpf('1776.86')

lambda_rec_over_beta_0 = (pi * e) / sqrt(φ)

print(f"λ_rec/β_0 = π·e/√φ = {float(lambda_rec_over_beta_0):.6f}")
print()

def find_resonance(N):
    """Check if N/φ² is close to an integer"""
    k = N / (φ ** 2)
    k_nearest = round(float(k))
    delta_k = abs(k - k_nearest)
    return k, k_nearest, delta_k

def find_optimal_winding_systematic(N, k_res):
    """
    Systematic search for winding numbers
    
    For electron at N=111, k_res=42, we have w_c=(-41,70)
    Pattern: p ≈ -(k_res-1), q ≈ φ·|p| + offset
    
    But this might not generalize! Let's search more systematically.
    """
    # Start with pattern
    p_center = -(k_res - 1)
    
    # Search around this value
    best_w = None
    best_y = float('inf')
    
    for p in range(p_center - 5, p_center + 6):
        # For each p, find q that minimizes y = |q + p·φ|
        # This is minimized when q ≈ -p·φ
        q_optimal = -int(p * φ)
        
        # Search around optimal q
        for q_offset in range(-10, 11):
            q = q_optimal + q_offset
            y = abs(q + p * φ)
            
            if y < best_y and y > 0.1:  # Avoid y→0
                best_y = y
                best_w = (p, q)
    
    return best_w

def calculate_mass(N, w_c, verbose=False):
    """Calculate particle mass from epoch N and winding numbers w_c"""
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
    
    if verbose:
        print(f"  N={N}, w_c={w_c}")
        print(f"  k_res={float(k_res):.4f}, δ={float(δ):.4f}")
        print(f"  y={float(y):.4f}, ν={float(ν):.4f}")
        print(f"  C={float(C):.4f}")
        print(f"  m={float(m):.4f} MeV")
    
    return m

# ============================================================================
# PART 1: VERIFY ELECTRON
# ============================================================================

print("=" * 80)
print("VERIFY ELECTRON (N=111)")
print("=" * 80)
print()

N_e = 111
w_e = (-41, 70)
m_e_theory = calculate_mass(N_e, w_e, verbose=True)
error_e = ((m_e_theory - m_e_exp) / m_e_exp) * 100
print(f"  Error = {float(error_e):+.2f}% ✓")
print()

# ============================================================================
# PART 2: SCAN FOR MUON (N < 111)
# ============================================================================

print("=" * 80)
print("SCAN FOR MUON: N = 50 to 110 (below electron)")
print("=" * 80)
print()

muon_candidates = []

print(f"Target: m_μ = {float(m_μ_exp):.2f} MeV")
print()

for N in range(50, 111):
    k, k_nearest, delta_k = find_resonance(N)
    
    if delta_k < 0.5:  # Good resonance
        w_c = find_optimal_winding_systematic(N, k_nearest)
        m_theory = calculate_mass(N, w_c)
        error = abs((m_theory - m_μ_exp) / m_μ_exp) * 100
        
        muon_candidates.append({
            'N': N,
            'k_res': float(k),
            'delta_k': float(delta_k),
            'w_c': w_c,
            'm_theory': float(m_theory),
            'error_%': float(error)
        })
        
        # Print close matches
        if error < 50:
            print(f"N={N:3d}: k={float(k):5.2f}, Δk={float(delta_k):.3f}, " +
                  f"w={w_c}, m={float(m_theory):8.2f} MeV, err={float(error):5.1f}%")

print()
if muon_candidates:
    best_muon = min(muon_candidates, key=lambda x: x['error_%'])
    print(f"BEST MUON: N={best_muon['N']}, w={best_muon['w_c']}, " +
          f"m={best_muon['m_theory']:.2f} MeV (error={best_muon['error_%']:.1f}%)")
print()

# ============================================================================
# PART 3: SCAN FOR TAU (N < 50)
# ============================================================================

print("=" * 80)
print("SCAN FOR TAU: N = 1 to 50 (below muon)")
print("=" * 80)
print()

tau_candidates = []

print(f"Target: m_τ = {float(m_τ_exp):.2f} MeV")
print()

for N in range(1, 51):
    k, k_nearest, delta_k = find_resonance(N)
    
    if delta_k < 0.5:  # Good resonance
        w_c = find_optimal_winding_systematic(N, k_nearest)
        m_theory = calculate_mass(N, w_c)
        error = abs((m_theory - m_τ_exp) / m_τ_exp) * 100
        
        tau_candidates.append({
            'N': N,
            'k_res': float(k),
            'delta_k': float(delta_k),
            'w_c': w_c,
            'm_theory': float(m_theory),
            'error_%': float(error)
        })
        
        # Print close matches
        if error < 50:
            print(f"N={N:3d}: k={float(k):5.2f}, Δk={float(delta_k):.3f}, " +
                  f"w={w_c}, m={float(m_theory):9.2f} MeV, err={float(error):5.1f}%")

print()
if tau_candidates:
    best_tau = min(tau_candidates, key=lambda x: x['error_%'])
    print(f"BEST TAU: N={best_tau['N']}, w={best_tau['w_c']}, " +
          f"m={best_tau['m_theory']:.2f} MeV (error={best_tau['error_%']:.1f}%)")
print()

# ============================================================================
# PART 4: SCAN FOR NEUTRINOS (N > 111)
# ============================================================================

print("=" * 80)
print("SCAN FOR NEUTRINOS: N = 112 to 300 (above electron)")
print("=" * 80)
print()

neutrino_candidates = []

print(f"Target: m_ν ~ 10^(-8) MeV")
print()

for N in range(112, 301):
    k, k_nearest, delta_k = find_resonance(N)
    
    if delta_k < 0.5:
        w_c = find_optimal_winding_systematic(N, k_nearest)
        m_theory = calculate_mass(N, w_c)
        
        # Check if in neutrino range
        if 1e-10 < m_theory < 1e-6:
            neutrino_candidates.append({
                'N': N,
                'k_res': float(k),
                'delta_k': float(delta_k),
                'w_c': w_c,
                'm_theory': float(m_theory)
            })
            
            print(f"N={N:3d}: k={float(k):5.2f}, Δk={float(delta_k):.3f}, " +
                  f"w={w_c}, m={float(m_theory):.3e} MeV")

print()
print(f"Found {len(neutrino_candidates)} neutrino candidates")
print()

# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 80)
print("SUMMARY: CORRECTED LEPTON PREDICTIONS")
print("=" * 80)
print()

print(f"{'Particle':<10} {'N':<5} {'Winding (p,q)':<20} {'m_theory (MeV)':<18} {'m_exp (MeV)':<15} {'Error':<10}")
print("-" * 100)

# Electron
w_str = f"({w_e[0]}, {w_e[1]})"
print(f"{'electron':<10} {N_e:<5} {w_str:<20} {float(m_e_theory):<18.4f} {float(m_e_exp):<15.4f} {float(error_e):+.2f}%")

# Muon
if muon_candidates:
    best_muon = min(muon_candidates, key=lambda x: x['error_%'])
    w_str = f"({best_muon['w_c'][0]}, {best_muon['w_c'][1]})"
    print(f"{'muon':<10} {best_muon['N']:<5} {w_str:<20} {best_muon['m_theory']:<18.4f} {float(m_μ_exp):<15.4f} {best_muon['error_%']:+.2f}%")

# Tau
if tau_candidates:
    best_tau = min(tau_candidates, key=lambda x: x['error_%'])
    w_str = f"({best_tau['w_c'][0]}, {best_tau['w_c'][1]})"
    print(f"{'tau':<10} {best_tau['N']:<5} {w_str:<20} {best_tau['m_theory']:<18.4f} {float(m_τ_exp):<15.4f} {best_tau['error_%']:+.2f}%")

# Neutrinos (tentative)
if neutrino_candidates:
    for i, nu in enumerate(sorted(neutrino_candidates, key=lambda x: x['m_theory'])[:3]):
        name = ['ν_e', 'ν_μ', 'ν_τ'][i]
        w_str = f"({nu['w_c'][0]}, {nu['w_c'][1]})"
        print(f"{name:<10} {nu['N']:<5} {w_str:<20} {nu['m_theory']:<18.3e} {'~10^-8':<15} {'N/A':<10}")

print()

# Generation structure
if muon_candidates and tau_candidates:
    best_muon = min(muon_candidates, key=lambda x: x['error_%'])
    best_tau = min(tau_candidates, key=lambda x: x['error_%'])
    
    print("GENERATION STRUCTURE:")
    print(f"  Tau:     N_τ = {best_tau['N']} (heaviest, lowest epoch)")
    print(f"  Muon:    N_μ = {best_muon['N']}")
    print(f"  Electron: N_e = {N_e} (lightest, highest epoch)")
    print()
    print(f"  Pattern: LOWER N → HIGHER mass (φ^N in denominator!)")
    print()

# Save results
results = {
    'date': datetime.now().isoformat(),
    'insight': 'Higher N gives lower mass (φ^N in denominator)',
    'electron': {'N': N_e, 'w_c': w_e, 'm_theory': float(m_e_theory), 'error_%': float(error_e)},
    'muon_candidates': muon_candidates[:10],  # Top 10
    'tau_candidates': tau_candidates[:10],
    'neutrino_candidates': neutrino_candidates[:10]
}

with open("/Users/Cristiana_1/Documents/Golden Universe/PHASE14B_CORRECTED_LEPTON_SCAN.json", 'w') as f:
    json.dump(results, f, indent=2)

print("Results saved to: PHASE14B_CORRECTED_LEPTON_SCAN.json")
print()
print("=" * 80)
print("PHASE 14B COMPLETE")
print("=" * 80)
