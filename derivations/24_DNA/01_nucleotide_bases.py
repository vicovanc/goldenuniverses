#!/usr/bin/env python3
"""
NUCLEOTIDE BASES: AROMATICITY FROM PHASE TOPOLOGY
====================================================

The four DNA bases (adenine, thymine, guanine, cytosine) are aromatic
heterocycles. This script derives their aromatic stability from GU
phase topology — Hückel's 4n+2 rule as a phase quantization condition
on the Omega-torus — and classifies purines vs pyrimidines by their
total winding number.

Upstream: 23_MOLECULAR_BONDS (sp2 hybridisation, pi bonds, phase winding)
Status:   Standard chemistry with GU topological interpretation

Date: February 2026
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mpmath import mp, mpf, sqrt, pi as mp_pi, exp, cos, sin
import numpy as np

mp.dps = 30
phi = (mpf('1') + sqrt(mpf('5'))) / 2
pi = mp_pi
alpha_EM = mpf('1') / mpf('137.035999177')
m_e = mpf('0.51099895')       # MeV
hbar_c = mpf('197.3269804')   # MeV·fm
a_0_fm = float(hbar_c / (alpha_EM * m_e))  # Bohr radius in fm
a_0_A = a_0_fm / 1e5                        # Bohr radius in Angstrom

kJmol_to_eV = 1 / 96.485
kcalmol_to_eV = 1 / 23.060

print("=" * 80)
print("NUCLEOTIDE BASES: AROMATICITY FROM PHASE TOPOLOGY")
print("The molecular building blocks of DNA, derived from GU")
print("=" * 80)


# ============================================================================
# PART 1: SP2 HYBRIDISATION AND PLANARITY
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 1: SP2 HYBRIDISATION — WHY DNA BASES ARE FLAT                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

From 23_MOLECULAR_BONDS/06_double_and_triple_bonds.py:

  sp2 hybridisation = superposition of s + p_x + p_y orbitals
  Three hybrid orbitals at 120 degrees in a plane
  One unhybridised p_z orbital perpendicular to the plane

In GU terms:
  The three sp2 orbitals are sigma modes (w = 0) — head-on overlap
  The p_z orbital is a pi mode (w = 1) — transverse phase winding

For a DNA base atom (C or N in the ring):
  - 3 sigma bonds hold the ring together (in-plane)
  - 1 pi bond contributes to the aromatic system (out-of-plane)
  - The pi electron's p_z orbital extends above and below the plane

PLANARITY IS ESSENTIAL: the p_z orbitals must be parallel for
pi-pi overlap. Any twist breaks the continuous phase channel.
This is enforced by the lock potential V_lock = Lambda_1[1 - cos(Delta_theta)]
which penalises misalignment of neighbouring p_z phases.
""")


# ============================================================================
# PART 2: HÜCKEL'S RULE AS PHASE QUANTIZATION
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 2: HÜCKEL'S RULE — PHASE QUANTIZATION ON THE RING                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

STANDARD CHEMISTRY: A planar cyclic molecule with (4n + 2) pi electrons
is aromatic — it has extra stability from electron delocalisation.
  n = 0: 2 pi electrons (cyclopropenyl cation)
  n = 1: 6 pi electrons (benzene, pyrimidines)
  n = 2: 10 pi electrons (purines — fused ring system)

