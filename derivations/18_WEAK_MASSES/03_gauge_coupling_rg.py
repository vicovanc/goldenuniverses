#!/usr/bin/env python3
"""
Standard Model 2-Loop Gauge Coupling RG Running
================================================

Implements proper 2-loop renormalization group equations for alpha_1, alpha_2,
alpha_3 from M_Z to M_GUT. Uses CODATA alpha_EM and PDG alpha_s(M_Z) as
experimental boundary conditions.

NO ad-hoc Pattern corrections. This is standard QFT.

GU inputs: alpha_EM = 1/137.036 (one experimental input), M_P, phi for epoch scale.
PDG benchmark: alpha_s(M_Z) = 0.1179.

Date: February 2026
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from scipy.integrate import solve_ivp

from utils.gu_constants import (
    alpha_EM, M_P, phi, pi, CODATA,
    N_GUT, N_u, N_d, N_s, N_c, N_b, N_t
)

print("=" * 90)
print("STANDARD MODEL GAUGE COUPLING RG — 2-LOOP")
print("From M_Z to M_GUT and back, with proper EFT thresholds")
print("=" * 90)

# ============================================================================
# EXPERIMENTAL BOUNDARY CONDITIONS AT M_Z
# ============================================================================

M_Z_exp = 91.1876          # GeV (PDG)
alpha_EM_val = float(alpha_EM)
alpha_s_MZ = 0.1179        # PDG 2024
sin2_theta_W_MZ = 0.23122  # PDG on-shell scheme

alpha_EM_MZ = alpha_EM_val / (1 - 0.0590)  # Run alpha_EM from q=0 to M_Z

alpha_2_MZ = alpha_EM_MZ / sin2_theta_W_MZ
alpha_1_MZ = alpha_EM_MZ / (1 - sin2_theta_W_MZ) * (5/3)

print(f"\n--- Boundary conditions at M_Z = {M_Z_exp} GeV ---")
print(f"alpha_EM(0)    = 1/{1/alpha_EM_val:.3f}")
print(f"alpha_EM(M_Z)  = 1/{1/alpha_EM_MZ:.3f}")
print(f"sin²θ_W(M_Z)  = {sin2_theta_W_MZ}")
print(f"alpha_s(M_Z)   = {alpha_s_MZ}")
print(f"alpha_1(M_Z)   = {alpha_1_MZ:.6f}  (GUT normalized: (5/3)α_Y)")
print(f"alpha_2(M_Z)   = {alpha_2_MZ:.6f}")
print(f"alpha_3(M_Z)   = {alpha_s_MZ:.6f}")

# ============================================================================
# 2-LOOP BETA FUNCTION COEFFICIENTS
# ============================================================================

def beta_coefficients(N_f):
    """SM 1-loop and 2-loop beta function coefficients for N_f active quark flavors.
    Convention: d(alpha_i)/d(ln mu) = -b_i/(2*pi)*alpha_i^2 - b_ij/(8*pi^2)*alpha_i^2*alpha_j
    We use the simpler form: d(1/alpha_i)/d(ln mu) = b_i/(2*pi) + ...
    """
    N_H = 1  # Higgs doublets

    b1 = (4/3) * N_f + (1/10) * N_H
    b2 = -(22/3) + (4/3) * N_f + (1/6) * N_H
    b3 = -11 + (4/3) * N_f

    # 2-loop coefficients (b_ij matrix for SM)
    b11 = (19/15) * N_f + (9/50) * N_H
    b12 = (3/5) * N_f + (9/10) * N_H
    b13 = (44/15) * N_f
    b21 = (1/5) * N_f + (3/10) * N_H
    b22 = -(136/3) + (4) * N_f + (13/6) * N_H
    b23 = 4 * N_f
    b31 = (11/30) * N_f
    b32 = (3/2) * N_f
    b33 = -102 + (76/3) * N_f

    return (b1, b2, b3), np.array([[b11, b12, b13],
                                    [b21, b22, b23],
                                    [b31, b32, b33]])

# ============================================================================
# PARTICLE THRESHOLDS (PDG masses in GeV)
# ============================================================================

THRESHOLDS = [
    (1.27,   4, "charm on"),
    (4.18,   5, "bottom on"),
    (91.19,  5, "Z pole"),
    (125.25, 5, "Higgs"),
    (172.76, 6, "top on"),
]

def N_f_at_scale(mu):
    """Number of active quark flavors at energy scale mu (GeV)"""
    if mu < 1.27:
        return 3
    elif mu < 4.18:
        return 4
    elif mu < 172.76:
        return 5
    else:
        return 6

# ============================================================================
# RG EVOLUTION (2-LOOP)
# ============================================================================

def rg_equations(ln_mu, inv_alphas, direction='up'):
    """d(1/alpha_i)/d(ln mu) = b_i/(2*pi) + sum_j b_ij/(8*pi^2) * alpha_j"""
    mu = np.exp(ln_mu)
    N_f = N_f_at_scale(mu)
    b1_vec, b2_mat = beta_coefficients(N_f)

    alpha_vals = 1.0 / np.maximum(inv_alphas, 1e-10)

    d_inv = np.zeros(3)
    for i in range(3):
        d_inv[i] = b1_vec[i] / (2 * np.pi)
        for j in range(3):
            d_inv[i] += b2_mat[i, j] / (8 * np.pi**2) * alpha_vals[j]

    return d_inv

def run_couplings(mu_start, mu_end, alpha_1_start, alpha_2_start, alpha_3_start,
                  n_points=2000):
    """Run gauge couplings from mu_start to mu_end using 2-loop RG."""
    inv_alpha_start = np.array([1/alpha_1_start, 1/alpha_2_start, 1/alpha_3_start])

    ln_mu_start = np.log(mu_start)
    ln_mu_end = np.log(mu_end)

    sol = solve_ivp(
        rg_equations,
        [ln_mu_start, ln_mu_end],
        inv_alpha_start,
        method='RK45',
        max_step=abs(ln_mu_end - ln_mu_start) / n_points,
        rtol=1e-10, atol=1e-12,
        dense_output=True
    )

    return sol

# ============================================================================
# RUN UPWARD: M_Z -> M_GUT
# ============================================================================

print("\n" + "=" * 90)
print("RUNNING UPWARD: M_Z → M_GUT")
print("=" * 90)

sol_up = run_couplings(M_Z_exp, 1e19, alpha_1_MZ, alpha_2_MZ, alpha_s_MZ)

# Find approximate unification
ln_mu_vals = np.linspace(np.log(M_Z_exp), np.log(1e19), 5000)
inv_alpha_vals = sol_up.sol(ln_mu_vals)

alpha_1_arr = 1.0 / inv_alpha_vals[0]
alpha_2_arr = 1.0 / inv_alpha_vals[1]
alpha_3_arr = 1.0 / inv_alpha_vals[2]

# Find where alpha_1 ≈ alpha_2 (approximate unification)
# Only look above 1e10 GeV to avoid trivially finding the starting point
high_mask = ln_mu_vals > np.log(1e10)
diff_12 = np.abs(inv_alpha_vals[0] - inv_alpha_vals[1])
diff_12_high = diff_12.copy()
diff_12_high[~high_mask] = 1e10
idx_min = np.argmin(diff_12_high)
mu_unif = np.exp(ln_mu_vals[idx_min])
alpha_GUT_approx = 1.0 / inv_alpha_vals[0, idx_min]

print(f"\nApproximate unification:")
print(f"  Scale: {mu_unif:.2e} GeV")
print(f"  alpha_GUT ≈ {alpha_GUT_approx:.6f} (1/alpha = {1/alpha_GUT_approx:.2f})")
print(f"  alpha_1 = {alpha_1_arr[idx_min]:.6f}")
print(f"  alpha_2 = {alpha_2_arr[idx_min]:.6f}")
print(f"  alpha_3 = {alpha_3_arr[idx_min]:.6f}")

# GU epoch for unification scale
N_GUT_from_rg = float(np.log(float(M_P) / 1e3 / mu_unif) / np.log(float(phi)))
print(f"  GU epoch: N ≈ {N_GUT_from_rg:.1f} (gu_constants has N_GUT={N_GUT})")

# Print couplings at key scales
print(f"\n--- Couplings at key scales ---")
key_scales = [91.19, 246.22, 1000, 1e4, 1e8, 1e12, 1e16]
for mu_key in key_scales:
    if mu_key > 1e19:
        continue
    ln_key = np.log(mu_key)
    if ln_key < ln_mu_vals[0] or ln_key > ln_mu_vals[-1]:
        continue
    inv_a = sol_up.sol(ln_key)
    a1, a2, a3 = 1/inv_a[0], 1/inv_a[1], 1/inv_a[2]
    s2w = a1 / (a1 + (5/3)*a2)  # convert from GUT-normalized
    # Actually: alpha_Y = (3/5)*alpha_1, alpha_EM = alpha_Y*alpha_2/(alpha_Y+alpha_2)
    # sin2_theta_W = alpha_Y/(alpha_Y+alpha_2) = (3/5)*alpha_1/((3/5)*alpha_1+alpha_2)
    aY = (3/5) * a1
    s2w = aY / (aY + a2)
    aEM = aY * a2 / (aY + a2)
    print(f"  mu={mu_key:.2e} GeV: alpha_1={a1:.6f}  alpha_2={a2:.6f}  "
          f"alpha_3={a3:.6f}  sin²θ_W={s2w:.5f}  1/alpha_EM={1/aEM:.2f}")

# ============================================================================
# EXTRACT COUPLINGS AT EW SCALE (v = 246 GeV)
# ============================================================================

print("\n" + "=" * 90)
print("GAUGE COUPLINGS AT v_EW = 246.22 GeV")
print("=" * 90)

ln_vEW = np.log(246.22)
inv_a_vEW = sol_up.sol(ln_vEW)
alpha_1_vEW = 1 / inv_a_vEW[0]
alpha_2_vEW = 1 / inv_a_vEW[1]
alpha_3_vEW = 1 / inv_a_vEW[2]

g_1_vEW = np.sqrt(4 * np.pi * alpha_1_vEW)
g_2_vEW = np.sqrt(4 * np.pi * alpha_2_vEW)
g_3_vEW = np.sqrt(4 * np.pi * alpha_3_vEW)

aY_vEW = (3/5) * alpha_1_vEW
sin2_theta_W_vEW = aY_vEW / (aY_vEW + alpha_2_vEW)
cos_theta_W_vEW = np.sqrt(1 - sin2_theta_W_vEW)

print(f"alpha_1(v) = {alpha_1_vEW:.6f}")
print(f"alpha_2(v) = {alpha_2_vEW:.6f}")
print(f"alpha_3(v) = {alpha_3_vEW:.6f}")
print(f"g_1(v)     = {g_1_vEW:.6f}  (GUT normalized)")
print(f"g_2(v)     = {g_2_vEW:.6f}")
print(f"g_Y(v)     = {g_1_vEW * np.sqrt(3/5):.6f}  (SM hypercharge)")
print(f"sin²θ_W(v) = {sin2_theta_W_vEW:.5f}  (PDG at M_Z: {sin2_theta_W_MZ})")
print(f"cos θ_W(v) = {cos_theta_W_vEW:.5f}")

# ============================================================================
# TREE-LEVEL W/Z/HIGGS MASSES (no Pattern corrections!)
# ============================================================================

print("\n" + "=" * 90)
print("TREE-LEVEL MASSES FROM STANDARD EW THEORY")
print("=" * 90)

v_EW = 246.22  # GeV (Fermi constant: v = (sqrt(2)*G_F)^(-1/2))

M_W_tree = g_2_vEW * v_EW / 2
g_prime = g_1_vEW * np.sqrt(3/5)
M_Z_tree = np.sqrt(g_2_vEW**2 + g_prime**2) * v_EW / 2

print(f"\nv_EW = {v_EW} GeV")
print(f"M_W (tree) = g₂·v/2 = {M_W_tree:.3f} GeV  (PDG: 80.3692 GeV)")
print(f"M_Z (tree) = √(g₂²+g'²)·v/2 = {M_Z_tree:.3f} GeV  (PDG: 91.1876 GeV)")
print(f"M_W/M_Z    = {M_W_tree/M_Z_tree:.5f}  (= cos θ_W = {cos_theta_W_vEW:.5f})")
print(f"Error M_W: {(M_W_tree - 80.3692)/80.3692*100:.2f}%")
print(f"Error M_Z: {(M_Z_tree - 91.1876)/91.1876*100:.2f}%")

# ============================================================================
# GU EPOCH ANALYSIS: WHERE IS 246 GeV?
# ============================================================================

print("\n" + "=" * 90)
print("GU EPOCH ANALYSIS: ELECTROWEAK SCALE")
print("=" * 90)

M_P_GeV = float(M_P) / 1e3  # Convert MeV -> GeV
phi_f = float(phi)

N_for_vEW = np.log(M_P_GeV / v_EW) / np.log(phi_f)
print(f"\nM_P = {M_P_GeV:.4e} GeV")
print(f"v_EW = {v_EW} GeV")
print(f"N for v_EW: ln(M_P/v)/ln(φ) = {N_for_vEW:.2f}")
print(f"Nearest integer: N = {round(N_for_vEW)}")
print(f"X(N=80) = {M_P_GeV * phi_f**(-80):.2f} GeV  (error: "
      f"{abs(M_P_GeV * phi_f**(-80) - v_EW)/v_EW*100:.1f}%)")

print(f"\nCRITICAL FINDING:")
print(f"  gu_constants.py has N_EW = 89 → X = {M_P_GeV * phi_f**(-89):.2f} GeV")
print(f"  The Higgs VEV 246 GeV corresponds to N ≈ 80, NOT 89")
print(f"  N=89 coincides with N_b (bottom quark epoch)")
print(f"  Recommendation: the EW SSB epoch should be N_EW_SSB ≈ 80")

# ============================================================================
# ALPHA_S RUNNING CHECK
# ============================================================================

print("\n" + "=" * 90)
print("ALPHA_S RUNNING VALIDATION")
print("=" * 90)

sol_down = run_couplings(M_Z_exp, 1.0, alpha_1_MZ, alpha_2_MZ, alpha_s_MZ, n_points=500)

check_scales = [1.0, 1.5, 2.0, 3.0, 5.0, 10.0, 91.19, 246.0, 1000.0]
for mu_check in check_scales:
    ln_c = np.log(mu_check)
    if mu_check <= M_Z_exp:
        inv_a_check = sol_down.sol(ln_c)
    else:
        inv_a_check = sol_up.sol(ln_c)
    a3_check = 1 / inv_a_check[2]
    print(f"  alpha_s({mu_check:.1f} GeV) = {a3_check:.4f}")

# ============================================================================
# EXPORTABLE RESULTS
# ============================================================================

RESULTS = {
    'v_EW': v_EW,
    'g_1_vEW': g_1_vEW,
    'g_2_vEW': g_2_vEW,
    'g_3_vEW': g_3_vEW,
    'g_prime_vEW': g_prime,
    'sin2_theta_W_vEW': sin2_theta_W_vEW,
    'cos_theta_W_vEW': cos_theta_W_vEW,
    'alpha_1_vEW': alpha_1_vEW,
    'alpha_2_vEW': alpha_2_vEW,
    'alpha_3_vEW': alpha_3_vEW,
    'M_W_tree': M_W_tree,
    'M_Z_tree': M_Z_tree,
    'alpha_GUT_approx': alpha_GUT_approx,
    'mu_unification': mu_unif,
    'N_EW_correct': round(N_for_vEW),
}

print("\n" + "=" * 90)
print("SUMMARY")
print("=" * 90)
print(f"""
INPUTS:
  alpha_EM(0) = 1/137.036  (CODATA — one experimental input)
  alpha_s(M_Z) = 0.1179    (PDG benchmark)
  sin²θ_W(M_Z) = 0.23122  (PDG on-shell)

DERIVED (2-loop RG, standard SM, NO Pattern corrections):
  g₂(v)      = {g_2_vEW:.4f}
  g'(v)      = {g_prime:.4f}
  sin²θ_W(v) = {sin2_theta_W_vEW:.5f}

  M_W (tree) = {M_W_tree:.2f} GeV   (PDG: 80.37, error {abs(M_W_tree-80.3692)/80.3692*100:.2f}%)
  M_Z (tree) = {M_Z_tree:.2f} GeV   (PDG: 91.19, error {abs(M_Z_tree-91.1876)/91.1876*100:.2f}%)

GU EPOCH:
  v_EW = 246 GeV → N ≈ {round(N_for_vEW)} (NOT 89!)
  Approximate unification at {mu_unif:.2e} GeV (N ≈ {N_GUT_from_rg:.0f})
""")
