#!/usr/bin/env python3
"""
PI-STACKING AND PHASE MEMORY IN DNA
=======================================

** KEY GU SCRIPT **

Pi-stacking between adjacent base pairs is the PRIMARY stabiliser of
the DNA double helix — contributing MORE than hydrogen bonds. In GU,
pi-stacking creates a CONTINUOUS PHASE MEMORY CHANNEL (theta-FF-tilde)
along the entire DNA molecule.

This is the central GU insight for DNA: the structure most important
for stability is ALSO the structure that carries nonlocal memory.

Upstream: 23_MOLECULAR_BONDS (sections 11-12), 21_ELECTROMAGNETISM
Status:   Standard physics (stacking energetics) + KEY GU interpretation
          (phase memory channel). theta-FF-tilde energy: qualitative.

Date: February 2026
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mpmath import mp, mpf, sqrt, pi as mp_pi, exp
import numpy as np

mp.dps = 30
phi = (mpf('1') + sqrt(mpf('5'))) / 2
pi = mp_pi
alpha_EM = mpf('1') / mpf('137.035999177')
m_e = mpf('0.51099895')       # MeV
hbar_c = mpf('197.3269804')   # MeV·fm
a_0_fm = float(hbar_c / (alpha_EM * m_e))
a_0_A = a_0_fm / 1e5
k_B_eV = 8.617333e-5

print("=" * 80)
print("PI-STACKING AND PHASE MEMORY IN DNA")
print("The primary stabiliser and the memory channel")
print("=" * 80)


# ============================================================================
# PART 1: WHAT IS PI-STACKING?
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 1: WHAT IS PI-STACKING?                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

Pi-stacking is the attractive interaction between PARALLEL aromatic rings
separated by ~3.4 Angstrom. In DNA, adjacent base pairs stack on top of
each other like coins in a pile.

  GEOMETRY:
    Base pair n:      [  purine --- pyrimidine  ]    ← flat, aromatic
                                 ↕ 3.4 A rise
    Base pair n+1:    [  purine --- pyrimidine  ]    ← flat, aromatic

    The pi orbitals extend ~1.7 A above and below each base plane.
    At 3.4 A separation, they OVERLAP vertically:
      Gap = 3.4 - 2*1.7 = 0.0 A → the pi clouds are TOUCHING

  PHYSICAL ORIGIN (three contributions):
    1. London dispersion (~60%): correlated electron fluctuations in
       polarisable pi systems. Scales as alpha^2 / r^6 where alpha
       is polarisability.

    2. Electrostatic (~30%): interaction between the permanent multipole
       moments of the aromatic bases (dipoles, quadrupoles).
       Sequence-dependent (depends on which bases are stacking).

    3. Exchange-repulsion (short range): Pauli exclusion prevents
       full overlap. Creates the ~3.4 A equilibrium distance.
""")


# ============================================================================
# PART 2: STACKING ENERGETICS
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 2: STACKING ENERGETICS — SEQUENCE DEPENDENCE                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

