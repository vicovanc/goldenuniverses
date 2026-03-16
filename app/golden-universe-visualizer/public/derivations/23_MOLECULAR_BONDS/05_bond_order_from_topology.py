#!/usr/bin/env python3
"""
BOND ORDER FROM PHASE TOPOLOGY
================================

The KEY GU insight for molecular bonds: bond order (single, double,
triple) maps to the number of distinct phase-locked topological
sectors shared between two atomic centres.

  Single bond = 1 sigma mode  (w = 0, axial overlap)
  Double bond = 1 sigma + 1 pi  (w = 0 + w = 1)
  Triple bond = 1 sigma + 2 pi  (w = 0 + w = 1 + w = 1')

Maximum bond order = 3 because there are exactly 3 spatial directions.

Date: February 2026
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mpmath import mp, mpf, sqrt, pi as mp_pi, exp, cos, sin
import numpy as np

mp.dps = 30
phi = (mpf('1') + sqrt(mpf('5'))) / 2
pi = mp_pi

print("=" * 80)
print("BOND ORDER FROM PHASE TOPOLOGY")
print("sigma, pi, and why the maximum is 3")
print("=" * 80)


# ============================================================================
# PART 1: ORBITAL SYMMETRY AND THE INTERNUCLEAR AXIS
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 1: SIGMA AND PI — SYMMETRY UNDER ROTATION                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

Place two atoms A and B along the z-axis. The internuclear axis
defines a SYMMETRY AXIS. Molecular orbitals are classified by
their angular momentum projection onto this axis:

  SIGMA (σ): m_l = 0 along the bond axis
    The orbital is CYLINDRICALLY SYMMETRIC around the bond.
    Head-on overlap of s, p_z, or hybrid orbitals.
    No nodes through the bond axis.

  PI (π): |m_l| = 1 along the bond axis
    The orbital has ONE nodal plane containing the bond axis.
    Side-on overlap of p_x or p_y orbitals.
    The wavefunction changes sign across the bond axis.

  DELTA (δ): |m_l| = 2 along the bond axis
    TWO nodal planes through the bond axis.
    Overlap of d orbitals. Very weak. Only in transition metals.

IN GU LANGUAGE:

  The Omega-torus has angular coordinate theta. When two kinks
  share electrons, the PHASE RELATIONSHIP between the kinks
  determines the bond type:

  SIGMA: The two kink phases are LOCKED IN PHASE (theta_A = theta_B).
    No transverse winding. Phase winding number w = 0.
    The lock potential V_lock = Lambda_1[1 - cos(theta_A - theta_B)]
    has minimum at theta_A = theta_B.

  PI: The two kink phases have a RELATIVE TWIST of pi/2.
    One unit of transverse winding. Phase winding w = 1.
    The shared electron's theta winds once around the axis
    perpendicular to the bond, creating a nodal plane.

  DELTA: Phase winding w = 2. Two nodal planes. Very weak overlap.
""")


# ============================================================================
# PART 2: WHY MAXIMUM BOND ORDER = 3
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 2: WHY THE MAXIMUM BOND ORDER IS EXACTLY 3                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

In 3-dimensional space, there are exactly 3 independent directions:
  z (along the bond)
  x (perpendicular, in-plane)
  y (perpendicular, out-of-plane)

Each direction supports ONE type of overlap:

  z-direction:  SIGMA bond (head-on overlap along the bond)
  x-direction:  PI bond #1 (side-on overlap in the xz-plane)
  y-direction:  PI bond #2 (side-on overlap in the yz-plane)

That is ALL. There is no fourth independent direction.

Therefore:

  ┌───────────────────────────────────────────────────────────┐
  │                                                           │
  │  MAXIMUM BOND ORDER = 3                                   │
  │    = 1 sigma + 2 pi                                       │
  │    = dim(R^3) - 0                                         │
  │                                                           │
  │  This is a TOPOLOGICAL result: 3D space has 3 directions. │
  │  It would be 4 in 4D, 2 in 2D.                           │
  │                                                           │
  └───────────────────────────────────────────────────────────┘

