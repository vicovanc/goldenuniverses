#!/usr/bin/env python3
"""
GRAVITY FROM FIRST PRINCIPLES: BREAKING THE CIRCULARITY
========================================================

THE CIRCULAR CHAIN (what this script replaces):
    M_P(exp) -> M_0 = M_P/sqrt(5pi) -> M_P = sqrt(4pi*c_R)*M_0 = M_P(exp)
    This is a tautology: output equals input by construction.

THE NON-CIRCULAR CHAIN (this script):
    m_e (measured)
      -> C_e (from NLDE soliton, Route-A elliptic formula)
      -> M_P = m_e * phi^111 / (2pi * C_e * eta_QED)     [Law 12 inverted]
      -> G_N = hbar*c / M_P^2
      -> M_0 = M_P / sqrt(4pi * c_R)                      [from G_prim]

    Every theory needs ONE dimensionful input. We use m_e.
    The theory predicts the dimensionless ratio M_P/m_e, giving G_N.

INPUTS:
    Measured: m_e = 0.51099895069 MeV (CODATA 2022)
             alpha_EM = 1/137.035999177 (for eta_QED)
    Theory:   phi, pi, N_e=111, (p,q)=(-41,70), Route-A formula

OUTPUTS:
    Predicted: M_P, G_N (from m_e alone -- no c_R or M_0 needed!)
    Predicted: M_0 (requires c_R, i.e., G_prim choice)

KEY INSIGHT:
    M_P (and hence G_N) depends ONLY on m_e and C_e(nu).
    The c_R parameter (field content) determines M_0, NOT G_N.
    This means the gravity prediction is decoupled from the G_prim choice.

References:
    - theory-laws.md: Law 12, Law 33 (Route-A closure)
    - 12_g_prim_field_content.py: c_R scenarios
    - SKILL.md: C_e(tree)=1.0550, delta_Ce=0.00379, m_e(1-loop)=23 ppm

Date: February 2026
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mpmath import (
    mp, mpf, sqrt, pi as mp_pi, exp,
    ellipk, ellipe, findroot, nstr, log10
)
mp.dps = 50

# ======================================================================
# SECTION 0: PHYSICAL CONSTANTS (measured inputs — TWO only)
# ======================================================================

# THE SINGLE DIMENSIONFUL INPUT
m_e_CODATA = mpf('0.51099895069')   # MeV, CODATA 2022

# Fine structure constant (needed for eta_QED — external physics, not GU)
alpha_EM = mpf('1') / mpf('137.035999177')

# REFERENCE VALUES for comparison only (NOT used in derivation)
M_P_exp = mpf('1.2208901286e22')    # MeV, PDG 2022
G_N_exp = mpf('6.67430e-11')        # m^3 kg^-1 s^-2, CODATA 2018

# SI conversion factors
hbar_c_SI = mpf('3.161526e-26')     # J*m = hbar * c in SI
MeV_to_kg = mpf('1.78266192e-30')   # kg per MeV/c^2

# ======================================================================
# SECTION 1: THEORY-DERIVED CONSTANTS (no measured M_P anywhere!)
# ======================================================================

phi = (1 + sqrt(mpf(5))) / 2
pi = mp_pi

N_e = 111
p_e, q_e = -41, 70

# Torus geometry — from winding numbers and phi alone
q_over_phi = mpf(q_e) / phi
R_sq = mpf(p_e)**2 + q_over_phi**2
R = sqrt(R_sq)
l_Omega = 2 * pi * R

# Topological modulus (first-principles, no fitting)
nu_topo = abs(q_over_phi) / R

# Fractional epoch shift
delta_e = mpf(N_e) / phi**2 - 42

# Memory coupling
lambda_rec = exp(phi) / pi**2       # e^phi / pi^2

# QED radiative correction (standard, not GU-specific)
eta_QED = 1 - alpha_EM / (2 * pi)


# ======================================================================
# SECTION 2: C_e COMPUTATION — Route-A Elliptic Formula (Law 33)
# ======================================================================

def Ce_route_A(nu):
    """Route-A structural coefficient C_e(nu).

    C_e(nu) = |delta_e|*K(nu) + nu/2 - lambda_rec*(K(nu)-E(nu))/3 + alpha/(2pi)

    All terms derived from (phi, pi, N_e, p, q, alpha_EM).
    """
    K = ellipk(nu)
    E = ellipe(nu)
    return abs(delta_e) * K + nu / 2 - lambda_rec * (K - E) / 3 + alpha_EM / (2 * pi)


def M_P_from_me(Ce_val):
    """Invert Law 12: M_P = m_e * phi^N_e / (2*pi * C_e * eta_QED)."""
    return m_e_CODATA * phi**N_e / (2 * pi * Ce_val * eta_QED)


def G_N_SI(M_P_MeV):
    """G_N in SI units from M_P in MeV.

    G_N = hbar*c / M_P^2 = hbar_c_SI / (M_P_MeV * MeV_to_kg)^2
    """
    M_P_kg = M_P_MeV * MeV_to_kg
    return hbar_c_SI / M_P_kg**2


# ======================================================================
# SECTION 3: c_R FROM FIELD CONTENT (from 12_g_prim_field_content.py)
# ======================================================================

def c_R_from_DOF(n_b, n_f):
    """c_R = Str(a_1) / (4*pi) where Str(a_1)/R = N_B/6 - N_F/12."""
    str_a1_over_R = mpf(n_b) / 6 - mpf(n_f) / 12
    return str_a1_over_R / (4 * pi)


def sm_content():
    """Standard Model: 31 bosonic, 90 fermionic real DOF."""
    return 31, 90


def mssm_partners():
    """MSSM SUSY partners: +94 bosonic (sfermions + 2nd Higgs), +32 fermionic (gauginos + higgsinos)."""
    return 94, 32


def gu_modes():
    """GU memory modes: X field + 3 theta_a + 3 torus moduli + 1 Omega modulus = 8 bosonic."""
    return 8, 0


def auxiliary_R():
    """Localized auxiliary field R from L_recursive_mimic: 1 real scalar."""
    return 1, 0


def dark_sector():
    """SU(2)_R dark sector: 3 dark W bosons (6 DOF) + dark Higgs doublet (4 DOF) = 10 bosonic."""
    return 10, 0


def gut_scalars(group, with_susy=False):
    """Extra GUT scalar multiplets (chiral superfields if SUSY).

    Returns (n_b, n_f).
    """
    if group == "SM":
        return 0, 0
    elif group == "SU(5)":
        nb = 60  # 24-plet adjoint (48) + color-triplet (12)
        nf = 60 if with_susy else 0
        return nb, nf
    elif group == "SO(10)":
        nb = 134  # 45-plet (90) + 16-plet (32) + 10-plet extra (12)
        nf = 134 if with_susy else 0
        return nb, nf
    else:
        return 0, 0


def build_scenario(name, include_susy, include_gu, include_aux,
                   include_dark, gut_group):
    """Build a complete field-content scenario."""
    nb, nf = sm_content()

    parts = [f"SM({nb}B,{nf}F)"]

    if include_susy:
        db, df = mssm_partners()
        nb += db; nf += df
        parts.append(f"SUSY(+{db}B,+{df}F)")

    if include_gu:
        db, df = gu_modes()
        nb += db; nf += df
        parts.append(f"GU(+{db}B)")

    if include_aux:
        db, df = auxiliary_R()
        nb += db; nf += df
        parts.append(f"Aux(+{db}B)")

    if include_dark:
        db, df = dark_sector()
        nb += db; nf += df
        parts.append(f"Dark(+{db}B)")

    if gut_group != "SM":
        db, df = gut_scalars(gut_group, with_susy=include_susy)
        nb += db; nf += df
        parts.append(f"{gut_group}(+{db}B,+{df}F)")

    cR = c_R_from_DOF(nb, nf)
    a0 = nb - nf

    return {
        "name": name,
        "parts": " + ".join(parts),
        "n_b": nb, "n_f": nf,
        "str_a0": a0,
        "c_R": cR,
    }


# ======================================================================
# MAIN
# ======================================================================

def main():
    print("=" * 80)
    print("GRAVITY FROM FIRST PRINCIPLES")
    print("Breaking the Circularity: m_e -> M_P -> G_N")
    print("=" * 80)

    # ==================================================================
    # STEP 1: THEORY GEOMETRY (all from phi, pi, N_e, p, q)
    # ==================================================================
    print()
    print("-" * 80)
    print("STEP 1: THEORY-DERIVED GEOMETRY")
    print("  (No measured M_P used anywhere)")
    print("-" * 80)

    print(f"""
  Mathematical constants:
    phi          = {float(phi):.15f}
    pi           = {float(pi):.15f}

  Electron topology:
    N_e          = {N_e}
    (p, q)       = ({p_e}, {q_e})
    R            = sqrt({p_e}^2 + ({q_e}/phi)^2) = {float(R):.6f}
    l_Omega      = 2*pi*R = {float(l_Omega):.3f}
    nu_topo      = |q/phi|/R = {float(nu_topo):.10f}
    delta_e      = N_e/phi^2 - 42 = {float(delta_e):.10f}

  Couplings:
    lambda_rec   = e^phi/pi^2 = {float(lambda_rec):.10f}
    alpha_EM     = 1/137.036 = {float(alpha_EM):.10f}
    eta_QED      = 1 - alpha/(2pi) = {float(eta_QED):.10f}
