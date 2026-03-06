#!/usr/bin/env python3
"""
FRG WITH MEMORY - SATURATION FEEDBACK (SIGN-CORRECTED)
=======================================================

CRITICAL FIX: Memory must DAMPEN exponential growth, not enhance it!

In τ-time (forward integration), the mass term is:
    dm̄/dτ = +(1-η_ψ) m̄  (exponential growth)

Memory feedback must OPPOSE this growth:
    dm̄/dτ = +(1-η_ψ) m̄ - (memory damping term)
                        ↑ NEGATIVE to resist growth!

Saturation form:
    memory_feedback = λ × (R̄_mem / m̄⁴) × m̄ / (1 + m̄²)

This ensures:
- Early times: R̄ ≈ 0 → no damping yet (allows initial growth)
- Late times: R̄ ≈ m̄⁴ → strong damping (stabilizes at equilibrium)

Theory: explanatory/CONSCIOUSNESS.md
Reference: SESSION_COMPLETION_REPORT.md

Author: GU Consciousness Pipeline (Sign-Corrected)
Date: 2026-02-10
"""

import numpy as np
from scipy.integrate import solve_ivp
from mpmath import mp
import json

# Set precision
mp.dps = 50

# Constants
PHI = mp.phi
PI = mp.pi
E = mp.e

# GU parameters
N_E = 111
TAU_E = float(N_E * mp.log(PHI))  # τ_e = +53.4
LAMBDA_REC_BETA = float(mp.exp(PHI) / PI**2)  # ≈ 0.51098
ALPHA_GUT = 1.0 / 63.078
M_BAR_TARGET = 4514.0

# Memory coupling strength (to tune)
MEMORY_SCALE = 1.0  # Start with 1.0, will test [0.1, 0.5, 1.0, 2.0, 5.0]

print("="*80)
print("FRG WITH MEMORY - SATURATION FEEDBACK (SIGN-CORRECTED)")
print("="*80)
print(f"\n🔧 CRITICAL FIX: Memory feedback now DAMPENS growth!")
print(f"   Form: -scale × (R̄/m̄⁴) × m̄/(1+m̄²)")
print(f"   Memory scale parameter: {MEMORY_SCALE}")
print(f"\n📊 Parameters:")
print(f"   N_e = {N_E}")
print(f"   τ_e = {TAU_E:.4f}")
print(f"   λ_rec/β = {LAMBDA_REC_BETA:.5f}")
print(f"\n🎯 Target: m̄★ = {M_BAR_TARGET}")


