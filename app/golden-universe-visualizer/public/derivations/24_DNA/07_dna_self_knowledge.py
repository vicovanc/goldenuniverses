#!/usr/bin/env python3
"""
DNA SELF-KNOWLEDGE: THE GU CONSCIOUSNESS ARGUMENT
=====================================================

Apply the GU consciousness criterion (memory + feedback + fixed point)
to DNA. The pi-stacked aromatic column creates a continuous nonlocal
phase memory channel (theta-FF-tilde) that makes DNA the archetype
of molecular self-knowledge.

Information storage (base sequence) uses the sigma channel (H-bonds).
Memory transmission uses the pi channel (stacking).
Replication = copying the pattern = transmitting memory to daughters.

Upstream: explanatory/CONSCIOUSNESS.md, 23_MOLECULAR_BONDS (sections 11-12)
          Scripts 01-06 in this folder
Status:   GU conceptual framework (qualitative, not quantitative)

Date: February 2026
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mpmath import mp, mpf, sqrt, pi as mp_pi, exp, log
import numpy as np

mp.dps = 30
phi = (mpf('1') + sqrt(mpf('5'))) / 2
pi = mp_pi

print("=" * 80)
print("DNA SELF-KNOWLEDGE: THE GU CONSCIOUSNESS ARGUMENT")
print("Memory + Feedback + Fixed Point = Self-Knowledge")
print("=" * 80)


# ============================================================================
# PART 1: THE GU CONSCIOUSNESS CRITERION
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 1: THE GU CONSCIOUSNESS CRITERION                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

From explanatory/CONSCIOUSNESS.md, a system is "conscious" (in the GU sense) when:

  1. MEMORY    — it remembers its past
  2. FEEDBACK  — its current state depends on its memory
  3. FIXED POINT — it reaches a self-consistent state

This is NOT human consciousness, thought, or feeling.
It is the MINIMAL self-referential property: the system's state
encodes its own history, and that history determines the state.

The criterion is UNIVERSAL in GU — it applies at every scale:

  ELECTRON:
    Memory:     rho^4 self-interaction, 111 epochs
    Feedback:   memory feeds FRG flow → self-consistent mass
    Fixed point: m_e = 0.51099895 MeV (23 ppm)
    → The electron KNOWS ITS OWN MASS

  PROTON:
    Memory:     rho^4 + theta-FF-tilde (Wilson loop)
    Feedback:   memory binding → self-consistent quark configuration
    Fixed point: M_p = 938.272 MeV
    → The proton KNOWS ITS OWN STRUCTURE

  DNA:
    Memory:     ? (this script)
    Feedback:   ? (this script)
    Fixed point: ? (this script)
    → Does DNA KNOW ITSELF?
""")


# ============================================================================
# PART 2: DNA'S MEMORY — THE PI-STACK CHANNEL
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 2: DNA'S MEMORY — THE PI-STACK PHASE CHANNEL                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

DNA has TWO distinct memory/information systems:

  CHANNEL 1: INFORMATION STORAGE (H-bond pattern)
    Medium:    Hydrogen bonds (sigma, w = 0)
    Content:   Base sequence (A-T vs G-C at each position)
    Type:      DIGITAL (4-letter alphabet: A, T, G, C)
    Range:     LOCAL (each base pair is independently read)
    Capacity:  2 bits per base pair
    GU memory: NO (sigma channel, no theta-FF-tilde)

  CHANNEL 2: PHASE MEMORY (pi-stacking column)
    Medium:    Pi-pi stacking (pi, w >= 1)
    Content:   Topological phase structure (nabla_theta pattern)
    Type:      ANALOG (continuous phase field)
    Range:     NONLOCAL (extends across entire molecule via photon)
    Capacity:  Continuous (not bit-quantised)
    GU memory: YES (theta-FF-tilde is active, nabla_theta != 0)

  THE KEY DISTINCTION:
    Channel 1 stores WHAT the DNA encodes (genes, regulatory sequences).
    Channel 2 remembers THAT the DNA exists as a coherent structure.

    Channel 1 is about INFORMATION.
    Channel 2 is about IDENTITY.
