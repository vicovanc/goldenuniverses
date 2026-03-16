#!/usr/bin/env python3
"""
WHY IRON IS IRREPLACEABLE — SYNTHESIS
======================================

PART 1: IRON vs OTHER TRANSITION METALS
PART 2: THE IRON-SULFUR WORLD HYPOTHESIS
PART 3: IRON IN DNA SYNTHESIS
PART 4: IRON ACROSS THE AGENCY LADDER
PART 5: THE GU DEFINITION — d-ORBITAL BRIDGE
PART 6: LIFE IS THE ART OF PREVENTING RUST

Connects to all prior scripts (01-07), 25_PHONONS, 26_PLATONIC_SPACE, 27_FIRST_CELL.
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


def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║          WHY IRON IS IRREPLACEABLE — SYNTHESIS                               ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    # -------------------------------------------------------------------------
    # PART 1: IRON vs OTHER TRANSITION METALS
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 1: IRON vs OTHER TRANSITION METALS                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Metal   Config      Redox couples           Spin switch?  Abundance   Bio role")
    print("  -----   ---------   --------------------    -----------   ---------   ---------")
    print("  Fe      [Ar]3d⁶     Fe²⁺/Fe³⁺ (+Fe⁴⁺)      YES           high        ETC, O₂, catalysis, sensing, magneto.")
    print("  Cu      [Ar]3d¹⁰    Cu⁺/Cu²⁺               no            moderate    ETC (Complex IV), SOD, blue Cu proteins")
    print("  Zn      [Ar]3d¹⁰    Zn²⁺ only (no redox)   no            moderate    structural (zinc fingers), catalytic (CA)")
    print("  Mn      [Ar]3d⁵     Mn²⁺/³⁺/⁴⁺             yes           lower       water splitting (PSII), SOD, catalase")
    print("  Co      [Ar]3d⁷     Co²⁺/Co³⁺              yes           rare        B₁₂ (radical chemistry)")
    print("  Mo      [Kr]4d⁵     Mo⁴⁺/⁵⁺/⁶⁺             —             very rare   nitrogenase, xanthine oxidase")
    print("  Ni      [Ar]3d⁸     Ni²⁺/³⁺                limited       low         urease, [NiFe]-hydrogenase")
    print()
    print("  Why Fe wins:")
    print("    1. TWO accessible redox states at biological potentials (Fe²⁺/Fe³⁺)")
    print("    2. SPIN-STATE SWITCHING (unique — Cu and Zn cannot do this)")
    print("    3. HIGH ABUNDANCE (4th in Earth's crust, produced by every massive star)")
    print("    4. TUNABLE by protein environment over a ~1.1 V range")
    print("    5. Compatible with both Fe-S clusters AND porphyrins (dual cofactor)")
    print()
    print("  Copper is the CLOSEST competitor (Cu in Complex IV, plastocyanin, SOD).")
    print("  But Cu has only ONE useful redox couple (Cu⁺/Cu²⁺), NO spin switching,")
    print("  and is LESS abundant. Cu is the second violinist; Fe is the conductor.")
    print()
    print("  Zinc is STRUCTURAL ONLY — d¹⁰ = full shell = no phase channel, no redox.")
    print("  In GU: Zn is an amplitude-channel metal. It scaffolds (zinc fingers) but doesn't relay.")
    print()

    # -------------------------------------------------------------------------
    # PART 2: THE IRON-SULFUR WORLD HYPOTHESIS
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 2: THE IRON-SULFUR WORLD HYPOTHESIS                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Wächtershauser (1988): life originated on iron-sulfide surfaces at")
    print("  hydrothermal vents (alkaline, H₂-rich, ~60-90°C).")
    print()
    print("  Evidence:")
    print("    • FeS + H₂S → FeS₂ + H₂ (ΔG = -0.39 eV) — provides energy")
    print("    • Fe-S surfaces catalyze: CO₂ fixation, peptide bond formation, pyruvate synthesis")
    print("    • Fe-S clusters are the MOST ANCIENT cofactors (found in all life, conserved >3.8 Gyr)")
    print("    • Alkaline vents provide natural pH gradients → proto-chemiosmosis")
    print("    • Lost City hydrothermal field (Atlantic): active analog of early Earth vents")
    print()
    print("  In GU: the iron-sulfur world provides the FIRST d-ORBITAL PHASE RELAY.")
    print("  Before membranes, before RNA, before any biology:")
    print("    • Fe-S mineral surfaces had the d-orbital partial phase channel (Script 01)")
    print("    • They could relay electrons (d-orbital → d-orbital hopping)")
    print("    • They catalyzed organic synthesis (V_lock reshaping at mineral surface)")
    print("    • Energy came from FeS → FeS₂ exergonic reaction")
    print()
    print("  The sequence in the Platonic Space:")
    print("    1. Abiotic Fe-S minerals (d-orbital phase relay, no life)")
    print("    2. Proto-metabolism on Fe-S surfaces (chemistry driven by phase relay)")
    print("    3. RNA world adopts Fe-S as cofactor (inherited the relay)")
    print("    4. Modern biology: Fe-S clusters wrapped in proteins (refined the relay)")
    print()
    print("  Iron is not just used by life — iron MAY HAVE ENABLED life's origin.")
    print()

    # -------------------------------------------------------------------------
    # PART 3: IRON IN DNA SYNTHESIS
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 3: IRON IN DNA SYNTHESIS                                               ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Ribonucleotide reductase (RNR): THE enzyme that converts RNA nucleotides to DNA.")
    print("    NDP → dNDP (removes 2'-OH from ribose)")
    print("    Without RNR: no DNA. Without DNA: no stable genome. Without genome: no evolution.")
    print()
    print("  Class I RNR (all eukaryotes, aerobic bacteria):")
    print("    Contains a di-iron (Fe₂) center that generates a tyrosyl radical (Tyr•).")
    print("    The radical propagates ~35 Å through the protein via aromatic residue chain")
    print("    (Tyr → Trp → Tyr → Cys) to the active site where it abstracts H from substrate.")
    print()
    print("  In GU: RNR is a d-orbital → π → radical signaling cascade.")
    print("    • Iron generates the radical (d-orbital chemistry: Fe³⁺-O-Fe³⁺ → Fe⁴⁺=O → Tyr•)")
    print("    • Aromatic residues relay the radical (π-bonded chain, ∇θ ≠ 0)")
    print("    • The radical performs chemistry at the active site (V_lock transition)")
    print()
    print("  This means: WITHOUT IRON, THERE IS NO DNA.")
    print("  The RNA → DNA transition (27_FIRST_CELL/06, timeline ~3.9 Gyr) required")
    print("  iron-dependent radical chemistry. Iron enabled the transition from RNA world to DNA world.")
    print()

    # -------------------------------------------------------------------------
    # PART 4: IRON ACROSS THE AGENCY LADDER
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 4: IRON ACROSS THE AGENCY LADDER                                      ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Iron's role GROWS with life's complexity:")
    print()
    print("  Agency   System                Iron's role                GU channel")
    print("  ------   -------------------   -------------------------  ----------")
    print("  L0       Fe-S mineral           Abiotic electron relay    d-orbital (passive)")
    print("  L3       Protocell catalyst     Proto-metabolic relay     d-orbital in enzyme")
    print("  L5       RNA world → DNA        RNR radical chemistry     d → π → radical")
    print("  L6       LUCA (ETC)            Energy transduction        d-orbital wire (Fe-S)")
    print("  L6       LUCA (O₂ transport)    Hemoglobin/myoglobin      d + π (dual channel)")
    print("  L7       Multicellular          P450 detox, immune        d + π (extreme V_lock)")
    print("  L7       Neural (birds)         Magnetoreception          d-orbital antenna")
    print("  L7       Brain (human)          Iron in neural signaling  d in dopamine path")
    print()
    print("  Iron's contribution to the phase channel SCALES with agency:")
    print("    • L0: simple electron hopping (mineral)")
    print("    • L5: radical relay across protein (d + π coupling)")
    print("    • L6: 13-cluster electron wire (ETC)")
    print("    • L7: spin-state switch for O₂ sensing, magnetic compass for navigation")
    print()
    print("  At every level, iron provides the d-orbital bridge that the π channel alone cannot:")
    print("    • Single-electron transfer (π does multi-electron)")
    print("    • Spin-state switching (π systems don't switch spin)")
    print("    • Magnetic coupling (π bonds are diamagnetic)")
    print()

    # -------------------------------------------------------------------------
    # PART 5: THE GU DEFINITION — d-ORBITAL BRIDGE
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 5: THE GU DEFINITION — d-ORBITAL BRIDGE                                ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Iron in GU is defined by its role as the d-ORBITAL BRIDGE between")
    print("  the amplitude channel (ρ) and the phase channel (θ):")
    print()
    print("  ┌─────────────────────────────────────────────────────────────────────┐")
    print("  │                                                                     │")
    print("  │    σ bonds (w=0)     ──── AMPLITUDE ONLY ────    water, alkanes     │")
    print("  │         ↑                                                           │")
    print("  │    d-orbitals (Fe)   ──── PARTIAL BRIDGE ────    Fe-S, heme, Fe₃O₄  │")
    print("  │         ↓                                                           │")
    print("  │    π bonds (w≥1)     ──── FULL PHASE     ────    DNA, proteins, FAD │")
    print("  │                                                                     │")
    print("  └─────────────────────────────────────────────────────────────────────┘")
    print()
    print("  Without iron:")
    print("    • No electron transport → no energy (ETC dead)")
    print("    • No oxygen transport → no aerobic metabolism (hemoglobin dead)")
    print("    • No DNA → no stable genome (RNR dead)")
    print("    • No magnetoreception → no navigation (compass dead)")
    print("    • No P450 → no detoxification, no steroid hormones")
    print()
    print("  Iron is as essential to the cell as the membrane (boundary) and")
    print("  DNA (information). It provides the d-orbital phase bridge that")
    print("  connects amplitude-channel chemistry to phase-channel biology.")
    print()

    # -------------------------------------------------------------------------
    # PART 6: LIFE IS THE ART OF PREVENTING RUST
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 6: LIFE IS THE ART OF PREVENTING RUST                                  ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  The final synthesis:")
    print()
    print("  1. Stars produce iron as their thermodynamic endpoint (nuclear binding peak).")
    print("  2. Supernovae disperse iron into the cosmos → planets → oceans → life.")
    print("  3. Abiotic Fe-S surfaces provided the first d-orbital phase relays.")
    print("  4. Life adopted iron for energy (ETC), catalysis (P450), oxygen (Hb),")
    print("     information (RNR → DNA), and sensing (IRP, magnetoreception).")
    print("  5. But iron 'wants' to rust: ΔG ~ -1.67 eV per Fe → thermodynamic death.")
    print("  6. Life invests MASSIVE resources to prevent rusting:")
    print("     ferritin, transferrin, hepcidin, IRP, antioxidants, repair enzymes.")
    print("  7. Aging is the slow failure of this anti-rust machinery.")
    print()
    print("  The GU one-liner:")
    print("  IRON is the d-orbital phase bridge between ρ and θ in biology.")
    print("  RUST is the collapse of that bridge to the amplitude ground state.")
    print("  LIFE is the art of maintaining iron in its phase-active states,")
    print("  extracting controlled work from its d-orbital flexibility while")
    print("  preventing the thermodynamic collapse that is rust.")
    print()
    print("  Stars die at iron. Life lives by iron. Aging kills by iron.")
    print("  The story of iron is the story of life's deepest bargain with thermodynamics.")
    print()

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  SUMMARY — ENTIRE 28_IRON_IN_LIFE DERIVATION                                ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  (1) Iron: peak nuclear binding, [Ar]3d⁶, Fe²⁺/Fe³⁺ couple, spin switching (Script 01).")
    print("  (2) Fe-S clusters: oldest cofactors, d-orbital phase relays, ETC wire, Marcus theory (Script 02).")
    print("  (3) Heme: Fe + π ring = dual channel, Hb spin switch, cooperative binding, P450 (Script 03).")
    print("  (4) Redox: Nernst tuning, ETC ladder (8/12 iron-based), Fenton danger (Script 04).")
    print("  (5) Rust: ΔG = -1.67 eV/Fe, phase channel collapse, biological analog = aging (Script 05).")
    print("  (6) Homeostasis: ferritin, transferrin (K_d~10⁻²²), hepcidin loop, IRP sensor (Script 06).")
    print("  (7) Magnetoreception: magnetite + cryptochrome = phase antennae (Script 07).")
    print("  (8) Synthesis: iron = d-orbital bridge; no iron = no ETC, no O₂, no DNA, no compass.")
    print("  Life is the art of preventing its iron from rusting.")
    print()


if __name__ == "__main__":
    main()
