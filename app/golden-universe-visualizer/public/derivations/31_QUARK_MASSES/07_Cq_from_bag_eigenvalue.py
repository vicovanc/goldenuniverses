#!/usr/bin/env python3
"""
C_q SHAPE FACTORS FROM THREE ROUTES
===================================

Derives the multiplicative correction factors C_q that convert the bare GU
phi-ladder mass M_P * phi^(-N_q) into the physical quark mass.

Routes:
  1. Bag eigenvalue → constituent → current mass (Sigma_DCSB from NJL)
  2. SU(5) Georgi-Jarlskog texture + RG running
  3. Mass ratio constraints (Leutwyler ellipse, epoch adjustments)
"""

import numpy as np
import mpmath
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.gu_constants import (
    phi,
    M_P,
    pi,
    e,
    alpha_EM,
    N_u, N_d, N_s, N_c, N_b, N_t,
    N_QCD,
)

# Load RG running from sibling script (avoids package layout)
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "rg_run",
    os.path.join(os.path.dirname(__file__), "03_rg_running_planck_to_2gev.py"),
)
rg_run = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rg_run)

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------

hbar_c = 197.3269804  # MeV·fm (CODATA)

# PDG quark masses (CODATA reference)
# MS-bar at 2 GeV for u, d, s; pole for c, b, t
m_u_PDG = 2.16    # MeV
m_d_PDG = 4.67    # MeV
m_s_PDG = 93.4    # MeV
m_c_PDG = 1270.0  # MeV
m_b_PDG = 4180.0  # MeV
m_t_PDG = 172760.0  # MeV

PDG = {
    'u': m_u_PDG, 'd': m_d_PDG, 's': m_s_PDG,
    'c': m_c_PDG, 'b': m_b_PDG, 't': m_t_PDG,
}

N_q = {'u': N_u, 'd': N_d, 's': N_s, 'c': N_c, 'b': N_b, 't': N_t}
quark_order = ['u', 'd', 's', 'c', 'b', 't']


def bare_mass(N):
    """GU bare scale mass: M_P * phi^(-N) [MeV]."""
    return float(M_P * phi**(-int(N)))


def C_q_from_PDG(flavor):
    """C_q = m_PDG / (M_P * phi^(-N_q))."""
    N = N_q[flavor]
    m_bare = bare_mass(N)
    return PDG[flavor] / m_bare


# ---------------------------------------------------------------------------
# ROUTE 1: BAG EIGENVALUE → CONSTITUENT → CURRENT MASS
# ---------------------------------------------------------------------------

def route1_bag_constituent_current():
    """
    MIT bag s1/2 eigenvalue omega*R = 2.0428.
    E_q = omega/R for massless quark in bag; R = R_bag.
    GU: c_B = (2*pi/phi)^2, R_bag = ((3*omega_bag)/(4*pi*c_B))^(1/4) * hbar_c/Lambda_QCD.
    Lambda_QCD = M_P * phi^(-95) * pi/3.
    """
    omega_R = 2.0428  # MIT bag dimensionless eigenvalue
    phi_f = float(phi)
    pi_f = float(pi)
    M_P_f = float(M_P)

    c_B = (2 * pi_f / phi_f) ** 2
    Lambda_QCD = M_P_f * (phi_f ** (-N_QCD)) * (pi_f / 3)  # ~179 MeV
    omega_bag = omega_R  # use same scale

    factor = (3 * omega_bag) / (4 * pi_f * c_B)
    R_bag_fm = (factor ** 0.25) * (hbar_c / Lambda_QCD)

    # E_per_quark in bag (MeV): 2.0428 * hbar_c / R_bag [R in fm]
    E_per_quark_MeV = omega_R * hbar_c / R_bag_fm

    # Constituent mass (u,d) ~ 310 MeV from bag + binding
    M_const_u_d = 310.0  # MeV (phenomenological)
    Sigma_DCSB_u = M_const_u_d - m_u_PDG  # ~308 MeV
    Sigma_DCSB_d = M_const_u_d - m_d_PDG  # ~305 MeV

    # Try Sigma from GU/NJL: Sigma ~ 4*pi*alpha_s * <psi-bar psi> / (3*M_const^2)
    # Condensate <psi-bar psi> ~ - (250 MeV)^3 at 2 GeV
    alpha_s_2gev = 0.30  # typical
    condensate_MeV3 = -(250.0 ** 3)
    Sigma_NJL_guess = 4 * pi_f * alpha_s_2gev * abs(condensate_MeV3) / (3 * (M_const_u_d ** 2))
    # Dimensionally wrong as written (Sigma in MeV needs condensate in MeV^3);
    # OPE gives Sigma ~ alpha_s * |<psi-bar psi>|^(1/3) roughly
    Sigma_NJL_rough = alpha_s_2gev * 250.0  # ~75 MeV, order-of-magnitude

    return {
        'omega_R': omega_R,
        'c_B': c_B,
        'Lambda_QCD_MeV': Lambda_QCD,
        'R_bag_fm': R_bag_fm,
        'E_per_quark_MeV': E_per_quark_MeV,
        'M_const_u_d': M_const_u_d,
        'Sigma_DCSB_u': Sigma_DCSB_u,
        'Sigma_DCSB_d': Sigma_DCSB_d,
        'Sigma_NJL_rough_MeV': Sigma_NJL_rough,
        'status': 'E_per_quark from bag OK; Sigma_DCSB from GU not derived (NJL estimate ~75 MeV vs needed ~308 MeV).',
    }