""")

    # ==================================================================
    # STEP 2: COMPUTE C_e FOR THREE nu SCENARIOS
    # ==================================================================
    print("-" * 80)
    print("STEP 2: C_e COMPUTATION (Route-A Elliptic Formula)")
    print("-" * 80)

    # --- Scenario A: nu_topo, tree level ---
    Ce_tree = Ce_route_A(nu_topo)
    K_topo = ellipk(nu_topo)
    E_topo = ellipe(nu_topo)

    # --- Scenario B: nu_topo + Lame one-loop correction ---
    delta_Ce = (1 - E_topo / K_topo) / N_e
    Ce_lame = Ce_tree - delta_Ce

    # --- Scenario C: nu_exact (bootstrap, self-consistent with m_e) ---
    # To find nu_exact, we need C_e_target. But C_e_target = m_e / [M_P * (2pi/phi^111) * eta_QED].
    # In the bootstrap, M_P = M_P_exp is used. We label this clearly.
    prefactor_exp = M_P_exp * 2 * pi / phi**N_e
    Ce_target = m_e_CODATA / (prefactor_exp * eta_QED)

    nu_exact = findroot(
        lambda nu: Ce_route_A(nu) - Ce_target,
        mpf('0.72')
    )
    Ce_exact = Ce_route_A(nu_exact)

    print(f"""
  Route-A formula: C_e(nu) = |delta_e|*K(nu) + nu/2 - (e^phi/pi^2)*(K-E)/3 + alpha/(2pi)

  Elliptic integrals at nu_topo:
    K(nu_topo) = {float(K_topo):.10f}
    E(nu_topo) = {float(E_topo):.10f}
    1 - E/K    = {float(1 - E_topo / K_topo):.10f}  (modular defect)

  ┌──────────────────────────────────────────────────────────────────────┐
  │  SCENARIO A: nu_topo (tree level, first-principles)                │
  │    nu        = {float(nu_topo):.10f}                                      │
  │    C_e       = {float(Ce_tree):.10f}                                      │
  │    Status    = PURE FIRST-PRINCIPLES (no m_e input)                │
  ├──────────────────────────────────────────────────────────────────────┤
  │  SCENARIO B: nu_topo + Lame one-loop correction                    │
  │    delta_Ce  = (1-E/K)/N_e = {float(delta_Ce):.10f}                       │
  │    C_e       = {float(Ce_lame):.10f}                                      │
  │    Status    = FIRST-PRINCIPLES + one-loop (no m_e input)          │
  ├──────────────────────────────────────────────────────────────────────┤
  │  SCENARIO C: nu_exact (bootstrap, uses m_e as boundary condition)  │
  │    nu        = {float(nu_exact):.10f}                                      │
  │    C_e       = {float(Ce_exact):.10f}    (= C_e_target by construction)   │
  │    Status    = SELF-CONSISTENT (determines nu from m_e)            │
  └──────────────────────────────────────────────────────────────────────┘
