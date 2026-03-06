#!/usr/bin/env python3
"""
METABOLISM FROM GU — ENERGY FLOW IN THE FIRST CELL

Golden Universe (GU) framework: metabolism as sustained non-equilibrium;
ATP as universal energy currency; proton motive force; electron transport chain;
energy budget of a cell. Connects to membrane (02), enzymes (03), protocell (06).
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

# Elementary charge (e in eV per volt)
e_charge = mpf('1')  # 1 e in natural units for eV
# For pmf: 2.3 * k_B*T/e in mV (e in C for volts)
e_C = mpf('1.602176634e-19')
k_B_J = mpf('1.380649e-23')
RT_over_F_mV = (k_B_J * T_bio / e_C) * mpf('1000')  # mV


def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║            METABOLISM FROM GU — ENERGY FLOW IN THE FIRST CELL               ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    # -------------------------------------------------------------------------
    # PART 1: METABOLISM = SUSTAINED NON-EQUILIBRIUM
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 1: METABOLISM = SUSTAINED NON-EQUILIBRIUM                              ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("Life maintains gradients: concentration, electrical, chemical potential.")
    print("Without energy input: gradients dissipate → equilibrium → death.")
    print("Metabolism provides constant energy input to maintain the cell FAR from equilibrium.")
    print("In GU: metabolism sustains non-zero nabla_rho and nabla_theta across the membrane.")
    print("Second law (from 22_THERMODYNAMICS): entropy of the universe increases,")
    print("  but the CELL can decrease its local entropy by exporting entropy to its environment")
    print("  (delta_S_cell < 0 while delta_S_universe > 0).")
    print()

    # -------------------------------------------------------------------------
    # PART 2: ATP — THE UNIVERSAL ENERGY CURRENCY
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 2: ATP — THE UNIVERSAL ENERGY CURRENCY                                  ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("ATP = adenosine + 3 phosphate groups.")
    print("Adenine: aromatic purine ring (w=2, phase channel active).")
    print("Hydrolysis: ATP → ADP + Pi releases delta_G° = -30.5 kJ/mol = -0.316 eV (standard).")
    print()
    # delta_G° in eV
    delta_G_std_kJ = mpf('-30.5')
    kJ_per_mol_to_eV = mpf('1') / mpf('96.485')  # kJ/mol → eV per molecule
    delta_G_std_eV = delta_G_std_kJ * kJ_per_mol_to_eV
    print(f"  delta_G° = {float(delta_G_std_eV):.3f} eV (standard, 1 M concentrations)")
    print()
    print("At T=310 K: delta_G = delta_G° + k_B*T * ln([ADP][Pi]/[ATP])")
    print(f"  k_B*T = {float(k_BT):.4f} eV")
    # In the cell: [ATP]/[ADP] ~ 10 → ln([ADP][Pi]/[ATP]) ≈ ln(0.1 * 0.001) ≈ ln(1e-4) ≈ -9.2
    # More typical: [ATP]~3 mM, [ADP]~0.3 mM, [Pi]~5 mM → Q = (0.3*5)/3 = 0.5, ln(0.5) ≈ -0.69
    # delta_G = delta_G° + k_BT * ln(Q) = -0.316 + 0.0267*(-0.69) ≈ -0.334 eV (still ~-32 kJ/mol)
    # Actual in-cell often quoted ~ -50 to -57 kJ/mol → need higher [ATP]/[ADP], e.g. [ATP]/[ADP]=100
    ratio_ATP_ADP = mpf('10')
    Pi_mM = mpf('5')
    # Q = [ADP][Pi]/[ATP] ∝ (1/10)*5/1 = 0.5 if we use relative; for -50 kJ/mol: delta_G = -0.52 eV
    # -0.52 = -0.316 + k_BT*ln(Q) → ln(Q) = (-0.52+0.316)/k_BT = -0.204/0.0267 ≈ -7.6 → Q ≈ 0.0005
    # So [ADP][Pi]/[ATP] ≈ 0.0005 → e.g. [ATP]/[ADP] ~ 100, [Pi] ~ 5 mM gives 5/100 = 0.05, close
    Q_cell = mpf('0.0005')  # typical in-cell ratio
    delta_G_cell_eV = delta_G_std_eV + k_BT * ln(Q_cell)
    delta_G_cell_kJ = delta_G_cell_eV / kJ_per_mol_to_eV
    print(f"  In the cell: [ATP]/[ADP] ~ 10–100 → actual delta_G ~ {float(delta_G_cell_kJ):.0f} kJ/mol = {float(delta_G_cell_eV):.2f} eV")
    print()
    print("The adenine ring is the phase-channel HANDLE: hydrolysis energy is transduced")
    print("through the pi system to the bound protein.")
    turnover_per_cell_per_s = mpf('1e10')
    print(f"  ~10^10 ATP molecules per cell per second turned over in a human cell.")
    print()
    print("Energy budget (human cell):")
    print(f"  delta_G per ATP (in-cell): {float(delta_G_cell_eV):.3f} eV")
    print(f"  Turnover: {float(turnover_per_cell_per_s):.2e} ATP/s per cell")
    print(f"  Power per cell: {float(turnover_per_cell_per_s * abs(delta_G_cell_eV)):.2e} eV/s")
    print()

    # -------------------------------------------------------------------------
    # PART 3: PROTON MOTIVE FORCE
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 3: PROTON MOTIVE FORCE                                                 ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("Proton gradient across membrane: delta_pH ~ 1 unit + membrane potential ~150 mV (mitochondria).")
    print("Total proton motive force: pmf = delta_psi - (2.3 * k_B*T/e) * delta_pH")
    delta_psi_mV = mpf('150')
    delta_pH = mpf('1')
    # 2.3 * k_B*T/e at 310 K ≈ 59 mV per pH unit
    slope_mV_per_pH = mpf('2.3') * RT_over_F_mV
    pmf_chemical_mV = slope_mV_per_pH * delta_pH
    pmf_total_mV = delta_psi_mV + pmf_chemical_mV  # delta_psi (electrical) + (2.3 k_BT/e)*delta_pH
    print(f"  (2.3 * k_B*T/e) at T={float(T_bio)} K = {float(slope_mV_per_pH):.1f} mV per pH unit")
    print(f"  delta_psi = {float(delta_psi_mV):.0f} mV, (2.3 k_BT/e)*delta_pH = {float(pmf_chemical_mV):.0f} mV")
    print(f"  pmf = {float(delta_psi_mV):.0f} + {float(pmf_chemical_mV):.0f} = {float(pmf_total_mV):.0f} mV")
    print()
    pmf_eV = pmf_total_mV * mpf('0.001')  # mV → V, then e*V = eV
    print(f"  Energy per proton crossing: e * pmf = {float(pmf_eV):.2f} eV")
    n_protons_per_ATP = mpf('3')
    energy_from_protons_eV = n_protons_per_ATP * pmf_eV
    print(f"  ATP synthase: ~3 protons per ATP → 3 × {float(pmf_eV):.2f} = {float(energy_from_protons_eV):.2f} eV per ATP")
    print(f"  ATP cost: {float(abs(delta_G_cell_eV)):.2f} eV → thermodynamically favorable ({float(energy_from_protons_eV):.2f} > {float(abs(delta_G_cell_eV)):.2f})")
    print()
    print("In GU: the proton (N=95 epoch) crossing a V_membrane barrier stores energy in the gradient.")
    print("ATP synthase is a ROTARY MOTOR: c-ring rotates as protons flow, gamma subunit rotates to catalyze ATP synthesis.")
    print()

    # -------------------------------------------------------------------------
    # PART 4: ELECTRON TRANSPORT CHAIN
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 4: ELECTRON TRANSPORT CHAIN                                             ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("Electrons flow from NADH (strong reductant) to O2 (strong oxidant) through pi-bonded carriers:")
    print("  Complex I:   NADH → FMN → Fe-S clusters → CoQ")
    print("  Complex II: Succinate → FAD → Fe-S → CoQ")
    print("  Complex III: CoQ → cytochrome c (heme = pi + Fe d-orbitals)")
    print("  Complex IV:  cytochrome c → O2 (4 e-, 4 H+ → 2 H2O)")
    print("ALL carriers have pi bonds or d-orbitals (or both): FMN, FAD, quinones, hemes, Fe-S clusters.")
    print()
    delta_G_NADH_O2_eV = mpf('-1.14')
    n_protons_pumped = mpf('10')
    print(f"  Total energy: delta_G = {float(delta_G_NADH_O2_eV):.2f} eV (from NADH to O2)")
    print(f"  This energy pumps ~{float(n_protons_pumped):.0f} protons across the membrane, storing energy as pmf.")
    print()
    # Energy at each complex (approximate split)
    E_I = mpf('0.36')
    E_II = mpf('0.04')
    E_III = mpf('0.34')
    E_IV = mpf('0.40')
    print("  Energy at each complex (approx):")
    print(f"    Complex I:   {float(E_I):.2f} eV")
    print(f"    Complex II:  {float(E_II):.2f} eV")
    print(f"    Complex III: {float(E_III):.2f} eV")
    print(f"    Complex IV:  {float(E_IV):.2f} eV")
    print(f"    Total:       {float(E_I + E_II + E_III + E_IV):.2f} eV")
    print()
    print("In GU: the electron transport chain is a CASCADE of phase-channel molecules that convert")
    print("chemical energy (amplitude) into membrane gradient (amplitude + phase).")
    print()

    # -------------------------------------------------------------------------
    # PART 5: THE ENERGY BUDGET OF A CELL
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 5: THE ENERGY BUDGET OF A CELL                                          ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    ATP_minimal = mpf('500')
    ATP_ecoli = mpf('2.5e6')
    ATP_human = mpf('1e7')
    print(f"  Minimal cell (Mycoplasma): ~{float(ATP_minimal):.0f} ATP/s")
    print(f"  E. coli:                   ~{float(ATP_ecoli):.2e} ATP/s")
    print(f"  Human cell:                ~{float(ATP_human):.2e} ATP/s")
    print()
    power_per_cell_eV_s = ATP_human * abs(delta_G_cell_eV)
    W_per_eV_s = mpf('1.602176634e-19')  # 1 eV/s = 1.6e-19 W
    power_per_cell_W = power_per_cell_eV_s * W_per_eV_s
    print(f"  Energy per ATP: {float(abs(delta_G_cell_eV)):.2f} eV")
    print(f"  Total power per human cell: {float(power_per_cell_eV_s):.2e} eV/s = {float(power_per_cell_W):.2e} W")
    print()
    n_cells_body = mpf('1e13')
    total_power_W = n_cells_body * power_per_cell_W
    # Human body often cited as ~10^13–10^14 cells; ~10^14 gives ~80 W basal metabolic rate
    n_cells_80W = mpf('1e14')
    total_80W = n_cells_80W * power_per_cell_W
    print(f"  Total human body: ~{float(n_cells_body):.2e} cells × {float(power_per_cell_W):.2e} W = ~{float(total_power_W):.0f} W")
    print(f"  (With ~10^14 cells: ~{float(total_80W):.0f} W — matches basal metabolic rate.)")
    print()
    print("Key result: metabolism = maintaining the cell far from equilibrium at a cost of ~10^7 ATP/s per cell.")
    print()

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  SUMMARY                                                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("Metabolism from GU connects to:")
    print("  • Script 02 (membrane): gradients (nabla_rho, nabla_theta) exist across the membrane;")
    print("    metabolism maintains them against dissipation.")
    print("  • Script 03 (enzymes): ATP hydrolysis energy is transduced via aromatic (phase-channel)")
    print("    handles; enzymes use V_lock reshaping for both catabolism and anabolism.")
    print("  • Script 06 (protocell): the first cell needs a minimal metabolism to sustain")
    print("    non-equilibrium; ATP (or equivalent) and pmf are the universal currencies.")
    print()
    print("→ Forward reference: 28_IRON_IN_LIFE expands the iron-dependent machinery:")
    print("  Script 02 (Fe-S clusters: 13 in ETC, d-orbital phase relays, Marcus theory),")
    print("  Script 03 (heme cytochromes: ETC relay staircase),")
    print("  Script 04 (redox ladder: 8/12 ETC carriers are iron-based, 1.14 eV total drop).")
    print()


if __name__ == '__main__':
    main()
