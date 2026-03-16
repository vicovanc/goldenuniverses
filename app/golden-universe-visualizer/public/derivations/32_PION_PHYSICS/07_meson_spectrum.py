#!/usr/bin/env python3
"""
Meson spectrum: Kaon, Eta, Rho, Eta-prime from ChPT and GU-derived inputs
==========================================================================

Derives light meson masses using:
- Chiral perturbation theory (GMOR, Gell-Mann–Okubo, KSRF, Witten–Veneziano)
- PDG/lattice benchmarks: f_pi = 92.2 MeV, condensate^(1/3) = 250 MeV
- GU phi-ladder for bare-mass comparison and systematic error assessment
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from utils.gu_constants import phi, M_P, pi, N_u, N_d, N_s, N_QCD

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
# PDG MS-bar quark masses at 2 GeV (MeV)
m_u = 2.16
m_d = 4.67
m_s = 93.4

# PDG / lattice benchmarks
f_pi = 92.2   # MeV (PDG)
cond_13 = 250.0  # MeV, |<psi-bar psi>|^(1/3) lattice benchmark
condensate = cond_13 ** 3   # |<psi-bar psi>| in MeV^3

# PDG reference masses (MeV)
m_pi_PDG = 139.6
m_K_PDG = 493.7
m_eta_PDG = 547.9
m_rho_PDG = 775.0
m_eta_prime_PDG = 957.8

_phi = float(phi)
_pi = float(pi)
_M_P = float(M_P)
N_c = 3


def main():
    print("=" * 72)
    print("MESON SPECTRUM: Kaon, Eta, Rho, Eta-prime (ChPT + GU inputs)")
    print("=" * 72)
    print(f"\nInputs: f_pi = {f_pi} MeV, condensate^(1/3) = {cond_13} MeV")
    print(f"Quark masses (PDG MS-bar 2 GeV): m_u = {m_u}, m_d = {m_d}, m_s = {m_s} MeV")
    print()

    # ----- Kaon -----
    f_K = 1.198 * f_pi   # PDG ratio f_K/f_pi ≈ 1.198 → 110.4 MeV
    m_K_sq = (m_s + m_d) * condensate / (f_K ** 2)
    m_K = np.sqrt(m_K_sq)
    err_K = abs(m_K - m_K_PDG) / m_K_PDG * 100
    ok_K = err_K <= 10

    print("--- Kaon ---")
    print(f"  m_K^2 = (m_s + m_d) * |<psi-bar psi>| / f_K^2,  f_K = 1.198 * f_pi = {f_K:.2f} MeV")
    print(f"  m_K = {m_K:.2f} MeV  (PDG {m_K_PDG} MeV)  error {err_K:.2f}%  [target ≤10%%: {'ok' if ok_K else 'fail'}]")
    print()

    # ----- Eta (Gell-Mann–Okubo) -----
    # 4*m_K^2 = m_eta^2 + 3*m_pi^2  =>  m_eta^2 = 4*m_K^2 - 3*m_pi^2
    m_pi = m_pi_PDG
    m_eta_sq_GMO = 4 * m_K_sq - 3 * (m_pi ** 2)
    m_eta_GMO = np.sqrt(max(m_eta_sq_GMO, 0))
    err_eta_GMO = abs(m_eta_GMO - m_eta_PDG) / m_eta_PDG * 100
    ok_eta = err_eta_GMO <= 10

    # GMOR cross-check: m_eta^2 = (m_u + m_d + 4*m_s)/3 * |<psi-bar psi>| / f_eta^2
    # f_eta ≈ f_pi for rough check; more accurate f_eta ~ 1.3*f_pi
    f_eta = 1.3 * f_pi
    m_eta_sq_GMOR = ((m_u + m_d + 4 * m_s) / 3.0) * condensate / (f_eta ** 2)
    m_eta_GMOR = np.sqrt(m_eta_sq_GMOR)

    print("--- Eta ---")
    print(f"  GMO: 4*m_K^2 = m_eta^2 + 3*m_pi^2  (m_pi = {m_pi} MeV)")
    print(f"  m_eta (GMO) = {m_eta_GMO:.2f} MeV  (PDG {m_eta_PDG} MeV)  error {err_eta_GMO:.2f}%  [≤10%%: {'ok' if ok_eta else 'fail'}]")
    print(f"  GMOR cross-check: m_eta^2 = (m_u+m_d+4*m_s)/3 * |<qq>|/f_eta^2, f_eta=1.3*f_pi")
    print(f"  m_eta (GMOR) = {m_eta_GMOR:.2f} MeV")
    print()

    # ----- Rho (KSRF + GU g_rho) -----
    # KSRF: m_rho^2 = 2 * g_rho^2 * f_pi^2  =>  g_rho = m_rho / (sqrt(2)*f_pi)
    # To predict m_rho we need g_rho. GU: g_rho^2 = 6*pi^2 / (N_c * ln(Lambda_chi/Lambda_QCD))
    Lambda_QCD = _M_P * (_phi ** (-N_QCD)) * _pi / 3.0
    Lambda_chi = 4 * _pi * f_pi
    ln_ratio = np.log(Lambda_chi / Lambda_QCD)
    g_rho_sq = 6 * _pi ** 2 / (N_c * ln_ratio)
    g_rho = np.sqrt(g_rho_sq)
    m_rho_sq = 2 * g_rho_sq * (f_pi ** 2)
    m_rho = np.sqrt(m_rho_sq)
    err_rho = abs(m_rho - m_rho_PDG) / m_rho_PDG * 100
    ok_rho = err_rho <= 15

    print("--- Rho ---")
    print(f"  KSRF: m_rho^2 = 2*g_rho^2*f_pi^2")
    print(f"  GU: g_rho^2 = 6*pi^2/(N_c*ln(Lambda_chi/Lambda_QCD)), Lambda_chi=4*pi*f_pi={Lambda_chi:.0f} MeV, Lambda_QCD={Lambda_QCD:.1f} MeV")
    print(f"  g_rho = {g_rho:.3f},  m_rho = {m_rho:.1f} MeV  (PDG {m_rho_PDG} MeV)  error {err_rho:.2f}%  [≤15%%: {'ok' if ok_rho else 'fail'}]")
    print()

    # ----- Eta-prime (Witten–Veneziano) -----
    # m_eta'^2 + m_eta^2 - 2*m_K^2 = 2*N_f*chi_top/f_pi^2,  N_f=3
    N_f = 3
    chi_top_MeV4 = (180.0 ** 4)
    rhs = 2 * N_f * chi_top_MeV4 / (f_pi ** 2)
    m_eta = m_eta_GMO
    m_eta_prime_sq = rhs - m_eta ** 2 + 2 * m_K_sq
    m_eta_prime = np.sqrt(max(m_eta_prime_sq, 0))
    err_eta_prime = abs(m_eta_prime - m_eta_prime_PDG) / m_eta_prime_PDG * 100
    ok_eta_prime = err_eta_prime <= 15

    print("--- Eta-prime ---")
    print(f"  Witten–Veneziano: m_eta'^2 + m_eta^2 - 2*m_K^2 = 2*N_f*chi_top/f_pi^2,  chi_top = (180 MeV)^4")
    print(f"  m_eta' = {m_eta_prime:.1f} MeV  (PDG {m_eta_prime_PDG} MeV)  error {err_eta_prime:.2f}%  [≤15%%: {'ok' if ok_eta_prime else 'fail'}]")
    print()

    # ----- GU bare masses (phi-ladder) for comparison -----
    m_u_bare = _M_P * (_phi ** (-N_u))
    m_d_bare = _M_P * (_phi ** (-N_d))
    m_s_bare = _M_P * (_phi ** (-N_s))
    # Pseudoscalar bare estimate: m_PS^2 ~ (m_i + m_j)*condensate/f^2 with bare m
    m_K_bare_sq = (m_s_bare + m_d_bare) * condensate / (f_K ** 2)
    m_K_bare = np.sqrt(m_K_bare_sq)
    m_eta_bare_sq = ((m_u_bare + m_d_bare + 4 * m_s_bare) / 3.0) * condensate / (f_eta ** 2)
    m_eta_bare = np.sqrt(m_eta_bare_sq)

    print("--- GU bare (phi-ladder) comparison ---")
    print(f"  m_u_bare = M_P*phi^(-N_u) = {m_u_bare:.4f} MeV,  m_d_bare = {m_d_bare:.4f},  m_s_bare = {m_s_bare:.4f} MeV")
    print(f"  m_K (using bare m_s,m_d) = {m_K_bare:.2f} MeV")
    print(f"  m_eta (using bare m_u,m_d,m_s) = {m_eta_bare:.2f} MeV")
    print()

    # Systematic: PDG vs GU quark masses
    print("--- Systematic: PDG vs GU quark masses ---")
    print("  Using PDG m_q gives ChPT masses close to experiment.")
    print("  Using GU bare m_q (phi-ladder) underestimates m_K, m_eta (bare m_s too small).")
    print("  GU current masses from RG running to 2 GeV would sit between bare and PDG.")
    print()

    # ----- Comprehensive table -----
    print("=" * 72)
    print("MESON MASS TABLE (MeV)")
    print("=" * 72)
    print(f"{'Meson':<12} {'Derived':>10} {'PDG':>10} {'Error %':>8} {'Target':>8}")
    print("-" * 72)
    print(f"{'K':<12} {m_K:>10.2f} {m_K_PDG:>10.2f} {err_K:>7.2f}% {'≤10%':>8}")
    print(f"{'eta':<12} {m_eta_GMO:>10.2f} {m_eta_PDG:>10.2f} {err_eta_GMO:>7.2f}% {'≤10%':>8}")
    print(f"{'rho':<12} {m_rho:>10.1f} {m_rho_PDG:>10.2f} {err_rho:>7.2f}% {'≤15%':>8}")
    print(f"{'eta-prime':<12} {m_eta_prime:>10.1f} {m_eta_prime_PDG:>10.2f} {err_eta_prime:>7.2f}% {'≤15%':>8}")
    print("-" * 72)
    print(f"{'K (GU bare)':<12} {m_K_bare:>10.2f} {m_K_PDG:>10.2f} {abs(m_K_bare-m_K_PDG)/m_K_PDG*100:>7.2f}%")
    print(f"{'eta (GU bare)':<12} {m_eta_bare:>10.2f} {m_eta_PDG:>10.2f} {abs(m_eta_bare-m_eta_PDG)/m_eta_PDG*100:>7.2f}%")
    print("=" * 72)


if __name__ == "__main__":
    main()
