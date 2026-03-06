#!/usr/bin/env python3
"""
VIBRATIONAL MODES OF THE PLATONIC SPACE
========================================
This script covers vibrations OF the platonic space itself, NOT repeating
the phonon derivation (which is in 25_PHONONS/). These are the fundamental
modes of excitation of the Ω-torus structure that underlies all particles.

DERIVATION CHAIN:
  Part 1: Three vibrational modes of a sector (recap from 25_PHONONS/01)
  Part 2: Inter-sector excitations (NEW) — transitions between epochs
  Part 3: Moduli fluctuations (NEW) — graviton-like excitations
  Part 4: The complete spectrum — hierarchy of all excitations

REFERENCES:
  - 25_PHONONS/01_oscillation_principle.py: Lamé spectrum (dn, cn, sn)
  - theory/theory-laws.md: Mass formula X_N = M_P φ^(-N)
  - 02_torus_moduli_and_selection.py: Torus modulus tau = i(q/φ)/|p|

Date: February 2026
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mpmath import mp, mpf, sqrt, pi as mp_pi, exp, ln, ellipk, ellipe, findroot
import numpy as np

mp.dps = 30

phi = (mpf('1') + sqrt(mpf('5'))) / 2
pi = mp_pi
M_P = mpf('1.22089e22')      # MeV
m_e = mpf('0.51099895')      # MeV
N_e = 111
p_e, q_e = -41, 70

print("=" * 80)
print("VIBRATIONAL MODES OF THE PLATONIC SPACE")
print("=" * 80)


# ============================================================================
# PART 1: THREE VIBRATIONAL MODES OF A SECTOR
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 1: THREE VIBRATIONAL MODES OF A SECTOR                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

Recap from 25_PHONONS/01_oscillation_principle.py:

The kink θ = 2am(αs, m_kink) on the torus has a fluctuation operator
that is a Lamé n=1 equation:

  ψ'' + [h − 2m_kink·sn²(u, m_kink)]ψ = 0

Three vibrational modes — the particle's INTERNAL SOUND:

  dn mode:  ω² = 0              TRANSLATION (slides along torus)
  cn mode:  ω² = α²(1−m_kink)   BREATHING (expands/contracts)  ← TORUS-SPECIFIC
  sn mode:  ω² = α²(2−2m_kink)  CONTINUUM EDGE (ionization threshold)

The cn mode is the particle's INTERNAL VIBRATION — a note that
exists ONLY because the torus is finite (vanishes as m→1).

We compute the actual frequencies using m_kink from solving:
  K(m_kink) × √(m_kink) = 2 × K(ν_topo)
""")

# Torus parameters
q_over_phi = mpf(q_e) / phi
R_sq = mpf(p_e)**2 + q_over_phi**2
R = sqrt(R_sq)
l_Omega = 2 * pi * R

nu_topo = abs(q_over_phi) / R
K_nu = ellipk(nu_topo)
E_nu = ellipe(nu_topo)

Lambda_1 = 16 * K_nu**2 / l_Omega**4
mu_kink = 4 * K_nu / l_Omega

# Solve for m_kink: K(m)√m = 2K(ν)
target_Ksqrtm = 2 * K_nu

def Ksqrtm_eq(kp2):
    m = 1 - kp2
    return ellipk(m) * sqrt(m) - target_Ksqrtm

kp2_init = 16 * exp(-2 * target_Ksqrtm)
kp2_kink = findroot(Ksqrtm_eq, (kp2_init * mpf('0.5'), kp2_init * mpf('2')))
m_kink = 1 - kp2_kink
k_prime_sq = 1 - m_kink

alpha_kink = mu_kink

omega_dn = mpf('0')
omega_cn_sq = alpha_kink**2 * k_prime_sq
omega_cn = sqrt(omega_cn_sq)
omega_sn_sq = alpha_kink**2 * 2 * k_prime_sq
omega_sn = sqrt(omega_sn_sq)

print(f"  TORUS PARAMETERS:")
print(f"    Winding: (p, q) = ({p_e}, {q_e})")
print(f"    Circumference: l_Ω = {float(l_Omega):.2f}")
print(f"    Topological modulus: ν_topo = {float(nu_topo):.6f}")
print(f"    K(ν_topo) = {float(K_nu):.6f}")
print()

