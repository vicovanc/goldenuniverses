#!/usr/bin/env python3
"""
MEMBRANE AS PLATONIC SPACE BOUNDARY

Golden Universe (GU) framework: the membrane as the first structure that creates
a controllable region in the Platonic Space — a potential barrier in field space
that separates inside/outside and enables agency and homeostasis.
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

# Elementary charge (C) for Nernst in volts; k_B in J/K for V = (k_B*T/e)*ln(...)
e_C = mpf("1.602176634e-19")
k_B_J = mpf("1.380649e-23")
RT_over_F = k_B_J * T_bio / e_C  # volts

def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║            MEMBRANE AS PLATONIC SPACE BOUNDARY (GU)                          ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    # -------------------------------------------------------------------------
    # PART 1: INSIDE vs OUTSIDE
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 1: INSIDE vs OUTSIDE                                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("The membrane creates two DISTINCT regions with different chemical composition:")
    print("  Inside:  high K+ (~140 mM), low Na+ (~12 mM), high protein, specific metabolites")
    print("  Outside: low K+ (~4 mM),   high Na+ (~145 mM), more dilute")
    print()
    print("In GU: the membrane is a POTENTIAL BARRIER V_membrane in field space.")
    V_barrier_eV_min = mpf("0.2")
    V_barrier_eV_max = mpf("0.3")
    print(f"  Barrier height: ~{float(V_barrier_eV_min)}–{float(V_barrier_eV_max)} eV for ions")
    print("  (energy to move an ion across the hydrophobic core)")
    print("  This barrier creates a separate REGION in the Platonic Space where rho and theta")
    print("  can be CONTROLLED.")
    print()

    # -------------------------------------------------------------------------
    # PART 2: MEMBRANE POTENTIAL (Nernst, Goldman)
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 2: MEMBRANE POTENTIAL                                                  ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("Nernst equation: E_ion = (k_B*T/e) * ln([ion]_out / [ion]_in)")
    print(f"  At T = {float(T_bio)} K: (k_B*T/e) = {float(RT_over_F)*1000:.2f} mV")
    print()

    # Concentrations in mM
    K_in, K_out = mpf("140"), mpf("4")
    Na_in, Na_out = mpf("12"), mpf("145")
    Ca_in, Ca_out = mpf("0.0001"), mpf("2")   # mM, typical
    Cl_in, Cl_out = mpf("4"), mpf("116")      # mM, typical (Cl higher outside)

    E_K  = RT_over_F * ln(K_out / K_in)
    E_Na = RT_over_F * ln(Na_out / Na_in)
    E_Ca = (RT_over_F / 2) * ln(Ca_out / Ca_in)  # z=2
    E_Cl = -RT_over_F * ln(Cl_out / Cl_in)       # anion: reversal

    print("Nernst equilibrium potentials (mV):")
    print(f"  E_K   = (k_BT/e) * ln([K+]_out/[K+]_in) = 26.7 * ln({float(K_out)}/{float(K_in)}) = {float(E_K)*1000:.2f} mV")
    print(f"  E_Na  = (k_BT/e) * ln([Na+]_out/[Na+]_in) = 26.7 * ln({float(Na_out)}/{float(Na_in)}) = {float(E_Na)*1000:.2f} mV")
    print(f"  E_Ca  = (k_BT/e)/(2) * ln([Ca2+]_out/[Ca2+]_in) = {float(E_Ca)*1000:.1f} mV")
    print(f"  E_Cl  = -(k_BT/e) * ln([Cl-]_out/[Cl-]_in) = {float(E_Cl)*1000:.2f} mV")
    print()
    print("Goldman: V_m depends on permeabilities P_K, P_Na, P_Cl.")
    V_m_rest = mpf("-0.07")  # -70 mV
    print(f"  Typical resting V_m ≈ {float(V_m_rest)*1000:.0f} mV (K+ dominates resting potential).")
    print("  The membrane potential is STORED ENERGY — like a charged capacitor.")
    print()

    # -------------------------------------------------------------------------
    # PART 3: MEMBRANE AS CAPACITOR
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 3: THE MEMBRANE AS CAPACITOR                                            ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("Capacitance: C = epsilon_0 * epsilon_r / d")
    eps0 = mpf("8.854e-14")   # F/cm
    eps_r = mpf("2")
    d_nm = mpf("4")
    d_cm = d_nm * mpf("1e-7")
    C_per_cm2 = eps0 * eps_r / d_cm
    print(f"  epsilon_r ~ {float(eps_r)} (hydrocarbon dielectric), d ~ {float(d_nm)} nm")
    print(f"  C ~ {float(C_per_cm2)*1e6:.2f} uF/cm²  (measured: 0.5–1.0 uF/cm²)")
    print()
    V_m_abs = abs(V_m_rest)
    E_stored_J_per_cm2 = mpf("0.5") * C_per_cm2 * (V_m_abs ** 2)
    print("Energy stored: E = (1/2) C V²")
    print(f"  E = (1/2) * ({float(C_per_cm2):.2e}) * ({float(V_m_abs)})² = {float(E_stored_J_per_cm2):.2e} J/cm²")
    # Per lipid: area per lipid ~ 0.64 nm² = 0.64e-14 cm²
    area_lipid_cm2 = mpf("0.64e-14")
    lipids_per_cm2 = mpf("1") / area_lipid_cm2
    E_per_lipid_J = E_stored_J_per_cm2 / lipids_per_cm2
    eV_per_J = mpf("1") / mpf("1.602176634e-19")
    E_per_lipid_eV = E_per_lipid_J * mpf("1.602176634e-19") ** (-1)
    print(f"  Per lipid: E_lipid = {float(E_stored_J_per_cm2):.2e} / (1/({float(area_lipid_cm2):.2e})) ≈ {float(E_per_lipid_eV):.2e} eV")
    print("  This energy is TINY per lipid but adds up:")
    n_lipids = mpf("1e9")
    total_eV = E_per_lipid_eV * n_lipids
    print(f"  For a cell with ~10^9 lipids, total ~ {float(total_eV):.0f} eV")
    print()

    # -------------------------------------------------------------------------
    # PART 4: SELECTIVE PERMEABILITY TABLE
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 4: SELECTIVE PERMEABILITY TABLE                                         ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    rows = [
        ("Molecule", "Size (nm)", "Charge", "Permeability (cm/s)", "GU interpretation"),
        ("O2", "0.29", "0", "11", "amplitude channel continuous"),
        ("H2O", "0.28", "0", "5e-3", "partially permeable"),
        ("Na+ (hydrated)", "0.36", "+1", "<1e-12", "BLOCKED (charge in hydrophobic barrier)"),
        ("K+ (hydrated)", "0.33", "+1", "<1e-12", "BLOCKED"),
        ("Glucose", "0.73", "0", "~1e-10", "needs transporter"),
    ]
    col_widths = [20, 12, 8, 24, 42]
    sep = "  ".join("-" * w for w in col_widths)
    for i, row in enumerate(rows):
        line = "  ".join(str(x).ljust(col_widths[j])[:col_widths[j]] for j, x in enumerate(row))
        print(line)
        if i == 0:
            print(sep)
    print()
    print("The membrane selectively controls the amplitude channel.")
    print("Phase channel (theta): blocked for sigma-bonded molecules; pi-stacked columns")
    print("could hypothetically bridge it.")
    print()

    # -------------------------------------------------------------------------
    # PART 5: THE PLATONIC SPACE BOUNDARY
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 5: THE PLATONIC SPACE BOUNDARY                                           ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("The membrane is the FIRST STRUCTURE that creates a controllable region in the")
    print("Platonic Space.")
    print("  Without membrane: no control, no agency, no homeostasis.")
    print("  With membrane: the cell can maintain gradients (rho), sustain patterns (theta),")
    print("                 and resist thermal noise.")
    print("The membrane is to the cell what the soliton topology is to the electron:")
    print("  a BOUNDARY CONDITION that creates identity.")
    print()

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  SUMMARY                                                                     ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("• Membrane = potential barrier V_membrane in field space (~0.2–0.3 eV for ions).")
    print("• Two distinct regions: inside/outside with different rho, theta control.")
    print("• Nernst/Goldman: E_K ≈ -94 mV, E_Na ≈ +66 mV; V_m ≈ -70 mV (capacitor-like).")
    print("• Capacitance ~0.44 uF/cm²; stored energy small per lipid, ~10^5 eV per cell.")
    print("• Selective permeability: O2/H2O pass; ions blocked; glucose needs transporters.")
    print("• Membrane = Platonic Space boundary: first structure for agency and homeostasis.")
    print()


if __name__ == "__main__":
    main()
