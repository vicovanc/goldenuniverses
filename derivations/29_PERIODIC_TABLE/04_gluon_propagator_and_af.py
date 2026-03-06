#!/usr/bin/env python3
"""
Gluon propagator and asymptotic freedom from GU.

1. Compute alpha_s(IR) as a GU HYPOTHESIS and compare with lattice/perturbative.
   NOTE: The formula alpha_s(IR) = pi^2/b_0 is NOT derived from L_total. It is a
   hypothesis (see derivations/33_PATTERN_K/04_pi_in_coupling_hierarchy.py for analysis).
   "Pattern-2" is an epoch label, not a multiplicative pi^2 factor.
2. Derive gluon condensate from Omega-torus bag constant (replace lattice/SVZ).
3. Compute gluon propagator (UV + IR scenarios) and show asymptotic freedom from GU Lagrangian.
"""

import sys
import os
import numpy as np

# Allow importing from derivations/utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.gu_constants import M_P, phi, pi, N_QCD, alpha_s_MZ

# ---------------------------------------------------------------------------
# Part 1: alpha_s(IR) from GU
# ---------------------------------------------------------------------------
def part1_alpha_s_IR():
    print("=" * 70)
    print("Part 1: alpha_s(IR) — GU HYPOTHESIS vs lattice/perturbative")
    print("=" * 70)

    # GU hypothesis: alpha_s(IR) = pi^2 / b_0
    # NOT derived from L_total — see 33_PATTERN_K/04 for why this is coincidental
    N_f = 3
    b_0 = 11 - 2 * N_f / 3
    alpha_s_IR_GU = float(pi**2) / b_0

    print(f"\nGU HYPOTHESIS (not derived): alpha_s(IR) = pi^2 / b_0 at N_QCD = {N_QCD}")
    print(f"  b_0 = 11 - 2*N_f/3 = {b_0}")
    print(f"  alpha_s_IR = pi^2 / {b_0} = {alpha_s_IR_GU:.6f}")
    print(f"  NOTE: pi^2/b_0 ~ 1.097 is a HYPOTHESIS, not a derivation.")
    print(f"        The pi^2 is coincidental (pi^2 ~ 9.87, b_0 = 9).")
    print(f"        See 33_PATTERN_K/04_pi_in_coupling_hierarchy.py.")

    alpha_s_1GeV_lattice = 0.5
    print(f"\nLattice/perturbative: alpha_s(~1 GeV) ~ {alpha_s_1GeV_lattice}")
    print(f"  GU hypothesis gives ~{alpha_s_IR_GU:.2f} — factor ~{alpha_s_IR_GU/alpha_s_1GeV_lattice:.1f}x larger")
    print(f"  This is in the non-perturbative regime; perturbation theory unreliable.")

    # Standard perturbative running: alpha_s(mu) = alpha_s(M_Z) / (1 + b_0*alpha_s(M_Z)*ln(mu^2/M_Z^2)/(4*pi))
    M_Z_GeV = 91.1876
    alpha_s_MZ_f = float(alpha_s_MZ)

    def alpha_s_perturbative(mu_GeV):
        if mu_GeV <= 0:
            return np.nan
        log_ratio = np.log((mu_GeV / M_Z_GeV) ** 2)
        denom = 1.0 + b_0 * alpha_s_MZ_f * log_ratio / (4 * np.pi)
        if denom <= 0:
            return np.nan  # Landau pole below mu
        return alpha_s_MZ_f / denom

    alpha_s_1GeV_pert = alpha_s_perturbative(1.0)
    print(f"\nPerturbative running (1-loop): alpha_s(mu) = alpha_s(M_Z) / (1 + b_0*alpha_s(M_Z)*ln(mu^2/M_Z^2)/(4*pi))")
    print(f"  alpha_s(M_Z) = {alpha_s_MZ_f:.4f} (from gu_constants)")
    print(f"  alpha_s(1 GeV) = {alpha_s_1GeV_pert:.4f}")
    print("")

