#!/usr/bin/env python3
"""
IRON'S ELECTRON DANCE — REDOX CHEMISTRY FROM GU
================================================

PART 1: THE Fe²⁺/Fe³⁺ REDOX COUPLE
PART 2: THE ETC REDOX POTENTIAL LADDER
PART 3: FENTON CHEMISTRY — WHEN IRON GOES ROGUE
PART 4: REACTIVE OXYGEN SPECIES AND DAMAGE
PART 5: NERNST EQUATION AND BIOLOGICAL TUNING

Connects to Script 01 (oxidation states), Script 02 (Fe-S potentials),
Script 03 (cytochrome potentials), Script 05 (rust), 27_FIRST_CELL/04 (ETC).
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
from mpmath import mp, mpf, sqrt, pi as mp_pi, exp, ln
mp.dps = 30
phi = (mpf('1') + sqrt(mpf('5'))) / 2
pi = mp_pi
k_B = mpf('8.617333e-5')
T_bio = mpf('310')
k_BT = k_B * T_bio
k_B_J = mpf('1.380649e-23')
e_C = mpf('1.602176634e-19')
RT_over_F = k_B_J * T_bio / e_C


def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║          IRON'S ELECTRON DANCE — REDOX CHEMISTRY FROM GU                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    # -------------------------------------------------------------------------
    # PART 1: THE Fe²⁺/Fe³⁺ REDOX COUPLE
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 1: THE Fe²⁺/Fe³⁺ REDOX COUPLE                                        ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    E0_Fe3_Fe2 = mpf('0.77')
    print(f"  Standard reduction potential: Fe³⁺ + e⁻ → Fe²⁺,  E° = +{float(E0_Fe3_Fe2):.2f} V")
    print()
    print("  This means Fe³⁺ is a MODERATE oxidant (wants electrons).")
    print("  Fe²⁺ is a MODERATE reductant (donates electrons easily).")
    print("  The couple sits in the MIDDLE of the biological redox range:")
    print("    NADH/NAD⁺: E° = -0.32 V  (strong reductant)")
    print("    Fe²⁺/Fe³⁺: E° = +0.77 V  (middle)")
    print("    O₂/H₂O:    E° = +0.82 V  (strong oxidant)")
    print()
    print("  BUT: in biology, the protein environment SHIFTS this potential dramatically:")
    print()
    print("  Context                    E° (V)       Shift from standard")
    print("  -------------------------  ----------   -------------------")
    print("  Free aqueous Fe³⁺/Fe²⁺     +0.77        reference")
    print("  Rubredoxin (Fe-Cys₄)       -0.06        -0.83 V")
    print("  Ferredoxin ([4Fe-4S])       -0.42        -1.19 V")
    print("  Cytochrome c (heme c)       +0.25        -0.52 V")
    print("  Cytochrome a₃ (heme a)      +0.39        -0.38 V")
    print("  HiPIP ([4Fe-4S])            +0.35        -0.42 V")
    print()
    print("  In GU: the protein is a V_lock TUNER. By changing the electrostatic environment,")
    print("  hydrogen bonds, and ligand field, the protein shifts the depth of the Fe²⁺ and Fe³⁺")
    print("  V_lock minima, changing which state is thermodynamically favored.")
    print()

    # -------------------------------------------------------------------------
    # PART 2: THE ETC REDOX POTENTIAL LADDER
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 2: THE ETC REDOX POTENTIAL LADDER                                     ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Electrons flow DOWN the potential ladder from NADH to O₂:")
    print()

    ladder = [
        ("NADH/NAD⁺", -0.32),
        ("FMN/FMNH₂", -0.30),
        ("Fe-S N1a [2Fe-2S]", -0.37),
        ("Fe-S N3 [4Fe-4S]", -0.25),
        ("Fe-S N2 [4Fe-4S]", -0.10),
        ("CoQ/CoQH₂", +0.04),
        ("Rieske [2Fe-2S]", +0.28),
        ("Cyt c₁ (heme c)", +0.22),
        ("Cyt c (mobile)", +0.25),
        ("Cyt a (heme a)", +0.21),
        ("Cyt a₃ (heme a)", +0.39),
        ("O₂/H₂O", +0.82),
    ]

    print("  Carrier                    E° (V)    Iron-based?")
    print("  -------------------------  --------  -----------")
    for name, E in ladder:
        is_iron = "YES (Fe-S)" if "Fe-S" in name else ("YES (heme)" if "Cyt" in name or "cyt" in name else "no")
        print(f"  {name:<28} {E:>+6.2f}    {is_iron}")
    print()

    delta_E_total = ladder[-1][1] - ladder[0][1]
    print(f"  Total potential drop: {delta_E_total:.2f} V = {delta_E_total:.2f} eV")
    print()

    iron_carriers = [c for c in ladder if "Fe-S" in c[0] or "Cyt" in c[0] or "cyt" in c[0]]
    print(f"  Iron-based carriers: {len(iron_carriers)} out of {len(ladder)} total ({len(iron_carriers)}/{len(ladder)})")
    print("  Iron dominates the ETC relay network. Without iron, no electron transport,")
    print("  no proton gradient, no ATP. Life's energy system IS an iron machine.")
    print()

    # -------------------------------------------------------------------------
    # PART 3: FENTON CHEMISTRY — WHEN IRON GOES ROGUE
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 3: FENTON CHEMISTRY — WHEN IRON GOES ROGUE                            ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Fenton reaction: Fe²⁺ + H₂O₂ → Fe³⁺ + OH• + OH⁻")
    print("  Haber-Weiss (net): O₂•⁻ + H₂O₂ → OH• + OH⁻ + O₂  (iron-catalyzed)")
    print()

    E_OH_radical_eV = mpf('5.1')
    print(f"  Hydroxyl radical (OH•): the MOST reactive ROS.")
    print(f"    Reduction potential: +2.31 V (= {float(E_OH_radical_eV)} eV ionization potential)")
    print("    Reacts with ANY biomolecule within ~1 nm in < 1 ns.")
    print("    Damages: DNA (strand breaks, base oxidation), proteins (carbonylation),")
    print("    lipids (peroxidation of membrane fatty acids).")
    print()
    print("  In GU: Fenton chemistry is DESTRUCTIVE PHASE-CHANNEL NOISE.")
    print("  The hydroxyl radical is a random V_lock transition that tears through")
    print("  the energy landscape without control — destroying information (DNA),")
    print("  structure (proteins), and boundaries (membranes).")
    print()
    print("  Iron is a DOUBLE-EDGED SWORD:")
    print("    CONTROLLED: electron relay (ETC, catalysis) → essential for life")
    print("    UNCONTROLLED: Fenton chemistry → lethal radical production")
    print("  This is WHY iron homeostasis is critical (Script 06).")
    print()

    # -------------------------------------------------------------------------
    # PART 4: REACTIVE OXYGEN SPECIES AND DAMAGE
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 4: REACTIVE OXYGEN SPECIES AND DAMAGE                                 ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  ROS hierarchy (iron-related):")
    print()
    print("  Species            Source                     Reactivity   Lifetime")
    print("  -----------------  -------------------------  ----------   --------")
    print("  O₂•⁻ (superoxide)  ETC leakage (1-2%)         moderate     ~1 µs")
    print("  H₂O₂ (peroxide)    SOD dismutation of O₂•⁻     mild         ~1 ms")
    print("  OH• (hydroxyl)     Fenton: Fe²⁺ + H₂O₂        EXTREME      ~1 ns")
    print("  Fe⁴⁺=O (ferryl)    Controlled (P450, perox.)  extreme      controlled")
    print()

    damage_per_day = mpf('10000')
    print(f"  Estimated DNA lesions per cell per day from ROS: ~{float(damage_per_day):.0f}")
    print("  Most repaired by base excision repair (BER); unrepaired → mutations → cancer/aging.")
    print()
    print("  The connection to iron:")
    print("    • 1-2% of electrons LEAK from the ETC → form O₂•⁻")
    print("    • SOD converts O₂•⁻ → H₂O₂")
    print("    • If FREE Fe²⁺ is present: H₂O₂ + Fe²⁺ → OH• (Fenton)")
    print("    • This is why free iron in the cytoplasm is kept EXTREMELY low (~1 µM labile pool)")
    print()
    print("  In GU: ROS damage is the price of using a d-orbital phase relay in an")
    print("  oxygen-rich environment. Life accepts this cost because the energy gain")
    print("  (~1.14 eV per NADH via aerobic ETC) vastly exceeds the repair cost.")
    print()

    # -------------------------------------------------------------------------
    # PART 5: NERNST EQUATION AND BIOLOGICAL TUNING
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 5: NERNST EQUATION AND BIOLOGICAL TUNING                              ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Nernst equation: E = E° - (k_BT/ne) ln(Q)")
    print("  For Fe³⁺/Fe²⁺ (n=1): E = E° - (k_BT/e) ln([Fe²⁺]/[Fe³⁺])")
    print()

    RT_over_F_mV = float(RT_over_F) * 1000
    print(f"  At T = {float(T_bio)} K: k_BT/e = {RT_over_F_mV:.2f} mV")
    print()

    ratios = [0.01, 0.1, 1.0, 10.0, 100.0]
    E0 = 0.77
    print(f"  E° = +{E0:.2f} V for free aqueous Fe³⁺/Fe²⁺")
    print()
    print("  [Fe²⁺]/[Fe³⁺]    E (V)")
    print("  ---------------   --------")
    for ratio in ratios:
        E = E0 - float(RT_over_F) * float(ln(mpf(str(ratio))))
        print(f"  {ratio:>10.2f}        {E:>+7.3f}")
    print()
    print("  In GU: the Nernst equation describes how the CONCENTRATION RATIO (ρ channel)")
    print("  shifts the V_lock depth (θ channel accessibility). Biology controls iron's")
    print("  redox state by controlling its concentration ratio AND its protein environment.")
    print()

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  SUMMARY                                                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print(f"  (1) Fe²⁺/Fe³⁺: E° = +0.77 V; protein tunes this from -0.5 V to +0.4 V.")
    print(f"  (2) ETC ladder: {len(iron_carriers)}/{len(ladder)} carriers are iron-based (Fe-S + heme).")
    print(f"      Total drop: {delta_E_total:.2f} eV from NADH to O₂.")
    print("  (3) Fenton: Fe²⁺ + H₂O₂ → OH• (most destructive ROS, reacts in <1 ns).")
    print("  (4) ~10,000 DNA lesions/cell/day from ROS; free Fe²⁺ kept at ~1 µM.")
    print("  (5) Nernst: concentration ratio shifts V_lock; biology controls both ratio and environment.")
    print("  Iron's dual nature: ESSENTIAL (controlled relay) and LETHAL (uncontrolled Fenton).")
    print()


if __name__ == "__main__":
    main()
