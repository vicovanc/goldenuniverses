#!/usr/bin/env python3
"""
QUARK MASS SUMMARY — COMPILATION OF ALL FIVE DERIVATION ROUTES (A1–A5)
========================================================================

Compiles results from:
  Route A: Yukawa / SU(5) — Clebsch-Gordan + confinement for light; C_q ~ 1 for heavy
  Route B: Confined soliton (NLDE) — constituent masses ~300 MeV, not current
  Route C: RG running — C_RG ~ 2–3 from Planck to 2 GeV
  Route D: Mass ratios — heavy (c/s, t/b) within factor ~2; light m_u/m_d = φ^(-5) vs PDG
  Route E: NJL constituent — M_const ~ 300–310 MeV for u,d; constituent ≈ current for heavy

Produces a final assessment: what is derived vs what requires more work.
Uses numpy only; no graphing.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np

from utils.gu_constants import (
    N_u, N_d, N_s, N_b, N_t,
)
from utils.gu_constants import N_c as N_charm_epoch

# -----------------------------------------------------------------------------
# Constants (numpy; user spec)
# -----------------------------------------------------------------------------
phi = (1 + np.sqrt(5)) / 2
M_P = 1.22089e22   # MeV

# PDG masses: MS-bar at 2 GeV for u,d,s; at m_c for charm; at m_b for bottom; pole for top
PDG_MeV = {
    'up':    2.16,
    'down':  4.67,
    'strange': 93.4,
    'charm':  1270.0,
    'bottom': 4180.0,
    'top':    172760.0,
}

# Epochs (charm as N_charm_epoch to avoid clash with N_colors=3)
N_q = {
    'up':     N_u,
    'down':   N_d,
    'strange': N_s,
    'charm':  N_charm_epoch,
    'bottom': N_b,
    'top':    N_t,
}

quark_order = ['up', 'down', 'strange', 'charm', 'bottom', 'top']

# -----------------------------------------------------------------------------
# Bare scale masses: M_P * φ^(-N_q)
# -----------------------------------------------------------------------------
def bare_scale(epoch):
    return M_P * (phi ** (-epoch))

bare_MeV = {q: bare_scale(N_q[q]) for q in quark_order}

# -----------------------------------------------------------------------------
# Route summaries (qualitative / representative numbers)
# -----------------------------------------------------------------------------
# Route A: Yukawa/SU(5): heavy C_q ~ 1; light need SU(5) Clebsch + confinement
route_A_note = "Heavy: C_q ~ 1. Light: need SU(5) Clebsch + confinement."

# Route B: Confined soliton → constituent ~300 MeV, not current masses
M_constituent_light_MeV = 300.0   # representative
route_B_note = f"Constituent ~{M_constituent_light_MeV:.0f} MeV for light quarks (not current)."

# Route C: RG running C_RG ~ 2–3
C_RG_min, C_RG_max = 2.0, 3.0
route_C_note = f"C_RG ~ {C_RG_min}-{C_RG_max} from Planck to 2 GeV (partial gap)."

# Route D: mass ratios — heavy within ~factor 2; light ratio
Delta_N_ud = N_d - N_u   # 105 - 110 = -5 → φ^(-5) for m_u/m_d
phi_ratio_ud = phi ** (-5)
PDG_ratio_ud = PDG_MeV['up'] / PDG_MeV['down']
route_D_note = f"Heavy ratios (c/s, t/b) within factor ~2. m_u/m_d: GU φ^(-5)={phi_ratio_ud:.3f} vs PDG {PDG_ratio_ud:.2f}."

# Route E: NJL constituent
M_njl_u, M_njl_d = 300.0, 310.0   # MeV
route_E_note = f"Constituent M_const ~ {M_njl_u:.0f}-{M_njl_d:.0f} MeV for u,d; constituent ≈ current for heavy."

# Proton mass (for conclusion)
m_proton_MeV = 938.272
M_const_avg = (M_njl_u + M_njl_d) / 2
proton_over_3 = m_proton_MeV / 3

# -----------------------------------------------------------------------------
# Print: header and constants
# -----------------------------------------------------------------------------
print("=" * 90)
print("QUARK MASS SUMMARY — ALL FIVE DERIVATION ROUTES (A1–A5)")
print("=" * 90)

print("\n--- Constants ---")
print(f"  φ = (1+√5)/2 = {phi:.10f}")
print(f"  M_P = {M_P:.5e} MeV")
print(f"  Epochs: N_u={N_u}, N_d={N_d}, N_s={N_s}, N_charm={N_charm_epoch}, N_b={N_b}, N_t={N_t}")

# -----------------------------------------------------------------------------
# Table 1: Per-quark bare scale vs PDG
# -----------------------------------------------------------------------------
print("\n" + "─" * 90)
print("  TABLE 1: BARE SCALE vs PDG (current masses)")
print("  Bare: M_P × φ^(-N_q).  PDG: MS-bar at 2 GeV (u,d,s); at m_c (c); at m_b (b); pole (t).")
print("─" * 90)
print(f"  {'Quark':>8}  {'N_q':>5}  {'Bare (MeV)':>14}  {'PDG (MeV)':>12}  {'PDG/Bare':>12}  {'Note':>20}")
print("  " + "─" * 90)

for q in quark_order:
    b = bare_MeV[q]
    p = PDG_MeV[q]
    ratio = p / b if b > 0 else 0
    note = "heavy" if p > 100 else "light"
    print(f"  {q:>8}  {N_q[q]:>5}  {b:>14.4e}  {p:>12.2f}  {ratio:>12.4e}  {note:>20}")

# -----------------------------------------------------------------------------
# Table 2: Route-by-route summary
# -----------------------------------------------------------------------------
print("\n" + "─" * 90)
print("  TABLE 2: ROUTE-BY-ROUTE SUMMARY")
print("─" * 90)
print("  Route A (Yukawa/SU(5)):  " + route_A_note)
print("  Route B (Confined soliton): " + route_B_note)
print("  Route C (RG running):    " + route_C_note)
print("  Route D (Mass ratios):  " + route_D_note)
print("  Route E (NJL constituent): " + route_E_note)

# -----------------------------------------------------------------------------
# Table 3: Light vs heavy — what works
# -----------------------------------------------------------------------------
print("\n" + "─" * 90)
print("  TABLE 3: LIGHT vs HEAVY — WHAT WORKS")
print("─" * 90)
print("  Heavy (t, b, c):  φ-ladder within factor ~2; RG running helps close gap.")
print("  Light (u, d, s):  φ-ladder gives wrong ratios; need Yukawa structure (Clebsch, flavor).")
print("  Proton mass:      Dominated by QCD dynamics (E_self), not quark current masses.")
print(f"  NJL constituent: M_const ~ {M_const_avg:.0f} MeV  →  proton/3 ≈ {proton_over_3:.1f} MeV  (match).")

# -----------------------------------------------------------------------------
# Honest assessment: derived vs more work
# -----------------------------------------------------------------------------
print("\n" + "=" * 90)
print("  HONEST ASSESSMENT: DERIVED vs REQUIRES MORE WORK")
print("=" * 90)

print("\n  DERIVED / WELL SUPPORTED:")
print("    • Heavy quark hierarchy (t > b > c): φ-ladder ordering and rough scale (factor ~2).")
print("    • RG running from Planck to low scale: C_RG ~ 2–3 captures part of the gap.")
print("    • Mass ratios for heavy quarks (e.g. c/s, t/b): within factor ~2 of PDG.")
print("    • Proton mass: dominated by E_self (QCD/confinement), not current quark masses.")
print("    • Constituent masses: NJL gives M_const ~ 300–310 MeV; proton/3 ≈ 313 MeV.")

print("\n  REQUIRES MORE WORK:")
print("    • Light quark current masses (u, d, s): absolute values and ratios (e.g. m_u/m_d) need")
print("      Yukawa/SU(5) Clebsch and flavor structure; φ^(-5) gives m_u/m_d ≈ 0.09 vs PDG ≈ 0.46.")
print("    • Exact C_q factors for each flavor from first principles (Route A).")
print("    • Precise connection: bare scale → MS-bar at 2 GeV (scheme and scale matching).")

# -----------------------------------------------------------------------------
# Key conclusions (numbered)
# -----------------------------------------------------------------------------
print("\n" + "=" * 90)
print("  KEY CONCLUSIONS")
print("=" * 90)
print("  1. Heavy quarks (t, b, c): φ-ladder works within factor ~2; RG running helps.")
print("  2. Light quarks (u, d, s): φ-ladder gives wrong ratios; need Yukawa structure.")
print("  3. Proton mass is dominated by QCD dynamics (E_self), not quark current masses.")
print("  4. NJL constituent masses match proton/3 ~ 313 MeV.")
print("=" * 90)