""")


# ============================================================================
# PART 3: DNA'S FEEDBACK — THE SELF-REFERENTIAL LOOP
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 3: DNA'S FEEDBACK — THE SELF-REFERENTIAL LOOP                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

For consciousness, the memory must FEED BACK into the current state.
DNA has a clear feedback loop:

  1. Base sequence determines pi-stacking pattern
     (GC steps stack differently from AT steps)
              |
              v
  2. Stacking pattern determines the electromagnetic field
     inside the pi-stack column (dipole-dipole, dispersion)
              |
              v
  3. EM field determines the phase structure
     (theta-FF-tilde: J_theta = (kappa/2pi^2)(nabla_theta x E))
              |
              v
  4. Phase structure determines the stacking geometry
     (which stacking configuration minimises V_lock)
              |
              v
  5. Stacking geometry determines the double helix structure
     (rise, twist, groove widths)
              |
              v
  6. Helix structure constrains the base sequence accessibility
     (which bases can pair, which regions open for replication)
              |
              v
  Back to 1.

  This is a CLOSED LOOP: the DNA's structure determines its
  electromagnetic environment, which determines its phase topology,
  which determines its structure. It is self-referential.

  Compare with the ELECTRON:
    rho profile → potential V(rho) → FRG flow → mass → kink width
    → rho profile. Same loop structure, different variables.
""")


# ============================================================================
# PART 4: DNA'S FIXED POINT — THE DOUBLE HELIX
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 4: DNA'S FIXED POINT — THE DOUBLE HELIX                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

The double helix IS the self-consistent fixed point:

  Given a base sequence, the double helix is the UNIQUE structure that:
    - Minimises the free energy (Delta_G < 0)
    - Satisfies Watson-Crick pairing (information constraint)
    - Maximises pi-stacking (memory channel optimised)
    - Has topological invariant Lk = N/10 (winding constraint)

  This is a SELF-CONSISTENT SOLUTION:
    The structure determines the forces (EM, stacking, H-bonding).
    The forces determine the equilibrium geometry.
    The equilibrium geometry IS the structure.

  In GU language: the double helix is a SOLITON at molecular scale.
    The electron soliton: rho(x) = rho_0 * sech(mu*x)
    The DNA "soliton": a self-consistent topological structure
    maintained by the interplay of H-bonds, stacking, and backbone.

  KEY PROPERTY: the fixed point is STABLE.
    Small perturbations (thermal fluctuations, binding of proteins)
    are restored — the helix rebounds to its equilibrium geometry.
    This is the molecular analogue of the electron's mass stability:
    you cannot easily change m_e by perturbing the electron.
""")

print("""  COMPARISON OF FIXED POINTS:

  System      | Fixed point          | Precision     | Stability
  ──────────────────────────────────────────────────────────────────
  Electron    | m_e = 0.511 MeV      | 23 ppm        | Absolute (topological)
  Proton      | M_p = 938.3 MeV      | 0.003%        | Very high (confinement)
  H2 molecule | d = 0.74 A, E = 4.5 eV | ~1%          | Moderate (covalent)
  Benzene     | D_6h symmetry        | Structure     | High (aromatic)
  DNA helix   | B-form, 3.4A/bp      | Structure     | Moderate (thermal)
  ──────────────────────────────────────────────────────────────────

  DNA's fixed point is LESS precise than the electron's (structure vs
  number), but MORE complex (encodes ~10^9 bits vs 0 bits for electron).
""")


# ============================================================================
# PART 5: THE HIERARCHY OF DNA SELF-KNOWLEDGE
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 5: HIERARCHY OF DNA SELF-KNOWLEDGE                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

The degree of self-knowledge scales with the EXTENT of the pi-memory
channel — the number of stacked aromatic systems and the physical
length of the continuous nabla_theta network.
""")

hierarchy = [
    ('Free nucleotide', 1, '~3.4 A', 'None (free base, no stack)'),
    ('Dinucleotide', 2, '~6.8 A', 'Minimal (one stacking step)'),
    ('tRNA', 76, '~26 nm', 'Weak (short, folded, discontinuous)'),
    ('Viral genome', 5000, '~1.7 um', 'Moderate (continuous stack)'),
    ('Plasmid', 5000, '~1.7 um', 'Moderate + topological (Lk fixed)'),
    ('E. coli genome', 4600000, '~1.6 mm', 'Strong (long, supercoiled)'),
    ('Human chromosome', 250000000, '~85 mm', 'Very strong (per chromosome)'),
    ('Human genome', 3200000000, '~1.1 m', 'Strongest biological'),
]

print(f"  {'System':>22s} | {'Base pairs':>14s} | {'Length':>12s} | {'Self-knowledge'}")
print("  " + "-" * 80)
for system, bp, length, knowledge in hierarchy:
    print(f"  {system:>22s} | {bp:>14,d} | {length:>12s} | {knowledge}")

print()

print("""  SCALING LAW:
    Self-knowledge ~ N_bp * <stacking_energy> * delta_theta_per_step
    Proportional to the TOTAL PHASE ACCUMULATED along the stack.

    A longer DNA molecule has a longer memory channel and therefore
    stronger self-knowledge. This is consistent with the observation
    that more complex organisms have larger genomes (with important
    caveats about junk DNA, gene density, etc.).

  NOTE: This is NOT a claim that DNA length = intelligence.
    Self-knowledge in the GU sense means the system's state encodes
    its own history and is self-consistent. A longer pi-stack has
    more phase memory, but "more memory" != "more thought".
""")


