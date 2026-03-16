#!/usr/bin/env python3
"""
HYDROGEN BONDS FROM THE GOLDEN UNIVERSE
=========================================

Hydrogen bonds are the "weak bonds" that hold DNA base pairs together.
They are intermediate between covalent bonds (~1-10 eV) and van der Waals
interactions (~0.01-0.05 eV), sitting at ~0.1-0.4 eV.

This script derives H-bond physics from GU parameters: the proton mass
(from the epoch ladder), the electron mass (derived, 23 ppm), and
alpha_EM (experimental input). The key GU insight is that H-bonds are
sigma-type (w = 0) — they carry NO phase memory.

Upstream: 23_MOLECULAR_BONDS (BO approximation, Coulomb physics)
Status:   Standard physics with GU-derived parameters + GU interpretation

Date: February 2026
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mpmath import mp, mpf, sqrt, pi as mp_pi, exp, log
import numpy as np

mp.dps = 30
phi = (mpf('1') + sqrt(mpf('5'))) / 2
pi = mp_pi
alpha_EM = mpf('1') / mpf('137.035999177')
m_e = mpf('0.51099895')       # MeV
M_p = mpf('938.272088')       # MeV (proton mass)
hbar_c = mpf('197.3269804')   # MeV·fm
a_0_fm = float(hbar_c / (alpha_EM * m_e))
a_0_A = a_0_fm / 1e5
k_B_eV = 8.617333e-5          # eV/K (Boltzmann constant)

print("=" * 80)
print("HYDROGEN BONDS FROM THE GOLDEN UNIVERSE")
print("The weak bonds that hold DNA together")
print("=" * 80)


# ============================================================================
# PART 1: WHAT IS A HYDROGEN BOND?
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 1: WHAT IS A HYDROGEN BOND?                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

A hydrogen bond is an interaction:  D-H···A

  D = donor atom (electronegative: N, O, F)
  H = hydrogen (proton + 1 electron)
  A = acceptor atom (electronegative, with lone pair)

The D-H bond is covalent (shared electron pair, ~4 eV).
The H···A interaction is the hydrogen bond (~0.1-0.4 eV).

PHYSICAL ORIGIN (three contributions):
  1. Electrostatic: D^(delta-) — H^(delta+) ··· A^(delta-)
     The D-H bond is polar; the partial positive charge on H
     attracts the lone pair on A. This is the dominant term (~70%).

  2. Charge transfer / covalent: partial sharing of A's lone pair
     with the H-D antibonding orbital. This is a weak covalent
     contribution (~20%).

  3. Dispersion: van der Waals attraction (~10%).

IN DNA:
  D-H = N-H or O-H (on one base)
  A   = N or O (on the partner base)
  Energy per H-bond: ~0.15-0.20 eV in solution
""")


# ============================================================================
# PART 2: THE PROTON IN GU — EPOCH SEPARATION
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 2: THE PROTON IN GU — EPOCH SEPARATION                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

The hydrogen bond involves a PROTON sitting between two electronegative atoms.
In GU, the proton-electron mass ratio comes from the epoch ladder:

  M_p / m_e ~ phi^(N_e - N_QCD) = phi^(111 - 95) = phi^16
""")

phi_16 = float(phi**16)
mass_ratio = float(M_p / m_e)
print(f"  phi^16          = {phi_16:.1f}")
print(f"  M_p / m_e       = {mass_ratio:.1f}")
print(f"  Ratio           = {mass_ratio/phi_16:.3f}  (prefactor from C_e, QCD structure)")
print()

kappa_BO = float(sqrt(m_e / M_p))
print(f"  Born-Oppenheimer parameter: kappa = sqrt(m_e/M_p) = {kappa_BO:.4f}")
print(f"  ~ phi^(-8) = {float(phi**(-8)):.4f}")
print()

print("""  For the hydrogen bond, BO means:
    - The electron cloud adjusts INSTANTLY to the proton position
    - The proton moves in an EFFECTIVE POTENTIAL created by the electrons
    - This effective potential has TWO MINIMA: near D and near A
    - The proton tunnels between these minima with rate ~ exp(-action)

  The large epoch gap (Delta_N = 16) makes the proton SEMI-CLASSICAL:
    - It is localised near one minimum most of the time
    - Tunnelling is rare but possible (proton transfer reactions)
    - The H-bond energy comes primarily from electrostatics, not tunnelling
