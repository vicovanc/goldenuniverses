#!/usr/bin/env python3
"""
CORRECTED FRG WITH MEMORY - PROPER DAMPING SIGN
"""

import numpy as np
from scipy.integrate import solve_ivp
from mpmath import mp

mp.dps = 50
PHI = mp.phi
PI = mp.pi
N_E = 111
T_E = -N_E * mp.log(PHI)
LAMBDA_REC_BETA = mp.exp(PHI) / PI**2

print("="*80)
print("FRG WITH MEMORY - CORRECTED DAMPING SIGN")
print("="*80)
print(f"λ_rec/β = {float(LAMBDA_REC_BETA):.5f}")
print(f"Target: m̄★ = 4514 at t_e = {float(T_E):.2f}")

def beta_with_memory(t, y):
    """Beta functions WITH memory damping (corrected sign)."""
    m_bar, lambda_S, lambda_V, alpha_1, alpha_2, alpha_3, R_mem = y

    pi2 = float(PI**2)
    eta_psi = (1.0 / (6.0 * pi2)) * 3.0 * (4.0/3.0) * alpha_3
    denom = 1.0 + m_bar**2
    h2 = 1.0 / (denom**2)
    lambda_rec_beta = float(LAMBDA_REC_BETA)

    # Memory generation
    P_gen = m_bar**4

    dydt = np.zeros(7)

    # MASS - WITH MEMORY DAMPING (NEGATIVE SIGN!)
    # Memory provides binding → resists growth
    dydt[0] = (-(1.0 - eta_psi) * m_bar
               + (1.0 / pi2) * lambda_S * m_bar / denom
               - lambda_rec_beta * R_mem / denom)  # ← DAMPING!

    # Four-fermion (with memory)
    dydt[1] = ((2.0 + 2.0*eta_psi) * lambda_S
               - (2.0 / pi2) * h2 * (lambda_S**2 + 1.5 * lambda_S * lambda_V + 1.5 * lambda_V**2)
               - (3.0 / pi2) * alpha_3 * lambda_S
               - lambda_rec_beta * R_mem * lambda_S)

    dydt[2] = ((2.0 + 2.0*eta_psi) * lambda_V
               - (2.0 / pi2) * h2 * (0.5 * lambda_S**2 + 1.25 * lambda_S * lambda_V + 0.75 * lambda_V**2)
               - (3.0 / pi2) * alpha_3 * lambda_V
               - lambda_rec_beta * R_mem * lambda_V)

    # Gauge
    b1, b2, b3 = 41.0/6.0, -19.0/6.0, -7.0
    dydt[3] = (b1 / (2.0 * np.pi)) * alpha_1**2
    dydt[4] = (b2 / (2.0 * np.pi)) * alpha_2**2
    dydt[5] = (b3 / (2.0 * np.pi)) * alpha_3**2

    # MEMORY ACCUMULATOR
    dydt[6] = P_gen - R_mem

    return dydt

# Initial conditions
alpha_GUT = 1.0/63.078
y0 = np.array([
    0.01,  # m_bar
    0.5,   # lambda_S
    0.1,   # lambda_V
    (3.0/5.0) * alpha_GUT,
    alpha_GUT,
    alpha_GUT,
    0.0    # R_mem (starts at zero)
])

print(f"\nInitial: m̄={y0[0]}, λ̄_S={y0[1]}, R̄_mem={y0[6]}")

# Test different time points
test_points = [float(T_E)/10, float(T_E)/5, float(T_E)/2, float(T_E)]

for t_test in test_points:
    sol = solve_ivp(
        beta_with_memory,
        (0.0, t_test),
        y0,
        method='Radau',
        rtol=1e-6,
        atol=1e-8,
        max_step=0.5
    )

    if sol.success:
        m_final = sol.y[0, -1]
        R_final = sol.y[6, -1]
        sat_ratio = R_final / (m_final**4 + 1e-100)
        print(f"\n✅ t = {t_test:7.2f}: m̄ = {m_final:12.2e}, R̄_mem = {R_final:12.2e}, sat={sat_ratio:.4f}")
    else:
        print(f"\n❌ t = {t_test:7.2f}: FAILED - {sol.message}")

# Full run with detailed output
print(f"\n{'='*80}")
print("FULL RUN TO ELECTRON EPOCH")
print(f"{'='*80}")

t_eval = np.linspace(0, float(T_E), 100)

sol_full = solve_ivp(
    beta_with_memory,
    (0.0, float(T_E)),
    y0,
    method='Radau',
    t_eval=t_eval,
    rtol=1e-6,
    atol=1e-8,
    max_step=0.5
)

if sol_full.success:
    print(f"\n✅ INTEGRATION SUCCESS!")

    m_traj = sol_full.y[0, :]
    R_traj = sol_full.y[6, :]

    print(f"\nKey trajectory points:")
    print(f"{'t':>10s} {'m̄':>15s} {'R̄_mem':>15s} {'R̄/m̄⁴':>10s}")
    print("="*60)

    indices = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, -1]
    for i in indices:
        t = sol_full.t[i]
        m = m_traj[i]
        R = R_traj[i]
        sat = R / (m**4 + 1e-100)
        print(f"{t:10.2f} {m:15.4e} {R:15.4e} {sat:10.4f}")

    m_final = m_traj[-1]
    R_final = R_traj[-1]

    print(f"\n🎯 FINAL RESULT:")
    print(f"   m̄★ = {m_final:.2f}")
    print(f"   Target: {4514}")
    print(f"   Error: {np.abs(m_final - 4514)/4514*100:.2f}%")
    print(f"\n   R̄_mem★ = {R_final:.2e}")
    print(f"   Saturation: R̄/m̄⁴ = {R_final/(m_final**4 + 1e-100):.4f}")

    if np.abs(m_final - 4514) / 4514 < 0.05:
        print(f"\n🎉 SUCCESS: m̄★ within 5% of target!")
    elif m_final < 1e10:
        print(f"\n⚠️ PARTIAL: Memory damping prevents runaway, but needs tuning")
    else:
        print(f"\n❌ FAILURE: Mass still runs away despite memory")

else:
    print(f"\n❌ INTEGRATION FAILED: {sol_full.message}")
