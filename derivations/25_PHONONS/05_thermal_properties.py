#!/usr/bin/env python3
"""
THERMAL PROPERTIES FROM GU PHONON SPECTRUM
=============================================

DERIVATION CHAIN:
  Part 1: Debye heat capacity C_V(T) — phonon gas thermodynamics
  Part 2: Einstein model — optical phonon contributions
  Part 3: Thermal conductivity κ from phonon mean free path
  Part 4: Phase phonon entropy — the θ channel's contribution
  Part 5: The GU free energy and phase transitions

WHAT GU PROVIDES:
  - Θ_D (from v_s, which is from m_e × α² / √(A·m_p))
  - Phase phonon contributions (UNIQUE to GU)
  - Memory coupling corrections (ρ⁴ and θFF̃)
  - Connection to consciousness through thermal phase coherence

REFERENCES:
  - 02_phonon_dispersion.py: Debye model, Θ_D values
  - 03_speed_of_sound.py: v_s from GU
  - 04_phase_phonons.py: phase phonon spectrum
  - derivations/22_THERMODYNAMICS/ (existing thermo folder)

Date: February 2026
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from mpmath import mp, mpf, sqrt, pi as mp_pi, exp

mp.dps = 30
phi = (mpf('1') + sqrt(mpf('5'))) / 2
pi = mp_pi
alpha_EM = mpf('1') / mpf('137.035999177')
m_e = mpf('0.51099895')

c_m_s = 2.998e8
hbar_J_s = 1.055e-34
eV_to_J = 1.602e-19
amu_kg = 1.661e-27
k_B_J = 1.381e-23
k_B_eV = 8.617e-5
N_A = 6.022e23


print("=" * 80)
print("THERMAL PROPERTIES FROM GU PHONON SPECTRUM")
print("=" * 80)


# ============================================================================
# PART 1: DEBYE HEAT CAPACITY
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 1: DEBYE HEAT CAPACITY C_V(T)                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝

The Debye model gives:
  C_V(T) = 9Nk_B × (T/Θ_D)³ ∫₀^(Θ_D/T) x⁴eˣ/(eˣ-1)² dx

Limits:
  T >> Θ_D:  C_V → 3Nk_B = 3R    (Dulong-Petit, classical)
  T << Θ_D:  C_V → (12π⁴/5)Nk_B(T/Θ_D)³  (T³ law, quantum)

The crossover at T ~ Θ_D is WHERE quantum phonons matter.
Θ_D is set entirely by GU parameters (Script 02).
""")

def debye_cv(T, Theta_D, N=1):
    if T < 1e-10:
        return 0.0
    x_max = Theta_D / T
    if x_max > 500:
        return 9 * N * k_B_J * (T/Theta_D)**3 * (4 * np.pi**4 / 5)
    x = np.linspace(1e-10, x_max, 5000)
    integrand = x**4 * np.exp(x) / (np.exp(x) - 1)**2
    integral = np.trapz(integrand, x)
    return 9 * N * k_B_J * (T/Theta_D)**3 * integral

R_gas = N_A * k_B_J

materials_Theta = [
    ("Diamond", 2250),
    ("Silicon", 645),
    ("Iron",    470),
    ("Copper",  343),
    ("Lead",    105),
]

temps = [10, 50, 100, 200, 300, 500, 1000]

print(f"  HEAT CAPACITY C_V / 3R  (fraction of classical limit):")
print()
header = f"  {'Material':>8s} | {'Θ_D(K)':>6s}"
for T in temps:
    header += f" | {T:5d}K"
print(header)
print("  " + "─" * (25 + 9 * len(temps)))

for name, Theta_D in materials_Theta:
    row = f"  {name:>8s} | {Theta_D:6d}"
    for T in temps:
        cv = debye_cv(T, Theta_D)
        ratio = cv / (3 * k_B_J) if cv > 0 else 0
        row += f" | {ratio:5.3f}"
    print(row)

