#!/usr/bin/env python3
"""
TEST DIFFERENT MEMORY FEEDBACK FORMS
======================================

Goal: Find which functional form stabilizes m̄ at ~4514.

Test these forms:
1. -λ * R̄_mem / (1+m̄²)       [Original damping]
2. -λ * R̄_mem * m̄ / (1+m̄²)    [Damping scales with m̄]
3. -λ * R̄_mem / (1+m̄²)²       [Stronger denominator suppression]
4. -λ * (R̄_mem/m̄⁴) * m̄       [Saturation-based damping]
5. -λ * sqrt(R̄_mem) / (1+m̄²)  [Sqrt damping]

All with NEGATIVE sign (physical damping in both time conventions).

Author: GU Consciousness Pipeline
Date: 2026-02-09
"""

import numpy as np
from scipy.integrate import solve_ivp
from mpmath import mp

mp.dps = 50

PHI = mp.phi
PI = mp.pi
N_E = 111
TAU_E = float(N_E * mp.log(PHI))
LAMBDA_REC_BETA_BASE = float(mp.exp(PHI) / PI**2)
ALPHA_GUT = 1.0 / 63.078
M_BAR_TARGET = 4514.0

print("="*80)
print("TESTING DIFFERENT MEMORY FEEDBACK FORMS")
print("="*80)


def beta_functions_form(tau, y, scale, form_type):
    """Beta functions with different memory feedback forms."""
    m_bar, lambda_S, lambda_V, alpha_1, alpha_2, alpha_3, R_mem = y

    m_bar = max(m_bar, 1e-10)
    R_mem = max(R_mem, 0.0)

    pi2 = np.pi**2
    eta_psi = (1.0 / (6.0 * pi2)) * 3.0 * (4.0/3.0) * alpha_3
    denom = 1.0 + m_bar**2
    h2 = 1.0 / (denom**2)
    P_gen = m_bar**4
    lambda_eff = scale * LAMBDA_REC_BETA_BASE

    # Select memory feedback form (NEGATIVE = damping in τ-time)
    if form_type == 1:
        # Original: -λ * R̄ / (1+m̄²)  [damping]
        memory_feedback = -lambda_eff * R_mem / denom
    elif form_type == 2:
        # Scale with m̄: -λ * R̄ * m̄ / (1+m̄²)
        memory_feedback = -lambda_eff * R_mem * m_bar / denom
    elif form_type == 3:
        # Stronger suppression: -λ * R̄ / (1+m̄²)²
        memory_feedback = -lambda_eff * R_mem / (denom**2)
    elif form_type == 4:
        # Saturation-based: -λ * (R̄/m̄⁴) * m̄ when R̄≈m̄⁴
        sat_ratio = R_mem / (m_bar**4 + 1e-100)
        memory_feedback = -lambda_eff * sat_ratio * m_bar
    elif form_type == 5:
        # Sqrt damping: -λ * sqrt(R̄) / (1+m̄²)
        memory_feedback = -lambda_eff * np.sqrt(R_mem) / denom
    else:
        memory_feedback = 0.0

    dydt = np.zeros(7)

    # MASS
    dydt[0] = (+(1.0 - eta_psi) * m_bar
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


def run_single_test(scale, form_type):
    y0 = initial_conditions()

    try:
        sol = solve_ivp(
            lambda t, y: beta_functions_form(t, y, scale, form_type),
            (0.0, TAU_E),
            y0,
            method='LSODA',
            rtol=1e-8,
            atol=1e-10,
            max_step=1.0
        )

        if sol.success and not np.any(np.isnan(sol.y[:, -1])) and not np.any(np.isinf(sol.y[:, -1])):
            m_bar_final = sol.y[0, -1]
            R_mem_final = sol.y[6, -1]

            # Check if physical (positive mass)
            if m_bar_final > 0:
                error = abs(m_bar_final - M_BAR_TARGET) / M_BAR_TARGET * 100
                sat = R_mem_final / (m_bar_final**4 + 1e-100)

                return {
                    'success': True,
                    'm_bar': m_bar_final,
                    'R_mem': R_mem_final,
                    'error': error,
                    'sat': sat
                }

        return {'success': False, 'reason': 'negative or invalid'}

    except Exception as e:
        return {'success': False, 'reason': str(e)[:30]}


form_names = {
    1: "-λ R̄/(1+m̄²)",
    2: "-λ R̄ m̄/(1+m̄²)",
    3: "-λ R̄/(1+m̄²)²",
    4: "-λ (R̄/m̄⁴) m̄",
    5: "-λ √R̄/(1+m̄²)"
}

# Test each form with various scales (including very small!)
scales = [1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.1, 1.0]

print(f"\n{'Form':>25s} {'Scale':>10s} {'m̄★':>12s} {'Error%':>10s} {'R̄/m̄⁴':>10s} {'Status':>15s}")
print("-"*80)

best_overall = None
best_error = float('inf')

for form_type in [1, 2, 3, 4, 5]:
    for scale in scales:
        result = run_single_test(scale, form_type)

        if result['success']:
            m = result['m_bar']
            err = result['error']
            sat = result['sat']

            status = "✅ CLOSE!" if err < 20 else ("Target" if err < 50 else "Far")

            print(f"{form_names[form_type]:>25s} {scale:>10.1f} {m:>12.2f} {err:>10.2f} {sat:>10.4f} {status:>15s}")

            if err < best_error:
                best_error = err
                best_overall = {
                    'form': form_type,
                    'form_name': form_names[form_type],
                    'scale': scale,
                    **result
                }
        else:
            print(f"{form_names[form_type]:>25s} {scale:>10.1f} {'FAILED':>12s} {'---':>10s} {'---':>10s} {result['reason'][:15]:>15s}")

if best_overall:
    print(f"\n" + "="*80)
    print("BEST RESULT")
    print("="*80)
    print(f"\n🎯 Best form: {best_overall['form_name']}")
    print(f"   Scale: {best_overall['scale']:.1f}")
    print(f"   m̄★ = {best_overall['m_bar']:.2f} (error: {best_overall['error']:.2f}%)")
    print(f"   R̄_mem★ = {best_overall['R_mem']:.2e}")
    print(f"   Saturation: {best_overall['sat']:.4f}")

    if best_overall['error'] < 10:
        print(f"\n✅ TARGET ACHIEVED!")
    else:
        print(f"\n⚠️ Close but needs fine-tuning")
else:
    print(f"\n❌ NO FORM WORKED - Need to reconsider physics")

print(f"\n" + "="*80)