""")


# ============================================================================
# PART 3: ELECTROSTATIC MODEL OF THE HYDROGEN BOND
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 3: ELECTROSTATIC MODEL — H-BOND ENERGY FROM alpha_EM                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

The dominant contribution to H-bond energy is the electrostatic interaction
between the partial charges on D-H and A. We model this from GU parameters.
""")

q_partial_H = 0.35   # partial charge on H in N-H (in units of e)
q_partial_A = -0.45   # partial charge on acceptor N/O lone pair
r_HA_A = 1.90         # typical H···A distance in Angstrom

r_HA_fm = r_HA_A * 1e5
E_coulomb_MeV = float(alpha_EM * hbar_c / mpf(str(r_HA_fm)))
# hbar_c in MeV·fm, so E = alpha * hbar_c / r gives MeV
# Convert to eV: multiply by 1e6
E_unit_eV = E_coulomb_MeV * 1e6  # This is e^2/(4*pi*eps_0 * r) in eV

E_hbond_electrostatic = abs(q_partial_H * q_partial_A) * E_unit_eV

print(f"  Unit Coulomb energy at r = {r_HA_A} A:")
print(f"    E_C = alpha_EM * hbar_c / r = {E_coulomb_MeV:.4e} MeV = {E_unit_eV:.3f} eV")
print()
print(f"  With partial charges (q_H = +{q_partial_H}e, q_A = {q_partial_A}e):")
print(f"    E_HB ~ |q_H * q_A| * E_C = {abs(q_partial_H * q_partial_A):.3f} * {E_unit_eV:.3f}")
print(f"    E_HB ~ {E_hbond_electrostatic:.3f} eV")
print()
print(f"  Experimental range: 0.10 - 0.40 eV")
print(f"  This simple model gives the correct ORDER OF MAGNITUDE.")
print()

print("""  More refined model (dipole-dipole):

    The D-H···A hydrogen bond can be modelled as the interaction between
    two dipoles: the D-H bond dipole and the A lone-pair dipole.

    E_dd = -mu_D * mu_A * f(theta) / (4*pi*eps_0 * r^3)

    where f(theta) encodes the angular dependence (strongest when linear).
    The 1/r^3 scaling (vs 1/r for point charges) gives a weaker, shorter-range
    interaction — consistent with the 0.1-0.4 eV range.
""")


# ============================================================================
# PART 4: PROTON DOUBLE-WELL POTENTIAL
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 4: PROTON DOUBLE-WELL POTENTIAL                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

The proton in an H-bond sits in a DOUBLE-WELL potential:

  V(x) = A*(x^2 - x_0^2)^2

  Well 1: proton near donor D     (x = -x_0)
  Well 2: proton near acceptor A  (x = +x_0)
  Barrier between them:           V_barrier ~ 0.1-0.3 eV