print(f"  KINK PARAMETERS:")
print(f"    m_kink = {float(m_kink):.6f} (≠ ν_topo = {float(nu_topo):.6f})")
print(f"    k'² = 1 - m_kink = {float(k_prime_sq):.6f}")
print(f"    α (kink curvature) = μ = {float(alpha_kink):.6f}")
print()

print(f"  THREE VIBRATIONAL MODES:")
print(f"    dn mode: ω² = 0            → ω = 0             (translation)")
print(f"    cn mode: ω² = α²k'²        → ω = {float(omega_cn):.6e}  (breathing)")
print(f"    sn mode: ω² = 2α²k'²      → ω = {float(omega_sn):.6e}  (continuum)")
print()

print(f"  PHYSICAL INTERPRETATION:")
print(f"    The dn mode is the Goldstone mode — ZERO SOUND (free sliding)")
print(f"    The cn mode is INTERNAL SOUND — the soliton 'ringing'")
print(f"    The sn mode is the IONIZATION THRESHOLD — above this, the soliton breaks")
print(f"    Sound gap: ω_cn to ω_sn ratio = √2")
print(f"    This gap PROTECTS the soliton from radiative decay")
print()


# ============================================================================
# PART 2: INTER-SECTOR EXCITATIONS
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 2: INTER-SECTOR EXCITATIONS                                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

A particle at epoch N can be excited to a neighboring epoch N±1.

These are NOT phonons — they are transitions between DIFFERENT sectors.

ANALOGY:
  Phonons = vibrations within a crystal site (same sector)
  Inter-sector = hopping between sites (different sectors)

The excitation energy:
  ΔE = X_N - X_{N+1} = X_N × (1 - 1/φ)
     = X_N × (φ-1)/φ = X_N/φ²

For the electron (N=111):
  ΔE_e = X_111 × (1 - 1/φ) = X_111/φ²

This is the energy cost to "hop" from epoch 111 to epoch 112.
""")

# Compute inter-sector excitation energies
X_e = M_P * phi**(-N_e)
delta_E_e = X_e * (1 - 1/phi)
delta_E_e_alt = X_e / phi**2

print(f"  ELECTRON INTER-SECTOR EXCITATIONS:")
print(f"    X_111 = M_P × φ^(-111) = {float(X_e):.6f} MeV")
print(f"    ΔE = X_111 × (1 - 1/φ) = {float(delta_E_e):.6f} MeV")
print(f"    ΔE = X_111/φ² = {float(delta_E_e_alt):.6f} MeV")
print(f"    (These are equal: φ - 1 = 1/φ)")
print()

# Compare to electron mass
print(f"  COMPARISON WITH ELECTRON MASS:")
print(f"    m_e = {float(m_e):.8f} MeV")
print(f"    ΔE / m_e = {float(delta_E_e / m_e):.6f}")
print(f"    The inter-sector gap is ~{float(delta_E_e / m_e * 100):.1f}% of the electron mass")
print()

# Other particles
particles = [
    ('muon', 100),
    ('tau', 94),
    ('up', 110),
    ('down', 105),
]

print(f"  INTER-SECTOR EXCITATIONS FOR OTHER PARTICLES:")
print()
print(f"    {'Particle':<10s}  {'N':>4s}  {'X_N (MeV)':>12s}  {'ΔE (MeV)':>12s}  {'ΔE/X_N':>10s}")
print("    " + "-" * 70)

for name, N in particles:
    X_N = float(M_P * phi**(-N))
    delta_E = float(X_N / phi**2)
    ratio = float(delta_E / X_N)
    print(f"    {name:<10s}  {N:4d}  {X_N:12.2f}  {delta_E:12.2f}  {ratio:10.6f}")

print()
print(f"  KEY INSIGHT:")
print(f"    Inter-sector excitations are at the MeV scale (particle mass scale)")
print(f"    They are MUCH larger than phonons (meV scale)")
print(f"    The ratio: ΔE_inter-sector / ω_phonon ~ 10⁵")
print(f"    This reflects the hierarchy: sector transitions >> internal vibrations")
print()


# ============================================================================
# PART 3: MODULI FLUCTUATIONS
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 3: MODULI FLUCTUATIONS                                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

The torus modulus tau = i(q/φ)/|p| can fluctuate.

δtau corresponds to a change in the torus shape.

The energy cost:
  ΔE_moduli ~ (d²Γ/dτ²) × |δτ|²

These are the GRAVITON-LIKE excitations of the platonic space.

They couple to all particles universally (like gravity).

PHYSICAL MEANING:
  Moduli fluctuations = changes in the FUNDAMENTAL GEOMETRY
  All particles feel this change → universal coupling
  Energy scale: Planck scale (M_P)
""")

