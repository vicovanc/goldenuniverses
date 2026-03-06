#!/usr/bin/env python3
"""
ν FROM THE EQUATIONS — NOT FROM GUESSING
==========================================

The correction to ν should come from the DERIVED equations (Laws 18, 30-35),
not from numerical exploration. This script traces the full chain:

  V''_lock(0; 111) → μ → ν → C_e → m_e

Chain of derived laws:
  Law 18 Lemma 3:  μ² = l²_Ω · V''_lock(0) / ρ²_vac
  Law 30 (kink):   θ_K(s) = 4 arctan(e^{μs}) on torus of length l_Ω
  Law 35 (closure): 4K(ν) = μ · l_Ω  (periodicity of kink on torus)
  Law 34 (Route B): C_e = G_e · 2μ · C_GY(μ)
  or
  Law 33 (Route A): C_e(ν) = |δ_e|·K(ν) + ... (elliptic formula)

The ν_topo we computed is a GEOMETRIC quantity from the winding numbers.
The PHYSICAL ν comes from the kink equation on the torus: 4K(ν) = μ·l_Ω.
The "correction" is the difference between ν_geometric and ν_physical.

Date: February 2026
"""

from mpmath import (
    mp, mpf, sqrt, pi as mp_pi, exp,
    ellipk, ellipe, findroot, nstr,
    sinh, cosh, ln
)

mp.dps = 50

# =============================================================================
# DERIVED CONSTANTS
# =============================================================================

phi = (mpf('1') + sqrt(mpf('5'))) / 2
pi = mp_pi
alpha_EM = mpf('1') / mpf('137.035999177')
M_P = mpf('1.2208901286e22')
m_e_CODATA = mpf('0.51099895069')
eta_QED = 1 - alpha_EM / (2 * pi)
lambda_rec_beta = exp(phi) / pi**2

N_e = 111
p_e, q_e = -41, 70

# Derived geometry
q_over_phi = mpf(q_e) / phi
l_Omega = 2 * pi * sqrt(mpf(p_e)**2 + q_over_phi**2)
nu_topo = abs(q_over_phi) / sqrt(mpf(p_e)**2 + q_over_phi**2)
delta_e = mpf(N_e) / phi**2 - 42
G_e = sqrt(mpf('5') / mpf('3'))

prefactor = M_P * 2 * pi / phi**N_e
C_e_target = m_e_CODATA / (prefactor * eta_QED)

def C_GY(mu):
    """Gel'fand-Yaglom determinant (Law 18, Lemma 5)"""
    return sqrt((mu + sinh(mu)) / (sinh(mu) * (cosh(mu) + 1)))

def Ce_route_A(nu):
    """Route A elliptic formula (Law 33) — BREAKTHROUGH version"""
    K = ellipk(nu)
    E = ellipe(nu)
    return abs(delta_e)*K + nu/2 - lambda_rec_beta*(K-E)/3 + alpha_EM/(2*pi)

def Ce_route_B(mu):
    """Route B Gel'fand-Yaglom formula (Law 34)"""
    return G_e * 2 * mu * C_GY(mu)

# =============================================================================
# THE EQUATION CHAIN
# =============================================================================

print("=" * 80)
print("THE EQUATION CHAIN: V''_lock → μ → ν → C_e → m_e")
print("=" * 80)
print()

print("""
The derived equations (ALL from theory/theory-laws.md):

  1. Law 18 Lemma 3:  μ² = l²_Ω · V''_lock(0; 111) / ρ²_vac(111)
  2. Law 35 Scale 1:  4K(ν) = μ_closure · l_Ω
  3. Law 33 Route A:  C_e(ν) = |δ_e|·K(ν) + ν/2 − (e^φ/π²)(K−E)/3 + α/(2π)
  4. Law 34 Route B:  C_e(μ) = √(5/3) · 2μ · C_GY(μ)
  5. Mass formula:    m_e = M_P · (2π/φ^111) · C_e · η_QED

  The PHYSICAL ν comes from equation (2), not from topology directly.
  ν_topo is a geometric approximation to this physical ν.
""")

# =============================================================================
# STEP 1: What value of V''_lock/ρ² is needed?
# =============================================================================

print("=" * 80)
print("STEP 1: WORK BACKWARDS — What V''_lock/ρ² gives exact m_e?")
print("=" * 80)
print()

# Route B directly: find μ_sc from C_e_target
mu_sc = findroot(lambda mu: Ce_route_B(mu) - C_e_target, mpf('0.42'))

# Route A: find ν_exact
nu_exact = findroot(
    lambda nu: Ce_route_A(nu) - C_e_target,
    (mpf('0.70'), mpf('0.73'))
)

