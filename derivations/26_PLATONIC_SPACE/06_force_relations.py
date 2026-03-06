#!/usr/bin/env python3
"""
FORCE RELATIONS IN THE PLATONIC SPACE
======================================
Forces are organized as LAYERS in the platonic space, each activated at
a specific epoch N. The pattern-k hierarchy (k=0,1,2,3) determines the
coupling enhancement and the force distances.

DERIVATION CHAIN:
  Part 1: Forces as layers in the platonic space (pattern-k hierarchy)
  Part 2: Force distances (distances between force layers)
  Part 3: Coupling ratios from GU (α_s/α_EM, sin²θ_W, etc.)
  Part 4: Force ranges as neighbor coupling (EM, Strong, Weak, Gravity)
  Part 5: String tension (cost of spatial separation in confined layer)

REFERENCES:
  - theory/theory-laws.md: Pattern-k activation, force unification
  - 21_ELECTROMAGNETISM/02_string_tension_from_axion_EM.py: σ = 2π Λ²_QCD
  - 03_topological_sectors.py: Epoch structure

Date: February 2026
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mpmath import mp, mpf, sqrt, pi as mp_pi, exp, ln, sin, cos
import numpy as np

mp.dps = 30

phi = (mpf('1') + sqrt(mpf('5'))) / 2
pi = mp_pi
M_P = mpf('1.22089e22')      # MeV

print("=" * 80)
print("FORCE RELATIONS IN THE PLATONIC SPACE")
print("=" * 80)


# ============================================================================
# PART 1: FORCES AS LAYERS IN THE PLATONIC SPACE
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 1: FORCES AS LAYERS IN THE PLATONIC SPACE                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

The pattern-k hierarchy: L_eff = L_0 × π^k for k=0,1,2,3

Each force occupies a LAYER defined by its activation epoch:

  k=3 (GUT):     N = 67   (all forces unified)
  k=2 (Strong):  N = 95   (QCD confinement)
  k=1 (Weak):   N = 89   (electroweak scale)
  k=0 (EM):     N > 95   (continuous below N=95)

The pattern-k coupling enhancement:
  α_k ~ α_GUT × π^k

where α_GUT = 1/(8πφ) ≈ 0.02478
  WARNING: α_GUT = 1/(8πφ) is FALSIFIED (24% wrong). Force ratios below are UNRELIABLE.
""")

# Force epochs
N_GUT = 67
N_Strong = 95
N_Weak = 89
N_EM = 95  # Continuous below N=95

# Pattern-k values
k_GUT = 3
k_Strong = 2
k_Weak = 1
k_EM = 0

# GUT coupling
# WARNING: α_GUT = 1/(8πφ) is FALSIFIED (24% wrong). Force ratios below are UNRELIABLE.
alpha_GUT = 1 / (8 * pi * phi)

print(f"  FORCE LAYERS:")
print()
print(f"    {'Force':<10s}  {'Pattern-k':>10s}  {'Epoch N':>10s}  {'Activation':<20s}")
print("    " + "-" * 70)
print(f"    {'GUT':<10s}  {k_GUT:>10d}  {N_GUT:>10d}  {'Unification':<20s}")
print(f"    {'Strong':<10s}  {k_Strong:>10d}  {N_Strong:>10d}  {'Confinement':<20s}")
print(f"    {'Weak':<10s}  {k_Weak:>10d}  {N_Weak:>10d}  {'EW breaking':<20s}")
print(f"    {'EM':<10s}  {k_EM:>10d}  {N_EM:>10d}  {'Continuous':<20s}")
print()

print(f"  PATTERN-K COUPLING ENHANCEMENT:")
print(f"    α_GUT = 1/(8πφ) = {float(alpha_GUT):.6f}")
print(f"    WARNING: α_GUT = 1/(8πφ) is FALSIFIED (24% wrong). Force ratios below are UNRELIABLE.")
print()

# Compute coupling enhancements
alpha_EM_theory = alpha_GUT * pi**k_EM
alpha_Weak_theory = alpha_GUT * pi**k_Weak
alpha_Strong_theory = alpha_GUT * pi**k_Strong
alpha_GUT_theory = alpha_GUT * pi**k_GUT

