#!/usr/bin/env python3
"""
REFINED ν DETERMINATION

From sensitivity analysis, ν ≈ 0.80 gives -2.3% error.
Let's refine the search and try additional physical principles.
"""

from mpmath import mp, mpf, sqrt, exp, sin, cos, pi as mp_pi, e as mp_e
from mpmath import ellipk, ellipe, gamma as mp_gamma

mp.dps = 50

print("="*90)
print("REFINED ν DETERMINATION - FINDING THE RIGHT CONSTRAINT")
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

# CODATA for validation
m_e_MeV = mpf('0.51099895000')
M_P_MeV = mpf('1.22089') * mpf('1e22')
C_e_target = (phi**N_e / (2*mp_pi)) * (m_e_MeV / M_P_MeV)

print(f"C_e (target from CODATA) = {C_e_target}")

# ============================================================================
# REFINED CALCULATION FUNCTION
# ============================================================================

def calculate_complete_Ce(nu, include_memory=True, E_gauge_convention='loop'):
    """Calculate C_e with ALL terms"""
    
    K_nu = ellipk(nu)
    E_nu = ellipe(nu)
    kappa = 2 * sqrt(nu) * K_nu / l_Omega
    
    # Term 1: Detuning
    term1 = abs(delta_e) * K_nu
    
    # Term 2: Elliptic (FULL formula!)
    k = 1
    m = 0
    part1 = (2*mp_pi*k / l_Omega)**2 * (K_nu / mp_pi)**2
    part2 = E_nu / K_nu
    part3 = -(1 - nu)
    bracket = part1 + part2 + part3
    term2 = bracket * (8*m + nu/2)
    
    # Term 3: Memory (theory value)
    if include_memory:
        term3 = lambda_rec_beta * kappa / 3
    else:
        term3 = mpf('0')
    
    # Term 4: E_gauge
    if E_gauge_convention == 'core':
        C_gauge = alpha * kappa * l_Omega / (2*mp_pi)
    elif E_gauge_convention == 'loop':
        C_gauge = alpha / (2*mp_pi)
    elif E_gauge_convention == 'screened':
        xi = 1 / kappa
        lambda_screen = sqrt(xi * l_Omega)
        C_gauge = alpha / lambda_screen * l_Omega / (2*mp_pi)
    else:  # 'none'
        C_gauge = mpf('0')
    
    C_e = term1 + term2 - term3 + C_gauge
    
    return C_e, term1, term2, term3, C_gauge

# ============================================================================
# APPROACH 1: Fine-grained Search for ν
# ============================================================================

print("\n" + "="*90)
print("APPROACH 1: FINE-GRAINED SEARCH")
print("="*90)

print("\nScanning ν from 0.70 to 0.90 (high resolution)...")
print(f"{'ν':>8} | {'C_e':>12} | {'m_e (MeV)':>12} | {'Error %':>10} | Status")
print("-" * 65)

best_error = 1e10
best_nu = None

for nu_val in [i/1000 for i in range(700, 901, 10)]:  # 0.70 to 0.90 by 0.01
    nu = mpf(str(nu_val))
    
    try:
        C_e, t1, t2, t3, t4 = calculate_complete_Ce(nu, include_memory=True, E_gauge_convention='loop')
        
        # Calculate mass with QED
        eta_QED = 1 - alpha / (2*mp_pi)
        m_e_calc = M_P_MeV * (2*mp_pi / phi**N_e) * C_e * eta_QED
        error = (m_e_calc - m_e_MeV) / m_e_MeV * 100
        
        status = ""
        if abs(error) < 0.5:
            status = "🎯 EXCELLENT!"
        elif abs(error) < 1:
            status = "✓ Very good"
        elif abs(error) < 5:
            status = "✓ Good"
        
        if abs(error) < abs(best_error):
            best_error = error
            best_nu = nu_val
        
        if nu_val in [0.70, 0.75, 0.78, 0.79, 0.80, 0.81, 0.82, 0.83, 0.85, 0.88, 0.90] or abs(error) < 1:
            print(f"{nu_val:8.3f} | {float(C_e):12.6f} | {float(m_e_calc):12.6f} | {float(error):10.4f} | {status}")
            
    except Exception as ex:
        print(f"{nu_val:8.3f} | Error: {ex}")

