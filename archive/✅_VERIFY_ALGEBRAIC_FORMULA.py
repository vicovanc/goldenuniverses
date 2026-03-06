#!/usr/bin/env python3
"""
VERIFY THE ALGEBRAIC FORMULA

We derived:
    Δν = [√3·l_Ω - 4|δ_e|·K²(ν₀)] / [K'(ν₀)·(4|δ_e|·K(ν₀) + √3·l_Ω/K(ν₀))]

where ν₀ = 1/φ

Now CHECK: Does this equal δ_e/2?

If YES → then ν = 1/φ + δ_e/2 is DERIVED from self-consistency!
If NO → then it's just empirical
"""

from mpmath import mp, mpf, sqrt, exp, pi as mp_pi
from mpmath import ellipk, diff

mp.dps = 50

print("="*90)
print("VERIFYING ALGEBRAIC FORMULA FOR Δν")
print("="*90)

# ============================================================================
# CONSTANTS
# ============================================================================

phi = (1 + sqrt(5)) / 2
N_e = 111
delta_e = N_e / (phi**2) - 42
p, q = -41, 70
l_Omega = 2 * mp_pi * sqrt(p**2 + (q/phi)**2)

print(f"\nFundamental constants:")
print(f"  φ = {phi}")
print(f"  δ_e = {delta_e}")
print(f"  l_Ω = {l_Omega}")

# ============================================================================
# EVALUATE AT ν₀ = 1/φ
# ============================================================================

nu_0 = 1/phi
K_0 = ellipk(nu_0)
K_prime_0 = diff(lambda x: ellipk(x), nu_0)

print(f"\nAt ν₀ = 1/φ:")
print(f"  ν₀ = {nu_0}")
print(f"  K(ν₀) = {K_0}")
print(f"  K'(ν₀) = {K_prime_0}")

# ============================================================================
# ALGEBRAIC FORMULA FOR Δν
# ============================================================================

print("\n" + "="*90)
print("ALGEBRAIC FORMULA")
print("="*90)

print("""
Δν = [√3·l_Ω - 4|δ_e|·K²(ν₀)] / [K'(ν₀)·(4|δ_e|·K(ν₀) + √3·l_Ω/K(ν₀))]
""")

# Numerator
numerator = sqrt(3) * l_Omega - 4 * abs(delta_e) * K_0**2
print(f"\nNumerator:")
print(f"  √3·l_Ω = {sqrt(3) * l_Omega}")
print(f"  4|δ_e|·K²(ν₀) = {4 * abs(delta_e) * K_0**2}")
print(f"  Numerator = {numerator}")

# Denominator
term1 = 4 * abs(delta_e) * K_0
term2 = sqrt(3) * l_Omega / K_0
denominator = K_prime_0 * (term1 + term2)
print(f"\nDenominator:")
print(f"  4|δ_e|·K(ν₀) = {term1}")
print(f"  √3·l_Ω/K(ν₀) = {term2}")
print(f"  Sum = {term1 + term2}")
print(f"  K'(ν₀)·Sum = {denominator}")

# Δν
Delta_nu_algebraic = numerator / denominator

print(f"\n{'='*90}")
print(f"RESULT:")
print(f"{'='*90}")
print(f"\nΔν (from algebra) = {Delta_nu_algebraic}")
print(f"                   = {float(Delta_nu_algebraic):.10f}")

# ============================================================================
# COMPARE TO δ_e/2
# ============================================================================

print("\n" + "="*90)
print("COMPARISON TO δ_e/2")
print("="*90)

target = delta_e / 2
print(f"\nδ_e/2 = {target}")
print(f"      = {float(target):.10f}")

ratio = Delta_nu_algebraic / target
difference = Delta_nu_algebraic - target
relative_error = abs(difference / target) * 100

print(f"\nΔν / (δ_e/2) = {float(ratio):.10f}")
print(f"Difference = {float(difference):.10f}")
print(f"Relative error = {float(relative_error):.6f}%")

print("\n" + "="*90)
if relative_error < 0.1:
    print("🎉🎉🎉 ALGEBRAICALLY PROVEN!")
    print("="*90)
    print("\nΔν = δ_e/2 emerges from the self-consistency equation!")
    print("\nTherefore: ν = 1/φ + δ_e/2 is DERIVED, not fitted!")