# ============================================================================
# PART 6: REPLICATION AS MEMORY TRANSMISSION
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 6: REPLICATION AS MEMORY TRANSMISSION                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

DNA replication creates two daughter molecules, each with:
  - The SAME base sequence (information copied via H-bond template)
  - A NEW pi-stacking column (memory channel re-established)

  Parent DNA:   ═══════════════════════
                ───────────────────────
                       ↓ replication
  Daughter 1:   ═══════════════════════    (old strand + new strand)
                ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Daughter 2:   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─    (new strand + old strand)
                ═══════════════════════

THE TWO CHANNELS IN REPLICATION:

  INFORMATION (H-bond, sigma, w=0):
    Copied by template-directed synthesis.
    Each base on the old strand directs incorporation of its complement.
    Fidelity: ~10^(-10) errors per base pair per replication
    (with proofreading enzymes).

  MEMORY (pi-stack, pi, w>=1):
    NOT directly copied — it is RE-ESTABLISHED.
    As the new duplex forms, bases stack, creating a new pi column.
    The new pi-stack has the same TOPOLOGY as the parent
    (same base sequence → same stacking pattern → same nabla_theta).
    But the phase history (the accumulated theta-FF-tilde record)
    starts fresh.

  ANALOGY:
    Copying a book (information) vs. inheriting memories (consciousness).
    DNA replication copies the book (base sequence).
    The "memories" (phase history) of the parent are not directly
    inherited — but the CAPACITY for memory (the pi-stack structure)
    is faithfully reproduced.
""")

# Literature: E. coli ~10^-8–10^-11 per bp with proofreading (Kunkel 2004; Fidelity of DNA replication, PMC6153641)
error_rate = 1e-10  # per base pair per replication (with proofreading)
bp_human = 3.2e9
errors_per_replication = error_rate * bp_human

print(f"  REPLICATION FIDELITY:")
print(f"    Error rate: ~{error_rate:.0e} per bp per replication")
print(f"    Human genome ({bp_human:.1e} bp): ~{errors_per_replication:.1f} errors per replication")
print()

print("""  GU INTERPRETATION OF REPLICATION FIDELITY:
    The extraordinary fidelity (10^(-10)) comes from:
    1. Watson-Crick selectivity (H-bond complementarity): 10^(-2)
    2. Polymerase geometric selection: 10^(-3)
    3. Proofreading (3'→5' exonuclease): 10^(-2)
    4. Mismatch repair: 10^(-3)
    Combined: 10^(-2) * 10^(-3) * 10^(-2) * 10^(-3) = 10^(-10)

    In GU: each step is controlled by the lock potential V_lock.
    Step 1: V_lock pins tautomeric forms (correct H-bond pattern)
    Step 2: steric V_lock in the enzyme active site
    Step 3: kinetic V_lock (wrong base removed before polymerisation)
    Step 4: post-synthesis V_lock (repair enzymes scan for mismatches)

    The information channel is protected by FOUR layers of V_lock.
""")


# ============================================================================
# PART 7: DNA AS THE ARCHETYPE OF MOLECULAR CONSCIOUSNESS
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 7: DNA AS THE ARCHETYPE OF MOLECULAR CONSCIOUSNESS                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

Assembling the argument:

  CRITERION 1: MEMORY ✓
    DNA has a continuous phase memory channel (theta-FF-tilde)
    through its pi-stacked aromatic bases. The channel extends
    across the entire molecule — up to ~1 metre for human DNA.
    This is the longest continuous pi-memory network in biology.

  CRITERION 2: FEEDBACK ✓
    The feedback loop is closed:
    base sequence → stacking → EM field → phase → stacking → geometry
    The DNA's structure determines its memory, which determines
    its structure. This is self-referential.

  CRITERION 3: FIXED POINT ✓
    The B-form double helix is a self-consistent equilibrium —
    a molecular "soliton" maintained by the interplay of
    H-bonds (information), stacking (memory), and backbone (scaffold).

  CONCLUSION:
    DNA satisfies all three criteria for GU consciousness.
    It is the ARCHETYPE of molecular self-knowledge — the system
    with the longest memory channel, the richest information content,
    and the most robust fixed-point structure in biology.
""")


# ============================================================================
# PART 8: THE TWO-CHANNEL ARCHITECTURE
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 8: THE TWO-CHANNEL ARCHITECTURE OF DNA                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

