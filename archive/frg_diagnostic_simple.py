#!/usr/bin/env python3
"""
Diagnostic: Test FRG beta functions WITHOUT memory first.
"""

import numpy as np
from scipy.integrate import solve_ivp
from mpmath import mp

mp.dps = 50
PHI = mp.phi
PI = mp.pi
N_E = 111
T_E = -N_E * mp.log(PHI)  # ≈ -53.4

print("Testing BASIC FRG (no memory yet)...")
print(f"t_e = {float(T_E):.4f}")

def beta_basic(t, y):
    """Beta functions WITHOUT memory."""
    m_bar, lambda_S, lambda_V, alpha_1, alpha_2, alpha_3 = y

    pi2 = float(PI**2)

    # Anomalous dimension
    eta_psi = (1.0 / (6.0 * pi2)) * 3.0 * (4.0/3.0) * alpha_3

    # Denominator
    denom = 1.0 + m_bar**2
    h2 = 1.0 / (denom**2)

    dydt = np.zeros(6)

    # Mass (NO memory)
    dydt[0] = -(1.0 - eta_psi) * m_bar + (1.0 / pi2) * lambda_S * m_bar / denom

    # Scalar four-fermion
    dydt[1] = ((2.0 + 2.0*eta_psi) * lambda_S
               - (2.0 / pi2) * h2 * (lambda_S**2 + 1.5 * lambda_S * lambda_V + 1.5 * lambda_V**2)
               - (3.0 / pi2) * alpha_3 * lambda_S)

    # Vector four-fermion
    dydt[2] = ((2.0 + 2.0*eta_psi) * lambda_V
               - (2.0 / pi2) * h2 * (0.5 * lambda_S**2 + 1.25 * lambda_S * lambda_V + 0.75 * lambda_V**2)
               - (3.0 / pi2) * alpha_3 * lambda_V)

    # Gauge
    b1 = 41.0 / 6.0
    b2 = -19.0 / 6.0
    b3 = -7.0

    dydt[3] = (b1 / (2.0 * np.pi)) * alpha_1**2
    dydt[4] = (b2 / (2.0 * np.pi)) * alpha_2**2
    dydt[5] = (b3 / (2.0 * np.pi)) * alpha_3**2

    return dydt

# Initial conditions
alpha_GUT = 1.0/63.078
y0 = np.array([
    0.01,  # m_bar
    0.5,   # lambda_S
    0.1,   # lambda_V
    (3.0/5.0) * alpha_GUT,  # alpha_1
    alpha_GUT,               # alpha_2
    alpha_GUT                # alpha_3
])

print(f"\nInitial: m̄={y0[0]}, λ̄_S={y0[1]}, λ̄_V={y0[2]}")
print(f"         α₁={y0[3]:.6f}, α₂={y0[4]:.6f}, α₃={y0[5]:.6f}")

# Try short integration first
t_short = float(T_E) / 10  # Just 10% of the way

print(f"\nTrying short integration to t={t_short:.4f}...")

sol = solve_ivp(
    beta_basic,
    (0.0, t_short),
    y0,
    method='Radau',
    dense_output=True,
    rtol=1e-6,
    atol=1e-8,
    max_step=0.5
)

if sol.success:
    print(f"✅ Short integration SUCCESS!")
    print(f"   Final: m̄={sol.y[0,-1]:.4f}, λ̄_S={sol.y[1,-1]:.4f}, λ̄_V={sol.y[2,-1]:.4f}")

    # Now try full integration
    print(f"\nTrying FULL integration to t_e={float(T_E):.4f}...")

    sol_full = solve_ivp(
        beta_basic,
        (0.0, float(T_E)),
        y0,
        method='Radau',
        dense_output=True,
        rtol=1e-6,
        atol=1e-8,
        max_step=0.5
    )

    if sol_full.success:
        print(f"✅ FULL integration SUCCESS!")
        m_bar_final = sol_full.y[0, -1]
        print(f"   Final: m̄★ = {m_bar_final:.2f}")
        print(f"   Target: m̄★ = 4514")
        print(f"   Ratio: {m_bar_final / 4514:.4f}")
    else:
        print(f"❌ FULL integration FAILED: {sol_full.message}")
        print(f"   Stopped at t={sol_full.t[-1]:.4f}")
        print(f"   Last m̄={sol_full.y[0,-1]:.4e}")
else:
    print(f"❌ Short integration FAILED: {sol.message}")