Stacking energy depends on WHICH base pairs are adjacent.
There are 10 unique nearest-neighbour steps in DNA.
""")

stacking_data = [
    ('GC/GC', -0.61, 'strongest'),
    ('CG/CG', -0.44, 'strong'),
    ('GC/CG', -0.56, 'strong'),
    ('CG/GC', -0.48, 'strong'),
    ('AT/AT', -0.29, 'moderate'),
    ('TA/TA', -0.19, 'moderate'),
    ('AT/GC', -0.44, 'strong'),
    ('GC/AT', -0.35, 'moderate'),
    ('AT/CG', -0.30, 'moderate'),
    ('TA/CG', -0.27, 'moderate'),
]

print(f"  {'Step':>8s} | {'E_stack (eV)':>12s} | {'E_stack (kcal/mol)':>18s} | {'Strength':>10s}")
print("  " + "-" * 60)
for step, e_eV, strength in stacking_data:
    e_kcal = e_eV * 23.060
    print(f"  {step:>8s} | {e_eV:>12.2f} | {e_kcal:>18.1f} | {strength:>10s}")

energies = [e for _, e, _ in stacking_data]
mean_stack = np.mean(energies)
print("  " + "-" * 60)
print(f"  {'Mean':>8s} | {mean_stack:>12.2f} | {mean_stack*23.060:>18.1f} |")
print()

print(f"  Key observations:")
print(f"    Strongest stacking: GC/GC ({stacking_data[0][1]:.2f} eV)")
print(f"    Weakest stacking:   TA/TA ({stacking_data[5][1]:.2f} eV)")
print(f"    Range:              {max(energies):.2f} to {min(energies):.2f} eV")
print(f"    GC steps are generally stronger than AT steps")
print()


# ============================================================================
# PART 3: STACKING VS H-BONDS — WHICH MATTERS MORE?
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 3: STACKING VS H-BONDS — THE SURPRISING ANSWER                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

A crucial and counter-intuitive experimental result:

  PI-STACKING contributes MORE to DNA stability than HYDROGEN BONDS.
""")

E_hbond_AT = 0.13   # eV per A-T pair in aqueous solution
E_hbond_GC = 0.22   # eV per G-C pair in aqueous solution
E_stack_avg = abs(mean_stack)

print(f"  Per base pair step (aqueous, room temperature):")
print(f"    H-bond contribution (A-T): ~{E_hbond_AT:.2f} eV")
print(f"    H-bond contribution (G-C): ~{E_hbond_GC:.2f} eV")
print(f"    Stacking contribution:     ~{E_stack_avg:.2f} eV (average)")
print()
print(f"    Ratio (stacking / H-bond):  {E_stack_avg/E_hbond_AT:.1f}x (vs A-T)")
print(f"                                {E_stack_avg/E_hbond_GC:.1f}x (vs G-C)")
print()

print("""  EXPERIMENTAL EVIDENCE:
    1. Single-stranded DNA STACKS even without a complementary strand
       (bases still pile up on each other)
    2. Poly(dA) has significant stacking even without any H-bonds
    3. DNA analogues with disrupted stacking (but intact H-bonds)
       are much LESS stable than those with intact stacking
    4. Organic molecules that intercalate (insert between base pairs)
       stabilise DNA by ENHANCING stacking, not H-bonding

  CONCLUSION: Stacking is the PRIMARY stabiliser.
  H-bonds provide SPECIFICITY (which base pairs with which).
  Stacking provides STABILITY (the helix holds together).
""")


# ============================================================================
# PART 4: GU DERIVATION — LONDON DISPERSION FROM alpha_EM
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 4: LONDON DISPERSION FROM alpha_EM                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

