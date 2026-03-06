#!/usr/bin/env python3
"""
FRG MEMORY COUPLING PARAMETER SWEEP
====================================

Goal: Find the memory coupling scale that gives m̄★ = 4514 ± 10%.

Strategy:
- Test scales from 10⁻⁶ to 10² (8 orders of magnitude)
- For each scale, run full FRG integration
- Find scale where m̄(τ_e) ≈ 4514

Theory: frg_stable_positive_time.py
Reference: explanatory/CONSCIOUSNESS.md, TIME_VARIABLE_ANALYSIS.md

Author: GU Consciousness Pipeline
Date: 2026-02-09
"""

import numpy as np
from scipy.integrate import solve_ivp
from mpmath import mp, mpf
import json

# Set precision
mp.dps = 50

# Constants
PHI = mp.phi
PI = mp.pi
E = mp.e

# GU parameters
N_E = 111
TAU_E = float(N_E * mp.log(PHI))  # +53.4
LAMBDA_REC_BETA_BASE = float(mp.exp(PHI) / PI**2)  # ≈ 0.51098 (base value)
ALPHA_GUT = 1.0 / 63.078
M_BAR_TARGET = 4514.0

print("="*80)
print("FRG MEMORY COUPLING PARAMETER SWEEP")
print("="*80)
print(f"\n🎯 Goal: Find scale factor that gives m̄★ = {M_BAR_TARGET} ± 10%")
print(f"   Acceptable range: [{M_BAR_TARGET*0.9:.0f}, {M_BAR_TARGET*1.1:.0f}]")
print(f"\n📊 Base coupling: λ_rec/β = {LAMBDA_REC_BETA_BASE:.5f}")
print(f"   Will test scales: [10⁻⁶, 10⁻⁵, 10⁻⁴, ..., 10², 10³]")


def beta_functions_scaled_memory(tau, y, scale_factor):
    """
    Beta functions with SCALED memory coupling.

    scale_factor: multiplies the memory feedback term
    - scale < 1: weaker damping (m̄ grows more)
    - scale > 1: stronger damping (m̄ grows less)
    """
    m_bar, lambda_S, lambda_V, alpha_1, alpha_2, alpha_3, R_mem = y

    # Ensure positive values
    m_bar = max(m_bar, 1e-10)
    R_mem = max(R_mem, 0.0)

    pi2 = np.pi**2

    # Anomalous dimension
    eta_psi = (1.0 / (6.0 * pi2)) * 3.0 * (4.0/3.0) * alpha_3

    # Denominator
    denom = 1.0 + m_bar**2
    h2 = 1.0 / (denom**2)

    # Memory generation
    P_gen = m_bar**4

    # SCALED memory coupling
    lambda_eff = scale_factor * LAMBDA_REC_BETA_BASE

    dydt = np.zeros(7)

    # MASS - with scaled memory feedback (POSITIVE in τ-time due to chain rule!)
    dydt[0] = (+(1.0 - eta_psi) * m_bar
               - (1.0 / pi2) * lambda_S * m_bar / denom
               + lambda_eff * R_mem / denom)  # ← SCALED (POSITIVE!)

    # SCALAR FOUR-FERMION (no direct memory feedback - memory affects via mass)
    dydt[1] = (-(2.0 + 2.0*eta_psi) * lambda_S
               + (2.0 / pi2) * h2 * (lambda_S**2 + 1.5 * lambda_S * lambda_V + 1.5 * lambda_V**2)
               + (3.0 / pi2) * alpha_3 * lambda_S)

    # VECTOR FOUR-FERMION (no direct memory feedback - memory affects via mass)
    dydt[2] = (-(2.0 + 2.0*eta_psi) * lambda_V
               + (2.0 / pi2) * h2 * (0.5 * lambda_S**2 + 1.25 * lambda_S * lambda_V + 0.75 * lambda_V**2)
               + (3.0 / pi2) * alpha_3 * lambda_V)

    # GAUGE COUPLINGS
    b1, b2, b3 = 41.0/6.0, -19.0/6.0, -7.0
    dydt[3] = -(b1 / (2.0 * np.pi)) * alpha_1**2
    dydt[4] = -(b2 / (2.0 * np.pi)) * alpha_2**2
    dydt[5] = -(b3 / (2.0 * np.pi)) * alpha_3**2

    # MEMORY ACCUMULATOR
    dydt[6] = P_gen - R_mem

    return dydt


