#!/usr/bin/env python3
"""
THE RNA WORLD — DUAL-FUNCTION MOLECULE FROM GU

Golden Universe (GU) framework: RNA as the minimum molecule with information,
memory, and catalysis; ribozymes; RNA stability and the DNA takeover;
RNA as the lowest-cost entry point for life. Connects to 24_DNA, Script 03 (catalysis), Script 06 (protocell).
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
k_B = mpf('8.617333e-5')  # eV/K
T_bio = mpf('310')  # K
k_BT = k_B * T_bio
lambda_rec_beta = exp(phi) / pi**2


def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║            THE RNA WORLD — DUAL-FUNCTION MOLECULE FROM GU                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    # -------------------------------------------------------------------------
    # PART 1: THE CHICKEN-AND-EGG PROBLEM
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 1: THE CHICKEN-AND-EGG PROBLEM                                         ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("DNA stores information but can't catalyze.")
    print("Proteins catalyze but can't template-replicate.")
    print("Which came first? Neither can exist without the other in modern cells.")
    print("RNA solves this: it can BOTH store information AND catalyze reactions.")
    print("This is the RNA world hypothesis.")
    print()

    # -------------------------------------------------------------------------
    # PART 2: RNA IN GU TERMS
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 2: RNA IN GU TERMS                                                     ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("RNA = ribose sugar + phosphate backbone + 4 bases (A, G, C, U).")
    print("Like DNA: bases are aromatic (pi-bonded, w >= 1).")
    print("Like DNA: bases can stack (nabla_theta != 0 in stacking columns).")
    print("Unlike DNA: single-stranded → can fold into complex 3D structures.")
    print()
    print("The 3D fold brings distant bases CLOSE together → aromatic residues cluster")
    print("→ local phase coupling CONCENTRATES.")
    print("This concentration of nabla_theta at the fold IS catalytic activity.")
    print()
    print("In GU: RNA is the MINIMUM molecule with THREE capabilities:")
    print("  1. Information (base sequence, sigma/H-bond channel)")
    print("  2. Memory (pi-stacking, theta/phase channel)")
    print("  3. Catalysis (3D fold concentrating nabla_theta)")
    print()

    # -------------------------------------------------------------------------
    # PART 3: RIBOZYMES — CATALYTIC RNA
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 3: RIBOZYMES — CATALYTIC RNA                                           ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("Known ribozymes: self-splicing introns (Group I, II), RNase P, hammerhead,")
    print("ribosome (peptidyl transferase).")
    print()
    print("The ribosome: THE most important ribozyme — translates RNA into protein.")
    print("  The catalytic core is RNA, NOT protein.")
    print("  This proves RNA came first: the translation machinery itself is an RNA enzyme.")
    print()
    print("Ribozyme rate enhancement: 10^3 to 10^11 (less than protein enzymes but sufficient).")
    print()
    print("In GU: ribozymes work by the same V_lock reshaping mechanism as protein enzymes")
    print("(Script 03), but using base stacking (aromatic) rather than amino acid side chains.")
    print()

    # -------------------------------------------------------------------------
    # PART 4: RNA STABILITY AND THE DNA TAKEOVER
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 4: RNA STABILITY AND THE DNA TAKEOVER                                  ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("RNA is LESS stable than DNA: 2'-OH group on ribose makes it susceptible to hydrolysis.")
    print("RNA half-life in water at 310 K: hours to days (depends on sequence).")
    print("DNA half-life: thousands to millions of years.")
    print()
    # RNA hydrolysis rate from V_lock barrier and Arrhenius: k = A * exp(-E_a / k_B*T)
    # Effective barrier ~0.7–1.1 eV (sequence/structure dependent); ~1.05 eV → ~1 h half-life at 310 K
    E_a_RNA_hydrolysis = mpf('1.05')  # eV (illustrative: gives order-of-magnitude hours)
    A_prefactor = mpf('1e13')  # /s typical attempt frequency
    k_hydrolysis = A_prefactor * exp(-E_a_RNA_hydrolysis / k_BT)
    half_life_s = ln(mpf('2')) / k_hydrolysis
    half_life_hours = half_life_s / mpf('3600')
    half_life_days = half_life_s / mpf('86400')
    print("  Compute: RNA hydrolysis rate from V_lock barrier and Arrhenius:")
    print(f"    k = A * exp(-E_a / k_B*T), E_a = {float(E_a_RNA_hydrolysis):.2f} eV, k_B*T = {float(k_BT):.4f} eV")
    print(f"    k ~ {float(k_hydrolysis):.2e} /s  →  half-life ~ {float(half_life_hours):.1f} h (~{float(half_life_days):.2f} days)")
    print()
    print("The RNA → DNA transition: when life needed LONGER-TERM information storage, DNA evolved.")
    print("  DNA = RNA minus the 2'-OH (deoxyribose) → dramatically more stable.")
    print("  The information function moved to DNA; the catalytic function moved to protein.")
    print("  RNA retained its role as INTERMEDIARY (mRNA, tRNA, rRNA).")
    print()

    # -------------------------------------------------------------------------
    # PART 5: RNA AS THE LOWEST-COST ENTRY POINT FOR LIFE
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 5: RNA AS THE LOWEST-COST ENTRY POINT FOR LIFE                          ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("To get life, you need: information + catalysis + replication.")
    print("With ONLY RNA: you get all three in one molecule type.")
    print("With DNA + protein: you need TWO molecule types AND a translation apparatus (ribosome).")
    print()
    print("RNA world is the CHEAPEST path: minimum molecular complexity for self-replication.")
    print("In GU: the RNA world minimizes the effective action — fewest molecular species,")
    print("simplest coupling.")
    print()
    print("The protocell (Script 06) starts with RNA in a lipid vesicle: the MINIMUM VIABLE CELL.")
    print()
    print("Key result: RNA is the lowest-cost entry to life in the Platonic Space because it is")
    print("the simplest molecule bridging information, memory, and catalysis.")
    print()

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  SUMMARY                                                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("The RNA world from GU connects to:")
    print("  • 24_DNA: same aromatic bases (A, G, C), pi-stacking and phase memory;")
    print("    RNA is the single-stranded, foldable precursor; DNA is the stable archive.")
    print("  • Script 03 (catalysis): ribozymes use V_lock reshaping via base stacking;")
    print("    same physics, different chemistry (ribose + bases vs amino acids).")
    print("  • Script 06 (protocell): the minimum viable cell is RNA inside a lipid vesicle;")
    print("    RNA provides information, memory, and catalysis in one molecule.")
    print()


if __name__ == '__main__':
    main()