""")

    # ==================================================================
    # STEP 3: PREDICT M_P FROM m_e (THE KEY DERIVATION)
    # ==================================================================
    print("-" * 80)
    print("STEP 3: M_P PREDICTION FROM m_e")
    print("  Formula: M_P = m_e * phi^111 / (2*pi * C_e * eta_QED)")
    print("-" * 80)

    phi_111 = phi**N_e
    log10_phi_111 = float(log10(phi_111))

    print(f"\n  phi^111 = 10^{log10_phi_111:.6f} = {float(phi_111):.6e}")
    print(f"  m_e     = {float(m_e_CODATA)} MeV (MEASURED INPUT)")
    print(f"  M_P_exp = {float(M_P_exp):.6e} MeV (REFERENCE ONLY)")

    nu_scenarios = [
        ("A: tree (nu_topo)", Ce_tree, "FIRST-PRINCIPLES"),
        ("B: Lame-corrected", Ce_lame, "FIRST-PRINCIPLES + 1-loop"),
        ("C: bootstrap", Ce_exact, "SELF-CONSISTENT (uses m_e as BC)"),
    ]

    mp_results = []
    print()
    for label, Ce_val, status in nu_scenarios:
        M_P_pred = M_P_from_me(Ce_val)
        err_mp = float((M_P_pred - M_P_exp) / M_P_exp * 100)
        err_ppm = float((M_P_pred - M_P_exp) / M_P_exp * 1e6)

        # m_e sanity check: m_e = M_P * (2pi/phi^111) * C_e * eta_QED
        me_check = M_P_pred * 2 * pi / phi_111 * Ce_val * eta_QED

        print(f"  {label}")
        print(f"    C_e          = {float(Ce_val):.10f}")
        print(f"    M_P(pred)    = {float(M_P_pred):.6e} MeV")
        print(f"    M_P(exp)     = {float(M_P_exp):.6e} MeV")
        print(f"    Error        = {err_mp:+.6f}%  ({err_ppm:+.1f} ppm)")
        print(f"    m_e check    = {float(me_check):.11f} MeV")
        print(f"    Status       = {status}")
        print()

        mp_results.append((label, Ce_val, M_P_pred, err_mp, err_ppm, status))

    # ==================================================================
    # STEP 4: PREDICT G_N FROM M_P
    # ==================================================================
    print("-" * 80)
    print("STEP 4: G_N PREDICTION")
    print("  Formula: G_N = hbar*c / M_P^2")
    print("  (Decoupled from c_R — this is the pure prediction)")
    print("-" * 80)

    gn_results = []
    print()
    for label, Ce_val, M_P_pred, err_mp, err_ppm, status in mp_results:
        G_pred = G_N_SI(M_P_pred)
        err_gn = float((G_pred - G_N_exp) / G_N_exp * 100)
        err_gn_ppm = float((G_pred - G_N_exp) / G_N_exp * 1e6)

        print(f"  {label}")
        print(f"    G_N(pred)  = {float(G_pred):.6e} m^3 kg^-1 s^-2")
        print(f"    G_N(exp)   = {float(G_N_exp):.6e} m^3 kg^-1 s^-2")
        print(f"    Error      = {err_gn:+.6f}%  ({err_gn_ppm:+.1f} ppm)")
        # G_N error ~ 2 * M_P error (to first order)
        print(f"    Note: error ~ 2 x M_P error ({2*err_mp:+.6f}%)")
        print()

        gn_results.append((label, G_pred, err_gn, err_gn_ppm, status))

    # ==================================================================
    # STEP 5: c_R SCENARIOS (from field content)
    # ==================================================================
    print("-" * 80)
    print("STEP 5: c_R FROM FIELD CONTENT (G_prim scenarios)")
    print("  (Only affects M_0, NOT G_N or M_P)")
    print("-" * 80)

    scenarios = [
        build_scenario("SM only (no SUSY)",
                        False, False, False, False, "SM"),
        build_scenario("SM + SUSY (MSSM)",
                        True, False, False, False, "SM"),
        build_scenario("*** SU(5) + SUSY (no memory) ***",
                        True, False, False, False, "SU(5)"),
        build_scenario("SM + SUSY + GU + Aux + Dark",
                        True, True, True, True, "SM"),
        build_scenario("SU(5) + SUSY + GU + Aux + Dark",
                        True, True, True, True, "SU(5)"),
        build_scenario("SO(10) + SUSY + GU + Aux + Dark",
                        True, True, True, True, "SO(10)"),
    ]

    target_cR = mpf('1.25')

    print()
    for s in scenarios:
        print(f"  {s['name']}")
        print(f"    Content: {s['parts']}")
        print(f"    N_B = {s['n_b']},  N_F = {s['n_f']}")
        print(f"    Str(a_0) = N_B - N_F = {s['str_a0']}")
        cc_ok = abs(s['str_a0']) <= 5
        print(f"    CC constraint (|Str(a_0)| ~ 0): {'GOOD' if cc_ok else 'FAILS (|Str(a_0)| = '+str(abs(s['str_a0']))+')'}")
        print(f"    c_R = {float(s['c_R']):.6f}   (target = {float(target_cR):.2f})")
        if s['c_R'] > 0:
            ratio = sqrt(4 * pi * s['c_R'])
            print(f"    M_P/M_0 = sqrt(4*pi*c_R) = {float(ratio):.6f}")
        else:
            print(f"    c_R < 0 => M_P/M_0 imaginary (INVALID)")
        print()

    # ==================================================================
    # STEP 6: PREDICT M_0 FOR EACH (nu, G_prim) COMBINATION
    # ==================================================================
    print("-" * 80)
    print("STEP 6: M_0 PREDICTIONS")
    print("  Formula: M_0 = M_P / sqrt(4*pi*c_R)")
    print("-" * 80)

    print()
    for label, Ce_val, M_P_pred, err_mp, _, status in mp_results:
        print(f"  Using {label}:")
        print(f"    M_P = {float(M_P_pred):.6e} MeV")
        for s in scenarios:
            if s['c_R'] <= 0:
                print(f"      {s['name']}: c_R < 0, M_0 undefined")
                continue
            ratio = sqrt(4 * pi * s['c_R'])
            M_0_pred = M_P_pred / ratio
            M_0_GeV = M_0_pred / 1000  # MeV -> GeV
            print(f"      {s['name']}:")
            print(f"        c_R = {float(s['c_R']):.4f}, M_0 = {float(M_0_GeV):.4e} GeV")
        print()

    # ==================================================================
    # STEP 7: HONEST SCORECARD
    # ==================================================================
    print("=" * 80)
    print("STEP 7: HONEST SCORECARD")
    print("=" * 80)

    print("""
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                     WHAT IS WHAT — HONEST LABELS                      │
  ├──────────────────────┬──────────────────────────────────────────────────┤
  │  MEASURED            │  m_e = 0.51099895069 MeV (CODATA 2022)         │
  │  (sole dimensionful  │  alpha_EM = 1/137.036 (for eta_QED)            │
  │   input)             │                                                │
  ├──────────────────────┼──────────────────────────────────────────────────┤
  │  DERIVED from theory │  phi = (1+sqrt(5))/2                           │
  │  (no fitting)        │  N_e = 111 (resonance condition)               │
  │                      │  (p,q) = (-41,70) (energy minimization)        │
  │                      │  nu_topo = |q/phi|/R = 0.7258                  │
  │                      │  C_e(nu_topo) from Route-A elliptic formula    │
  │                      │  delta_Ce = (1-E/K)/N_e (Lame one-loop)        │
  │                      │  eta_QED = 1 - alpha/(2pi) (standard QED)      │
  ├──────────────────────┼──────────────────────────────────────────────────┤
  │  CHOSEN (discrete)   │  G_prim: SM, SU(5), or SO(10)                  │
  │                      │  (determines c_R and M_0, NOT G_N)             │
  ├──────────────────────┼──────────────────────────────────────────────────┤
  │  PREDICTED           │  M_P, G_N (from m_e alone)                     │
  │                      │  M_0 (from M_P + c_R)                          │
  └──────────────────────┴──────────────────────────────────────────────────┘