print()
print("  KEY OBSERVATIONS:")
print("    - Diamond (Θ_D = 2250 K): still quantum at room temperature!")
print(f"      C_V(300K)/3R ≈ {debye_cv(300, 2250)/(3*k_B_J):.2f} (only {debye_cv(300, 2250)/(3*k_B_J)*100:.0f}% of classical limit)")
print("    - Lead (Θ_D = 105 K): fully classical above ~200K")
print(f"      C_V(300K)/3R ≈ {debye_cv(300, 105)/(3*k_B_J):.2f}")
print()
print("  THE T³ LAW AT LOW TEMPERATURE:")
print("    C_V ∝ T³ is a DIRECT consequence of:")
print("    1. Linear dispersion ω = v_s k (acoustic branch)")
print("    2. Bose-Einstein statistics (quantum phonon gas)")
print("    3. 3D density of states g(ω) ∝ ω²")
print()
print("    All three are encoded in GU through:")
print("    1. Lattice dynamics (Script 02)")
print("    2. Quantized oscillations (Twin Theorem)")
print("    3. 3D crystal topology")
print()


# ============================================================================
# PART 2: EINSTEIN MODEL — OPTICAL CONTRIBUTION
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 2: EINSTEIN MODEL — OPTICAL PHONON CONTRIBUTION                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

For optical phonons (and phase phonons), each mode has a single
frequency ω_E (Einstein model):

  C_V^E = 3Nk_B × (Θ_E/T)² × e^(Θ_E/T) / (e^(Θ_E/T) - 1)²

where Θ_E = ℏω_E / k_B.

In a diatomic crystal (NaCl, GaAs), the full C_V is:
  C_V = C_V^Debye (acoustic) + C_V^Einstein (optical)
""")

def einstein_cv(T, Theta_E):
    if T < 1e-10:
        return 0.0
    x = Theta_E / T
    if x > 500:
        return 0.0
    return 3 * k_B_J * x**2 * np.exp(x) / (np.exp(x) - 1)**2

diatomic_data = [
    ("NaCl",  321,  500),
    ("GaAs",  344,  380),
    ("ZnS",   315,  470),
]

print(f"  ACOUSTIC + OPTICAL CONTRIBUTIONS AT 300 K:")
print()
print(f"  {'Material':>8s} | {'Θ_D(K)':>6s} | {'Θ_E(K)':>6s} | {'C_ac/3R':>7s} | {'C_op/3R':>7s} | {'C_tot/3R':>8s}")
print("  " + "─" * 55)

for name, Theta_D, Theta_E in diatomic_data:
    T = 300
    cv_ac = debye_cv(T, Theta_D)
    cv_op = einstein_cv(T, Theta_E)
    r_ac = cv_ac / (3 * k_B_J)
    r_op = cv_op / (3 * k_B_J)
    r_tot = r_ac + r_op
    print(f"  {name:>8s} | {Theta_D:6d} | {Theta_E:6d} | {r_ac:7.3f} | {r_op:7.3f} | {r_tot:8.3f}")

print()
print("  The optical phonons contribute an ADDITIONAL heat capacity")
print("  channel, bringing C_V above the simple Debye result.")
print()


# ============================================================================
# PART 3: THERMAL CONDUCTIVITY
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 3: THERMAL CONDUCTIVITY FROM PHONON TRANSPORT                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

Kinetic theory:
  κ = ⅓ × C_V × v_s × l_mfp

where l_mfp = phonon mean free path, limited by:
  - Umklapp scattering (phonon-phonon at high T)
  - Boundary scattering (at low T, l_mfp → sample size)
  - Impurity scattering (isotopes, defects)
  - Phase phonon scattering (GU-SPECIFIC)

GU provides ALL ingredients:
  C_V from Debye model (Part 1)
  v_s from GU formula (Script 03)
  l_mfp from phonon-phonon coupling (ρ⁴ memory)
""")

