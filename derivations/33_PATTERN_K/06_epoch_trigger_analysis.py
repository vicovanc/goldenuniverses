#!/usr/bin/env python3
"""
06_epoch_trigger_analysis.py
============================

What "Pattern-k" really means in the primary GU theory.

From the Formation document (Section 1.4.2) and theory-laws.md (line 7065):
Pattern-k is NOT a multiplicative factor pi^k. It is an EPOCH TRIGGER —
an index labeling WHICH SECTOR of V_Omega goes critical (m^2 crosses zero)
at which X-value.

This script traces the epoch triggers and shows that "k" labels the sequence
of phase transitions, not a power of pi.

Reference:
  - Formation.md, lines 188-212 (Section 1.4.2)
  - theory-laws.md, lines 7065-7067
  - V2.md, line 563, 706, 1543
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from utils.gu_constants import phi, pi, M_P, M_0, N_GUT, N_EW, N_QCD, N_e

PI = float(pi)
PHI = float(phi)
MP = float(M_P)
M0 = float(M_0)

print("=" * 80)
print("WHAT 'PATTERN-K' REALLY MEANS")
print("Epoch triggers, not multiplicative pi^k")
print("=" * 80)

# ============================================================================
# THE PRIMARY THEORY DEFINITION
# ============================================================================

print("\n" + "-" * 80)
print("THE PRIMARY THEORY DEFINITION")
print("(Formation.md, Section 1.4.2; theory-laws.md lines 7065-7067)")
print("-" * 80)

print("""
  The Master Potential (Formation.md, line 194):

    V_Omega = m_H^2(X) * (H†H) + m_Q^2(X) * (Q†Q) + lambda_H(X) * (H†H)^2 + ...

  Pattern-k labels the SEQUENCE of phase transitions:

    k=0 (Primordial, high X):  m_H^2(X) > 0, m_Q^2(X) > 0
                                All symmetries manifest, no structure.

    k=1 (EW, X ≈ X_EW):       m_H^2(X_EW) = 0
                                H condenses, SU(2)_L x U(1)_Y -> U(1)_EM

    k=2 (QCD, X ≈ X_QCD):     m_Q^2(X) term + gluon dynamics dominate
                                Q confines into hadrons, SU(3)_C confining

  FROM V2.md (line 563):
    "It is not Omega literally splitting, but rather the X-driven dynamics
    of L_total causing different irreducible representations within V_prim
    to become dynamically significant at different cosmic epochs X_k."

  FROM V2.md (line 706):
    "Pattern-k layers = phase transitions triggered by X-driven evolution"

  CRUCIALLY: k is an INTEGER INDEX labeling the phase transition,
  NOT a power of pi. There is no factor of pi^k anywhere in these
  definitions.
""")

# ============================================================================
# COMPUTING THE EPOCH THRESHOLDS
# ============================================================================

print("-" * 80)
print("THE EPOCH THRESHOLDS: X_k values from the golden ladder")
print("-" * 80)

def X_at_epoch(N):
    return MP * PHI**(-N)

epochs = [
    ("k=3: GUT unification",   N_GUT, "SU(5) -> SM"),
    ("k=1: Electroweak",       N_EW,  "SU(2)xU(1) -> U(1)_EM"),
    ("k=2: QCD confinement",   N_QCD, "SU(3) confining"),
    ("k=0: EM / lepton",       N_e,   "Stable leptons form"),
]

print(f"\n  {'Epoch':<30} {'N':<6} {'X (MeV)':<16} {'Transition'}")
print("  " + "-" * 70)
for name, N, transition in epochs:
    X = X_at_epoch(N)
    print(f"  {name:<30} {N:<6} {X:<16.4f} {transition}")

print(f"""
  The ordering in X (descending, as the universe cools):
    1. GUT:  N={N_GUT}, X ~ {X_at_epoch(N_GUT):.0e} MeV  (~ 10^16 GeV — GUT scale)
    2. EW:   N={N_EW}, X ~ {X_at_epoch(N_EW):.2f} MeV      (~ 100-200 GeV)
    3. QCD:  N={N_QCD}, X ~ {X_at_epoch(N_QCD):.2f} MeV       (~ 0.2 GeV — Lambda_QCD)
    4. EM:   N={N_e}, X ~ {X_at_epoch(N_e):.4f} MeV           (~ 0.5 MeV — electron mass)