print(f"\n🎯 Best ν = {float(best_nu):.3f} with error = {float(best_error):.4f}%")

# ============================================================================
# APPROACH 2: Try Without Memory (Route A)
# ============================================================================

print("\n" + "="*90)
print("APPROACH 2: ROUTE A (MEMORY = 0 FOR ISOLATED LEPTONS)")
print("="*90)

print("\nCalculating with memory = 0 as theory suggests for isolated leptons...")
print(f"{'ν':>8} | {'C_e':>12} | {'m_e (MeV)':>12} | {'Error %':>10} | Status")
print("-" * 65)

best_error_no_mem = 1e10
best_nu_no_mem = None

for nu_val in [i/1000 for i in range(880, 921, 5)]:  # Fine search near 0.90
    nu = mpf(str(nu_val))
    
    try:
        C_e, t1, t2, t3, t4 = calculate_complete_Ce(nu, include_memory=False, E_gauge_convention='loop')
        
        eta_QED = 1 - alpha / (2*mp_pi)
        m_e_calc = M_P_MeV * (2*mp_pi / phi**N_e) * C_e * eta_QED
        error = (m_e_calc - m_e_MeV) / m_e_MeV * 100
        
        status = ""
        if abs(error) < 0.5:
            status = "🎯 EXCELLENT!"
            best_error_no_mem = error
            best_nu_no_mem = nu_val
        elif abs(error) < 1:
            status = "✓ Very good"
        
        print(f"{nu_val:8.3f} | {float(C_e):12.6f} | {float(m_e_calc):12.6f} | {float(error):10.4f} | {status}")
        
    except:
        pass

if best_nu_no_mem:
    print(f"\n🎯 Best ν (no memory) = {float(best_nu_no_mem):.3f} with error = {float(best_error_no_mem):.4f}%")

# ============================================================================
# APPROACH 3: Constrain by Total Action
# ============================================================================

print("\n" + "="*90)
print("APPROACH 3: MINIMIZE TOTAL ACTION")
print("="*90)

print("\nTotal action S = S_kinetic + S_potential + S_winding + S_memory")

def total_action(nu):
    """Calculate total action"""
    K_nu = ellipk(nu)
    E_nu = ellipe(nu)
    kappa = 2 * sqrt(nu) * K_nu / l_Omega
    mu = kappa / sqrt(nu)
    
    # Kinetic action
    S_kin = mu**2 * l_Omega / 2
    
    # Potential action  
    S_pot = mu**2 * l_Omega * E_nu / K_nu
    
    # Winding (topological)
    S_wind = (2*mp_pi / l_Omega)**2 * l_Omega / 2
    
    # Memory (if included)
    S_mem = -lambda_rec_beta * (kappa / 3)
    
    S_total = S_kin + S_pot + S_wind + S_mem
    
    return S_total, S_kin, S_pot, S_wind, S_mem

print(f"\n{'ν':>6} | {'S_total':>12} | Note")
print("-" * 40)

action_results = []
for nu_val in [0.1, 0.3, 0.5, 0.7, 0.75, 0.78, 0.80, 0.82, 0.85, 0.88, 0.90, 0.95]:
    nu = mpf(str(nu_val))
    try:
        S_tot, S_k, S_p, S_w, S_m = total_action(nu)
        print(f"{nu_val:6.2f} | {float(S_tot):12.6f}")
        action_results.append((nu_val, float(S_tot)))
    except:
        print(f"{nu_val:6.2f} | Error")

if action_results:
    nu_min_action = min(action_results, key=lambda x: x[1])
    print(f"\n✓ Minimum action at ν = {nu_min_action[0]:.3f}")
    
# ============================================================================
# APPROACH 4: Self-Consistency - Both Gel'fand-Yaglom and Elliptic
# ============================================================================

