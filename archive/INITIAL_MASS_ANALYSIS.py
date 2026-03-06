#!/usr/bin/env python3
"""
INITIAL MASS m₀ AT PLANCK SCALE
================================

What should the initial dimensionless mass be at the Planck scale?

Date: 2026-02-11
"""

from mpmath import mp, mpf, sqrt, pi as mp_pi, exp, log

mp.dps = 50

print("="*80)
print("INITIAL MASS m₀ ANALYSIS")
print("="*80)
print()

# Constants
phi = (mpf('1') + sqrt(mpf('5'))) / mpf('2')
pi = mp_pi
e = exp(mpf('1'))
alpha_GUT = mpf('1') / (mpf('8') * pi * phi)

print("FUNDAMENTAL SCALES:")
print("-" * 40)
print(f"Planck mass M_P = 1.22 × 10²² MeV")
print(f"Electron mass m_e = 0.511 MeV")
print(f"Ratio m_e/M_P = 4.2 × 10⁻²³")
print()

# =============================================================================
# WHAT IS m̄?
# =============================================================================

print("="*80)
print("WHAT IS THE DIMENSIONLESS MASS m̄?")
print("="*80)
print()

print("In the FRG formalism:")
print("m̄(k) = m(k)/k")
print()
print("where:")
print("• m(k) is the mass parameter at scale k")
print("• k is the RG scale (momentum cutoff)")
print()

print("At Planck scale:")
print("• k = M_P")
print("• m̄₀ = m₀/M_P")
print()

# =============================================================================
# OPTION 1: ZERO INITIAL MASS
# =============================================================================

print("="*80)
print("OPTION 1: m₀ = 0 (MASSLESS AT PLANCK SCALE)")
print("="*80)
print()

print("Arguments FOR:")
print("• All masses generated dynamically")
print("• No fundamental mass scale except M_P")
print("• Clean, minimal assumption")
print()

print("Arguments AGAINST:")
print("• FRG beta function: dm̄/dτ = (1-η_ψ)m̄ + ...")
print("• If m̄₀ = 0, stays at 0 (no seed)")
print("• Need non-zero m̄ to evolve")
print()

# =============================================================================
# OPTION 2: SMALL SEED MASS
# =============================================================================

print("="*80)
print("OPTION 2: SMALL SEED MASS (m̄₀ ~ 0.01)")
print("="*80)
print()

m0_seed = mpf('0.01')
print(f"m̄₀ = {float(m0_seed)}")
print(f"This means m₀ = {float(m0_seed)} × M_P")
print()

print("Arguments FOR:")
print("• Provides seed for RG evolution")
print("• Small enough to be 'natural'")
print("• Allows dynamics to dominate")
print()

print("Arguments AGAINST:")
print("• Arbitrary choice")
print("• Why 0.01 and not 0.001?")
print()

# =============================================================================
# OPTION 3: FROM SYMMETRY BREAKING
# =============================================================================

print("="*80)
print("OPTION 3: FROM GUT SYMMETRY BREAKING")
print("="*80)
print()

print("At Planck scale, SU(5) → SU(3)×SU(2)×U(1)")
print()

# GUT scale
M_GUT = mpf('2e16') / mpf('1.22e22')  # In Planck units
print(f"M_GUT/M_P ≈ {float(M_GUT):.6f}")
print()

print("Natural initial mass from GUT breaking:")
m0_GUT = M_GUT
print(f"m̄₀ = M_GUT/M_P ≈ {float(m0_GUT):.6f}")
print()

# =============================================================================
# OPTION 4: FROM DIMENSIONAL ANALYSIS
# =============================================================================

print("="*80)
print("OPTION 4: FROM DIMENSIONAL ANALYSIS")
print("="*80)
print()

print("The FRG equation in dimensionless form:")
print("dm̄/dτ = (1-η_ψ)m̄ - (1/π²)λ̄_S m̄/(1+m̄²)")
print()

