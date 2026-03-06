#!/usr/bin/env python3
"""
RUST AND OXIDATION — PHASE CHANNEL DEATH
=========================================

PART 1: WHAT IS RUST
PART 2: THERMODYNAMICS OF RUSTING
PART 3: METALLIC Fe vs RUST — PHASE CHANNEL COLLAPSE
PART 4: WHY RUSTING IS SLOW (KINETICS)
PART 5: BIOLOGICAL RUSTING — AGING AND OXIDATIVE DAMAGE

Connects to Script 01 (iron states), Script 04 (Fenton), Script 06 (homeostasis),
27_FIRST_CELL/10 (homeostasis failure).
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
T_room = mpf('298')
k_BT_room = k_B * T_room


def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║          RUST AND OXIDATION — PHASE CHANNEL DEATH                            ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    # -------------------------------------------------------------------------
    # PART 1: WHAT IS RUST
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 1: WHAT IS RUST                                                        ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Rust = iron(III) oxide-hydroxide: Fe₂O₃·nH₂O (hydrated ferric oxide).")
    print("  Also written as FeOOH (goethite, lepidocrocite) or Fe(OH)₃ (ferrihydrite).")
    print()
    print("  Overall reaction:")
    print("    4Fe + 3O₂ + 6H₂O → 4Fe(OH)₃")
    print()
    print("  Step-by-step:")
    print("    1. Fe → Fe²⁺ + 2e⁻  (anodic dissolution)")
    print("    2. O₂ + 2H₂O + 4e⁻ → 4OH⁻  (cathodic reduction)")
    print("    3. Fe²⁺ + 2OH⁻ → Fe(OH)₂  (green rust, intermediate)")
    print("    4. 4Fe(OH)₂ + O₂ → 4FeOOH + 2H₂O  (oxidation to rust)")
    print()
    print("  Rust is the THERMODYNAMIC GROUND STATE of iron in the presence of O₂ and H₂O.")
    print("  Metallic iron is METASTABLE — it 'wants' to become rust.")
    print()

    # -------------------------------------------------------------------------
    # PART 2: THERMODYNAMICS OF RUSTING
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 2: THERMODYNAMICS OF RUSTING                                          ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    delta_G_Fe2O3_kJ = mpf('-742.2')
    delta_G_per_Fe_kJ = delta_G_Fe2O3_kJ / mpf('2')
    kJ_to_eV = mpf('1') / mpf('96.485')
    delta_G_per_Fe_eV = delta_G_per_Fe_kJ * kJ_to_eV

    print("  Formation of Fe₂O₃ from elements:")
    print("    2Fe + 3/2 O₂ → Fe₂O₃")
    print(f"    ΔG°f(Fe₂O₃) = {float(delta_G_Fe2O3_kJ):.1f} kJ/mol")
    print(f"    Per Fe atom: {float(delta_G_per_Fe_kJ):.1f} kJ/mol = {float(delta_G_per_Fe_eV):.2f} eV")
    print()

    delta_G_FeOOH_kJ = mpf('-489.8')
    delta_G_FeOOH_eV = delta_G_FeOOH_kJ * kJ_to_eV

    print("  Formation of FeOOH (goethite, common rust form):")
    print("    Fe + 3/4 O₂ + 1/2 H₂O → FeOOH")
    print(f"    ΔG°f(FeOOH) = {float(delta_G_FeOOH_kJ):.1f} kJ/mol = {float(delta_G_FeOOH_eV):.2f} eV per Fe")
    print()

    delta_G_rust_per_Fe_eV = mpf('-1.67')
    print(f"  Effective ΔG for complete rusting (Fe → Fe(OH)₃): ~{float(delta_G_rust_per_Fe_eV)} eV per Fe")
    print(f"  This is ~{float(abs(delta_G_rust_per_Fe_eV) / k_BT_room):.0f} × k_BT at room temperature")
    print("  → MASSIVELY favorable. Iron doesn't just 'want' to rust — it's thermodynamically compelled.")
    print()

    delta_G_bio_Fe_eV = mpf('-0.3')
    print("  Compare to biological iron redox:")
    print(f"    Typical ΔG per electron transfer step in ETC: ~{float(delta_G_bio_Fe_eV)} eV")
    print(f"    Rusting releases ~{float(abs(delta_G_rust_per_Fe_eV) / abs(delta_G_bio_Fe_eV)):.0f}× more energy per Fe")
    print("    → Biology uses CONTROLLED, small-step electron transfer to extract useful work.")
    print("    → Rust is UNCONTROLLED, all-at-once collapse to the ground state.")
    print()

    # -------------------------------------------------------------------------
    # PART 3: METALLIC Fe vs RUST — PHASE CHANNEL COLLAPSE
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 3: METALLIC Fe vs RUST — PHASE CHANNEL COLLAPSE                       ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  METALLIC IRON (Fe⁰):")
    print("    • d-electrons delocalized in bands → electrical conductor")
    print("    • Ferromagnetic: spins align collectively → macroscopic magnetism")
    print("    • Partial phase channel ACTIVE: spin-orbit coupling, magnetic ordering")
    print("    • In GU: d-orbital phase channel is OPEN — iron has agency-like properties")
    print()
    print("  RUST (Fe₂O₃):")
    print("    • d-electrons LOCALIZED in Fe-O ionic bonds → electrical insulator")
    print("    • Antiferromagnetic (hematite) or paramagnetic → no useful magnetism")
    print("    • Phase channel KILLED: no free d-electrons, no spin switching, no relay")
    print("    • In GU: d-orbital phase channel is CLOSED — rust is amplitude-only dead matter")
    print()
    print("  The GU interpretation of rust:")
    print("    Rusting = COLLAPSE of the d-orbital phase channel to the amplitude ground state.")
    print("    The d-electrons, which were mobile and phase-active in metal or protein,")
    print("    become trapped in insulating Fe-O bonds.")
    print("    Information-carrying capacity: DESTROYED.")
    print("    Electron relay function: DESTROYED.")
    print("    Spin-state switching: DESTROYED.")
    print()
    print("    Rust is the THERMODYNAMIC DEATH of iron's phase channel.")
    print("    Life = maintaining iron in phase-active states AGAINST this thermodynamic pull.")
    print()

    # -------------------------------------------------------------------------
    # PART 4: WHY RUSTING IS SLOW (KINETICS)
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 4: WHY RUSTING IS SLOW (KINETICS)                                     ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Despite ΔG ~ -1.67 eV, metallic iron doesn't instantly rust. Why?")
    print()

    E_a_rust_eV = mpf('0.5')
    print(f"  Activation barrier: E_a ~ {float(E_a_rust_eV)} eV (for anodic dissolution in neutral pH)")
    print(f"  Arrhenius: k ~ A exp(-E_a/k_BT)")
    print(f"  At 298 K: exp(-E_a/k_BT) = exp(-{float(E_a_rust_eV/k_BT_room):.1f}) = {float(exp(-E_a_rust_eV/k_BT_room)):.2e}")
    print()
    print("  Requirements for rusting:")
    print("    1. WATER: electrolyte for ion transport (Fe²⁺ must dissolve)")
    print("    2. OXYGEN: electron acceptor (cathodic half-reaction)")
    print("    3. ELECTROLYTE: ions (e.g. NaCl) increase conductivity → faster rusting")
    print()
    print("  Without water: rusting essentially stops (dry iron in vacuum is stable indefinitely).")
    print("  In GU: water enables the amplitude-channel ion transport that feeds the rusting reaction.")
    print("  This is an ironic parallel: water enables life (amplitude medium for the cell),")
    print("  and water also enables iron's death (amplitude medium for rusting).")
    print()
    print("  Protective mechanisms:")
    print("    • Passivation: thin Fe₃O₄ (magnetite) layer on surface resists further oxidation")
    print("    • Stainless steel: Cr₂O₃ passivation layer (chromium replaces iron at surface)")
    print("    • Galvanizing: Zn coating sacrificially oxidizes instead of Fe")
    print("    • In biology: PROTEINS wrap iron, preventing contact with water + O₂ (ferritin, Hb)")
    print()

    # -------------------------------------------------------------------------
    # PART 5: BIOLOGICAL RUSTING — AGING AND OXIDATIVE DAMAGE
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 5: BIOLOGICAL RUSTING — AGING AND OXIDATIVE DAMAGE                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Aging is, in part, the slow 'rusting' of the cell's iron machinery:")
    print()
    print("  1. Mitochondrial ETC becomes less efficient with age")
    print("     → More electron leakage → more O₂•⁻ and H₂O₂")
    print("     → More Fenton chemistry if labile iron increases")
    print()
    print("  2. Iron accumulates in aging tissues")
    print("     Brain iron increases ~30% from age 20 to 80")
    print("     Liver iron increases; ferritin capacity may be exceeded")
    print("     → Free iron pool grows → more Fenton damage")
    print()
    print("  3. Repair mechanisms decline")
    print("     BER (base excision repair) efficiency drops")
    print("     Proteasome activity decreases (damaged proteins accumulate)")
    print("     → Damage accumulates faster than repair")
    print()
    print("  4. Lipofuscin: 'age pigment' — indigestible aggregates of oxidized lipids,")
    print("     proteins, and iron. Accumulates in lysosomes of neurons and cardiac cells.")
    print("     Contains iron trapped in non-functional, oxidized form.")
    print()
    print("  In GU: aging = gradual collapse of iron homeostasis (Script 06).")
    print("  The six-loop cellular homeostasis (27_FIRST_CELL/10) degrades,")
    print("  and the iron sub-loop is one of the first to fail because iron")
    print("  is simultaneously the most essential and most dangerous cofactor.")
    print()
    print("  Neurodegenerative diseases linked to iron:")
    print("    • Alzheimer's: iron accumulates in amyloid plaques")
    print("    • Parkinson's: iron in substantia nigra (dopamine neurons)")
    print("    • Friedreich's ataxia: genetic defect in frataxin → mitochondrial iron overload")
    print("    → All involve loss of iron homeostasis → uncontrolled phase-channel collapse")
    print()
    print("  The deep GU insight:")
    print("  Life is the art of preventing its iron from rusting.")
    print("  Aging is what happens when that art fails.")
    print()

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  SUMMARY                                                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print(f"  (1) Rust = Fe₂O₃·nH₂O. ΔG ~ {float(delta_G_rust_per_Fe_eV)} eV per Fe (massively favorable).")
    print("  (2) Metallic Fe: d-electrons delocalized, phase channel ACTIVE (conductor, magnetic).")
    print("  (3) Rust: d-electrons localized in Fe-O bonds, phase channel DEAD (insulator).")
    print("  (4) Rusting = collapse of d-orbital phase channel to amplitude ground state.")
    print(f"  (5) Kinetic barrier ~{float(E_a_rust_eV)} eV; requires water + O₂; biology wraps iron in proteins.")
    print("  (6) Aging = slow biological rusting: iron accumulation + declining repair → damage.")
    print("  Life maintains iron against thermodynamic death; aging is when this maintenance fails.")
    print()


if __name__ == "__main__":
    main()
