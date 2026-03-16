#!/usr/bin/env python3
"""
W and Z Boson Masses from Standard Electroweak Theory
=====================================================

Derives M_W, M_Z using standard EW theory with GU-derived inputs:
  - v_EW from the golden ladder epoch (N ~ 80 for EWSB)
  - sin^2(theta_W) = 0.23122 (CODATA)
  - alpha_EM = 1/137.036 (CODATA)

No ad-hoc Pattern-k pi^k corrections are used. Pattern-k is an epoch
label (see derivations/33_PATTERN_K/), not a multiplicative factor.

For the full 2-loop RG calculation, see 03_gauge_coupling_rg.py.
For 1-loop radiative corrections, see 02_precise_weak_masses.py.
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from utils.gu_constants import phi, pi, M_P, N_EW

PI = float(pi)
PHI = float(phi)
MP_GeV = float(M_P) / 1e3  # Convert MeV to GeV

print("=" * 80)
print("W AND Z BOSON MASSES — STANDARD EW + GU EPOCH")
print("No Pattern-k pi^k factors (see 33_PATTERN_K/ for why)")
print("=" * 80)

# ============================================================================
# ELECTROWEAK VEV FROM THE GOLDEN LADDER
# ============================================================================

print("\n" + "-" * 80)
print("ELECTROWEAK VEV FROM THE GOLDEN LADDER")
print("-" * 80)

N_EW_SSB = 80  # EWSB epoch (from 03_gauge_coupling_rg.py analysis)
X_EW_80 = MP_GeV * PHI**(-N_EW_SSB)
X_EW_89 = MP_GeV * PHI**(-N_EW)

print(f"""
  The EW VEV v = 246.22 GeV corresponds to epoch N ~ 80 on the golden ladder.

  X(N=80)  = M_P * phi^(-80) = {X_EW_80:.2f} GeV  (5% from 246 GeV)
  X(N=89)  = M_P * phi^(-89) = {X_EW_89:.4f} GeV  (too low — N=89 is the QCD/EW boundary)

  Using N_EW_SSB = 80 as the EWSB epoch.
  v_EW(GU) = {X_EW_80:.2f} GeV  vs  CODATA: 246.22 GeV
  Error: {abs(X_EW_80 - 246.22)/246.22*100:.1f}%