print("For balance at early times:")
print("(1-η_ψ) ≈ (1/π²)λ̄_S/(1+m̄²)")
print()

eta_psi = mpf('0')  # Classical scaling
lambda_S0 = mpf('0.5')  # Initial four-fermion

m0_balance = sqrt(lambda_S0 / pi**2 - mpf('1'))
if m0_balance.imag == 0:
    print(f"Balance point: m̄₀ ≈ {float(m0_balance.real):.6f}")
else:
    print(f"No real balance point for λ̄_S₀ = {float(lambda_S0)}")

print()

# =============================================================================
# OPTION 5: FROM GOLDEN RATIO
# =============================================================================

print("="*80)
print("OPTION 5: FROM GOLDEN RATIO PRINCIPLE")
print("="*80)
print()

print("Golden Universe suggests special values:")
print()

candidates = [
    (mpf('1')/phi, "1/φ"),
    (mpf('1')/phi**2, "1/φ²"),
    (mpf('1')/phi**3, "1/φ³"),
    (mpf('1')/(phi * pi), "1/(φπ)"),
    (alpha_GUT, "α_GUT"),
    (sqrt(alpha_GUT), "√α_GUT"),
]

print("Candidate    | Value      | Physical meaning")
print("-" * 50)
for value, name in candidates:
    print(f"{name:12} | {float(value):.8f} | Natural scale from φ")

print()

# =============================================================================
# RG FLOW TEST
# =============================================================================

print("="*80)
print("RG FLOW FROM DIFFERENT m̄₀")
print("="*80)
print()

def simple_rg_flow(m0, steps=10):
    """Simple RG evolution"""
    m = m0
    tau = mpf('0')
    dtau = mpf('0.1')

    lambda_S = mpf('0.5')

    path = []
    for i in range(steps):
        dm = m - (mpf('1')/pi**2) * lambda_S * m / (mpf('1') + m**2)
        m = m + dm * dtau
        tau += dtau
        lambda_S *= mpf('0.95')  # Decay
        path.append(float(m))

    return path

print("Evolution for first 10 steps:")
print("-" * 40)

test_m0 = [mpf('0.001'), mpf('0.01'), mpf('0.1'), mpf('1')/phi**2]

for m0 in test_m0:
    path = simple_rg_flow(m0, 10)
    print(f"m̄₀ = {float(m0):.6f} → {path[-1]:.6f}")

print()

# =============================================================================
# THEORETICAL CONSTRAINT
# =============================================================================

print("="*80)
print("THEORETICAL CONSTRAINT FROM GOLDEN UNIVERSE")
print("="*80)
print()

print("From theory-laws.md:")
print("• All scales from φ, π, e")
print("• No arbitrary parameters")
print()

print("This suggests m̄₀ should be:")
print("• Derived from α_GUT = 1/(8πφ)")
print("• Or from golden ratio directly")
print()

m0_theory = mpf('1') / phi**2
print(f"Most natural: m̄₀ = 1/φ² = {float(m0_theory):.10f}")
print()

print("This gives:")
print(f"• Clean golden ratio origin")
print(f"• Small but non-zero ({float(m0_theory):.4f})")
print(f"• Allows RG evolution")
print()

# =============================================================================
# RECOMMENDATION
# =============================================================================

print("="*80)
print("RECOMMENDATION")
print("="*80)
print()

print("USE: m̄₀ = 1/φ² = 0.3820")
print()
print("Reasons:")
print("1. Non-zero (allows RG flow)")
print("2. From golden ratio (no arbitrariness)")
print("3. Natural scale O(1) in Planck units")
print("4. Consistent with Golden Universe principles")
print()

print("Alternative: m̄₀ = α_GUT = 0.0156")
print("(Also from first principles)")
print()

print("AVOID:")
print("• m̄₀ = 0 (no evolution)")
print("• m̄₀ = arbitrary number (not from φ, π, e)")
print("• m̄₀ = 1 (too large, unnatural)")
print()

print("="*80)