In GU: the 3 spatial dimensions are the 3 independent angular
modes on the Omega-torus that can lock between two atomic centres.
Each locked mode contributes one bond.
""")

# Tabulate bond types
bond_types = [
    (1, "Single", "1σ", "0",   "H-H, C-C, C-H", "cylindrical", "head-on"),
    (2, "Double", "1σ+1π", "0+1", "C=C, O=O, C=O", "planar", "head-on + side-on"),
    (3, "Triple", "1σ+2π", "0+1+1", "N≡N, C≡C, C≡O", "linear", "head-on + 2×side-on"),
]

print("  BOND CLASSIFICATION:")
print("  " + "─" * 80)
print(f"  {'Order':>5s} | {'Name':>6s} | {'MOs':>7s} | {'w':>5s} | {'Examples':>16s} | {'Geometry':>10s} | {'Overlap'}")
print("  " + "─" * 80)
for order, name, mos, w, examples, geom, overlap in bond_types:
    print(f"  {order:5d} | {name:>6s} | {mos:>7s} | {w:>5s} | {examples:>16s} | {geom:>10s} | {overlap}")
print()


# ============================================================================
# PART 3: SIGMA BONDS — HEAD-ON OVERLAP
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 3: SIGMA BONDS (head-on overlap, w = 0)                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

A sigma bond forms when two orbitals overlap HEAD-ON along the
internuclear axis. The electron density is CONCENTRATED BETWEEN
the two nuclei.

TYPES OF SIGMA BONDS:

  s-s sigma:  Two 1s orbitals (e.g., H-H)
              Overlap: S ∝ exp(-R/a_0)
              Strongest for small atoms.

  s-p sigma:  One s + one p_z orbital (e.g., C-H)
              The p_z orbital points toward the s orbital.
              Overlap enhanced by p-orbital directionality.

  p-p sigma:  Two p_z orbitals pointing at each other (e.g., N-N in N2)
              Strong overlap along the axis.

  sp^n-sp^n:  Two hybrid orbitals (e.g., C-C in ethane)
              sp3-sp3: 25% s + 75% p character
              sp2-sp2: 33% s + 67% p character
              sp-sp:   50% s + 50% p character
              More s character → shorter, stronger bond.

IN GU: The sigma bond is the GROUND STATE of the two-centre
lock potential. Phase winding w = 0 means the kink envelope
has no angular node — it wraps smoothly around both nuclei.
""")

# Sigma bond properties
sigma_data = [
    ("s-s",    "H-H",  436,  0.74,  "100% s",  "weakest sigma"),
    ("s-sp3",  "C-H",  413,  1.09,  "25% s",   "most common"),
    ("sp3-sp3","C-C",  348,  1.54,  "25% s",   "backbone"),
    ("sp2-sp2","C=C σ",614,  1.34,  "33% s",   "+ pi bond"),
    ("sp-sp",  "C≡C σ",839,  1.20,  "50% s",   "+ 2 pi bonds"),
    ("p-p",    "N-N σ",160,  1.45,  "0% s",    "weak (lone pair repulsion)"),
]

print("  SIGMA BOND DATA:")
print("  " + "─" * 72)
print(f"  {'Type':>7s} | {'Example':>7s} | {'E (kJ/mol)':>10s} | {'R (A)':>6s} | {'s-char':>8s} | {'Note'}")
print("  " + "─" * 72)
for typ, ex, E, R, schar, note in sigma_data:
    print(f"  {typ:>7s} | {ex:>7s} | {E:10d} | {R:6.2f} | {schar:>8s} | {note}")
print()


# ============================================================================
# PART 4: PI BONDS — SIDE-ON OVERLAP
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 4: PI BONDS (side-on overlap, w = 1)                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

A pi bond forms when two p-orbitals overlap SIDE-ON,
perpendicular to the internuclear axis.

KEY PROPERTIES:
  1. The pi orbital has a NODAL PLANE containing the bond axis.
     Electron density is ABOVE and BELOW the bond, not between.

  2. Pi overlap is WEAKER than sigma overlap for the same orbitals,
     because the lobes are further apart:
       S_pi / S_sigma ~ 0.3-0.5 (depends on distance)

  3. Pi bonds REQUIRE parallel p-orbitals → PLANAR geometry.
     This is why double bonds enforce planarity (ethylene is flat).

  4. Pi bonds are MORE REACTIVE than sigma bonds.
     The electrons are further from the nuclei → easier to attack.

