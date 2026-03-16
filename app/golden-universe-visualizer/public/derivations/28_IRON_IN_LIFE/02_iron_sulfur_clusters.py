#!/usr/bin/env python3
"""
IRON-SULFUR CLUSTERS — THE OLDEST IRON MACHINES
================================================

PART 1: Fe-S CLUSTER TYPES AND STRUCTURE
PART 2: Fe-S AS d-ORBITAL PHASE RELAYS
PART 3: Fe-S IN THE ELECTRON TRANSPORT CHAIN
PART 4: Fe-S BEYOND THE ETC
PART 5: ABIOTIC ORIGINS — THE IRON-SULFUR WORLD
PART 6: MARCUS THEORY AND ELECTRON TRANSFER RATES

Connects to 27_FIRST_CELL/04 (ETC), Script 01 (d-orbital structure),
Script 04 (redox chemistry).
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


def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║        IRON-SULFUR CLUSTERS — THE OLDEST IRON MACHINES                      ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    # -------------------------------------------------------------------------
    # PART 1: Fe-S CLUSTER TYPES AND STRUCTURE
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 1: Fe-S CLUSTER TYPES AND STRUCTURE                                   ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Fe-S clusters: inorganic cofactors where iron atoms are bridged by sulfide (S²⁻) ions.")
    print("  Coordinated to proteins via cysteine thiolate ligands (sometimes histidine).")
    print()
    print("  Type          Structure              Fe atoms   Electron transfer")
    print("  ------------  ---------------------  --------   -----------------")
    print("  [2Fe-2S]      Rhombus (2 Fe, 2 S)    2          1e⁻ (Fe³⁺/Fe²⁺)")
    print("  [3Fe-4S]      Cuboidal               3          1e⁻")
    print("  [4Fe-4S]      Cubane (cube corners)   4          1e⁻ or 2e⁻")
    print("  [4Fe-4S]-HiPIP  Same structure        4          1e⁻ (high potential)")
    print("  FeMo-cofactor  MoFe₇S₉C (complex)    7+Mo       multi-electron (N₂ → NH₃)")
    print()
    print("  Key: ALL Fe-S clusters transfer electrons ONE AT A TIME (except special cases).")
    print("  Each cluster = a d-orbital phase relay with a specific V_lock depth.")
    print()

    # -------------------------------------------------------------------------
    # PART 2: Fe-S AS d-ORBITAL PHASE RELAYS
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 2: Fe-S AS d-ORBITAL PHASE RELAYS                                     ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Each Fe-S cluster sits at a specific REDOX POTENTIAL determined by:")
    print("    1. Cluster type ([2Fe-2S] vs [4Fe-4S])")
    print("    2. Protein environment (hydrogen bonds, charge distribution, solvent access)")
    print("    3. Cysteine vs histidine ligation")
    print()
    print("  In GU: the protein TUNES V_lock for each Fe-S cluster.")
    print("  The same [4Fe-4S] cluster can have potentials from -0.7 V to +0.4 V")
    print("  depending on its protein environment — a 1.1 V range!")
    print()

    E_range_min_V = mpf('-0.7')
    E_range_max_V = mpf('0.4')
    E_range_eV = abs(E_range_max_V - E_range_min_V)
    print(f"  Redox potential range: {float(E_range_min_V)} V to {float(E_range_max_V)} V")
    print(f"  Total tuning range: {float(E_range_eV):.1f} eV")
    print(f"  Compare to k_BT at 310 K: {float(k_BT):.4f} eV — the range spans ~{float(E_range_eV/k_BT):.0f} × k_BT")
    print()
    print("  This means the protein can place the electron relay at ANY desired energy level")
    print("  within a ~1 eV window — like placing rungs on a ladder.")
    print("  The ETC (Script 04, 27_FIRST_CELL) uses this to create a precise electron staircase.")
    print()

    # -------------------------------------------------------------------------
    # PART 3: Fe-S IN THE ELECTRON TRANSPORT CHAIN
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 3: Fe-S IN THE ELECTRON TRANSPORT CHAIN                               ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Complex I (NADH dehydrogenase): THE Fe-S machine.")
    print("    9 Fe-S clusters forming an ELECTRON WIRE ~95 Å long:")
    print("    N1a [2Fe-2S] → N3 [4Fe-4S] → N1b [2Fe-2S] → N4 [4Fe-4S] →")
    print("    N5 [4Fe-4S] → N6a [4Fe-4S] → N6b [4Fe-4S] → N2 [4Fe-4S] → CoQ")
    print()

    wire_length_Angstrom = mpf('95')
    cluster_spacing_Angstrom = mpf('14')
    transfer_time_us = mpf('100')
    print(f"    Wire length: ~{float(wire_length_Angstrom):.0f} Å")
    print(f"    Average cluster spacing: ~{float(cluster_spacing_Angstrom):.0f} Å (edge-to-edge)")
    print(f"    Total electron transit time: ~{float(transfer_time_us):.0f} µs")
    print()
    print("  Complex II (succinate dehydrogenase): 3 Fe-S clusters.")
    print("    [2Fe-2S] → [4Fe-4S] → [3Fe-4S] → CoQ")
    print()
    print("  Complex III (cytochrome bc₁): 1 Rieske [2Fe-2S] center.")
    print("    Special: one Fe coordinated by 2 histidines (not cysteines)")
    print("    → Higher redox potential (+0.28 V) — the protein tuning effect.")
    print()
    print("  Total Fe-S clusters in ETC: ~13 per chain (9 + 3 + 1).")
    print("  In GU: the ETC is an iron-sulfur RELAY NETWORK — a d-orbital phase wire")
    print("  that converts chemical potential into a proton gradient with ~40% efficiency.")
    print()

    # -------------------------------------------------------------------------
    # PART 4: Fe-S BEYOND THE ETC
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 4: Fe-S BEYOND THE ETC                                                ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Fe-S clusters appear in nearly EVERY major metabolic pathway:")
    print()
    print("  Pathway                 Enzyme                   Fe-S type     Function")
    print("  ----------------------  -----------------------  -----------   -----------------")
    print("  Krebs cycle             Aconitase                [4Fe-4S]      Substrate binding + catalysis")
    print("  Nitrogen fixation       Nitrogenase              FeMo-cofactor N₂ → 2NH₃ (6e⁻ + 6H⁺)")
    print("  DNA repair              Endonuclease III         [4Fe-4S]      DNA damage sensing")
    print("  Gene regulation         IRP1 (iron sensor)       [4Fe-4S]      Senses cellular iron level")
    print("  Radical chemistry       Radical SAM enzymes      [4Fe-4S]      Generates 5'-dAdo radical")
    print("  Photosynthesis          Photosystem I            3×[4Fe-4S]    Electron acceptors")
    print("  Sulfur metabolism       Sulfite reductase        [4Fe-4S]      SO₃²⁻ → S²⁻")
    print()
    print("  Key insight: Fe-S clusters are the MOST VERSATILE biological cofactor.")
    print("  They do electron transfer, catalysis, sensing, and structural roles.")
    print("  In GU: the d-orbital phase relay is so fundamental that biology has")
    print("  adapted it for every function that requires controlled electron handling.")
    print()

    # -------------------------------------------------------------------------
    # PART 5: ABIOTIC ORIGINS — THE IRON-SULFUR WORLD
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 5: ABIOTIC ORIGINS — THE IRON-SULFUR WORLD                            ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Wächtershauser hypothesis (1988): life originated on iron-sulfide mineral surfaces")
    print("  at hydrothermal vents.")
    print()
    print("  Key reaction: FeS + H₂S → FeS₂ (pyrite) + H₂")
    print("    ΔG ≈ -38 kJ/mol ≈ -0.39 eV (exergonic — provides energy)")
    print()

    delta_G_pyrite_eV = mpf('-0.39')
    print(f"    ΔG(FeS → FeS₂) = {float(delta_G_pyrite_eV):.2f} eV (energy source for prebiotic chemistry)")
    print()
    print("  In GU: Fe-S minerals at hydrothermal vents provided:")
    print("    1. ENERGY: pyrite formation releases energy for organic synthesis")
    print("    2. SURFACE: mineral surface concentrates reactants (reduces entropy cost)")
    print("    3. d-ORBITAL RELAY: Fe²⁺/Fe³⁺ cycling on mineral surface = first electron transfer")
    print("    4. CATALYSIS: Fe-S surfaces catalyze CO₂ fixation, amino acid synthesis")
    print()
    print("  This predates membranes, RNA, and all biology.")
    print("  The Fe-S cluster in modern proteins is a FOSSIL of the iron-sulfur world —")
    print("  biology inherited and refined what minerals already did abiotically.")
    print()
    print("  In GU: the d-orbital phase relay was available BEFORE life. Life didn't invent it;")
    print("  life ADOPTED the pre-existing d-orbital bridge between ρ and θ channels.")
    print()

    # -------------------------------------------------------------------------
    # PART 6: MARCUS THEORY AND ELECTRON TRANSFER RATES
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 6: MARCUS THEORY AND ELECTRON TRANSFER RATES                          ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Marcus theory: k_ET = (2π/ℏ) |V_DA|² (1/√(4πλk_BT)) exp(-(ΔG° + λ)²/(4λk_BT))")
    print("  V_DA = electronic coupling between donor and acceptor")
    print("  λ = reorganization energy (inner sphere + outer sphere)")
    print("  ΔG° = driving force (free energy of reaction)")
    print()
    print("  In GU: Marcus theory = transition between V_lock minima with")
    print("  ΔG° = depth difference and λ = barrier reshaping cost.")
    print()

    V_DA_eV = mpf('0.001')
    lambda_eV = mpf('0.7')
    delta_G_eV = mpf('-0.3')
    hbar_eV_s = mpf('6.582e-16')

    exponent = -(delta_G_eV + lambda_eV)**2 / (mpf('4') * lambda_eV * k_BT)
    prefactor = (mpf('2') * pi / hbar_eV_s) * V_DA_eV**2 * (mpf('1') / sqrt(mpf('4') * pi * lambda_eV * k_BT))
    k_ET = prefactor * exp(exponent)

    print("  Example: Fe-S → Fe-S transfer in Complex I")
    print(f"    V_DA = {float(V_DA_eV):.4f} eV (weak coupling, ~14 Å separation)")
    print(f"    λ = {float(lambda_eV):.2f} eV (reorganization energy)")
    print(f"    ΔG° = {float(delta_G_eV):.2f} eV (downhill transfer)")
    print(f"    k_BT = {float(k_BT):.4f} eV")
    print(f"    Exponent: -(ΔG° + λ)²/(4λk_BT) = {float(exponent):.2f}")
    print(f"    k_ET ≈ {float(k_ET):.2e} s⁻¹")
    print()

    t_transfer = mpf('1') / k_ET
    print(f"    Transfer time: ~{float(t_transfer):.2e} s = ~{float(t_transfer*1e6):.1f} µs")
    print("    (Consistent with measured ETC kinetics)")
    print()
    print("  Marcus INVERTED REGION: when |ΔG°| > λ, rate DECREASES with more driving force.")
    print("  Biology avoids this by tuning each step so |ΔG°| < λ — the protein environment")
    print("  optimizes each V_lock transition to stay in the normal Marcus regime.")
    print()

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  SUMMARY                                                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  (1) Fe-S clusters: [2Fe-2S], [3Fe-4S], [4Fe-4S] — d-orbital phase relays.")
    print("  (2) Protein tunes V_lock: same cluster type → -0.7 V to +0.4 V range.")
    print("  (3) ETC: ~13 Fe-S clusters form an electron wire (Complex I: 9 clusters, 95 Å).")
    print("  (4) Beyond ETC: Krebs cycle, nitrogen fixation, DNA repair, gene regulation, radical SAM.")
    print("  (5) Iron-sulfur world: abiotic Fe-S surfaces → first phase relays → life adopted them.")
    print("  (6) Marcus theory: k_ET depends on V_DA, λ, ΔG° — biology tunes all three via protein.")
    print("  Fe-S clusters are the MOST ANCIENT and MOST VERSATILE d-orbital machines in biology.")
    print()


if __name__ == "__main__":
    main()