""")

# ============================================================================
# THE m^2(X) FUNCTIONS — when do they cross zero?
# ============================================================================

print("-" * 80)
print("THE m^2(X) FUNCTIONS: what triggers each transition?")
print("-" * 80)

print("""
  From the Formation document, the effective mass-squared terms in V_Omega
  are FUNCTIONS of X. Schematically:

    m_H^2(X) = mu_H^2 * (1 - X_EW^2/X^2)   for the Higgs doublet
    m_Q^2(X) = mu_Q^2 * (1 - X_QCD^2/X^2)   for the quark triplet

  where mu_H and mu_Q are GU parameters built from M_0, pi, phi.

  Phase transition occurs when m^2(X_crit) = 0, i.e., X_crit = X_k.

  The DIFFERENT X_k for different sectors comes from DIFFERENT mu and
  different phi-scaling in the potential — NOT from pi^k factors.
""")

X_EW = X_at_epoch(N_EW)
X_QCD = X_at_epoch(N_QCD)

X_vals = np.logspace(np.log10(0.01), np.log10(1e13), 500)

print("  Schematic m^2(X) behavior:")
print(f"  {'X (MeV)':<15} {'m_H^2 sign':<15} {'m_Q^2 sign':<15} {'Pattern'}")
print("  " + "-" * 55)
X_display = [1e12, 1e8, X_EW*1.1, X_EW*0.9, X_QCD*1.1, X_QCD*0.9, 1.0, 0.01]
for X in X_display:
    m_H2 = "+" if X > X_EW else "-"
    m_Q2 = "+" if X > X_QCD else "-"
    if X > X_EW:
        pattern = "k=0 (symmetric)"
    elif X > X_QCD:
        pattern = "k=1 (EW broken)"
    else:
        pattern = "k=2 (QCD confining)"
    print(f"  {X:<15.2e} {m_H2:<15} {m_Q2:<15} {pattern}")

# ============================================================================
# THE KEY INSIGHT: k COUNTS BROKEN SECTORS, NOT pi POWERS
# ============================================================================

print("\n" + "-" * 80)
print("THE KEY INSIGHT: k counts broken sectors, not pi powers")
print("-" * 80)

print("""
  k = (number of gauge sectors that have undergone phase transition)

    k=0: 0 sectors broken — symmetric vacuum
    k=1: 1 sector broken (EW) — Higgs condensed, W/Z massive
    k=2: 2 sectors broken (EW + QCD confining) — quarks confined to hadrons

  This is like counting the number of symmetry-breaking steps in a
  sequential phase transition. It has nothing to do with pi.

  In standard physics, the same idea exists:
    - At T >> T_EW: full SU(3)xSU(2)xU(1) symmetry
    - At T_QCD < T < T_EW: EW broken, QCD deconfined (quark-gluon plasma)
    - At T < T_QCD: EW broken, QCD confined (our world)

  The GU contribution is that the THRESHOLDS X_k are derivable from
  the golden ladder: X_k = M_P * phi^(-N_k), and the epochs N_k
  are determined by the V_Omega structure with pi, phi parameters.
""")

# ============================================================================
# WHERE pi^k APPEARS (AND DOESN'T) IN THE EPOCH ANALYSIS
# ============================================================================

print("-" * 80)
print("WHERE pi^k APPEARS (AND DOESN'T) IN THE EPOCH ANALYSIS")
print("-" * 80)

print(f"""
  Let's check if there's any correlation between pi^k and the epoch scales:

  k=0: X_EM  = M_P * phi^(-{N_e})  = {X_at_epoch(N_e):.4f} MeV
       pi^0  = 1
       X_EM * pi^0 = {X_at_epoch(N_e) * 1:.4f} MeV

  k=1: X_EW  = M_P * phi^(-{N_EW})  = {X_at_epoch(N_EW):.2f} MeV
       pi^1  = {PI:.4f}
       X_EW * pi^1 = {X_at_epoch(N_EW) * PI:.2f} MeV
       X_EW / pi^1 = {X_at_epoch(N_EW) / PI:.2f} MeV

  k=2: X_QCD = M_P * phi^(-{N_QCD}) = {X_at_epoch(N_QCD):.2f} MeV
       pi^2  = {PI**2:.4f}
       X_QCD * pi^2 = {X_at_epoch(N_QCD) * PI**2:.2f} MeV
       X_QCD / pi^2 = {X_at_epoch(N_QCD) / PI**2:.2f} MeV

  None of these produce meaningful physical scales. The epoch scales X_k
  are determined by phi^(-N_k), not by pi^k.