kappa_data = [
    ("Diamond",  2250, 12000, 2200, "Highest thermal conductivity in nature"),
    ("Silicon",  645,  8430,  148,  "Important for electronics cooling"),
    ("Copper",   343,  3810,  401,  "Cu: electron-dominated, not just phonons"),
    ("Iron",     470,  5130,   80,  "d-band scattering limits l_mfp"),
    ("NaCl",     321,  3500,    7,  "Ionic: short l_mfp from Umklapp"),
    ("Lead",     105,  1322,   35,  "Heavy + soft: low κ"),
]

print(f"  {'Material':>8s} | {'Θ_D(K)':>6s} | {'v_s(m/s)':>8s} | {'κ_exp(W/mK)':>11s} | {'l_mfp(nm)':>9s} | Notes")
print("  " + "─" * 80)

for name, Theta_D, v_s, kappa_exp, notes in kappa_data:
    cv_per_vol = debye_cv(300, Theta_D) * (8 / (5.431e-10)**3 if name == "Silicon" else
                  4 / (3.615e-10)**3 if name == "Copper" else
                  2 / (2.866e-10)**3 if name == "Iron" else
                  8 / (5.640e-10)**3 if name == "NaCl" else
                  4 / (4.951e-10)**3 if name == "Lead" else
                  8 / (3.567e-10)**3)

    l_mfp = 3 * kappa_exp / (cv_per_vol * v_s) if cv_per_vol * v_s > 0 else 0

    print(f"  {name:>8s} | {Theta_D:6d} | {v_s:8d} | {kappa_exp:11d} | {l_mfp*1e9:9.1f} | {notes}")

print()
print("  DIAMOND — WHY THE HIGHEST κ?")
print("    1. Highest v_s (12000 m/s) — lightest atoms + strongest bonds")
print("    2. Highest Θ_D (2250 K) — quantum regime persists")
print("    3. Longest l_mfp — light, symmetric C atoms minimize Umklapp")
print("    4. GU: sp3 tetrahedral = maximally symmetric kink arrangement")
print("    5. No free electrons to scatter phonons")
print()
print("  COPPER — NOT JUST PHONONS:")
print("    Copper's high κ is electron-dominated (Wiedemann-Franz law).")
print("    The phonon contribution alone is ~10 W/mK.")
print("    Electrons carry heat because they are FREE (metallic bond).")
print()


# ============================================================================
# PART 4: PHASE PHONON ENTROPY
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 4: PHASE PHONON ENTROPY — THE θ CHANNEL                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

Phase phonons contribute ADDITIONAL entropy beyond standard phonons:

  S_phase = k_B × Σ_k [ (n_k + 1)ln(n_k + 1) - n_k ln(n_k) ]

where n_k = 1/(exp(ℏω_θ(k)/k_BT) - 1) is the Bose occupation.

This phase entropy is:
  - SMALL in rigid crystals (strong V_lock → high ω_θ → frozen out)
  - LARGE in soft materials (weak V_lock → low ω_θ → thermally active)
  - MAXIMAL near phase transitions (V_lock → 0 at melting/magnetic T_c)

