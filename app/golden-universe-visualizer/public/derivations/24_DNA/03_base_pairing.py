#!/usr/bin/env python3
"""
WATSON-CRICK BASE PAIRING FROM GU
=====================================

Why adenine pairs with thymine and guanine pairs with cytosine.
Geometric complementarity (purine + pyrimidine = constant width)
plus hydrogen bond donor/acceptor pattern specificity.

The base pair is the fundamental information unit of DNA.
In GU, each base pair merges two aromatic pi systems into a single
coplanar phase topology — the building block of the phase memory column.

Upstream: 01_nucleotide_bases.py, 02_hydrogen_bonds.py
Status:   Standard biochemistry with GU topological interpretation

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

print("=" * 80)
print("WATSON-CRICK BASE PAIRING FROM GU")
print("Why A pairs with T, and G pairs with C")
print("=" * 80)


# ============================================================================
# PART 1: THE GEOMETRIC CONSTRAINT — CONSTANT WIDTH
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 1: GEOMETRIC CONSTRAINT — PURINE + PYRIMIDINE = CONSTANT WIDTH       ║
╚══════════════════════════════════════════════════════════════════════════════╝

The DNA double helix has a CONSTANT DIAMETER of ~20 Angstrom.
This requires that every base pair has the SAME WIDTH across the helix.

  If purine paired with purine:   too wide  (~12 A)
  If pyrimidine paired with pyrimidine: too narrow (~8 A)
  Purine + pyrimidine:           just right (~10.85 A)

This geometric constraint is TOPOLOGY-INDEPENDENT — it follows from
the physical sizes of the molecules (set by a_0 = hbar_c/(alpha_EM * m_e)).
""")

d_C1_C1 = 10.85  # C1'-C1' distance in Angstrom (standard B-DNA)
purine_width = 5.4  # approximate purine extent from glycosidic bond
pyrimidine_width = 3.4

print(f"  Standard B-DNA C1'-C1' distance: {d_C1_C1:.2f} A")
print(f"  In Bohr radii:                   {d_C1_C1/a_0_A:.1f} a_0")
print()
print(f"  Purine extent:    ~{purine_width:.1f} A = {purine_width/a_0_A:.1f} a_0")
print(f"  Pyrimidine extent: ~{pyrimidine_width:.1f} A = {pyrimidine_width/a_0_A:.1f} a_0")
print(f"  Combined:          ~{purine_width + pyrimidine_width + 2.0:.1f} A (+ H-bond gap ~2.0 A)")
print()

print("""  RULE 1: Every base pair must be PURINE + PYRIMIDINE.
  This eliminates A-A, A-G, G-G, T-T, T-C, C-C pairings.
  Remaining possibilities: A-T, A-C, G-T, G-C (and reverses).
""")


# ============================================================================
# PART 2: H-BOND DONOR/ACCEPTOR COMPLEMENTARITY
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 2: H-BOND DONOR/ACCEPTOR COMPLEMENTARITY                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

Each base has a specific pattern of hydrogen bond DONORS (D, gives H)
and ACCEPTORS (A, receives H) along its Watson-Crick edge.

For proper pairing, every donor on one base must face an acceptor
on the partner, and vice versa.
""")

print("""  H-BOND PATTERNS (reading from major groove side):

    ADENINE:    A — D — A
      Position 1 (N1):    Acceptor (lone pair)
      Position 6 (N6-H):  Donor    (amino NH₂)
      Position 7 (N7):    Acceptor (lone pair)

    THYMINE:    D — A — D
      Position 3 (N3-H):  Donor    (N-H)
      Position 4 (O4):    Acceptor (C=O lone pair)
      Position 2 (O2):    Donor-adjacent

    A-T pairing:  A-D-A  matched with  D-A-D  → COMPLEMENTARY (2 H-bonds)

    GUANINE:    A — D — D — A
      Position 6 (O6):    Acceptor (C=O)
      Position 1 (N1-H):  Donor    (N-H)
      Position 2 (N2-H):  Donor    (amino NH₂)

    CYTOSINE:   D — A — A — D
      Position 4 (N4-H):  Donor    (amino NH₂)
      Position 3 (N3):    Acceptor (lone pair)
      Position 2 (O2):    Acceptor (C=O)

    G-C pairing: A-D-D-A  matched with  D-A-A-D → COMPLEMENTARY (3 H-bonds)
""")

print("""  MISMATCHES:

    A-C: A(A-D-A) vs C(D-A-A-D) → donor-donor clash at position 2
    G-T: G(A-D-D-A) vs T(D-A-D) → steric/electronic mismatch
    These mismatches are energetically unfavourable by ~0.1-0.3 eV.

  RULE 2: Only A-T and G-C have fully complementary donor/acceptor patterns.
