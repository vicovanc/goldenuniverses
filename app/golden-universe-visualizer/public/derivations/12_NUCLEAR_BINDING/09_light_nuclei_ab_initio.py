#!/usr/bin/env python3
"""
AB INITIO LIGHT NUCLEI WITH GU-DERIVED NUCLEAR POTENTIAL
========================================================

Computes binding energies for deuteron, He-3, He-4 using a simplified
GU nuclear potential V_NN = V_OPEP + V_short + V_memory and simple
variational wave functions. Purpose: show the GU potential gives
reasonable nuclear physics (order-of-magnitude and trends).

Limitations: Simple product/variational ansätze do not reproduce exact
binding energies; full ab initio would require proper few-body methods
and tensor/spin-orbit terms.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar

from utils.gu_constants import CODATA

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
phi = (1 + np.sqrt(5)) / 2
M_P = 1.22089e22  # MeV
hbar_c = 197.3269804  # MeV·fm
pi = np.pi

# Nucleon mass (use proton from CODATA; deuteron uses average N mass)
m_N = CODATA["proton"]  # 938.272 MeV
m_pi_pdg = 139.57   # MeV (PDG)
g_piNN_pdg = 12.97  # PDG-style coupling

# GU-derived (from 07_opep / 32_pion): Lambda_QCD, f_pi, g_piNN_gu, m_pi_gu
Lambda_QCD = float((pi / 3) * M_P * phi**(-95))
# V_0 = (4*pi/phi) * Lambda_QCD
V_0 = (4 * pi / phi) * Lambda_QCD  # MeV
R_short = 0.4675   # fm (GU bag radius)
C_mem = 1.283
sigma = 2 * pi * (179.0 / 197.3269804)**2  # MeV/fm
R_mem = hbar_c / 179.0  # fm

# GU pion/nucleon (for "pure GU" run): from 07_opep
f_pi_njl = 109.4   # ~NJL/ Pagels-Stokar
g_A = 1.2754
g_piNN_gu = g_A * m_N / f_pi_njl
m_pi_gu = 90.4     # MeV (GU from GMOR/NJL)


def V_OPEP(r_fm, m_pi, g_piNN, m_N_MeV):
    """Central OPEP: -(g_piNN^2/4pi) * m_pi^3/(4*m_N^2) * exp(-m_pi*r/hbar_c)/(m_pi*r/hbar_c) / hbar_c."""
    if r_fm <= 1e-12:
        return 0.0
    x = m_pi * r_fm / hbar_c
    yukawa = np.exp(-x) / x
    pref = -(g_piNN**2 / (4 * pi)) * (m_pi**3 / (4 * m_N_MeV**2)) / hbar_c
    return pref * yukawa


def V_short(r_fm):
    """V_0 * exp(-r^2/(2*R^2))."""
    return V_0 * np.exp(-r_fm**2 / (2 * R_short**2))


def V_memory(r_fm):
    """-C_mem * sigma * r * exp(-r/R_mem)."""
    return -C_mem * sigma * r_fm * np.exp(-r_fm / R_mem)


def V_NN(r_fm, m_pi, g_piNN, m_N_MeV):
    """Full central potential V_OPEP + V_short + V_memory (MeV)."""
    return V_OPEP(r_fm, m_pi, g_piNN, m_N_MeV) + V_short(r_fm) + V_memory(r_fm)


# ---------------------------------------------------------------------------
# Deuteron (A=2): variational with psi = N * exp(-alpha*r)
# u(r) = r*psi => u = r*exp(-alpha*r). Normalization: N^2 = alpha^3/pi.
# <T> = (hbar_c)^2 * alpha^2 / (2*mu), mu = m_N/2.
# <V> = 4*pi * N^2 * int_0^inf V(r) exp(-2*alpha*r) r^2 dr.
# ---------------------------------------------------------------------------
def deuteron_energy(alpha, m_pi, g_piNN, m_N_MeV):
    mu = m_N_MeV / 2.0
    if alpha <= 0:
        return 1e10
    N_sq = alpha**3 / pi
    T = (hbar_c**2) * (alpha**2) / (2 * mu)

    def integrand(r):
        if r <= 1e-12:
            return 0.0
        return V_NN(r, m_pi, g_piNN, m_N_MeV) * np.exp(-2 * alpha * r) * r**2

    V_int, _ = quad(integrand, 0, np.inf, limit=200)
    V = 4 * pi * N_sq * V_int
    return T + V


def solve_deuteron(m_pi, g_piNN, m_N_MeV):
    res = minimize_scalar(
        lambda a: deuteron_energy(a, m_pi, g_piNN, m_N_MeV),
        bounds=(0.002, 3.0),
        method="bounded",
    )
    E = res.fun
    alpha_opt = res.x
    return -E if E < 0 else 0.0, alpha_opt, E


# ---------------------------------------------------------------------------
# He-3 (A=3): 3 pairs. Crude model: E = 3 * [ (hbar_c)^2 alpha^2/(2*mu) + <V_NN> ].
# ---------------------------------------------------------------------------
def he3_energy(alpha, m_pi, g_piNN, m_N_MeV):
    mu = m_N_MeV / 2.0
    if alpha <= 0:
        return 1e10
    N_sq = alpha**3 / pi
    T_per_pair = (hbar_c**2) * (alpha**2) / (2 * mu)
    def integrand(r):
        if r <= 1e-12:
            return 0.0
        return V_NN(r, m_pi, g_piNN, m_N_MeV) * np.exp(-2 * alpha * r) * r**2
    V_int, _ = quad(integrand, 0, np.inf, limit=200)
    V_per_pair = 4 * pi * N_sq * V_int
    return 3 * (T_per_pair + V_per_pair)


def solve_he3(m_pi, g_piNN, m_N_MeV):
    res = minimize_scalar(
        lambda a: he3_energy(a, m_pi, g_piNN, m_N_MeV),
        bounds=(0.002, 3.0),
        method="bounded",
    )
    E = res.fun
    return -E if E < 0 else 0.0, E


# ---------------------------------------------------------------------------
# He-4 (A=4): 6 pairs. E = 6 * [ T_per_pair + <V_NN> ].
# ---------------------------------------------------------------------------
def he4_energy(alpha, m_pi, g_piNN, m_N_MeV):
    mu = m_N_MeV / 2.0
    if alpha <= 0:
        return 1e10
    N_sq = alpha**3 / pi
    T_per_pair = (hbar_c**2) * (alpha**2) / (2 * mu)
    def integrand(r):
        if r <= 1e-12:
            return 0.0
        return V_NN(r, m_pi, g_piNN, m_N_MeV) * np.exp(-2 * alpha * r) * r**2
    V_int, _ = quad(integrand, 0, np.inf, limit=200)
    V_per_pair = 4 * pi * N_sq * V_int
    return 6 * (T_per_pair + V_per_pair)


def solve_he4(m_pi, g_piNN, m_N_MeV):
    res = minimize_scalar(
        lambda a: he4_energy(a, m_pi, g_piNN, m_N_MeV),
        bounds=(0.002, 3.0),
        method="bounded",
    )
    E = res.fun
    return -E if E < 0 else 0.0, E


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("AB INITIO LIGHT NUCLEI — GU NUCLEAR POTENTIAL")
    print("=" * 70)
    print("\nPotential: V_NN = V_OPEP + V_short + V_memory")
    print("  V_OPEP:  -(g_piNN^2/4pi) * m_pi^3/(4*m_N^2) * exp(-m_pi*r/hbar_c)/(m_pi*r/hbar_c) / hbar_c")
    print("  V_short: V_0 * exp(-r^2/(2*R^2)),  V_0 = (4*pi/phi)*Lambda_QCD,  R = 0.4675 fm")
    print("  V_memory: -C_mem * sigma * r * exp(-r/R_mem),  R_mem = hbar_c/179 fm")
    print(f"\nConstants: phi = {phi:.6f},  hbar_c = {hbar_c} MeV·fm,  m_N = {m_N:.3f} MeV")
    print(f"  Lambda_QCD = {Lambda_QCD:.2f} MeV,  V_0 = {V_0:.1f} MeV,  R_short = {R_short} fm")
    print(f"  C_mem = {C_mem},  sigma = {sigma:.4f} MeV/fm,  R_mem = {R_mem:.4f} fm")

    # PDG parameters
    print("\n" + "-" * 70)
    print("PARAMETER SET: GU–PDG (m_pi, g_piNN from PDG/experiment)")
    print(f"  m_pi = {m_pi_pdg} MeV,  g_piNN = {g_piNN_pdg}")
    print("-" * 70)

    BE_d_pdg, alpha_d_pdg, E_d_pdg = solve_deuteron(m_pi_pdg, g_piNN_pdg, m_N)
    print(f"\n1. DEUTERON (A=2)")
    print(f"   Experimental:  B.E. = 2.225 MeV,  r_rms ≈ 1.97 fm")
    print(f"   GU–PDG:       B.E. = {BE_d_pdg:.4f} MeV  (alpha = {alpha_d_pdg:.4f} fm^-1, E_min = {E_d_pdg:.6f} MeV)")

    BE_he3_pdg, E_he3_pdg = solve_he3(m_pi_pdg, g_piNN_pdg, m_N)
    print(f"\n2. HELIUM-3 (A=3, ppn)")
    print(f"   Experimental:  B.E. = 7.718 MeV")
    print(f"   GU–PDG:       B.E. = {BE_he3_pdg:.4f} MeV")

    BE_he4_pdg, E_he4_pdg = solve_he4(m_pi_pdg, g_piNN_pdg, m_N)
    print(f"\n3. HELIUM-4 (A=4, ppnn)")
    print(f"   Experimental:  B.E. = 28.296 MeV")
    print(f"   GU–PDG:       B.E. = {BE_he4_pdg:.4f} MeV")

    # Pure GU parameters
    print("\n" + "-" * 70)
    print("PARAMETER SET: PURE GU (m_pi, g_piNN from GU/NJL)")
    print(f"  m_pi = {m_pi_gu} MeV,  g_piNN = {g_piNN_gu:.4f}")
    print("-" * 70)

    BE_d_gu, alpha_d_gu, _ = solve_deuteron(m_pi_gu, g_piNN_gu, m_N)
    print(f"\n1. DEUTERON:  B.E.(pure GU) = {BE_d_gu:.4f} MeV  (alpha = {alpha_d_gu:.4f} fm^-1)")

    BE_he3_gu, _ = solve_he3(m_pi_gu, g_piNN_gu, m_N)
    print(f"2. HELIUM-3:  B.E.(pure GU) = {BE_he3_gu:.4f} MeV")

    BE_he4_gu, _ = solve_he4(m_pi_gu, g_piNN_gu, m_N)
    print(f"3. HELIUM-4:  B.E.(pure GU) = {BE_he4_gu:.4f} MeV")

    # Summary table
    print("\n" + "=" * 70)
    print("SUMMARY TABLE")
    print("=" * 70)
    print(f"  {'Nucleus':<12} {'B.E.(exp) [MeV]':<18} {'B.E.(GU-PDG) [MeV]':<22} {'B.E.(pure GU) [MeV]':<22} {'Error (GU-PDG)':<16}")
    print("-" * 70)
    for name, exp, pdg, gu in [
        ("Deuteron", 2.225, BE_d_pdg, BE_d_gu),
        ("He-3", 7.718, BE_he3_pdg, BE_he3_gu),
        ("He-4", 28.296, BE_he4_pdg, BE_he4_gu),
    ]:
        err = abs(pdg - exp) / exp * 100 if exp else 0
        print(f"  {name:<12} {exp:<18.3f} {pdg:<22.4f} {gu:<22.4f} {err:.1f}%")
    print("-" * 70)

    print("\nLimitations:")
    print("  - Simple variational ansätze (single exponent per pair) do not reproduce")
    print("    exact binding; full ab initio requires proper few-body methods, tensor")
    print("    and spin-orbit terms, and three-body forces.")
    print("  - This script uses a central-only potential; the GU repulsive core (V_short)")
    print("    is strong at short range, so the single-exponential trial may not find a")
    print("    bound state. Realistic binding requires tensor OPEP and tuned short-range")
    print("    terms.")
    print("  - Purpose: show the GU-derived potential structure; with full physics it")
    print("    can give reasonable nuclear binding (order and trend: d < He-3 < He-4).")
    print("=" * 70)


if __name__ == "__main__":
    main()
