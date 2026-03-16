#!/usr/bin/env python3
"""
QUARK WINDING NUMBERS AND C-FACTORS — BOTTOM-UP PROTON DERIVATION (Phase 1)
=============================================================================

For each quark flavor, this script:
  1. Runs the 4-layer winding number solver (from 30_WINDING_NUMBERS)
  2. Extracts (p, q), nu_topo, L_Omega, S_topo, K(nu), E(nu)
  3. Computes C_q from the Route A elliptic formula
  4. Compares C_q * M_P * phi^(-N_q) with PDG quark masses
  5. Honestly assesses what works and what doesn't

CONFINEMENT CAVEAT:
  The electron's C_e comes from a FREE soliton on the Omega-torus at N=111.
  Quarks are CONFINED — they don't exist as free particles. The NLDE/winding
  approach may not directly apply. The "quark mass" in the PDG is a running
  parameter extracted from perturbative QCD processes, not a pole mass.
  The C_q factors derived here assume the same free-soliton formula, which
  is a hypothesis that MUST be tested against lattice QCD and experiment.

CANONICAL EPOCHS (from gu_constants.py):
  N_u=110, N_d=105, N_s=102, N_c=97, N_b=89, N_t=81

Date: February 2026
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from math import gcd
from mpmath import mp, mpf, sqrt, pi as mp_pi, exp, ellipk, ellipe, ln, power
mp.dps = 50

phi = (mpf('1') + sqrt(mpf('5'))) / 2
phi_sq = phi ** 2
pi = mp_pi
M_P = mpf('1.22089e22')  # MeV
alpha_EM = mpf('1') / mpf('137.035999084')
lambda_rec_beta = exp(phi) / pi**2

from utils.gu_constants import (
    N_u, N_d, N_s, N_c, N_b, N_t,
    N_e, N_mu, N_tau, N_QCD, CODATA,
)

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '30_WINDING_NUMBERS'))
from importlib import import_module
winding_mod = import_module('01_winding_number_solver')
find_winding_numbers = winding_mod.find_winding_numbers
find_winding_universal = winding_mod.find_winding_universal
WindingResult = winding_mod.WindingResult
print_result = winding_mod.print_result
resonance_filter = winding_mod.resonance_filter

# PDG 2024 quark masses (MS-bar at 2 GeV for u,d,s; pole-like for c,b,t)
PDG_QUARKS = {
    'up':      {'N': N_u, 'mass_MeV': 2.16,   'mass_err': 0.49,  'note': 'MS-bar at 2 GeV'},
    'down':    {'N': N_d, 'mass_MeV': 4.67,   'mass_err': 0.48,  'note': 'MS-bar at 2 GeV'},
    'strange': {'N': N_s, 'mass_MeV': 93.4,   'mass_err': 8.6,   'note': 'MS-bar at 2 GeV'},
    'charm':   {'N': N_c, 'mass_MeV': 1270.0, 'mass_err': 20.0,  'note': 'MS-bar at m_c'},
    'bottom':  {'N': N_b, 'mass_MeV': 4180.0, 'mass_err': 30.0,  'note': 'MS-bar at m_b'},
    'top':     {'N': N_t, 'mass_MeV': 172760., 'mass_err': 300.,  'note': 'pole mass'},
}


def Ce_route_A(nu, delta_val):
    """Route A elliptic formula (Law 33) applied at any epoch."""
    K = ellipk(nu)
    E = ellipe(nu)
    return abs(delta_val) * K + nu / 2 - lambda_rec_beta * (K - E) / 3 + alpha_EM / (2 * pi)


# ============================================================================
# MAIN
# ============================================================================

print("=" * 90)
print("QUARK WINDING NUMBERS AND C-FACTORS")
print("Bottom-Up Proton Mass Derivation — Phase 1")
print("=" * 90)

# ------------------------------------------------------------------
# STEP 1: RUN WINDING SOLVER FOR ALL QUARK EPOCHS
# ------------------------------------------------------------------

print("""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║  STEP 1: WINDING NUMBERS FOR ALL 6 QUARK EPOCHS                                    ║
║  Using the 4-layer algorithm with the quark admissibility lattice                   ║
╚══════════════════════════════════════════════════════════════════════════════════════╝
""")

quark_results = {}
quark_order = ['up', 'down', 'strange', 'charm', 'bottom', 'top']

for name in quark_order:
    info = PDG_QUARKS[name]
    N = info['N']

    print(f"\n{'─' * 80}")
    print(f"  {name.upper()} QUARK (N = {N})")
    print(f"{'─' * 80}")

    # Try quark lattice first
    result = find_winding_numbers(N, sector='quark', require_primitive=True, verbose=True)

    if result is None:
        print(f"\n  No primitive winding in quark lattice. Trying universal fallback...")
        result = find_winding_universal(N, verbose=True)

    if result is not None:
        print()
        print_result(result, indent="  ")
    else:
        print(f"  WARNING: No winding found even in universal lattice for N={N}")

    quark_results[name] = result

# ------------------------------------------------------------------
# STEP 2: SUMMARY TABLE
# ------------------------------------------------------------------

print(f"\n\n{'=' * 90}")
print("STEP 2: COMPLETE QUARK WINDING NUMBER TABLE")
print("=" * 90)

print(f"\n  {'Quark':>8s}  {'N':>4s}  {'(p, q)':>12s}  {'gcd':>4s}  {'prim':>5s}  "
      f"{'Lattice':>9s}  {'L_Ω':>10s}  {'ν':>10s}  {'k_res':>5s}  {'δ':>8s}  {'res':>4s}")
print("  " + "─" * 100)

for name in quark_order:
    r = quark_results[name]
    N = PDG_QUARKS[name]['N']
    if r is not None:
        passes_r, _, _ = resonance_filter(N)
        g = gcd(r.abs_p, r.abs_q)
        print(f"  {name:>8s}  {N:>4d}  ({r.p:+4d}, {r.q:3d})  {g:>4d}  "
              f"{'Y' if r.coprime else 'N':>5s}  {r.lattice_name:>9s}  "
              f"{float(r.l_Omega):>10.4f}  {float(r.nu):>10.6f}  "
              f"{r.k_res:>5d}  {r.delta:>+8.4f}  "
              f"{'PASS' if passes_r else 'FAIL':>4s}")
    else:
        print(f"  {name:>8s}  {N:>4d}  {'NONE':>12s}")

# ------------------------------------------------------------------
# STEP 3: C-FACTORS FROM ELLIPTIC FORMULA
# ------------------------------------------------------------------

print(f"\n\n{'=' * 90}")
print("STEP 3: QUARK C-FACTORS FROM ROUTE A ELLIPTIC FORMULA")
print("=" * 90)

print("""
  The Route A formula gives the shape factor C for free solitons:

    C(ν, δ) = |δ|·K(ν) + ν/2 − (λ_rec/β)·(K−E)/3 + α_EM/(2π)

  For the electron at N=111: C_e = 1.00014 → gives m_e to 23 ppm.
  For quarks: this formula assumes FREE solitons, which quarks are NOT.
  The results below test whether the formula gives reasonable quark masses
  despite the confinement caveat.
