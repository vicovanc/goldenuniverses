#!/usr/bin/env python3
"""
PROPER VARIATIONAL PRINCIPLE FOR ν

Document line 4159 states:
    ∂C_e/∂ν = 0  (determines ν uniquely!)

Let me implement this with ALL terms and solve numerically.

C_e(ν) = |δ_e|·K(ν) + η_μ(ν)·(ν/2) - (λ_rec/β)·κ(ν)/3 + α/(2π)

where:
  η_μ(ν) = (2K(ν)/l_Ω)² + E(ν)/K(ν) - (1-ν)  [FULL FORMULA!]
  κ(ν) = 2√ν·K(ν)/l_Ω

Solve: dC_e/dν = 0
"""

from mpmath import mp, mpf, sqrt, exp, sin, pi as mp_pi
from mpmath import ellipk, ellipe, diff

mp.dps = 50

print("="*90)
print("VARIATIONAL PRINCIPLE: ∂C_e/∂ν = 0")
print("="*90)

# ============================================================================
# CONSTANTS
# ============================================================================

phi = (1 + sqrt(5)) / 2
N_e = 111
delta_e = N_e / (phi**2) - 42
p, q = -41, 70
l_Omega = 2 * mp_pi * sqrt(p**2 + (q/phi)**2)
lambda_rec_beta = exp(phi) / (mp_pi ** 2)
alpha = mpf('1') / mpf('137.035999084')

print(f"\nConstants:")
print(f"  δ_e = {float(delta_e):.8f}")
print(f"  l_Ω = {float(l_Omega):.3f}")
print(f"  λ_rec/β = {float(lambda_rec_beta):.6f}")

# ============================================================================
# DEFINE C_e WITH ALL TERMS
# ============================================================================

def C_e_complete(nu):
    """Complete C_e formula with ALL terms"""
    K_nu = ellipk(nu)
    E_nu = ellipe(nu)
    
    # Term 1: Detuning
    term1 = abs(delta_e) * K_nu
    
    # Term 2: Elliptic (FULL formula from line 4020!)
    k, m = 1, 0
    part1 = (2*mp_pi*k / l_Omega)**2 * (K_nu / mp_pi)**2
    part2 = E_nu / K_nu
    part3 = -(1 - nu)
    eta_mu = part1 + part2 + part3
    term2 = eta_mu * (8*m + nu/2)
    
    # Term 3: Memory
    kappa = 2 * sqrt(nu) * K_nu / l_Omega
    term3 = lambda_rec_beta * kappa / 3
    
    # Term 4: E_gauge  
    term4 = alpha / (2*mp_pi)
    
    C_e = term1 + term2 - term3 + term4
    
    return C_e

# ============================================================================
# CALCULATE dC_e/dν
# ============================================================================

print("\n" + "="*90)
print("COMPUTING dC_e/dν")
print("="*90)

# Use mpmath's automatic differentiation
dCe_dnu = lambda nu: diff(C_e_complete, nu)

print(f"\n{'ν':>8} | {'C_e':>12} | {'dC_e/dν':>15}")
print("-" * 45)

for nu_val in [0.5, 0.6, 0.7, 0.75, 0.80, 0.82, 0.85, 0.88, 0.90, 0.92, 0.95]:
    nu = mpf(str(nu_val))
    C_e = C_e_complete(nu)
    dCe = dCe_dnu(nu)
    print(f"{nu_val:8.2f} | {float(C_e):12.8f} | {float(dCe):15.8f}")

# ============================================================================
# FIND ν WHERE dC_e/dν = 0
# ============================================================================

print("\n" + "="*90)
print("FINDING ν WHERE dC_e/dν = 0")
print("="*90)

print("\nSearching for zero crossing...")

# Check for sign changes
test_points = [mpf(str(v)) for v in [0.5, 0.6, 0.7, 0.8, 0.85, 0.9, 0.95, 0.99]]
derivatives = [dCe_dnu(nu) for nu in test_points]

print(f"\nSign changes:")
for i in range(len(test_points)-1):
    if derivatives[i] * derivatives[i+1] < 0:
        print(f"  Between ν = {float(test_points[i]):.2f} and {float(test_points[i+1]):.2f}")
        print(f"    dC_e/dν changes from {float(derivatives[i]):.6f} to {float(derivatives[i+1]):.6f}")

if all(d > 0 for d in derivatives):
    print("\n⚠️ dC_e/dν > 0 everywhere → C_e is INCREASING")
    print("   No minimum! Variational principle has no solution!")
elif all(d < 0 for d in derivatives):
    print("\n⚠️ dC_e/dν < 0 everywhere → C_e is DECREASING")
    print("   No minimum! Variational principle has no solution!")
else:
    print("\n✓ Sign change found! Using Newton's method to find zero...")
    
    # Use mpmath's findroot to solve dC_e/dν = 0
    from mpmath import findroot
    
    try:
        nu_stationary = findroot(dCe_dnu, 0.7)
        C_e_stat = C_e_complete(nu_stationary)
        
        print(f"\n🎯 SOLUTION FOUND!")
        print(f"ν (stationary) = {nu_stationary}")
        print(f"             = {float(nu_stationary):.10f}")
        print(f"C_e(ν) = {float(C_e_stat):.10f}")
        print(f"dC_e/dν = {float(dCe_dnu(nu_stationary)):.10e}")
        
        # Calculate mass
        M_P_MeV = mpf('1.22089') * mpf('1e22')
        eta_QED = 1 - alpha / (2*mp_pi)
        m_e = M_P_MeV * (2*mp_pi / phi**N_e) * C_e_stat * eta_QED
        
        m_e_CODATA = mpf('0.51099895000')
        error = (m_e - m_e_CODATA) / m_e_CODATA * 100
        
        print(f"\nm_e (calculated) = {float(m_e):.8f} MeV")
        print(f"m_e (CODATA)     = {float(m_e_CODATA):.8f} MeV")
        print(f"Error            = {float(error):.6f}%")
        
    except Exception as ex:
        print(f"\n✗ Could not find zero: {ex}")

# ============================================================================
# ANALYSIS
# ============================================================================

print("\n" + "="*90)
print("ANALYSIS")
print("="*90)

print("""
Document Line 4159 claims:
    "∂C_e/∂ν = 0 gives a unique ν = ν*"

But from the calculation above:
""")

if all(d > 0 for d in derivatives):
    print("""
✗ C_e(ν) is MONOTONICALLY INCREASING!
  
This means:
- dC_e/dν > 0 everywhere
- No stationary point exists
- Variational principle has NO solution

Conclusion: The document's claim in line 4159 is WRONG!

The variational principle does NOT determine ν uniquely!

This is why the document then FITS ν = 0.912 on line 4771!
""")
else:
    print("""
✓ Stationary point exists!
  
The variational principle DOES work if we include all terms!
""")

print("\n" + "="*90)
print("FINAL CONCLUSION")
print("="*90)

print("""
Based on the complete calculation with ALL terms:

ν is determined by the variational principle ∂C_e/∂ν = 0

IF this has a solution, then ν is DERIVED from first principles!
IF this has NO solution (C_e monotonic), then ν is phenomenological!
""")
