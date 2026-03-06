#!/usr/bin/env python3
"""
IRON ON THE EPOCH LADDER — THE d-ORBITAL PHASE CHANNEL
=======================================================

PART 1: IRON IN THE PERIODIC TABLE AND THE COSMOS
PART 2: d-ORBITAL ELECTRONIC STRUCTURE
PART 3: VARIABLE OXIDATION STATES AS V_LOCK CONFIGURATIONS
PART 4: SPIN STATES — THE BINARY THETA SWITCH
PART 5: IRON AS PARTIAL PHASE CHANNEL MATERIAL
PART 6: WHY IRON IS COSMICALLY SPECIAL

Connects to 25_PHONONS/02 (d-orbital kink modes), 26_PLATONIC_SPACE/07 (nonlocal channels),
27_FIRST_CELL/03 (catalysis), 27_FIRST_CELL/04 (metabolism).
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
from mpmath import mp, mpf, sqrt, pi as mp_pi, exp, ln, log
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


def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║          IRON ON THE EPOCH LADDER — THE d-ORBITAL PHASE CHANNEL            ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    # -------------------------------------------------------------------------
    # PART 1: IRON IN THE PERIODIC TABLE AND THE COSMOS
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 1: IRON IN THE PERIODIC TABLE AND THE COSMOS                          ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    Z_Fe = 26
    A_Fe = 56
    m_Fe_amu = mpf('55.934936')
    m_Fe_MeV = m_Fe_amu * mpf('931.494')
    BE_per_nucleon_MeV = mpf('8.790')
    BE_total_MeV = BE_per_nucleon_MeV * A_Fe

    print(f"  Iron: Z = {Z_Fe}, A = {A_Fe}")
    print(f"  Mass: {float(m_Fe_amu):.6f} amu = {float(m_Fe_MeV):.1f} MeV")
    print(f"  Binding energy per nucleon: {float(BE_per_nucleon_MeV):.3f} MeV (PEAK of BE curve)")
    print(f"  Total binding energy: {float(BE_total_MeV):.1f} MeV")
    print()
    print("  Fe-56 sits at the MAXIMUM of the nuclear binding energy curve.")
    print("  Lighter nuclei release energy by FUSION (stars).")
    print("  Heavier nuclei release energy by FISSION.")
    print("  Iron is the THERMODYNAMIC ENDPOINT of stellar nucleosynthesis:")
    print("    → Stars die at iron. When the core becomes iron, fusion stops → core collapse → supernova.")
    print("    → Iron is dispersed into the interstellar medium → incorporated into planets → available for life.")
    print()
    print("  In GU: iron occupies a special position on the epoch ladder — it is the nucleus where")
    print("  the strong-force V(ρ) landscape reaches its DEEPEST minimum per nucleon.")
    print("  Everything lighter is climbing toward iron; everything heavier is falling away from it.")
    print("  Iron is the nuclear fixed point.")
    print()

    abundance_ppm_earth = mpf('63000')
    abundance_ppm_crust = mpf('50000')
    abundance_rank_universe = 6
    print(f"  Cosmic abundance: {abundance_rank_universe}th most abundant element in the universe (after H, He, O, C, Ne).")
    print(f"  Earth's crust: ~{float(abundance_ppm_crust):.0f} ppm (5% by mass — 4th most abundant).")
    print(f"  Earth's core: ~{float(abundance_ppm_earth):.0f} ppm equivalent; the core IS mostly iron.")
    print()

    # -------------------------------------------------------------------------
    # PART 2: d-ORBITAL ELECTRONIC STRUCTURE
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 2: d-ORBITAL ELECTRONIC STRUCTURE                                     ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Electronic configuration: [Ar] 3d⁶ 4s²")
    print("  Five d-orbitals: dxy, dxz, dyz, dx²-y², dz²")
    print("  Six 3d electrons fill these orbitals according to Hund's rule.")
    print()
    print("  In a LIGAND FIELD (crystal field theory):")
    print("    Octahedral: d-orbitals split into t₂g (lower, 3 orbitals) and eg (higher, 2 orbitals).")
    print("    Splitting energy: Δ_oct (10Dq).")
    print("    The competition between Δ_oct and pairing energy P determines spin state.")
    print()

    IE_1_eV = mpf('7.902')
    IE_2_eV = mpf('16.188')
    IE_3_eV = mpf('30.652')
    print("  Ionization energies:")
    print(f"    IE₁ (Fe → Fe⁺):   {float(IE_1_eV):.3f} eV   (remove 4s electron)")
    print(f"    IE₂ (Fe⁺ → Fe²⁺): {float(IE_2_eV):.3f} eV  (remove 4s electron)")
    print(f"    IE₃ (Fe²⁺ → Fe³⁺):{float(IE_3_eV):.3f} eV  (remove 3d electron)")
    print()
    print("  Fe²⁺: [Ar] 3d⁶  — six d-electrons, partially filled")
    print("  Fe³⁺: [Ar] 3d⁵  — five d-electrons, HALF-FILLED (extra stability)")
    print("  The Fe²⁺/Fe³⁺ couple is uniquely suited for biology:")
    print("    → Both states are accessible at biological potentials (~-0.5 to +0.5 V)")
    print("    → Fe³⁺ is stabilized by half-filled d-shell symmetry")
    print("    → Single-electron transfer: Fe²⁺ ↔ Fe³⁺ + e⁻")
    print()

    # -------------------------------------------------------------------------
    # PART 3: VARIABLE OXIDATION STATES AS V_LOCK CONFIGURATIONS
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 3: VARIABLE OXIDATION STATES AS V_LOCK CONFIGURATIONS                ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Each oxidation state = a different ρ configuration in V_lock:")
    print()
    print("  State    Config     d-electrons   V_lock minimum   Role in biology")
    print("  ------   --------   -----------   --------------   ---------------")
    print("  Fe⁰      [Ar]3d⁶4s² 8 (total)     metallic band    abiotic (minerals)")
    print("  Fe²⁺     [Ar]3d⁶     6             octahedral       soluble, active (hemoglobin, Fe-S)")
    print("  Fe³⁺     [Ar]3d⁵     5 (half)      octahedral       stable, storage (ferritin, transferrin)")
    print("  Fe⁴⁺     [Ar]3d⁴     4             rare, reactive   transient (P450 ferryl intermediate)")
    print()
    print("  In GU: oxidation state changes are TRANSITIONS between V_lock minima.")
    print("  The protein environment TUNES which minimum is deepest:")
    print("    → Hemoglobin: stabilizes Fe²⁺ (needs to bind O₂)")
    print("    → Ferritin: stabilizes Fe³⁺ (safe storage)")
    print("    → Cytochrome P450: accesses Fe⁴⁺ transiently (extreme catalysis)")
    print()
    print("  The key GU insight: the d-orbital manifold gives iron MULTIPLE V_lock minima,")
    print("  each accessible at biological energies. This multiplicity is what makes iron")
    print("  the most versatile transition metal in biology.")
    print()

    # -------------------------------------------------------------------------
    # PART 4: SPIN STATES — THE BINARY THETA SWITCH
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 4: SPIN STATES — THE BINARY THETA SWITCH                             ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Fe²⁺ (d⁶) in octahedral field:")
    print("    HIGH-SPIN (weak field): t₂g⁴ eg² → S = 2, paramagnetic, larger ionic radius")
    print("    LOW-SPIN (strong field): t₂g⁶ eg⁰ → S = 0, diamagnetic, smaller ionic radius")
    print()

    Delta_oct_weak_eV = mpf('0.8')
    Delta_oct_strong_eV = mpf('2.5')
    pairing_energy_eV = mpf('1.5')
    print(f"  Crystal field splitting: Δ_oct ~ {float(Delta_oct_weak_eV)}–{float(Delta_oct_strong_eV)} eV (depends on ligands)")
    print(f"  Pairing energy: P ~ {float(pairing_energy_eV)} eV")
    print()
    print("  If Δ_oct < P: HIGH-SPIN (electrons avoid pairing → spread across all orbitals)")
    print("  If Δ_oct > P: LOW-SPIN (electrons pair up in lower orbitals)")
    print()

    spin_state_gap_eV = mpf('0.1')
    print("  HEMOGLOBIN EXAMPLE:")
    print("    Deoxy-Hb: Fe²⁺ high-spin (S=2), 0.4 Å out of porphyrin plane (too big to fit)")
    print("    Oxy-Hb:   Fe²⁺ low-spin (S=0), moves INTO plane upon O₂ binding")
    print("    This 0.4 Å movement pulls the proximal histidine → triggers allosteric change")
    print(f"    Spin-state energy gap: ~{float(spin_state_gap_eV)} eV (comparable to k_BT at 310 K = {float(k_BT):.4f} eV)")
    print()
    print("  In GU: the spin-state transition is a BINARY THETA-CHANNEL SWITCH.")
    print("  High-spin = one V_lock minimum; low-spin = another.")
    print("  The transition between them carries information (O₂ bound / not bound).")
    print("  This is a d-orbital implementation of the phase channel at the molecular scale.")
    print()

    # Spin-orbit coupling energy
    zeta_3d_Fe_cm = mpf('400')
    cm_to_eV = mpf('1.2398e-4')
    zeta_3d_Fe_eV = zeta_3d_Fe_cm * cm_to_eV
    print("  Spin-orbit coupling:")
    print(f"    ζ₃d(Fe) ≈ {float(zeta_3d_Fe_cm):.0f} cm⁻¹ = {float(zeta_3d_Fe_eV):.4f} eV")
    print("    This couples spin and orbital angular momentum → the d-orbital PHASE channel.")
    print("    Without spin-orbit coupling, d-orbitals would be amplitude-only.")
    print("    Spin-orbit coupling is what makes iron a PARTIAL PHASE CHANNEL material.")
    print()

    # -------------------------------------------------------------------------
    # PART 5: IRON AS PARTIAL PHASE CHANNEL MATERIAL
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 5: IRON AS PARTIAL PHASE CHANNEL MATERIAL                             ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Phase channel hierarchy (from 25_PHONONS, 26_PLATONIC_SPACE):")
    print()
    print("  Material            Winding   Phase channel   Examples")
    print("  ------------------  --------  -------------   --------------------------------")
    print("  σ-bonded (sp³)      w = 0     NONE            water, diamond, alkanes")
    print("  π-bonded (sp²)      w ≥ 1     FULL            DNA, graphene, aromatic amino acids")
    print("  d-orbital metals    partial   PARTIAL         iron, copper, cobalt, manganese")
    print("  π + d (dual)        w ≥ 1 + d FULL + partial  heme (Fe in porphyrin ring)")
    print()
    print("  Iron provides a PARTIAL phase channel through:")
    print("    1. Spin-orbit coupling (ζ₃d ≈ 0.05 eV): couples orbital motion to spin")
    print("    2. Spin-state switching (high↔low): binary information carrier")
    print("    3. Variable oxidation (Fe²⁺↔Fe³⁺): controlled electron transfer")
    print("    4. Magnetic ordering (ferromagnetism in bulk): collective spin alignment")
    print()
    print("  The phase channel is PARTIAL because:")
    print("    — d-orbitals are localized (unlike delocalized π systems)")
    print("    — Spin-orbit coupling is weaker than π-stacking (0.05 eV vs 0.39 eV)")
    print("    — But: d-orbitals can be TUNED by ligand field (protein environment)")
    print("    — And: they enable SINGLE-ELECTRON transfer (π systems do multi-electron)")
    print()
    print("  Key result: iron is the bridge between amplitude-only (σ) and phase-active (π).")
    print("  Biology uses iron WHERE it needs single-electron relays and spin-state sensing.")
    print()

    # -------------------------------------------------------------------------
    # PART 6: WHY IRON IS COSMICALLY SPECIAL
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 6: WHY IRON IS COSMICALLY SPECIAL                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Iron is cosmically special for FOUR converging reasons:")
    print()
    print("  1. NUCLEAR: peak of binding energy curve → thermodynamic endpoint of fusion")
    print("     → Stars die at iron → supernovae disperse it → abundant in planets")
    print()
    print("  2. ELECTRONIC: partially filled 3d⁶ shell → multiple stable oxidation states")
    print("     → Fe²⁺/Fe³⁺ accessible at biological potentials (~±0.5 V)")
    print()
    print("  3. SPIN: high-spin/low-spin switching via ligand field tuning")
    print("     → Binary theta-channel switch → information carrier (O₂ sensing)")
    print()
    print("  4. COUPLING: spin-orbit interaction → partial phase channel")
    print("     → Bridges amplitude and phase channels in biology")
    print("     → Enables electron relay, catalysis, magnetoreception")
    print()
    print("  No other element combines all four. Copper comes closest (d⁹/d¹⁰) but has only")
    print("  ONE accessible redox couple and no spin-state switching. Manganese has multiple")
    print("  oxidation states but is less abundant. Cobalt works but is rare.")
    print()
    print("  In GU: iron is the LOWEST-COST d-orbital phase bridge that the Platonic Space")
    print("  can access at biological temperatures and abundances.")
    print("  Stars produce iron as their thermodynamic endpoint;")
    print("  life uses iron as its phase-channel relay. The connection is not accidental.")
    print()

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  SUMMARY                                                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  (1) Fe-56: peak nuclear binding energy → endpoint of stellar fusion → cosmic abundance.")
    print("  (2) [Ar] 3d⁶: partially filled d-shell → Fe²⁺/Fe³⁺ redox couple at bio potentials.")
    print("  (3) Spin states: high-spin ↔ low-spin = binary theta-channel switch (hemoglobin).")
    print("  (4) Spin-orbit coupling (ζ ≈ 0.05 eV): makes d-orbitals a partial phase channel.")
    print("  (5) Iron = lowest-cost d-orbital phase bridge in biology.")
    print("  Connects to: 25_PHONONS/02 (d-orbital kink modes), 26_PLATONIC_SPACE/07 (nonlocal),")
    print("  27_FIRST_CELL/03 (catalysis), 27_FIRST_CELL/04 (ETC).")
    print()


if __name__ == "__main__":
    main()