""")

# First compute electron C_e for reference
electron_result = find_winding_numbers(111, sector='lepton')
if electron_result:
    C_e = Ce_route_A(electron_result.nu, electron_result.delta)
    m_e_pred = float(C_e * M_P * phi**(-111))
    print(f"  REFERENCE — Electron (N=111):")
    print(f"    C_e = {float(C_e):.10f}")
    print(f"    m_e = C_e × M_P × φ^(-111) = {m_e_pred:.6f} MeV  (CODATA: 0.51100 MeV)")
    print()

print(f"\n  {'Quark':>8s}  {'N':>4s}  {'ν':>10s}  {'δ':>10s}  {'C_q':>12s}  "
      f"{'M_P·φ^(-N)':>12s}  {'C_q·M_P·φ^(-N)':>15s}  {'PDG':>10s}  {'Ratio':>8s}")
print("  " + "─" * 105)

c_factors = {}
for name in quark_order:
    r = quark_results[name]
    info = PDG_QUARKS[name]
    N = info['N']
    m_pdg = info['mass_MeV']

    if r is not None:
        C_q = Ce_route_A(r.nu, r.delta)
        bare_scale = float(M_P * phi**(-N))
        m_pred = float(C_q) * bare_scale
        ratio = m_pred / m_pdg if m_pdg > 0 else float('inf')

        c_factors[name] = {
            'C_q': float(C_q),
            'bare_scale': bare_scale,
            'm_pred': m_pred,
            'm_pdg': m_pdg,
            'ratio': ratio,
        }

        print(f"  {name:>8s}  {N:>4d}  {float(r.nu):>10.6f}  {r.delta:>+10.4f}  "
              f"{float(C_q):>12.6f}  {bare_scale:>12.4f}  {m_pred:>15.4f}  "
              f"{m_pdg:>10.2f}  {ratio:>8.4f}")
    else:
        print(f"  {name:>8s}  {N:>4d}  {'—':>10s}  {'—':>10s}  {'—':>12s}  "
              f"{'—':>12s}  {'—':>15s}  {m_pdg:>10.2f}  {'—':>8s}")

# ------------------------------------------------------------------
# STEP 4: ANALYSIS
# ------------------------------------------------------------------

print(f"\n\n{'=' * 90}")
print("STEP 4: HONEST ANALYSIS")
print("=" * 90)

print("""
  KEY FINDINGS:

  1. QUARK LATTICE RESULTS:
     The quark admissibility lattice (q = 30s, p = 2t − s) produces valid
     primitive windings for some quark epochs but not others. This is a
     structural consequence of the quark's SU(5) gauge congruences.

  2. C-FACTOR INTERPRETATION:
     The Route A elliptic formula C(ν, δ) was DERIVED for the electron
     (a free charged lepton). Applying it to quarks is a HYPOTHESIS.
     The formula assumes a free soliton on the Ω-torus, but quarks are
     CONFINED inside hadrons — their wave function is fundamentally
     different from a free soliton.

  3. WHAT THIS MEANS FOR THE PROTON:
     The bottom-up proton mass requires individual quark contributions.
     If C_q ≈ O(1) like C_e, the quark mass contributions are small
     (~few MeV) compared to the total proton mass (938 MeV).
     The dominant contribution comes from QCD confinement (gluons),
     not from quark rest masses.

  CONFINEMENT CAVEAT (critical):
     The current quark masses in the PDG (m_u ≈ 2.2 MeV, m_d ≈ 4.7 MeV)
     are MS-bar scheme masses at μ = 2 GeV. They are scheme-dependent
     and NOT directly comparable to M_P · φ^(-N_q) (bare scale).
     The GU bare scale masses need to be run from the Planck scale
     down to μ = 2 GeV via the QCD RG equations to make a valid
     comparison. This RG running is NOT yet implemented.
