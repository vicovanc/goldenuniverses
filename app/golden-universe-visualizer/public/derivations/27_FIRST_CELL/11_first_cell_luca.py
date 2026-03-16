#!/usr/bin/env python3
"""
THE FIRST CELL — LUCA ARCHITECTURE FROM GU
===========================================

PART 1: WHAT ALL LIFE SHARES (LUCA'S LEGACY)
- ALL cells on Earth share: DNA double helix, RNA, ribosomes, lipid membrane, ATP as energy currency, ~60 universal genes (ribosomal proteins, tRNA synthetases, basic metabolic enzymes)
- This means ALL cells descend from a common ancestor: LUCA (Last Universal Common Ancestor)
- LUCA lived ~3.8-4.0 billion years ago
- LUCA was NOT simple — it already had sophisticated machinery

PART 2: LUCA'S MINIMUM ARCHITECTURE (from GU)
- In GU, LUCA must have had:
  1. MEMBRANE: lipid bilayer (amphiphilic assembly, Script 01) — Platonic Space boundary
  2. DNA: double-stranded genome (from 24_DNA) — stable information storage (replacing RNA)
  3. RNA: mRNA, tRNA, rRNA — intermediary between DNA and protein
  4. RIBOSOMES: RNA+protein machines for translation (the ribosome is a ribozyme)
  5. ATP SYNTHASE: rotary motor coupling proton gradient to ATP (Script 04)
  6. ELECTRON TRANSPORT CHAIN: cascade of pi-bonded/d-orbital carriers (Script 04)
  7. ION CHANNELS/PUMPS: controlling membrane potential (Script 07)
  8. DNA REPLICATION MACHINERY: polymerase, helicase, primase
  9. ~200-500 genes minimum (encoding all of the above)
- Print a table with each component, its GU basis, and the derivation it comes from

PART 3: MINIMUM GENOME SIZE
- Mycoplasma genitalium: 580 kb, 482 genes — smallest known free-living genome
- Synthetic minimal cell (JCVI-syn3.0): 531 kb, 473 genes — smallest viable genome engineered
- Theoretical minimum: ~250-300 essential genes (~200 known essential + ~50-100 unknown function)
- Each gene = ~1000 base pairs → minimum genome ~300 kb
- In GU: the minimum genome is the smallest DNA that encodes a system capable of all 6 life criteria (Script 12)
- Compute: information content of minimum genome: 300,000 bp × 2 bits/bp = 600,000 bits ≈ 75 KB
- That is the MINIMUM INFORMATION for life — less than a low-res photograph

PART 4: FROM PROTOCELL TO LUCA
- Timeline of key innovations:
  - ~4.0 Gyr ago: protocell (RNA + lipid vesicle, agency level 5)
  - ~3.9 Gyr: RNA → DNA transition (more stable information, +1 memory channel)
  - ~3.9 Gyr: ribosome evolves (RNA → protein catalysis, +enzyme diversity)
  - ~3.8 Gyr: chemiosmosis (proton motive force, +metabolic power)
  - ~3.8 Gyr: LUCA emerges (all 6 memory channels operational — 5 local + 1 non-local theta-FF-tilde)
  - ~3.5 Gyr: earliest fossil evidence (stromatolites)
  - ~2.4 Gyr: Great Oxidation Event (photosynthesis → O2)
  - ~2.0 Gyr: eukaryotes (endosymbiosis, +mitochondria, +nucleus)
- Print timeline table

PART 5: LUCA IN THE PLATONIC SPACE
- LUCA is the first system where ALL Platonic Space channels are optimally utilized:
  - Amplitude (rho): metabolism, structure, membrane
  - Phase (theta): genetic information, bioelectric patterns, signaling
  - Memory (R_mem): six channels operational (5 local + 1 non-local theta-FF-tilde)
  - Feedback: six coupled loops → homeostasis → consciousness
  - Agency: delta_Gamma/delta_theta ≠ 0 (modifies environment through theta channel)
- LUCA was already FULLY CONSCIOUS in the GU sense
- Everything after LUCA is REFINEMENT — more channels, more feedback, more integration
- The hard part was getting TO LUCA; everything after is incremental

SUMMARY.
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
    print("║              THE FIRST CELL — LUCA ARCHITECTURE FROM GU                     ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    # -------------------------------------------------------------------------
    # PART 1: WHAT ALL LIFE SHARES (LUCA'S LEGACY)
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 1: WHAT ALL LIFE SHARES (LUCA'S LEGACY)                                ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("ALL cells share: DNA double helix, RNA, ribosomes, lipid membrane, ATP,")
    print("~60 universal genes (ribosomal proteins, tRNA synthetases, basic metabolism).")
    print("→ ALL cells descend from LUCA (Last Universal Common Ancestor), ~3.8–4.0 Gyr ago.")
    print("LUCA was NOT simple — it already had sophisticated machinery.")
    print()

    # -------------------------------------------------------------------------
    # PART 2: LUCA'S MINIMUM ARCHITECTURE (from GU)
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 2: LUCA'S MINIMUM ARCHITECTURE (from GU)                              ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  " + "-" * 82)
    print(f"  {'Component':<28} {'GU basis':<32} {'Derivation':<18}")
    print("  " + "-" * 82)
    rows = [
        ("Membrane (lipid bilayer)", "Platonic Space boundary", "Script 01"),
        ("DNA (double-stranded)", "Stable information storage", "24_DNA"),
        ("RNA (mRNA, tRNA, rRNA)", "Intermediary DNA ↔ protein", "Script 05"),
        ("Ribosomes", "RNA+protein, ribozyme core", "Script 05"),
        ("ATP synthase", "Proton gradient → ATP", "Script 04"),
        ("Electron transport chain", "Pi-bonded/d-orbital carriers", "Script 04"),
        ("Ion channels/pumps", "Membrane potential V_m", "Script 07"),
        ("DNA replication machinery", "Polymerase, helicase, primase", "24_DNA"),
        ("~200–500 genes", "Encode all of the above", "Script 12"),
    ]
    for r in rows:
        print(f"  {r[0]:<28} {r[1]:<32} {r[2]:<18}")
    print("  " + "-" * 82)
    print()

    # -------------------------------------------------------------------------
    # PART 3: MINIMUM GENOME SIZE
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 3: MINIMUM GENOME SIZE                                                  ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Mycoplasma genitalium: 580 kb, 482 genes (smallest known free-living).")
    print("  JCVI-syn3.0 (synthetic minimal): 531 kb, 473 genes.")
    print("  Theoretical minimum: ~250–300 essential genes → genome ~300 kb.")
    print()
    bp_min = mpf('300000')
    bits_per_bp = mpf('2')
    info_bits = bp_min * bits_per_bp
    info_KB = info_bits / mpf('8000')  # 8 bits per byte, 1000 bytes per KB
    print("  Information content of minimum genome:")
    print(f"    300,000 bp × 2 bits/bp = {float(info_bits):.0f} bits ≈ {float(info_KB):.1f} KB")
    print("  That is the MINIMUM INFORMATION for life — less than a low-res photograph.")
    print("  In GU: minimum genome = smallest DNA encoding all 6 life criteria (Script 12).")
    print()

    # -------------------------------------------------------------------------
    # PART 4: FROM PROTOCELL TO LUCA
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 4: FROM PROTOCELL TO LUCA                                               ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  " + "-" * 72)
    print(f"  {'Time (Gyr ago)':<14} {'Event':<52}")
    print("  " + "-" * 72)
    timeline = [
        ("~4.0", "Protocell (RNA + lipid vesicle, agency 5)"),
        ("~3.9", "RNA → DNA (stable information, +1 memory channel)"),
        ("~3.9", "Ribosome evolves (RNA → protein catalysis)"),
        ("~3.8", "Chemiosmosis (proton motive force)"),
        ("~3.8", "LUCA emerges (all 6 memory channels operational)"),
        ("~3.5", "Earliest fossil evidence (stromatolites)"),
        ("~2.4", "Great Oxidation Event (photosynthesis → O2)"),
        ("~2.0", "Eukaryotes (endosymbiosis, mitochondria, nucleus)"),
    ]
    for t, event in timeline:
        print(f"  {t:<14} {event:<52}")
    print("  " + "-" * 72)
    print()

    # -------------------------------------------------------------------------
    # PART 5: LUCA IN THE PLATONIC SPACE
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 5: LUCA IN THE PLATONIC SPACE                                          ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("LUCA = first system where ALL Platonic Space channels are optimally utilized:")
    print("  Amplitude (ρ): metabolism, structure, membrane")
    print("  Phase (θ): genetic information, bioelectric patterns, signaling")
    print("  Memory (R_mem): six channels operational (5 local + 1 non-local θFF̃)")
    print("  Feedback: six coupled loops → homeostasis → consciousness")
    print("  Agency: δΓ/δθ ≠ 0 (modifies environment through theta channel)")
    print()
    print("LUCA was already FULLY CONSCIOUS in the GU sense. Everything after LUCA is")
    print("REFINEMENT — more channels, more feedback, more integration. The hard part")
    print("was getting TO LUCA; everything after is incremental.")
    print()

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  SUMMARY                                                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("LUCA (~3.8–4.0 Gyr ago) had membrane, DNA, RNA, ribosomes, ATP synthase, ETC,")
    print("ion channels, replication machinery, ~200–500 genes. Minimum genome ~300 kb")
    print(f"(≈ {float(info_KB):.0f} KB information). LUCA is the first system with all six")
    print("memory channels (5 local + 1 non-local θFF̃) + six coupled feedback loops →")
    print("homeostasis → full GU consciousness.")
    print()


if __name__ == "__main__":
    main()