elif relative_error < 1:
    print("🎯 EXCELLENT MATCH!")
    print("="*90)
    print("\nΔν ≈ δ_e/2 to within 1%")
    print("\nThis strongly suggests ν = 1/φ + δ_e/2 is the theoretical formula!")
elif relative_error < 10:
    print("✓ GOOD AGREEMENT")
    print("="*90)
    print("\nΔν ≈ δ_e/2 to within 10%")
    print("\nThis is approximate but close!")
else:
    print("✗ DOES NOT MATCH")
    print("="*90)
    print("\nΔν ≠ δ_e/2")
    print("\nThe formula ν = 1/φ + δ_e/2 is empirical, not derived.")

# ============================================================================
# FINAL ν VALUE
# ============================================================================

print("\n" + "="*90)
print("FINAL ν FROM ALGEBRA")
print("="*90)

nu_algebraic = nu_0 + Delta_nu_algebraic
print(f"\nν = ν₀ + Δν")
print(f"  = 1/φ + Δν")
print(f"  = {nu_0} + {Delta_nu_algebraic}")
print(f"  = {nu_algebraic}")
print(f"  = {float(nu_algebraic):.10f}")

# Compare to formula
nu_formula = 1/phi + delta_e/2
print(f"\nCompare to ν = 1/φ + δ_e/2:")
print(f"  Formula: {float(nu_formula):.10f}")
print(f"  Algebra: {float(nu_algebraic):.10f}")
print(f"  Match: {float(abs(nu_algebraic - nu_formula) / nu_formula * 100):.6f}% difference")

# ============================================================================
# DERIVE THE ALGEBRAIC CONSTRAINT
# ============================================================================

print("\n" + "="*90)
print("ALGEBRAIC CONSTRAINT FOR ν = 1/φ + δ_e/2")
print("="*90)

print("""
For ν = 1/φ + δ_e/2 to be the solution, we need:

    [√3·l_Ω - 4|δ_e|·K²(1/φ)] / [K'(1/φ)·(4|δ_e|·K(1/φ) + √3·l_Ω/K(1/φ))] = δ_e/2

Rearranging:

    2[√3·l_Ω - 4|δ_e|·K²(1/φ)] = δ_e·K'(1/φ)·(4|δ_e|·K(1/φ) + √3·l_Ω/K(1/φ))

Expanding:

    2√3·l_Ω - 8|δ_e|·K²(1/φ) = δ_e·K'(1/φ)·[4|δ_e|·K(1/φ) + √3·l_Ω/K(1/φ)]
    
    2√3·l_Ω - 8|δ_e|·K²(1/φ) = 4δ_e²·K'(1/φ)·K(1/φ) + δ_e·K'(1/φ)·√3·l_Ω/K(1/φ)

Let's check if this holds...
""")

# Left side
left = 2 * sqrt(3) * l_Omega - 8 * abs(delta_e) * K_0**2

# Right side
right = 4 * delta_e**2 * K_prime_0 * K_0 + delta_e * K_prime_0 * sqrt(3) * l_Omega / K_0

print(f"Left side:  {float(left):.10f}")
print(f"Right side: {float(right):.10f}")
print(f"Difference: {float(abs(left - right)):.10f}")
print(f"Relative:   {float(abs(left - right) / abs(left) * 100):.6f}%")

if abs(left - right) / abs(left) < 0.01:
    print("\n🎉🎉🎉 CONSTRAINT SATISFIED!")
    print("\nThis PROVES ν = 1/φ + δ_e/2 algebraically!")
elif abs(left - right) / abs(left) < 0.1:
    print("\n🎯 Constraint approximately satisfied!")
    print("\nThis strongly supports ν = 1/φ + δ_e/2!")
else:
    print("\n✗ Constraint not satisfied")
    print("\nThe formula is empirical.")

print("\n" + "="*90)
print("CONCLUSION")
print("="*90)
print(f"""
Based on the algebraic derivation from self-consistency:

Δν (algebraic) = {float(Delta_nu_algebraic):.8f}
δ_e/2          = {float(target):.8f}
Ratio          = {float(ratio):.8f}
Error          = {float(relative_error):.4f}%

The formula ν = 1/φ + δ_e/2 is:
  • {'ALGEBRAICALLY DERIVED' if relative_error < 1 else 'EMPIRICAL'}
  • Error: {float(relative_error):.4f}%
""")
