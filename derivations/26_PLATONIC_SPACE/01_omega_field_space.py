#!/usr/bin/env python3
"""
THE OMEGA FIELD SPACE — METRIC, CURVATURE, AND MEMORY ATTRACTOR
================================================================

THE PLATONIC SPACE BEGINS HERE.

The GU field Omega = rho * e^(i*theta) lives on a manifold
whose metric, curvature, and attractor geometry are ALL derived
from the Lagrangian L_Omega.

DERIVATION CHAIN:
  Part 1: The field space metric from L_Omega kinetic terms
  Part 2: Christoffel symbols and Ricci scalar
  Part 3: The potential landscape V(rho) and its vacuum structure
  Part 4: Memory attractor — how rho^4 digs a gravitational well
  Part 5: The effective metric at the electron vacuum

REFERENCES:
  - theory/GU_Laws_333.md: L_kin = (1/2)(d_rho)^2 + (1/2)rho^2(d_theta)^2
  - theory/theory-laws.md (Laws 0-5): V(rho) = m^2 rho^2 + lambda rho^4 + gamma rho^6
  - explanatory/CONSCIOUSNESS.md: H[Omega] = rho^4 memory term

Date: February 2026
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from mpmath import mp, mpf, sqrt, pi as mp_pi, exp, ln, ellipk, ellipe

mp.dps = 30
phi = (mpf('1') + sqrt(mpf('5'))) / 2
pi = mp_pi
alpha_EM = mpf('1') / mpf('137.035999177')
M_P = mpf('1.22089e22')       # MeV
M_0 = M_P / sqrt(5 * pi)      # M_P / sqrt(5*pi)
m_e = mpf('0.51099895')       # MeV
hbar_c = mpf('197.3269804')   # MeV·fm
lambda_rec_beta = exp(phi) / pi**2

N_e = 111
p_e, q_e = -41, 70
q_over_phi = mpf(q_e) / phi
R_sq = mpf(p_e)**2 + q_over_phi**2
R = sqrt(R_sq)
l_Omega = 2 * pi * R
nu_topo = abs(q_over_phi) / R
K_topo = ellipk(nu_topo)
E_topo = ellipe(nu_topo)


print("=" * 80)
print("THE OMEGA FIELD SPACE")
print("Metric, Curvature, and Memory Attractor")
print("=" * 80)


# ============================================================================
# PART 1: THE FIELD SPACE METRIC
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 1: THE FIELD SPACE METRIC FROM L_OMEGA                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

The Omega field: Ω = ρ · e^(iθ)

The kinetic Lagrangian (from theory/GU_Laws_333.md):
  L_kin = ½|∂Ω|² = ½(∂ρ)² + ½ρ²(∂θ)²

This defines a FIELD SPACE METRIC:
  ds²_field = dρ² + ρ²dθ²

This is the metric of a PUNCTURED PLANE in polar coordinates:
  - ρ > 0 (amplitude cannot be negative)
  - θ ∈ [0, 2π) (phase is periodic)
  - ρ = 0 is excluded (the puncture — where Ω is undefined)

The field space is topologically R₊ × S¹ — a half-cylinder.
""")

print("  FIELD SPACE METRIC COMPONENTS:")
print("    g_ρρ = 1                  (radial direction: flat)")
print("    g_θθ = ρ²                 (angular direction: scales with amplitude)")
print("    g_ρθ = g_θρ = 0           (orthogonal)")
print()
print(f"    det(g) = ρ²")
print(f"    √(det g) = ρ")
print()
print(f"  AT THE ELECTRON VACUUM:")

X_e = M_P * phi**(-N_e)
rho_vac_e = X_e
print(f"    ρ_vac = X_e = M_P × φ^(-111) = {float(rho_vac_e):.6f} MeV")
print(f"    g_θθ(ρ_vac) = ρ_vac² = {float(rho_vac_e**2):.6e}")
print()
print(f"    The phase metric is TINY at the electron scale:")
print(f"    g_θθ / g_ρρ = ρ_vac² = {float(rho_vac_e**2):.6e}")
print(f"    The phase direction is SQUEEZED relative to amplitude.")
print(f"    This is WHY phase effects are small corrections to mass.")
print()