""")


# ============================================================================
# PART 3: BASE PAIR ENERGETICS
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 3: BASE PAIR ENERGETICS                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

E_AT_hbond = 0.34  # eV, 2 H-bonds
E_GC_hbond = 0.55  # eV, 3 H-bonds

E_AT_gas = 0.59    # eV, gas-phase total (includes dispersion, polarisation)
E_GC_gas = 1.13    # eV, gas-phase total

E_AT_aq = 0.13     # eV, aqueous solution (screened by water)
E_GC_aq = 0.22     # eV, aqueous solution

print(f"  {'':>15s} | {'A-T':>10s} | {'G-C':>10s} | {'Ratio G-C/A-T':>14s}")
print("  " + "-" * 58)
print(f"  {'H-bonds only':>15s} | {E_AT_hbond:>8.2f} eV | {E_GC_hbond:>8.2f} eV | {E_GC_hbond/E_AT_hbond:>14.2f}")
print(f"  {'Gas phase':>15s} | {E_AT_gas:>8.2f} eV | {E_GC_gas:>8.2f} eV | {E_GC_gas/E_AT_gas:>14.2f}")
print(f"  {'Aqueous':>15s} | {E_AT_aq:>8.2f} eV | {E_GC_aq:>8.2f} eV | {E_GC_aq/E_AT_aq:>14.2f}")
print()

print("""  Notes:
    - Gas phase: full interaction (H-bonds + dispersion + polarisation)
    - Aqueous: water competes for H-bond sites, screening by factor ~4
    - In DNA: the base pairs are STACKED and SHIELDED from water,
      so the effective energy is between gas-phase and aqueous values
    - Pi-stacking contributes ADDITIONAL energy (Script 04)
""")


# ============================================================================
# PART 4: TAUTOMERIC SPECIFICITY — LOCK POTENTIAL
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 4: TAUTOMERIC SPECIFICITY — THE LOCK POTENTIAL                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

Each base can exist in multiple TAUTOMERIC forms — the protons can be
on different nitrogen or oxygen atoms. Only the CANONICAL tautomer
gives correct Watson-Crick pairing.

  Example: Cytosine
    Amino form (canonical):  NH₂ group is a DONOR  → pairs with G
    Imino form (rare):       N-H shifts, pattern changes → mispairs with A

  Tautomer populations at equilibrium:
    Canonical form: > 99.99%  (favoured by ~0.5-1.0 eV)
    Rare tautomers: < 0.01%
""")

dE_tautomer = 0.7  # eV, typical energy difference
K_eq = np.exp(-dE_tautomer / (8.617e-5 * 310.15))  # Boltzmann at body temp
error_rate = K_eq / (1 + K_eq)

print(f"  Tautomeric energy gap:       Delta_E ~ {dE_tautomer:.1f} eV")
print(f"  At body temperature (310 K): K_eq = exp(-Delta_E/k_BT)")
print(f"                               K_eq ~ {K_eq:.2e}")
print(f"  Mispairing rate:             ~ {error_rate:.2e}")
print()

print("""  GU INTERPRETATION:

    The lock potential V_lock = Lambda_1[1 - cos(theta)] pins the
    Omega-field phase at each atomic site. The CANONICAL tautomer
    corresponds to the GLOBAL MINIMUM of V_lock for the base.

    Rare tautomers are LOCAL MINIMA at higher energy — they require
    a proton to hop over the lock-potential barrier:

      V_barrier ~ Lambda_1 ~ 0.5-1.0 eV (molecular scale)

    The tautomeric equilibrium is controlled by the SAME lock potential
    that determines aromatic stability (Script 01).

    The extraordinarily LOW error rate (10^-10 per base pair per
    replication, with proofreading enzymes) means that DNA's
    information storage is protected by the lock potential.

    In GU: the lock potential is not just about individual bonds —
    it is the mechanism that PRESERVES INFORMATION in the phase topology.
""")


# ============================================================================
# PART 5: THE BASE PAIR AS A PHASE TOPOLOGY UNIT
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 5: THE BASE PAIR AS A PHASE TOPOLOGY UNIT                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

When A pairs with T (or G with C), the two aromatic systems become
COPLANAR. Their pi systems, while not fully conjugated across the
H-bonds, are brought into close proximity:

  Base separation across H-bonds: ~2.8-3.0 A
  Pi orbital extent above/below plane: ~1.7 A each
  => pi clouds are ~0.6-1.2 A apart across the pair