# ---------------------------------------------------------------------------
# Part 2: Gluon condensate from GU bag constant
# ---------------------------------------------------------------------------
def part2_gluon_condensate():
    print("=" * 70)
    print("Part 2: Gluon condensate from GU bag constant (Omega-torus)")
    print("=" * 70)

    # GU bag constant: c_B = (2*pi/phi)^2
    c_B = float((2 * pi / phi) ** 2)
    print(f"\nGU bag constant: c_B = (2*pi/phi)^2 = {c_B:.6f}")

    # Lambda_QCD: empirical value ~ 332 MeV (PDG, N_f=3, MS-bar)
    # GU ladder gives X(95) = M_P * phi^(-95) ~ 178 MeV (the QCD epoch scale)
    X_QCD_MeV = float(M_P * phi ** (-N_QCD))
    Lambda_QCD_MeV = 332.0  # PDG (N_f=3, MS-bar)
    Lambda_QCD_GeV = Lambda_QCD_MeV / 1000.0
    print(f"  X(N={N_QCD}) = M_P * phi^(-{N_QCD}) = {X_QCD_MeV:.3f} MeV")
    print(f"  Lambda_QCD (PDG, N_f=3) = {Lambda_QCD_MeV:.0f} MeV = {Lambda_QCD_GeV:.3f} GeV")
    print(f"  Ratio Lambda_QCD / X(95) = {Lambda_QCD_MeV/X_QCD_MeV:.2f}")

    # B_QCD = c_B * Lambda_QCD^4 (in same units as Lambda_QCD)
    # Lambda in GeV -> B in GeV^4
    B_QCD_GeV4 = c_B * (Lambda_QCD_GeV ** 4)
    print(f"  B_QCD = c_B * Lambda_QCD^4 = {B_QCD_GeV4:.6e} GeV^4")

    # SVZ gluon condensate: <(alpha_s/pi)*G^2> = (b_0/(32*pi^2)) * 4 * B_QCD
    # (4 from convention relating bag constant to trace anomaly)
    b_0 = 11 - 2 * 3 / 3  # N_f=3
    gluon_condensate_GU = (b_0 / (32 * np.pi**2)) * 4 * B_QCD_GeV4
    print(f"\nSVZ relation: <(alpha_s/pi)*G^2> = (b_0/(32*pi^2)) * 4 * B_QCD")
    print(f"  GU: <(alpha_s/pi)*G^2> = {gluon_condensate_GU:.6e} GeV^4")

    gluon_condensate_lattice = 0.012  # GeV^4
    print(f"  Lattice: <(alpha_s/pi)*G^2> ≈ {gluon_condensate_lattice} GeV^4")
    print(f"  Ratio GU/lattice: {gluon_condensate_GU / gluon_condensate_lattice:.3f}")
    print("")