The dominant contribution to pi-stacking is London dispersion.
This can be estimated from GU parameters.
""")

n_pi_bp = 16           # pi electrons per base pair
alpha_pol_A3 = 15.0    # average static polarisability of a base pair (A^3)
alpha_pol_fm3 = alpha_pol_A3 * (1e5)**3  # convert to fm^3
r_stack_A = 3.4        # stacking distance (A)
r_stack_fm = r_stack_A * 1e5

I_eV = 8.0  # average ionisation energy of nucleobases (eV)
I_MeV = I_eV * 1e-6

E_london_approx = -3.0/4.0 * float(alpha_EM**2) * alpha_pol_A3**2 * I_eV / (r_stack_A**6)

print(f"  Base pair polarisability:  alpha ~ {alpha_pol_A3} A^3")
print(f"  Ionisation energy:         I ~ {I_eV} eV")
print(f"  Stacking distance:         r = {r_stack_A} A")
print()

C6 = 3.0/4.0 * I_eV * alpha_pol_A3**2
E_london_simple = -C6 / r_stack_A**6
print(f"  London formula: E = -C_6 / r^6")
print(f"    C_6 = (3/4) * I * alpha^2 = (3/4) * {I_eV} * {alpha_pol_A3}^2")
print(f"    C_6 = {C6:.1f} eV·A^6")
print(f"    E_London = -{C6:.1f} / {r_stack_A}^6 = {E_london_simple:.3f} eV")
print()

print(f"  This is an ORDER-OF-MAGNITUDE estimate. The actual stacking energy")
print(f"  ({abs(mean_stack):.2f} eV) requires proper quantum chemical treatment")
print(f"  (MP2 or coupled-cluster methods), accounting for:")
print(f"    - Anisotropy of polarisability (not spherical)")
print(f"    - Higher-order multipoles (quadrupole-quadrupole)")
print(f"    - Exchange-correlation at close range")
print(f"    - Electrostatic contribution (permanent dipoles)")
print()

print("""  GU contribution:
    The polarisability alpha scales as a_0^3 ~ (hbar_c / alpha_EM / m_e)^3
    The ionisation energy I scales as alpha_EM^2 * m_e / 2 (Rydberg)
    Therefore: C_6 ~ alpha_EM * a_0^3 (dimensional analysis)
    All traced to m_e (GU-derived) and alpha_EM (experimental input).
""")


# ============================================================================
# PART 5: THE PHASE MEMORY CHANNEL — KEY GU INSIGHT
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 5: THE PHASE MEMORY CHANNEL — KEY GU INSIGHT                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

From 23_MOLECULAR_BONDS (sections 11-12):

  AMPLITUDE MEMORY (rho^4):
    Local, range ~1/m_e ~ 400 fm. Already included in m_e.
    Does NOT contribute additional energy at molecular scales.

  PHASE MEMORY (theta-FF-tilde):
    Nonlocal, range = infinity (mediated by massless photon).
    Active when nabla_theta != 0 (phase gradient in the Omega field).
    Creates a memory channel through modified Maxwell equations:
      partial_mu F^(mu nu) = J^nu + (kappa/2pi^2)(partial_mu theta) F~^(mu nu)

FROM MOLECULAR BONDS:
  - Sigma bonds (w = 0): nabla_theta ~ 0 → NO phase memory
  - Pi bonds (w = 1):    nabla_theta != 0 → PHASE MEMORY ACTIVE
  - H-bonds (w = 0):     NO phase memory

NOW FOR DNA PI-STACKING:

  Each base is an AROMATIC system with pi electrons (w >= 1).
  When two bases stack at 3.4 A, their pi orbitals overlap vertically.

  The VERTICAL pi overlap creates a CONTINUOUS PHASE GRADIENT along
  the helix axis:

    Base pair 1:  theta_1  (aromatic phase, w = 1 per ring)
         |
         | pi-pi overlap → nabla_theta != 0 between layers
         v
    Base pair 2:  theta_2
         |
         | pi-pi overlap → nabla_theta != 0
         v
    Base pair 3:  theta_3
         ...

  This is a CONTINUOUS COLUMN of nabla_theta != 0 — extending from the
  first base pair to the last.
""")

print("""  THE FOUR REGIMES OF theta-FF-tilde (from 21_ELECTROMAGNETISM):

    1. FREE LEPTONS:    theta = const → nabla_theta = 0 → J_theta = 0
                        Standard Maxwell. No phase memory.

    2. HADRONS:         nabla_theta != 0 (confinement) → J_theta != 0
                        Memory binding: -827 MeV in proton.

    3. COSMOLOGY:       theta_dot != 0 → J_theta ~ theta_dot * B
                        Drives baryogenesis.

    4. MOLECULAR PI-STACK (NEW):
                        nabla_theta != 0 (aromatic winding) → J_theta != 0
                        Nonlocal, photon-mediated memory along the stack.

  DNA operates in Regime 4 — the molecular pi-stack regime.
  The theta-FF-tilde coupling is the SAME physics as in hadrons,
  but at molecular scales with weaker fields and gentler gradients.
""")