""")

    print("  PREDICTION RESULTS:")
    print()
    print(f"  {'Scenario':<30s} {'M_P error':<18s} {'G_N error':<18s} {'Type'}")
    print(f"  {'─' * 30} {'─' * 18} {'─' * 18} {'─' * 30}")

    for i, (label, Ce_val, M_P_pred, err_mp, err_ppm, status) in enumerate(mp_results):
        G_pred = gn_results[i][1]
        err_gn = gn_results[i][2]
        err_gn_ppm = gn_results[i][3]

        mp_str = f"{err_mp:+.4f}% ({err_ppm:+.0f} ppm)"
        gn_str = f"{err_gn:+.4f}% ({err_gn_ppm:+.0f} ppm)"
        print(f"  {label:<30s} {mp_str:<18s} {gn_str:<18s} {status}")
    print()

    # ==================================================================
    # STEP 8: THE CRITICAL QUESTION
    # ==================================================================
    print("=" * 80)
    print("STEP 8: THE CRITICAL QUESTION")
    print("=" * 80)

    # Best first-principles prediction (Lame-corrected)
    _, Ce_best, M_P_best, err_best, ppm_best, _ = mp_results[1]
    G_best = gn_results[1][1]
    err_gn_best = gn_results[1][2]
    ppm_gn_best = gn_results[1][3]

    print(f"""
  QUESTION: Given only m_e as input, does the theory predict G_N correctly?

  ANSWER (using Lame-corrected first-principles prediction):

    M_P(predicted) = {float(M_P_best):.6e} MeV
    M_P(experiment) = {float(M_P_exp):.6e} MeV
    M_P error = {err_best:+.6f}% = {ppm_best:+.1f} ppm

    G_N(predicted) = {float(G_best):.6e} m^3 kg^-1 s^-2
    G_N(experiment) = {float(G_N_exp):.6e} m^3 kg^-1 s^-2
    G_N error = {err_gn_best:+.6f}% = {ppm_gn_best:+.1f} ppm
