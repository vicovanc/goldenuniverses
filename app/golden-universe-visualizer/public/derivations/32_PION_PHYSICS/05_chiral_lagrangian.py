#!/usr/bin/env python3
"""
Leading-order chiral Lagrangian with GU-derived parameters
==========================================================

LO chiral Lagrangian:
  L = (f_pi^2/4) * Tr(d_mu U^dag d^mu U) + (f_pi^2/4) * Tr(chi^dag U + U^dag chi)
  U = exp(i*pi*tau/f_pi),  chi = 2*B_0 * M_q,  B_0 = |<psi-bar psi>| / f_pi^2

Computes: B_0, m_pi, m_K, m_eta, pi-pi scattering lengths (Weinberg),
          pi-N Weinberg-Tomozawa scattering length.
Uses GU scales (phi, M_P, Lambda_QCD) and NJL-derived f_pi and condensate.
numpy only; no mpmath.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from utils.gu_constants import N_u, N_d, N_s, CODATA

# ---------------------------------------------------------------------------
# GU and mathematical constants (float, no mpmath)
# ---------------------------------------------------------------------------
phi = (1.0 + np.sqrt(5.0)) / 2.0
pi = np.pi
M_P = 1.22089e22   # MeV
Lambda_QCD = (pi / 3.0) * M_P * (phi ** (-95))
Lambda_f = float(Lambda_QCD)
N_colors = 3

# ---------------------------------------------------------------------------
# GU-derived chiral parameters (NJL)
# ---------------------------------------------------------------------------
M_const = 310.0
Lambda_NJL = 631.4
EL = np.sqrt(Lambda_NJL**2 + M_const**2)
I_1 = Lambda_NJL * EL / 2.0 - (M_const**2 / 2.0) * np.log((Lambda_NJL + EL) / M_const)
cond_njl = -N_colors / (pi**2) * M_const * I_1   # <psi-bar psi> ~ -(243 MeV)^3
f_pi = np.sqrt(N_colors / (4 * pi**2) * M_const**2 * np.log(1 + Lambda_NJL**2 / M_const**2))

# B_0 from LO definition: B_0 = |<psi-bar psi>| / f_pi^2
cond_abs = np.abs(cond_njl)
B_0 = cond_abs / (f_pi**2)

# ---------------------------------------------------------------------------
# Quark masses (PDG MS-bar at 2 GeV, MeV)
# ---------------------------------------------------------------------------
m_u_pdg = 2.16
m_d_pdg = 4.67
m_s_pdg = 93.4
m_hat = (m_u_pdg + m_d_pdg) / 2.0

# GU bare (from phi-ladder) for reference
m_u_bare = float(M_P * phi**(-N_u))
m_d_bare = float(M_P * phi**(-N_d))
m_s_bare = float(M_P * phi**(-N_s))

# ---------------------------------------------------------------------------
# Experimental / PDG reference values
# ---------------------------------------------------------------------------
m_pi_exp = 139.570   # charged pion, MeV
m_pi0_exp = 134.977  # neutral
m_K_exp = 493.677    # charged kaon
m_eta_exp = 547.862  # eta
m_N_exp = CODATA['proton']   # nucleon mass for pi-N
a00_exp = 0.220
a02_exp = -0.0444

# ---------------------------------------------------------------------------
# LO chiral Lagrangian predictions
# ---------------------------------------------------------------------------

# 1. B_0 (already computed above)
# 2. Pion mass: m_pi^2 = B_0 * (m_u + m_d) = 2*B_0*m_hat
m_pi_sq = 2.0 * B_0 * m_hat
m_pi = np.sqrt(m_pi_sq)

# 3. Kaon mass: m_K^2 = B_0 * (m_u + m_s) for K+ (u bar s)
m_K_sq = B_0 * (m_u_pdg + m_s_pdg)
m_K = np.sqrt(m_K_sq)

# 4. Eta mass (Gell-Mann-Okubo): m_eta^2 = B_0 * (m_u + m_d + 4*m_s) / 3
m_eta_sq = B_0 * (m_u_pdg + m_d_pdg + 4.0 * m_s_pdg) / 3.0
m_eta = np.sqrt(m_eta_sq)

# 5. Weinberg pi-pi scattering lengths (LO)
# a_0^0 = 7*m_pi^2/(32*pi*f_pi^2),  a_0^2 = -m_pi^2/(16*pi*f_pi^2)
a00 = 7.0 * m_pi_sq / (32.0 * pi * f_pi**2)
a02 = -m_pi_sq / (16.0 * pi * f_pi**2)

# 6. Weinberg-Tomozawa pi-N scattering length (simplified LO)
# a_(pi-N) = m_pi/(8*pi*f_pi^2) * (m_N + m_pi)^(-1) [isospin factor 2 for WT]
# Dimension: 1/MeV. Convert to fm: 1 fm = 1/197.327 MeV^{-1}
m_N = m_N_exp
a_piN_WT = (m_pi / (8.0 * pi * f_pi**2)) * (1.0 / (m_N + m_pi))
hbar_c_MeV_fm = 197.327
a_piN_fm = a_piN_WT * hbar_c_MeV_fm   # in fm

# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
def main():
    print("=" * 78)
    print("LEADING-ORDER CHIRAL LAGRANGIAN WITH GU-DERIVED PARAMETERS")
    print("=" * 78)
    print("\n  LO Lagrangian: L = (f_pi^2/4) Tr(d_mu U^dag d^mu U) + (f_pi^2/4) Tr(chi^dag U + U^dag chi)")
    print("  U = exp(i*pi*tau/f_pi),  chi = 2*B_0*M_q,  B_0 = |<psi-bar psi>|/f_pi^2")

    print("\n" + "-" * 78)
    print("  GU SCALES (numpy, no mpmath)")
    print("-" * 78)
    print(f"  phi         = (1+sqrt(5))/2 = {phi:.10f}")
    print(f"  M_P         = {M_P:.3e} MeV")
    print(f"  Lambda_QCD  = (pi/3)*M_P*phi^(-95) = {Lambda_f:.2f} MeV")

    print("\n" + "-" * 78)
    print("  GU-DERIVED CHIRAL INPUTS (NJL)")
    print("-" * 78)
    print(f"  f_pi        = {f_pi:.2f} MeV  (NJL Pagels-Stokar)")
    print(f"  |<psi-bar psi>|^(1/3) = {cond_abs**(1/3):.1f} MeV")
    print(f"  B_0         = |cond|/f_pi^2 = {B_0:.2f} MeV")

    print("\n" + "-" * 78)
    print("  QUARK MASSES (PDG MS-bar at 2 GeV)")
    print("-" * 78)
    print(f"  m_u = {m_u_pdg} MeV,  m_d = {m_d_pdg} MeV,  m_s = {m_s_pdg} MeV")
    print(f"  m_hat = (m_u+m_d)/2 = {m_hat:.2f} MeV")
    print(f"  GU bare: m_u = {m_u_bare:.4f}, m_d = {m_d_bare:.4f}, m_s = {m_s_bare:.4f} MeV")

    print("\n" + "-" * 78)
    print("  CHIRAL PREDICTIONS (LO)")
    print("-" * 78)
    print(f"  1. B_0 = |<psi-bar psi>|/f_pi^2 = {B_0:.2f} MeV")
    print(f"  2. m_pi^2 = 2*B_0*m_hat  ->  m_pi = {m_pi:.2f} MeV   (exp: {m_pi_exp:.2f})")
    print(f"  3. m_K^2 = B_0*(m_u+m_s) ->  m_K  = {m_K:.2f} MeV   (exp: {m_K_exp:.2f})")
    print(f"  4. m_eta^2 = B_0*(m_u+m_d+4*m_s)/3 -> m_eta = {m_eta:.2f} MeV   (exp: {m_eta_exp:.2f})")
    print(f"  5. pi-pi scattering (Weinberg LO):")
    print(f"     a_0^0 = 7*m_pi^2/(32*pi*f_pi^2) = {a00:.4f}   (exp: {a00_exp})")
    print(f"     a_0^2 = -m_pi^2/(16*pi*f_pi^2)  = {a02:.4f}   (exp: {a02_exp})")
    print(f"  6. pi-N Weinberg-Tomozawa (simplified LO):")
    print(f"     a_(pi-N) = m_pi/(8*pi*f_pi^2*(m_N+m_pi)) = {a_piN_WT:.6e} MeV^-1 = {a_piN_fm:.4f} fm")

    print("\n" + "=" * 78)
    print("  SUMMARY: CHIRAL PREDICTIONS vs EXPERIMENT")
    print("=" * 78)
    rows = [
        ("m_pi (MeV)", m_pi, m_pi_exp, (m_pi - m_pi_exp) / m_pi_exp * 100),
        ("m_K (MeV)", m_K, m_K_exp, (m_K - m_K_exp) / m_K_exp * 100),
        ("m_eta (MeV)", m_eta, m_eta_exp, (m_eta - m_eta_exp) / m_eta_exp * 100),
        ("a_0^0", a00, a00_exp, (a00 - a00_exp) / a00_exp * 100 if a00_exp != 0 else 0),
        ("a_0^2", a02, a02_exp, (a02 - a02_exp) / np.abs(a02_exp) * 100 if a02_exp != 0 else 0),
    ]
    print(f"\n  {'Quantity':<14}  {'LO prediction':>14}  {'Experiment':>12}  {'Error %':>10}")
    print("  " + "-" * 54)
    for name, pred, exp_val, err_pct in rows:
        print(f"  {name:<14}  {pred:>14.4f}  {exp_val:>12.4f}  {err_pct:>+9.2f}%")
    print("\n  (LO uses GU f_pi ~ 109 MeV and NJL condensate; PDG quark masses.)")
    print("  (Scattering lengths in units of m_pi^{-1}; experiment from NA48/2, etc.)")


if __name__ == "__main__":
    main()
