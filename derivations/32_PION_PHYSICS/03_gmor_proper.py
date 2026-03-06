#!/usr/bin/env python3
"""
PROPER GMOR RELATION — ALL GU-DERIVED INPUTS (SELF-CONTAINED)
=============================================================

Gell-Mann–Oakes–Renner:  m_pi^2 * f_pi^2 = -(m_u + m_d) * <psi-bar psi>

All inputs from GU or self-contained NJL:
  - Lambda_QCD from GU; Lambda_NJL candidates from GU
  - NJL gap, condensate, f_pi (Pagels–Stokar) solved self-contained
  - Quark masses: PDG (Scenarios A, B) or GU bare phi-ladder (Scenario C)

BENCHMARK: m_pi = 139.570 MeV (PDG charged pion). Target: within 10%.
"""

import sys
import os
import numpy as np

# Path for utils.gu_constants (derivations/utils/)
_derivations = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
if _derivations not in sys.path:
    sys.path.insert(0, _derivations)

from utils.gu_constants import phi, M_P, pi, N_u, N_d, N_s, N_QCD, alpha_EM

# Float versions for numerical work
phi_f = float(phi)
M_P_MeV = float(M_P)   # 1.22089e22 MeV
pi_f = float(pi)

# ---------------------------------------------------------------------------
# GU-derived inputs
# ---------------------------------------------------------------------------

# Lambda_QCD = M_P * phi^(-95) * pi/3  (MeV)
Lambda_QCD = M_P_MeV * (phi_f ** (-N_QCD)) * (pi_f / 3)

# NJL cutoff candidates (GU-derived)
Lambda_NJL_A = (2 * pi_f / phi_f) * Lambda_QCD   # (2*pi/phi)*Lambda_QCD
Lambda_NJL_B = phi_f * pi_f * Lambda_QCD         # phi*pi*Lambda_QCD

# PDG current masses (MS-bar at 2 GeV), MeV
m_u_PDG = 2.16
m_d_PDG = 4.67
m_avg_current = (m_u_PDG + m_d_PDG) / 2

# GU bare quark masses (phi-ladder, no C_q)
m_u_bare = M_P_MeV * (phi_f ** (-N_u))
m_d_bare = M_P_MeV * (phi_f ** (-N_d))

N_c = 3
m_pi_PDG = 139.570  # MeV (charged pion)

# ---------------------------------------------------------------------------
# NJL: self-contained gap, condensate, f_pi
# ---------------------------------------------------------------------------

def I_1(M, Lambda):
    """NJL loop integral I_1(M, Lambda)."""
    E_L = np.sqrt(Lambda**2 + M**2)
    return Lambda * E_L / 2 - (M**2 / 2) * np.log((Lambda + E_L) / M)


def solve_gap(m_current, Lambda, G_times_Lambda_sq=9.0, M_init=300.0, tol=1e-6, max_iter=200):
    """
    Gap equation: M = m + G*N_c/pi^2 * M * I_1(M, Lambda).
    G set by G*Lambda^2 = G_times_Lambda_sq.
    Returns (M_constituent, G).
    """
    G = G_times_Lambda_sq / (Lambda ** 2)
    M = M_init
    for _ in range(max_iter):
        I1 = I_1(M, Lambda)
        M_new = m_current + G * N_c / (pi_f ** 2) * M * I1
        if abs(M_new - M) < tol:
            return M_new, G
        M = M_new
    return M, G


def condensate_njl(M, Lambda):
    """<psi-bar psi> = -N_c/(2*pi^2) * [M*Lambda*E_L/2 - M^3/2 * ln((Lambda+E_L)/M)]"""
    E_L = np.sqrt(Lambda**2 + M**2)
    bracket = M * Lambda * E_L / 2 - (M**3 / 2) * np.log((Lambda + E_L) / M)
    return -N_c / (2 * pi_f**2) * bracket


def f_pi_sq_pagels_stokar(M, Lambda):
    """f_pi^2 = N_c*M^2/(4*pi^2) * [ln((Lambda+E_L)/M) - Lambda/E_L]"""
    E_L = np.sqrt(Lambda**2 + M**2)
    bracket = np.log((Lambda + E_L) / M) - Lambda / E_L
    return N_c * (M**2) / (4 * pi_f**2) * bracket


def gmor_m_pi_sq(m_u_plus_m_d, cond, f_pi_sq):
    """m_pi^2 = -(m_u + m_d) * <psi-bar psi> / f_pi^2."""
    return -(m_u_plus_m_d) * cond / f_pi_sq


# ---------------------------------------------------------------------------
# Run scenarios
# ---------------------------------------------------------------------------