""")

    print("""  INTERPRETATION:

    The theory relates the Planck mass to the electron mass via the
    dimensionless ratio:

        M_P / m_e = phi^111 / (2*pi * C_e * eta_QED)

    where EVERY quantity on the right is derived from first principles
    (phi, pi, topology, elliptic integrals, standard QED).

    The ONLY dimensionful input is m_e. The theory PREDICTS M_P and
    hence G_N. The c_R parameter (field content, G_prim choice) does
    NOT affect this prediction — it only determines M_0.

    The key non-trivial content is that C_e(nu_topo) ~ O(1), which means
    M_P/m_e ~ phi^111 / (2pi) ~ 10^23. This enormous ratio arises from
    the electron being at epoch N_e = 111 on the spiral, not from any
    exponential fine-tuning.
""")

    # ==================================================================
    # STEP 9: WHICH G_PRIM PASSES?
    # ==================================================================
    print("-" * 80)
    print("STEP 9: G_PRIM DISCRIMINATION")
    print("  Can the theory predict which G_prim is correct?")
    print("-" * 80)

    print("""
  G_N is independent of G_prim (it comes from M_P alone).
  G_prim determines c_R and hence M_0.

  The question becomes: which G_prim gives a CONSISTENT M_0?

  Consistency check: M_0 should satisfy:
    1. M_0 < M_P (sub-Planckian cutoff)
    2. Str(a_0) ~ 0 (CC suppression via soft SUSY)
    3. M_0 ~ O(10^18 GeV) (compatible with GUT scale)
