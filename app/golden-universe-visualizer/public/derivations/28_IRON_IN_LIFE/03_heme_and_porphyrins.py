#!/usr/bin/env python3
"""
HEME AND PORPHYRINS — IRON IN THE PI RING
==========================================

PART 1: THE PORPHYRIN RING — AROMATIC MACROCYCLE
PART 2: HEMOGLOBIN — THE SPIN-STATE SWITCH
PART 3: COOPERATIVE BINDING — ALLOSTERIC V_LOCK COUPLING
PART 4: CYTOCHROMES — ELECTRON RELAYS IN THE ETC
PART 5: CYTOCHROME P450 — EXTREME V_LOCK RESHAPING

Connects to Script 01 (spin states), Script 02 (Fe-S relays), 27_FIRST_CELL/04 (ETC),
23_MOLECULAR_BONDS/05 (bond order from topology).
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
from mpmath import mp, mpf, sqrt, pi as mp_pi, exp, ln, log
mp.dps = 30
phi = (mpf('1') + sqrt(mpf('5'))) / 2
pi = mp_pi
k_B = mpf('8.617333e-5')
T_bio = mpf('310')
k_BT = k_B * T_bio
hbar_c = mpf('197.3269804')


def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║          HEME AND PORPHYRINS — IRON IN THE PI RING                          ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    # -------------------------------------------------------------------------
    # PART 1: THE PORPHYRIN RING — AROMATIC MACROCYCLE
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 1: THE PORPHYRIN RING — AROMATIC MACROCYCLE                            ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Porphyrin: a planar macrocycle of four pyrrole rings linked by methine bridges.")
    print("  18 π electrons in the conjugated ring → aromatic (Hückel: 4n+2, n=4).")
    print("  Winding number w ≥ 2 (extended conjugation) → FULL phase channel.")
    print()
    print("  In GU: the porphyrin ring is one of biology's most important π systems.")
    print("  It provides a CONTINUOUS ∇θ ≠ 0 domain that encloses the central metal.")
    print()
    print("  Fe in porphyrin = DUAL CHANNEL:")
    print("    • d-orbitals (iron): partial phase channel via spin-orbit coupling")
    print("    • π ring (porphyrin): full phase channel via conjugation")
    print("    • The two couple: iron d-orbitals overlap with porphyrin π orbitals")
    print("    → This makes heme the MOST VERSATILE iron cofactor in biology.")
    print()

    n_pi_electrons = 18
    ring_diameter_Angstrom = mpf('8.5')
    print(f"  Porphyrin ring: {n_pi_electrons} π electrons, diameter ~{float(ring_diameter_Angstrom)} Å")
    print("  Absorption: intense Soret band at ~400 nm (explains red color of blood)")
    print("  The Soret band = π → π* transition of the macrocycle, modified by Fe d-orbitals.")
    print()

    # -------------------------------------------------------------------------
    # PART 2: HEMOGLOBIN — THE SPIN-STATE SWITCH
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 2: HEMOGLOBIN — THE SPIN-STATE SWITCH                                 ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Hemoglobin (Hb): 4 subunits (α₂β₂), each with one heme (Fe²⁺ in protoporphyrin IX).")
    print("  Fifth ligand: proximal histidine (His F8). Sixth: O₂ (when bound) or vacant.")
    print()
    print("  DEOXY-Hb (no O₂):")
    print("    Fe²⁺ is HIGH-SPIN (S=2, paramagnetic)")
    print("    Ionic radius: ~0.92 Å — TOO LARGE to fit in porphyrin plane")
    print("    Fe sits 0.4 Å OUT of the plane (toward proximal His)")
    print("    → Porphyrin is domed")
    print()
    print("  OXY-Hb (O₂ bound):")
    print("    O₂ binding → Fe²⁺ transitions to LOW-SPIN (S=0, diamagnetic)")
    print("    Ionic radius shrinks to ~0.75 Å → Fe moves INTO the plane")
    print("    This 0.4 Å movement PULLS the proximal histidine")
    print("    → Triggers conformational change in the entire subunit (T → R state)")
    print()

    displacement_Angstrom = mpf('0.4')
    E_O2_binding_eV = mpf('0.43')
    spin_gap_eV = mpf('0.1')

    print(f"  Fe displacement upon O₂ binding: {float(displacement_Angstrom)} Å")
    print(f"  O₂ binding energy: ~{float(E_O2_binding_eV)} eV per heme")
    print(f"  Spin-state energy gap: ~{float(spin_gap_eV)} eV")
    print(f"  Compare k_BT: {float(k_BT):.4f} eV → spin gap is ~{float(spin_gap_eV/k_BT):.0f} × k_BT")
    print()
    print("  In GU: the spin-state transition is a V_lock transition triggered by O₂.")
    print("  The 0.4 Å movement is a MECHANICAL SIGNAL — the d-orbital phase switch (spin)")
    print("  is TRANSDUCED into a structural change (amplitude channel) via the porphyrin.")
    print("  This is a d-orbital → π → protein signaling cascade.")
    print()

    # -------------------------------------------------------------------------
    # PART 3: COOPERATIVE BINDING — ALLOSTERIC V_LOCK COUPLING
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 3: COOPERATIVE BINDING — ALLOSTERIC V_LOCK COUPLING                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Hill equation: Y = pO₂ⁿ / (P₅₀ⁿ + pO₂ⁿ)")
    print("    Y = fractional saturation, pO₂ = oxygen partial pressure")
    print("    P₅₀ = pressure at half-saturation, n = Hill coefficient")
    print()

    P50_mmHg = mpf('26')
    n_Hill = mpf('2.8')
    print(f"  Hemoglobin: P₅₀ ≈ {float(P50_mmHg)} mmHg, n ≈ {float(n_Hill)}")
    print("  n = 2.8 (close to max of 4 for a tetramer) → STRONG cooperativity.")
    print()
    print("  Mechanism: O₂ binding at one heme SHIFTS V_lock landscape of neighboring hemes.")
    print("    • First O₂: hardest to bind (T state, low affinity)")
    print("    • Each subsequent O₂: easier (progressive T → R transition)")
    print("    • Fourth O₂: easiest (R state, high affinity)")
    print()

    pO2_values = [20, 40, 60, 80, 100]
    print("  Binding curve (Hill equation):")
    print("    pO₂ (mmHg)   Y (fraction bound)")
    print("    ----------    ------------------")
    for pO2 in pO2_values:
        Y = float((mpf(pO2)**n_Hill) / (P50_mmHg**n_Hill + mpf(pO2)**n_Hill))
        print(f"    {pO2:>6}         {Y:.3f}")
    print()
    print("  In GU: cooperativity = V_lock coupling ACROSS subunits through the")
    print("  π-bonded porphyrin-protein network. One spin-state switch (θ) propagates")
    print("  through the protein's aromatic residues to shift the neighbor's V_lock.")
    print("  This is the non-local θFF̃ channel operating at the molecular scale.")
    print()

    # -------------------------------------------------------------------------
    # PART 4: CYTOCHROMES — ELECTRON RELAYS IN THE ETC
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 4: CYTOCHROMES — ELECTRON RELAYS IN THE ETC                           ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Cytochromes: heme-containing proteins that cycle Fe²⁺ ↔ Fe³⁺ for electron transfer.")
    print()
    print("  Type          Heme type   E° (V)       Location         Function")
    print("  ------------  ---------   ----------   ---------------  ----------------------")
    print("  Cytochrome b  Heme b      -0.08/+0.05  Complex III      Low-pot. / high-pot. pair")
    print("  Cytochrome c₁ Heme c      +0.22        Complex III      Passes e⁻ to cyt c")
    print("  Cytochrome c  Heme c      +0.25        Mobile carrier   Shuttles e⁻: III → IV")
    print("  Cytochrome a  Heme a      +0.21        Complex IV       First acceptor in IV")
    print("  Cytochrome a₃ Heme a      +0.39        Complex IV       O₂ reduction site")
    print()
    print("  Cytochrome c: small (12 kDa), soluble, shuttles electrons between Complex III and IV.")
    print("  Heme c: covalently bonded to protein via thioether links (Cys-X-X-Cys-His motif).")
    print("  In GU: each cytochrome is a heme at a specific V_lock depth, tuned by the protein")
    print("  environment. The ETC staircase: Fe-S relays (Script 02) hand off to heme relays,")
    print("  creating a continuous d-orbital phase wire from NADH to O₂.")
    print()

    # -------------------------------------------------------------------------
    # PART 5: CYTOCHROME P450 — EXTREME V_LOCK RESHAPING
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 5: CYTOCHROME P450 — EXTREME V_LOCK RESHAPING                         ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Cytochrome P450: the most powerful biological oxidant.")
    print("  P450 = 'pigment absorbing at 450 nm' when CO-bound (Soret shift due to thiolate ligand).")
    print()
    print("  Catalytic cycle:")
    print("    1. Fe³⁺ (resting) → substrate binds → spin state changes")
    print("    2. Fe³⁺ → Fe²⁺ (first electron from NADPH via reductase)")
    print("    3. Fe²⁺ + O₂ → Fe²⁺-O₂ (oxy-ferrous)")
    print("    4. Second electron → Fe³⁺-O₂²⁻ (peroxo)")
    print("    5. Protonation → Fe³⁺-OOH (hydroperoxo)")
    print("    6. O-O bond cleavage → Fe⁴⁺=O + H₂O  (COMPOUND I — the ferryl intermediate)")
    print("    7. Fe⁴⁺=O oxidizes substrate (C-H → C-OH, etc.) → Fe³⁺ returns")
    print()

    ferryl_oxidation_state = 4
    print(f"  Compound I: Fe⁴⁺=O (ferryl oxo). Oxidation state +{ferryl_oxidation_state}.")
    print("  This is the most extreme Fe oxidation state accessed in biology.")
    print("  Compound I can break C-H bonds with BDE up to ~100 kcal/mol (~4.3 eV).")
    print()
    print("  In GU: P450 accesses a TRANSIENT, high-energy V_lock minimum (Fe⁴⁺=O)")
    print("  that no other enzyme reaches routinely. The porphyrin π system stabilizes")
    print("  this extreme state: the 18-electron ring delocalizes the radical character,")
    print("  preventing destructive radical escape.")
    print()
    print("  Biological scope: ~57,000 known P450 genes across all kingdoms of life.")
    print("  Functions: drug metabolism, steroid synthesis, fatty acid oxidation,")
    print("  vitamin D synthesis, xenobiotic detoxification.")
    print("  P450 is the cell's most versatile oxidative tool — enabled by Fe + π ring.")
    print()

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  SUMMARY                                                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  (1) Porphyrin: 18 π electrons, w ≥ 2, full phase channel. Fe + π = dual channel.")
    print("  (2) Hemoglobin: spin-state switch (high↔low) upon O₂ binding → 0.4 Å Fe movement")
    print("      → allosteric signal. Binary theta switch transduced to structural change.")
    print("  (3) Cooperativity (n=2.8): V_lock coupling across subunits via π-bonded network.")
    print("      Non-local θFF̃ channel at molecular scale.")
    print("  (4) Cytochromes: heme at tuned V_lock depths → ETC electron relay staircase.")
    print("  (5) P450: accesses Fe⁴⁺=O (ferryl) → most powerful biological oxidant.")
    print("      π ring stabilizes extreme state. 57,000+ genes across all life.")
    print("  Heme = iron's most powerful configuration: dual-channel (d + π) enables")
    print("  oxygen transport, electron relay, and extreme catalysis.")
    print()


if __name__ == "__main__":
    main()