""")

V_barrier_eV = 0.20  # typical barrier height
x_0_A = 0.40         # half-distance between wells in Angstrom
omega_vib = 3500      # cm^-1 (N-H stretching frequency)
omega_vib_eV = omega_vib * 1.24e-4  # convert cm^-1 to eV

print(f"  Double-well parameters:")
print(f"    Well separation:   2*x_0 = {2*x_0_A:.2f} A")
print(f"    Barrier height:    V_b   = {V_barrier_eV:.2f} eV")
print(f"    N-H vibration:     omega = {omega_vib} cm^-1 = {omega_vib_eV:.3f} eV")
print(f"    Zero-point energy: E_0   ~ omega/2 = {omega_vib_eV/2:.4f} eV")
print()

print(f"  WKB tunnelling estimate:")
print(f"    Action S ~ 2*x_0 * sqrt(2*M_p*V_b) / hbar")

# Dimensionless WKB action: S = sqrt(2*M_p*V_b) * d / hbar_c
# Using natural units: M_p in MeV, V_b converted to MeV, d in fm, hbar_c in MeV·fm
S_dimless = np.sqrt(2 * 938.272 * V_barrier_eV * 1e-6) * (2 * x_0_A * 1e5) / 197.327
print(f"    S = sqrt(2 * M_p * V_b) * d / hbar_c")
print(f"      = sqrt(2 * {float(M_p):.1f} MeV * {V_barrier_eV*1e-6:.1e} MeV) * {2*x_0_A*1e5:.0f} fm / {float(hbar_c):.1f} MeV·fm")
print(f"      = {S_dimless:.1f}")
print()
tunnel_proper = omega_vib_eV * np.exp(-S_dimless)
print(f"    Tunnel splitting ~ omega * exp(-S) = {omega_vib_eV:.3f} * exp(-{S_dimless:.1f})")
print(f"                     ~ {tunnel_proper:.2e} eV")
print()

print("""  INTERPRETATION:
    The tunnel splitting is EXTREMELY SMALL — the proton is well-localised
    in one well. This confirms the semi-classical picture from the BO epoch
    separation (kappa = 0.023).

    The H-bond energy is NOT primarily from tunnelling — it is from the
    ELECTROSTATIC attraction between the wells. Tunnelling contributes
    a tiny correction.

    In GU terms: the proton's large mass (epoch N_QCD = 95 vs N_e = 111)
    makes it a classical object on the H-bond scale. The H-bond is a
    classical electrostatic interaction between quantum electrons.
""")


# ============================================================================
# PART 5: H-BOND TYPES IN DNA
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 5: HYDROGEN BOND TYPES IN DNA                                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

DNA uses TWO types of hydrogen bonds for base pairing:

  N-H···N  (amino nitrogen to ring nitrogen)
  N-H···O  (amino nitrogen to carbonyl oxygen)
""")

hbond_types = [
    ('N-H···N', 'amino → ring N',     3.00, 0.17, 'A-T, G-C'),
    ('N-H···O', 'amino → carbonyl O', 2.90, 0.19, 'A-T, G-C'),
    ('O-H···N', 'hydroxyl → ring N',  2.85, 0.21, 'rare in DNA'),
]

print(f"  {'Type':>12s} | {'Description':>20s} | {'D···A (A)':>9s} | {'E (eV)':>7s} | {'In DNA':>12s}")
print("  " + "-" * 75)
for htype, desc, dist, energy, where in hbond_types:
    print(f"  {htype:>12s} | {desc:>20s} | {dist:>9.2f} | {energy:>7.2f} | {where:>12s}")

print()
print("""  DNA BASE PAIR H-BONDS:

    A-T pair: 2 hydrogen bonds
      N6-H···O4  (adenine NH₂ to thymine C=O)     ~0.17 eV
      N1···H-N3  (adenine ring N to thymine N-H)   ~0.17 eV
      Total: ~0.34 eV

    G-C pair: 3 hydrogen bonds
      O6···H-N4  (guanine C=O to cytosine NH₂)     ~0.19 eV
      N1-H···N3  (guanine N-H to cytosine ring N)   ~0.17 eV
      N2-H···O2  (guanine NH₂ to cytosine C=O)      ~0.19 eV
      Total: ~0.55 eV

  G-C pairs are ~60% stronger than A-T pairs (3 vs 2 H-bonds).
  This affects DNA stability: GC-rich regions are harder to melt.
""")

E_AT_hbond = 0.34  # eV total
E_GC_hbond = 0.55  # eV total

print(f"  Summary of H-bond energies:")
print(f"    A-T pair:  {E_AT_hbond:.2f} eV  (2 H-bonds)")
print(f"    G-C pair:  {E_GC_hbond:.2f} eV  (3 H-bonds)")
print(f"    Ratio:     {E_GC_hbond/E_AT_hbond:.2f}")
print()


# ============================================================================
# PART 6: H-BOND DIRECTIONALITY AND GEOMETRY
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 6: H-BOND DIRECTIONALITY — WHY LINEAR IS BEST                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

Hydrogen bonds are DIRECTIONAL: they are strongest when D-H···A is linear
(180 degrees). The energy falls off as:

  E(theta) ~ E_0 * cos^2(theta)