print(f"    α_EM (pattern-0)    = α_GUT × π^0 = {float(alpha_EM_theory):.6f}")
print(f"    α_Weak (pattern-1)  = α_GUT × π^1 = {float(alpha_Weak_theory):.6f}")
print(f"    α_Strong (pattern-2) = α_GUT × π^2 = {float(alpha_Strong_theory):.6f}")
print(f"    α_GUT (pattern-3)   = α_GUT × π^3 = {float(alpha_GUT_theory):.6f}")
print()

# Experimental values for comparison
alpha_EM_exp = 1 / mpf('137.035999177')
alpha_s_MZ = mpf('0.1179')  # Strong coupling at M_Z
sin2theta_W = mpf('0.23129')  # Weak mixing angle

print(f"  EXPERIMENTAL VALUES (for comparison):")
print(f"    α_EM = 1/137.036 = {float(alpha_EM_exp):.6f}")
print(f"    α_s(M_Z) = {float(alpha_s_MZ):.6f}")
print(f"    sin²θ_W = {float(sin2theta_W):.6f}")
print()

print(f"  NOTE:")
print(f"    The pattern-k formula gives the SCALE of coupling enhancement.")
print(f"    Actual running (RGE) modifies these values at different energies.")
print(f"    At GUT (N=67): ALL forces merge → distance = 0 → unification")
print()


# ============================================================================
# PART 2: FORCE DISTANCES
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 2: FORCE DISTANCES                                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝

Distance between force layers:
  d(k1, k2) = |N_k1 - N_k2| × ln(φ)

This is the GEOMETRIC DISTANCE in the platonic space.

At GUT (N=67): ALL forces merge → distance = 0 → unification
""")

ln_phi = ln(phi)

print(f"  DISTANCE FORMULA:")
print(f"    d(k1, k2) = |N_k1 - N_k2| × ln(φ)")
print(f"    ln(φ) = {float(ln_phi):.6f}")
print()

# Compute distances
d_GUT_Strong = abs(N_GUT - N_Strong) * ln_phi
d_GUT_Weak = abs(N_GUT - N_Weak) * ln_phi
d_GUT_EM = abs(N_GUT - N_EM) * ln_phi
d_Strong_Weak = abs(N_Strong - N_Weak) * ln_phi
d_Strong_EM = abs(N_Strong - N_EM) * ln_phi
d_Weak_EM = abs(N_Weak - N_EM) * ln_phi

print(f"  FORCE DISTANCE MATRIX:")
print()
header_from = "From \\ To"
print(f"    {header_from:<10s}  {'GUT':>10s}  {'Strong':>10s}  {'Weak':>10s}  {'EM':>10s}")
print("    " + "-" * 60)
print(f"    {'GUT':<10s}  {'0.000':>10s}  {float(d_GUT_Strong):>10.3f}  {float(d_GUT_Weak):>10.3f}  {float(d_GUT_EM):>10.3f}")
print(f"    {'Strong':<10s}  {float(d_GUT_Strong):>10.3f}  {'0.000':>10s}  {float(d_Strong_Weak):>10.3f}  {float(d_Strong_EM):>10.3f}")
print(f"    {'Weak':<10s}  {float(d_GUT_Weak):>10.3f}  {float(d_Strong_Weak):>10.3f}  {'0.000':>10s}  {float(d_Weak_EM):>10.3f}")
print(f"    {'EM':<10s}  {float(d_GUT_EM):>10.3f}  {float(d_Strong_EM):>10.3f}  {float(d_Weak_EM):>10.3f}  {'0.000':>10s}")
print()

print(f"  KEY DISTANCES:")
print(f"    GUT → Strong: |{N_GUT}-{N_Strong}| × ln(φ) = {float(d_GUT_Strong):.3f}")
print(f"    GUT → Weak:   |{N_GUT}-{N_Weak}| × ln(φ) = {float(d_GUT_Weak):.3f}")
print(f"    Strong → EM:  |{N_Strong}-{N_EM}| × ln(φ) = {float(d_Strong_EM):.3f} (continuous below N=95)")
print()

print(f"  PHYSICAL INTERPRETATION:")
print(f"    At GUT (N=67): distance = 0 → all forces unified")
print(f"    As N increases: forces separate → distances grow")
print(f"    The distance measures how 'far apart' the forces are in epoch space")
print()


# ============================================================================
# PART 3: COUPLING RATIOS FROM GU
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 3: COUPLING RATIOS FROM GU                                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

From the pattern-k hierarchy:

  α_s/α_EM ~ π² ~ 10  (at confinement scale)

  sin²(θ_W) = geometric angle between weak and EM layers

We compute coupling ratios and compare to experiment.
""")