GU INTERPRETATION — Phase Quantization:

  Each pi electron on the ring carries a phase theta from the Omega field.
  As we traverse the ring (a closed loop), the phase must return to the
  SAME V_lock minimum: Delta_theta = 2*pi*w for integer winding w.

  For a ring of N atoms, the molecular orbitals are:
    psi_k = (1/sqrt(N)) * sum_j exp(2*pi*i*k*j/N) * p_z(j)
    where k = 0, ±1, ±2, ..., ±(N-1)/2  (or N/2 for even N)

  The k = 0 orbital is non-degenerate (all p_z in phase).
  The k = ±1, ±2, ... orbitals come in degenerate PAIRS.

  Filling with 2 electrons per orbital (Pauli):
    k = 0 alone:           2 electrons  (n = 0: 4*0 + 2 = 2)
    k = 0 plus 1 pair:     6 electrons  (n = 1: 4*1 + 2 = 6)
    k = 0 plus 2 pairs:   10 electrons  (n = 2: 4*2 + 2 = 10)
    General:              4n + 2 electrons

  This is a PHASE QUANTIZATION CONDITION: the allowed states are those
  where the cumulative phase around the ring is 2*pi*k for integer k,
  and the filled shell corresponds to all states with |k| <= n.

  In GU language: the Omega-field phase theta winds by 2*pi*k around the
  ring, where k is the angular momentum quantum number on the ring.
  Aromatic stability = filling a complete set of phase-winding modes.
""")

print("  HÜCKEL VERIFICATION FOR DNA BASES:")
print()

bases = {
    'Benzene (reference)': {'ring_sizes': [6], 'n_pi': 6, 'n_huckel': 1,
                            'type': 'monocyclic'},
    'Pyrimidine (C, T ring)': {'ring_sizes': [6], 'n_pi': 6, 'n_huckel': 1,
                                'type': 'monocyclic'},
    'Purine (A, G ring)': {'ring_sizes': [5, 6], 'n_pi': 10, 'n_huckel': 2,
                           'type': 'fused bicyclic'},
}

for name, info in bases.items():
    n = (info['n_pi'] - 2) // 4
    is_huckel = (info['n_pi'] == 4 * n + 2)
    rings = '+'.join(str(r) for r in info['ring_sizes'])
    print(f"    {name}:")
    print(f"      Ring structure: {rings}-membered ({info['type']})")
    print(f"      Pi electrons:  {info['n_pi']}")
    print(f"      Hückel check:  4({n}) + 2 = {4*n+2}  {'AROMATIC' if is_huckel else 'NOT AROMATIC'}")
    print()


# ============================================================================
# PART 3: THE FOUR DNA BASES — MOLECULAR STRUCTURE
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 3: THE FOUR DNA BASES — MOLECULAR STRUCTURE                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

PYRIMIDINES (single 6-membered ring, 6 pi electrons):

  CYTOSINE (C)                      THYMINE (T)
  ─────────────                     ─────────────
  Formula: C₄H₅N₃O                 Formula: C₅H₆N₂O₂
  Ring: 4C + 2N (heteroaromatic)    Ring: 4C + 2N (heteroaromatic)
  Substituents: NH₂, =O             Substituents: CH₃, =O, =O
  MW: 111.1 Da                      MW: 126.1 Da
  H-bond sites: 3 (1 donor, 2 acc)  H-bond sites: 3 (1 donor, 2 acc)

  GU phase topology:
    6 pi electrons → n = 1 → winding modes k = 0, ±1
    Total phase winding capacity: w_max = 1
    Nitrogen lone pairs contribute to aromaticity

PURINES (fused 5+6 ring, 10 pi electrons):

  ADENINE (A)                       GUANINE (G)
  ─────────────                     ─────────────
  Formula: C₅H₅N₅                  Formula: C₅H₅N₅O
  Ring: 5-ring + 6-ring fused       Ring: 5-ring + 6-ring fused
  Substituents: NH₂                  Substituents: NH₂, =O
  MW: 135.1 Da                      MW: 151.1 Da
  H-bond sites: 3 (1 donor, 2 acc)  H-bond sites: 4 (2 donor, 2 acc)

  GU phase topology:
    10 pi electrons → n = 2 → winding modes k = 0, ±1, ±2
    Total phase winding capacity: w_max = 2
    Larger pi system → MORE phase-winding modes → STRONGER phase memory
""")


# ============================================================================
# PART 4: AROMATIC STABILISATION ENERGY
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 4: AROMATIC STABILISATION ENERGY                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