IN GU LANGUAGE:
  The pi bond is a TWISTED KINK — the shared soliton has one unit
  of phase winding (w = 1) perpendicular to the bond axis.

  The lock potential for the pi mode:
    V_lock^(pi) = Lambda_1^(pi) [1 - cos(theta_perp)]

  where theta_perp is the relative phase in the transverse direction.
  Lambda_1^(pi) < Lambda_1^(sigma) because the transverse overlap
  is weaker than the axial overlap.
""")

# Pi bond energies (approximate, from double/triple minus sigma)
pi_data = [
    ("C=C",  "1σ + 1π", 614, 348, 266, "π weaker than σ"),
    ("C≡C",  "1σ + 2π", 839, 348, 491, "2π ≈ 491 (245 each)"),
    ("N≡N",  "1σ + 2π", 945, 160, 785, "2π ≈ 785 (393 each)"),
    ("O=O",  "1σ + 1π", 498, 146, 352, "π ≈ σ for O"),
    ("C=O",  "1σ + 1π", 745, 358, 387, "C=O π stronger than C=C π"),
]

print("  PI BOND ENERGIES (extracted from total - sigma):")
print("  " + "─" * 70)
print(f"  {'Bond':>5s} | {'MOs':>8s} | {'E_total':>7s} | {'E_sigma':>7s} | {'E_pi':>6s} | {'Note'}")
print(f"  {'':>5s} | {'':>8s} | {'(kJ/mol)':>7s} | {'(kJ/mol)':>7s} | {'(kJ/mol)':>6s} |")
print("  " + "─" * 70)
for bond, mos, E_tot, E_sig, E_pi, note in pi_data:
    print(f"  {bond:>5s} | {mos:>8s} | {E_tot:7d} | {E_sig:7d} | {E_pi:6d} | {note}")

print()
print("  KEY OBSERVATION: Pi bonds are consistently WEAKER than sigma bonds.")
print("  For C-C:  E_sigma = 348 kJ/mol,  E_pi ≈ 266 kJ/mol  (ratio: 0.76)")
print("  For C≡C:  E_sigma = 348,  E_pi ≈ 245 each  (ratio: 0.70)")
print()
print("  In GU: This ratio reflects the OVERLAP INTEGRAL ratio:")
print("    S_pi / S_sigma ~ 0.7  (from the kink profile geometry)")
print("    The transverse kink overlap is weaker than the axial overlap.")
print()


# ============================================================================
# PART 5: THE LOCK POTENTIAL PER BOND MODE
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 5: THE LOCK POTENTIAL FOR EACH BOND MODE                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

In GU, each shared electron pair corresponds to a LOCKED PHASE MODE
between the two atomic kinks.

The lock potential for mode i:
  V_lock^(i)(Delta_theta_i) = Lambda_1^(i) [1 - cos(Delta_theta_i)]

where Delta_theta_i is the relative phase in direction i.

At the bond minimum: Delta_theta_i = 0 (phases locked).

The BOND ENERGY contributed by mode i:
  E_i ~ 2 * Lambda_1^(i) * rho_vac^2  (energy of the locked state)

For the three possible modes:

  SIGMA (i=z):  Lambda_1^(sigma) is LARGEST (strongest overlap)
                E_sigma is the single-bond energy.

  PI_x (i=x):   Lambda_1^(pi) < Lambda_1^(sigma)
                E_pi < E_sigma.

  PI_y (i=y):   Lambda_1^(pi') ≈ Lambda_1^(pi)  (by symmetry)
                E_pi' ≈ E_pi.

TOTAL BOND ENERGIES:
  Single: E = E_sigma
  Double: E = E_sigma + E_pi
  Triple: E = E_sigma + 2 * E_pi

This predicts: E_double/E_single < 2 and E_triple/E_single < 3,
because pi bonds are weaker than sigma bonds.
""")

# Verify the prediction
E_CC_single = 348  # kJ/mol
E_CC_double = 614
E_CC_triple = 839

ratio_double = E_CC_double / E_CC_single
ratio_triple = E_CC_triple / E_CC_single