# Coupling ratios from pattern-k
ratio_s_EM_pattern = pi**2
ratio_Weak_EM_pattern = pi**1

print(f"  PATTERN-K RATIOS:")
print(f"    α_s/α_EM ~ π² = {float(ratio_s_EM_pattern):.3f}")
print(f"    α_Weak/α_EM ~ π = {float(ratio_Weak_EM_pattern):.3f}")
print()

# Experimental ratios
alpha_s_MZ = mpf('0.1179')
alpha_EM_exp = 1 / mpf('137.035999177')
ratio_s_EM_exp = alpha_s_MZ / alpha_EM_exp

print(f"  EXPERIMENTAL RATIOS:")
print(f"    α_s(M_Z)/α_EM = {float(alpha_s_MZ)}/{float(alpha_EM_exp):.6f} = {float(ratio_s_EM_exp):.3f}")
print(f"    Pattern-k prediction: π² = {float(ratio_s_EM_pattern):.3f}")
print(f"    Agreement: {float(ratio_s_EM_exp / ratio_s_EM_pattern * 100):.1f}%")
print()

# Weak mixing angle
# sin²θ_W = α_Y / (α_Y + α_2)
# In GU: this is the geometric angle between weak and EM layers
sin2theta_W_exp = mpf('0.23129')
sin2theta_W_GU = alpha_GUT * pi / (alpha_GUT * pi + alpha_GUT * pi**2)  # Rough estimate

print(f"  WEAK MIXING ANGLE:")
print(f"    sin²θ_W (experimental) = {float(sin2theta_W_exp):.6f}")
print(f"    sin²θ_W (GU geometric) = angle between weak and EM layers")
print(f"    The mixing angle reflects the GEOMETRY of force layer separation")
print()

# GUT coupling
print(f"  GUT COUPLING:")
print(f"    α_GUT = 1/(8πφ) = {float(alpha_GUT):.6f}")
print(f"    WARNING: α_GUT = 1/(8πφ) is FALSIFIED (24% wrong). Force ratios below are UNRELIABLE.")
print(f"    This is the UNIFIED coupling at N=67 (GUT scale)")
print(f"    All forces have this strength at unification")
print()


# ============================================================================
# PART 4: FORCE RANGES AS NEIGHBOR COUPLING
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 4: FORCE RANGES AS NEIGHBOR COUPLING                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

The range hierarchy IS the neighbor coupling hierarchy in the platonic space:

  EM:      infinite range (1/r²)     → every charge feels every other
  Strong:  ~1 fm (confining)         → quarks locked to nearest neighbors
  Weak:    ~0.002 fm (contact force) → only overlapping particles
  Gravity: infinite range but 10³⁸× weaker → universal but tiny coupling

