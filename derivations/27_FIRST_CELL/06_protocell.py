#!/usr/bin/env python3
"""
THE PROTOCELL — MINIMUM VIABLE CELL FROM GU
============================================

PART 1: WHAT A PROTOCELL NEEDS (GU MINIMUM REQUIREMENTS)
- Four essential components derived from GU:
  1. MEMBRANE (Script 01): lipid bilayer creates Platonic Space boundary, separates inside/outside
  2. GENETIC MATERIAL (Script 05): RNA for information + catalysis + replication
  3. ENERGY SOURCE: chemical energy (simple redox, thioester bonds, pyrophosphate, UV light)
  4. WATER: amplitude-channel medium, transparent to phase information
- This is the MINIMUM: fewer components and the system cannot self-replicate with enclosure
- In GU: the protocell is the simplest system at AGENCY LEVEL 5 (self-replicating)

PART 2: HOW THE PROTOCELL WORKS
- RNA replicase (ribozyme): an RNA molecule that copies RNA
  - Template strand provides the sequence (information, sigma channel)
  - Replicase reads the template and assembles complementary strand (catalysis, phase channel)
  - The copied RNA can fold and function → self-sustaining
- Membrane growth: fatty acids in the environment partition into the bilayer
  - As internal osmotic pressure increases (from RNA replication), the membrane stretches
  - When surface area/volume ratio exceeds critical: vesicle DIVIDES (purely physical, no machinery)
- Energy coupling: simple redox reactions or UV-driven chemistry provide the ~0.5 eV per nucleotide needed for RNA polymerization
- The protocell CYCLE: (1) RNA replicates → (2) osmotic pressure rises → (3) fatty acids incorporated → (4) vesicle divides → (5) repeat
- Print the energy budget for one replication cycle

PART 3: MINIMUM GENOME SIZE
- A self-replicating RNA replicase needs at least ~200-300 nucleotides (based on smallest known ribozymes)
- The protocell genome = 1 RNA molecule (the replicase that copies itself)
- Information content: 4^200 possible sequences ~ 10^120 → finding a functional one is astronomically unlikely by random search
- BUT: the V_lock landscape GUIDES evolution — only sequences that fold into stable structures persist
  - Folded RNA = deep V_lock minimum (thermodynamically stable)
  - Unfolded RNA = shallow or no minimum → degrades quickly
  - Natural selection among RNA molecules: those that replicate faster persist
- In GU: the energy landscape (Script 04 of 26_PLATONIC_SPACE) selects viable RNA sequences, NOT random search
- The sequence space has deep valleys (functional ribozymes) separated by barriers (non-functional sequences)

PART 4: THE THRESHOLD OF LIFE
- The protocell satisfies the GU LIFE criteria (from Script 12):
  1. ENCLOSURE: lipid membrane ✓
  2. TWO-CHANNEL: RNA stacking (theta) + metabolism (rho) ✓
  3. SELF-REPLICATION: RNA replicase copies genome ✓
  4. HOMEOSTASIS: crude — replication rate ≈ degradation rate at steady state ✓ (barely)
  5. AGENCY: RNA catalysis modifies local chemistry ✓ (minimal)
  6. CONSCIOUSNESS: memory (RNA sequence) + feedback (replication success) + fixed point (stable population) ✓ (minimal)
- The protocell is ALIVE — just barely
- It is the SIMPLEST living system: one membrane, one RNA, simple chemistry
- In GU: it sits at the threshold — the phase transition from non-life (agency 0-3) to life (agency 4+)

PART 5: FROM PROTOCELL TO MODERN CELL
- Timeline: ~4.0 Gyr ago (earliest protocells) → ~3.8 Gyr (LUCA, Script 11) → ~3.5 Gyr (first fossils)
- Key innovations:
  - RNA → DNA (more stable information storage, ~3.9 Gyr ago)
  - RNA → protein catalysis (ribosome evolves, ~3.8 Gyr ago)
  - Simple → chemiosmotic metabolism (proton motive force, ~3.8 Gyr ago)
  - Single → double membrane (better gradient control, ~3.7 Gyr ago)
- Each step INCREASES the number of memory channels and feedback loops → HIGHER consciousness
- Print a table: time, innovation, memory channels gained, agency level

SUMMARY connecting to all prior scripts and forward to Scripts 07-12.
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
from mpmath import mp, mpf, sqrt, pi as mp_pi, exp, ln
mp.dps = 30
phi = (mpf('1') + sqrt(mpf('5'))) / 2
pi = mp_pi
alpha_EM = mpf('1') / mpf('137.035999177')
M_P = mpf('1.22089e22')
m_e = mpf('0.51099895')
hbar_c = mpf('197.3269804')
k_B = mpf('8.617333e-5')
T_bio = mpf('310')
k_BT = k_B * T_bio
lambda_rec_beta = exp(phi) / pi**2


def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║            THE PROTOCELL — MINIMUM VIABLE CELL FROM GU                       ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    # -------------------------------------------------------------------------
    # PART 1: WHAT A PROTOCELL NEEDS (GU MINIMUM REQUIREMENTS)
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 1: WHAT A PROTOCELL NEEDS (GU MINIMUM REQUIREMENTS)                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("Four essential components derived from GU:")
    print("  1. MEMBRANE (Scripts 01–02): lipid bilayer creates Platonic Space boundary,")
    print("     separates inside/outside.")
    print("  2. GENETIC MATERIAL (Script 05): RNA for information + catalysis + replication.")
    print("  3. ENERGY SOURCE: chemical energy (simple redox, thioester bonds, pyrophosphate,")
    print("     UV light).")
    print("  4. WATER: amplitude-channel medium, transparent to phase information.")
    print()
    print("This is the MINIMUM: fewer components and the system cannot self-replicate")
    print("with enclosure. In GU: the protocell is the simplest system at AGENCY LEVEL 5")
    print("(self-replicating).")
    print()

    # -------------------------------------------------------------------------
    # PART 2: HOW THE PROTOCELL WORKS
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 2: HOW THE PROTOCELL WORKS                                              ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("RNA replicase (ribozyme): an RNA molecule that copies RNA.")
    print("  - Template strand: sequence (information, sigma channel).")
    print("  - Replicase: reads template, assembles complementary strand (catalysis, phase channel).")
    print("  - Copied RNA can fold and function → self-sustaining.")
    print()
    print("Membrane growth: fatty acids partition into bilayer; osmotic pressure from RNA")
    print("replication stretches membrane; when S/V exceeds critical → vesicle DIVIDES (physical).")
    print()
    print("Protocell CYCLE: (1) RNA replicates → (2) osmotic pressure rises → (3) fatty acids")
    print("incorporated → (4) vesicle divides → (5) repeat.")
    print()

    # Energy budget for one replication cycle
    E_per_nt_eV = mpf('0.5')   # ~0.5 eV per nucleotide for RNA polymerization
    N_nt = mpf('250')          # minimum replicase ~200–300 nt; use 250
    E_RNA_copy_eV = E_per_nt_eV * N_nt
    E_RNA_copy_kBT = E_RNA_copy_eV / k_BT
    # Membrane: order-of-magnitude ~few k_BT per lipid added; ~1e4 lipids per vesicle, growth ~10% → ~1e3 lipids × ~5 k_BT
    k_BT_per_lipid = mpf('5')
    lipids_added = mpf('1000')
    E_membrane_kBT = k_BT_per_lipid * lipids_added
    E_membrane_eV = E_membrane_kBT * k_BT
    E_total_eV = E_RNA_copy_eV + E_membrane_eV
    E_total_kBT = E_total_eV / k_BT

    print("  ENERGY BUDGET FOR ONE REPLICATION CYCLE (one daughter vesicle):")
    print("  " + "-" * 60)
    print(f"    RNA replication ({float(N_nt):.0f} nt × {float(E_per_nt_eV):.2f} eV/nt)  = {float(E_RNA_copy_eV):.2f} eV  = {float(E_RNA_copy_kBT):.1f} k_B T")
    print(f"    Membrane growth (~{float(lipids_added):.0f} lipids × ~{float(k_BT_per_lipid):.0f} k_B T) = {float(E_membrane_eV):.2f} eV  = {float(E_membrane_kBT):.0f} k_B T")
    print("  " + "-" * 60)
    print(f"    TOTAL (order of magnitude)                  ≈ {float(E_total_eV):.0f} eV  ≈ {float(E_total_kBT):.0f} k_B T")
    print()
    print("  Energy source: simple redox or UV-driven chemistry must supply this per cycle.")
    print()

    # -------------------------------------------------------------------------
    # PART 3: MINIMUM GENOME SIZE
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 3: MINIMUM GENOME SIZE                                                  ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("Self-replicating RNA replicase: at least ~200–300 nucleotides (smallest known ribozymes).")
    print("Protocell genome = 1 RNA molecule (the replicase that copies itself).")
    print()
    # 4^200 ≈ 10^(200*log10(4)) ≈ 10^120
    log10_4 = ln(mpf('4')) / ln(mpf('10'))
    log10_N_seq = 200 * log10_4
    print(f"  Information content: 4^200 possible sequences ≈ 10^{float(log10_N_seq):.0f}.")
    print("  Finding a functional one by random search is astronomically unlikely.")
    print()
    print("BUT: the V_lock landscape GUIDES evolution (Script 04, 26_PLATONIC_SPACE):")
    print("  - Folded RNA = deep V_lock minimum (thermodynamically stable).")
    print("  - Unfolded RNA = shallow or no minimum → degrades quickly.")
    print("  - Natural selection: sequences that replicate faster persist.")
    print("  - Sequence space has deep valleys (functional ribozymes) separated by barriers.")
    print()

    # -------------------------------------------------------------------------
    # PART 4: THE THRESHOLD OF LIFE
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 4: THE THRESHOLD OF LIFE                                                ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("The protocell satisfies the GU LIFE criteria (from Script 12):")
    print("  1. ENCLOSURE: lipid membrane ✓")
    print("  2. TWO-CHANNEL: RNA stacking (theta) + metabolism (rho) ✓")
    print("  3. SELF-REPLICATION: RNA replicase copies genome ✓")
    print("  4. HOMEOSTASIS: crude — replication rate ≈ degradation rate ✓ (barely)")
    print("  5. AGENCY: RNA catalysis modifies local chemistry ✓ (minimal)")
    print("  6. CONSCIOUSNESS: memory (RNA sequence) + feedback (replication success)")
    print("     + fixed point (stable population) ✓ (minimal)")
    print()
    print("The protocell is ALIVE — just barely. Simplest living system: one membrane,")
    print("one RNA, simple chemistry. In GU: phase transition from non-life (agency 0–3)")
    print("to life (agency 4+).")
    print()

    # -------------------------------------------------------------------------
    # PART 5: FROM PROTOCELL TO MODERN CELL
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 5: FROM PROTOCELL TO MODERN CELL                                        ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("Timeline: ~4.0 Gyr (earliest protocells) → ~3.8 Gyr (LUCA, Script 11) → ~3.5 Gyr (fossils).")
    print()
    print("  Time (Gyr ago)  Innovation                              Memory channels    Agency")
    print("  " + "-" * 78)
    rows = [
        ("4.0", "Protocell (membrane + RNA replicase)", "1 (RNA sequence)", "5"),
        ("3.9", "RNA → DNA (stable information storage)", "+1 (DNA)", "5→6"),
        ("3.8", "Ribosome (RNA → protein catalysis)", "+1 (protein sequences)", "6→7"),
        ("3.8", "Chemiosmotic metabolism (proton motive force)", "+1 (ion gradients)", "7"),
        ("3.7", "Double membrane (gradient control)", "+1 (compartmentation)", "7→8"),
    ]
    for t, innov, mem, ag in rows:
        print(f"  {t:>12}  {innov:<42}  {mem:<18}  {ag}")
    print("  " + "-" * 78)
    print()
    print("Each step increases memory channels and feedback loops → higher consciousness.")
    print()

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  SUMMARY — CONNECTIONS TO PRIOR AND LATER SCRIPTS                            ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("BACK: Scripts 01–02 (membrane, Platonic boundary), 03 (catalysis from V_lock),")
    print("      05 (RNA), 26_PLATONIC_SPACE/04 (energy landscape), Script 12 (LIFE criteria).")
    print()
    print("THIS: The protocell is the minimal closed system that meets GU life: enclosure,")
    print("      two-channel (sigma + phase), self-replication, crude homeostasis, minimal")
    print("      agency and consciousness. Energy landscape selects viable RNA; no random search.")
    print()
    print("FORWARD: Scripts 07–12 (from first cell to LUCA, metabolism, genetics, LIFE criteria,")
    print("         consciousness ladder). The protocell is the root of that ladder.")
    print()


if __name__ == "__main__":
    main()