""")

v_EW = X_EW_80  # GU-derived VEV

# ============================================================================
# GAUGE COUPLINGS AT M_Z
# ============================================================================

print("-" * 80)
print("GAUGE COUPLINGS AT M_Z (from CODATA/PDG inputs)")
print("-" * 80)

alpha_EM = 1 / 137.035999084
sin2_tw = 0.23122  # CODATA sin^2(theta_W) at M_Z
alpha_s_mz = 0.1179

g1_sq = 4 * PI * alpha_EM / (1 - sin2_tw) * 5/3  # GUT-normalized U(1)
g2_sq = 4 * PI * alpha_EM / sin2_tw

g1 = np.sqrt(g1_sq)
g2 = np.sqrt(g2_sq)

cos_tw = np.sqrt(1 - sin2_tw)
sin_tw = np.sqrt(sin2_tw)

print(f"  alpha_EM   = 1/137.036 = {alpha_EM:.6e}")
print(f"  sin^2(theta_W) = {sin2_tw:.5f}")
print(f"  g_1 (GUT norm) = {g1:.4f}")
print(f"  g_2             = {g2:.4f}")
print(f"  cos(theta_W)    = {cos_tw:.6f}")

# ============================================================================
# TREE-LEVEL W AND Z MASSES
# ============================================================================

print("\n" + "-" * 80)
print("TREE-LEVEL W AND Z MASSES")
print("-" * 80)

M_W_tree = g2 * v_EW / 2
M_Z_tree = np.sqrt(g1_sq * 3/5 + g2_sq) * v_EW / 2  # g1 in SM normalization

M_W_exp = 80.3692  # GeV (CODATA 2022)
M_Z_exp = 91.1876  # GeV (CODATA 2022)

print(f"""
  Standard EW formulas (tree level):
    M_W = g_2 * v / 2 = {g2:.4f} * {v_EW:.2f} / 2 = {M_W_tree:.2f} GeV
    M_Z = sqrt(g'^2 + g_2^2) * v / 2 = {M_Z_tree:.2f} GeV

  CODATA values:
    M_W = {M_W_exp} GeV
    M_Z = {M_Z_exp} GeV

  Errors (tree level with GU VEV):
    M_W: {abs(M_W_tree - M_W_exp)/M_W_exp*100:.2f}%
    M_Z: {abs(M_Z_tree - M_Z_exp)/M_Z_exp*100:.2f}%
""")

# ============================================================================
# 1-LOOP RADIATIVE CORRECTIONS (simplified)
# ============================================================================

print("-" * 80)
print("1-LOOP RADIATIVE CORRECTIONS (simplified)")
print("-" * 80)

m_top = 172.76  # GeV
M_H = 125.25    # GeV (Higgs mass, CODATA)

# Delta_r correction (Sirlin)
Delta_alpha = alpha_EM / (3 * PI) * (1 + alpha_s_mz / PI) * np.log(M_Z_exp**2 / (0.000511**2))
Delta_rho_top = 3 * alpha_EM / (16 * PI * sin2_tw) * (m_top / M_W_exp)**2

Delta_r = Delta_alpha - Delta_rho_top

M_W_1loop = M_W_tree * np.sqrt(1 + Delta_r)

print(f"  Delta_alpha (from fermion loops) = {Delta_alpha:.4f}")
print(f"  Delta_rho (top quark)            = {Delta_rho_top:.4f}")
print(f"  Delta_r (total, simplified)      = {Delta_r:.4f}")
print(f"  M_W (1-loop) = {M_W_1loop:.2f} GeV  (error: {abs(M_W_1loop - M_W_exp)/M_W_exp*100:.2f}%)")

# ============================================================================
# WHY W/Z ARE MASSIVE AND PHOTON IS MASSLESS
# ============================================================================

print("\n" + "-" * 80)
print("WHY W/Z ARE MASSIVE AND PHOTON IS MASSLESS")
print("-" * 80)

print("""
  In the GU framework, the mechanism is standard EWSB:

  1. The Omega field contains a Higgs-like doublet H
  2. At epoch N ~ 80, m_H^2(X) crosses zero (see 33_PATTERN_K/06)
  3. H acquires a VEV: <H> = v/sqrt(2) = 174 GeV
  4. SU(2)_L x U(1)_Y -> U(1)_EM spontaneously
  5. W+, W-, Z become massive via the Higgs mechanism
  6. Photon remains massless (unbroken U(1)_EM generator)

  This is the SAME mechanism as the Standard Model.
  The GU contribution: v_EW = M_P * phi^(-80) from the golden ladder.
  No pi^k "Pattern" factors are needed or derived (see 33_PATTERN_K/).
""")

# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 80)
print("SUMMARY")
print("=" * 80)

rho = (M_W_tree / (M_Z_tree * cos_tw))**2

print(f"""
  GU-derived VEV: v = M_P * phi^(-80) = {v_EW:.2f} GeV (vs 246.22 CODATA)
  Tree-level:
    M_W = {M_W_tree:.2f} GeV  (error {abs(M_W_tree - M_W_exp)/M_W_exp*100:.2f}%)
    M_Z = {M_Z_tree:.2f} GeV  (error {abs(M_Z_tree - M_Z_exp)/M_Z_exp*100:.2f}%)
  With 1-loop:
    M_W = {M_W_1loop:.2f} GeV  (error {abs(M_W_1loop - M_W_exp)/M_W_exp*100:.2f}%)
  rho parameter = {rho:.6f}  (custodial symmetry: rho = 1)

  STATUS: Standard EW theory with GU epoch for v_EW.
  No ad-hoc pi^k Pattern corrections.
  For full 2-loop RG, see 03_gauge_coupling_rg.py.
  For Higgs mass, see 04_higgs_from_omega.py.
""")