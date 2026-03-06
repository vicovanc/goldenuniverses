#!/usr/bin/env python3
"""
Golden Universe Theory - Phase 15: CORRECT Generation Lattice Structure
========================================================================

CRITICAL CORRECTION:
The generation jumps ΔN_μ = 11 and ΔN_τ = 17 are the MANHATTAN LENGTHS
of step vectors in (p,q) space, NOT simple N subtractions!

Given:
- Electron: (p_e, q_e) = (-41, 70), N_e = |p_e| + |q_e| = 111
- Generation step: (Δp, Δq) with |Δp| + |Δq| = 11 or 17
- Muon: (p_μ, q_μ) = (p_e + Δp, q_e + Δq)
- N_μ = |p_μ| + |q_μ| ≠ N_e - 11 in general!

TASK: Find which step vector gives N_μ ≈ 107 (from our scan)
"""

from mpmath import mp, mpf, sqrt, pi, e, ellipk, ellipe
import json

mp.dps = 50

φ = (1 + sqrt(5)) / 2
M_P_MeV = mpf('1.22091e+22')
α = mpf('1') / mpf('137.035999177')
η_QED = 1 - α / (2 * pi)
lambda_rec_over_beta_0 = (pi * e) / sqrt(φ)

m_e_exp = mpf('0.51099895069')
m_μ_exp = mpf('105.6583755')
m_τ_exp = mpf('1776.86')

print("=" * 80)
print("PHASE 15: CORRECT GENERATION LATTICE STRUCTURE")
print("=" * 80)
print()

print("CRITICAL INSIGHT:")
print("  ΔN = |Δp| + |Δq| is Manhattan length of step vector")
print("  NOT the same as N_new - N_old!")
print()

# Electron base point
p_e, q_e = -41, 70
N_e = abs(p_e) + abs(q_e)
print(f"Electron: (p, q) = ({p_e}, {q_e}), N = {N_e}")
print()

def calculate_mass(N, p, q):
    """Calculate mass from epoch N and winding numbers (p,q)"""
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
    
    return m, float(k_res), float(δ), float(y)

# ============================================================================
# PART 1: Find which step vector with |Δp| + |Δq| = 11 gives N ≈ 107
# ============================================================================

print("=" * 80)
print("PART 1: Search for Muon Step Vector (|Δp| + |Δq| = 11)")
print("=" * 80)
print()

print(f"Target: N_μ ≈ 107 (from scan), m_μ = {float(m_μ_exp)} MeV")
print()

muon_candidates = []

# Generate all step vectors with Manhattan length 11
print("Testing all step vectors with |Δp| + |Δq| = 11:")
print()

for Δp in range(-11, 12):
    for Δq in range(-11, 12):
        if abs(Δp) + abs(Δq) == 11:
            # Calculate new position
            p_μ = p_e + Δp
            q_μ = q_e + Δq
            N_μ = abs(p_μ) + abs(q_μ)
            
            # Only consider if N is reasonable (around 107)
            if 100 <= N_μ <= 115:
                try:
                    m_μ, k_res, δ, y = calculate_mass(N_μ, p_μ, q_μ)
                    error = abs((m_μ - m_μ_exp) / m_μ_exp) * 100
                    
                    muon_candidates.append({
                        'step': (Δp, Δq),
                        'position': (p_μ, q_μ),
                        'N': N_μ,
                        'k_res': k_res,
                        'delta_k': δ,
                        'y': y,
                        'm_theory': float(m_μ),
                        'error_%': float(error)
                    })
                    
                    if error < 10:
                        print(f"  Step ({Δp:+3d}, {Δq:+3d}) → ({p_μ:+3d}, {q_μ:+3d}), " +
                              f"N={N_μ:3d}, m={float(m_μ):7.2f} MeV, err={float(error):5.2f}%")
                except:
                    pass

print()
if muon_candidates:
    best_muon = min(muon_candidates, key=lambda x: x['error_%'])
    print(f"BEST MUON MATCH:")
    print(f"  Step vector: (Δp, Δq) = {best_muon['step']}")
    print(f"  |Δp| + |Δq| = {abs(best_muon['step'][0]) + abs(best_muon['step'][1])}")
    print(f"  Position: (p_μ, q_μ) = {best_muon['position']}")
    print(f"  N_μ = {best_muon['N']}")
    print(f"  m_μ (theory) = {best_muon['m_theory']:.2f} MeV")
    print(f"  m_μ (exp)    = {float(m_μ_exp):.2f} MeV")
    print(f"  Error = {best_muon['error_%']:+.2f}%")
else:
    print("  ❌ No good muon candidates found!")

print()

# ============================================================================
# PART 2: Find which step vector with |Δp| + |Δq| = 17 gives tau
# ============================================================================

print("=" * 80)
print("PART 2: Search for Tau Step Vector (|Δp| + |Δq| = 17)")
print("=" * 80)
print()

print(f"Target: m_τ = {float(m_τ_exp)} MeV")
print("Testing step vectors from electron position...")
print()

tau_candidates = []

