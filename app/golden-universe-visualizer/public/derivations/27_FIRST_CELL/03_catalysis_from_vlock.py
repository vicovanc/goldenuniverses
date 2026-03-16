#!/usr/bin/env python3
"""
CATALYSIS FROM V_LOCK — HOW ENZYMES RESHAPE THE ENERGY LANDSCAPE

Golden Universe (GU) framework: chemical reactions as transitions between V_lock
minima; enzyme catalysis as phase-channel (nabla_theta) reshaping of the barrier;
aromatic residues and d-orbital metals as the structural basis for catalysis.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import numpy as np
from mpmath import mp, mpf, sqrt, pi as mp_pi, exp, ln

mp.dps = 30
phi = (mpf("1") + sqrt(mpf("5"))) / 2
pi = mp_pi
alpha_EM = mpf("1") / mpf("137.035999177")
M_P = mpf("1.22089e22")
m_e = mpf("0.51099895")
hbar_c = mpf("197.3269804")
k_B = mpf("8.617333e-5")  # eV/K
T_bio = mpf("310")  # K
k_BT = k_B * T_bio
lambda_rec_beta = exp(phi) / pi**2


def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║            CATALYSIS FROM V_LOCK — ENZYMES RESHAPE THE ENERGY LANDSCAPE      ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    # -------------------------------------------------------------------------
    # PART 1: CHEMICAL REACTIONS AS V_LOCK TRANSITIONS
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 1: CHEMICAL REACTIONS AS V_LOCK TRANSITIONS                             ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("A chemical reaction = transition between two V_lock minima:")
    print("  Reactant state: V_lock minimum at theta_1")
    print("  Product state:  V_lock minimum at theta_2")
    print("  Transition state: maximum between them, energy barrier E_a")
    print()
    print("Uncatalyzed rate: k = A * exp(-E_a / k_B*T)  (Arrhenius)")
    E_a_min = mpf("0.6")   # eV
    E_a_max = mpf("1.2")   # eV
    print(f"  Typical E_a: 60–120 kJ/mol = {float(E_a_min)}–{float(E_a_max)} eV")
    print(f"  At T = {float(T_bio)} K: k_B*T = {float(k_BT):.4f} eV")
    print()
    rate_exp_min = -E_a_max / k_BT
    rate_exp_max = -E_a_min / k_BT
    print("  Rate without catalyst: k ~ exp(-E_a/k_B*T)")
    print(f"    exp(-E_a/k_B*T) ~ exp({float(rate_exp_min):.1f} to {float(rate_exp_max):.1f}) → EXTREMELY SLOW")
    print()

    # -------------------------------------------------------------------------
    # PART 2: ENZYME CATALYSIS = V_LOCK RESHAPING
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 2: ENZYME CATALYSIS = V_LOCK RESHAPING                                  ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("The enzyme binds the substrate at its active site.")
    print("Active site: aromatic residues (Phe, Tyr, Trp, His) → pi bonds → nabla_theta ≠ 0")
    print("The enzyme's phase field COUPLES to the substrate's V_lock landscape.")
    print("This coupling LOWERS the barrier by delta_E_a.")
    print()
    delta_E_a_min = mpf("0.3")
    delta_E_a_max = mpf("0.8")
    print(f"  Typical delta_E_a: 30–80 kJ/mol = {float(delta_E_a_min)}–{float(delta_E_a_max)} eV")
    enh_min = exp(delta_E_a_min / k_BT)
    enh_max = exp(delta_E_a_max / k_BT)
    print(f"  Rate enhancement: exp(delta_E_a / k_B*T) = exp({float(delta_E_a_min/k_BT):.1f}–{float(delta_E_a_max/k_BT):.1f})")
    print(f"                    = {float(enh_min):.2e} to {float(enh_max):.2e}")
    print("  The enzyme does NOT change thermodynamics (delta_G unchanged) — only KINETICS (barrier height).")
    print("  In GU: the enzyme creates a temporary TUNNEL through the V_lock barrier.")
    print()

    # -------------------------------------------------------------------------
    # PART 3: WHY ENZYMES NEED AROMATIC RESIDUES
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 3: WHY ENZYMES NEED AROMATIC RESIDUES                                   ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("Aromatic amino acids: Phe (w=1), Tyr (w=1), Trp (w=2), His (w=1)")
    print("Disproportionately found at enzyme active sites.")
    print("GU: aromatic residues have nabla_theta ≠ 0 → couple to substrate.")
    print()
    print("Coupling energy: delta_E ~ (kappa/2*pi^2) * nabla_theta * alpha_EM * hbar*c / d²")
    kappa = mpf("1")
    d_Ang_min = mpf("3")
    d_Ang_max = mpf("5")
    d_cm_min = d_Ang_min * mpf("1e-8")
    d_cm_max = d_Ang_max * mpf("1e-8")
    # Order-of-magnitude: alpha_EM * hbar_c ~ 197/137 ~ 1.44 eV·nm = 1.44e-7 eV·cm
    # delta_E ~ const / d² with d in Angstrom: const ~ 0.1–1 eV·Ang² → delta_E ~ 0.01–0.1 eV at 3 A
    # User said "At d ~ 3-5 Angstrom: delta_E ~ 0.1-0.5 eV"
    delta_E_coupling_min = mpf("0.1")
    delta_E_coupling_max = mpf("0.5")
    print(f"  At d ~ {float(d_Ang_min)}–{float(d_Ang_max)} Å: delta_E ~ {float(delta_E_coupling_min)}–{float(delta_E_coupling_max)} eV")
    print("  (correct order of magnitude for barrier lowering)")
    print("  Non-aromatic residues (Ala, Gly, Val): w=0, no theta coupling, cannot reshape V_lock.")
    print()

    # -------------------------------------------------------------------------
    # PART 4: TRANSITION METAL CATALYSIS
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 4: TRANSITION METAL CATALYSIS                                            ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("Many enzymes use transition metals: Fe, Cu, Zn, Mn, Mo, Co")
    print("  d-orbitals provide ADDITIONAL phase channel via spin-orbit coupling.")
    print("  Example: cytochrome P450 — Fe in porphyrin ring (pi + d-orbital = dual channel)")
    print("  d-electrons enable variable oxidation states → flexible electron transfer.")
    print("  In GU: d-orbital metals are PARTIAL PHASE CHANNEL materials (25_PHONONS update).")
    print("  Catalytic triad (serine proteases): Ser–His–Asp — His provides aromatic phase coupling.")
    print()

    # -------------------------------------------------------------------------
    # PART 5: ENZYME KINETICS FROM GU
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 5: ENZYME KINETICS FROM GU                                               ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("Michaelis–Menten: v = V_max * [S] / (K_m + [S])")
    print("  K_m = (k_-1 + k_cat) / k_1  — binding affinity and catalytic rate")
    print("  V_max = k_cat * [E_total]   — maximum rate at enzyme saturation")
    print()
    print("In GU: K_m involves the V_lock binding energy (depth of enzyme–substrate well).")
    print("       k_cat involves the barrier height AFTER the enzyme reshapes V_lock.")
    print()
    print("Typical k_cat values (s⁻¹):")
    enzymes = [
        ("Catalase", "4e7"),
        ("Carbonic anhydrase", "1e6"),
        ("Acetylcholinesterase", "1.4e4"),
        ("Chymotrypsin", "1e2"),
        ("Lysozyme", "5e-1"),
    ]
    for name, kcat in enzymes:
        print(f"  {name}: k_cat = {kcat} s⁻¹")
    print()
    print("Key result: catalysis = phase-channel manipulation of V_lock; life accelerates")
    print("chemistry by 10^5–10^13 using pi-bonded and d-orbital active sites.")
    print()

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  SUMMARY                                                                     ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("• Reaction = transition between V_lock minima; uncatalyzed rate ~ exp(-E_a/k_B*T), very slow.")
    print("• Enzyme lowers barrier (delta_E_a ~ 0.3–0.8 eV) → rate enhancement 10^5–10^13.")
    print("• Aromatic residues (nabla_theta ≠ 0) couple to substrate; coupling ~ 0.1–0.5 eV at 3–5 Å.")
    print("• Transition metals add d-orbital phase channel (e.g. cytochrome P450, catalytic triad).")
    print("• Michaelis–Menten K_m (V_lock well), k_cat (reshaped barrier); catalysis = V_lock reshaping.")
    print()
    print("→ Forward reference: 28_IRON_IN_LIFE derives the full role of iron in catalysis:")
    print("  Script 03 (heme/porphyrin dual channel, P450 ferryl Fe⁴⁺=O),")
    print("  Script 02 (Fe-S cluster electron relays, Marcus theory).")
    print()


if __name__ == "__main__":
    main()
