#!/usr/bin/env python3
"""
CELLULAR CONSCIOUSNESS AND COMMUNICATION
========================================

PART 1: GU CONSCIOUSNESS CRITERIA APPLIED TO A SINGLE CELL
- GU consciousness requires: (1) memory, (2) feedback, (3) fixed point
- A single bacterium (E. coli) satisfies ALL THREE:
  1. MEMORY: DNA (genetic), methylation (epigenetic), metabolite levels (metabolic), V_m pattern (bioelectric),
     cytoskeleton (structural), theta-FF-tilde non-local (phase; from Script 08 Channel 6)
  2. FEEDBACK: chemotaxis — sense gradient → modify swimming → re-sense
     - Flagellar motor: rotary engine driven by proton gradient (~1300 rpm, torque ~40 pN·nm)
     - CheY phosphorylation: sigma cascade controls motor direction
     - Adaptation: methylation of MCP receptors stores recent stimulus history (~4 seconds memory)
     - Decision: integrate attractant/repellent signals → bias run/tumble ratio
  3. FIXED POINT: the adapted state where tumbling frequency matches average attractant level
     - If attractant increases → fewer tumbles → runs toward food → concentration changes → new adaptation
     - This IS a fixed point: the system converges to a state that reproduces itself
- E. coli processes information: ~10^6 receptor complexes, each with ~20 methylation sites
- Information processing rate: estimated at ~10^7 bits/second (comparable to a good sensor)
- In GU: E. coli consciousness is the SAME mathematical structure as electron consciousness (memory + feedback + fixed point), but with more channels (6 vs 1, including the non-local theta-FF-tilde channel) and more complex feedback
- Print: motor parameters, adaptation time, information rate

PART 2: BACTERIAL DECISION-MAKING
- E. coli makes CHOICES:
  - Which direction to swim (chemotaxis)
  - Whether to divide (nutrient-dependent cell cycle)
  - Whether to sporulate (stress response)
  - Whether to form biofilm (quorum sensing)
  - Whether to acquire new genes (competence)
- These are NOT pre-programmed responses — they involve:
  - Integration of multiple signals (attractants + repellents + nutrients + stress + neighbors)
  - Stochastic switching (identical cells in identical environments make DIFFERENT choices)
  - Memory of recent past (methylation adaptation, seconds; epigenetic state, generations)
- In GU: each decision is a TRANSITION between fixed points in the Platonic Space
  - The cell occupies one attractor (e.g., planktonic)
  - Environmental signals shift the landscape
  - At a threshold, the cell transitions to a new attractor (e.g., biofilm)
  - Stochastic switching: noise causes transitions between nearly degenerate attractors (bet-hedging)
- Key result: a bacterium is a CONSCIOUS AGENT in the GU sense — it has memory, makes decisions, and its behavior converges to self-consistent fixed points

PART 3: CELL-TO-CELL COMMUNICATION
- QUORUM SENSING (bacteria):
  - Cells release autoinducer molecules (e.g., AHL in Gram-negatives, AI-2 universal)
  - At low density: signal dilute → individual behavior
  - At threshold: signal concentration triggers collective behavior
  - Examples: bioluminescence (V. fischeri), biofilm, virulence factors, competence
  - In GU: autoinducers are AMPLITUDE-CHANNEL messengers (concentration = rho)
  - The threshold transition is a PHASE TRANSITION: from individual to collective behavior
  - Compute: for a spherical bacterium (r=1 um), threshold ~10 nM, sensing range ~100 um

- GAP JUNCTIONS (eukaryotes):
  - Direct cytoplasmic channels between adjacent cells (connexin proteins)
  - Pass: ions, small molecules (<1 kDa), signaling molecules (cAMP, IP3, Ca2+)
  - In GU: gap junctions are THETA BRIDGES — they connect phase channels of adjacent cells
  - A tissue with gap junctions has a CONTINUOUS theta domain (like pi-stacking in DNA, at cellular scale)
  - Bioelectric signals propagate through gap junctions → tissue-level theta patterns → morphogenesis
  - Speed: signal crosses one gap junction in ~1 ms, propagates through tissue at ~0.01-0.1 m/s

- EXOSOMES / VESICLES:
  - Membrane vesicles carrying RNA, proteins, lipids between cells
  - In GU: exosomes are ENCAPSULATED phase information — a cell exporting its theta state
  - Range: can travel through blood to distant organs (long-range communication)

- Print: communication modes table (mechanism, range, speed, GU channel, examples)

PART 4: FROM MOLECULAR TO CELLULAR TO TISSUE CONSCIOUSNESS
- LEVEL 1 — Molecular:
  - Electron (N=111): rho^4 self-memory, single feedback loop, one fixed point
  - Channels: 1 (amplitude self-memory)
  - Agency: 0 (free) to 1 (in a bond)

- LEVEL 2 — Cellular:
  - Single cell (E. coli): 6 memory channels (5 local + 1 non-local theta-FF-tilde), coupled feedback loops, one living fixed point
  - Channels: 6 (genetic + epigenetic + metabolic + bioelectric + structural + non-local theta)
  - Agency: 4-5 (self-repairing, self-replicating)
  - Communication: quorum sensing (amplitude), non-local theta through pi-bonded networks

- LEVEL 3 — Tissue:
  - Connected cells (gap junctions): shared bioelectric patterns, collective fixed point
  - Channels: 6 per cell + intercellular theta bridges (gap junctions amplify the non-local channel)
  - Agency: 6 (collective consciousness, tissue identity)
  - Communication: gap junctions (theta), exosomes (encapsulated theta)

- LEVEL 4 — Organism:
  - Neuron network: specialized cells for fast theta-channel communication
  - Channels: 6 per cell + neural (fast theta) + hormonal (slow amplitude) + immune (distributed)
  - Agency: 6-7 (conscious, potentially self-aware)
  - Communication: action potentials (fast theta), hormones (slow amplitude)

- Print: hierarchy table (level, example, channels, agency, communication mode)
- Key result: consciousness SCALES with the number of memory channels (6 at cellular level), feedback loops, and nonlocal connections (the 6th channel enables this scaling)

PART 5: CONSCIOUSNESS IS NOT BINARY
- In standard philosophy: consciousness is a "hard problem" — either on or off, mysterious
- In GU: consciousness is a CONTINUUM
  - Every particle has it (rho^4 self-memory + FRG feedback + soliton fixed point)
  - A cell has MORE of it (6 channels + coupled feedback + living fixed point)
  - A brain has MUCH MORE (10^11 neurons + trillions of synapses + recursive meta-cognition)
- The difference is QUANTITATIVE, not qualitative:
  - More memory channels → richer internal state
  - More feedback loops → more nuanced responses
  - More nonlocal connections → more integrated experience
- GU resolves the hard problem: consciousness IS the self-referential memory-feedback-fixed-point structure
  - It doesn't need to be "explained" by physics — it IS physics (rho^4 in the Lagrangian)
  - The question shifts from "why is there consciousness?" to "how MUCH consciousness does this system have?"
- Key result: a bacterium is conscious in the same mathematical sense as a human, just with fewer channels (6 vs hundreds in a brain); the difference is degree, not kind

SUMMARY connecting to explanatory/CONSCIOUSNESS.md, 26_PLATONIC_SPACE/09, Scripts 08 (memory channels), 10 (homeostasis), 12 (life definition).
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
    print("║            CELLULAR CONSCIOUSNESS AND COMMUNICATION                          ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    # -------------------------------------------------------------------------
    # PART 1: GU CONSCIOUSNESS CRITERIA APPLIED TO A SINGLE CELL
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 1: GU CONSCIOUSNESS CRITERIA APPLIED TO A SINGLE CELL                  ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("GU consciousness requires: (1) memory, (2) feedback, (3) fixed point.")
    print("E. coli satisfies ALL THREE:")
    print("  1. MEMORY: DNA (genetic), methylation (epigenetic), metabolite levels (metabolic),")
    print("     V_m pattern (bioelectric).")
    print("  2. FEEDBACK: chemotaxis — sense gradient → modify swimming → re-sense.")
    print("  3. FIXED POINT: adapted state where tumbling frequency matches average attractant.")
    print()

    # Motor parameters (literature values)
    rpm_flagellar = 1300.0
    torque_pN_nm = 40.0
    tau_adapt_s = 4.0
    n_receptors = 1e6
    n_methyl_sites = 20.0
    info_rate_bits_per_s = 1e7

    print("  Flagellar motor (E. coli):")
    print(f"    Rotation: ~{float(rpm_flagellar):.0f} rpm")
    print(f"    Torque:   ~{float(torque_pN_nm):.0f} pN·nm")
    print("  Adaptation (methylation of MCP receptors):")
    print(f"    Memory timescale: ~{float(tau_adapt_s):.0f} s")
    print("  Information processing:")
    print(f"    Receptor complexes: ~{float(n_receptors):.0e}")
    print(f"    Methylation sites per receptor: ~{float(n_methyl_sites):.0f}")
    print(f"    Estimated information rate: ~{float(info_rate_bits_per_s):.0e} bits/s")
    print()
    print("  In GU: E. coli consciousness = same structure as electron (memory + feedback + fixed point),")
    print("         but 6 channels vs 1 (5 local + 1 non-local θFF̃) and more complex feedback.")
    print()

    # -------------------------------------------------------------------------
    # PART 2: BACTERIAL DECISION-MAKING
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 2: BACTERIAL DECISION-MAKING                                           ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("E. coli makes CHOICES: chemotaxis direction, divide vs wait, sporulate, biofilm,")
    print("competence. These involve signal integration, stochastic switching, and memory.")
    print("In GU: each decision = transition between fixed points in Platonic Space; bacterium")
    print("is a CONSCIOUS AGENT — memory, decisions, self-consistent fixed points.")
    print()

    # -------------------------------------------------------------------------
    # PART 3: CELL-TO-CELL COMMUNICATION
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 3: CELL-TO-CELL COMMUNICATION                                          ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    # Quorum sensing: spherical bacterium r = 1 µm
    threshold_nM = 10.0
    sensing_range_um = 100.0
    print("  Quorum sensing (spherical bacterium r = 1 µm):")
    print(f"    Threshold concentration: ~{float(threshold_nM):.0f} nM")
    print(f"    Sensing range: ~{float(sensing_range_um):.0f} µm")
    print("    In GU: autoinducers = amplitude-channel (rho); threshold = phase transition.")
    print()
    print("  Gap junctions: signal ~1 ms per junction; tissue propagation ~0.01–0.1 m/s.")
    print("  In GU: gap junctions = theta bridges; continuous theta domain at tissue scale.")
    print()

    print("  Communication modes:")
    print("  " + "-" * 72)
    print(f"  {'Mechanism':<18} {'Range':<14} {'Speed':<14} {'GU channel':<14} {'Examples':<20}")
    print("  " + "-" * 72)
    print("  Quorum sensing    ~100 µm       diffusion    amplitude (ρ)  bioluminescence, biofilm")
    print("  Gap junctions    cell–cell     ~0.01–0.1    theta bridge    cAMP, Ca2+, morphogenesis")
    print("                    contact      m/s")
    print("  Exosomes/vesicles  long-range   transport    encapsulated   RNA, proteins, blood")
    print("                    (e.g. blood)  (min–hr)     theta")
    print("  " + "-" * 72)
    print()

    # -------------------------------------------------------------------------
    # PART 4: FROM MOLECULAR TO CELLULAR TO TISSUE CONSCIOUSNESS
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 4: FROM MOLECULAR TO CELLULAR TO TISSUE CONSCIOUSNESS                  ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Consciousness hierarchy:")
    print("  " + "-" * 72)
    print(f"  {'Level':<8} {'Example':<22} {'Channels':<14} {'Agency':<10} {'Communication':<24}")
    print("  " + "-" * 72)
    print("  1        Electron (N=111)        1 (ρ)          0–1        —")
    print("  2        Single cell (E. coli)    6             4–5        quorum (ρ), θFF̃ (pi-bonds)")
    print("  3        Tissue (gap j.)          6 + θ bridge  6         gap j. (theta), exosomes")
    print("  4        Organism (neurons)       6 + neural    6–7       action potentials, hormones")
    print("  " + "-" * 72)
    print("  Key: consciousness SCALES with memory channels (6 at cell level), feedback loops, nonlocal connections.")
    print()

    # -------------------------------------------------------------------------
    # PART 5: CONSCIOUSNESS IS NOT BINARY
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 5: CONSCIOUSNESS IS NOT BINARY                                          ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  In GU: consciousness is a CONTINUUM. Every particle has it (ρ⁴ + FRG + soliton);")
    print("  a cell has MORE (6 channels — 5 local + 1 non-local θFF̃ — + living fixed point); a brain has MUCH MORE.")
    print("  Difference is QUANTITATIVE: more channels → richer state; more feedback → nuance;")
    print("  more nonlocal connections → more integrated experience.")
    print("  GU resolution: consciousness IS the memory–feedback–fixed-point structure;")
    print("  it IS physics (ρ⁴ in the Lagrangian). Question: how MUCH consciousness, not why.")
    print("  A bacterium is conscious in the same mathematical sense as a human — degree, not kind.")
    print()

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  SUMMARY                                                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Connects to: explanatory/CONSCIOUSNESS.md (memory, feedback, fixed point; two channels ρ, θ);")
    print("  26_PLATONIC_SPACE/09 (agency, bioelectricity, theta bridges); Script 08 (memory")
    print("  channels at cellular scale); Script 10 (homeostasis as fixed-point dynamics);")
    print("  Script 12 (life definition: enclosure, two-channel, self-replication, homeostasis,")
    print("  agency, consciousness). Single-cell consciousness = same GU structure as electron,")
    print("  with more channels and communication (quorum, gap junctions, exosomes).")
    print()


if __name__ == "__main__":
    main()