# ---------------------------------------------------------------------------
# ROUTE 2: SU(5) GEORGI–JARLSKOG TEXTURE
# ---------------------------------------------------------------------------

def route2_georgi_jarlskog():
    """
    At GUT scale: m_b/m_tau = 1, m_s/m_mu = 1/3, m_d/m_e = 3 (Clebsch–Gordan).
    Combine with RG running from GUT to 2 GeV (or pole). C_q_GJ for down-type.
    """
    # Lepton masses for GJ ratios (MeV)
    m_e = 0.51099895069
    m_mu = 105.6583755
    m_tau = 1776.86

    # GJ factors at GUT (down-type)
    # m_b = m_tau, m_s = m_mu/3, m_d = 3*m_e  at GUT
    GJ_b = 1.0
    GJ_s = 1.0 / 3.0
    GJ_d = 3.0

    # Get C_RG from 03_rg_running_planck_to_2gev
    results_rg = {}
    for name in quark_order:
        N = N_q[name]
        if name in ('u', 'd', 's'):
            mu_tgt = 2000.0
        elif name == 'c':
            mu_tgt = rg_run.M_CHARM_POLE
        elif name == 'b':
            mu_tgt = rg_run.M_BOT_POLE
        else:
            mu_tgt = rg_run.M_TOP_POLE
        m_bare, m_run, C_RG, _ = rg_run.run_mass_full(N, mu_tgt)
        results_rg[name] = {'m_bare': m_bare, 'm_run': m_run, 'C_RG': C_RG}

    # Down-type: m_PDG = m_bare * C_RG * C_GJ  =>  C_GJ = m_PDG / (m_bare * C_RG)
    # So total C_q = m_PDG/m_bare = C_RG * C_GJ  =>  C_GJ = C_q / C_RG
    C_GJ_d = (m_d_PDG / results_rg['d']['m_bare']) / results_rg['d']['C_RG']
    C_GJ_s = (m_s_PDG / results_rg['s']['m_bare']) / results_rg['s']['C_RG']
    C_GJ_b = (m_b_PDG / results_rg['b']['m_bare']) / results_rg['b']['C_RG']

    # Check: does m_b_bare * C_RG give m_b_PDG? (C_RG alone, no GJ)
    m_b_run = results_rg['b']['m_run']
    ratio_b_run_to_PDG = m_b_run / m_b_PDG

    return {
        'GJ_factors': {'d': GJ_d, 's': GJ_s, 'b': GJ_b},
        'C_RG': {q: results_rg[q]['C_RG'] for q in quark_order},
        'C_GJ_from_fit': {'d': C_GJ_d, 's': C_GJ_s, 'b': C_GJ_b},
        'm_b_run': m_b_run,
        'm_b_PDG': m_b_PDG,
        'ratio_b_run_to_PDG': ratio_b_run_to_PDG,
        'status': 'GJ gives ratios at GUT; C_GJ fitted from data. m_b_run vs m_b_PDG shows RG alone is not enough.',
    }


# ---------------------------------------------------------------------------
# ROUTE 3: MASS RATIO CONSTRAINTS
# ---------------------------------------------------------------------------

