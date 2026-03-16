#!/usr/bin/env python3
"""
THE IRON ECONOMY — IRON HOMEOSTASIS
====================================

PART 1: WHY IRON HOMEOSTASIS EXISTS
PART 2: FERRITIN — IRON STORAGE
PART 3: TRANSFERRIN — IRON TRANSPORT
PART 4: HEPCIDIN-FERROPORTIN — SYSTEMIC REGULATION
PART 5: IRON REGULATORY PROTEINS — CELLULAR SENSING
PART 6: THE DAILY IRON BUDGET
PART 7: WHEN IRON HOMEOSTASIS FAILS

Connects to Script 04 (Fenton danger), Script 05 (rust),
27_FIRST_CELL/10 (six-loop homeostasis), 27_FIRST_CELL/08 (memory channels).
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


def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║              THE IRON ECONOMY — IRON HOMEOSTASIS                             ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    # -------------------------------------------------------------------------
    # PART 1: WHY IRON HOMEOSTASIS EXISTS
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 1: WHY IRON HOMEOSTASIS EXISTS                                        ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Iron is simultaneously ESSENTIAL and LETHAL:")
    print("    ESSENTIAL: ETC (energy), hemoglobin (O₂), catalysis (P450, RNR), sensing (IRP)")
    print("    LETHAL: Fenton chemistry → OH• radical → DNA/protein/lipid damage")
    print()
    print("  No other element in biology has this extreme duality.")
    print("  Therefore: iron MUST be precisely regulated at every level:")
    print("    • Absorption (gut)")
    print("    • Transport (blood)")
    print("    • Storage (ferritin)")
    print("    • Utilization (mitochondria, cytosol)")
    print("    • Recycling (macrophages)")
    print()
    print("  In GU: iron homeostasis is a MINIATURE VERSION of the six-loop cellular homeostasis")
    print("  (27_FIRST_CELL/10). It has its own sensor → signal → response → feedback structure.")
    print("  It exists because the d-orbital phase bridge is too dangerous to leave unregulated.")
    print()

    # -------------------------------------------------------------------------
    # PART 2: FERRITIN — IRON STORAGE
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 2: FERRITIN — IRON STORAGE                                            ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    ferritin_subunits = 24
    max_Fe_per_ferritin = 4500
    Fe_per_ferritin_typical = 2000
    ferritin_outer_nm = mpf('12')
    ferritin_inner_nm = mpf('8')

    print(f"  Ferritin: {ferritin_subunits}-subunit protein shell (H + L chains).")
    print(f"  Outer diameter: ~{float(ferritin_outer_nm)} nm; inner cavity: ~{float(ferritin_inner_nm)} nm.")
    print(f"  Maximum capacity: ~{max_Fe_per_ferritin} Fe³⁺ atoms per ferritin.")
    print(f"  Typical loading: ~{Fe_per_ferritin_typical} Fe³⁺ atoms.")
    print()
    print("  Iron enters as Fe²⁺ → oxidized to Fe³⁺ by ferroxidase centers (H-chain) →")
    print("  stored as ferrihydrite mineral core (5Fe₂O₃·9H₂O) inside the shell.")
    print()
    print("  In GU: ferritin is an AMPLITUDE-CHANNEL SEQUESTRATION device.")
    print("  It converts phase-active Fe²⁺ into phase-dead Fe³⁺ mineral (like controlled rusting)")
    print("  and wraps it in a protein shell that prevents contact with water and H₂O₂.")
    print("  Key: the iron INSIDE ferritin is effectively rust — but REVERSIBLE rust.")
    print("  When iron is needed, H-chain ferrireductase converts Fe³⁺ → Fe²⁺, which exits.")
    print()

    # -------------------------------------------------------------------------
    # PART 3: TRANSFERRIN — IRON TRANSPORT
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 3: TRANSFERRIN — IRON TRANSPORT                                        ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    Kd_transferrin = mpf('1e-22')
    transferrin_sites = 2
    serum_Fe_uM = mpf('20')
    transferrin_saturation_pct = mpf('30')

    print(f"  Transferrin: serum glycoprotein, binds {transferrin_sites} Fe³⁺ ions.")
    print(f"  Binding affinity: K_d ~ 10⁻²² M (extraordinarily tight).")
    print(f"  At this K_d, essentially NO free Fe³⁺ exists in blood.")
    print()
    print(f"  Serum iron: ~{float(serum_Fe_uM)} µM (all bound to transferrin).")
    print(f"  Transferrin saturation: ~{float(transferrin_saturation_pct)}% (normally 2/3 empty → reserve capacity).")
    print()
    print("  Iron delivery: transferrin binds to Transferrin Receptor 1 (TfR1) on cell surface →")
    print("  endocytosis → endosome acidified (pH ~5.5) → Fe³⁺ released →")
    print("  reduced to Fe²⁺ by STEAP3 → exits endosome via DMT1 → enters labile iron pool.")
    print()
    print("  In GU: transferrin ensures ZERO free iron in blood.")
    print("  Free iron + oxygen + H₂O₂ (from normal metabolism) = Fenton chemistry in the bloodstream.")
    print("  Transferrin prevents this by keeping K_d at 10⁻²² M — one of the tightest")
    print("  protein-metal interactions in biology.")
    print()

    # -------------------------------------------------------------------------
    # PART 4: HEPCIDIN-FERROPORTIN — SYSTEMIC REGULATION
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 4: HEPCIDIN-FERROPORTIN — SYSTEMIC REGULATION                         ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Hepcidin: small peptide hormone (25 amino acids), produced by liver.")
    print("  Ferroportin: the ONLY known cellular iron exporter.")
    print()
    print("  The feedback loop:")
    print("    High serum iron / high transferrin saturation")
    print("      → Liver senses via HFE/TfR2 pathway")
    print("      → Hepcidin production INCREASES")
    print("      → Hepcidin binds ferroportin on gut enterocytes and macrophages")
    print("      → Ferroportin internalized and degraded")
    print("      → Less iron exported into blood")
    print("      → Serum iron DECREASES")
    print("      → Loop closes: NEGATIVE FEEDBACK")
    print()
    print("  Low iron / anemia / hypoxia:")
    print("      → Hepcidin production DECREASES")
    print("      → Ferroportin active → more iron exported into blood")
    print("      → Serum iron INCREASES")
    print()
    print("  In GU: the hepcidin-ferroportin axis is a CLASSIC homeostatic feedback loop:")
    print("    Sensor: HFE/TfR2 (transferrin saturation)")
    print("    Signal: hepcidin (hormone, amplitude channel)")
    print("    Response: ferroportin degradation (gate control)")
    print("    Feedback: negative (high iron → less export → iron drops)")
    print()
    print("  This is IDENTICAL in structure to the six homeostatic loops (27_FIRST_CELL/10):")
    print("  sensor → signal → response → feedback → fixed point.")
    print("  The iron economy IS a homeostatic sub-loop within the metabolic loop (Loop 3).")
    print()

    # -------------------------------------------------------------------------
    # PART 5: IRON REGULATORY PROTEINS — CELLULAR SENSING
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 5: IRON REGULATORY PROTEINS — CELLULAR SENSING                        ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  IRP1 and IRP2: Iron Regulatory Proteins — post-transcriptional regulators.")
    print()
    print("  When cellular iron is LOW:")
    print("    IRP1 loses its [4Fe-4S] cluster → changes conformation → binds IRE (Iron")
    print("    Responsive Element) in mRNA.")
    print("    IRE in 5' UTR (ferritin, ferroportin mRNA) → translation BLOCKED")
    print("    IRE in 3' UTR (TfR1 mRNA) → mRNA STABILIZED → more TfR1 made")
    print("    Result: MORE iron import (TfR1↑), LESS storage (ferritin↓)")
    print()
    print("  When cellular iron is HIGH:")
    print("    IRP1 assembles [4Fe-4S] cluster → becomes aconitase (Krebs cycle enzyme)")
    print("    IRP2 is ubiquitinated and degraded (FBXL5 pathway)")
    print("    Result: ferritin↑ (storage), TfR1↓ (less import)")
    print()
    print("  In GU: the Fe-S cluster on IRP1 is a d-ORBITAL SENSOR.")
    print("  The cluster's assembly state directly reports cellular iron availability:")
    print("    [4Fe-4S] assembled → iron sufficient → aconitase function → Krebs cycle")
    print("    [4Fe-4S] disassembled → iron deficient → IRP function → gene regulation")
    print("  One protein, two functions, switched by a d-orbital cofactor.")
    print("  This is a molecular-scale d-orbital → gene regulation → protein expression")
    print("  feedback loop: the iron sub-loop at its most fundamental.")
    print()

    # -------------------------------------------------------------------------
    # PART 6: THE DAILY IRON BUDGET
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 6: THE DAILY IRON BUDGET                                              ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    total_body_Fe_g = mpf('3.5')
    Hb_Fe_g = mpf('2.5')
    storage_Fe_g = mpf('0.5')
    myoglobin_Fe_g = mpf('0.3')
    enzyme_Fe_g = mpf('0.2')
    daily_absorption_mg = mpf('1.5')
    daily_loss_mg = mpf('1.5')
    daily_recycled_mg = mpf('25')

    print(f"  Total body iron (adult): ~{float(total_body_Fe_g):.1f} g")
    print(f"    Hemoglobin:  {float(Hb_Fe_g):.1f} g  ({float(Hb_Fe_g/total_body_Fe_g*100):.0f}%)")
    print(f"    Storage:     {float(storage_Fe_g):.1f} g  ({float(storage_Fe_g/total_body_Fe_g*100):.0f}%)")
    print(f"    Myoglobin:   {float(myoglobin_Fe_g):.1f} g  ({float(myoglobin_Fe_g/total_body_Fe_g*100):.0f}%)")
    print(f"    Enzymes/ETC: {float(enzyme_Fe_g):.1f} g  ({float(enzyme_Fe_g/total_body_Fe_g*100):.0f}%)")
    print()
    print(f"  Daily absorption (gut):   ~{float(daily_absorption_mg):.1f} mg")
    print(f"  Daily loss (skin, gut):    ~{float(daily_loss_mg):.1f} mg")
    print(f"  Daily recycling (RBCs):    ~{float(daily_recycled_mg):.0f} mg")
    print()

    recycle_ratio = daily_recycled_mg / daily_absorption_mg
    print(f"  Recycling / absorption ratio: {float(recycle_ratio):.0f}×")
    print("  The body recycles ~17× more iron than it absorbs — the iron economy is")
    print("  a nearly CLOSED LOOP with minimal exchange with the environment.")
    print()
    print("  RBC lifespan: ~120 days. Senescent RBCs phagocytosed by macrophages →")
    print("  heme degraded → Fe²⁺ released → exported via ferroportin → loaded onto transferrin.")
    print("  This recycling is the LARGEST iron flux in the body.")
    print()
    print("  In GU: the iron budget reveals a CONSERVED LOOP — biology hoards iron")
    print("  because it's too valuable to lose and too dangerous to import freely.")
    print()

    # -------------------------------------------------------------------------
    # PART 7: WHEN IRON HOMEOSTASIS FAILS
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 7: WHEN IRON HOMEOSTASIS FAILS                                        ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  TOO MUCH IRON:")
    print("    • Hemochromatosis (HFE mutation): hepcidin too low → excessive absorption")
    print("      → iron overload in liver, heart, pancreas → organ damage")
    print("    • Transfusion overload: repeated transfusions (thalassemia) → ferritin overwhelmed")
    print("    • Ferroptosis: iron-dependent cell death via lipid peroxidation")
    print("      (recently discovered; cancer cells are vulnerable)")
    print()
    print("  TOO LITTLE IRON:")
    print("    • Iron-deficiency anemia: insufficient hemoglobin → poor O₂ delivery")
    print("      Most common nutritional deficiency worldwide (~2 billion people)")
    print("    • Anemia of inflammation: hepcidin chronically elevated → iron sequestered")
    print("      → functional iron deficiency despite adequate stores")
    print()
    print("  MISLOCALIZED IRON:")
    print("    • Alzheimer's: iron accumulates in amyloid plaques → Fenton damage")
    print("    • Parkinson's: iron in substantia nigra → dopamine neuron death")
    print("    • Friedreich's ataxia: frataxin deficiency → mitochondrial iron overload")
    print()
    print("  In GU: all iron diseases are HOMEOSTASIS FAILURES — the iron sub-loop loses")
    print("  its fixed point. Too much, too little, or wrong location: all break the balance")
    print("  between iron's essential phase-relay function and its destructive Fenton potential.")
    print()

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  SUMMARY                                                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print(f"  (1) Ferritin: stores up to {max_Fe_per_ferritin} Fe³⁺ as reversible rust in protein shell.")
    print(f"  (2) Transferrin: K_d ~ 10⁻²² M; zero free iron in blood.")
    print("  (3) Hepcidin-ferroportin: systemic feedback loop (sensor→signal→response→feedback).")
    print("  (4) IRP1/IRP2: cellular Fe-S cluster sensor → gene regulation; d-orbital sensing.")
    print(f"  (5) Budget: {float(total_body_Fe_g)} g total; {float(daily_recycled_mg):.0f} mg/day recycled vs {float(daily_absorption_mg)} mg absorbed.")
    print("  (6) Failure: hemochromatosis, anemia, ferroptosis, neurodegeneration.")
    print("  Iron homeostasis = a mini-homeostatic loop nested within the cellular six-loop system.")
    print()


if __name__ == "__main__":
    main()