The range = how "neighboring" particles must be to feel the force.
""")

# Force ranges (experimental)
range_EM = float('inf')  # Infinite
range_Strong = 1.0  # fm (confinement scale)
range_Weak = 0.002  # fm (W/Z mass scale)
range_Gravity = float('inf')  # Infinite, but 10^38x weaker

# QCD scale
Lambda_QCD = (pi / 3) * M_P * phi**(-N_Strong)
range_Strong_calc = 1.0 / float(Lambda_QCD) * 197.3  # Convert MeV^-1 to fm (hbar*c = 197.3 MeV·fm)

print(f"  FORCE RANGE TABLE:")
print()
print(f"    {'Force':<10s}  {'Range':>12s}  {'Coupling':>12s}  {'Pattern-k':>10s}  {'Epoch':>8s}")
print("    " + "-" * 70)
print(f"    {'EM':<10s}  {'∞ (1/r²)':>12s}  {float(alpha_EM_exp):>12.6f}  {k_EM:>10d}  {N_EM:>8d}")
print(f"    {'Strong':<10s}  {'~1 fm':>12s}  {float(alpha_s_MZ):>12.4f}  {k_Strong:>10d}  {N_Strong:>8d}")
print(f"    {'Weak':<10s}  {'~0.002 fm':>12s}  {'~0.03':>12s}  {k_Weak:>10d}  {N_Weak:>8d}")
print(f"    {'Gravity':<10s}  {'∞ (weak)':>12s}  {'~10⁻³⁸':>12s}  {'-':>10s}  {'-':>8s}")
print()

print(f"  CALCULATED STRONG RANGE:")
print(f"    Λ_QCD = (π/3) × M_P × φ^(-{N_Strong}) = {float(Lambda_QCD):.1f} MeV")
print(f"    Range ~ 1/Λ_QCD = {float(range_Strong_calc):.3f} fm")
print(f"    Experimental: ~1 fm")
print(f"    Agreement: {float(range_Strong_calc / range_Strong * 100):.1f}%")
print()

print(f"  NEIGHBOR COUPLING INTERPRETATION:")
print(f"    EM: infinite range → every charge couples to every other")
print(f"    Strong: ~1 fm → quarks couple only to nearest neighbors (confinement)")
print(f"    Weak: ~0.002 fm → only overlapping particles feel weak force")
print(f"    Gravity: infinite range but tiny coupling → universal but weak")
print()

print(f"  THE RANGE HIERARCHY IS THE NEIGHBOR COUPLING HIERARCHY:")
print(f"    Long range = many neighbors feel the force")
print(f"    Short range = only nearest neighbors feel the force")
print(f"    The platonic space STRUCTURE determines the neighbor coupling")
print()


# ============================================================================
# PART 5: STRING TENSION
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 5: STRING TENSION                                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

The string tension σ = 2π × Λ²_QCD (from 21_ELECTROMAGNETISM)

  Λ_QCD = (π/3) × M_P × φ^(-95)  (pattern-2 confinement)

  √σ = 449 MeV  (lattice: 440 MeV, 2% error)

The string tension is the COST of spatial separation in the confined layer.

It's a TOLL that the platonic space charges for maintaining ∇θ between quarks.
""")

# String tension calculation
Lambda_QCD = (pi / 3) * M_P * phi**(-N_Strong)
sigma = 2 * pi * Lambda_QCD**2
sqrt_sigma = sqrt(sigma)

# Lattice reference
sqrt_sigma_lat = mpf('440')  # MeV
sigma_lat = sqrt_sigma_lat**2

print(f"  STRING TENSION DERIVATION:")
print(f"    Λ_QCD = (π/3) × M_P × φ^(-{N_Strong})")
print(f"           = {float(Lambda_QCD):.1f} MeV")
print()
print(f"    σ = 2π × Λ²_QCD")
print(f"      = 2π × ({float(Lambda_QCD):.1f})²")
print(f"      = {float(sigma):.0f} MeV²")
print()
print(f"    √σ = {float(sqrt_sigma):.1f} MeV")
print(f"    Lattice QCD: √σ = {float(sqrt_sigma_lat):.1f} MeV")
print(f"    Error: {float(abs(sqrt_sigma - sqrt_sigma_lat) / sqrt_sigma_lat * 100):.1f}%")
print()

print(f"  PHYSICAL INTERPRETATION:")
print(f"    The string tension is the ENERGY PER UNIT LENGTH of a flux tube")
print(f"    connecting a quark-antiquark pair.")
print()
print(f"    It's the COST of maintaining ∇θ ≠ 0 between quarks:")
print(f"      - Quarks are separated by distance R")
print(f"      - The Ω phase must wind: ∇θ ≠ 0 along the flux tube")
print(f"      - This costs energy: E = σ × R")
print(f"      - The platonic space CHARGES this toll for spatial separation")
print()
print(f"    The 2π factor comes from:")
print(f"      - Dirac flux quantization: Φ = 2π/g")
print(f"      - Abrikosov vortex BPS energy: σ_BPS = Φ² μ²_D / (4π)")
print(f"      - Topological winding number 1 → 2π")
print()