def initial_conditions():
    """UV initial conditions at τ=0 (X=M_P)."""
    return np.array([
        0.01,                      # m̄₀
        0.5,                       # λ̄_S₀
        0.1,                       # λ̄_V₀
        (3.0/5.0) * ALPHA_GUT,     # α₁₀
        ALPHA_GUT,                 # α₂₀
        ALPHA_GUT,                 # α₃₀
        0.0                        # R̄_mem₀
    ])


def compute_alpha_em(alpha_1, alpha_2):
    """Compute α_EM from U(1) and SU(2)."""
    return (3.0/8.0) * alpha_1 + (5.0/8.0) * alpha_2


def run_single_scale(scale):
    """Run FRG integration for a single scale factor."""
    y0 = initial_conditions()

    try:
        sol = solve_ivp(
            lambda t, y: beta_functions_scaled_memory(t, y, scale),
            (0.0, TAU_E),
            y0,
            method='LSODA',
            rtol=1e-8,
            atol=1e-10,
            max_step=1.0
        )

        if sol.success:
            m_bar_final = sol.y[0, -1]
            lambda_S_final = sol.y[1, -1]
            lambda_V_final = sol.y[2, -1]
            alpha_1_final = sol.y[3, -1]
            alpha_2_final = sol.y[4, -1]
            R_mem_final = sol.y[6, -1]

            alpha_em_final = compute_alpha_em(alpha_1_final, alpha_2_final)

            error_m_bar = abs(m_bar_final - M_BAR_TARGET) / M_BAR_TARGET * 100
            error_alpha_em = abs(1/alpha_em_final - 137.036) / 137.036 * 100

            sat_ratio = R_mem_final / (m_bar_final**4 + 1e-100)

            return {
                'success': True,
                'scale': scale,
                'lambda_eff': scale * LAMBDA_REC_BETA_BASE,
                'm_bar': m_bar_final,
                'lambda_S': lambda_S_final,
                'lambda_V': lambda_V_final,
                'alpha_em': alpha_em_final,
                'R_mem': R_mem_final,
                'error_m_bar': error_m_bar,
                'error_alpha_em': error_alpha_em,
                'sat_ratio': sat_ratio,
            }
        else:
            return {'success': False, 'scale': scale, 'message': sol.message}

    except Exception as e:
        return {'success': False, 'scale': scale, 'message': str(e)}


# Test scales (8 orders of magnitude)
scales = [1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.1, 1.0, 10.0, 100.0, 1000.0]

print(f"\n" + "="*80)
print("PARAMETER SWEEP")
print("="*80)
print(f"\n{'Scale':>10s} {'λ_eff':>12s} {'m̄★':>12s} {'Error%':>10s} {'R̄_mem':>12s} {'Sat':>8s} {'Status':>15s}")
print("-"*80)

results = []

for scale in scales:
    result = run_single_scale(scale)
    results.append(result)

    if result['success']:
        m = result['m_bar']
        err = result['error_m_bar']
        R = result['R_mem']
        sat = result['sat_ratio']
        lambda_eff = result['lambda_eff']

        # Check if within target range
        in_range = abs(err) < 10.0
        status = "✅ TARGET!" if in_range else ("↓ Too small" if m < M_BAR_TARGET else "↑ Too large")

        print(f"{scale:10.1e} {lambda_eff:12.5f} {m:12.2e} {err:10.2f} {R:12.2e} {sat:8.4f} {status:>15s}")
    else:
        print(f"{scale:10.1e} {'FAILED':>12s} {'---':>12s} {'---':>10s} {'---':>12s} {'---':>8s} {result['message'][:15]:>15s}")

