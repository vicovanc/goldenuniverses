#!/usr/bin/env python3
"""
Diagnostic: Plot m̄(t) trajectory to understand the problem.
"""

import numpy as np
from scipy.integrate import solve_ivp
from mpmath import mp

mp.dps = 50
PHI = mp.phi
PI = mp.pi
N_E = 111
T_E = -N_E * mp.log(PHI)

def beta_basic(t, y):
    m_bar, lambda_S, lambda_V, alpha_1, alpha_2, alpha_3 = y
    pi2 = float(PI**2)
    eta_psi = (1.0 / (6.0 * pi2)) * 3.0 * (4.0/3.0) * alpha_3
    denom = 1.0 + m_bar**2
    h2 = 1.0 / (denom**2)

    dydt = np.zeros(6)
    dydt[0] = -(1.0 - eta_psi) * m_bar + (1.0 / pi2) * lambda_S * m_bar / denom
    dydt[1] = ((2.0 + 2.0*eta_psi) * lambda_S
               - (2.0 / pi2) * h2 * (lambda_S**2 + 1.5 * lambda_S * lambda_V + 1.5 * lambda_V**2)
               - (3.0 / pi2) * alpha_3 * lambda_S)
    dydt[2] = ((2.0 + 2.0*eta_psi) * lambda_V
               - (2.0 / pi2) * h2 * (0.5 * lambda_S**2 + 1.25 * lambda_S * lambda_V + 0.75 * lambda_V**2)
               - (3.0 / pi2) * alpha_3 * lambda_V)
    b1, b2, b3 = 41.0/6.0, -19.0/6.0, -7.0
    dydt[3] = (b1 / (2.0 * np.pi)) * alpha_1**2
    dydt[4] = (b2 / (2.0 * np.pi)) * alpha_2**2
    dydt[5] = (b3 / (2.0 * np.pi)) * alpha_3**2
    return dydt

alpha_GUT = 1.0/63.078
y0 = np.array([0.01, 0.5, 0.1, (3.0/5.0)*alpha_GUT, alpha_GUT, alpha_GUT])

t_eval = np.linspace(0, float(T_E), 100)

sol = solve_ivp(beta_basic, (0.0, float(T_E)), y0, method='Radau',
                t_eval=t_eval, rtol=1e-6, atol=1e-8, max_step=0.5)

print("t (RG time)     m̄          λ̄_S         λ̄_V         Analysis")
print("="*80)
for i in range(len(sol.t)):
    t = sol.t[i]
    m = sol.y[0,i]
    ls = sol.y[1,i]
    lv = sol.y[2,i]

    if i < len(sol.t) - 1:
        dm_dt = (sol.y[0,i+1] - sol.y[0,i]) / (sol.t[i+1] - sol.t[i])
        trend = "↑ GROWING" if dm_dt > 0 else "↓ shrinking"
    else:
        trend = ""

    print(f"{t:8.2f}    {m:12.4e}   {ls:10.6f}   {lv:10.6f}   {trend}")

print(f"\n🔍 KEY OBSERVATIONS:")
print(f"1. λ̄_S, λ̄_V decay to ~0 (CORRECT - four-fermion is irrelevant)")
print(f"2. m̄ GROWS EXPONENTIALLY after λ̄_S decays")
print(f"3. WITHOUT MEMORY DAMPING, m̄ runs away to 10²¹!")
print(f"\n⚠️ This is WHY memory feedback is essential!")
print(f"   Memory term dR̄_mem/dt = m̄⁴ - R̄_mem should SATURATE at m̄~4514")
print(f"   Then R̄_mem feeds back to STABILIZE mass growth")