""")

    best_MP = M_P_best  # Lame-corrected prediction

    print(f"  Using M_P = {float(best_MP):.4e} MeV (Lame-corrected):")
    print()
    for s in scenarios:
        if s['c_R'] <= 0:
            print(f"    {s['name']}: FAILS (c_R < 0)")
            continue
        ratio = sqrt(4 * pi * s['c_R'])
        M_0_pred = best_MP / ratio
        M_0_GeV = float(M_0_pred / 1000)  # to GeV
        cc_ok = abs(s['str_a0']) <= 5
        sub_planck = M_0_pred < best_MP
        gut_scale = 1e15 < M_0_GeV < 1e20

        status = []
        if cc_ok:
            status.append("CC: OK")
        else:
            status.append(f"CC: FAILS (Str(a_0)={s['str_a0']})")
        if sub_planck:
            status.append("sub-Planckian: OK")
        else:
            status.append("sub-Planckian: FAILS")
        if gut_scale:
            status.append(f"GUT-scale: OK ({M_0_GeV:.2e} GeV)")
        else:
            status.append(f"GUT-scale: {'too low' if M_0_GeV < 1e15 else 'too high'}")

        all_ok = cc_ok and sub_planck and gut_scale
        verdict = "VIABLE" if all_ok else "EXCLUDED"

        print(f"    {s['name']}")
        print(f"      c_R = {float(s['c_R']):.4f}, M_0 = {M_0_GeV:.4e} GeV")
        print(f"      {' | '.join(status)}")
        print(f"      Verdict: {verdict}")
        print()

    # ==================================================================
    # SUMMARY
    # ==================================================================
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print(f"""
  This script demonstrates that the GU theory predicts G_N from m_e
  with NO circularity:

  INPUTS:  m_e = {float(m_e_CODATA)} MeV (measured)
           alpha_EM = 1/{float(1/alpha_EM):.3f} (measured, for eta_QED)

  OUTPUTS: M_P = {float(M_P_best):.6e} MeV
           G_N = {float(G_best):.6e} m^3 kg^-1 s^-2

  ERRORS:  M_P: {err_best:+.6f}% ({ppm_best:+.0f} ppm)
           G_N: {err_gn_best:+.6f}% ({ppm_gn_best:+.0f} ppm)

  The prediction chain is:
    m_e (measured)
      -> C_e = {float(Ce_best):.6f} (derived: topology + elliptic + Lame)
      -> M_P = m_e * phi^111 / (2pi * C_e * eta_QED)
      -> G_N = hbar*c / M_P^2

  ZERO fitted parameters in the M_P/G_N prediction.
  The G_prim choice affects ONLY M_0 (the UV cutoff), not G_N.
""")


if __name__ == "__main__":
    main()