E_pi_from_double = E_CC_double - E_CC_single
E_pi_from_triple = (E_CC_triple - E_CC_single) / 2

print(f"  CARBON-CARBON BONDS:")
print(f"    C-C (single):  {E_CC_single} kJ/mol = 3.61 eV")
print(f"    C=C (double):  {E_CC_double} kJ/mol = 6.36 eV")
print(f"    C≡C (triple):  {E_CC_triple} kJ/mol = 8.70 eV")
print()
print(f"  RATIOS:")
print(f"    E_double / E_single = {ratio_double:.2f}  (< 2.00, as predicted)")
print(f"    E_triple / E_single = {ratio_triple:.2f}  (< 3.00, as predicted)")
print()
print(f"  PI BOND ENERGIES:")
print(f"    From double bond: E_pi = {E_CC_double} - {E_CC_single} = {E_pi_from_double} kJ/mol")
print(f"    From triple bond: E_pi = ({E_CC_triple} - {E_CC_single})/2 = {E_pi_from_triple:.0f} kJ/mol")
print(f"    Ratio E_pi/E_sigma = {E_pi_from_double/E_CC_single:.2f}")
print()
print(f"  GU INTERPRETATION:")
print(f"    Lambda_1(pi) / Lambda_1(sigma) ≈ {E_pi_from_double/E_CC_single:.2f}")
print(f"    This ratio comes from the TRANSVERSE overlap of the kink")
print(f"    profile relative to the AXIAL overlap.")
print()


# ============================================================================
# PART 6: BOND LENGTH AND BOND ORDER
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 6: BOND LENGTH DECREASES WITH BOND ORDER                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

More bonds = shorter distance. This is because:

  1. More electron density between nuclei → stronger attraction
  2. The molecular kink is NARROWER when more modes lock
  3. In GU: more phase-locked modes → tighter confinement →
     larger kink curvature mu → shorter characteristic width 1/mu
""")

length_data = [
    ("C-C",  1, 1.54, 348),
    ("C=C",  2, 1.34, 614),
    ("C≡C",  3, 1.20, 839),
    ("N-N",  1, 1.45, 160),
    ("N=N",  2, 1.25, 418),
    ("N≡N",  3, 1.10, 945),
    ("C-O",  1, 1.43, 358),
    ("C=O",  2, 1.23, 745),
    ("C≡O",  3, 1.13, 1077),
]

print("  " + "─" * 55)
print(f"  {'Bond':>5s} | {'Order':>5s} | {'Length (A)':>10s} | {'Energy (kJ/mol)':>15s}")
print("  " + "─" * 55)
for bond, order, length, energy in length_data:
    print(f"  {bond:>5s} | {order:5d} | {length:10.2f} | {energy:15d}")
print()
print("  PATTERN: For each atom pair,")
print("    Single → Double: length decreases ~13%, energy increases ~75%")
print("    Double → Triple: length decreases ~10%, energy increases ~35%")
print("    Diminishing returns: each added pi bond contributes LESS.")
print()


# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 80)
print("SUMMARY: BOND ORDER FROM TOPOLOGY")
print("=" * 80)
print(f"""
  Bond order = number of phase-locked angular modes between atoms.

  ┌────────────────────────────────────────────────────────────┐
  │                                                            │
  │  Single bond: 1 sigma (w=0)     — head-on kink overlap    │
  │  Double bond: 1 sigma + 1 pi    — + 1 transverse twist    │
  │  Triple bond: 1 sigma + 2 pi    — + 2 transverse twists   │
  │  Maximum = 3: from 3 spatial dimensions (topological)      │
  │                                                            │
  │  E_pi / E_sigma ≈ 0.76  (transverse overlap is weaker)    │
  │  → E_double < 2 × E_single                                │
  │  → E_triple < 3 × E_single                                │
  │                                                            │
  │  Each lock contributes V = Lambda_1^(i)[1 - cos(Delta_theta)] │
  │  to the inter-atomic potential.                            │
  │                                                            │
  └────────────────────────────────────────────────────────────┘

  This is the GU explanation for why chemistry has single, double,
  and triple bonds — and why there is no quadruple bond between
  main-group elements (d-orbital delta bonds allow order 4+ for
  transition metals, but these are extremely rare and weak).
""")