def route3_mass_ratios():
    """
    GU bare ratio m_u/m_d = phi^(N_d - N_u) = phi^(-5) ≈ 0.090. PDG ≈ 0.46.
    Leutwyler ellipse: (m_u/m_d)^2 + (1/Q^2)*(m_s/m_d - m_u*m_s/m_d^2) = 1, Q = 22.7.
    Check epoch adjustments ±1–2 to fix u/d ratio.
    """
    Q_Leutwyler = 22.7
    ratio_gu_bare = float(phi ** (N_d - N_u))  # phi^(-5)
    ratio_pdg = m_u_PDG / m_d_PDG

    # Leutwyler: (m_u/m_d)^2 + (1/Q^2)*(m_s/m_d - m_u*m_s/m_d^2) = 1
    # With PDG values:
    term1 = (m_u_PDG / m_d_PDG) ** 2
    term2 = (1 / Q_Leutwyler**2) * (m_s_PDG/m_d_PDG - m_u_PDG*m_s_PDG/(m_d_PDG**2))
    lhs_pdg = term1 + term2

    # What m_u/m_d would satisfy ellipse if we fix m_s/m_d?
    # 1 = (r)^2 + (1/Q^2)*(m_s/m_d - r * m_s/m_d) = r^2 + (1/Q^2)*(m_s/m_d)*(1 - r)
    # Solve for r = m_u/m_d
    ms_over_md = m_s_PDG / m_d_PDG
    # r^2 + (1/Q^2)*ms_over_md*(1-r) - 1 = 0
    a_coef = 1.0
    b_coef = -(1/Q_Leutwyler**2) * ms_over_md
    c_coef = (1/Q_Leutwyler**2) * ms_over_md - 1
    disc = b_coef**2 - 4*a_coef*c_coef
    r_ellipse = (-b_coef + np.sqrt(disc)) / (2*a_coef) if disc >= 0 else float('nan')

    # Epoch adjustments: if N_u -> N_u + dn, N_d -> N_d, then m_u/m_d = phi^(N_d - N_u - dn) = ratio_gu_bare * phi^(-dn)
    # We need ratio_gu_bare * phi^(-dn) ≈ 0.46  =>  phi^(-dn) ≈ 0.46/0.09 ≈ 5.1  =>  -dn*ln(phi) = ln(5.1)  =>  dn ≈ -5.7
    # So N_u smaller by ~6 gives ratio ~5; or N_d larger. Try ±1, ±2.
    adjustments = []
    for du in range(-3, 4):
        for dd in range(-3, 4):
            r = float(phi ** ((N_d + dd) - (N_u + du)))
            if 0.3 < r < 0.6:
                adjustments.append((du, dd, r))

    return {
        'ratio_gu_bare': ratio_gu_bare,
        'ratio_pdg': ratio_pdg,
        'Q_Leutwyler': Q_Leutwyler,
        'ellipse_LHS_PDG': lhs_pdg,
        'r_ellipse': r_ellipse,
        'epoch_adjustments_in_range': adjustments[:10],
        'status': 'GU bare u/d ratio ~0.09 vs PDG 0.46; off by ~5. Epoch tweaks (±1–2) cannot fix without breaking other ratios.',
    }


# ---------------------------------------------------------------------------
# MAIN: COMPUTE ALL AND PRINT TABLE
# ---------------------------------------------------------------------------