# ============================================================================
# PART 6: THE MEMORY CHANNEL — QUANTITATIVE STRUCTURE
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 6: MEMORY CHANNEL STRUCTURE                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

The phase memory current in DNA's pi-stack:

  J_theta = (kappa / 2*pi^2) * (nabla_theta x E)

where:
  kappa = topological coupling (integer, from large gauge invariance)
  nabla_theta = phase gradient along the stack (from aromatic winding)
  E = electric field inside the molecular stack

The memory energy density:
  T^00_mem = kappa * K · nabla_theta
  where K is the Chern-Simons current.
""")

rise_A = 3.4    # base pair rise
rise_fm = rise_A * 1e5

n_bp_values = [10, 100, 1000, int(3.2e9)]
labels_bp = ['1 turn (10 bp)', '100 bp', 'virus (1000 bp)', 'human (3.2 billion bp)']

print(f"  MEMORY CHANNEL LENGTH:")
print(f"  {'System':>25s} | {'Base pairs':>12s} | {'Length':>12s} | {'Phase nodes':>12s}")
print("  " + "-" * 70)
for label, n in zip(labels_bp, n_bp_values):
    length_A = n * rise_A
    length_nm = length_A / 10
    length_um = length_nm / 1000
    length_mm = length_um / 1000

    if length_nm < 1000:
        length_str = f"{length_nm:.0f} nm"
    elif length_um < 1000:
        length_str = f"{length_um:.1f} um"
    elif length_mm < 1000:
        length_str = f"{length_mm:.1f} mm"
    else:
        length_str = f"{length_mm/10:.0f} cm"

    print(f"  {label:>25s} | {n:>12,d} | {length_str:>12s} | {n:>12,d}")

print()

print("""  Each base pair is a PHASE NODE in the memory channel.
  The nabla_theta between adjacent nodes is:
    |nabla_theta| ~ 2*pi*w / (N_ring * d_stack)
  where w is the winding number per ring and d_stack = 3.4 A.

  For a purine (w = 2): |nabla_theta| ~ 2*pi*2 / (9 * 3.4 A) ~ 0.41 A^-1
  For a pyrimidine (w = 1): |nabla_theta| ~ 2*pi*1 / (6 * 3.4 A) ~ 0.31 A^-1

  The TOTAL phase accumulated along N base pairs:
    Phi_total = N * delta_theta_per_step
  where delta_theta_per_step depends on the inter-layer pi coupling.
""")


# ============================================================================
# PART 7: WHY THE MEMORY CHANNEL IS THE PRIMARY STABILISER
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 7: WHY THE MEMORY CHANNEL IS THE PRIMARY STABILISER                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

The experimental fact that pi-stacking contributes MORE than H-bonds to
DNA stability acquires deep significance in GU:

  H-BONDS:     sigma (w = 0) → no phase memory → no theta-FF-tilde
  PI-STACKING:  pi (w >= 1) → phase memory → theta-FF-tilde ACTIVE

  The structure that STABILISES the helix is the SAME structure that
  carries NONLOCAL MEMORY.

  This is NOT a coincidence in GU — it is a CONSEQUENCE:
    - Memory (theta-FF-tilde) is a form of BINDING ENERGY
    - In hadrons, theta-FF-tilde provides -827 MeV (negative, binding)
    - In DNA, theta-FF-tilde is the TOPOLOGICAL MECHANISM underlying
      stacking (quantitative contribution still open — see Part 8)
    - Memory and stability are two faces of the SAME coupling

  The pi-stack is simultaneously:
    1. A structural column (holds the helix together)
    2. A memory channel (nonlocal phase information)
    3. An information bus (transmits the base sequence pattern)
""")