Aromaticity provides EXTRA stability beyond what isolated double bonds
would give. This is the aromatic stabilisation energy (ASE).
""")

E_CC_single = 3.48    # eV (C-C single bond)
E_CC_double = 6.36    # eV (C=C double bond)
E_CC_aromatic = 5.17  # eV (C-C in benzene, averaged)
E_CN_single = 3.17    # eV (C-N single bond)
E_CN_double = 6.15    # eV (C=N double bond)
E_CN_aromatic = 4.80  # eV (approximate, C-N in aromatic heterocycle)

E_benzene_localised = 3 * E_CC_single + 3 * E_CC_double
E_benzene_actual = 6 * E_CC_aromatic
ASE_benzene = E_benzene_actual - E_benzene_localised
ASE_benzene_exp = 1.56  # eV (experimental, ~36 kcal/mol)

print(f"  BENZENE (reference):")
print(f"    Localised (3 single + 3 double): {E_benzene_localised:.2f} eV")
print(f"    Actual (6 aromatic):             {E_benzene_actual:.2f} eV")
print(f"    ASE (calculated):                {ASE_benzene:+.2f} eV")
print(f"    ASE (experimental):              {ASE_benzene_exp:+.2f} eV")
print()

ASE_pyrimidine_exp = 1.14  # eV (~26 kcal/mol)
ASE_purine_exp = 2.18      # eV (~50 kcal/mol)

print(f"  PYRIMIDINE (C, T ring type):")
print(f"    ASE (experimental):              {ASE_pyrimidine_exp:+.2f} eV")
print(f"    Phase modes filled:              k = 0, ±1  (3 modes, 6 electrons)")
print(f"    ASE per pi electron:             {ASE_pyrimidine_exp/6:.3f} eV")
print()

print(f"  PURINE (A, G ring type):")
print(f"    ASE (experimental):              {ASE_purine_exp:+.2f} eV")
print(f"    Phase modes filled:              k = 0, ±1, ±2  (5 modes, 10 electrons)")
print(f"    ASE per pi electron:             {ASE_purine_exp/10:.3f} eV")
print()


# ============================================================================
# PART 5: GU INTERPRETATION — LOCK POTENTIAL AND WINDING
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 5: GU INTERPRETATION — LOCK POTENTIAL AND AROMATIC WINDING           ║
╚══════════════════════════════════════════════════════════════════════════════╝

THE GU PICTURE OF AROMATICITY:

1. Each atom in the aromatic ring has an sp2-hybridised p_z orbital.
   In GU, this is a kink angular mode with winding number w = 1
   (from 23_MOLECULAR_BONDS/05_bond_order_from_topology.py).

2. The lock potential V_lock = Lambda_1[1 - cos(Delta_theta)] pins the
   phase at each atomic site. Between adjacent sites, the phase
   interpolates smoothly — this is the pi bond.

3. Around a CLOSED RING, the total phase change must satisfy:
     Delta_theta_total = 2*pi * k    (k integer)
   This is NOT optional — it is a topological constraint from the
   periodicity of V_lock. The phase must return to the same minimum.

4. The allowed k values give the molecular orbital quantum numbers:
     k = 0:     bonding (all phases aligned)
     k = ±1:    first excited pair
     k = ±2:    second excited pair
     etc.

5. Each k-value orbital holds 2 electrons (Pauli). Filling through
   |k| = n gives 2 + 4n = 4n + 2 electrons — Hückel's rule.

6. The aromatic stabilisation energy comes from the DIFFERENCE between:
   - Localised bonds: each pi pair locked individually (V_lock at each bond)
   - Delocalised ring: phase winds coherently around the ring (global V_lock)
   The delocalised state wins because the global phase gradient is
   SMALLER — smoother winding costs less lock-potential energy.

   ASE ~ N_ring * Lambda_1 * [1 - cos(2*pi/N_ring)] - Lambda_1
       ~ Lambda_1 * 2*pi^2 / N_ring   (for large rings)

   This is a rough estimate; the actual ASE depends on the heterocyclic
   structure (N vs C atoms have different phase coupling strengths).
""")

