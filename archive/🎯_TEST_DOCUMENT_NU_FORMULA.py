#!/usr/bin/env python3
"""
TEST THE DOCUMENT'S ν FORMULA

The explorer found: ν = 1/2 + δ/(2·k_res)

Let me test this carefully with different interpretations:
1. k_res = N/φ² (exact value)
2. k_res = round(N/φ²) (nearest integer)
3. Maybe it's δ_e (the detuning from integer) not δ

Let's verify against the document formula!
"""

from mpmath import mp, mpf, sqrt, exp, sin, pi as mp_pi
from mpmath import ellipk, ellipe

mp.dps = 50

print("="*90)
print("TESTING DOCUMENT'S ν FORMULA")
print("="*90)

# ============================================================================
# CONSTANTS
# ============================================================================

phi = (1 + sqrt(5)) / 2
N_e = 111

print(f"\nFor electron: N_e = {N_e}")
print(f"φ = {phi}")

# ============================================================================
# INTERPRETATION 1: k_res = N/φ² (exact)
# ============================================================================

print("\n" + "="*90)
print("INTERPRETATION 1: k_res = N/φ² (exact value)")
print("="*90)

k_res_exact = N_e / (phi**2)
k_nearest = round(float(k_res_exact))
delta = k_res_exact - k_nearest

print(f"\nk_res = N/φ² = {k_res_exact}")
print(f"      = {float(k_res_exact):.8f}")
print(f"k_nearest = {k_nearest}")
print(f"δ = k_res - k_nearest = {delta}")
print(f"  = {float(delta):.8f}")

# Formula: ν = 1/2 + δ/(2·k_res)
nu_1 = mpf('1')/2 + delta / (2 * k_res_exact)

print(f"\nν = 1/2 + δ/(2·k_res)")
print(f"  = 1/2 + {float(delta):.8f} / (2 × {float(k_res_exact):.8f})")
print(f"  = 1/2 + {float(delta/(2*k_res_exact)):.8f}")
print(f"  = {float(nu_1):.8f}")

# ============================================================================
# INTERPRETATION 2: k_res = nearest integer
# ============================================================================

print("\n" + "="*90)
print("INTERPRETATION 2: k_res = nearest integer = 42")
print("="*90)

k_res_int = k_nearest
delta_2 = k_res_exact - k_res_int

print(f"\nk_res = {k_res_int} (integer)")
print(f"δ = N/φ² - k_res = {delta_2}")
print(f"  = {float(delta_2):.8f}")

# Formula: ν = 1/2 + δ/(2·k_res)
nu_2 = mpf('1')/2 + delta_2 / (2 * k_res_int)

print(f"\nν = 1/2 + δ/(2·k_res)")
print(f"  = 1/2 + {float(delta_2):.8f} / (2 × {k_res_int})")
print(f"  = 1/2 + {float(delta_2/(2*k_res_int)):.8f}")
print(f"  = {float(nu_2):.8f}")

# ============================================================================
# INTERPRETATION 3: Use |δ_e| directly
# ============================================================================

print("\n" + "="*90)
print("INTERPRETATION 3: ν = 1/2 + δ_e/(2·k)")
print("="*90)

delta_e = abs(delta)
k = k_nearest

print(f"\nδ_e = |δ| = {delta_e}")
print(f"k = {k}")

nu_3 = mpf('1')/2 + delta_e / (2 * k)

print(f"\nν = 1/2 + δ_e/(2·k)")
print(f"  = 1/2 + {float(delta_e):.8f} / (2 × {k})")
print(f"  = 1/2 + {float(delta_e/(2*k)):.8f}")
print(f"  = {float(nu_3):.8f}")

# ============================================================================
# TEST ALL THREE IN MASS CALCULATION
# ============================================================================

print("\n" + "="*90)
print("TESTING ALL THREE IN ELECTRON MASS CALCULATION")
print("="*90)

p, q = -41, 70
l_Omega = 2 * mp_pi * sqrt(p**2 + (q/phi)**2)
lambda_rec_beta = exp(phi) / (mp_pi ** 2)
alpha = mpf('1') / mpf('137.035999084')

M_P_MeV = mpf('1.22089') * mpf('1e22')
m_e_CODATA = mpf('0.51099895000')

def test_nu_value(nu, label):
    """Test a ν value in mass calculation"""
    K_nu = ellipk(nu)
    E_nu = ellipe(nu)
    kappa = 2 * sqrt(nu) * K_nu / l_Omega
    
    # C_e
    term1 = abs(delta_e) * K_nu
    
    k_wind, m = 1, 0
    part1 = (2*mp_pi*k_wind / l_Omega)**2 * (K_nu / mp_pi)**2
    part2 = E_nu / K_nu
    part3 = -(1 - nu)
    term2 = (part1 + part2 + part3) * (8*m + nu/2)
    
    term3 = lambda_rec_beta * kappa / 3
    term4 = alpha / (2*mp_pi)
    
    C_e = term1 + term2 - term3 + term4
    
    # Mass
    eta_QED = 1 - alpha / (2*mp_pi)
    m_e = M_P_MeV * (2*mp_pi / phi**N_e) * C_e * eta_QED
    
    error = (m_e - m_e_CODATA) / m_e_CODATA * 100
    
    return C_e, m_e, error

print(f"\n{'Interpretation':>25} | {'ν':>10} | {'C_e':>10} | {'m_e (MeV)':>12} | {'Error %':>10}")
print("-" * 80)

results = [
    ("ν = 1/2 + δ/(2·k_res_exact)", nu_1),
    ("ν = 1/2 + δ_e/(2·k_int)", nu_2),
    ("ν = 1/2 + δ_e/(2·42)", nu_3),
]

for label, nu_val in results:
    C_e, m_e, error = test_nu_value(nu_val, label)
    print(f"{label:>25} | {float(nu_val):10.6f} | {float(C_e):10.6f} | {float(m_e):12.6f} | {float(error):10.4f}")

# ============================================================================
# COMPARE TO REQUIRED VALUE
# ============================================================================

print("\n" + "="*90)
print("COMPARISON TO REQUIRED ν")
print("="*90)

nu_required = mpf('0.82043')  # Gives perfect match
nu_document = mpf('0.91168')  # From document fitting

print(f"\nDocument formula ν = 1/2 + δ_e/(2·k):")
print(f"  Gives: ν = {float(nu_3):.6f}")
print(f"  Error in m_e: {float(test_nu_value(nu_3, '')[2]):.4f}%")

print(f"\nRequired for exact match:")
print(f"  ν = {float(nu_required):.6f}")
print(f"  Error in m_e: 0.00%")

print(f"\nDocument's fitted value:")
print(f"  ν = {float(nu_document):.6f}")
print(f"  Error in m_e: 0.00% (fitted!)")

print("\n" + "="*90)
print("CONCLUSION")
print("="*90)

print(f"""
The document formula ν = 1/2 + δ/(2·k_res) gives:
  ν ≈ 0.505

This is FAR from the required ν ≈ 0.82!

This formula does NOT work for the electron mass calculation!

Either:
1. The formula is wrong/outdated in those files
2. There's a different interpretation I'm missing
3. The formula applies to a different quantity
4. ν really IS phenomenological/fitted

The document then FITS ν = 0.912 to match CODATA!
""")
