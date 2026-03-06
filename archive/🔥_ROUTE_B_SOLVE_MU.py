#!/usr/bin/env python3
"""
ROUTE-B SELF-CONSISTENCY: SOLVE FOR μ(111)

Route-B formula:
    m_e = E_P · (2π/φ^111) · C_e(μ)
    
where:
    C_e(μ) = G_e · C_lock(μ) · C_GY(μ) · C_mem
           = √(5/3) · (2μ) · [(μ+sinh μ)/(sinh μ(cosh μ+1))]^(1/2) · 1

Self-consistency requires:
    C_e(μ) = m_e / [M_P · (2π/φ^111) · η_QED]

Solve for μ!
"""

from mpmath import mp, mpf, sqrt, sin, sinh, cosh, pi as mp_pi, findroot, re
from mpmath import ellipk

mp.dps = 50

print("="*90)
print("ROUTE-B: SOLVE FOR μ FROM SELF-CONSISTENCY")
print("="*90)

# ============================================================================
# CONSTANTS
# ============================================================================

phi = (1 + sqrt(5)) / 2
N_e = 111
pi_111 = N_e * sin(mp_pi / N_e)

# CODATA
M_P_MeV = mpf('1.22089') * mpf('1e22')
m_e_CODATA = mpf('0.51099895000')
alpha = mpf('1') / mpf('137.035999084')
eta_QED = 1 - alpha / (2*mp_pi)

# Target C_e from CODATA
C_e_target = m_e_CODATA / (M_P_MeV * (2*pi_111 / phi**N_e) * eta_QED)

print(f"\nConstants:")
print(f"  φ = {float(phi):.10f}")
print(f"  N_e = {N_e}")
print(f"  π_111 = {float(pi_111):.10f}")
print(f"  M_P = {float(M_P_MeV):.5e} MeV")
print(f"  m_e = {float(m_e_CODATA):.11f} MeV")
print(f"  η_QED = {float(eta_QED):.10f}")

print(f"\nTarget:")
print(f"  C_e^(CODATA) = {float(C_e_target):.12f}")

# ============================================================================
# ROUTE-B FORMULA
# ============================================================================

print("\n" + "="*90)
print("ROUTE-B FORMULA")
print("="*90)

# Group factor from SU(5)
G_e = sqrt(mpf('5')/mpf('3'))

print(f"\nGroup factor:")
print(f"  G_e = √(5/3) = {float(G_e):.10f}")

def C_e_RouteB(mu):
    """Route-B structural coefficient"""
    # C_lock
    C_lock = 2 * mu
    
    # C_GY (Gel'fand-Yaglom determinant)
    numerator = mu + sinh(mu)
    denominator = sinh(mu) * (cosh(mu) + 1)
    C_GY = sqrt(numerator / denominator)
    
    # C_mem
    C_mem = 1  # Phase-only sector
    
    # Total
    C_e = G_e * C_lock * C_GY * C_mem
    
    return C_e, C_lock, C_GY, C_mem

# ============================================================================
# TEST SOME μ VALUES
# ============================================================================

print("\n" + "="*90)
print("TESTING DIFFERENT μ VALUES")
print("="*90)

print(f"\n{'μ':>10} | {'C_lock':>10} | {'C_GY':>10} | {'C_e':>10} | {'Target':>10} | {'Diff':>10}")
print("-" * 75)

test_mu_values = [0.01, 0.02, 0.028, 0.03, 0.05, 0.1, 0.5, 1.0, 1.5, 2.0]

for mu_val in test_mu_values:
    mu = mpf(str(mu_val))
    C_e, C_lock, C_GY, C_mem = C_e_RouteB(mu)
    diff = C_e - C_e_target
    
    print(f"{mu_val:10.3f} | {float(C_lock):10.5f} | {float(C_GY):10.5f} | {float(C_e):10.5f} | {float(C_e_target):10.5f} | {float(diff):+10.5f}")

# ============================================================================
# SOLVE FOR μ
# ============================================================================

print("\n" + "="*90)
print("SOLVING: C_e(μ) = C_e^(CODATA)")
print("="*90)

def constraint_RouteB(mu):
    """Returns: C_e(μ) - C_e^(CODATA)"""
    C_e, _, _, _ = C_e_RouteB(mu)
    return C_e - C_e_target

print(f"\nSearching for μ where C_e(μ) = {float(C_e_target):.10f}...")

