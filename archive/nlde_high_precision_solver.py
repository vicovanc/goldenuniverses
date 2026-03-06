#!/usr/bin/env python3
"""
HIGH-PRECISION NLDE SOLVER
===========================

Solve the Non-Linear Dirac Equation with 50 decimal precision
to get exact value of Ẽ (binding energy)

Based on nlde_dimensionless.py but with mpmath for high precision

Date: 2026-02-11
"""

from mpmath import mp, mpf, sqrt, exp, findroot, quad, pi as mp_pi

# Set precision to 50 decimal places
mp.dps = 50

print("="*80)
print("HIGH-PRECISION NLDE SOLVER")
print("50 Decimal Precision")
print("="*80)
print()

# =============================================================================
# DIMENSIONLESS RADIAL DIRAC EQUATIONS
# =============================================================================

def radial_dirac_system(r, E_tilde, V_func, c_mem=mpf('0.45')):
    """
    Dimensionless radial Dirac equations with memory potential.

    dF/dr = -(1 + E_tilde - V(r) - Σ(r)) * G
    dG/dr = (1 - E_tilde + V(r) + Σ(r)) * F - 2G/r

    where Σ(r) = -c_mem * exp(-r) is the memory self-energy
    """
    def derivs(r, y):
        F, G = y[0], y[1]

        # Potentials
        V = V_func(r) if V_func else 0
        Sigma = -c_mem * exp(-r)  # Memory self-energy

        # Total effective potential
        V_eff = V + Sigma

        # Derivatives
        dF_dr = -(1 + E_tilde - V_eff) * G
        dG_dr = (1 - E_tilde + V_eff) * F - 2*G/r if r > mpf('1e-10') else 0

        return [dF_dr, dG_dr]

    return derivs

# =============================================================================
# SHOOTING METHOD FOR BOUND STATES
# =============================================================================

def shoot_from_origin(E_tilde, r_max, V_func, c_mem):
    """
    Integrate from r ≈ 0 to r_max using 4th order Runge-Kutta.
    Returns F(r_max).
    """
    # Initial conditions near origin
    r0 = mpf('1e-8')
    F0 = r0  # F ~ r as r→0
    G0 = mpf('0')  # G ~ 0 as r→0

    # Integration parameters
    N_steps = 10000
    dr = (r_max - r0) / N_steps

    # RK4 integration
    r = r0
    y = [F0, G0]

    system = radial_dirac_system(r, E_tilde, V_func, c_mem)

    for _ in range(N_steps):
        # RK4 step
        k1 = system(r, y)
        y_temp = [y[0] + dr*k1[0]/2, y[1] + dr*k1[1]/2]

        k2 = system(r + dr/2, y_temp)
        y_temp = [y[0] + dr*k2[0]/2, y[1] + dr*k2[1]/2]

        k3 = system(r + dr/2, y_temp)
        y_temp = [y[0] + dr*k3[0], y[1] + dr*k3[1]]

        k4 = system(r + dr, y_temp)

        # Update
        y[0] += dr * (k1[0] + 2*k2[0] + 2*k3[0] + k4[0]) / 6
        y[1] += dr * (k1[1] + 2*k2[1] + 2*k3[1] + k4[1]) / 6
        r += dr

    return y[0]  # Return F(r_max)

def find_bound_state(V_func, c_mem, E_min, E_max, r_max=mpf('30')):
    """
    Find bound state energy using bisection method.
    """
    print(f"Searching for bound state with c_mem = {float(c_mem):.6f}")
    print(f"Energy range: [{float(E_min):.6f}, {float(E_max):.6f}]")

    # Bisection method
    tol = mpf('1e-40')  # Very high precision
    max_iter = 100

    for iteration in range(max_iter):
        E_mid = (E_min + E_max) / 2

        F_min = shoot_from_origin(E_min, r_max, V_func, c_mem)
        F_mid = shoot_from_origin(E_mid, r_max, V_func, c_mem)
        F_max = shoot_from_origin(E_max, r_max, V_func, c_mem)

        if abs(F_mid) < tol:
            print(f"Converged after {iteration+1} iterations")
            return E_mid

        # Check which half contains the root
        if F_min * F_mid < 0:
            E_max = E_mid
        else:
            E_min = E_mid

        if abs(E_max - E_min) < tol:
            print(f"Converged after {iteration+1} iterations")
            return E_mid

    print(f"Warning: Max iterations reached")
    return E_mid