def main():
    print("=" * 90)
    print("C_q SHAPE FACTORS: THREE DERIVATION ROUTES")
    print("C_q converts bare M_P * phi^(-N_q) into physical quark mass")
    print("=" * 90)

    # Base: needed C_q from PDG
    print("\n" + "-" * 90)
    print("BASE: PDG MASSES AND REQUIRED C_q")
    print("-" * 90)
    print(f"\n  {'flavor':>6s}  {'N':>4s}  {'m_bare [MeV]':>16s}  {'m_PDG [MeV]':>14s}  {'C_q = m_PDG/m_bare':>20s}")
    print("  " + "-" * 70)
    C_q_needed = {}
    for q in quark_order:
        N = N_q[q]
        m_b = bare_mass(N)
        cq = C_q_from_PDG(q)
        C_q_needed[q] = cq
        print(f"  {q:>6s}  {N:>4d}  {m_b:>16.6e}  {PDG[q]:>14.2f}  {cq:>20.6f}")

    # Route 1
    print("\n" + "-" * 90)
    print("ROUTE 1: BAG EIGENVALUE → CONSTITUENT → CURRENT MASS")
    print("-" * 90)
    r1 = route1_bag_constituent_current()
    print(f"  MIT bag omega*R = {r1['omega_R']}")
    print(f"  c_B = (2*pi/phi)^2 = {r1['c_B']:.6f}")
    print(f"  Lambda_QCD = M_P*phi^(-95)*pi/3 = {r1['Lambda_QCD_MeV']:.2f} MeV")
    print(f"  R_bag = {r1['R_bag_fm']:.4f} fm")
    print(f"  E_per_quark (bag) = {r1['E_per_quark_MeV']:.2f} MeV")
    print(f"  M_const (u,d) ≈ {r1['M_const_u_d']:.0f} MeV  =>  Sigma_DCSB(u) ≈ {r1['Sigma_DCSB_u']:.0f} MeV")
    print(f"  NJL rough Sigma ~ alpha_s * 250 MeV ≈ {r1['Sigma_NJL_rough_MeV']:.0f} MeV")
    print(f"  STATUS: {r1['status']}")

    # Route 2
    print("\n" + "-" * 90)
    print("ROUTE 2: SU(5) GEORGI–JARLSKOG + RG RUNNING")
    print("-" * 90)
    r2 = route2_georgi_jarlskog()
    print(f"  GJ at GUT: m_b/m_tau=1, m_s/m_mu=1/3, m_d/m_e=3")
    print(f"  m_b after RG (no C_q): {r2['m_b_run']:.2f} MeV  |  m_b PDG: {r2['m_b_PDG']:.0f} MeV  =>  ratio: {r2['ratio_b_run_to_PDG']:.4f}")
    print(f"  Fitted C_GJ (beyond RG): d={r2['C_GJ_from_fit']['d']:.4f}, s={r2['C_GJ_from_fit']['s']:.4f}, b={r2['C_GJ_from_fit']['b']:.4f}")
    print(f"  STATUS: {r2['status']}")

    # Route 3
    print("\n" + "-" * 90)
    print("ROUTE 3: MASS RATIO CONSTRAINTS (LEUTWYLER ELLIPSE)")
    print("-" * 90)
    r3 = route3_mass_ratios()
    print(f"  GU bare m_u/m_d = phi^(-5) = {r3['ratio_gu_bare']:.4f}  |  PDG: {r3['ratio_pdg']:.4f}")
    print(f"  Leutwyler Q = {r3['Q_Leutwyler']}; ellipse LHS (PDG) = {r3['ellipse_LHS_PDG']:.6f}  (target 1)")
    print(f"  r = m_u/m_d from ellipse: {r3['r_ellipse']:.4f}")
    if r3['epoch_adjustments_in_range']:
        print(f"  Epoch (dN_u, dN_d) giving 0.3 < m_u/m_d < 0.6: {r3['epoch_adjustments_in_range']}")
    print(f"  STATUS: {r3['status']}")

    # Summary table: all three routes vs PDG
    print("\n" + "=" * 90)
    print("SUMMARY: C_q BY ROUTE vs PDG-REQUIRED")
    print("=" * 90)
    print(f"\n  {'flavor':>6s}  {'C_q (PDG)':>14s}  {'Route1':>12s}  {'Route2':>12s}  {'Route3':>12s}  {'Notes':>20s}")
    print("  " + "-" * 90)

    notes = {
        'u': 'R1: constituent; R2: no GJ; R3: ratio off',
        'd': 'R1: Sigma_DCSB; R2: GJ d=3; R3: ellipse',
        's': 'R1: not computed; R2: GJ 1/3; R3: ellipse',
        'c': 'R1: heavy; R2: no GJ; R3: N/A',
        'b': 'R1: N/A; R2: GJ b=1, C_RG; R3: N/A',
        't': 'R1: N/A; R2: pole; R3: N/A',
    }
    for q in quark_order:
        cq_pdg = C_q_needed[q]
        # Route 1: only gives constituent/current for u,d; no C_q number
        r1_cq = "—" if q not in ('u', 'd') else "const."
        # Route 2: C_q = m_PDG/m_bare = C_RG * C_GJ; we have C_RG and fitted C_GJ
        r2_cq = cq_pdg  # same as PDG by construction when using fitted C_GJ
        r2_str = f"{r2_cq:.4f}" if isinstance(r2_cq, (int, float)) else "—"
        # Route 3: no direct C_q, only ratio
        r3_cq = "ratio" if q in ('u', 'd', 's') else "—"
        print(f"  {q:>6s}  {cq_pdg:>14.6f}  {r1_cq:>12s}  {r2_str:>12s}  {r3_cq:>12s}  {notes[q]:>20s}")

    print("\n  Honest assessment:")
    print("    • Route 1: Bag formula gives E_per_quark ~862 MeV (R_bag ~0.47 fm); constituent 310 MeV is phenomenological.")
    print("      Sigma_DCSB from GU/NJL not derived (NJL rough ~75 MeV vs needed ~308 MeV).")
    print("    • Route 2: C_RG from 03 script; GJ factors explain GUT ratios; C_q beyond RG still fitted.")
    print("    • Route 3: Bare u/d ratio wrong by ~5; epoch shifts ±1–2 insufficient; ellipse constrains light-quark sector.")
    print("=" * 90)


if __name__ == "__main__":
    main()
