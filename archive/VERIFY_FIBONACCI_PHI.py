#!/usr/bin/env python3
"""
VERIFY: Is φ_111 = F_112/F_111 equal to φ asymptotic?
Check if document's φ^111 value is correct
"""

from mpmath import mp, mpf, sqrt, sin, pi as mp_pi

mp.dps = 50

print("="*80)
print("VERIFY FIBONACCI RATIO vs GOLDEN RATIO")
print("="*80)

# Golden ratio (exact)
phi_exact = (1 + sqrt(5)) / 2
print(f"\nφ (exact) = (1+√5)/2 = {phi_exact}")

# Calculate Fibonacci numbers up to F_112
def fibonacci(n):
    """Calculate Fibonacci number F_n"""
    if n == 0:
        return mpf('0')
    elif n == 1:
        return mpf('1')
    
    a, b = mpf('0'), mpf('1')
    for _ in range(2, n+1):
        a, b = b, a + b
    return b

print(f"\nCalculating F_111 and F_112...")
F_111 = fibonacci(111)
F_112 = fibonacci(112)

print(f"\nF_111 = {F_111}")
print(f"F_112 = {F_112}")

phi_111 = F_112 / F_111
print(f"\nφ_111 = F_112/F_111 = {phi_111}")

print(f"\nComparison:")
print(f"φ (exact)  = {phi_exact}")
print(f"φ_111      = {phi_111}")
print(f"Difference = {abs(phi_111 - phi_exact)}")
print(f"Relative   = {float(abs(phi_111 - phi_exact) / phi_exact * 100):.6e}%")

print(f"\nFor practical purposes: φ_111 ≈ φ (difference < 10^-40)")

# Now calculate φ^111 with both values
print(f"\n" + "="*80)
print("CALCULATE φ^111")
print("="*80)

phi_pow_exact = phi_exact ** 111
phi_pow_111 = phi_111 ** 111

print(f"\nφ^111 (using φ exact)     = {phi_pow_exact}")
print(f"φ^111 (using φ_111)       = {phi_pow_111}")
print(f"\nScientific notation:")
print(f"φ^111 (φ exact)  = {float(phi_pow_exact):.10e}")
print(f"φ^111 (φ_111)    = {float(phi_pow_111):.10e}")

# Document claims φ^111 ≈ 2.15579×10²³
phi_doc = mpf('2.15579e23')
print(f"\nDocument claims: φ^111 ≈ 2.15579×10²³")
print(f"Ratio (doc/calculated): {phi_doc / phi_pow_exact}")

# Try with 2π instead of 2π_111
print(f"\n" + "="*80)
print("TRY DIFFERENT FORMULA INTERPRETATIONS")
print("="*80)

M_P = mpf('1.22091e+22')
C_e = mpf('1.64894')
N_e = 111
pi_111 = N_e * sin(mp_pi / N_e)
phi = phi_exact

# Method 1: My interpretation
m_e_v1 = M_P * (2 * pi_111 * C_e) / (phi_111 ** N_e)
print(f"\nV1: M_P · (2π_111 · C_e / φ_111^111) = {m_e_v1} MeV")
error_v1 = float((m_e_v1 - mpf('0.51099895')) / mpf('0.51099895') * 100)
print(f"    Error: {error_v1:+.2f}%")

# Method 2: Maybe it's (2π/φ^N) · C_e not 2π·C_e/φ^N?
m_e_v2 = M_P * (2 * mp_pi / (phi ** N_e)) * C_e
print(f"\nV2: M_P · (2π/φ^N) · C_e = {m_e_v2} MeV")
error_v2 = float((m_e_v2 - mpf('0.51099895')) / mpf('0.51099895') * 100)
print(f"    Error: {error_v2:+.2f}%")

# Method 3: Maybe NO 2π factor?
m_e_v3 = M_P * C_e / (phi ** N_e)
print(f"\nV3: M_P · (C_e / φ^N) = {m_e_v3} MeV")
error_v3 = float((m_e_v3 - mpf('0.51099895')) / mpf('0.51099895') * 100)
print(f"    Error: {error_v3:+.2f}%")

# Method 4: Maybe C_e is ALREADY including the 2π factor?
C_e_adjusted = C_e / (2 * pi_111)
m_e_v4 = M_P * C_e_adjusted / (phi ** N_e)
print(f"\nV4: M_P · (C_e/(2π_111)) / φ^N = {m_e_v4} MeV")
error_v4 = float((m_e_v4 - mpf('0.51099895')) / mpf('0.51099895') * 100)
print(f"    Error: {error_v4:+.2f}%")

# Find what C_e SHOULD be for perfect match
print(f"\n" + "="*80)
print("REVERSE CALCULATION")
print("="*80)

m_e_target = mpf('0.51099895')
C_e_needed = m_e_target * (phi ** N_e) / (M_P * 2 * pi_111)
print(f"\nFor m_e = {m_e_target} MeV with formula M_P·(2π_111·C_e/φ^111):")
print(f"Required C_e = {C_e_needed}")
print(f"Document has C_e = {C_e}")
print(f"Ratio: {C_e / C_e_needed}")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)
print("\nEither:")
print("1. Document's φ^111 = 2.15579×10²³ is WRONG (should be 1.576×10²³)")
print("2. OR document is using DIFFERENT formula structure")
print("3. OR C_e = 1.64894 is not the right value for this formula")
print("\nMy Phase 23 elliptic formula with C_e=1.0479 gives -0.21% ✅")
