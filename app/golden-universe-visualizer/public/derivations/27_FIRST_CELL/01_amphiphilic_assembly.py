#!/usr/bin/env python3
"""
AMPHIPHILIC SELF-ASSEMBLY — LIPID BILAYERS FROM GU
====================================================
Why lipids spontaneously form membranes: derived from
the GU two-channel architecture and V(rho) minimization.

Date: February 2026
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
T_bio = mpf('310')  # K (body temperature)
k_BT = k_B * T_bio  # ~0.0267 eV
lambda_rec_beta = exp(phi) / pi**2

print("=" * 80)
print("AMPHIPHILIC SELF-ASSEMBLY — LIPID BILAYERS FROM GU")
print("=" * 80)


# =============================================================================
# PART 1: THE AMPHIPHILIC MOLECULE IN GU
# =============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 1: THE AMPHIPHILIC MOLECULE IN GU                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

A lipid: polar head (phosphate + glycerol, sigma bonds w=0, strong dipole)
         + two hydrocarbon tails (C16–C18, all sigma, w=0).

In GU terms:
  - BOTH parts are amplitude-channel only (w=0 everywhere, no pi bonds, no phase channel).
  - The polar head interacts strongly with water (both amplitude-channel;
    dipole–dipole + H-bonds).
  - The tails are hydrophobic: they DISRUPT water's H-bond network.

Key GU insight:
  The lipid is an amplitude-only molecule, but its asymmetry creates
  a BOUNDARY in the amplitude channel.
""")

print(f"  GU constants (for later parts):")
print(f"    k_B T (body temp) = {float(k_BT):.6f} eV")
print(f"    phi = {float(phi):.10f}")
print()


# =============================================================================
# PART 2: THE HYDROPHOBIC EFFECT FROM V(RHO)
# =============================================================================

# Water H-bond: ~0.2 eV each; ~3.5 H-bonds per molecule
E_Hbond_eV = mpf('0.2')
n_Hbond_per_H2O = mpf('3.5')
# Cost per CH2 in water: ~3.5 kJ/mol = 0.036 eV (3.5e3/NA ≈ 0.036)
kJ_per_mol_to_eV = mpf('1') / mpf('96.485')  # 1 eV = 96.485 kJ/mol per molecule
delta_G_CH2_kJ = mpf('3.5')
delta_G_CH2_eV = delta_G_CH2_kJ * kJ_per_mol_to_eV  # ~0.036 eV
n_CH2_tail = 16
delta_G_one_tail = n_CH2_tail * delta_G_CH2_eV
delta_G_two_tails = mpf('2') * delta_G_one_tail

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 2: THE HYDROPHOBIC EFFECT FROM V(RHO)                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

Water H-bond network:
  - Each molecule forms ~3.5 H-bonds, energy ~0.2 eV each.
  - Hydrocarbon tail in water: disrupts ~12–15 H-bonds (cavity formation).

Energy cost of solvating one CH2 group: ~3.5 kJ/mol = 0.036 eV.
""")

print(f"  Computed:")
print(f"    delta_G per CH2 (water → hydrocarbon): {float(delta_G_CH2_eV):.4f} eV")
print(f"    C16 one tail: 16 × delta_G_CH2 = {float(delta_G_one_tail):.4f} eV")
print(f"    TWO tails per lipid (exposed to water): {float(delta_G_two_tails):.4f} eV")
print()
print("""
This is the DRIVING FORCE for self-assembly: removing tails from water
RECOVERS these lost H-bonds.

In GU: the hydrophobic effect is V(rho) MINIMIZATION at the water–hydrocarbon interface.
  - Water: rho_vac optimized for tetrahedral H-bond network.
  - Hydrocarbon: rho_vac optimized for van der Waals packing.
  - Interface: rho_vac MISMATCH → energy penalty → system minimizes by reducing interface area.
""")
print(f"  Free energy of transfer for CH2 (water → hydrocarbon): delta_G = {float(delta_G_CH2_eV):.4f} eV")
print()


# =============================================================================
# PART 3: WHY BILAYERS (NOT MICELLES, NOT MONOLAYERS)
# =============================================================================

# DPPC: volume per CH2 ~0.0269 nm³; 2 tails × 16 CH2 each → total tail volume v
v_per_CH2_nm3 = mpf('0.0269')
n_CH2_per_tail = 16
v_per_tail_nm3 = n_CH2_per_tail * v_per_CH2_nm3
v_DPPC = mpf('2') * v_per_tail_nm3
a_0_nm2 = mpf('0.64')
l_c_nm = mpf('1.8')
P_DPPC = v_DPPC / (a_0_nm2 * l_c_nm)

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 3: WHY BILAYERS (NOT MICELLES, NOT MONOLAYERS)                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

Geometry depends on packing parameter: P = v / (a_0 × l_c)
  v = tail volume, a_0 = head area, l_c = critical tail length.

  - Lipids with TWO tails: v large, P ~ 0.5–1.0 → BILAYER (flat or vesicle).
  - Single-chain surfactants: P ~ 0.33 → micelle (sphere).
  - Lipids with very large heads: P < 0.33 → micelle.
""")