""")

# ============================================================================
# THE RATIO X_k / X_{k-1} — is it pi?
# ============================================================================

print("-" * 80)
print("THE RATIO X_k / X_{k-1} — is it pi?")
print("-" * 80)

X_GUT_val = X_at_epoch(N_GUT)
X_EW_val = X_at_epoch(N_EW)
X_QCD_val = X_at_epoch(N_QCD)
X_EM_val = X_at_epoch(N_e)

print(f"  X_GUT / X_EW  = phi^({N_EW}-{N_GUT}) = phi^{N_EW-N_GUT} = {PHI**(N_EW-N_GUT):.4e}")
print(f"  X_EW / X_QCD  = phi^({N_QCD}-{N_EW}) = phi^{N_QCD-N_EW} = {PHI**(N_QCD-N_EW):.4e}")
print(f"  X_QCD / X_EM  = phi^({N_e}-{N_QCD}) = phi^{N_e-N_QCD} = {PHI**(N_e-N_QCD):.4e}")
print()
print(f"  pi^13  = {PI**13:.4e}")
print(f"  pi^15  = {PI**15:.4e}")
print(f"  pi^16  = {PI**16:.4e}")
print()
print(f"  These ratios are phi^(Delta_N), not pi^anything.")
print(f"  The golden ladder uses phi, not pi, for scale separation.")

# ============================================================================
# THE FORMATION DOCUMENT'S OWN WORDS
# ============================================================================

print("\n" + "-" * 80)
print("THE FORMATION DOCUMENT'S OWN WORDS")
print("-" * 80)

print("""
  Formation.md, line 190:
    "The abstract concept of the 'Pattern-k recursive split' [...] is not
    a separate postulate. It is a phenomenological DESCRIPTION of the
    solutions to the Euler-Lagrange equations derived from L_total."

  Formation.md, line 212:
    "The 'Pattern-k' model is therefore a powerful SHORTHAND for
    describing the sequential condensation of different components of
    the single, unified Omega field"

  V2.md, line 706:
    "'Pattern-k layers' of our effective U_n model" — LAYERS, not
    multiplicative factors.

  These are the PRIMARY theory documents. They define Pattern-k as:
    1. An EPOCH LABEL (which transition happened)
    2. A SHORTHAND (not a formula)
    3. A DESCRIPTION of solutions (not a separate postulate)

  Pattern-k is NOT defined as "multiply by pi^k" anywhere in these docs.
""")

# ============================================================================
# VERDICT
# ============================================================================

print("=" * 80)
print("VERDICT: Pattern-k is an epoch trigger")
print("=" * 80)

print(f"""
  PATTERN-k IN PRIMARY THEORY:
    k = sequence index for V_Omega phase transitions
    k=0: symmetric vacuum (all m^2 > 0)
    k=1: EW symmetry breaking (m_H^2 crosses zero at X_EW)
    k=2: QCD confinement (gluon dynamics dominate at X_QCD)
    k=3: GUT unification (SU(5) -> SM at X_GUT)

  WHAT PATTERN-k IS NOT:
    - Not a multiplicative factor pi^k
    - Not a coupling enhancement
    - Not derived from the Lagrangian as L_eff = L_0 * pi^k

  THE FORMULA "L_eff = L_0 * pi^k":
    - First appears in COMPLETE_GOLDEN_UNIVERSE_THEORY.md (secondary summary)
    - NOT present in theory-laws.md (primary)
    - NOT present in Formation.md (primary)
    - NOT present in V2.md (primary)
    - Propagated to 40+ derivation scripts via gu_constants.py pattern_factor(k)
    - Should be retired as a heuristic that was over-propagated

  THE CORRECT INTERPRETATION:
    Pattern-k tells you WHICH EPOCH you're in, and therefore which terms
    in V_Omega are dynamically important. The mass formula m = M_P * C *
    (2*pi/phi^N) gets its pi from the recursion phase (Script 02),
    not from Pattern-k.
""")

print("=" * 80)
print("DONE: 06_epoch_trigger_analysis.py")
print("=" * 80)
