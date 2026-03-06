#!/usr/bin/env python3
"""
FRG WITH MEMORY - DIRECT FEEDBACK (NO SATURATION)
==================================================

Simpler form that doesn't require saturation:
    memory_feedback = -scale × R̄_mem / (1 + m̄²)

This provides immediate damping once R̄ starts accumulating.

Theory: explanatory/CONSCIOUSNESS.md
Date: 2026-02-10
"""

import numpy as np
from scipy.integrate import solve_ivp
from mpmath import mp
import json

mp.dps = 50

PHI = mp.phi
PI = mp.pi
E = mp.e

N_E = 111
TAU_E = float(N_E * mp.log(PHI))
LAMBDA_REC_BETA = float(mp.exp(PHI) / PI**2)
ALPHA_GUT = 1.0 / 63.078
M_BAR_TARGET = 4514.0

# Memory coupling (will sweep this)
MEMORY_SCALE = 1.0

print("="*80)
print("FRG WITH MEMORY - DIRECT FEEDBACK (SIMPLIFIED)")
print("="*80)
print(f"\nForm: -scale × R̄/(1+m̄²)  (no saturation factor)")
print(f"Testing scales: [10, 50, 100, 500, 1000, 5000, 10000]")
print(f"\n🎯 Target: m̄★ = {M_BAR_TARGET}")


def beta_functions_direct(tau, y):
    """Direct memory feedback without saturation factor."""
    m_bar, lambda_S, lambda_V, alpha_1, alpha_2, alpha_3, R_mem = y

    m_bar = max(m_bar, 1e-10)
    R_mem = max(R_mem, 0.0)

    pi2 = np.pi**2
    eta_psi = (1.0 / (6.0 * pi2)) * 3.0 * (4.0/3.0) * alpha_3
    denom = 1.0 + m_bar**2
    h2 = 1.0 / (denom**2)
    P_gen = m_bar**4

    # DIRECT memory feedback (NO saturation factor)
    memory_feedback = -MEMORY_SCALE * LAMBDA_REC_BETA * R_mem / denom

    dydt = np.zeros(7)

    # MASS
    dydt[0] = ((1.0 - eta_psi) * m_bar
               - (1.0 / pi2) * lambda_S * m_bar / denom
               + memory_feedback)

    # FOUR-FERMION
    dydt[1] = (-(2.0 + 2.0*eta_psi) * lambda_S
               + (2.0 / pi2) * h2 * (lambda_S**2 + 1.5 * lambda_S * lambda_V + 1.5 * lambda_V**2)
               + (3.0 / pi2) * alpha_3 * lambda_S)

    dydt[2] = (-(2.0 + 2.0*eta_psi) * lambda_V
               + (2.0 / pi2) * h2 * (0.5 * lambda_S**2 + 1.25 * lambda_S * lambda_V + 0.75 * lambda_V**2)
               + (3.0 / pi2) * alpha_3 * lambda_V)

    # GAUGE
    b1, b2, b3 = 41.0/6.0, -19.0/6.0, -7.0
    dydt[3] = -(b1 / (2.0 * np.pi)) * alpha_1**2
    dydt[4] = -(b2 / (2.0 * np.pi)) * alpha_2**2
    dydt[5] = -(b3 / (2.0 * np.pi)) * alpha_3**2

    # MEMORY
    dydt[6] = P_gen - R_mem

    return dydt


def initial_conditions():
    return np.array([0.01, 0.5, 0.1, (3.0/5.0) * ALPHA_GUT, ALPHA_GUT, ALPHA_GUT, 0.0])


def compute_alpha_em(alpha_1, alpha_2):
    return (3.0/8.0) * alpha_1 + (5.0/8.0) * alpha_2