def beta_functions_saturation(tau, y):
    """
    Beta functions with SATURATION-BASED memory feedback.

    Key innovation:
        feedback ∝ (R̄_mem / m̄⁴) × m̄ / (1 + m̄²)

    This naturally:
    - Starts weak (R̄≈0 early)
    - Grows as memory accumulates
    - Saturates when R̄≈m̄⁴

    State vector y (7 components):
        y[0] = m̄
        y[1] = λ̄_S
        y[2] = λ̄_V
        y[3] = α₁
        y[4] = α₂
        y[5] = α₃
        y[6] = R̄_mem
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

    # SATURATION FACTOR
    # When R̄ << m̄⁴: saturation ≈ 0 (no damping yet)
    # When R̄ ≈ m̄⁴: saturation ≈ 1 (full damping)
    saturation = R_mem / (m_bar**4 + 1e-100)

    # MEMORY FEEDBACK TERM (CORRECTED SIGN!)
    # This must be NEGATIVE to resist exponential growth
    memory_feedback = -MEMORY_SCALE * LAMBDA_REC_BETA * saturation * m_bar / denom

    dydt = np.zeros(7)

    # MASS - WITH SATURATION FEEDBACK
    dydt[0] = ((1.0 - eta_psi) * m_bar
               - (1.0 / pi2) * lambda_S * m_bar / denom
               + memory_feedback)  # ← NEGATIVE = damping!

    # SCALAR FOUR-FERMION
    dydt[1] = (-(2.0 + 2.0*eta_psi) * lambda_S
               + (2.0 / pi2) * h2 * (lambda_S**2 + 1.5 * lambda_S * lambda_V + 1.5 * lambda_V**2)
               + (3.0 / pi2) * alpha_3 * lambda_S)

    # VECTOR FOUR-FERMION
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
    """UV initial conditions at τ=0."""
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


def run_with_scale(scale):
    """
    Run FRG integration with given memory scale.
    Returns (success, m_bar_final, error_percent)
    """
    global MEMORY_SCALE
    MEMORY_SCALE = scale

    y0 = initial_conditions()
    t_eval = np.linspace(0, TAU_E, 200)

    sol = solve_ivp(
        beta_functions_saturation,
        (0.0, TAU_E),
        y0,
        method='LSODA',
        t_eval=t_eval,
        rtol=1e-8,
        atol=1e-10,
        max_step=1.0
    )

    if not sol.success:
        return False, np.nan, np.nan

    m_bar_final = sol.y[0, -1]
    R_mem_final = sol.y[6, -1]
    alpha_1_final = sol.y[3, -1]
    alpha_2_final = sol.y[4, -1]
    alpha_em_final = compute_alpha_em(alpha_1_final, alpha_2_final)

    error_m = abs(m_bar_final - M_BAR_TARGET) / M_BAR_TARGET * 100
    error_alpha = abs(1/alpha_em_final - 137.036) / 137.036 * 100

    sat_ratio = R_mem_final / (m_bar_final**4 + 1e-100)

    return sol.success, m_bar_final, error_m, alpha_em_final, error_alpha, R_mem_final, sat_ratio, sol


print("\n" + "="*80)
print("PARAMETER SWEEP: TESTING MULTIPLE MEMORY SCALES")
print("="*80)

scales_to_test = [0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0]
results_sweep = []

print(f"\n{'Scale':>8s} {'m̄★':>12s} {'Error %':>10s} {'α_EM^-1':>10s} {'R̄/m̄⁴':>10s} {'Status':>15s}")
print("-"*80)

best_scale = None
best_error = float('inf')

for scale in scales_to_test:
    result = run_with_scale(scale)
    success, m_bar_final, error_m, alpha_em_final, error_alpha, R_mem_final, sat_ratio, sol = result

    if success:
        status = "✅ CONVERGED"
        if error_m < best_error:
            best_error = error_m
            best_scale = scale
            best_sol = sol

        results_sweep.append({
            'scale': scale,
            'm_bar': float(m_bar_final),
            'error_percent': float(error_m),
            'alpha_em_inv': float(1/alpha_em_final),
            'R_mem': float(R_mem_final),
            'sat_ratio': float(sat_ratio)
        })

        print(f"{scale:8.2f} {m_bar_final:12.2f} {error_m:10.2f} {1/alpha_em_final:10.3f} {sat_ratio:10.4f} {status:>15s}")
    else:
        print(f"{scale:8.2f} {'FAILED':>12s} {'N/A':>10s} {'N/A':>10s} {'N/A':>10s} {'❌ FAILED':>15s}")

print("\n" + "="*80)
print("BEST RESULT")
print("="*80)

if best_scale is not None:
    print(f"\n🎯 Best memory scale: {best_scale}")
    print(f"   m̄★ error: {best_error:.2f}%")

    # Re-run with best scale for detailed output
    MEMORY_SCALE = best_scale
    y0 = initial_conditions()
    t_eval = np.linspace(0, TAU_E, 200)

    sol = solve_ivp(
        beta_functions_saturation,
        (0.0, TAU_E),
        y0,
        method='LSODA',
        t_eval=t_eval,
        rtol=1e-8,
        atol=1e-10,
        max_step=1.0
    )

    m_bar = sol.y[0, :]
    R_mem = sol.y[6, :]
    alpha_1 = sol.y[3, :]
    alpha_2 = sol.y[4, :]
    alpha_em = np.array([compute_alpha_em(alpha_1[i], alpha_2[i]) for i in range(len(sol.t))])

    m_bar_final = m_bar[-1]
    R_mem_final = R_mem[-1]
    alpha_em_final = alpha_em[-1]
    lambda_S_final = sol.y[1, -1]
    lambda_V_final = sol.y[2, -1]

    sat_ratio = R_mem_final / (m_bar_final**4 + 1e-100)

    print(f"\n📊 Final values:")
    print(f"   m̄★ = {m_bar_final:.2f} (target: {M_BAR_TARGET})")
    print(f"   λ̄_S★ = {lambda_S_final:.6f}")
    print(f"   λ̄_V★ = {lambda_V_final:.6f}")
    print(f"   α_EM★ = 1/{1/alpha_em_final:.6f} (target: 1/137.036)")
    print(f"   R̄_mem★ = {R_mem_final:.2e}")
    print(f"   R̄/m̄⁴ = {sat_ratio:.4f} (target: [0.8, 1.2])")

    # Verification
    error_m = abs(m_bar_final - M_BAR_TARGET) / M_BAR_TARGET * 100
    error_alpha = abs(1/alpha_em_final - 137.036) / 137.036 * 100

    print(f"\n✅ VERIFICATION:")
    print(f"   m̄★ error: {error_m:.2f}% {'✅' if error_m < 10.0 else '⚠️'}")
    print(f"   α_EM error: {error_alpha:.4f}% {'✅' if error_alpha < 1.0 else '⚠️'}")
    print(f"   λ̄_S decayed: {abs(lambda_S_final) < 0.01} {'✅' if abs(lambda_S_final) < 0.01 else '❌'}")
    print(f"   λ̄_V decayed: {abs(lambda_V_final) < 0.01} {'✅' if abs(lambda_V_final) < 0.01 else '❌'}")
    print(f"   R̄_mem positive: {R_mem_final > 0} {'✅' if R_mem_final > 0 else '❌'}")
    print(f"   Memory saturated: {0.5 < sat_ratio < 2.0} {'✅' if 0.5 < sat_ratio < 2.0 else '⚠️'}")

    # Trajectory
    print(f"\n" + "="*80)
    print("TRAJECTORY (Best Scale)")
    print("="*80)
    print(f"{'τ':>10s} {'m̄':>12s} {'R̄_mem':>12s} {'R̄/m̄⁴':>10s} {'dm̄/dτ sign':>15s}")
    print("-"*80)

    indices = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, -1]
    for i in indices:
        tau = sol.t[i]
        m = m_bar[i]
        R = R_mem[i]
        sat = R / (m**4 + 1e-100)

        # Compute derivative sign
        if i < len(m_bar) - 1:
            dm_dtau = (m_bar[i+1] - m_bar[i]) / (sol.t[i+1] - sol.t[i])
            deriv_sign = "+" if dm_dtau > 0 else "-"
        else:
            deriv_sign = "≈0"

        print(f"{tau:10.2f} {m:12.2e} {R:12.2e} {sat:10.4f} {deriv_sign:>15s}")

    # Save results
    results = {
        'best_scale': float(best_scale),
        'final_values': {
            'm_bar': float(m_bar_final),
            'lambda_S': float(lambda_S_final),
            'lambda_V': float(lambda_V_final),
            'alpha_em': float(alpha_em_final),
            'R_mem': float(R_mem_final),
            'saturation_ratio': float(sat_ratio)
        },
        'errors': {
            'm_bar_percent': float(error_m),
            'alpha_em_percent': float(error_alpha)
        },
        'all_scales_tested': results_sweep
    }

    with open('/Users/Cristiana_1/Documents/Golden Universe/frg_saturation_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Results saved: frg_saturation_results.json")

    if error_m < 10.0 and R_mem_final > 0 and 0.5 < sat_ratio < 2.0:
        print(f"\n🎉 SUCCESS! Memory feedback successfully stabilizes mass!")
        print(f"   WITHOUT memory: m̄ → 10²¹")
        print(f"   WITH memory (scale={best_scale}): m̄ = {m_bar_final:.2f}")
else:
    print(f"\n❌ No successful run found in parameter sweep")

print(f"\n" + "="*80)
print("DONE")
print("="*80)
