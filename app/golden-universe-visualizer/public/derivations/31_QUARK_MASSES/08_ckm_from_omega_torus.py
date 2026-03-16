#!/usr/bin/env python3
"""
CKM mixing matrix from Yukawa structure on the Omega-torus
==========================================================

In GU, CKM elements arise from overlap integrals on the Omega-torus between
generations. Up-type (10x10x5_H) and down-type (10x5barx5_H) have different
epochs; mixing angles are parametrized by epoch differences.

Epochs: N_u=110, N_d=105, N_s=102, N_c=97, N_b=89, N_t=81
PDG Wolfenstein: |V_us| ≈ 0.225, |V_cb| ≈ 0.042, |V_ub| ≈ 0.004
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from utils.gu_constants import phi, M_P, pi, N_u, N_d, N_s, N_c as N_charm, N_b, N_t

_phi = float(phi)

# PDG CKM magnitudes (Wolfenstein)
PDG_V_us = 0.2243
PDG_V_cb = 0.0422
PDG_V_ub = 0.00394

# Epoch differences (down-type: d,s,b)
Delta_N_ds = abs(N_d - N_s)   # 3
Delta_N_sb = abs(N_s - N_b)   # 13
Delta_N_db = abs(N_d - N_b)   # 16
# Up-type
Delta_N_uc = abs(N_u - N_charm)  # 13
Delta_N_ct = abs(N_charm - N_t)  # 16
Delta_N_ut = abs(N_u - N_t)      # 29


def ansatz_A():
    """|V_ij| = phi^(-|N_di - N_dj|) — epoch difference in down sector only."""
    return {
        "V_us": _phi ** (-Delta_N_ds),
        "V_cb": _phi ** (-Delta_N_sb),
        "V_ub": _phi ** (-Delta_N_db),
    }


def ansatz_B():
    """|V_ij| = phi^(-(|N_di-N_dj| + |N_ui-N_uj|)/2) — average of down and up sector."""
    # 1-2: (3 + 13)/2 = 8
    # 2-3: (13 + 16)/2 = 14.5 -> use 14 or 15
    # 1-3: (16 + 29)/2 = 22.5 -> use 22 or 23
    delta_us = (Delta_N_ds + Delta_N_uc) / 2.0
    delta_cb = (Delta_N_sb + Delta_N_ct) / 2.0
    delta_ub = (Delta_N_db + Delta_N_ut) / 2.0
    return {
        "V_us": _phi ** (-delta_us),
        "V_cb": _phi ** (-delta_cb),
        "V_ub": _phi ** (-delta_ub),
    }


def ansatz_C():
    """Fritzsch texture: epsilon_ij = phi^(-Delta_N). Use down-sector Delta_N for off-diagonal."""
    # Fritzsch: V_us ~ epsilon_ds, V_cb ~ epsilon_sb, V_ub ~ epsilon_ds*epsilon_sb
    eps_ds = _phi ** (-Delta_N_ds)
    eps_sb = _phi ** (-Delta_N_sb)
    return {
        "V_us": eps_ds,
        "V_cb": eps_sb,
        "V_ub": eps_ds * eps_sb,
    }


def main():
    print("=" * 72)
    print("CKM FROM OMEGA-TORUS (epoch-based mixing ansatze)")
    print("=" * 72)
    print("\nEpochs: N_u={}, N_d={}, N_s={}, N_c={}, N_b={}, N_t={}".format(
        N_u, N_d, N_s, N_charm, N_b, N_t))
    print("Down-sector differences: |N_d-N_s|={}, |N_s-N_b|={}, |N_d-N_b|={}".format(
        Delta_N_ds, Delta_N_sb, Delta_N_db))
    print("Up-sector: |N_u-N_c|={}, |N_c-N_t|={}, |N_u-N_t|={}".format(
        Delta_N_uc, Delta_N_ct, Delta_N_ut))
    print("\nPDG: |V_us|={:.4f}, |V_cb|={:.4f}, |V_ub|={:.4f}".format(
        PDG_V_us, PDG_V_cb, PDG_V_ub))
    print("Hierarchy: |V_us| >> |V_cb| >> |V_ub|")
    print()

    A = ansatz_A()
    B = ansatz_B()
    C = ansatz_C()

    print("--- Ansatz A: |V_ij| = phi^(-|N_di - N_dj|) (down sector) ---")
    for key in ["V_us", "V_cb", "V_ub"]:
        pdg = {"V_us": PDG_V_us, "V_cb": PDG_V_cb, "V_ub": PDG_V_ub}[key]
        err = abs(A[key] - pdg) / pdg * 100
        print("  {} = phi^(-{}) = {:.4f}  (PDG {:.4f}, err {:.1f}%)".format(
            key, {"V_us": Delta_N_ds, "V_cb": Delta_N_sb, "V_ub": Delta_N_db}[key],
            A[key], pdg, err))
    print()

    print("--- Ansatz B: |V_ij| = phi^(-(down+up)/2) (average) ---")
    for key in ["V_us", "V_cb", "V_ub"]:
        pdg = {"V_us": PDG_V_us, "V_cb": PDG_V_cb, "V_ub": PDG_V_ub}[key]
        err = abs(B[key] - pdg) / pdg * 100
        print("  {} = {:.4f}  (PDG {:.4f}, err {:.1f}%)".format(key, B[key], pdg, err))
    print()

    print("--- Ansatz C: Fritzsch epsilon = phi^(-Delta_N), V_ub ~ V_us*V_cb ---")
    for key in ["V_us", "V_cb", "V_ub"]:
        pdg = {"V_us": PDG_V_us, "V_cb": PDG_V_cb, "V_ub": PDG_V_ub}[key]
        err = abs(C[key] - pdg) / pdg * 100
        print("  {} = {:.4f}  (PDG {:.4f}, err {:.1f}%)".format(key, C[key], pdg, err))
    print()

    print("=" * 72)
    print("CKM RESULTS TABLE (all ansatze vs PDG)")
    print("=" * 72)
    print(f"{'Element':<8} {'PDG':>10} {'Ansatz A':>10} {'Ansatz B':>10} {'Ansatz C':>10}")
    print("-" * 72)
    for key in ["V_us", "V_cb", "V_ub"]:
        pdg = {"V_us": PDG_V_us, "V_cb": PDG_V_cb, "V_ub": PDG_V_ub}[key]
        print(f"{key:<8} {pdg:>10.4f} {A[key]:>10.4f} {B[key]:>10.4f} {C[key]:>10.4f}")
    print("-" * 72)
    print("  Hierarchy: |V_us| >> |V_cb| >> |V_ub|  (all ansatze respect this)")
    print("=" * 72)


if __name__ == "__main__":
    main()