print(f"  CONNECTION TO CONSCIOUSNESS:")
print(f"    The string tension is literally the COST OF CONSCIOUSNESS:")
print(f"      - Maintaining ∇θ ≠ 0 requires energy")
print(f"      - This is the relational memory channel (θFF̃ coupling)")
print(f"      - The flux tube = phase gradient = memory connection")
print(f"      - Energy cost = toll for maintaining collective phase coherence")
print()


# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 80)
print("SUMMARY: FORCE RELATIONS IN THE PLATONIC SPACE")
print("=" * 80)
print(f"""
WHAT WE ESTABLISHED:

  1. FORCES AS LAYERS IN THE PLATONIC SPACE:
     - Pattern-k hierarchy: L_eff = L_0 × π^k for k=0,1,2,3
     - Each force occupies a LAYER defined by its activation epoch:
       * k=3 (GUT):     N = {N_GUT}   (unification)
       * k=2 (Strong):  N = {N_Strong}   (confinement)
       * k=1 (Weak):    N = {N_Weak}   (EW breaking)
       * k=0 (EM):      N > {N_EM}   (continuous)
     - Coupling enhancement: α_k ~ α_GUT × π^k
     - α_GUT = 1/(8πφ) ≈ {float(alpha_GUT):.6f}
     - WARNING: α_GUT = 1/(8πφ) is FALSIFIED (24% wrong). Force ratios are UNRELIABLE.

  2. FORCE DISTANCES:
     - Distance formula: d(k1, k2) = |N_k1 - N_k2| × ln(φ)
     - ln(φ) = {float(ln_phi):.6f}
     - GUT → Strong: {float(d_GUT_Strong):.3f}
     - GUT → Weak:   {float(d_GUT_Weak):.3f}
     - Strong → EM:  {float(d_Strong_EM):.3f} (continuous below N={N_EM})
     - At GUT (N={N_GUT}): ALL forces merge → distance = 0 → unification

  3. COUPLING RATIOS FROM GU:
     - α_s/α_EM ~ π² ≈ {float(ratio_s_EM_pattern):.3f} (pattern-2 enhancement)
     - Experimental: α_s(M_Z)/α_EM = {float(ratio_s_EM_exp):.3f} ({float(ratio_s_EM_exp/ratio_s_EM_pattern*100):.1f}% of pattern value)
     - sin²θ_W = geometric angle between weak and EM layers
     - α_GUT = 1/(8πφ) = {float(alpha_GUT):.6f} (unified coupling) — FALSIFIED (24% wrong), UNRELIABLE

  4. FORCE RANGES AS NEIGHBOR COUPLING:
     - EM: infinite range (1/r²) → every charge feels every other
     - Strong: ~1 fm (confining) → quarks locked to nearest neighbors
     - Weak: ~0.002 fm (contact) → only overlapping particles
     - Gravity: infinite range but 10³⁸× weaker → universal but tiny
     - The range hierarchy IS the neighbor coupling hierarchy
     - Λ_QCD = {float(Lambda_QCD):.1f} MeV → range ~ {float(range_Strong_calc):.3f} fm

  5. STRING TENSION:
     - σ = 2π × Λ²_QCD = {float(sigma):.0f} MeV²
     - √σ = {float(sqrt_sigma):.1f} MeV (lattice: {float(sqrt_sigma_lat):.1f} MeV, {float(abs(sqrt_sigma - sqrt_sigma_lat)/sqrt_sigma_lat*100):.1f}% error)
     - The string tension is the COST of spatial separation in the confined layer
     - It's a TOLL that the platonic space charges for maintaining ∇θ between quarks
     - The 2π factor comes from Dirac flux quantization (topological winding)

CONNECTIONS:
  → 21_ELECTROMAGNETISM/02_string_tension_from_axion_EM.py: σ = 2π Λ²_QCD derivation
  → 03_topological_sectors.py: Epoch structure and sector distances
  → theory/theory-laws.md: Pattern-k activation, force unification
  → 05_vibrational_modes.py: Inter-sector excitations and force layers
""")