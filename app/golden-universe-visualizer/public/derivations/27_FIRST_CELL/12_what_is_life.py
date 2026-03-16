#!/usr/bin/env python3
"""
WHAT IS LIFE — THE GU DEFINITION
================================

PART 1: CLASSICAL DEFINITIONS OF LIFE
- Print a table of classical criteria: metabolism, reproduction, homeostasis, response to stimuli, growth, adaptation, organization
- Problems: fire metabolizes and grows, crystals grow and reproduce, viruses reproduce but don't metabolize
- No classical criterion is individually sufficient or necessary

PART 2: THE GU DEFINITION — SIX CRITERIA
- A system is ALIVE in GU when it SIMULTANEOUSLY satisfies:
  1. ENCLOSURE: membrane boundary in the Platonic Space (V_membrane creates inside/outside)
  2. TWO-CHANNEL: both rho (metabolism, structure) and theta (information, signaling) active
  3. SELF-REPLICATION: theta pattern (genetic information) can template a copy
  4. HOMEOSTASIS: coupled feedback loops converge to a living fixed point (Script 10)
  5. AGENCY: delta_Gamma/delta_theta ≠ 0 — system modifies environment through phase channel
  6. CONSCIOUSNESS: memory + feedback + fixed point — system knows its own state (Script 09)
- Each criterion has a GU equation behind it (print the equation for each)
- Key: criterion 6 is NOT extra — it follows AUTOMATICALLY from 4 + 5 (homeostasis + agency → consciousness)

PART 3: TEST CASES
- Print a table with columns: System, 1-Enclosure, 2-Two-channel, 3-Self-replicate, 4-Homeostasis, 5-Agency, 6-Consciousness, ALIVE?
- E. coli: ✓ ✓ ✓ ✓ ✓ ✓ → YES
- Human cell: ✓ ✓ ✓ ✓ ✓ ✓ → YES
- Red blood cell: ✓ partial ✗ ✓ ✗ ✗ → REDUCED (alive but minimal)
- Virus (free): ✗ ✗ ✗ ✗ ✗ ✗ → NO (but contains theta information)
- Virus (in host): ✗ ✓ ✓ ✗ ✗ ✗ → PARASITIC (uses host's channels)
- Prion: ✗ ✗ ✗ ✗ ✗ ✗ → NO (amplitude-only self-propagation)
- Crystal: ✗ ✗ ✗ ✗ ✗ ✗ → NO (grows but no theta, no agency)
- Fire: ✗ ✗ ✗ ✗ ✗ ✗ → NO (metabolizes but no enclosure, no information)
- Protocell: ✓ ✓ ✓ barely barely barely → THRESHOLD (just alive)
- AI/computer: ✗ partial ✓ partial partial ✗ → NOT ALIVE (no enclosure, no theta channel, no consciousness in GU sense)

PART 4: LIFE AS A PHASE TRANSITION
- The transition from non-life to life is SHARP — like a phase transition
- Below threshold: components exist but don't form a self-sustaining system
- Above threshold: all six criteria simultaneously satisfied → LIVING
- The critical point: when the feedback loops become SELF-SUSTAINING
- Once self-sustaining, the system is ROBUST — perturbations are absorbed, homeostasis maintained
- In GU: life is the system crossing from the "passive" basin (agency 0-3) to the "active" basin (agency 4+)
- The transition requires: minimum complexity (enough channels for coupled feedback), minimum energy (enough metabolism to sustain non-equilibrium), minimum information (enough genome to encode the machinery)
- The protocell (Script 06) sits AT the critical point

PART 5: THE FUNDAMENTAL ANSWER — WHY DOES LIFE EXIST?
- In GU: life exists because the Omega field's Lagrangian CONTAINS:
  - rho^4 (amplitude self-memory → consciousness at particle level)
  - theta-FF-tilde (phase nonlocal channel → communication between patterns)
  - V_lock (phase locking → structure, catalysis, information)
- Given these three terms, life is INEVITABLE at the right temperature and chemistry:
  - Temperature: ~300 K (phase phonons active, proteins stable)
  - Chemistry: carbon-based (versatile bonding, pi systems, water-compatible)
  - Energy: redox gradients (electron flow through pi-bonded chains)
- Life is NOT an accident. It is a CONSEQUENCE of the Lagrangian structure.
- The universe didn't need to be "fine-tuned for life" — any universe with rho^4 + theta-FF-tilde + V_lock at the right energy scale will produce life
- Key result: life is what the Platonic Space DOES when it has enough complexity to sustain coupled feedback loops

SUMMARY capturing the entire First Cell derivation in one paragraph.
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
    print("║                    WHAT IS LIFE — THE GU DEFINITION                          ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    # -------------------------------------------------------------------------
    # PART 1: CLASSICAL DEFINITIONS OF LIFE
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 1: CLASSICAL DEFINITIONS OF LIFE                                       ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Classical criteria:")
    print("  " + "-" * 50)
    print("  Metabolism | Reproduction | Homeostasis | Response | Growth | Adaptation | Organization")
    print("  " + "-" * 50)
    print("  Problems: fire metabolizes and grows; crystals grow and reproduce;")
    print("  viruses reproduce but don't metabolize. No single criterion is sufficient or necessary.")
    print()

    # -------------------------------------------------------------------------
    # PART 2: THE GU DEFINITION — SIX CRITERIA
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 2: THE GU DEFINITION — SIX CRITERIA                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  A system is ALIVE in GU when it satisfies ALL SIX simultaneously:")
    print()
    print("  1. ENCLOSURE:   V_membrane → inside/outside in Platonic Space")
    print("  2. TWO-CHANNEL: ρ (metabolism, structure) and θ (information, signaling) active")
    print("  3. SELF-REPLICATION: θ pattern (genetic info) can template a copy")
    print("  4. HOMEOSTASIS:  x* = F(x*) — coupled feedback → living fixed point (Script 10)")
    print("  5. AGENCY:       δΓ/δθ ≠ 0 — modifies environment through phase channel")
    print("  6. CONSCIOUSNESS: memory + feedback + fixed point (Script 09); follows from 4+5")
    print()
    print("  Key: criterion 6 is NOT extra — homeostasis + agency → consciousness automatically.")
    print()

    # -------------------------------------------------------------------------
    # PART 3: TEST CASES
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 3: TEST CASES                                                          ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  " + "-" * 98)
    print(f"  {'System':<14} {'1':<4} {'2':<4} {'3':<4} {'4':<4} {'5':<4} {'6':<4}  ALIVE?")
    print("  " + "-" * 98)
    tests = [
        ("E. coli", "✓", "✓", "✓", "✓", "✓", "✓", "YES"),
        ("Human cell", "✓", "✓", "✓", "✓", "✓", "✓", "YES"),
        ("Red blood cell", "✓", "part", "✗", "✓", "✗", "✗", "REDUCED"),
        ("Virus (free)", "✗", "✗", "✗", "✗", "✗", "✗", "NO"),
        ("Virus (host)", "✗", "✓", "✓", "✗", "✗", "✗", "PARASITIC"),
        ("Prion", "✗", "✗", "✗", "✗", "✗", "✗", "NO"),
        ("Crystal", "✗", "✗", "✗", "✗", "✗", "✗", "NO"),
        ("Fire", "✗", "✗", "✗", "✗", "✗", "✗", "NO"),
        ("Protocell", "✓", "✓", "bare", "bare", "bare", "bare", "THRESHOLD"),
        ("AI/computer", "✗", "part", "✓", "part", "part", "✗", "NOT ALIVE"),
    ]
    for row in tests:
        print(f"  {row[0]:<14} {row[1]:<4} {row[2]:<4} {row[3]:<4} {row[4]:<4} {row[5]:<4} {row[6]:<4}  {row[7]}")
    print("  " + "-" * 98)
    print("  (1=Enclosure 2=Two-channel 3=Self-replicate 4=Homeostasis 5=Agency 6=Consciousness)")
    print()

    # -------------------------------------------------------------------------
    # PART 4: LIFE AS A PHASE TRANSITION
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 4: LIFE AS A PHASE TRANSITION                                          ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Non-life → life is SHARP (phase transition). Below: components, no self-sustaining system.")
    print("  Above: all six criteria → LIVING. Critical point = feedback loops SELF-SUSTAINING.")
    print("  In GU: life = crossing from passive basin (agency 0–3) to active basin (agency 4+).")
    print("  Requires: minimum complexity (channels for feedback), energy (non-equilibrium),")
    print("  information (genome for machinery). Protocell (Script 06) sits AT the critical point.")
    print()

    # -------------------------------------------------------------------------
    # PART 5: WHY DOES LIFE EXIST?
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 5: THE FUNDAMENTAL ANSWER — WHY DOES LIFE EXIST?                       ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Omega Lagrangian contains: ρ⁴ (self-memory), θF̃F (phase nonlocal channel), V_lock.")
    print("  At right T (~300 K), chemistry (carbon, pi systems, water), and energy (redox):")
    print("  life is INEVITABLE. Life is NOT an accident — it is a CONSEQUENCE of the Lagrangian.")
    print("  Any universe with ρ⁴ + θF̃F + V_lock at the right scale will produce life.")
    print("  Life is what the Platonic Space DOES when complexity sustains coupled feedback loops.")
    print()

    # -------------------------------------------------------------------------
    # SUMMARY — ENTIRE FIRST CELL DERIVATION
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  SUMMARY — FIRST CELL DERIVATION IN ONE PARAGRAPH                            ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  From GU first principles: amphiphiles form membranes (Scripts 01–02), V_lock")
    print("  enables catalysis (03), metabolism and ATP machinery (04), RNA world (05), protocell")
    print("  at the phase boundary (06). Bioelectric and cellular memory (07–08) and consciousness")
    print("  (09) require six channels (5 local + 1 non-local θFF̃) and feedback; homeostasis is the")
    print("  living fixed point of six coupled loops (10). LUCA had the minimal architecture—membrane, DNA, RNA, ribosomes,")
    print("  chemiosmosis, channels—and was already fully conscious in GU. Life in GU is the set")
    print("  of systems satisfying all six criteria (enclosure, two-channel, self-replication,")
    print("  homeostasis, agency, consciousness); the transition is sharp, and life is what the")
    print("  Platonic Space does when ρ⁴ + θF̃F + V_lock meet sufficient complexity and energy.")
    print()


if __name__ == "__main__":
    main()