# From ν_exact, get μ_closure via 4K(ν) = μ · l_Ω
mu_closure_exact = 4 * ellipk(nu_exact) / l_Omega

# From μ_sc and l_Ω, get the needed V''_lock/ρ² (Lemma 3)
# μ²_sc = l²_Ω · V''_lock / ρ²_vac
# → V''_lock / ρ²_vac = μ²_sc / l²_Ω
ratio_needed_sc = mu_sc**2 / l_Omega**2

# Also from μ_closure:
ratio_needed_clos = mu_closure_exact**2 / l_Omega**2

print("Working backwards from m_e = 0.511 MeV:")
print()
print(f"  Route B (Law 34) requires:")
print(f"    μ_sc = {nstr(mu_sc, 15)}")
print(f"    → V''_lock / ρ²_vac = μ²/l²_Ω = {float(ratio_needed_sc):.15e}")
print()
print(f"  Route A (Law 33) requires:")
print(f"    ν = {nstr(nu_exact, 15)}")
print(f"    → μ_closure = 4K(ν)/l_Ω = {nstr(mu_closure_exact, 15)}")
print(f"    → V''_lock / ρ²_vac = μ²/l²_Ω = {float(ratio_needed_clos):.15e}")
print()

# Now from ν_topo:
mu_closure_topo = 4 * ellipk(nu_topo) / l_Omega
ratio_topo = mu_closure_topo**2 / l_Omega**2

print(f"  From ν_topo (geometry):")
print(f"    ν_topo = {nstr(nu_topo, 15)}")
print(f"    → μ_clos = {nstr(mu_closure_topo, 15)}")
print(f"    → V''_lock / ρ²_vac = {float(ratio_topo):.15e}")
print()

delta_ratio = ratio_topo - ratio_needed_clos
print(f"  Gap in V''_lock/ρ²:")
print(f"    Δ(V''/ρ²) = {float(delta_ratio):.6e}")
print(f"    Relative:   {float(delta_ratio/ratio_needed_clos * 100):+.4f}%")
print()

# =============================================================================
# STEP 2: What determines V''_lock/ρ² in the FRG?
# =============================================================================

print("=" * 80)
print("STEP 2: V''_lock/ρ² FROM THE FRG EQUATIONS")
print("=" * 80)
print()

print("""
From the Lagrangian (theory/theory-laws.md):
  V_lock(θ; X) = Σ_{m≥1} Λ_m(X) · [1 − cos(mθ)]
  V''_lock(0; X) = Σ_{m≥1} m² · Λ_m(X)

For the dominant m=1 harmonic:
  V''_lock(0) ≈ Λ₁(X₁₁₁)

The FRG β function for Λ₁ (from §EVAL-6):
  ∂_t Λ̄₁ = (2 + 2η_ψ) · Λ̄₁ + (lock-sector bubble)

At LEADING order: β_Λ₁ ≈ 0 (marginal coupling)
→ Λ₁(X₁₁₁) ≈ Λ₁(M_P) = const

So: V''_lock / ρ²_vac ≈ Λ₁(UV) / ρ²_vac(111)
""")

# What Λ₁/ρ² is needed?
print(f"Needed: V''_lock/ρ²_vac = {float(ratio_needed_clos):.6e}")
print()

# Two scenarios:
# A) ρ_vac is the dimensionless FRG field at vacuum (ρ̄ = ρ/X)
# B) ρ_vac is the physical field value

# In scenario A: if ρ̄_vac ~ O(1), then Λ₁ ~ 10⁻⁹ (very small)
# In scenario B: Λ₁/v₁₁₁² with v₁₁₁ ~ X₁₁₁

print("If ρ̄_vac = 1 (dimensionless): Λ₁ needed = {:.6e}".format(float(ratio_needed_clos)))
print("If ρ̄_vac = m̄★ ≈ 4514:        Λ₁ needed = {:.6e}".format(float(ratio_needed_clos * 4514**2)))
print("If ρ̄_vac = φ²:               Λ₁ needed = {:.6e}".format(float(ratio_needed_clos * phi**4)))
print()

# =============================================================================
# STEP 3: THE EQUATION THAT DETERMINES ν (not guessing!)
# =============================================================================

print("=" * 80)
print("STEP 3: THE EQUATION THAT DETERMINES ν")
print("=" * 80)
print()

print("""
EQUATION (Law 35 + Law 18 Lemma 3):

  4K(ν_physical) = μ · l_Ω = l_Ω · √(l²_Ω · V''_lock / ρ²_vac)
                 = l²_Ω · √(V''_lock / ρ²_vac)

So: K(ν) = (l²_Ω / 4) · √(V''_lock / ρ²_vac)

Given l_Ω = 374.50:
  K(ν) = (374.50² / 4) · √(V''_lock / ρ²_vac)
       = 35,063 · √(V''_lock / ρ²_vac)

This is THE equation that determines ν from the lock physics.
""")