try:
    # Solve numerically - search between 0.1 and 0.5
    mu_solution_raw = findroot(constraint_RouteB, (0.4, 0.45))  # Bracketed search
    mu_solution = re(mu_solution_raw)
    
    C_e_calc, C_lock_calc, C_GY_calc, C_mem_calc = C_e_RouteB(mu_solution)
    
    print(f"\n🎯 SOLUTION FOUND!")
    print(f"\nμ(111) from Route-B self-consistency:")
    print(f"  μ = {mu_solution}")
    print(f"    = {float(mu_solution):.15f}")
    
    print(f"\nComponents:")
    print(f"  G_e = {float(G_e):.10f}")
    print(f"  C_lock = 2μ = {float(C_lock_calc):.10f}")
    print(f"  C_GY = {float(C_GY_calc):.10f}")
    print(f"  C_mem = {float(C_mem_calc):.10f}")
    print(f"  C_e = {float(C_e_calc):.15f}")
    
    print(f"\nVerification:")
    print(f"  C_e(μ) = {float(C_e_calc):.15f}")
    print(f"  Target = {float(C_e_target):.15f}")
    print(f"  Match:   {float(abs(C_e_calc - C_e_target)):.3e}")
    
    # Calculate mass
    m_e_RouteB = M_P_MeV * (2*pi_111 / phi**N_e) * C_e_calc * eta_QED
    error = (m_e_RouteB - m_e_CODATA) / m_e_CODATA * 100
    
    print(f"\nElectron mass:")
    print(f"  m_e (Route-B) = {float(m_e_RouteB):.11f} MeV")
    print(f"  m_e (CODATA)  = {float(m_e_CODATA):.11f} MeV")
    print(f"  Error         = {float(error):.3e}%")
    
except Exception as ex:
    print(f"\n✗ Could not solve: {ex}")

# ============================================================================
# COMPARE TO ROUTE-A (CLOSURE EQUATION)
# ============================================================================

print("\n" + "="*90)
print("COMPARISON TO ROUTE-A")
print("="*90)

# From Route-A
nu_RouteA = mpf('0.82054')
K_nu = ellipk(nu_RouteA)
l_Omega = 374.503

# Closure equation
mu_from_closure = 4 * K_nu / l_Omega

print(f"\nRoute-A results:")
print(f"  ν = {float(nu_RouteA):.8f}")
print(f"  K(ν) = {float(K_nu):.8f}")
print(f"  l_Ω = {float(l_Omega):.3f}")

print(f"\nFrom closure equation 4K(ν) = μ·l_Ω:")
print(f"  μ_closure = 4K(ν)/l_Ω")
print(f"            = {float(mu_from_closure):.10f}")

if 'mu_solution' in locals():
    print(f"\nRoute-B self-consistency:")
    print(f"  μ_self-consistent = {float(mu_solution):.10f}")
    
    ratio = mu_solution / mu_from_closure
    print(f"\nRatio μ_RouteB / μ_closure = {float(ratio):.6f}")
    
    if abs(ratio - 1) < 0.01:
        print(f"\n✅ MATCH! Routes are consistent!")
    else:
        print(f"\n⚠️ DIFFERENT! μ from Route-B ≠ μ from closure")
        print(f"\nThis means:")
        print(f"  1. Closure equation 4K(ν) = μ·l_Ω is incomplete, OR")
        print(f"  2. Route-A and Route-B use different conventions, OR")
        print(f"  3. μ in Route-B includes additional physics")

# ============================================================================
# WHAT THIS TELLS US
# ============================================================================

print("\n" + "="*90)
print("ANALYSIS")
print("="*90)

print(f"""
Route-B gives us a DIFFERENT way to determine μ:

Instead of:
  μ = 4K(ν)/l_Ω (from closure, gives μ ≈ 0.028)

We have:
  μ determined by: G_e · (2μ) · C_GY(μ) = C_e^(CODATA)

""")

if 'mu_solution' in locals():
    print(f"This gives: μ = {float(mu_solution):.6f}")
    print(f"\nIf they're different, then:")
    print(f"  - Route-A and Route-B are NOT simply related by 4K(ν) = μ·l_Ω")
    print(f"  - They represent different physics or different conventions")
    print(f"  - OR one of them has missing terms")
else:
    print(f"(Could not solve for μ)")

print(f"\n{'='*90}")
print("NEXT STEPS")
print("="*90)
print(f"""
1. Understand why μ_RouteB ≠ μ_closure (if they differ)
2. Search documents for Λ_m(X), V_Ω, ρ_vac
3. Try to derive μ from V_Ω directly (Route-B proper path)
4. Reconcile both routes completely
""")