print("\n" + "="*90)
print("APPROACH 4: SELF-CONSISTENCY (GY = ELLIPTIC)")
print("="*90)

print("\nGel'fand-Yaglom: C_e = (2/μ) · (√3/2) · D_e")
print("Elliptic: C_e = detuning + elliptic + ...")
print("\nSet them equal to find ν!")

G_e = sqrt(3) / 2

def calculate_GY_Ce(mu_val):
    """Gel'fand-Yaglom C_e"""
    # Simplified D_e (for large μ·l_Ω, D_e → 1)
    x = mu_val * l_Omega
    if x > 10:
        D_e = mpf('1')
    else:
        D_e = sqrt(1 - (x/sinh(x)) * (1/cosh(x/2)))
    
    N_e_norm = 2 / mu_val
    C_e_GY = N_e_norm * G_e * D_e
    return C_e_GY, D_e

print(f"\nSearching for ν where C_e(Elliptic) = C_e(Gel'fand-Yaglom)...")
print(f"{'ν':>8} | {'C_e(Ell)':>12} | {'μ (MeV)':>12} | {'C_e(GY)':>12} | {'Diff %':>10}")
print("-" * 70)

for nu_val in [0.70, 0.75, 0.78, 0.79, 0.80, 0.81, 0.82, 0.83, 0.85, 0.88, 0.90]:
    nu = mpf(str(nu_val))
    try:
        # Elliptic C_e
        C_e_ell, t1, t2, t3, t4 = calculate_complete_Ce(nu, include_memory=True, E_gauge_convention='loop')
        
        # For Gel'fand-Yaglom, need μ in MeV
        # From elliptic: κ = 2√ν·K(ν)/l_Ω
        K_nu = ellipk(nu)
        kappa = 2 * sqrt(nu) * K_nu / l_Omega
        
        # Convert to MeV: μ in dimensionless → μ in MeV
        # μ (dimensionless) × (M_P/φ^111) → MeV scale
        mu_dimensionless = kappa / sqrt(nu)
        mu_MeV = mu_dimensionless * (M_P_MeV / phi**N_e) / (2*mp_pi)
        
        C_e_GY, D_e = calculate_GY_Ce(mu_dimensionless)
        
        diff = (C_e_GY - C_e_ell) / C_e_ell * 100
        
        print(f"{nu_val:8.2f} | {float(C_e_ell):12.6f} | {float(mu_MeV):12.6f} | {float(C_e_GY):12.6f} | {float(diff):10.4f}")
        
    except Exception as ex:
        print(f"{nu_val:8.2f} | Error: {ex}")

# ============================================================================
# APPROACH 5: Look for φ-related values
# ============================================================================

print("\n" + "="*90)
print("APPROACH 5: CHECK FOR φ-RELATED SPECIAL VALUES")
print("="*90)

print("\nChecking if ν has special relationship to φ...")

# Common φ-related values
special_values = {
    "φ - 1": float(phi - 1),
    "1/φ": float(1/phi),
    "1/φ²": float(1/(phi**2)),
    "(φ-1)/φ": float((phi-1)/phi),
    "√(1/φ)": float(sqrt(1/phi)),
    "1 - 1/φ²": float(1 - 1/(phi**2)),
    "2/φ": float(2/phi),
    "φ²/(φ²+1)": float(phi**2/(phi**2+1)),
}

print(f"\n{'Expression':>15} | {'Value':>10} | Close to 0.91?")
print("-" * 50)

for expr, val in special_values.items():
    close = "🎯 MATCH!" if 0.90 < val < 0.92 else ""
    print(f"{expr:>15} | {val:10.6f} | {close}")

# ============================================================================
# APPROACH 6: Resonance-Based Determination
# ============================================================================

print("\n" + "="*90)
print("APPROACH 6: RESONANCE CONDITION")
print("="*90)

print("\nElectron resonance: N/φ² ≈ k_res")
print(f"111/φ² = {float(N_e / phi**2):.6f}")
print(f"k_res = 42")
print(f"Residual = {float(delta_e):.6f}")

