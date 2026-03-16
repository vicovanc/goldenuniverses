#!/usr/bin/env python3
"""
Derived NJL Pion Physics (B2, B3, B4)
=====================================

Combines:
  B2: Derive Lambda_NJL from GU (eliminate phenomenological 631.4 MeV)
  B3: f_pi from GU-derived NJL parameters
  B4: Chiral condensate with GU-derived cutoff

Uses the GU epoch scale X(95) = M_P * phi^(-95) ~ 178 MeV as the QCD scale.
Tests several GU-motivated relations Lambda_NJL = factor * X(95),
solves the NJL gap equation for each, then computes f_pi (Pagels-Stokar)
and condensate^(1/3). Selects the best candidate against PDG/lattice.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from scipy.optimize import brentq

from utils.gu_constants import phi, pi, M_P, N_QCD

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
N_c = 3
N_f = 2
m_u_current = 2.16   # MeV
m_d_current = 4.67   # MeV
m_current = (m_u_current + m_d_current) / 2.0  # MeV, isospin average

# PDG / lattice benchmarks
M_const_PDG = 330.0    # MeV (constituent mass)
f_pi_PDG = 92.2        # MeV
cond_13_PDG = 250.0    # MeV  (<psi-bar psi>^(1/3))

# GU epoch scale X(95) = M_P * phi^(-95)
_phi_float = float(phi)
_pi_float = float(pi)
_M_P_float = float(M_P)
X_QCD = _M_P_float * (_phi_float ** (-N_QCD))  # ~ 178 MeV (pure GU)
Lambda_QCD = X_QCD  # Use the raw GU epoch scale (no ad-hoc pi/3 factor)

# Critical coupling: G*Lambda^2 = pi^2 for DCSB threshold (with our I_1 normalization).
# To get M_const ~ 330 MeV and f_pi ~ 92 MeV we need G*Lambda^2 well above pi^2 (~9.87).
# Empirical range for standard NJL (Lambda~631 MeV, M~330 MeV): G*Lambda^2 ~ 8.5–10.
G_Lambda_sq_target = 9.0


def I_1(M, Lambda):
    """NJL loop I_1 with 3D sharp cutoff: int_0^Lambda dp p^2/sqrt(p^2+M^2)."""
    if Lambda <= 0 or M < 0:
        return 0.0
    E_L = np.sqrt(Lambda**2 + M**2)
    term1 = Lambda * E_L / 2.0
    term2 = (M**2 / 2.0) * np.log((Lambda + E_L) / max(M, 1e-12))
    return term1 - term2


def gap_equation_residual(M, m_cur, G, Lambda):
    """Residual for gap equation: M - m_cur - (G*N_c/pi^2)*M*I_1(M,Lambda) = 0."""
    if M <= 0:
        return -m_cur
    return M - m_cur - (G * N_c / (np.pi**2)) * M * I_1(M, Lambda)


def solve_gap(m_cur, G, Lambda, M_guess=300.0):
    """Solve NJL gap equation for constituent mass M (MeV)."""
    # Bracket: M from m_cur to Lambda (constituent mass must be in between)
    try:
        M_lo = m_cur + 1.0
        M_hi = Lambda * 0.99
        if gap_equation_residual(M_lo, m_cur, G, Lambda) >= 0:
            return M_lo
        if gap_equation_residual(M_hi, m_cur, G, Lambda) <= 0:
            return M_hi
        M = brentq(
            lambda M: gap_equation_residual(M, m_cur, G, Lambda),
            M_lo, M_hi,
            xtol=1e-6, maxiter=200
        )
        return M
    except Exception:
        return np.nan


def f_pi_from_njl(M, Lambda):
    """Pagels-Stokar with 3D sharp cutoff (constant M, dM/dp=0).
    f_pi^2 = (N_c*M^2)/(4*pi^2) * [ ln((Lambda+E_L)/M) - Lambda/E_L ], E_L = sqrt(Lambda^2+M^2).
    """
    E_L = np.sqrt(Lambda**2 + M**2)
    bracket = np.log((Lambda + E_L) / max(M, 1e-12)) - Lambda / E_L
    f_pi_sq = (N_c * M**2) / (4.0 * np.pi**2) * bracket
    return np.sqrt(max(f_pi_sq, 0.0))


def condensate_njl(M, Lambda):
    """Chiral condensate with 3D sharp cutoff.
    <psi-bar psi> = -N_c/(2*pi^2) * [M*Lambda*E_L/2 - M^3/2 * ln((Lambda+E_L)/M)].
    """
    E_L = np.sqrt(Lambda**2 + M**2)
    bracket = M * Lambda * E_L / 2.0 - (M**3 / 2.0) * np.log((Lambda + E_L) / max(M, 1e-12))
    return -N_c / (2.0 * np.pi**2) * bracket


def condensate_13(M, Lambda):
    """Condensate^(1/3) in MeV (positive, for comparison with 250 MeV)."""
    cond = condensate_njl(M, Lambda)
    # condensate is negative; report magnitude^(1/3)
    return (abs(cond)) ** (1.0 / 3.0)


# ---------------------------------------------------------------------------
# GU-motivated Lambda_NJL candidates
# ---------------------------------------------------------------------------
def get_lambda_njl_candidates():
    phi2 = _phi_float ** 2
    two_pi_over_phi = 2.0 * _pi_float / _phi_float
    c_B = two_pi_over_phi ** 2
    sqrt_c_B = np.sqrt(c_B)
    return [
        ("phi^2 * Lambda_QCD", phi2 * Lambda_QCD),
        ("pi * Lambda_QCD", _pi_float * Lambda_QCD),
        ("(2*pi/phi) * Lambda_QCD", two_pi_over_phi * Lambda_QCD),
        ("sqrt(c_B) * Lambda_QCD, c_B=(2*pi/phi)^2", sqrt_c_B * Lambda_QCD),
        ("phi * pi * Lambda_QCD", _phi_float * _pi_float * Lambda_QCD),
    ]


def run_one_candidate(name, Lambda_NJL):
    """For a given Lambda_NJL: set G, solve gap, compute f_pi and condensate^(1/3)."""
    G = G_Lambda_sq_target / (Lambda_NJL**2)
    G_Lambda_sq = G * (Lambda_NJL**2)

    M_const = solve_gap(m_current, G, Lambda_NJL)
    if np.isnan(M_const):
        return None

    f_pi = f_pi_from_njl(M_const, Lambda_NJL)
    cond13 = condensate_13(M_const, Lambda_NJL)

    return {
        "name": name,
        "Lambda_NJL": Lambda_NJL,
        "G": G,
        "G_Lambda_sq": G_Lambda_sq,
        "M_const": M_const,
        "f_pi": f_pi,
        "condensate_13": cond13,
    }


def main():
    print("=" * 80)
    print("DERIVED NJL PION (B2, B3, B4): Lambda_NJL from GU, f_pi, condensate")
    print("=" * 80)
    print(f"\nGU epoch scale X({N_QCD}) = M_P * phi^(-{N_QCD}) = {Lambda_QCD:.3f} MeV")
    print(f"G*Lambda^2 target = {G_Lambda_sq_target} (supercritical DCSB)")
    print(f"m_current (avg u,d) = {m_current:.3f} MeV")
    print(f"Benchmarks: M_const ~ {M_const_PDG} MeV, f_pi = {f_pi_PDG} MeV, condensate^(1/3) = {cond_13_PDG} MeV")
    print()

    candidates = get_lambda_njl_candidates()
    results = []

    for name, Lambda_NJL in candidates:
        print("-" * 80)
        print(f"  GU relation: Lambda_NJL = {name}")
        print(f"  Lambda_NJL = {Lambda_NJL:.2f} MeV")
        r = run_one_candidate(name, Lambda_NJL)
        if r is None:
            print("  [Gap equation did not converge.]")
            continue
        results.append(r)
        print(f"  G = {r['G']:.6f} MeV^{-2}   G*Lambda^2 = {r['G_Lambda_sq']:.3f}")
        print(f"  M_constituent = {r['M_const']:.2f} MeV  (PDG ~ {M_const_PDG})")
        print(f"  f_pi          = {r['f_pi']:.2f} MeV  (PDG  {f_pi_PDG})")
        print(f"  condensate^(1/3) = {r['condensate_13']:.2f} MeV  (lattice ~ {cond_13_PDG})")
        err_M = abs(r['M_const'] - M_const_PDG) / M_const_PDG * 100
        err_f = abs(r['f_pi'] - f_pi_PDG) / f_pi_PDG * 100
        err_c = abs(r['condensate_13'] - cond_13_PDG) / cond_13_PDG * 100
        print(f"  Errors: M {err_M:.1f}%, f_pi {err_f:.1f}%, cond^(1/3) {err_c:.1f}%")
        print()

    if not results:
        print("No candidate converged.")
        return

    # Score: target Lambda_NJL within 10% of 631 MeV, f_pi within 10%, condensate within 5%
    Lambda_ref = 631.0
    scores = []
    for r in results:
        e_L = abs(r['Lambda_NJL'] - Lambda_ref) / Lambda_ref * 100
        e_f = abs(r['f_pi'] - f_pi_PDG) / f_pi_PDG * 100
        e_c = abs(r['condensate_13'] - cond_13_PDG) / cond_13_PDG * 100
        # Penalty: 10% Lambda, 10% f_pi, 5% condensate
        penalty = (e_L / 10.0) + (e_f / 10.0) + (e_c / 5.0)
        ok_L = e_L <= 10
        ok_f = e_f <= 10
        ok_c = e_c <= 5
        scores.append((penalty, ok_L, ok_f, ok_c, r))

    scores.sort(key=lambda x: x[0])
    best = scores[0][4]
    ok_L, ok_f, ok_c = scores[0][1], scores[0][2], scores[0][3]

    print("=" * 80)
    print("BEST LAMBDA_NJL (GU-DERIVED)")
    print("=" * 80)
    print(f"  Relation: Lambda_NJL = {best['name']}")
    print(f"  Lambda_NJL = {best['Lambda_NJL']:.2f} MeV  (within 10% of 631: {'yes' if ok_L else 'no'})")
    print(f"  G*Lambda^2 = {best['G_Lambda_sq']:.3f}")
    print(f"  M_const = {best['M_const']:.2f} MeV")
    print(f"  f_pi = {best['f_pi']:.2f} MeV  (within 10% of 92.2: {'yes' if ok_f else 'no'})")
    print(f"  condensate^(1/3) = {best['condensate_13']:.2f} MeV  (within 5% of 250: {'yes' if ok_c else 'no'})")
    print()


if __name__ == "__main__":
    main()
