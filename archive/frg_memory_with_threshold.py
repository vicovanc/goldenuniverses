#!/usr/bin/env python3
"""
FRG WITH THRESHOLD-ACTIVATED MEMORY
====================================

Key insight: Memory feedback should only activate once R̄_mem has built up.

Strategy: Use smooth threshold function to gradually turn on memory damping.
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
print("FRG WITH THRESHOLD-ACTIVATED MEMORY FEEDBACK")
print("="*80)


def beta_functions_threshold(tau, y, memory_scale, threshold_tau):
    """
    Memory feedback activates smoothly after τ > threshold.

    activation(τ) = 1/(1 + exp(-k(τ - threshold)))
    """
    m_bar, lambda_S, lambda_V, alpha_1, alpha_2, alpha_3, R_mem = y

    m_bar = max(m_bar, 1e-10)
    R_mem = max(R_mem, 0.0)

    pi2 = np.pi**2
    eta_psi = (1.0 / (6.0 * pi2)) * 3.0 * (4.0/3.0) * alpha_3
    denom = 1.0 + m_bar**2
    h2 = 1.0 / (denom**2)
    P_gen = m_bar**4
    lambda_eff = memory_scale * LAMBDA_REC_BETA_BASE

    # Smooth activation function
    k = 0.2  # Steepness
    activation = 1.0 / (1.0 + np.exp(-k * (tau - threshold_tau)))

    # Memory feedback (negative for damping, modulated by activation)
    memory_feedback = -activation * lambda_eff * R_mem / denom

    dydt = np.zeros(7)

    dydt[0] = (+(1.0 - eta_psi) * m_bar
               - (1.0 / pi2) * lambda_S * m_bar / denom
               + memory_feedback)

    dydt[1] = (-(2.0 + 2.0*eta_psi) * lambda_S
               + (2.0 / pi2) * h2 * (lambda_S**2 + 1.5 * lambda_S * lambda_V + 1.5 * lambda_V**2)
               + (3.0 / pi2) * alpha_3 * lambda_S)

    dydt[2] = (-(2.0 + 2.0*eta_psi) * lambda_V
               + (2.0 / pi2) * h2 * (0.5 * lambda_S**2 + 1.25 * lambda_S * lambda_V + 0.75 * lambda_V**2)
               + (3.0 / pi2) * alpha_3 * lambda_V)

    b1, b2, b3 = 41.0/6.0, -19.0/6.0, -7.0
    dydt[3] = -(b1 / (2.0 * np.pi)) * alpha_1**2
    dydt[4] = -(b2 / (2.0 * np.pi)) * alpha_2**2
    dydt[5] = -(b3 / (2.0 * np.pi)) * alpha_3**2

    dydt[6] = P_gen - R_mem

    return dydt


def initial_conditions():
    return np.array([0.01, 0.5, 0.1, (3.0/5.0) * ALPHA_GUT, ALPHA_GUT, ALPHA_GUT, 0.0])


def run_test(memory_scale, threshold_tau):
    y0 = initial_conditions()

    try:
        sol = solve_ivp(
            lambda t, y: beta_functions_threshold(t, y, memory_scale, threshold_tau),
            (0.0, TAU_E),
            y0,
            method='LSODA',
            rtol=1e-8,
            atol=1e-10,
            max_step=1.0
        )

        if sol.success:
            m_bar_final = sol.y[0, -1]
            R_mem_final = sol.y[6, -1]
            alpha_1_final = sol.y[3, -1]
            alpha_2_final = sol.y[4, -1]

            if m_bar_final > 0 and not np.isnan(m_bar_final) and not np.isinf(m_bar_final):
                alpha_em = (3.0/8.0) * alpha_1_final + (5.0/8.0) * alpha_2_final
                error_m = abs(m_bar_final - M_BAR_TARGET) / M_BAR_TARGET * 100
                sat = R_mem_final / (m_bar_final**4 + 1e-100)

                return {
                    'success': True,
                    'm_bar': m_bar_final,
                    'R_mem': R_mem_final,
                    'alpha_em': alpha_em,
                    'error_m': error_m,
                    'sat': sat
                }

        return {'success': False}

    except:
        return {'success': False}


# Test various thresholds and scales
print(f"\nTesting threshold activation strategy...")
print(f"(Memory feedback only activates after τ > threshold)\n")

print(f"{'Scale':>12s} {'Threshold':>12s} {'m̄★':>12s} {'Error%':>10s} {'Status':>15s}")
print("-"*65)

# Try different activation times
thresholds = [10.0, 20.0, 30.0, 40.0]
scales = [0.001, 0.01, 0.1, 1.0, 10.0]

best = None
best_error = float('inf')

for threshold in thresholds:
    for scale in scales:
        result = run_test(scale, threshold)

        if result['success']:
            m = result['m_bar']
            err = result['error_m']

            status = "✅ TARGET!" if err < 10 else ("Close" if err < 30 else "Far")

            print(f"{scale:12.3f} {threshold:12.1f} {m:12.2f} {err:10.2f} {status:>15s}")

            if err < best_error:
                best_error = err
                best = {'scale': scale, 'threshold': threshold, **result}
        else:
            print(f"{scale:12.3f} {threshold:12.1f} {'FAILED':>12s} {'---':>10s} {'---':>15s}")

if best and best_error < 20:
    print(f"\n" + "="*80)
    print("🎉 SUCCESS!")
    print("="*80)
    print(f"\n📊 Optimal parameters:")
    print(f"   Memory scale: {best['scale']:.3f}")
    print(f"   Activation threshold: τ > {best['threshold']:.1f}")
    print(f"\n📊 Final values:")
    print(f"   m̄★ = {best['m_bar']:.2f} (error: {best['error_m']:.2f}%)")
    print(f"   α_EM★ = 1/{1/best['alpha_em']:.3f}")
    print(f"   R̄_mem★ = {best['R_mem']:.2e} (saturation: {best['sat']:.4f})")
elif best:
    print(f"\n⚠️ Best error: {best_error:.2f}% with scale={best['scale']:.3f}, threshold={best['threshold']:.1f}")
    print(f"   m̄★ = {best['m_bar']:.2f}")
else:
    print(f"\n❌ ALL TESTS FAILED")

print("\n" + "="*80)