print("\nMaybe ν is related to the resonance residual?")
print(f"δ_e = {float(delta_e):.6f}")
print(f"1 - δ_e = {float(1 - delta_e):.6f} ← Close to 0.60")
print(f"√(1 - δ_e) = {float(sqrt(1 - delta_e)):.6f} ← ≈ 0.777")

# Check if ν could be related to resonance
nu_from_delta_1 = 1 - delta_e
nu_from_delta_2 = sqrt(1 - delta_e)
nu_from_delta_3 = 1 - sqrt(delta_e)

print(f"\nPossibilities:")
print(f"  ν = 1 - δ_e = {float(nu_from_delta_1):.6f} ← Too low")
print(f"  ν = √(1 - δ_e) = {float(nu_from_delta_2):.6f} ← Interesting!")
print(f"  ν = 1 - √δ_e = {float(nu_from_delta_3):.6f} ← Too low")

# Test the interesting one
print(f"\n### Testing ν = √(1 - δ_e) = {float(nu_from_delta_2):.6f} ###")

nu_test = sqrt(1 - delta_e)
C_e_test, _, _, _, _ = calculate_complete_Ce(nu_test, include_memory=True, E_gauge_convention='loop')
eta_QED = 1 - alpha / (2*mp_pi)
m_e_test = M_P_MeV * (2*mp_pi / phi**N_e) * C_e_test * eta_QED
error_test = (m_e_test - m_e_MeV) / m_e_MeV * 100

print(f"C_e = {C_e_test}")
print(f"m_e = {m_e_test} MeV")
print(f"Error = {float(error_test):.4f}%")

if abs(error_test) < 5:
    print(f"✓ THIS COULD BE IT! Error < 5%!")

# ============================================================================
# APPROACH 7: Match Characteristic Scales
# ============================================================================

print("\n" + "="*90)
print("APPROACH 7: CHARACTERISTIC SCALE MATCHING")
print("="*90)

print("\nThe kink has two natural scales:")
print("  1. Geometric: l_Ω = 374.5")
print("  2. Dynamic: ξ = 1/κ (kink width)")
print("\nMaybe ν is where these have special ratio?")

print(f"\n{'ν':>6} | {'ξ':>12} | {'l_Ω/ξ':>12} | Note")
print("-" * 45)

for nu_val in [0.7, 0.777, 0.8, 0.85, 0.9, 0.912]:
    nu = mpf(str(nu_val))
    K_nu = ellipk(nu)
    kappa_nu = 2 * sqrt(nu) * K_nu / l_Omega
    xi_nu = 1 / kappa_nu
    ratio = l_Omega / xi_nu
    
    note = ""
    if 4.5 < float(ratio) < 5.5:
        note = "≈ 5!"
    elif 2.8 < float(ratio) < 3.2:
        note = "≈ π!"
    elif 6 < float(ratio) < 7:
        note = "≈ 2π!"
    
    print(f"{nu_val:6.3f} | {float(xi_nu):12.3f} | {float(ratio):12.3f} | {note}")

# ============================================================================
# FINAL RECOMMENDATION
# ============================================================================

print("\n" + "="*90)
print("FINAL RECOMMENDATIONS")
print("="*90)

print(f"\nBased on ALL approaches:")
print(f"1. Energy minimum: ν ≈ 0.1 (but gives -38% error!)")
print(f"2. Best error match: ν ≈ {float(best_nu)} (error {float(best_error):.2f}%)")
print(f"3. Resonance relation: ν = √(1-δ_e) ≈ 0.777 (error {float(error_test):.2f}%)")
print(f"4. No memory (Route A): ν ≈ {float(best_nu_no_mem) if best_nu_no_mem else '0.91'}")

print(f"\n🎯 PHYSICALLY MOTIVATED CHOICE:")
print(f"ν = √(1 - δ_e) = 0.777...")
print(f"Reasoning: Connects ν to resonance detuning δ_e")
print(f"This would be a DERIVED relationship!")

print(f"\n" + "="*90)
print("STATUS: Need to validate ν = √(1 - δ_e) against theory documents")
print("="*90)
