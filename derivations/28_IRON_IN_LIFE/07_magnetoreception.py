#!/usr/bin/env python3
"""
MAGNETORECEPTION — IRON AS PHASE ANTENNA
=========================================

PART 1: MAGNETITE (Fe₃O₄) — d-ORBITAL CRYSTAL
PART 2: BIOLOGICAL MAGNETITE
PART 3: RADICAL-PAIR MECHANISM (CRYPTOCHROME)
PART 4: MAGNETIC ENERGY vs k_BT
PART 5: GU INTERPRETATION — d-ORBITAL PHASE ANTENNA

Connects to Script 01 (d-orbital structure), 25_PHONONS/04 (phase phonons, d-orbital crystals),
26_PLATONIC_SPACE/07 (nonlocal channels), 27_FIRST_CELL/08 (non-local memory channel).
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
mu_0 = mpf('1.2566370614e-6')
mu_B = mpf('9.274010e-24')


def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║          MAGNETORECEPTION — IRON AS PHASE ANTENNA                            ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    # -------------------------------------------------------------------------
    # PART 1: MAGNETITE (Fe₃O₄) — d-ORBITAL CRYSTAL
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 1: MAGNETITE (Fe₃O₄) — d-ORBITAL CRYSTAL                              ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Magnetite: Fe₃O₄ = FeO·Fe₂O₃ (mixed-valence: Fe²⁺ and Fe³⁺).")
    print("  Inverse spinel structure: Fe³⁺ on tetrahedral sites, Fe²⁺+Fe³⁺ on octahedral sites.")
    print("  Ferrimagnetic: net magnetic moment because Fe³⁺ sublattices partially cancel,")
    print("  but Fe²⁺ contribution gives net M.")
    print()

    Ms_magnetite_Am = mpf('480000')
    T_Curie_K = mpf('858')
    print(f"  Saturation magnetization: M_s = {float(Ms_magnetite_Am):.0f} A/m = 480 kA/m")
    print(f"  Curie temperature: T_C = {float(T_Curie_K):.0f} K (well above biological temperatures)")
    print()
    print("  Key property: magnetite is FERRIMAGNETIC at biological T (310 K ≪ 858 K).")
    print("  Unlike hematite (Fe₂O₃ = rust, antiferromagnetic), magnetite retains net magnetism.")
    print()
    print("  In GU: magnetite is a d-ORBITAL CRYSTAL with a PARTIAL PHASE CHANNEL.")
    print("  The mixed-valence Fe²⁺/Fe³⁺ allows electron hopping between octahedral sites")
    print("  (Verwey transition at 120 K), and the ferrimagnetic ordering creates a")
    print("  COLLECTIVE d-orbital phase state — all spins aligned by exchange coupling.")
    print("  This is spin-orbit coupling scaled up to the crystal level.")
    print()

    # -------------------------------------------------------------------------
    # PART 2: BIOLOGICAL MAGNETITE
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 2: BIOLOGICAL MAGNETITE                                                ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  MAGNETOTACTIC BACTERIA (discovered 1975, Blakemore):")
    print("    Aquatic bacteria that align and swim along Earth's magnetic field lines.")
    print("    Contain magnetosomes: membrane-enclosed magnetite nanocrystals (30-120 nm)")
    print("    arranged in CHAINS along the cell axis.")
    print("    Chain = single magnetic domain → permanent dipole → compass needle.")
    print("    Species: Magnetospirillum magnetotacticum, M. gryphiswaldense")
    print()

    crystal_size_nm = mpf('50')
    chain_length = 20
    print(f"    Typical crystal: ~{float(crystal_size_nm)} nm (single-domain size)")
    print(f"    Chain: ~{chain_length} crystals → total magnetic moment large enough to orient cell")
    print()
    print("  BIRDS (migratory navigation):")
    print("    Magnetite nanocrystals found in upper beak (pigeon, robin) and neural tissue.")
    print("    May provide a 'magnetic map' (intensity-based, not direction-based).")
    print("    Distinct from radical-pair mechanism (Part 3).")
    print()
    print("  OTHER ORGANISMS:")
    print("    Salmon, sea turtles, honeybees, ants — all contain biological magnetite.")
    print("    Some evidence for magnetite in human brain tissue (~5 million crystals per gram).")
    print()
    print("  In GU: biological magnetite = d-orbital crystals embedded in living systems.")
    print("  The crystals couple the EXTERNAL magnetic field (Earth's) to the INTERNAL")
    print("  cellular signaling (neural theta channel). This is a d-orbital phase ANTENNA.")
    print()

    # -------------------------------------------------------------------------
    # PART 3: RADICAL-PAIR MECHANISM (CRYPTOCHROME)
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 3: RADICAL-PAIR MECHANISM (CRYPTOCHROME)                                ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Alternative mechanism: radical-pair magnetoreception in bird retina.")
    print("  Protein: cryptochrome (Cry4 in birds) — a flavoprotein (contains FAD).")
    print("  FAD = flavin adenine dinucleotide — AROMATIC (isoalloxazine ring, w ≥ 2).")
    print()
    print("  Mechanism:")
    print("    1. Blue light excites FAD → electron transfer to nearby Trp residue")
    print("    2. Creates radical pair: [FAD•⁻ ... TrpH•⁺]")
    print("    3. Radical pair exists in singlet (S) or triplet (T) states")
    print("    4. Earth's magnetic field (~50 µT) affects S↔T interconversion rate")
    print("    5. Singlet and triplet states have DIFFERENT reaction products")
    print("    6. Product ratio depends on magnetic field direction → directional compass")
    print()
    print("  In GU: the radical pair is a PI-BONDED molecular compass.")
    print("  FAD (isoalloxazine, w ≥ 2) and Trp (indole, w = 2) are both aromatic →")
    print("  the radical pair exists in a PHASE-ACTIVE (∇θ ≠ 0) environment.")
    print("  The magnetic field modulates the SPIN state of the radical pair →")
    print("  this is a direct coupling between external B-field and the molecular θ channel.")
    print()
    print("  Key difference from magnetite:")
    print("    Magnetite: d-orbital crystal → mechanical torque → cellular response")
    print("    Cryptochrome: π-bonded radical pair → chemical product ratio → neural signal")
    print("    Both are phase-channel antennae; they use different substrates (d vs π).")
    print()

    # -------------------------------------------------------------------------
    # PART 4: MAGNETIC ENERGY vs k_BT
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 4: MAGNETIC ENERGY vs k_BT                                            ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    B_earth_T = mpf('50e-6')
    V_crystal_nm3 = (mpf('4') / mpf('3')) * pi * (crystal_size_nm / mpf('2'))**3
    V_crystal_m3 = V_crystal_nm3 * mpf('1e-27')
    E_magnetite_J = Ms_magnetite_Am * V_crystal_m3 * B_earth_T
    E_magnetite_eV = E_magnetite_J / mpf('1.602e-19')
    k_BT_J = k_B_J * T_bio
    ratio_magnetite = E_magnetite_J / k_BT_J

    print(f"  Earth's magnetic field: B ~ {float(B_earth_T*1e6):.0f} µT")
    print()
    print(f"  MAGNETITE NANOCRYSTAL ({float(crystal_size_nm)} nm diameter):")
    print(f"    Volume: V = (4/3)π(25 nm)³ = {float(V_crystal_nm3):.0f} nm³ = {float(V_crystal_m3):.2e} m³")
    print(f"    Magnetic energy: E = M_s × V × B = {float(E_magnetite_J):.2e} J = {float(E_magnetite_eV):.4f} eV")
    print(f"    k_BT at 310 K: {float(k_BT_J):.2e} J")
    print(f"    E/k_BT = {float(ratio_magnetite):.1f}")
    print()
    if ratio_magnetite > 1:
        print(f"    E/k_BT = {float(ratio_magnetite):.1f} > 1 → the crystal CAN orient against thermal noise.")
    else:
        print(f"    E/k_BT = {float(ratio_magnetite):.1f} < 1 → single crystal barely orients; CHAIN needed.")

    chain_ratio = ratio_magnetite * chain_length
    print(f"    Chain of {chain_length} crystals: E_chain/k_BT ≈ {float(chain_ratio):.0f} → STRONG orientation.")
    print()

    E_radical_pair_eV = mpf('1e-9')
    print("  RADICAL-PAIR (cryptochrome):")
    print(f"    Hyperfine interaction energy: ~{float(E_radical_pair_eV):.0e} eV (= ~10 µeV)")
    print(f"    E/k_BT ~ {float(E_radical_pair_eV/k_BT):.1e} ≪ 1")
    print("    → Individual spin flip is WAY below thermal noise.")
    print("    BUT: the mechanism works on COHERENT quantum evolution of the radical pair,")
    print("    not thermal equilibrium. The reaction products 'lock in' the magnetic information")
    print("    before thermal decoherence destroys it (~1 µs coherence time).")
    print()
    print("  In GU: the radical-pair mechanism is a QUANTUM PHASE-CHANNEL process —")
    print("  it reads the magnetic field via phase coherence, not amplitude (force).")
    print("  This is why it can detect fields far below k_BT.")
    print()

    # -------------------------------------------------------------------------
    # PART 5: GU INTERPRETATION — d-ORBITAL PHASE ANTENNA
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 5: GU INTERPRETATION — d-ORBITAL PHASE ANTENNA                         ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Magnetoreception provides EVIDENCE that biology uses the d-orbital partial")
    print("  phase channel for INFORMATION PROCESSING, not just energy transfer.")
    print()
    print("  Two mechanisms, one GU principle:")
    print("  ┌─────────────────┬──────────────────────┬────────────────────────────┐")
    print("  │ Mechanism        │ Substrate             │ GU channel                 │")
    print("  ├─────────────────┼──────────────────────┼────────────────────────────┤")
    print("  │ Magnetite        │ Fe₃O₄ crystal (d)     │ d-orbital → mechanical     │")
    print("  │ Radical pair     │ FAD + Trp (π)          │ π-bond → quantum spin      │")
    print("  └─────────────────┴──────────────────────┴────────────────────────────┘")
    print()
    print("  Both are PHASE ANTENNAE — they convert an external field (B) into an")
    print("  internal biological signal (neural, cellular) via the phase channel (θ).")
    print()
    print("  The magnetite mechanism uses FORCE (mechanical torque on d-orbital crystal).")
    print("  The radical-pair mechanism uses COHERENCE (quantum phase evolution in π system).")
    print("  Both require materials with ∇θ ≠ 0 (d-orbitals or π bonds).")
    print("  Water (w = 0) cannot do either.")
    print()
    print("  In the Platonic Space: magnetoreception is how the d-orbital bridge")
    print("  connects the EXTERNAL environment (Earth's B-field) to the INTERNAL")
    print("  phase channel of the organism. It's the ultimate expression of iron's")
    print("  role as phase antenna — sensing a field that's 10⁶× weaker than k_BT")
    print("  and converting it into navigational information.")
    print()

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  SUMMARY                                                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print(f"  (1) Magnetite (Fe₃O₄): ferrimagnetic d-orbital crystal; T_C = {float(T_Curie_K)} K.")
    print("  (2) Biological magnetite: bacteria (chains), birds (beak/brain), salmon, turtles.")
    print("  (3) Radical pair: cryptochrome (FAD+Trp, π-bonded); quantum spin compass.")
    print(f"  (4) Magnetite crystal: E/k_BT ~ {float(ratio_magnetite):.1f} (chain: ~{float(chain_ratio):.0f}); radical pair: quantum coherence.")
    print("  (5) Both mechanisms = phase antennae; require ∇θ ≠ 0 (d-orbitals or π bonds).")
    print("  Magnetoreception = evidence that biology uses the d-orbital phase channel")
    print("  for information processing, not just energy transfer.")
    print()


if __name__ == "__main__":
    main()