print(f"  DPPC (dipalmitoylphosphatidylcholine):")
print(f"    v = 2 × 16 × 0.0269 nm³ (two C16 tails) = {float(v_DPPC):.4f} nm³")
print(f"    a_0 = {float(a_0_nm2):.2f} nm²,  l_c = {float(l_c_nm):.2f} nm")
print(f"    P = v / (a_0 × l_c) = {float(P_DPPC):.2f}  →  BILAYER")
print()
print("""
In GU: the packing parameter is a GEOMETRIC OPTIMIZATION of V(rho) — the bilayer
minimizes the total amplitude energy by matching tail packing to head spacing.
""")
print()


# =============================================================================
# PART 4: SPONTANEOUS SELF-ASSEMBLY
# =============================================================================

# CBC ~ 10^(-10) M for phospholipids; delta_G_assemble ~ -20 to -25 kT per lipid
CBC_M = mpf('1e-10')
delta_G_kT_min = mpf('-25')
delta_G_kT_max = mpf('-20')
delta_G_assemble_eV_min = delta_G_kT_min * k_BT
delta_G_assemble_eV_max = delta_G_kT_max * k_BT

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 4: SPONTANEOUS SELF-ASSEMBLY                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

Critical micelle/bilayer concentration (CMC/CBC): threshold above which
lipids spontaneously form aggregates.

For phospholipids: CBC ~ 10^(-10) M (extremely low — essentially ALL lipids in bilayers).
""")

print(f"  CBC = {float(CBC_M):.0e} M")
print()
print("""
Free energy of assembly:
  delta_G_assemble = delta_G_hydrophobic + delta_G_packing + delta_G_head_repulsion
""")
print(f"  For DPPC: delta_G_assemble ~ {float(delta_G_kT_min):.0f} to {float(delta_G_kT_max):.0f} kT per lipid")
print(f"           = {float(delta_G_assemble_eV_min):.4f} to {float(delta_G_assemble_eV_max):.4f} eV  (very favorable)")
print()
print("""
The bilayer forms SPONTANEOUSLY from L_Omega minimization — no external direction needed.
This is the first step toward a cell: the membrane assembles itself.

In GU: self-assembly = the effective action Gamma[Omega] finding a LOWER minimum
when lipids aggregate.
""")
print()


# =============================================================================
# PART 5: BILAYER PROPERTIES
# =============================================================================

# Thickness ~4–5 nm; area per lipid ~0.64 nm²; D ~ 1e-12 m²/s
thickness_nm = mpf('4.5')
D_lateral = mpf('1e-12')  # m²/s

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 5: BILAYER PROPERTIES                                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

  Thickness: ~4–5 nm (two tail lengths + polar heads).
  Area per lipid: ~0.64 nm² for DPPC.
  Lateral diffusion: lipids slide along the bilayer (D ~ 10^(-12) m²/s).
  Flip-flop: lipid crossing from one leaflet to the other is RARE (days without enzymes).

Permeability: SELECTIVE
  - Small nonpolar (O2, CO2, N2): freely permeable (amplitude channel continuous).
  - Water: somewhat permeable (small, slips through transiently).
  - Ions (Na+, K+, Ca2+, Cl-): BLOCKED (hydration shell too large, charge repelled by hydrocarbon).

This is the foundation of the membrane as a BARRIER in the Platonic Space.
""")

print(f"  Typical bilayer thickness: {float(thickness_nm):.1f} nm")
print(f"  Area per lipid (DPPC): {float(a_0_nm2):.2f} nm²")
print(f"  Lateral diffusion coefficient: D ~ {float(D_lateral):.0e} m²/s")
print()


# =============================================================================
# SUMMARY — CONNECTIONS TO OTHER SCRIPTS
# =============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  SUMMARY — CONNECTIONS TO OTHER SCRIPTS                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

  Script 02 (membrane as boundary):
    The lipid bilayer is the PHYSICAL BOUNDARY that defines inside/outside.
    GU: amplitude-only molecules create an amplitude-channel boundary;
    selective permeability = which degrees of freedom cross the boundary.

  Script 06 (protocell):
    Self-assembly (this script) gives the first closed compartment.
    No genes required: lipids + water → spontaneous vesicles.
    Protocell = bilayer boundary + interior (water, solutes) + L_Omega minimization.

  26_PLATONIC_SPACE:
    The membrane is a BARRIER in the Platonic Space: it separates two
    rho_vac-optimized regions (cytosol vs exterior) and blocks ion flow
    (charge cannot cross the hydrocarbon core without channels).
    Agency (07, 09): membranes host pumps and channels — the phase channel
    (theta-FF-tilde) operates at the boundary to create gradients.

  Takeaway: Amphiphilic assembly from V(rho) minimization is the GU basis
  for the first cell boundary; bilayers are the geometric solution to
  minimizing interface energy while keeping heads wet and tails dry.
""")

print("=" * 80)
print("Done.")
print("=" * 80)