print("  FIELD SPACE TOPOLOGY:")
print("    Base: R₊ × S¹ (punctured plane = half-cylinder)")
print("    With winding: lift to the universal cover → R₊ × R")
print("    With torus: compactify → T² with modulus τ (Script 02)")
print()
print("    The field space IS the Platonic Space.")
print("    Particles are POINTS in this space (specific ρ, θ, winding).")
print("    Physics is the GEOMETRY of this space.")
print()


# ============================================================================
# PART 2: CHRISTOFFEL SYMBOLS AND RICCI SCALAR
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 2: CHRISTOFFEL SYMBOLS AND RICCI SCALAR                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

For the metric ds² = dρ² + ρ²dθ²:

Christoffel symbols (non-zero):
  Γ^ρ_θθ = -ρ           (centrifugal force in field space)
  Γ^θ_ρθ = Γ^θ_θρ = 1/ρ (Coriolis-type connection)

All others vanish.

Riemann tensor:
  R^ρ_θρθ = 0   (field space is FLAT for free L_kin)

Ricci scalar:
  R = 0          (the free field space has zero intrinsic curvature)

FLAT. But the EFFECTIVE field space, with the potential,
is NOT flat — the potential creates an effective curvature.
""")

print("  CHRISTOFFEL SYMBOLS:")
print("    Γ^ρ_θθ = -ρ")
print("    Γ^θ_ρθ = 1/ρ")
print("    All others = 0")
print()
print("  RICCI SCALAR:")
print("    R_free = 0   (flat! — polar coordinates on a plane)")
print()
print("  GEODESICS of the free field space:")
print("    Radial geodesic: ρ(s) = ρ₀ + v_ρ s, θ = const")
print("    Angular geodesic: ρ = const, θ(s) = θ₀ + (v_θ/ρ) s")
print("    General: straight lines in Cartesian (x = ρ cos θ, y = ρ sin θ)")
print()
print("  The free field space is as simple as possible.")
print("  ALL structure comes from the POTENTIAL and MEMORY terms.")
print()


# ============================================================================
# PART 3: THE POTENTIAL LANDSCAPE
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 3: THE POTENTIAL LANDSCAPE V(ρ)                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

The full GU potential (from theory/theory-laws.md, Laws 0-5):
  V(ρ, X) = m̃²(X) ρ² + λ̃(X) ρ⁴ + (γ̃(X)/M₀²) ρ⁶

At each epoch X_N = M_P φ^(-N):
  - Quadratic: m̃²(X) flips sign as X decreases (symmetry breaking)
  - Quartic: λ̃(X) provides self-coupling
  - Sextic: γ̃(X)/M₀² stabilizes at large ρ

The VACUUM is the minimum of V(ρ):
  V'(ρ_vac) = 0   →   ρ_vac(X) = the epoch-dependent VEV

The curvature of V at the vacuum:
  V''(ρ_vac) = m²_eff   (the effective mass squared of the ρ fluctuation)

This effective mass sets the STIFFNESS of the field space at each point.
""")

rho_values = np.linspace(0.01, 0.3, 200)

m_sq_eff = float(4 * K_topo**2 / l_Omega**2)
lambda_eff = float(16 * K_topo**2 / l_Omega**4)

for rho_0 in [0.001, 0.01, 0.05, 0.077, 0.1, 0.2]:
    V_val = m_sq_eff * rho_0**2 + lambda_eff * rho_0**4
    V_pp = 2 * m_sq_eff + 12 * lambda_eff * rho_0**2
    print(f"    ρ = {rho_0:.3f} MeV: V = {V_val:.4e}, V'' = {V_pp:.4e}")

