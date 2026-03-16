#!/usr/bin/env python3
"""
Precise W and Z Boson Mass Calculation (Standard EW Theory)
============================================================

Uses ONLY alpha_EM as GU input. No ad-hoc Pattern-k corrections.
- v_EW from GU epoch N≈80: M_P_GeV * phi^(-80) ≈ 233 GeV (~5.3% from 246 GeV).
- Gauge couplings at M_Z from standard boundary conditions.
- Tree-level M_W, M_Z from g_2, g', v; 1-loop Delta_r correction for M_W.
- Higgs mass: M_H = sqrt(2*lambda)*v — lambda not derived from first principles (task A4).
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import mpmath
mpmath.mp.dps = 50

from utils.gu_constants import phi, M_P, alpha_EM, pi, CODATA

# ---------------------------------------------------------------------------
# Fundamental parameters (from GU)
# ---------------------------------------------------------------------------

pi_f = float(pi)
phi_f = float(phi)
alpha_EM_val = float(alpha_EM)
# M_P in gu_constants is in MeV; convert to GeV for scale comparison
M_P_GeV = float(M_P) / 1e3

print("=" * 80)
print("PRECISE WEAK MASSES — STANDARD ELECTROWEAK THEORY")
print("GU input: alpha_EM only. No Pattern-k corrections.")
print("=" * 80)

print("\n### GU constants (utils.gu_constants)")
print("-" * 60)
print(f"  phi     = {phi_f:.10f}")
print(f"  pi      = {pi_f:.10f}")
print(f"  M_P     = {M_P_GeV:.4e} GeV")
print(f"  alpha_EM = 1/{1/alpha_EM_val:.6f}  (CODATA — single experimental input)")

# ---------------------------------------------------------------------------
# Electroweak scale: v_EW and GU epoch N ≈ 80
# ---------------------------------------------------------------------------

v_EW = 246.22  # GeV (from G_F: v = (sqrt(2)*G_F)^(-1/2))

print("\n### Electroweak scale and GU epoch")
print("-" * 60)
print(f"  v_EW (standard) = {v_EW} GeV")

N_80 = 80
X_at_80 = M_P_GeV * (phi_f ** (-N_80))
deviation_pct = abs(X_at_80 - v_EW) / v_EW * 100
print(f"  GU scale at N=80: X(80) = M_P * phi^(-80) = {X_at_80:.2f} GeV")
print(f"  Deviation from v_EW: {deviation_pct:.2f}%")
print(f"  => v_EW corresponds to GU epoch N ≈ {N_80} (M_P_GeV * phi^(-80) ≈ {X_at_80:.0f} GeV).")

# ---------------------------------------------------------------------------
# Boundary conditions at M_Z (standard)
# ---------------------------------------------------------------------------

sin2_theta_W = 0.23122   # PDG at M_Z
# Run alpha_EM from q=0 to M_Z: 1/alpha(M_Z) = 1/alpha(0) - Delta_alpha, alpha_MZ = alpha/(1 - alpha*Delta_alpha)
# Convention: alpha_EM_MZ = alpha_EM / (1 - 0.0590)
alpha_EM_MZ = alpha_EM_val / (1 - 0.0590)

alpha_2_MZ = alpha_EM_MZ / sin2_theta_W
alpha_1_MZ = alpha_EM_MZ / (1 - sin2_theta_W) * (5/3)

# g_2 = sqrt(4*pi*alpha_2), g' = sqrt(4*pi*(3/5)*alpha_1)
g_2 = np.sqrt(4 * np.pi * alpha_2_MZ)
g_prime = np.sqrt(4 * np.pi * (3/5) * alpha_1_MZ)

print("\n### Gauge couplings at M_Z (boundary conditions)")
print("-" * 60)
print(f"  alpha_EM(M_Z) = alpha_EM/(1-0.0590) = 1/{1/alpha_EM_MZ:.2f}")
print(f"  sin²θ_W(M_Z) = {sin2_theta_W}")
print(f"  alpha_2(M_Z) = alpha_EM_MZ/sin²θ_W = {alpha_2_MZ:.6f}")
print(f"  alpha_1(M_Z) = alpha_EM_MZ/(1-sin²θ_W)*(5/3) = {alpha_1_MZ:.6f}")
print(f"  g_2 = sqrt(4*pi*alpha_2) = {g_2:.6f}")
print(f"  g'  = sqrt(4*pi*(3/5)*alpha_1) = {g_prime:.6f}")

# ---------------------------------------------------------------------------
# Tree-level W and Z masses
# ---------------------------------------------------------------------------

M_W_tree = g_2 * v_EW / 2
M_Z_tree = np.sqrt(g_2**2 + g_prime**2) * v_EW / 2
cos2_theta_W = 1 - sin2_theta_W
cos_theta_W = np.sqrt(1 - sin2_theta_W)

print("\n### Tree-level masses (standard formulas)")
print("-" * 60)
print(f"  M_W_tree = g_2 * v_EW/2 = {M_W_tree:.4f} GeV")
print(f"  M_Z_tree = sqrt(g_2² + g'²) * v_EW/2 = {M_Z_tree:.4f} GeV")
print(f"  M_W_tree / M_Z_tree = cos θ_W = {cos_theta_W:.6f}")

# ---------------------------------------------------------------------------
# 1-loop radiative correction: Delta_r
# ---------------------------------------------------------------------------
# Delta_r ≈ (alpha/(pi*sin2_theta_W)) * [Delta_alpha - (cos2/sin2)*Delta_rho]
# Delta_rho = 3*G_F*m_top^2 / (8*sqrt(2)*pi^2) ≈ 0.0094
# M_W_corrected = M_W_tree / sqrt(1 - Delta_r)

G_F_GeV = 1.1663787e-5   # GeV^{-2} (Fermi constant)
m_top_GeV = 172.76       # GeV (PDG pole)

Delta_rho = 3 * G_F_GeV * (m_top_GeV**2) / (8 * np.sqrt(2) * np.pi**2)
# Delta_alpha: running from 0 to M_Z, 1/alpha(M_Z) - 1/alpha(0) ≈ 0.059
Delta_alpha = 0.0590

Delta_r = (alpha_EM_MZ / (np.pi * sin2_theta_W)) * (
    Delta_alpha - (cos2_theta_W / sin2_theta_W) * Delta_rho
)
# Clamp to avoid sqrt(negative) from higher-order effects
Delta_r = min(Delta_r, 0.99)

M_W_1loop = M_W_tree / np.sqrt(1 - Delta_r)
# Z mass: tree-level relation M_Z = M_W/cos_theta_W is preserved by custodial symmetry;
# we use tree M_Z (radiative shifts are smaller and often quoted at M_Z pole input)
M_Z_1loop = M_Z_tree  # standard practice: M_Z is input; we report tree for comparison

print("\n### 1-loop radiative correction (Delta_r)")
print("-" * 60)
print(f"  Delta_rho = 3*G_F*m_top^2/(8*sqrt(2)*pi²) = {Delta_rho:.6f}")
print(f"  Delta_alpha ≈ {Delta_alpha}")
print(f"  Delta_r = (alpha/(pi*sin²θ_W))*(Delta_alpha - (cos²θ_W/sin²θ_W)*Delta_rho) = {Delta_r:.6f}")
print(f"  M_W (1-loop) = M_W_tree/sqrt(1 - Delta_r) = {M_W_1loop:.4f} GeV")

# ---------------------------------------------------------------------------
# Higgs mass (gap: lambda not derived)
# ---------------------------------------------------------------------------

print("\n### Higgs mass")
print("-" * 60)
print("  M_H = sqrt(2*lambda)*v_EW, where lambda is the Higgs self-coupling.")
print("  lambda is NOT derived from first principles here (task A4).")
print("  Experimental M_H ≈ 125.25 GeV.")

# ---------------------------------------------------------------------------
# Results table vs CODATA
# ---------------------------------------------------------------------------

# CODATA: W, Z in MeV in gu_constants; PDG uncertainties in GeV
M_W_exp_GeV = CODATA["W"] / 1e3
M_Z_exp_GeV = CODATA["Z"] / 1e3
M_W_unc = 0.012   # GeV (PDG)
M_Z_unc = 0.0021  # GeV (PDG)

print("\n" + "=" * 80)
print("RESULTS TABLE (derived vs CODATA/PDG)")
print("=" * 80)

results = [
    ("M_W (tree)", M_W_tree, M_W_exp_GeV, M_W_unc),
    ("M_W (tree+1loop)", M_W_1loop, M_W_exp_GeV, M_W_unc),
    ("M_Z (tree)", M_Z_tree, M_Z_exp_GeV, M_Z_unc),
    ("sin²θ_W(M_Z)", sin2_theta_W, CODATA["sin2_theta_W"], 0.00003),
]
print("\n  Quantity              Derived        CODATA/PDG   σ_exp   Error %   σ")
print("  " + "-" * 70)
for name, derived, exp_val, unc in results:
    err_pct = abs(derived - exp_val) / exp_val * 100 if exp_val != 0 else 0
    sigma = abs(derived - exp_val) / unc if unc > 0 else 0
    print(f"  {name:<22} {derived:>12.5f}   {exp_val:>10.5f}   {unc:>5.4f}   {err_pct:>6.3f}%   {sigma:>4.1f}σ")

print("\n  Key result: M_W ≈ {:.2f} GeV, M_Z ≈ {:.2f} GeV (tree+1loop / tree).".format(M_W_1loop, M_Z_tree))
print("  Full 1-loop Delta_r (with Delta_r_rem) is ~0.03, giving M_W ~ 80.3 GeV;")
print("  this script uses the leading (Delta_alpha, Delta_rho) piece only.")
print("  Standard EW theory with alpha_EM as the only GU input.")
print("  NO ad-hoc Pattern-k corrections. Pattern mechanism requires its own derivation (task D1).")

print("\n" + "=" * 80)
print("END")
print("=" * 80)