# ---------------------------------------------------------------------------
# Part 3: Gluon propagator (Landau gauge, UV + IR)
# ---------------------------------------------------------------------------
def part3_gluon_propagator():
    print("=" * 70)
    print("Part 3: Gluon propagator (Landau gauge)")
    print("=" * 70)

    # Lambda_QCD and effective gluon mass
    Lambda_QCD_MeV = 332.0  # PDG (N_f=3, MS-bar)
    Lambda_QCD_GeV = Lambda_QCD_MeV / 1000.0
    m_g_GeV = Lambda_QCD_GeV / float(phi)  # ~110 MeV -> 0.11 GeV
    Lambda_G = Lambda_QCD_GeV  # Gribov scale ~ Lambda_QCD

    print("\nLandau gauge: D_mu_nu(q) = (delta_mu_nu - q_mu*q_nu/q^2) * D(q^2)")
    print("  UV (perturbative): D(q^2) = 1/q^2 * (1 + corrections)")
    print("  IR: confinement modifications (GZ or massive)")

    # 1-loop gluon self-energy coefficient (for reference)
    N_c, N_f = 3, 3
    # Pi(q^2) = -alpha_s*q^2/(4*pi) * [(11/3)*N_c - (4/3)*N_f/2] * ln(q^2/mu^2)
    coeff = (11/3)*N_c - (4/3)*(N_f/2)
    print(f"\n1-loop gluon self-energy: Pi(q^2) = -alpha_s*q^2/(4*pi) * [ (11/3)*N_c - (4/3)*N_f/2 ] * ln(q^2/mu^2)")
    print(f"  Coefficient (11/3)*{N_c} - (4/3)*{N_f/2} = {coeff}")
    print("  Renormalized: D_renorm(q^2) = 1/(q^2*(1 - Pi(q^2)/q^2))")

    # IR models
    print(f"\nGU IR: m_g ~ Lambda_QCD/phi ≈ {m_g_GeV*1000:.0f} MeV = {m_g_GeV:.4f} GeV")
    print("  Gribov-Zwanziger: D(q^2) = q^2 / (q^4 + Lambda_G^4)  -> 0 at q=0")
    print("  Massive gluon:     D(q^2) = 1 / (q^2 + m_g^2)")

    def D_UV(q2_GeV2):
        """Perturbative: 1/q^2 (tree)."""
        if q2_GeV2 <= 0:
            return np.nan
        return 1.0 / q2_GeV2

    def D_GZ(q2_GeV2):
        """Gribov-Zwanziger: q^2/(q^4 + Lambda_G^4)."""
        q4 = q2_GeV2**2
        return q2_GeV2 / (q4 + Lambda_G**4)

    def D_massive(q2_GeV2):
        """Massive: 1/(q^2 + m_g^2)."""
        return 1.0 / (q2_GeV2 + m_g_GeV**2)

    # Print D(q^2) over q = 0 to 5 GeV (values only, no matplotlib)
    print("\n  q (GeV)    q^2 (GeV^2)   D_UV(1/q^2)   D_GZ(q^2)   D_massive(q^2)")
    print("  " + "-" * 60)
    q_GeV_arr = np.linspace(0.05, 5.0, 21)  # avoid q=0 for UV
    for q in q_GeV_arr:
        q2 = q**2
        d_uv = D_UV(q2)
        d_gz = D_GZ(q2)
        d_m = D_massive(q2)
        print(f"  {q:6.2f}     {q2:8.4f}     {d_uv:12.4e}   {d_gz:10.4e}   {d_m:12.4e}")
    print("  (At q=0: D_GZ(0)=0, D_massive(0)=1/m_g^2)")
    print("")

# ---------------------------------------------------------------------------
# Part 4: Asymptotic freedom (one-loop beta, GU preserves standard QCD)
# ---------------------------------------------------------------------------
def part4_asymptotic_freedom():
    print("=" * 70)
    print("Part 4: Asymptotic freedom (GU inherits SU(3) gauge structure)")
    print("=" * 70)

    print("\nL_gauge = -(1/4) F^a_mu_nu F^a_mu_nu  (SU(3))")
    print("One-loop beta: beta_0 = (11*C_A - 4*T_F*N_f) / (3*(4*pi)^2)")
    print("  C_A = N_c = 3 (adjoint), T_F = 1/2 (fundamental)")
    print("  beta_0 = (33 - 2*N_f) / (48*pi^2)")
    print("  For N_f < 16.5: beta_0 > 0  =>  alpha_s DECREASES at high energy (AF).")

    N_c = 3
    T_F = 0.5
    C_A = N_c
    for N_f in [3, 4, 5, 6]:
        beta_0 = (11 * C_A - 4 * T_F * N_f) / (3 * (4 * np.pi)**2)
        b_0_GU = 11 - 2 * N_f / 3  # same as 4*pi*beta_0 in standard normalization
        print(f"  N_f = {N_f}:  beta_0 = {beta_0:.6e},  b_0 = 11 - 2*N_f/3 = {b_0_GU:.2f}  (positive => AF)")

    print("\n  GU preserves standard QCD gauge structure (from SU(5)); asymptotic freedom unchanged.")
    print("")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    part1_alpha_s_IR()
    part2_gluon_condensate()
    part3_gluon_propagator()
    part4_asymptotic_freedom()
    print("Done.")

if __name__ == "__main__":
    main()