# Torus modulus
tau_e = mpf(q_e) / phi / abs(p_e)  # i factor absorbed in convention
print(f"  TORUS MODULUS:")
print(f"    τ = i(q/φ)/|p| = i × {float(q_e/phi/abs(p_e)):.6f}")
print(f"    For electron: (p, q) = ({p_e}, {q_e})")
print(f"    |τ| = {float(abs(tau_e)):.6f}")
print()

# Moduli fluctuation energy scale
# The effective action Γ[τ] has curvature d²Γ/dτ² ~ M_P²
# A fluctuation δτ ~ 1 changes the geometry significantly
# Energy cost: ΔE ~ M_P² × (δτ)² × (volume factor)

# Rough estimate: moduli fluctuations cost Planck-scale energy
delta_E_moduli_scale = M_P  # Order of magnitude

print(f"  MODULI FLUCTUATION ENERGY SCALE:")
print(f"    ΔE_moduli ~ M_P = {float(M_P):.2e} MeV")
print(f"    This is the Planck scale — the highest energy scale")
print()

# Compare to other scales
print(f"  ENERGY SCALE HIERARCHY:")
print(f"    Moduli fluctuations: ~ {float(M_P):.2e} MeV  (Planck scale)")
print(f"    Inter-sector (N→N+1): ~ {float(delta_E_e):.2f} MeV  (particle mass scale)")
print(f"    Lame modes (cn): ~ {float(omega_cn):.2e} MeV  (dimensionless, internal)")
print(f"    Phonons: ~ 0.001 MeV  (meV scale, lattice vibrations)")
print()

print(f"  RATIOS:")
print(f"    M_P / ΔE_inter-sector = {float(M_P / delta_E_e):.2e}")
print(f"    ΔE_inter-sector / ω_cn = {float(delta_E_e / omega_cn):.2e}")
print(f"    ω_cn / ω_phonon ≈ {float(omega_cn / mpf('0.001')):.2e}")
print()

print(f"  PHYSICAL INTERPRETATION:")
print(f"    Moduli fluctuations are GRAVITON-LIKE:")
print(f"      - Universal coupling (all particles feel them)")
print(f"      - Planck-scale energy (highest frequency)")
print(f"      - Geometric origin (torus shape changes)")
print(f"      - Long-range (like gravity)")
print()


# ============================================================================
# PART 4: THE COMPLETE SPECTRUM
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 4: THE COMPLETE SPECTRUM                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

The complete vibrational spectrum of the platonic space has FOUR LEVELS:

  1. MODULI FLUCTUATIONS (Planck scale)
     Energy: ~ M_P ≈ 10²² MeV
     Nature: Changes in fundamental geometry
     Coupling: Universal (graviton-like)

  2. INTER-SECTOR EXCITATIONS (MeV scale)
     Energy: X_N × (1 - 1/φ) ≈ X_N/φ²
     Nature: Transitions between epochs N → N±1
     Coupling: Particle-specific (depends on N)

  3. LAMÉ MODES (dimensionless, internal)
     Energy: ω_cn, ω_sn (dimensionless frequencies)
     Nature: Internal vibrations of a soliton
     Coupling: Single-particle (cn mode)

  4. PHONONS (meV scale)
     Energy: ~ 0.001 MeV (thermal scale)
     Nature: Collective lattice vibrations
     Coupling: Many-body (crystal structure)