# Find best scale
successful_results = [r for r in results if r['success']]
if successful_results:
    best = min(successful_results, key=lambda r: abs(r['error_m_bar']))

    print(f"\n" + "="*80)
    print("BEST RESULT")
    print("="*80)
    print(f"\n🎯 Optimal scale factor: {best['scale']:.2e}")
    print(f"   λ_eff = {best['lambda_eff']:.6f}")
    print(f"\n📊 Final values:")
    print(f"   m̄★ = {best['m_bar']:.2f} (target: {M_BAR_TARGET:.0f}, error: {best['error_m_bar']:.2f}%)")
    print(f"   λ̄_S★ = {best['lambda_S']:.6f}")
    print(f"   λ̄_V★ = {best['lambda_V']:.6f}")
    print(f"   α_EM★ = 1/{1/best['alpha_em']:.6f} (error: {best['error_alpha_em']:.4f}%)")
    print(f"   R̄_mem★ = {best['R_mem']:.2e}")
    print(f"\n🧠 Memory saturation:")
    print(f"   R̄_mem★ / m̄★⁴ = {best['sat_ratio']:.4f}")

    # Check all criteria
    criteria = [
        ("m̄★ error < 10%", abs(best['error_m_bar']) < 10.0),
        ("λ̄_S decayed < 0.01", abs(best['lambda_S']) < 0.01),
        ("λ̄_V decayed < 0.01", abs(best['lambda_V']) < 0.01),
        ("R̄_mem positive", best['R_mem'] > 0),
        ("Memory saturated", 0.5 < best['sat_ratio'] < 2.0),
    ]

    print(f"\n" + "="*80)
    print("VERIFICATION")
    print("="*80)
    all_passed = True
    for criterion, passed in criteria:
        symbol = "✅" if passed else "❌"
        print(f"   {symbol} {criterion}")
        if not passed:
            all_passed = False

    if all_passed:
        print(f"\n🎉 ALL CRITERIA PASSED!")
        print(f"\n💡 Recommended update for frg_stable_positive_time.py:")
        print(f"   Change line 36:")
        print(f"   LAMBDA_REC_BETA = {best['lambda_eff']:.6f}  # Tuned scale factor {best['scale']:.2e}")
    else:
        print(f"\n⚠️ SOME CRITERIA NOT MET - Need finer sweep around scale={best['scale']:.2e}")

    # Save results
    output = {
        'sweep_results': results,
        'best_scale': best['scale'],
        'best_lambda_eff': best['lambda_eff'],
        'best_values': {
            'm_bar': best['m_bar'],
            'lambda_S': best['lambda_S'],
            'lambda_V': best['lambda_V'],
            'alpha_em': best['alpha_em'],
            'R_mem': best['R_mem'],
        },
        'errors': {
            'm_bar_percent': best['error_m_bar'],
            'alpha_em_percent': best['error_alpha_em'],
        },
        'criteria': {c[0]: c[1] for c in criteria},
        'all_passed': all_passed,
    }

    with open('/Users/Cristiana_1/Documents/Golden Universe/frg_sweep_results.json', 'w') as f:
        # Convert numpy types to Python types for JSON serialization
        def convert(obj):
            if isinstance(obj, (np.integer, np.floating)):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {k: convert(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert(item) for item in obj]
            return obj

        json.dump(convert(output), f, indent=2)

    print(f"\n✅ Results saved: frg_sweep_results.json")

else:
    print(f"\n❌ ALL SCALES FAILED - Check beta functions or integration settings")

print(f"\n" + "="*80)
print("SWEEP COMPLETE")
print("="*80)