# Compute K for exact ν
K_exact = ellipk(nu_exact)
K_topo = ellipk(nu_topo)

print(f"At ν_exact: K = {nstr(K_exact, 15)}")
print(f"At ν_topo:  K = {nstr(K_topo, 15)}")
print(f"ΔK = {float(K_topo - K_exact):.10f}")
print(f"ΔK/K = {float((K_topo-K_exact)/K_exact*100):+.6f}%")
print()

# The lock ratio that gives K_exact:
lock_ratio_needed = (4 * K_exact / l_Omega**2)**2
print(f"Lock ratio V''/ρ² needed for ν_exact:")
print(f"  V''/ρ² = (4K/l²_Ω)² = {float(lock_ratio_needed):.15e}")
print()

# =============================================================================
# STEP 4: SCAN — m_e as function of V''_lock/ρ²
# =============================================================================

print("=" * 80)
print("STEP 4: m_e AS FUNCTION OF V''_lock/ρ² (the missing FRG output)")
print("=" * 80)
print()

print(f"{'V''/ρ²':>14s} | {'μ_closure':>12s} | {'ν':>12s} | {'C_e(ν)':>12s} | {'m_e (MeV)':>12s} | {'Error':>10s}")
print("─" * 85)

# Scan V''/ρ² around the needed value
r_exact = float(ratio_needed_clos)
for factor in [0.5, 0.8, 0.9, 0.95, 0.99, 1.0, 1.005, 1.01, 1.05, 1.1, 1.2, 1.5, 2.0]:
    r = mpf(str(r_exact * factor))
    mu_c = l_Omega * sqrt(r)  # μ_closure from Lemma 3
    # 4K(ν) = μ · l_Ω
    target_K = mu_c * l_Omega / 4
    # Solve K(ν) = target_K
    try:
        nu = findroot(lambda n: ellipk(n) - target_K, mpf('0.5'))
        if hasattr(nu, 'imag') and abs(nu.imag) > 1e-20:
            continue
        nu = nu.real if hasattr(nu, 'real') else nu
        if nu <= 0 or nu >= 1:
            continue
        Ce = Ce_route_A(nu)
        me = prefactor * Ce * eta_QED
        err = float((me - m_e_CODATA)/m_e_CODATA * 100)
        marker = "★★" if abs(err) < 0.02 else "★" if abs(err) < 0.1 else ""
        print(f"  {float(r):12.6e} | {float(mu_c):12.8f} | {float(nu):12.8f} | "
              f"{float(Ce):12.8f} | {float(me):12.8f} | {err:+9.4f}% {marker}")
    except Exception as e:
        print(f"  {float(r):12.6e} | failed: {e}")

print()

# =============================================================================
# STEP 5: THE PHYSICAL PICTURE
# =============================================================================

print("=" * 80)
print("STEP 5: THE PHYSICAL PICTURE — WHY ν_topo ≠ ν_physical")
print("=" * 80)
print()

print("""
ν_topo = |q/φ| / √(p² + (q/φ)²) = sin(arctan(|q|/(|p|φ)))

This is the GEOMETRIC angle of the winding path on the torus.
It answers: "What direction does the path go?"

ν_physical = K⁻¹( μ·l_Ω/4 )

This is the ELLIPTIC MODULUS of the kink profile on the torus.
It answers: "How does the kink's shape adapt to the torus size?"

These are DIFFERENT QUESTIONS answered by DIFFERENT EQUATIONS.

The fact that ν_topo ≈ ν_physical (within 0.7%) is because the
torus geometry CONSTRAINS the kink shape. But the constraint is
not exact — the lock potential curvature V''_lock introduces
a correction.

THE CORRECTION IS NOT AD-HOC. IT IS:
  ν_physical = K⁻¹( l²_Ω · √(V''/ρ²) / 4 )
       vs
  ν_topo = sin(arctan(|q|/(|p|φ)))

The difference comes from the LOCK POTENTIAL CURVATURE V''_lock/ρ².
""")

# What lock ratio gives ν_topo (i.e., no correction)?
K_topo_val = ellipk(nu_topo)
mu_clos_topo = 4 * K_topo_val / l_Omega
r_topo = mu_clos_topo**2 / l_Omega**2

print(f"For ν_topo (no correction):")
print(f"  V''/ρ² would need to be:  {float(r_topo):.15e}")
print()
print(f"For ν_exact (correct m_e):")
print(f"  V''/ρ² needs to be:       {float(ratio_needed_clos):.15e}")
print()
print(f"Ratio: {float(r_topo/ratio_needed_clos):.10f}")
print(f"Relative shift: {float((r_topo - ratio_needed_clos)/ratio_needed_clos * 100):+.4f}%")
print()