def run_with_scale(scale):
    global MEMORY_SCALE
    MEMORY_SCALE = scale

    y0 = initial_conditions()
    t_eval = np.linspace(0, TAU_E, 200)

    sol = solve_ivp(
        beta_functions_direct,
        (0.0, TAU_E),
        y0,
        method='LSODA',
        t_eval=t_eval,
        rtol=1e-8,
        atol=1e-10,
        max_step=1.0
    )

    if not sol.success:
        return False, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, None

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
print("PARAMETER SWEEP")
print("="*80)

# Test much stronger scales
scales_to_test = [10.0, 50.0, 100.0, 500.0, 1000.0, 5000.0, 10000.0, 50000.0, 100000.0]

print(f"\n{'Scale':>10s} {'m̄★':>12s} {'Error %':>10s} {'α_EM^-1':>10s} {'R̄/m̄⁴':>10s} {'Status':>15s}")
print("-"*90)

best_scale = None
best_error = float('inf')
best_sol = None

for scale in scales_to_test:
    result = run_with_scale(scale)
    success, m_bar_final, error_m, alpha_em_final, error_alpha, R_mem_final, sat_ratio, sol = result

    if success:
        if abs(m_bar_final) < 1e50:  # Reasonable value
            status = "✅ OK"
            if error_m < best_error:
                best_error = error_m
                best_scale = scale
                best_sol = sol

            print(f"{scale:10.1f} {m_bar_final:12.2f} {error_m:10.2f} {1/alpha_em_final:10.3f} {sat_ratio:10.4f} {status:>15s}")
        else:
            print(f"{scale:10.1f} {m_bar_final:12.2e} {'RUNAWAY':>10s} {'N/A':>10s} {'N/A':>10s} {'❌ TOO LARGE':>15s}")
    else:
        print(f"{scale:10.1f} {'FAILED':>12s} {'N/A':>10s} {'N/A':>10s} {'N/A':>10s} {'❌ FAILED':>15s}")

print("\n" + "="*80)
if best_scale is not None:
    print(f"BEST RESULT: scale = {best_scale}, error = {best_error:.2f}%")
    print("="*80)

    # Detailed output for best
    MEMORY_SCALE = best_scale
    y0 = initial_conditions()
    t_eval = np.linspace(0, TAU_E, 200)

    sol = solve_ivp(beta_functions_direct, (0.0, TAU_E), y0, method='LSODA',
                   t_eval=t_eval, rtol=1e-8, atol=1e-10, max_step=1.0)

    m_bar = sol.y[0, :]
    R_mem = sol.y[6, :]
    m_bar_final = m_bar[-1]
    R_mem_final = R_mem[-1]
    lambda_S_final = sol.y[1, -1]
    lambda_V_final = sol.y[2, -1]
    alpha_em_final = compute_alpha_em(sol.y[3, -1], sol.y[4, -1])

    print(f"\n📊 Final values:")
    print(f"   m̄★ = {m_bar_final:.2f} (target: {M_BAR_TARGET})")
    print(f"   α_EM★ = 1/{1/alpha_em_final:.3f} (target: 1/137.036)")
    print(f"   λ̄_S★ = {lambda_S_final:.6f}")
    print(f"   λ̄_V★ = {lambda_V_final:.6f}")
    print(f"   R̄_mem★ = {R_mem_final:.2e}")

    error_m = abs(m_bar_final - M_BAR_TARGET) / M_BAR_TARGET * 100
    print(f"\n✅ Error: {error_m:.2f}%")

    if error_m < 10.0:
        print(f"\n🎉 SUCCESS! Memory stabilization working!")

    # Save
    results = {
        'best_scale': float(best_scale),
        'final_values': {
            'm_bar': float(m_bar_final),
            'error_percent': float(error_m),
            'alpha_em': float(alpha_em_final),
            'R_mem': float(R_mem_final)
        }
    }

    with open('/Users/Cristiana_1/Documents/Golden Universe/frg_direct_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ Saved: frg_direct_results.json")
else:
    print("❌ No successful convergence found")

print(f"\n" + "="*80)
print("DONE")
print("="*80)