""")

base_sep = 2.9  # A, across H-bonds
pi_extent = 1.7  # A, above/below base plane
pi_gap = base_sep - 2 * pi_extent  # gap between pi clouds

print(f"  Inter-base distance (H-bond): {base_sep:.1f} A")
print(f"  Pi cloud extent:              {pi_extent:.1f} A per base")
print(f"  Pi cloud gap:                 {max(0, pi_gap):.1f} A")
print()

print("""  Although the pi clouds DO NOT overlap strongly across the H-bonds
  (the gap is too large for significant conjugation), the base pair
  as a whole presents a SINGLE PLANAR UNIT for stacking:

    Top view:       [  purine  ] --- H-bonds --- [ pyrimidine ]
                    [  w = 2    ]                [  w = 1      ]

    The combined phase topology of the base pair:
      Total pi electrons: 10 + 6 = 16 (A-T) or 10 + 6 = 16 (G-C)
      But NOT a single 16-electron aromatic system (no ring closure)
      Instead: two independent aromatic units held coplanar by H-bonds

  FOR STACKING (Script 04):
    What matters is that the base pair presents a FLAT, POLARISABLE
    surface of ~100 A^2 area. When two base pairs stack:
      - Pi orbitals from adjacent pairs overlap VERTICALLY
      - This DOES create conjugation between layers
      - This is where the phase memory channel forms
""")

area_AT = 60 + 40  # approximate area in A^2 (purine + pyrimidine)
print(f"  Approximate base pair area:   ~{area_AT} A^2")
print(f"  In units of a_0^2:            ~{area_AT / a_0_A**2:.0f} a_0^2")
print()


# ============================================================================
# PART 6: INFORMATION CONTENT
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 6: INFORMATION CONTENT OF BASE PAIRING                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

Watson-Crick pairing creates a binary choice at each position:
  A-T  or  G-C  (and their reverses: T-A, C-G)

Each base pair stores approximately:
  I = log_2(4) = 2 bits  (4 possibilities: A-T, T-A, G-C, C-G)
  Or equivalently: 1 bit for identity (A-T vs G-C)
                 + 1 bit for orientation (which strand)
""")

n_pairs_4 = [4, 1e3, 1e6, 3.2e9]
labels = ['1 base pair', 'virus (~1000 bp)', 'bacterium (~10^6 bp)',
          'human (~3.2×10^9 bp)']

print(f"  {'System':>25s} | {'Base pairs':>12s} | {'Bits':>12s} | {'Bytes':>12s}")
print("  " + "-" * 70)
for label, n in zip(labels, n_pairs_4):
    bits = 2 * n
    bytes_val = bits / 8
    if bytes_val < 1e3:
        bytes_str = f"{bytes_val:.0f} B"
    elif bytes_val < 1e6:
        bytes_str = f"{bytes_val/1e3:.0f} KB"
    elif bytes_val < 1e9:
        bytes_str = f"{bytes_val/1e6:.0f} MB"
    else:
        bytes_str = f"{bytes_val/1e9:.1f} GB"

    if bits < 1e3:
        bits_str = f"{bits:.0f}"
    else:
        bits_str = f"{bits:.2e}"

    print(f"  {label:>25s} | {n:>12.2e} | {bits_str:>12s} | {bytes_str:>12s}")

print()

print("""  GU INTERPRETATION:

    Each base pair is a TOPOLOGICAL CHOICE:
      A-T: purine(w=2) + pyrimidine(w=1), 2 H-bonds (weak coupling)
      G-C: purine(w=2) + pyrimidine(w=1), 3 H-bonds (strong coupling)

    The base pair identity is stored in the H-BOND PATTERN
    (donor/acceptor arrangement), while the pi topology is the SAME
    for both (purine + pyrimidine coplanar).

    This means DNA stores information in the ELECTROSTATIC layer
    (H-bonds, w=0) while transmitting memory through the TOPOLOGICAL
    layer (pi stacking, w >= 1). Information and memory use
    DIFFERENT physical channels — a form of multiplexing.

    Information:  H-bond pattern  (electrostatic, sigma, w = 0)
    Memory:       Pi-stack column (topological, pi, w >= 1)
""")


# ============================================================================
# SUMMARY
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  SUMMARY: WATSON-CRICK BASE PAIRING FROM GU                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

WHAT DETERMINES BASE PAIRING:
  1. GEOMETRY: purine + pyrimidine = constant width (from a_0)
  2. COMPLEMENTARITY: donor/acceptor patterns must match
  3. TAUTOMERIC STABILITY: lock potential pins canonical forms
  4. RESULT: only A-T and G-C satisfy all three constraints

GU INSIGHTS:
  5. Geometric constraint from molecular size (set by m_e, alpha_EM)
  6. Lock potential V_lock pins tautomeric forms → information fidelity
  7. Base pair = purine(w=2) + pyrimidine(w=1) coplanar → flat stacking unit
  8. Information stored in H-bond pattern (sigma, w=0)
  9. Memory transmitted through pi-stack (pi, w>=1) — DIFFERENT CHANNEL

ENERGETICS:
  A-T:  0.34 eV (H-bonds), 0.59 eV (gas phase), ~0.13 eV (aqueous)
  G-C:  0.55 eV (H-bonds), 1.13 eV (gas phase), ~0.22 eV (aqueous)

CONNECTIONS:
  -> Script 04: How base pairs STACK to create the phase memory column
  -> Script 05: How stacking + pairing creates the double helix
  -> Script 07: Information + memory = DNA self-knowledge
""")