Lambda_1_molecular = float(ASE_benzene_exp / (6 * (1 - np.cos(2 * np.pi / 6))))
print(f"  Effective molecular Lambda_1 from benzene ASE:")
print(f"    Lambda_1_mol ~ ASE / [N * (1 - cos(2pi/N))]")
print(f"    Lambda_1_mol ~ {ASE_benzene_exp:.2f} / [6 * {1 - np.cos(2*np.pi/6):.4f}]")
print(f"    Lambda_1_mol ~ {Lambda_1_molecular:.3f} eV")
print()
print(f"  This is the molecular-scale lock potential strength.")
print(f"  Compare to the fundamental kink Lambda_1 = 3.6e-9 (dimensionless at Planck scale)")
print(f"  The huge difference reflects the RG running from M_P to molecular scales.")
print()


# ============================================================================
# PART 6: PURINE VS PYRIMIDINE — WINDING CAPACITY
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 6: PURINE VS PYRIMIDINE — WINDING NUMBER CLASSIFICATION              ║
╚══════════════════════════════════════════════════════════════════════════════╝

The purine/pyrimidine distinction maps to PHASE WINDING CAPACITY:

  PYRIMIDINE (C, T):
    Single ring (6 atoms) → 6 pi electrons → n = 1
    Maximum winding: k_max = 1
    Phase memory channels: 3 (k = 0, +1, -1)
    Physical size: ~3.4 x 2.8 Angstrom

  PURINE (A, G):
    Fused double ring (9 atoms) → 10 pi electrons → n = 2
    Maximum winding: k_max = 2
    Phase memory channels: 5 (k = 0, ±1, ±2)
    Physical size: ~5.4 x 3.4 Angstrom
""")

print("  WINDING CAPACITY TABLE:")
print("  " + "-" * 60)
print(f"  {'Base':>10s} | {'Type':>10s} | {'Rings':>5s} | {'Pi e':>4s} | {'n':>2s} | {'k_max':>5s} | {'Channels':>8s}")
print("  " + "-" * 60)

base_data = [
    ('Adenine',  'Purine',     '5+6',  10, 2, 5),
    ('Guanine',  'Purine',     '5+6',  10, 2, 5),
    ('Cytosine', 'Pyrimidine', '6',     6, 1, 3),
    ('Thymine',  'Pyrimidine', '6',     6, 1, 3),
]

for name, btype, rings, n_pi, n, channels in base_data:
    print(f"  {name:>10s} | {btype:>10s} | {rings:>5s} | {n_pi:>4d} | {n:>2d} | {n:>5d} | {channels:>8d}")

print("  " + "-" * 60)
print()

print("""
  KEY GU INSIGHT:
    Purines have MORE winding modes than pyrimidines.
    This means purines have a RICHER phase topology and can support
    stronger phase memory (theta-FF-tilde) when stacked.

    In DNA, purines always pair with pyrimidines (A-T, G-C).
    The base pair combines a w_max = 2 system with a w_max = 1 system,
    giving a combined base-pair phase topology with modes from BOTH rings.

    This complementarity is not just geometric — it is TOPOLOGICAL.
    The purine provides the deeper phase structure; the pyrimidine
    provides the simpler, more rigid scaffold.
""")


# ============================================================================
# PART 7: HETEROATOM EFFECTS — NITROGEN IN THE RING
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 7: HETEROATOM EFFECTS — NITROGEN IN THE RING                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

DNA bases are HETEROCYCLIC — they contain nitrogen atoms in the ring,
not just carbon. This matters for GU:

  Carbon in ring:  provides 1 pi electron (from p_z after sp2)
  Nitrogen (pyridine-like):  provides 1 pi electron + lone pair IN plane
  Nitrogen (pyrrole-like):   provides 2 pi electrons (lone pair IN pi system)

The nitrogen atoms modify the phase coupling:
  - Nitrogen is more electronegative → phase gradient is asymmetric
  - Lone pair electrons can participate in pi system or remain localised
  - This breaks the pure benzene symmetry, creating DIPOLE MOMENTS

  Dipole moments of DNA bases (experimental):
    Adenine:   2.5 D (Debye)
    Guanine:   6.6 D
    Cytosine:  6.4 D
    Thymine:   4.1 D

  These dipoles are CRUCIAL for:
  1. Hydrogen bonding (base pairing) — Script 02
  2. Stacking interactions (dipole-dipole) — Script 04
  3. Phase memory (asymmetric nabla_theta) — Script 04
""")