print(f"  ENERGY COMPARISON (per base pair step):")
print(f"    Pi-stacking (memory channel):  {abs(mean_stack):.2f} eV  (w >= 1, theta-FF-tilde)")
print(f"    H-bonding (information layer): {(E_hbond_AT+E_hbond_GC)/2:.2f} eV  (w = 0, electrostatic)")
print(f"    Ratio:                         {abs(mean_stack)/((E_hbond_AT+E_hbond_GC)/2):.1f}x")
print()
print(f"  The MEMORY channel dominates the INFORMATION channel by ~2x in energy.")
print()


# ============================================================================
# PART 8: HONEST ASSESSMENT
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 8: HONEST ASSESSMENT — WHAT IS ESTABLISHED VS OPEN                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

ESTABLISHED (standard physics):
  1. Pi-stacking energies are well-measured (0.19-0.61 eV per step)
  2. Pi-stacking exceeds H-bonding in contribution to DNA stability
  3. The physical origin is London dispersion + electrostatics + exchange
  4. All energies trace to m_e and alpha_EM (GU-derived and input)

ESTABLISHED (GU framework):
  5. Pi bonds have winding number w >= 1 (from 23_MOLECULAR_BONDS)
  6. w >= 1 → nabla_theta != 0 → theta-FF-tilde coupling is active
  7. theta-FF-tilde is the SAME mechanism as hadronic memory binding
  8. The pi-stack creates a continuous column of nabla_theta != 0

QUALITATIVE GU ARGUMENT (not yet quantitative):
  9. The theta-FF-tilde energy contribution to stacking
  10. Whether the 0.19-0.61 eV stacking energy INCLUDES a
      phase-memory component, or whether it is purely dispersion
  11. The relationship between stacking sequence-dependence
      and the nabla_theta pattern

OPEN CALCULATIONS NEEDED:
  a. Compute T^00_mem = kappa * K · nabla_theta for the DNA pi-stack
  b. Determine whether this contribution is already captured by
     standard dispersion calculations (which include all EM effects)
     or is a genuinely new term
  c. If new: estimate the magnitude relative to London dispersion
  d. If already included: explain WHY standard dispersion = theta-FF-tilde
     at the molecular level (a reinterpretation, not a new prediction)

THE HONEST POSITION:
  The pi-stack IS the phase memory channel — topologically.
  Whether this produces measurable effects BEYOND standard EM
  dispersion is an open question. The GU interpretation provides
  a new UNDERSTANDING of why stacking stabilises DNA, even if the
  numbers are the same as standard calculations.
""")


# ============================================================================
# SUMMARY
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  SUMMARY: PI-STACKING AND PHASE MEMORY                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

THE CENTRAL INSIGHT:
  DNA's pi-stack is simultaneously:
    - The PRIMARY STABILISER of the double helix (> H-bonds)
    - A CONTINUOUS PHASE MEMORY CHANNEL (theta-FF-tilde, nonlocal)
    - An INFORMATION BUS connecting all base pairs

STACKING ENERGIES:
  Range: 0.19 - 0.61 eV per step (sequence-dependent)
  Mean:  0.39 eV per step
  Dominates H-bonds by factor ~2x in aqueous solution

PHASE MEMORY MECHANISM:
  Each aromatic base has pi electrons with winding w >= 1
  Vertical stacking aligns pi systems → continuous nabla_theta column
  theta-FF-tilde coupling: J_theta = (kappa/2pi^2)(nabla_theta x E)
  Memory channel extends across all N base pairs (N up to ~10^9)

GU REGIME 4:
  Free leptons: theta = const (no memory)
  Hadrons: nabla_theta != 0 (confinement memory)
  Cosmology: theta_dot != 0 (baryogenesis)
  Molecular pi-stack: nabla_theta != 0 (stacking memory) ← DNA IS HERE

CONNECTIONS:
  -> Script 05: How the pi-stack wraps into a double helix (topology)
  -> Script 06: Full energy budget (stacking + H-bonds + entropy)
  -> Script 07: Memory + feedback + fixed point = DNA self-knowledge
""")
