#!/usr/bin/env python3
"""
COMPLETE NUCLEON-NUCLEON POTENTIAL FROM GU-DERIVED PARAMETERS
=============================================================

V_NN = V_OPEP + V_short + V_memory

  V_OPEP:   One-pion exchange (central + tensor)
  V_short:  Short-range repulsion from quark-gluon overlap (bag)
  V_memory: GU memory kernel from Wilson loop area law (confining + screening)

Uses only numpy. Compares PDG vs GU inputs; variational deuteron estimate;
honest assessment of what is derived vs what needs more work.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import numpy as np
from utils.gu_constants import CODATA

# =============================================================================
# CONSTANTS
# =============================================================================
phi = (1 + np.sqrt(5)) / 2
M_P = 1.22089e22   # MeV
hbar_c = 197.3269804  # MeV·fm
Lambda_QCD = (np.pi / 3) * M_P * phi**(-95)
Lambda_QCD = float(Lambda_QCD)

# GU-derived parameters
m_N = 938.272   # MeV (nucleon mass)
m_pi_PDG = 139.57   # MeV (PDG)
m_pi_GU = 90.4      # MeV (GU/NJL)
g_piNN_PDG = 12.97
g_piNN_GU = 10.94
f_pi_PDG = 92.2     # MeV
f_pi_GU = 109.4     # MeV (GU NJL)
R_bag = 0.4675      # fm (GU bag radius)
C_mem = 1.2826      # GU memory coefficient
sigma = 2 * np.pi * Lambda_QCD**2   # string tension (MeV^2)
R_mem = hbar_c / Lambda_QCD         # memory screening length (fm)

# =============================================================================
# OPEP: Y(x), T(x) and V_C
# =============================================================================
def Y(x):
    """Yukawa function: exp(-x)/x."""
    x = np.atleast_1d(np.asarray(x, dtype=float))
    out = np.zeros_like(x)
    ok = x > 1e-12
    out[ok] = np.exp(-x[ok]) / x[ok]
    return float(out.flat[0]) if out.size == 1 else out

def T(x):
    """Tensor function: (1 + 3/x + 3/x^2)*exp(-x)/x."""
    x = np.atleast_1d(np.asarray(x, dtype=float))
    out = np.zeros_like(x)
    ok = x > 1e-12
    out[ok] = (1 + 3/x[ok] + 3/x[ok]**2) * np.exp(-x[ok]) / x[ok]
    return float(out.flat[0]) if out.size == 1 else out

def V_OPEP_central(r_fm, m_pi, g_piNN):
    """Central OPEP: V_C = -(g^2/4pi) * m_pi^3/(4*m_N^2) * Y(m_pi*r/hbar_c) / hbar_c (MeV)."""
    x = m_pi * r_fm / hbar_c
    pref = -(g_piNN**2 / (4 * np.pi)) * (m_pi**3 / (4 * m_N**2)) / hbar_c
    return pref * Y(x)

def V_OPEP_tensor(r_fm, m_pi, g_piNN):
    """Tensor part (same prefactor as central, T instead of Y)."""
    x = m_pi * r_fm / hbar_c
    pref = -(g_piNN**2 / (4 * np.pi)) * (m_pi**3 / (4 * m_N**2)) / hbar_c
    return pref * T(x)

def V_OPEP(r_fm, m_pi, g_piNN, S_sigma=1, S_tau=-3, S12=0):
    """Full OPEP for deuteron (S=1, T=0): S_sigma=1, tau1·tau2=-3, S12=0 for S-wave only."""
    Vc = V_OPEP_central(r_fm, m_pi, g_piNN)
    Vt = V_OPEP_tensor(r_fm, m_pi, g_piNN)
    return S_sigma * S_tau * Vc + S12 * S_tau * Vt

# =============================================================================
# V_short: repulsion from bag overlap
# =============================================================================
V_0_short = (4 * np.pi / phi) * Lambda_QCD   # MeV

def V_short(r_fm):
    """Short-range repulsion: V_0 * exp(-r^2/(2*R_bag^2))."""
    return V_0_short * np.exp(-r_fm**2 / (2 * R_bag**2))

# =============================================================================
# V_memory: Wilson loop area law + screening
# =============================================================================
# sigma is in MeV^2; for V in MeV with r in fm use (sigma/hbar_c) [MeV/fm]
sigma_per_fm = sigma / hbar_c   # MeV/fm

def V_memory(r_fm):
    """GU memory kernel: -C_mem * sigma * r * exp(-r/R_mem), sigma in MeV/fm for r in fm."""
    return -C_mem * sigma_per_fm * r_fm * np.exp(-r_fm / R_mem)

# =============================================================================
# Full V_NN (S-wave deuteron channel: central OPEP only for simplicity)
# =============================================================================
def V_NN(r_fm, m_pi, g_piNN, S_sigma=1, S_tau=-3, S12=0):
    """V_NN = V_OPEP + V_short + V_memory."""
    return (
        V_OPEP(r_fm, m_pi, g_piNN, S_sigma, S_tau, S12)
        + V_short(r_fm)
        + V_memory(r_fm)
    )

# =============================================================================
# TABLES: V_NN(r) for r in [0.2, 5.0] fm, PDG vs GU
# =============================================================================
def main():
    print("=" * 90)
    print("COMPLETE NUCLEON-NUCLEON POTENTIAL: V_NN = V_OPEP + V_short + V_memory")
    print("=" * 90)

    print("\n--- Constants ---")
    print(f"  phi         = {phi:.6f}")
    print(f"  M_P         = {M_P:.3e} MeV")
    print(f"  hbar_c      = {hbar_c:.4f} MeV·fm")
    print(f"  Lambda_QCD  = (pi/3)*M_P*phi^(-95) = {Lambda_QCD:.4f} MeV")
    print(f"  sigma       = 2*pi*Lambda_QCD^2 = {sigma:.2f} MeV^2  ({sigma_per_fm:.2f} MeV/fm)")
    print(f"  R_mem       = hbar_c/Lambda_QCD = {R_mem:.4f} fm")
    print(f"  R_bag       = {R_bag:.4f} fm (GU)")
    print(f"  C_mem       = {C_mem:.4f} (GU)")
    print(f"  V_0_short   = (4*pi/phi)*Lambda_QCD = {V_0_short:.2f} MeV")

    print("\n--- GU-derived vs PDG parameters ---")
    print(f"  m_N         = {m_N} MeV")
    print(f"  m_pi        = {m_pi_PDG} (PDG)  vs  {m_pi_GU} (GU/NJL) MeV")
    print(f"  g_piNN      = {g_piNN_PDG:.2f} (PDG)  vs  {g_piNN_GU:.2f} (GU)")
    print(f"  f_pi        = {f_pi_PDG} (PDG)  vs  {f_pi_GU} (GU NJL) MeV")

    r_vals = np.linspace(0.2, 5.0, 25)
    print("\n" + "-" * 90)
    print("  r [fm]   V_OPEP(PDG)  V_OPEP(GU)   V_short    V_memory   V_NN(PDG)   V_NN(GU)")
    print("-" * 90)
    for r in r_vals:
        v_opep_p = V_OPEP(r, m_pi_PDG, g_piNN_PDG)
        v_opep_g = V_OPEP(r, m_pi_GU, g_piNN_GU)
        v_s = V_short(r)
        v_m = V_memory(r)
        v_nn_p = V_NN(r, m_pi_PDG, g_piNN_PDG)
        v_nn_g = V_NN(r, m_pi_GU, g_piNN_GU)
        print(f"  {r:5.2f}   {v_opep_p:10.2f}   {v_opep_g:10.2f}   {v_s:8.2f}   {v_m:8.2f}   {v_nn_p:8.2f}   {v_nn_g:8.2f}")

    # Dense grid for integration
    r_grid = np.linspace(0.05, 12.0, 1200)

    # -------------------------------------------------------------------------
    # Variational deuteron: trial u(r) = r * exp(-alpha*r), minimize E = <T> + <V>
    # -------------------------------------------------------------------------
    # <T> = (hbar_c)^2 * alpha^2 / mu  (mu = m_N/2), with u normalized: int u^2 dr = 1/(4*alpha^3)
    # so normalized u(r) = 2*alpha^(3/2) * r * exp(-alpha*r)
    mu = m_N / 2

    def kinetic(alpha):
        return (hbar_c**2) * (alpha**2) / mu

    def potential_integral(alpha, m_pi, g_piNN):
        u = 2 * (alpha**1.5) * r_grid * np.exp(-alpha * r_grid)
        u_sq = u**2
        V = V_NN(r_grid, m_pi, g_piNN)
        return np.trapezoid(V * u_sq, r_grid)

    def total_energy(alpha, m_pi, g_piNN):
        return kinetic(alpha) + potential_integral(alpha, m_pi, g_piNN)

    # Minimize over alpha (grid search then refine)
    alphas = np.linspace(0.05, 0.8, 100)
    E_pdg = np.array([total_energy(a, m_pi_PDG, g_piNN_PDG) for a in alphas])
    E_gu = np.array([total_energy(a, m_pi_GU, g_piNN_GU) for a in alphas])
    i_pdg = np.argmin(E_pdg)
    i_gu = np.argmin(E_gu)
    alpha_opt_pdg = alphas[i_pdg]
    alpha_opt_gu = alphas[i_gu]
    E_min_pdg = E_pdg[i_pdg]
    E_min_gu = E_gu[i_gu]

    # Refine with finer grid
    for _ in range(2):
        alphas_fine = np.linspace(max(0.02, alpha_opt_pdg - 0.05), alpha_opt_pdg + 0.05, 50)
        E_fine = np.array([total_energy(a, m_pi_PDG, g_piNN_PDG) for a in alphas_fine])
        alpha_opt_pdg = alphas_fine[np.argmin(E_fine)]
        E_min_pdg = np.min(E_fine)
        alphas_fine = np.linspace(max(0.02, alpha_opt_gu - 0.05), alpha_opt_gu + 0.05, 50)
        E_fine = np.array([total_energy(a, m_pi_GU, g_piNN_GU) for a in alphas_fine])
        alpha_opt_gu = alphas_fine[np.argmin(E_fine)]
        E_min_gu = np.min(E_fine)

    E_d_exp = -2.225  # MeV

    print("\n" + "=" * 90)
    print("DEUTERON BINDING (variational: trial u(r) = r*exp(-alpha*r))")
    print("=" * 90)
    print(f"  Trial: psi ~ exp(-alpha*r)*r  =>  u(r) = 2*alpha^(3/2)*r*exp(-alpha*r),  int u^2 dr = 1")
    print(f"  <T> = (hbar_c)^2 * alpha^2 / mu,  mu = m_N/2")
    print()
    print(f"  PDG inputs:  alpha_opt = {alpha_opt_pdg:.4f} fm^-1   E_min = {E_min_pdg:.4f} MeV")
    print(f"  GU inputs:  alpha_opt = {alpha_opt_gu:.4f} fm^-1   E_min = {E_min_gu:.4f} MeV")
    print(f"  Experimental E_d = {E_d_exp} MeV")
    print(f"  PDG vs exp:  E_min - E_d = {E_min_pdg - E_d_exp:.3f} MeV")
    print(f"  GU vs exp:   E_min - E_d = {E_min_gu - E_d_exp:.3f} MeV")

    # Scattering length estimate: for shallow bound state 1/a_0 ~ sqrt(2*mu*|E_d|)/hbar
    # a_0 ~ hbar_c / sqrt(2*mu*|E_d|) in fm (with E_d in MeV, mu in MeV)
    a_0_exp = 5.42   # fm (experimental nn/pp triplet)
    a_0_est_pdg = hbar_c / np.sqrt(2 * mu * max(1e-6, -E_min_pdg)) if E_min_pdg < 0 else np.nan
    a_0_est_gu = hbar_c / np.sqrt(2 * mu * max(1e-6, -E_min_gu)) if E_min_gu < 0 else np.nan
    print("\n  Scattering length (estimate from binding): a_0 ~ hbar_c/sqrt(2*mu*|E|)")
    print(f"  PDG: a_0 ~ {a_0_est_pdg:.2f} fm   GU: a_0 ~ {a_0_est_gu:.2f} fm   (exp nn ~ {a_0_exp} fm)")

    # -------------------------------------------------------------------------
    # Honest assessment
    # -------------------------------------------------------------------------
    print("\n" + "=" * 90)
    print("HONEST ASSESSMENT: WHAT IS DERIVED VS WHAT NEEDS MORE WORK")
    print("=" * 90)
    print("""
  DERIVED FROM GU (used in this script):
    - Lambda_QCD = (pi/3)*M_P*phi^(-95)  [zero free parameters]
    - sigma = 2*pi*Lambda_QCD^2  [string tension from area law]
    - R_bag = 0.4675 fm  [from GU bag/Y-junction derivation]
    - C_mem = 1.2826  [from pi/sqrt(2*N_c) color-geometry]
    - R_mem = hbar_c/Lambda_QCD  [screening scale]
    - V_0_short = (4*pi/phi)*Lambda_QCD  [bag overlap ansatz]

  INPUT FROM EXPERIMENT / EXTERNAL MODELS:
    - m_N = 938.272 MeV  (PDG; GU proton mass is close but not fixed here)
    - m_pi, g_piNN, f_pi: we compare PDG vs GU/NJL values; GU values come from
      chiral/NJL chains that themselves depend on Lambda_QCD and conventions.

  WHAT NEEDS MORE WORK:
    - Deuteron binding E_d: variational with S-wave-only trial gives a rough
      estimate; tensor force (D-state) and full 3D1-3S1 coupling are needed for
      quantitative agreement with -2.225 MeV.
    - Scattering length a_0: proper calculation requires solving the Schrödinger
      equation at k=0, not just the binding estimate.
    - Short-range repulsion: V_0 and Gaussian width R_bag are GU-motivated but
      the exact form (Gaussian vs other shapes) and strength are model-dependent.
    - Memory kernel: -C_mem*sigma*r*exp(-r/R_mem) is a minimal confining+screening
      form; spin/isospin and channel dependence are not included.
    - OPEP: we use central + tensor with deuteron quantum numbers; full NN
      potential would include 1S0, 3S1-3D1, etc.

  BOTTOM LINE:
    The script builds a consistent V_NN from GU-derived Lambda_QCD, R_bag, and
    C_mem. The structure V_OPEP + V_short + V_memory is physically motivated.
    Quantitative fit to E_d and a_0 would require either refining the short-range
    and memory terms or adding more channels and tensor coupling.
""")
    print("=" * 90)

if __name__ == "__main__":
    main()