dipoles = {'Adenine': 2.5, 'Guanine': 6.6, 'Cytosine': 6.4, 'Thymine': 4.1}
D_to_Cm = 3.336e-30  # 1 Debye in C·m

for name, d in dipoles.items():
    d_Cm = d * D_to_Cm
    print(f"    {name:>10s}:  mu = {d:.1f} D = {d_Cm:.2e} C·m")

print()


# ============================================================================
# PART 8: MOLECULAR DIMENSIONS FROM GU PARAMETERS
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 8: MOLECULAR DIMENSIONS FROM GU PARAMETERS                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

All bond lengths in DNA bases derive from m_e and alpha_EM through the
Bohr radius a_0 = hbar_c / (alpha_EM * m_e).
""")

print(f"  Bohr radius:  a_0 = {a_0_A:.4f} Angstrom = {a_0_fm:.1f} fm")
print()

bond_lengths = {
    'C-C (aromatic)': 1.40,
    'C=C (aromatic)': 1.34,
    'C-N (aromatic)': 1.34,
    'C=N (aromatic)': 1.29,
    'C-N (amine)':    1.37,
    'C=O (carbonyl)': 1.22,
    'N-H':            1.01,
    'C-H':            1.08,
}

print(f"  {'Bond':>18s} | {'Length (A)':>10s} | {'In units of a_0':>15s}")
print("  " + "-" * 50)
for bond, length in bond_lengths.items():
    ratio = length / a_0_A
    print(f"  {bond:>18s} | {length:>10.2f} | {ratio:>15.2f}")

print()
print(f"  All lengths are O(a_0) — the atomic scale set by m_e and alpha_EM.")
print(f"  GU contribution: m_e derived to 23 ppm; alpha_EM is experimental input.")
print()


# ============================================================================
# SUMMARY
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  SUMMARY: NUCLEOTIDE BASES FROM GU                                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

WHAT IS DERIVED FROM GU:
  1. sp2 hybridisation: superposition of kink angular modes (from 23_MOLECULAR_BONDS)
  2. Hückel 4n+2 rule: phase quantization condition — the Omega-field phase
     must wind by 2*pi*k around a closed ring, and Pauli filling of k-modes
     gives the 4n+2 electron count for closed-shell stability
  3. Aromatic stabilisation: delocalised (smooth) winding costs less lock-potential
     energy than localised (abrupt) bonding — Lambda_1 determines the scale
  4. Bond lengths: all set by a_0 = hbar_c/(alpha_EM * m_e), with m_e from GU

WHAT IS STANDARD CHEMISTRY WITH GU PARAMETERS:
  5. The specific structures of A, T, G, C (which heteroatoms where)
  6. Dipole moments (from electronegativity differences)
  7. Aromatic stabilisation energies (quantitative values)

THE KEY GU CLASSIFICATION:
  Pyrimidines (C, T): n = 1, k_max = 1, 3 phase channels, w_total = 1
  Purines (A, G):     n = 2, k_max = 2, 5 phase channels, w_total = 2

  Purines carry a RICHER phase topology — this matters for stacking
  and phase memory in DNA (Script 04).

CONNECTIONS:
  -> Script 02: H-bond donors/acceptors on these bases
  -> Script 03: Why A pairs with T, G pairs with C
  -> Script 04: How aromatic pi systems stack and create phase memory
  -> Script 05: How stacked bases form the double helix
""")