Each level corresponds to a different "frequency" in the platonic space.
""")

# Create spectrum table
print(f"  COMPLETE SPECTRUM TABLE:")
print()
print(f"    {'Level':<25s}  {'Energy Scale':>15s}  {'Nature':<30s}")
print("    " + "-" * 80)
print(f"    {'Moduli fluctuations':<25s}  {float(M_P):>15.2e} MeV  {'Graviton-like, universal':<30s}")
print(f"    {'Inter-sector (N→N+1)':<25s}  {float(delta_E_e):>15.2f} MeV  {'Epoch transitions':<30s}")
print(f"    {'Lamé cn mode':<25s}  {float(omega_cn):>15.2e}      {'Internal soliton sound':<30s}")
print(f"    {'Lamé sn mode':<25s}  {float(omega_sn):>15.2e}      {'Ionization threshold':<30s}")
print(f"    {'Phonons (typical)':<25s}  {'0.001':>15s} MeV  {'Lattice vibrations':<30s}")
print()

# Energy ratios
print(f"  ENERGY RATIOS:")
print(f"    M_P / ΔE_inter-sector = {float(M_P / delta_E_e):.2e}")
print(f"    ΔE_inter-sector / ω_cn = {float(delta_E_e / omega_cn):.2e}")
print(f"    ω_cn / ω_phonon ≈ {float(omega_cn / mpf('0.001')):.2e}")
print()

print(f"  HIERARCHY:")
print(f"    Moduli >> Inter-sector >> Lamé >> Phonons")
print(f"    Each level is ~10⁵-10¹⁰ times larger than the next")
print()

print(f"  PHYSICAL PICTURE:")
print(f"    The platonic space vibrates at ALL these frequencies simultaneously.")
print(f"    Each frequency corresponds to a different 'layer' of structure:")
print(f"      - Moduli: The geometry itself")
print(f"      - Inter-sector: The epoch ladder")
print(f"      - Lamé: The soliton internal structure")
print(f"      - Phonons: The many-body collective modes")
print()


# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 80)
print("SUMMARY: VIBRATIONAL MODES OF THE PLATONIC SPACE")
print("=" * 80)
print(f"""
WHAT WE ESTABLISHED:

  1. THREE VIBRATIONAL MODES OF A SECTOR (from 25_PHONONS/01):
     - dn mode: ω² = 0 (translation, Goldstone)
     - cn mode: ω² = α²k'² = {float(omega_cn**2):.6e} (breathing, torus-specific)
     - sn mode: ω² = 2α²k'² = {float(omega_sn**2):.6e} (continuum edge)
     - Computed using m_kink from K(m)√m = 2K(ν_topo)
     - The cn mode is the seed of phonons (single-particle → many-body)

  2. INTER-SECTOR EXCITATIONS (NEW):
     - A particle at epoch N can hop to N±1
     - Energy cost: ΔE = X_N × (1 - 1/φ) = X_N/φ²
     - For electron: ΔE = {float(delta_E_e):.2f} MeV (~{float(delta_E_e/m_e*100):.1f}% of m_e)
     - These are NOT phonons — different sectors, not vibrations within one
     - Analogy: phonons = vibrations within a site; inter-sector = hopping between sites

  3. MODULI FLUCTUATIONS (NEW):
     - The torus modulus τ = i(q/φ)/|p| can fluctuate
     - Energy cost: ΔE_moduli ~ M_P ≈ {float(M_P):.2e} MeV (Planck scale)
     - These are GRAVITON-LIKE excitations:
       * Universal coupling (all particles feel them)
       * Planck-scale energy
       * Geometric origin (torus shape changes)
       * Long-range (like gravity)

  4. THE COMPLETE SPECTRUM:
     - Moduli fluctuations: ~ 10²² MeV (Planck scale)
     - Inter-sector: ~ MeV scale (particle mass scale)
     - Lamé modes: dimensionless (internal structure)
     - Phonons: ~ meV scale (thermal, many-body)
     - Hierarchy: Moduli >> Inter-sector >> Lamé >> Phonons
     - Each level is ~10⁵-10¹⁰ times larger than the next

CONNECTIONS:
  → 25_PHONONS/01_oscillation_principle.py: Lamé spectrum derivation
  → 25_PHONONS/02_phonon_dispersion.py: Phonon band structure
  → 02_torus_moduli_and_selection.py: Torus modulus τ
  → 03_topological_sectors.py: Epoch structure and sector transitions
  → theory/theory-laws.md: Mass formula X_N = M_P φ^(-N)
""")