def run_scenario(name, Lambda_NJL, m_u, m_d, label_quark):
    """Solve NJL with given Lambda and quark masses; return dict of results."""
    m_avg = (m_u + m_d) / 2
    M, G = solve_gap(m_avg, Lambda_NJL, G_times_Lambda_sq=9.0, M_init=300.0)
    cond = condensate_njl(M, Lambda_NJL)
    f_pi_sq = f_pi_sq_pagels_stokar(M, Lambda_NJL)
    f_pi = np.sqrt(f_pi_sq)
    m_pi_sq = gmor_m_pi_sq(m_u + m_d, cond, f_pi_sq)
    m_pi = np.sqrt(max(0, m_pi_sq))
    err_pct = (m_pi - m_pi_PDG) / m_pi_PDG * 100
    cbrt_cond = abs(cond)**(1/3)
    return {
        "name": name,
        "Lambda_NJL": Lambda_NJL,
        "label_quark": label_quark,
        "m_u": m_u, "m_d": m_d,
        "M": M, "G": G,
        "cond": cond, "cbrt_cond": cbrt_cond,
        "f_pi": f_pi, "f_pi_sq": f_pi_sq,
        "m_pi": m_pi, "m_pi_sq": m_pi_sq,
        "err_pct": err_pct,
    }


def main():
    print("=" * 90)
    print("GMOR PION MASS — GU-DERIVED INPUTS (SELF-CONTAINED)")
    print("=" * 90)

    print("\n--- GU-derived inputs (from utils.gu_constants) ---")
    print(f"  phi = {phi_f:.10f}")
    print(f"  M_P = {M_P_MeV:.5e} MeV")
    print(f"  N_QCD = {N_QCD}  →  Lambda_QCD = M_P * phi^(-N_QCD) * pi/3")
    print(f"  Lambda_QCD = {Lambda_QCD:.4f} MeV")
    print(f"  Lambda_NJL candidate A: (2*pi/phi)*Lambda_QCD = {Lambda_NJL_A:.4f} MeV")
    print(f"  Lambda_NJL candidate B: phi*pi*Lambda_QCD     = {Lambda_NJL_B:.4f} MeV")
    print(f"  PDG: m_u = {m_u_PDG} MeV, m_d = {m_d_PDG} MeV  (MS-bar @ 2 GeV)")
    print(f"  GU bare (no C_q): m_u = M_P*phi^(-N_u) = {m_u_bare:.6f} MeV, m_d = {m_d_bare:.6f} MeV")

    print("\n" + "-" * 90)
    print("Scenario A: PDG quark masses + NJL with Lambda = (2*pi/phi)*Lambda_QCD")
    print("-" * 90)
    rA = run_scenario("A", Lambda_NJL_A, m_u_PDG, m_d_PDG, "PDG")
    _print_result(rA)

    print("\n" + "-" * 90)
    print("Scenario B: PDG quark masses + NJL with Lambda = phi*pi*Lambda_QCD")
    print("-" * 90)
    rB = run_scenario("B", Lambda_NJL_B, m_u_PDG, m_d_PDG, "PDG")
    _print_result(rB)

    print("\n" + "-" * 90)
    print("Scenario C: GU bare quark masses (no C_q) + NJL (Lambda_A) — why it fails")
    print("-" * 90)
    rC = run_scenario("C", Lambda_NJL_A, m_u_bare, m_d_bare, "GU bare")
    _print_result(rC)
    print(f"  → GU bare m_u + m_d = {m_u_bare + m_d_bare:.4f} MeV << PDG {m_u_PDG + m_d_PDG} MeV")
    print("  → m_pi^2 ∝ (m_u+m_d) ⇒ pion mass far too low without C_q calibration.")

    print("\n" + "=" * 90)
    print("SUMMARY")
    print("=" * 90)
    print(f"  PDG m_pi = {m_pi_PDG} MeV.  Target: within 10%.")
    for r in (rA, rB, rC):
        ok = "✓ within 10%" if abs(r["err_pct"]) <= 10 else "✗"
        print(f"  Scenario {r['name']}: m_pi = {r['m_pi']:.2f} MeV  (error {r['err_pct']:+.1f}%)  {ok}")
    print()


def _print_result(r):
    print(f"  Lambda_NJL = {r['Lambda_NJL']:.2f} MeV   quark masses: {r['label_quark']}")
    print(f"  Constituent M = {r['M']:.2f} MeV   G*Lambda^2 = 9.0")
    print(f"  <psi-bar psi>^(1/3) = {r['cbrt_cond']:.2f} MeV   f_pi = {r['f_pi']:.2f} MeV")
    print(f"  m_pi = {r['m_pi']:.2f} MeV   (PDG 139.57 MeV, error {r['err_pct']:+.1f}%)")


if __name__ == "__main__":
    main()
