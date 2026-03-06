#!/usr/bin/env python3
"""
BIOELECTRIC MEMORY AND THE BIOELECTRIC CODE
===========================================

PART 1: ION CHANNEL HARDWARE
- Ion channels: transmembrane proteins, pore selectively passes ions
- In GU: the channel is a VALVE in the Platonic Space (rho modulation gates theta flow)
- K+, Na+, Ca2+, Cl- selectivity and gating; Nernst and Goldman equations

PART 2: BIOELECTRIC PATTERNS (Michael Levin's bioelectric code)
- V_m as spatial pattern; proliferation, differentiation, wound healing, regeneration, cancer
- GU: theta-channel state at cellular scale

PART 3: BIOELECTRIC MEMORY
- Self-sustaining V_m ↔ gene expression loop; cellular-scale theta-channel memory

PART 4: BIOELECTRIC SIGNALING SPEED
- Timescales from channel opening to pattern persistence

PART 5: CONNECTION TO 26_PLATONIC_SPACE
- Channels = hardware, bioelectric patterns = software; theta channel at cellular scale

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

# For Nernst: E_ion (V) = (k_B*T / (z*e)) * ln([ion]_out / [ion]_in); e in eV/V = 1
# So E (V) = (k_BT/z) * ln(ratio) with k_BT in eV; E_mV = 1000 * (k_BT/z) * ln(ratio)
k_BT_mV = mpf('1000') * k_BT  # (k_BT/e) in mV at 310 K ≈ 26.7 mV


def nernst_cation(conc_out, conc_in, z=1):
    """E_ion in mV for cation. E = (k_BT/(ze)) * ln([out]/[in])."""
    return float(k_BT_mV / mpf(str(z)) * ln(mpf(str(conc_out)) / mpf(str(conc_in))))


def nernst_anion(conc_out, conc_in):
    """E_ion in mV for anion (Cl-). E = -(k_BT/e) * ln([out]/[in])."""
    return float(-k_BT_mV * ln(mpf(str(conc_out)) / mpf(str(conc_in))))


def goldman_vm(P_K, P_Na, P_Cl, K_in, K_out, Na_in, Na_out, Cl_in, Cl_out):
    """V_m in mV. Goldman: V_m = (k_BT/e)*ln((P_K*K_out+P_Na*Na_out+P_Cl*Cl_in)/(P_K*K_in+P_Na*Na_in+P_Cl*Cl_out))."""
    num = P_K * K_out + P_Na * Na_out + P_Cl * Cl_in
    den = P_K * K_in + P_Na * Na_in + P_Cl * Cl_out
    return float(k_BT_mV * ln(num / den))


def main():
    print()
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║         BIOELECTRIC MEMORY AND THE BIOELECTRIC CODE                         ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()

    # -------------------------------------------------------------------------
    # PART 1: ION CHANNEL HARDWARE
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 1: ION CHANNEL HARDWARE                                               ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("Ion channels: transmembrane proteins; pore selectively passes ions.")
    print("In GU: the channel is a VALVE in the Platonic Space (rho modulation gates theta flow).")
    print("K+ channel: selectivity filter with carbonyl oxygens mimicking K+ hydration shell (amplitude matching).")
    print("Na+ channel: tighter filter, different V_lock geometry. Ca2+ channel: dual-valve (selectivity + voltage sensor).")
    print("Gating: voltage-gated, ligand-gated, mechanically gated.")
    print()
    print("Nernst equation: E_ion = (k_B*T/(z*e)) * ln([ion]_out / [ion]_in)")
    print("Goldman equation: V_m = (k_B*T/e) * ln((P_K[K]_out + P_Na[Na]_out + P_Cl[Cl]_in) / (P_K[K]_in + P_Na[Na]_in + P_Cl[Cl]_out))")
    print()

    # Typical concentrations in mM (mammalian neuron/resting)
    K_in, K_out = 140, 5
    Na_in, Na_out = 15, 145
    Ca_in, Ca_out = 0.0001, 2
    Cl_in, Cl_out = 10, 110

    E_K = nernst_cation(K_out, K_in, 1)
    E_Na = nernst_cation(Na_out, Na_in, 1)
    E_Ca = nernst_cation(Ca_out, Ca_in, 2)
    E_Cl = nernst_anion(Cl_out, Cl_in)

    print("  Nernst potentials (typical concentrations, 310 K):")
    print(f"    k_B*T/e = {float(k_BT_mV):.2f} mV")
    print()
    print("  Ion    [in] (mM)   [out] (mM)   E_ion (mV)   (typical approx)")
    print("  ----   ---------   ----------   ----------   -----------------")
    print(f"  K+     {K_in:>6}       {K_out:>6}        {E_K:>+7.1f}      (~ -95 mV)")
    print(f"  Na+    {Na_in:>6}       {Na_out:>6}        {E_Na:>+7.1f}      (~ +67 mV)")
    print(f"  Ca2+   {Ca_in:>6.4f}    {Ca_out:>6}        {E_Ca:>+7.1f}      (~ +129 mV)")
    print(f"  Cl-    {Cl_in:>6}       {Cl_out:>6}        {E_Cl:>+7.1f}      (~ -82 mV)")
    print()

    P_K, P_Na, P_Cl = 1.0, 0.04, 0.45
    V_m = goldman_vm(mpf(P_K), mpf(P_Na), mpf(P_Cl),
                     mpf(K_in), mpf(K_out), mpf(Na_in), mpf(Na_out),
                     mpf(Cl_in), mpf(Cl_out))
    print("  Goldman (P_K : P_Na : P_Cl = 1 : 0.04 : 0.45):")
    print(f"    V_m = {V_m:.1f} mV  (typical resting ~ -70 mV)")
    print()

    # -------------------------------------------------------------------------
    # PART 2: BIOELECTRIC PATTERNS
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 2: BIOELECTRIC PATTERNS (Michael Levin's bioelectric code)              ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("A cell's V_m is NOT a single number — it's a SPATIAL PATTERN across the cell surface.")
    print("Different regions have different V_m (different channel densities and types).")
    print("V_m patterns control: proliferation, differentiation, wound healing, regeneration, cancer.")
    print()
    print("  V_m range (mV)      Cell state              GU interpretation")
    print("  ----------------    --------------------    ----------------------------------------")
    print("  -10 to -30          Proliferating (dividing) Depolarized = theta flow permissive")
    print("  -60 to -90          Quiescent                Hyperpolarized = theta channel restrained")
    print("  Pattern-dependent   Cell fate / identity    Theta-channel state specifies fate")
    print("  Injury → depolar.   Wound / repair           Restore V_m pattern = restore identity")
    print("  Regeneration        Body plan (e.g. planaria) Bioelectric pattern stores body plan")
    print("  Persistent depolar. Cancer (forgot identity) Theta-channel fixed point lost")
    print()
    print("In GU: molecular theta = nabla_theta in pi-stacking (angstrom, ps);")
    print("       cellular theta = V_m pattern (micron, hours–days);")
    print("       tissue theta = bioelectric gradients (mm–cm, days–years).")
    print()

    # -------------------------------------------------------------------------
    # PART 3: BIOELECTRIC MEMORY
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 3: BIOELECTRIC MEMORY                                                 ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("V_m patterns persist on timescales of hours to DAYS (much longer than channel openings ~ms).")
    print("Mechanism: V_m influences gene expression → gene products (channels, pumps) maintain V_m → self-sustaining loop.")
    print("This IS memory in the GU sense: a self-consistent fixed point.")
    print("Experimentally: artificially changing V_m → permanently changes cell fate (Levin lab).")
    print("Example: depolarizing frog cells that would become gut → they become brain (bioelectric reprogramming).")
    print("In GU: bioelectric memory is CELLULAR-SCALE theta-channel memory.")
    print("It sits BETWEEN genetic memory (DNA, generations) and transient signaling (seconds).")
    print("Key result: the bioelectric code is the CELLULAR manifestation of the theta channel;")
    print("it carries non-genetic, morphogenetic information that controls development and regeneration.")
    print()

    # -------------------------------------------------------------------------
    # PART 4: BIOELECTRIC SIGNALING SPEED
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 4: BIOELECTRIC SIGNALING SPEED                                        ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("  Process                              Timescale         GU niche")
    print("  ---------------------------------   ---------------   -------------------------")
    print("  Ion channel opening                 ~1 ms             Fast theta gate")
    print("  Action potential propagation        1–100 m/s         Neurons")
    print("  (non-neural propagation)            0.01–0.1 m/s      Slow bioelectric spread")
    print("  Gap junction coupling               ~ms per cell      Theta shared across cells")
    print("  Bioelectric pattern establishment   minutes–hours     Pattern = theta state")
    print("  Bioelectric pattern persistence     hours–days        Memory timescale")
    print("  ---")
    print("  DNA replication                     hours             Genetic channel")
    print("  Protein synthesis                   minutes           Downstream of genetic")
    print("  Metabolic response                  seconds           Rho (amplitude) channel")
    print()
    print("In GU: bioelectric signaling is FASTER than genetic signaling but SLOWER than metabolic —")
    print("it occupies a unique temporal niche.")
    print()

    # -------------------------------------------------------------------------
    # PART 5: CONNECTION TO 26_PLATONIC_SPACE
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  PART 5: CONNECTION TO 26_PLATONIC_SPACE                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("Script 09 of 26_PLATONIC_SPACE introduced ion channels as valves.")
    print("This script EXPANDS: channels are the hardware, bioelectric patterns are the SOFTWARE.")
    print("The pattern is stored in the DISTRIBUTION of open/closed channels across the membrane.")
    print("Like a computer: channels = transistors, V_m pattern = program state.")
    print("The bioelectric code is how the Platonic Space's theta channel manifests at cellular scale.")
    print("Key result: bioelectricity is not just electrical signaling — it is a MEMORY and INFORMATION")
    print("system that sits between the genome and the environment.")
    print()

    # -------------------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------------------
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  SUMMARY                                                                    ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print()
    print("(1) Ion channels are Platonic valves (rho gates theta); Nernst/Goldman quantify V_m.")
    print("(2) V_m is a spatial pattern (bioelectric code) controlling proliferation, fate, repair, regeneration.")
    print("(3) Bioelectric memory is a self-sustaining V_m ↔ gene-expression fixed point (hours–days).")
    print("(4) Bioelectric timescales sit between metabolic (seconds) and genetic (hours+).")
    print("(5) Bioelectricity = cellular-scale theta channel: memory and information between genome and environment.")
    print()


if __name__ == "__main__":
    main()