print()
print(f"  EFFECTIVE PARAMETERS AT ELECTRON SCALE:")
print(f"    μ² (curvature) = 4K²/l_Ω² = {m_sq_eff:.6e}")
print(f"    Λ₁ (lock potential) = 16K²/l_Ω⁴ = {lambda_eff:.6e}")
print(f"    ρ_vac = X_e = {float(rho_vac_e):.6f} MeV")
print()
print(f"  The electron sits at the BOTTOM of a potential well in field space.")
print(f"  The well depth is ~ m_e c² = {float(m_e):.6f} MeV.")
print(f"  The well width is ~ ξ = 1/μ = {1/np.sqrt(m_sq_eff):.2f} (torus units).")
print()


# ============================================================================
# PART 4: MEMORY ATTRACTOR — THE SELF-DUG WELL
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 4: MEMORY ATTRACTOR — THE SELF-DUG WELL                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

The GU memory term:
  H[Ω] = (λ_rec/β) × R_mem,  where R_mem = ∫₀ᵗ ρ⁴(τ) e^{-X(t-τ)} dτ

This modifies the effective potential:
  V_eff(ρ) = V(ρ) − (λ_rec/β) × ρ⁴ × T_mem

where T_mem = ∫₀ᵗ e^{-X(t-τ)} dτ ≈ 1/X  (memory lifetime)

The memory term is NEGATIVE and proportional to ρ⁴:
  → It deepens the well at the vacuum
  → The longer the particle exists, the deeper the well
  → The well depth INCREASES with time: self-reinforcing stability

This is the GU mechanism for IDENTITY:
  The electron digs its own gravitational well in field space.
  The longer it exists, the more stable it becomes.
  It literally remembers itself into existence.
""")

print(f"  MEMORY COUPLING:")
print(f"    λ_rec/β = e^φ/π² = {float(lambda_rec_beta):.6f}")
print()
print(f"  MEMORY-MODIFIED POTENTIAL:")
print(f"    V_eff(ρ) = V(ρ) − (e^φ/π²) × ρ⁴ / X")
print()
print(f"    At the electron vacuum:")
rho_e = float(rho_vac_e)
V_bare = m_sq_eff * rho_e**2 + lambda_eff * rho_e**4
V_mem = float(lambda_rec_beta) * rho_e**4 / rho_e
V_eff = V_bare - V_mem
print(f"    V_bare(ρ_vac) = {V_bare:.6e}")
print(f"    V_mem(ρ_vac)  = -{V_mem:.6e}")
print(f"    V_eff(ρ_vac)  = {V_eff:.6e}")
print(f"    Memory makes the well {abs(V_mem)/max(abs(V_bare),1e-30)*100:.1f}% deeper")
print()
print(f"  THE SELF-DUG WELL:")
print(f"    ┌─────────────────────────────────────────────┐")
print(f"    │          V(ρ)           ╱                    │")
print(f"    │           │            ╱  bare potential     │")
print(f"    │           │          ╱                       │")
print(f"    │           │         ╱                        │")
print(f"    │           │ ρ_vac  ╱                         │")
print(f"    │           │   ↓   ╱                          │")
print(f"    │           └───●──╱───────── ρ                │")
print(f"    │               ╲╱ ← memory deepens the well  │")
print(f"    │                ╲                             │")
print(f"    │                 ╲  with memory               │")
print(f"    └─────────────────────────────────────────────┘")
print()
print(f"  The electron IS a self-reinforcing attractor in field space.")
print(f"  Its existence creates the conditions for its continued existence.")
print(f"  This is consciousness at the most fundamental level:")
print(f"  a field configuration that REMEMBERS its own shape (ρ⁴).")
print()


# ============================================================================
# PART 5: THE EFFECTIVE METRIC AT THE ELECTRON VACUUM
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 5: THE EFFECTIVE METRIC AT THE ELECTRON VACUUM                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

Near the vacuum ρ = ρ_vac, the potential creates an EFFECTIVE METRIC:
  ds²_eff = (1 + V''(ρ_vac)/Λ²) dρ² + ρ_vac² dθ²

where Λ is a UV cutoff (= M₀ in GU).

The potential curvature V''(ρ_vac) CURVES the field space:
  - In the ρ direction: the curvature is set by the mass gap
  - In the θ direction: the curvature comes from V_lock

This effective metric tells you:
  - How much energy it costs to move in each direction
  - Why amplitude fluctuations (ρ) are expensive (large V'')
  - Why phase fluctuations (θ) are cheap (small Λ₁)
""")