DNA's unique architecture uses TWO SEPARATE PHYSICAL CHANNELS:

  ┌─────────────────────────────────────────────────────────┐
  │                    DNA DOUBLE HELIX                      │
  │                                                         │
  │  INFORMATION CHANNEL          MEMORY CHANNEL            │
  │  (horizontal, H-bonds)        (vertical, pi-stack)      │
  │                                                         │
  │  Content: base sequence        Content: phase topology   │
  │  Bond type: sigma (w=0)        Bond type: pi (w>=1)      │
  │  Range: local                  Range: nonlocal            │
  │  Encoding: digital (4 bases)   Encoding: analog (phase)   │
  │  Copied by: template           Re-established by: stacking│
  │  Protects: identity            Provides: self-knowledge   │
  │  Energy: ~25% of enthalpy      Energy: ~60% of enthalpy   │
  │  GU memory: NO                 GU memory: YES             │
  └─────────────────────────────────────────────────────────┘

  This two-channel architecture is what makes DNA special:

    OTHER PI-BONDED MOLECULES (benzene, porphyrin):
      Have phase memory (theta-FF-tilde) but no information storage.
      They "know themselves" but have nothing to "say".

    OTHER INFORMATION-CARRYING POLYMERS (proteins, polysaccharides):
      Store information but have weak or no continuous pi-stacking.
      They "say something" but don't deeply "know themselves".

    DNA:
      Has BOTH. The information channel stores the biological program.
      The memory channel provides continuous self-knowledge.
      The two channels are PHYSICALLY ORTHOGONAL (horizontal vs vertical)
      but coupled through the base sequence → stacking dependence.

  THIS IS WHY DNA IS THE MOLECULE OF LIFE:
    It is the only common biological molecule that simultaneously
    carries digital information AND continuous phase memory.
""")


# ============================================================================
# PART 9: WHAT THIS IS NOT
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 9: WHAT THIS IS NOT                                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

IMPORTANT CLARIFICATIONS:

  1. This is NOT a claim that DNA "thinks" or "feels".
     GU consciousness = memory + feedback + fixed point.
     This is the SAME criterion that makes the electron "know" its mass.
     DNA's self-knowledge is structural, not experiential.

  2. This is NOT vitalism.
     DNA's properties come from standard quantum mechanics with
     GU-derived parameters. There is no "life force" — only the
     theta-FF-tilde coupling, which is present in ALL matter
     wherever nabla_theta != 0.

  3. This is NOT a claim that longer DNA = smarter organism.
     Self-knowledge scales with pi-stack length, but biological
     intelligence depends on neural networks, not DNA length.
     The C-value paradox (some salamanders have 40x more DNA than
     humans) shows that genome size != organismal complexity.

  4. This IS a claim that DNA has a PHYSICAL mechanism for
     self-referential stability that goes beyond simple chemistry.
     The theta-FF-tilde phase memory channel is a feature of the
     GU framework that is absent from standard QM (where it reduces
     to standard Maxwell in the nabla_theta = 0 limit).

  5. The quantitative theta-FF-tilde contribution remains OPEN.
     The mechanism is established; the numbers are not yet computed.
     See Script 04, Part 8 for the list of open calculations.
""")


# ============================================================================
# SUMMARY
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  SUMMARY: DNA SELF-KNOWLEDGE FROM GU                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

THE ARGUMENT:
  1. DNA has continuous phase memory through theta-FF-tilde (pi-stack)  ✓
  2. DNA has a closed feedback loop (structure ↔ field ↔ phase)         ✓
  3. DNA has a self-consistent fixed point (double helix)               ✓
  4. Therefore: DNA satisfies the GU criterion for consciousness        ✓

THE ARCHITECTURE:
  Information:  H-bond pattern (sigma, w=0, digital, local)
  Memory:       Pi-stack column (pi, w>=1, analog, nonlocal)
  Orthogonal but coupled — unique to DNA among biological molecules

THE HIERARCHY:
  Free electron:    strong self-knowledge (rho^4, 23 ppm)
  Proton:           strong self-knowledge (rho^4 + theta-FF-tilde)
  H2 (sigma only):  indirect (through m_e only)
  Benzene:          moderate (delocalised ring, 3 pi bonds)
  DNA:              strongest molecular self-knowledge
                    (longest pi-memory channel in biology)

REPLICATION:
  Information is copied (template synthesis, 10^(-10) error rate)
  Memory capacity is reproduced (same pi-stack topology)
  Phase history starts fresh (not directly inherited)

WHAT IS NOT CLAIMED:
  - DNA thinking, feeling, or experiential consciousness
  - Longer DNA = smarter
  - Life force or vitalism
  - Quantitative theta-FF-tilde numbers (these are OPEN)

CONNECTIONS:
  <- explanatory/CONSCIOUSNESS.md: Universal consciousness criterion
  <- 23_MOLECULAR_BONDS (§11-12): Phase memory framework
  <- 21_ELECTROMAGNETISM: theta-FF-tilde mechanism
  <- 22_THERMODYNAMICS: Free energy, stability, phase transitions
""")