# Generate all step vectors with Manhattan length 17
for Δp in range(-17, 18):
    for Δq in range(-17, 18):
        if abs(Δp) + abs(Δq) == 17:
            # Calculate new position
            p_τ = p_e + Δp
            q_τ = q_e + Δq
            N_τ = abs(p_τ) + abs(q_τ)
            
            # Wide range for tau
            if 50 <= N_τ <= 150:
                try:
                    m_τ, k_res, δ, y = calculate_mass(N_τ, p_τ, q_τ)
                    error = abs((m_τ - m_τ_exp) / m_τ_exp) * 100
                    
                    tau_candidates.append({
                        'step': (Δp, Δq),
                        'position': (p_τ, q_τ),
                        'N': N_τ,
                        'k_res': k_res,
                        'delta_k': δ,
                        'y': y,
                        'm_theory': float(m_τ),
                        'error_%': float(error)
                    })
                    
                    if error < 20:
                        print(f"  Step ({Δp:+3d}, {Δq:+3d}) → ({p_τ:+3d}, {q_τ:+3d}), " +
                              f"N={N_τ:3d}, m={float(m_τ):7.2f} MeV, err={float(error):5.2f}%")
                except:
                    pass

print()
if tau_candidates:
    best_tau = min(tau_candidates, key=lambda x: x['error_%'])
    print(f"BEST TAU MATCH:")
    print(f"  Step vector: (Δp, Δq) = {best_tau['step']}")
    print(f"  |Δp| + |Δq| = {abs(best_tau['step'][0]) + abs(best_tau['step'][1])}")
    print(f"  Position: (p_τ, q_τ) = {best_tau['position']}")
    print(f"  N_τ = {best_tau['N']}")
    print(f"  m_τ (theory) = {best_tau['m_theory']:.2f} MeV")
    print(f"  m_τ (exp)    = {float(m_τ_exp):.2f} MeV")
    print(f"  Error = {best_tau['error_%']:+.2f}%")
else:
    print("  ❌ No good tau candidates found!")

print()

# ============================================================================
# PART 3: Alternative - Search from MUON position
# ============================================================================

if muon_candidates:
    print("=" * 80)
    print("PART 3: Alternative - Tau from Muon Position")
    print("=" * 80)
    print()
    
    best_muon = min(muon_candidates, key=lambda x: x['error_%'])
    p_μ, q_μ = best_muon['position']
    N_μ = best_muon['N']
    
    print(f"Starting from muon: (p_μ, q_μ) = ({p_μ}, {q_μ}), N_μ = {N_μ}")
    print()
    
    tau_from_muon = []
    
    # Try various step sizes from muon
    for step_size in [6, 11, 17]:  # Test different Manhattan lengths
        print(f"Testing steps with |Δp| + |Δq| = {step_size}:")
        for Δp in range(-step_size, step_size+1):
            for Δq in range(-step_size, step_size+1):
                if abs(Δp) + abs(Δq) == step_size:
                    p_τ = p_μ + Δp
                    q_τ = q_μ + Δq
                    N_τ = abs(p_τ) + abs(q_τ)
                    
                    if 50 <= N_τ <= 150:
                        try:
                            m_τ, k_res, δ, y = calculate_mass(N_τ, p_τ, q_τ)
                            error = abs((m_τ - m_τ_exp) / m_τ_exp) * 100
                            
                            if error < 20:
                                tau_from_muon.append({
                                    'step_size': step_size,
                                    'step': (Δp, Δq),
                                    'position': (p_τ, q_τ),
                                    'N': N_τ,
                                    'm_theory': float(m_τ),
                                    'error_%': float(error)
                                })
                                
                                print(f"    Step ({Δp:+3d}, {Δq:+3d}) → ({p_τ:+3d}, {q_τ:+3d}), " +
                                      f"N={N_τ:3d}, m={float(m_τ):7.2f} MeV, err={float(error):5.2f}%")
                        except:
                            pass
        print()

# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 80)
print("SUMMARY: CORRECT LATTICE STRUCTURE")
print("=" * 80)
print()

print(f"{'Generation':<12} {'Position (p,q)':<20} {'N':<5} {'Step from e':<15} {'m (MeV)':<12} {'Error'}")
print("-" * 90)

# Electron
print(f"{'Electron':<12} {str((p_e, q_e)):<20} {N_e:<5} {'-':<15} {float(m_e_exp):<12.2f} {'baseline'}")

# Muon
if muon_candidates:
    best = min(muon_candidates, key=lambda x: x['error_%'])
    step_str = f"{best['step']}"
    print(f"{'Muon':<12} {str(best['position']):<20} {best['N']:<5} {step_str:<15} {best['m_theory']:<12.2f} {best['error_%']:+.2f}%")

# Tau
if tau_candidates:
    best = min(tau_candidates, key=lambda x: x['error_%'])
    step_str = f"{best['step']}"
    print(f"{'Tau':<12} {str(best['position']):<20} {best['N']:<5} {step_str:<15} {best['m_theory']:<12.2f} {best['error_%']:+.2f}%")

print()

# Save results
output = {
    'electron': {'position': (p_e, q_e), 'N': N_e},
    'muon_candidates': muon_candidates[:5] if muon_candidates else [],
    'tau_candidates': tau_candidates[:5] if tau_candidates else [],
}

with open("/Users/Cristiana_1/Documents/Golden Universe/PHASE15_CORRECT_LATTICE.json", 'w') as f:
    json.dump(output, f, indent=2)

print("Results saved to: PHASE15_CORRECT_LATTICE.json")
print()
print("=" * 80)
print("PHASE 15 COMPLETE")
print("=" * 80)