# =============================================================================
# STEP 6: IS THERE A φ,π EXPRESSION FOR THE LOCK RATIO?
# =============================================================================

print("=" * 80)
print("STEP 6: SEARCHING FOR V''_lock/ρ² IN TERMS OF φ, π")
print("=" * 80)
print()

r_needed = ratio_needed_clos

# What simple expressions give a number close to r_needed?
expressions = {
    '1/(4π²φ² N²_e)':        1/(4*pi**2*phi**2*N_e**2),
    '1/(l²_Ω · N_e)':        1/(l_Omega**2 * N_e),
    '(2π/l_Ω)^4':            (2*pi/l_Omega)**4,
    'α²/(l²_Ω)':             alpha_EM**2 / l_Omega**2,
    '1/(l⁴_Ω)':              1/l_Omega**4,
    '1/(4π N_e l²_Ω)':       1/(4*pi*N_e*l_Omega**2),
    '(λ_rec/β)²/(l⁴_Ω)':    lambda_rec_beta**2 / l_Omega**4,
    'φ^(-2N)/(4π²)':         phi**(-2*N_e)/(4*pi**2),
    'α/(2π l²_Ω N_e)':       alpha_EM/(2*pi*l_Omega**2*N_e),
    '1/(2π²φ²l²_Ω)':        1/(2*pi**2*phi**2*l_Omega**2),
    'δ²_e/l⁴_Ω':             delta_e**2/l_Omega**4,
    '1/(8π³φ l²_Ω)':         1/(8*pi**3*phi*l_Omega**2),
    '(λ_rec/β)/(N_e l²_Ω)':  lambda_rec_beta/(N_e*l_Omega**2),
    'φ⁻⁴/l²_Ω':              phi**(-4)/l_Omega**2,
    '1/(π φ l_Ω)⁴':          1/(pi*phi*l_Omega)**4,
}

print(f"  r_needed = V''/ρ² = {float(r_needed):.6e}")
print()
print(f"  {'Expression':30s} | {'Value':>14s} | {'Ratio to needed':>16s}")
print("  " + "─" * 70)

expr_results = []
for label, val in expressions.items():
    ratio = float(val / r_needed)
    expr_results.append((abs(ratio - 1), label, float(val), ratio))

expr_results.sort()
for _, label, val, ratio in expr_results[:12]:
    marker = "★" if abs(ratio - 1) < 0.1 else ""
    print(f"  {label:30s} | {val:14.6e} | {ratio:16.6f} {marker}")

print()

# =============================================================================
# STEP 7: THE HONEST BOTTOM LINE
# =============================================================================

print("=" * 80)
print("THE HONEST BOTTOM LINE")
print("=" * 80)
print(f"""
THE EQUATION CHAIN IS COMPLETE AND DERIVED:

  1. l_Ω = 2π√(p²+(q/φ)²) = {float(l_Omega):.4f}          [✅ DERIVED]
  2. V''_lock / ρ² = ??? (from FRG lock-sector)       [❌ NOT YET COMPUTED]
  3. μ = l_Ω · √(V''/ρ²)                              [✅ DERIVED formula]
  4. 4K(ν) = μ · l_Ω → ν                              [✅ DERIVED equation]
  5. C_e(ν) → m_e                                     [✅ DERIVED formula]

The SINGLE missing number is: V''_lock(0; 111) / ρ²_vac(111)

  Needed value: {float(r_needed):.6e}

This comes from the FRG lock-sector flow:
  V''_lock = Σ m² Λ_m(X₁₁₁)
  ρ_vac = |Ω_c|_vacuum at epoch 111

The lock-sector β functions (currently frozen at β = 0) are:
  ∂_t Λ̄_m = (2 + 2η_ψ)Λ̄_m + (lock bubble from Wetterich STr)

To COMPUTE this ratio, we need to:
  1. Evaluate the Wetterich supertrace projected onto cos(mθ)
  2. This gives the lock-sector β functions
  3. Flow Λ₁ from Planck to epoch 111
  4. Extract V''_lock = Λ₁(111)
  5. Get ρ_vac from the potential minimum at epoch 111

CURRENT STATUS:
  ✅ Steps 1, 3, 4, 5 of the equation chain are implemented
  ❌ Step 2 requires the Wetterich supertrace evaluation
  
  The "ν²/N correction" we found numerically is an APPROXIMATION
  to the exact correction that comes from step 2.

  When we compute V''/ρ² properly, the correction will emerge
  AUTOMATICALLY from the equations — no guessing needed.
""")
