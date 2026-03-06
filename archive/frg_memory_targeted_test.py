#!/usr/bin/env python3
"""
TARGETED TEST OF MEMORY FEEDBACK
==================================

Based on equilibrium analysis:
- Form: -λ R̄/(1+m̄²)
- At equilibrium: m̄★ = 1/λ_eff
- For m̄★ = 4514: λ_eff = 1/4514 ≈ 2.2×10⁻⁴
- Scale factor: 2.2×10⁻⁴ / 0.51 ≈ 4×10⁻⁴

Test scales around this value.
"""

import numpy as np
from scipy.integrate import solve_ivp
from mpmath import mp

mp.dps = 50

PHI = mp.phi
PI = mp.pi
N_E = 111
TAU_E = float(N_E * mp.log(PHI))
LAMBDA_REC_BETA_BASE = float(mp.exp(PHI) / PI**2)  # ≈ 0.51
ALPHA_GUT = 1.0 / 63.078
M_BAR_TARGET = 4514.0

# Predicted scale
lambda_eff_predicted = 1.0 / M_BAR_TARGET
scale_predicted = lambda_eff_predicted / LAMBDA_REC_BETA_BASE

print("="*80)
print("TARGETED MEMORY COUPLING TEST")
print("="*80)
print(f"\n🎯 Target: m̄★ = {M_BAR_TARGET}")
print(f"📐 Equilibrium analysis:")
print(f"   For m̄★ = 1/λ_eff → λ_eff = {lambda_eff_predicted:.6e}")
print(f"   Scale = λ_eff / base = {scale_predicted:.6e}")
print(f"\nTesting scales around {scale_predicted:.2e}...\n")


def beta_functions(tau, y, scale):
    m_bar, lambda_S, lambda_V, alpha_1, alpha_2, alpha_3, R_mem = y

    m_bar = max(m_bar, 1e-10)
    R_mem = max(R_mem, 0.0)

    pi2 = np.pi**2
    eta_psi = (1.0 / (6.0 * pi2)) * 3.0 * (4.0/3.0) * alpha_3
    denom = 1.0 + m_bar**2
    h2 = 1.0 / (denom**2)
    P_gen = m_bar**4
    lambda_eff = scale * LAMBDA_REC_BETA_BASE

    # Memory feedback: -λ R̄/(1+m̄²)
    memory_feedback = -lambda_eff * R_mem / denom

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


def run_test(scale):
    y0 = initial_conditions()

    try:
        sol = solve_ivp(
            lambda t, y: beta_functions(t, y, scale),
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

            # Check validity
            if m_bar_final > 0 and not np.isnan(m_bar_final) and not np.isinf(m_bar_final):
                alpha_em = (3.0/8.0) * alpha_1_final + (5.0/8.0) * alpha_2_final
                error_m = abs(m_bar_final - M_BAR_TARGET) / M_BAR_TARGET * 100
                error_alpha = abs(1/alpha_em - 137.036) / 137.036 * 100
                sat = R_mem_final / (m_bar_final**4 + 1e-100)

                return {
                    'success': True,
                    'm_bar': m_bar_final,
                    'R_mem': R_mem_final,
                    'alpha_em': alpha_em,
                    'error_m': error_m,
                    'error_alpha': error_alpha,
                    'sat': sat
                }

        return {'success': False}

    except:
        return {'success': False}


# Test scales around predicted value
test_scales = [
    scale_predicted * 0.1,
    scale_predicted * 0.5,
    scale_predicted * 1.0,
    scale_predicted * 2.0,
    scale_predicted * 5.0,
    scale_predicted * 10.0
]

print(f"{'Scale':>15s} {'λ_eff':>15s} {'m̄★':>12s} {'Error%':>10s} {'α_EM':>12s} {'Status':>15s}")
print("-"*80)

best = None
best_error = float('inf')

for scale in test_scales:
    result = run_test(scale)

    if result['success']:
        m = result['m_bar']
        err_m = result['error_m']
        err_a = result['error_alpha']
        alpha_em = result['alpha_em']
        lambda_eff = scale * LAMBDA_REC_BETA_BASE

        status = "✅ CLOSE!" if err_m < 15 else ("Target" if err_m < 50 else "Far")

        print(f"{scale:15.6e} {lambda_eff:15.6e} {m:12.2f} {err_m:10.2f} 1/{1/alpha_em:>10.2f} {status:>15s}")

        if err_m < best_error:
            best_error = err_m
            best = {'scale': scale, **result}
    else:
        print(f"{scale:15.6e} {'---':>15s} {'FAILED':>12s} {'---':>10s} {'---':>12s} {'---':>15s}")

if best and best_error < 20:
    print(f"\n" + "="*80)
    print("🎉 SUCCESS!")
    print("="*80)
    print(f"\n📊 Optimal parameters:")
    print(f"   Scale factor: {best['scale']:.6e}")
    print(f"   λ_eff: {best['scale'] * LAMBDA_REC_BETA_BASE:.6e}")
    print(f"\n📊 Final values:")
    print(f"   m̄★ = {best['m_bar']:.2f} (error: {best['error_m']:.2f}%)")
    print(f"   α_EM★ = 1/{1/best['alpha_em']:.3f} (error: {best['error_alpha']:.2f}%)")
    print(f"   R̄_mem★ = {best['R_mem']:.2e} (saturation: {best['sat']:.4f})")
elif best:
    print(f"\n⚠️ Best error: {best_error:.2f}% - needs fine-tuning")
else:
    print(f"\n❌ ALL TESTS FAILED")

print("\n" + "="*80)