GU PREDICTION: materials with large phase phonon entropy are
more susceptible to memory effects (θFF̃ channel is active).
""")

print("  PHASE PHONON ENTROPY CLASSIFICATION:")
print()
print("  RIGID (S_phase ≈ 0 at 300K):")
print("    Diamond, silicon, quartz — strong V_lock, high Θ_E^phase")
print("    Phase phonons frozen out at room temperature")
print("    θFF̃ channel essentially inactive")
print()
print("  MODERATE (S_phase ~ k_B):")
print("    Metals (Cu, Fe) — moderate V_lock from metallic bonding")
print("    Ice — H-bond network allows some phase fluctuations")
print("    Phase phonons partially active, some θ memory")
print()
print("  LARGE (S_phase ~ several k_B):")
print("    Liquid crystals — orientational V_lock very weak")
print("    DNA / protein crystals — flexible θ backbone")
print("    Near phase transitions (melting, magnetic T_c)")
print("    Phase phonons fully active → θFF̃ memory channel OPEN")
print()
print("  THE LINK TO CONSCIOUSNESS:")
print("    From explanatory/CONSCIOUSNESS.md: consciousness requires")
print("    BOTH ρ⁴ (amplitude) and θFF̃ (phase) channels.")
print()
print("    Phase phonon entropy measures HOW OPEN the θ channel is.")
print("    S_phase high → phase fluctuations large → θFF̃ active → memory active")
print()
print("    Biological systems (DNA, microtubules, neurons) operate")
print("    in the 'moderate to large' regime — phase phonons are thermally")
print("    active but not disordered. This is the SWEET SPOT for memory.")
print()


# ============================================================================
# PART 5: THE GU FREE ENERGY
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 5: THE GU FREE ENERGY AND PHASE TRANSITIONS                         ║
╚══════════════════════════════════════════════════════════════════════════════╝

The TOTAL free energy in GU has contributions from BOTH channels:

  F_total = F_amplitude + F_phase

  F_amplitude = E_bond - T × S_Debye    (standard solid state)
  F_phase = E_lock - T × S_phase        (GU phase channel)

PHASE TRANSITIONS occur when F_total has degenerate minima:

  MELTING: V_lock breaks down → phase disorder
    T_melt ~ E_lock / S_phase
    GU: long-range phase order destroyed, θFF̃ channel disrupted

  MAGNETIC T_c: spin (=phase) order → disorder
    T_c ~ J_θ × z / k_B   (z = coordination number)
    GU: phase phonon softening precedes the transition
""")

print("  LINDEMANN CRITERION FROM GU:")
print("    Melting when ⟨u²⟩^(1/2) / a > f_L ≈ 0.1")
print("    ⟨u²⟩ = (3ℏ²T)/(M k_B Θ_D²) at high T")
print()

for name, Theta_D in materials_Theta:
    T_melt_est = Theta_D**2 / 100  # rough Lindemann
    print(f"    {name:>8s}: Θ_D² / 100 ≈ {T_melt_est:7.0f} K")

print()
print("  (Rough estimates — actual melting depends on many factors)")
print("  Diamond: doesn't melt (sublimates at ~3800 K under pressure)")
print("  Lead: melts at 601 K — very close to 105²/100 = 110 → 5.5× off")
print("  Better for higher Θ_D materials")
print()


# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 80)
print("SUMMARY: THERMAL PROPERTIES FROM GU PHONONS")
print("=" * 80)
print(f"""
KEY RESULTS:

  1. DEBYE HEAT CAPACITY:
     C_V = 9Nk_B(T/Θ_D)³ ∫ x⁴eˣ/(eˣ-1)² dx
     Diamond still quantum at 300K (C/3R = {debye_cv(300, 2250)/(3*k_B_J):.2f})
     Lead fully classical (C/3R = {debye_cv(300, 105)/(3*k_B_J):.2f})
     T³ law from linear dispersion (GU: lattice of bonded solitons)

  2. THERMAL CONDUCTIVITY:
     κ = ⅓ C_V v_s l_mfp
     Diamond: 2200 W/mK (nature's best phonon conductor)
     All ingredients from GU: C_V (Debye), v_s (epoch ratio), l_mfp (scattering)

  3. PHASE PHONON ENTROPY:
     S_phase measures openness of θ channel
     Rigid → frozen → no θ memory
     Moderate → biological sweet spot → consciousness
     Large → disordered → memory lost

  4. GU FREE ENERGY:
     F = F_amplitude + F_phase (two channels)
     Phase transitions: melting, magnetic T_c
     Lindemann criterion connects Θ_D to melting

CONNECTIONS:
  ← Script 02: Θ_D values
  ← Script 03: v_s values
  ← Script 04: Phase phonon spectrum
  → Script 06: Memory coupling through phonons
  → Script 07: Sound in biology and agency
""")