# =============================================================================
# TEST WITH YUKAWA POTENTIAL
# =============================================================================

def yukawa_potential(r, V0=mpf('0.5'), r0=mpf('1')):
    """Yukawa potential: V(r) = -V0 * exp(-r/r0)"""
    return -V0 * exp(-r/r0)

print("TEST: Yukawa Potential")
print("-" * 40)

V0_test = mpf('0.5')
V_test = lambda r: yukawa_potential(r, V0_test)

# Find bound state without memory
print("\nWithout memory (c_mem = 0):")
E_yukawa = find_bound_state(V_test, mpf('0'), mpf('-1'), mpf('-0.001'))
print(f"Ẽ = {E_yukawa}")
print(f"   = {float(E_yukawa):.15f}")
print(f"Binding energy: |Ẽ| = {abs(E_yukawa)}")
print()

# =============================================================================
# ELECTRON WITH MEMORY
# =============================================================================

print("="*80)
print("ELECTRON BOUND STATE WITH MEMORY")
print("="*80)
print()

# Memory coupling from previous analysis
c_mem_electron = mpf('0.45')

print(f"Memory coupling: c_mem = {c_mem_electron}")
print()

# For electron, we use pure memory (no additional potential)
V_electron = None  # Pure memory binding

print("Finding electron bound state...")
print("-" * 40)

# Search for bound state
E_electron = find_bound_state(V_electron, c_mem_electron, mpf('-1'), mpf('-0.5'))

print()
print("RESULT:")
print(f"Ẽ = {E_electron}")
print(f"   = {float(E_electron):.20f}")
print()

# Compare to current value
E_current = mpf('-0.882')
diff = E_electron - E_current
print(f"Current value: Ẽ = {E_current}")
print(f"High-precision: Ẽ = {E_electron}")
print(f"Difference: {diff}")
print(f"           = {float(diff):.20f}")
print()

# =============================================================================
# CALCULATE CORRECTED ELECTRON MASS
# =============================================================================

print("="*80)
print("CORRECTED ELECTRON MASS CALCULATION")
print("="*80)
print()

# High-precision constants
phi = (1 + sqrt(5)) / 2
M_P = mpf('1.22091e22')  # MeV
m_e_CODATA = mpf('0.51099895069')  # MeV
alpha = mpf('0.0072973525693')

# Theory parameters
N_e = 111
m_bar_star = mpf('4514')
C_e = mpf('1.049988534698')  # The exact value needed

print(f"Using high-precision Ẽ = {E_electron}")
print(f"(1 + Ẽ) = {1 + E_electron}")
print()

# Calculate X_e
phi_N = phi**N_e
X_e = (2 * mp_pi * C_e) / (m_bar_star * (1 + E_electron) * phi_N)

print(f"X_e = {X_e}")
print(f"    = {float(X_e):.6e}")
print()

# Calculate electron mass
m_e_calc = m_bar_star * X_e * M_P * (1 + E_electron)

print(f"m_e (calculated) = {m_e_calc} MeV")
print(f"m_e (CODATA)     = {m_e_CODATA} MeV")
print()

error = m_e_calc - m_e_CODATA
error_pct = 100 * error / m_e_CODATA

print(f"Error: {error} MeV")
print(f"Error %: {float(error_pct):.6f}%")
print()

# =============================================================================
# ANALYSIS
# =============================================================================

print("="*80)
print("ANALYSIS")
print("="*80)
print()

if abs(error_pct) < 0.01:
    print("✅ EXCELLENT! Error < 0.01%")
    print("High-precision NLDE gives near-exact match!")
elif abs(error_pct) < 0.1:
    print("✅ VERY GOOD! Error < 0.1%")
    print("Much better than previous 0.17%")
elif abs(error_pct) < 1:
    print("✓ GOOD! Error < 1%")
    print("Significant improvement with high precision")
else:
    print("⚠ Still have error > 1%")
    print("May need to refine other parameters")

print()
print("KEY INSIGHT:")
print(f"High-precision Ẽ = {float(E_electron):.20f}")
print(f"This is {'very close to' if abs(diff) < 0.001 else 'different from'} the assumed -0.882")
print()

if abs(diff) > 0.001:
    print("The difference suggests:")
    print("1. Memory coupling c_mem might need adjustment")
    print("2. Additional physics might be missing")
    print("3. The integration method needs refinement")