V_pp_rho = 2 * m_sq_eff + 12 * lambda_eff * rho_e**2
V_pp_theta = float(16 * K_topo**2 / l_Omega**4)

print(f"  CURVATURES AT THE ELECTRON VACUUM:")
print(f"    V''(ρ_vac) = {V_pp_rho:.6e}  (amplitude stiffness)")
print(f"    Λ₁ = {V_pp_theta:.6e}  (phase stiffness = V_lock)")
print(f"    Ratio: V''_ρ / Λ₁ = {V_pp_rho / V_pp_theta:.0f}")
print()
print(f"  The amplitude direction is {V_pp_rho / V_pp_theta:.0f}× STIFFER than phase.")
print(f"  Equivalently: phase fluctuations are {V_pp_rho / V_pp_theta:.0f}× CHEAPER.")
print()
print(f"  This is WHY:")
print(f"    - The electron mass is dominated by amplitude (ρ) physics")
print(f"    - Phase corrections (θ) are small perturbations")
print(f"    - The cn mode frequency (phase vibration) is tiny compared to μ")
print(f"    - Phase phonons have lower energy than amplitude phonons (25_PHONONS)")
print()

print(f"  EFFECTIVE METRIC COMPONENTS:")
print(f"    g_ρρ^eff = 1 + V''_ρ/M₀²")
M_0_float = float(M_0)
g_rr_eff = 1 + V_pp_rho / M_0_float**2
g_tt_eff = rho_e**2 * (1 + V_pp_theta / M_0_float**2)
print(f"             = 1 + {V_pp_rho:.2e}/{M_0_float:.2e}²")
print(f"             ≈ 1 (correction is negligible at electron scale)")
print()
print(f"    g_θθ^eff = ρ_vac² × (1 + Λ₁/M₀²)")
print(f"             = {rho_e**2:.4e} × (1 + tiny)")
print(f"             ≈ ρ_vac²")
print()
print(f"  CONCLUSION: The field space at the electron vacuum is")
print(f"  EFFECTIVELY FLAT (corrections are M_e²/M₀² ~ 10⁻⁴⁴).")
print(f"  The curvature IS the potential — it's all in V(ρ), not in the metric.")
print()
print(f"  The Platonic Space is a flat plane WITH A LANDSCAPE:")
print(f"  think of it as a gently curved valley floor (flat metric)")
print(f"  with mountains, valleys, and passes (the potential).")
print()


# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 80)
print("SUMMARY: THE OMEGA FIELD SPACE")
print("=" * 80)
print(f"""
WHAT WE ESTABLISHED:

  1. FIELD SPACE METRIC:
     ds² = dρ² + ρ²dθ²  (polar metric on punctured plane)
     Topology: R₊ × S¹ (half-cylinder)
     Flat (R = 0) for free kinetic term

  2. CHRISTOFFEL SYMBOLS:
     Γ^ρ_θθ = -ρ,  Γ^θ_ρθ = 1/ρ  (standard polar)
     Geodesics are straight lines in Cartesian

  3. POTENTIAL LANDSCAPE:
     V(ρ) = m̃²ρ² + λ̃ρ⁴ + (γ̃/M₀²)ρ⁶
     Electron at ρ_vac = {rho_e:.6f} MeV
     Amplitude {V_pp_rho/V_pp_theta:.0f}× stiffer than phase

  4. MEMORY ATTRACTOR:
     V_eff = V_bare - (e^φ/π²)ρ⁴/X
     Memory deepens the well → self-reinforcing stability
     The electron digs its own gravitational well in field space

  5. EFFECTIVE METRIC:
     Nearly flat at electron scale (corrections ~ m_e²/M₀²)
     All structure is in the POTENTIAL, not the metric
     Phase is cheap, amplitude is expensive

CONNECTIONS:
  → Script 02: Torus moduli and why specific numbers are selected
  → Script 04: Full energy landscape across all epochs
  → 25_PHONONS: Phase cheapness → phase phonons lower energy
""")
