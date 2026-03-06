#!/usr/bin/env python3
"""
BASIC FRG CHECK WITHOUT MEMORY
================================

Verify the basic FRG setup works before adding memory.
"""

import numpy as np
from scipy.integrate import solve_ivp
from mpmath import mp

mp.dps = 50

PHI = mp.phi
PI = mp.pi
N_E = 111
TAU_E = float(N_E * mp.log(PHI))
ALPHA_GUT = 1.0 / 63.078

print("="*80)
print("BASIC FRG TEST (NO MEMORY)")
print("="*80)


def beta_functions_no_memory(tau, y):
    m_bar, lambda_S, lambda_V, alpha_1, alpha_2, alpha_3 = y

    m_bar = max(m_bar, 1e-10)

    pi2 = np.pi**2
    eta_psi = (1.0 / (6.0 * pi2)) * 3.0 * (4.0/3.0) * alpha_3
    denom = 1.0 + m_bar**2
    h2 = 1.0 / (denom**2)

    dydt = np.zeros(6)

    # MASS (no memory)
    dydt[0] = (+(1.0 - eta_psi) * m_bar
               - (1.0 / pi2) * lambda_S * m_bar / denom)

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

    return dydt


y0 = np.array([0.01, 0.5, 0.1, (3.0/5.0) * ALPHA_GUT, ALPHA_GUT, ALPHA_GUT])

print(f"\n📍 Initial: m̄₀={y0[0]}, λ̄_S₀={y0[1]}, λ̄_V₀={y0[2]}")
print(f"\n🔄 Integrating τ: [0, {TAU_E:.2f}]...")

sol = solve_ivp(
    beta_functions_no_memory,
    (0.0, TAU_E),
    y0,
    method='LSODA',
    rtol=1e-8,
    atol=1e-10
)

if sol.success:
    m_final = sol.y[0, -1]
    lambda_S_final = sol.y[1, -1]
    lambda_V_final = sol.y[2, -1]
    alpha_1_final = sol.y[3, -1]
    alpha_2_final = sol.y[4, -1]

    alpha_em = (3.0/8.0) * alpha_1_final + (5.0/8.0) * alpha_2_final

    print(f"\n✅ SUCCESS")
    print(f"\n📊 Final values:")
    print(f"   m̄★ = {m_final:.2e}")
    print(f"   λ̄_S★ = {lambda_S_final:.6e}")
    print(f"   λ̄_V★ = {lambda_V_final:.6e}")
    print(f"   α_EM★ = 1/{1/alpha_em:.3f}")

    # Show trajectory
    print(f"\n📈 Trajectory sample:")
    print(f"{'τ':>10s} {'m̄':>15s} {'λ̄_S':>15s} {'λ̄_V':>15s}")
    print("-"*55)
    for i in [0, len(sol.t)//4, len(sol.t)//2, 3*len(sol.t)//4, -1]:
        tau = sol.t[i]
        m = sol.y[0, i]
        lS = sol.y[1, i]
        lV = sol.y[2, i]
        print(f"{tau:10.2f} {m:15.2e} {lS:15.2e} {lV:15.2e}")

    print(f"\n💡 Analysis:")
    print(f"   WITHOUT memory: m̄ grows to {m_final:.2e}")
    print(f"   This demonstrates the runaway problem!")
    print(f"   Four-fermion couplings: λ̄_S={lambda_S_final:.2e}, λ̄_V={lambda_V_final:.2e}")

else:
    print(f"\n❌ FAILED: {sol.message}")

print("\n" + "="*80)