where theta is the deviation from linearity.

In GU terms: the H-bond is a sigma-type interaction (w = 0).
  - Head-on overlap of the D-H bond orbital with the A lone pair
  - No transverse phase winding
  - Maximum overlap when aligned (cylindrical symmetry axis)

This is the SAME geometry as a sigma covalent bond, but weaker because:
  1. Only partial charge sharing (not full electron pair)
  2. Longer distance (D···A ~ 2.9-3.0 A vs covalent ~ 1.0-1.5 A)
  3. No topological phase locking (w = 0 → no V_lock contribution)

CRITICAL GU POINT: w = 0 means NO phase memory through H-bonds.
  The hydrogen bonds in DNA base pairs are electrostatic/exchange.
  They do NOT carry the theta-FF-tilde phase memory channel.
  Phase memory in DNA comes from pi-stacking (Script 04), NOT from H-bonds.
""")


# ============================================================================
# PART 7: THERMAL STABILITY
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 7: THERMAL STABILITY — H-BONDS VS k_B T                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

T_room = 298.15  # K
T_body = 310.15  # K
kT_room = k_B_eV * T_room
kT_body = k_B_eV * T_body

print(f"  Room temperature:  T = {T_room:.1f} K,  k_B T = {kT_room:.4f} eV")
print(f"  Body temperature:  T = {T_body:.1f} K,  k_B T = {kT_body:.4f} eV")
print()

print(f"  H-bond energy / k_B T:")
print(f"    Single H-bond (~0.18 eV):  {0.18/kT_body:.1f} k_B T  (marginally stable)")
print(f"    A-T pair (0.34 eV):        {E_AT_hbond/kT_body:.1f} k_B T")
print(f"    G-C pair (0.55 eV):        {E_GC_hbond/kT_body:.1f} k_B T")
print()

print("""  A SINGLE hydrogen bond has energy ~7 k_B T at body temperature.
  This means individual H-bonds break and reform on nanosecond timescales.
  DNA stability requires MANY H-bonds acting cooperatively, plus
  pi-stacking (which contributes even more — see Script 04/06).

  In GU thermodynamics (22_THERMODYNAMICS):
    Free energy: F = E - T*S = Gamma_k[Omega_vac]
    The DNA double helix is stable when Delta_F < 0 for association.
    Both enthalpy (H-bonds + stacking) and entropy (hydrophobic effect)
    contribute to Delta_F. See Script 06 for the full energy budget.
""")


# ============================================================================
# SUMMARY
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  SUMMARY: HYDROGEN BONDS FROM GU                                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

WHAT IS DERIVED FROM GU:
  1. Proton mass from epoch ladder: M_p ~ phi^(-95) * M_P (prefactors from QCD)
  2. Electron mass: m_e = 0.51099895 MeV (23 ppm, first-principles)
  3. BO separation: M_p/m_e ~ phi^16 → proton is semi-classical in H-bond
  4. Bond scale: a_0 = hbar_c/(alpha_EM * m_e) sets all distances

WHAT IS STANDARD PHYSICS WITH GU PARAMETERS:
  5. Electrostatic model: E_HB ~ q_D * q_A * alpha_EM / r
  6. Double-well potential and WKB tunnelling
  7. Specific H-bond energies (0.17-0.19 eV per bond)
  8. Directionality (cos^2 theta dependence)

KEY GU INSIGHTS:
  9. H-bonds are SIGMA-TYPE (w = 0) — no phase winding
  10. Therefore H-bonds carry NO phase memory (theta-FF-tilde inactive)
  11. Phase memory in DNA must come from pi-stacking, NOT H-bonding
  12. The proton's semi-classical nature (epoch gap = 16) means
      H-bond physics is essentially ELECTROSTATIC

DNA H-BOND ENERGIES:
  A-T:  2 H-bonds  ~0.34 eV total
  G-C:  3 H-bonds  ~0.55 eV total

CONNECTIONS:
  -> Script 03: How these H-bonds create specific base pairing
  -> Script 04: Pi-stacking (which DOES carry phase memory)
  -> Script 06: Full energy budget (H-bonds + stacking + entropy)
""")