""")

# ------------------------------------------------------------------
# STEP 5: BARE SCALE vs PDG — WITHOUT C-FACTORS
# ------------------------------------------------------------------

print(f"\n{'=' * 90}")
print("STEP 5: BARE SCALE MASSES vs PDG (no C-factor)")
print("=" * 90)

print(f"\n  For completeness, compare the bare φ-ladder scales to PDG:")
print(f"\n  {'Quark':>8s}  {'N':>4s}  {'M_P·φ^(-N) [MeV]':>20s}  {'PDG [MeV]':>12s}  "
      f"{'Ratio PDG/bare':>15s}  {'log_φ(ratio)':>14s}")
print("  " + "─" * 80)

for name in quark_order:
    N = PDG_QUARKS[name]['N']
    m_pdg = PDG_QUARKS[name]['mass_MeV']
    bare = float(M_P * phi**(-N))
    ratio = m_pdg / bare
    log_ratio = float(ln(mpf(str(ratio))) / ln(phi)) if ratio > 0 else 0.0
    print(f"  {name:>8s}  {N:>4d}  {bare:>20.6f}  {m_pdg:>12.2f}  "
          f"{ratio:>15.4f}  {log_ratio:>14.4f}")

print("""
  INTERPRETATION:
    - The ratio PDG/bare tells us how much C_q (including RG running,
      confinement effects, and scheme matching) would need to be.
    - If log_φ(ratio) ≈ integer, it means the PDG mass is at a
      DIFFERENT effective epoch N_eff = N - round(log_φ(ratio)).
    - This is NOT a derivation — it's diagnostic information.
""")

# ------------------------------------------------------------------
# STEP 6: PROTON VALENCE QUARK CONTRIBUTION
# ------------------------------------------------------------------

print(f"\n{'=' * 90}")
print("STEP 6: PROTON VALENCE QUARK CONTRIBUTION (bare scale)")
print("=" * 90)

m_u_bare = float(M_P * phi**(-N_u))
m_d_bare = float(M_P * phi**(-N_d))
E_phase_bare = 2 * m_u_bare + m_d_bare

m_u_pdg = PDG_QUARKS['up']['mass_MeV']
m_d_pdg = PDG_QUARKS['down']['mass_MeV']
E_phase_pdg = 2 * m_u_pdg + m_d_pdg

m_p_codata = 938.27208816

print(f"""
  Valence quarks: u + u + d

  Bare scale (M_P · φ^(-N)):
    m_u = M_P · φ^(-{N_u}) = {m_u_bare:.6f} MeV
    m_d = M_P · φ^(-{N_d}) = {m_d_bare:.6f} MeV
    E_phase = 2·m_u + m_d = {E_phase_bare:.6f} MeV  ({E_phase_bare/m_p_codata*100:.3f}% of m_p)

  PDG current masses:
    m_u = {m_u_pdg:.2f} ± {PDG_QUARKS['up']['mass_err']:.2f} MeV
    m_d = {m_d_pdg:.2f} ± {PDG_QUARKS['down']['mass_err']:.2f} MeV
    E_phase = 2·m_u + m_d = {E_phase_pdg:.2f} MeV  ({E_phase_pdg/m_p_codata*100:.3f}% of m_p)

  CONCLUSION:
    Current quark masses (whether from bare scale or PDG) contribute
    less than 1% of the proton mass. The proton is overwhelmingly
    a QCD phenomenon — its mass comes from gluon dynamics and the
    trace anomaly, not from quark rest masses.
    
    The E_phase term in the 4-term ansatz is a SMALL correction.
    Getting C_q exactly right matters for precision but not for
    the leading-order proton mass.
""")

# ------------------------------------------------------------------
# SUMMARY
# ------------------------------------------------------------------

print("=" * 90)
print("SUMMARY — PHASE 1 COMPLETE")
print("=" * 90)

n_quark_lattice = sum(1 for r in quark_results.values()
                      if r is not None and r.lattice_name == 'quark')
n_universal = sum(1 for r in quark_results.values()
                  if r is not None and r.lattice_name == 'universal')
n_failed = sum(1 for r in quark_results.values() if r is None)

print(f"""
  Quark lattice primitive windings: {n_quark_lattice}/6
  Universal fallback windings:      {n_universal}/6
  No winding found:                 {n_failed}/6

  The quark admissibility lattice works for epochs where the lattice
  generator q=30s allows coprime (p,q) pairs. For some epochs,
  the universal fallback is needed.

  C-FACTORS:
    The Route A elliptic formula provides C_q values, but their physical
    meaning for confined quarks is uncertain. The free-soliton assumption
    behind Route A may not apply inside a hadron.

  NEXT STEPS (Phase 2):
    → Derive gluon contributions at N_QCD=95
    → These dominate the proton mass (~99% comes from QCD dynamics)
""")
