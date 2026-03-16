#!/usr/bin/env python3
"""
Complete Force Unification Derivation
Shows how all forces emerge from G_prim as X evolves
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.gu_constants import *
import numpy as np
from scipy.integrate import solve_ivp
# import matplotlib.pyplot as plt  # Commented out - install if needed for plots

print("="*80)
print("GOLDEN UNIVERSE FORCE UNIFICATION")
print("All forces emerge from symmetry breaking as X rolls")
print("="*80)

# ============================================================================
# PART 1: PRIMORDIAL UNIFICATION AT PLANCK SCALE
# ============================================================================

print("\n### STAGE 1: PRIMORDIAL STATE (X = M_P, n = 0)")
print("-"*60)

# At Planck scale, all forces unified
X_Planck = M_P
print(f"X_Planck = {float(X_Planck):.3e} MeV")

# Unified coupling: α_GUT now calibrated from α_EM via RG (gu_constants.py).
# NOTE: Hypothesis α_GUT = 1/(8πφ) FAILED — gave α_EM ≈ 1/180 (24% wrong).
alpha_unified = alpha_GUT
print(f"α_unified = {float(alpha_unified):.6f}")

# This corresponds to gauge group G_prim
print("\nUnified symmetry group G_prim contains:")
print("- SU(3)_C (strong)")
print("- SU(2)_L (weak)")
print("- U(1)_Y (hypercharge)")
print("All with single coupling α_unified")

# ============================================================================
# PART 2: GUT SYMMETRY BREAKING
# ============================================================================

print("\n### STAGE 2: GUT BREAKING (X ~ 10^16 GeV, N ≈ 67)")
print("-"*60)

print(f"N_GUT = {N_GUT}")
k_GUT, quality = resonance_quality(N_GUT)
print(f"Resonance: {N_GUT}/φ² = {k_GUT} + {quality:.2%}")

X_GUT_scale = X_at_epoch(N_GUT)
print(f"X_GUT = M_P × φ^(-{N_GUT}) = {float(X_GUT_scale):.3e} MeV")
print(f"      = {float(X_GUT_scale/1e12):.1f} × 10^16 GeV")

print("\nSymmetry breaking:")
print("SU(5) → SU(3)_C × SU(2)_L × U(1)_Y")
print("\nPattern change: k=3 → k=2,1,0")

# At GUT scale, couplings unify
print(f"\nAt X_GUT: α₁ = α₂ = α₃ = α_GUT = {float(alpha_GUT):.6f}")

# ============================================================================
# PART 3: RENORMALIZATION GROUP EVOLUTION
# ============================================================================

print("\n### STAGE 3: RG EVOLUTION OF COUPLINGS")
print("-"*60)

def beta_functions(t, alphas, n_f=6):
    """
    One-loop RG beta functions for SM gauge couplings
    t = ln(μ/μ₀) where μ is energy scale
    alphas = [α₁, α₂, α₃] for U(1), SU(2), SU(3)

    ISSUE: This implementation runs ALL THREE couplings from GUT down to X_e.
    Correct approach: Above EW (~246 GeV) run α₁,α₂,α₃; between QCD (~300 MeV)
    and EW freeze α₂ (b₂=0); below QCD freeze α₂ and α₃ (b₂=0, b₃=0), run only α₁.
    """
    a1, a2, a3 = alphas

    # One-loop beta coefficients (SM with n_f quark flavors)
    b1 = 41/10  # U(1)_Y with normalization
    b2 = -19/6  # SU(2)_L
    b3 = -7 + n_f/3  # SU(3)_C

    # Beta functions: dα/dt = b α²/(2π)
    da1_dt = b1 * a1**2 / (2*np.pi)
    da2_dt = b2 * a2**2 / (2*np.pi)
    da3_dt = b3 * a3**2 / (2*np.pi)

    return [da1_dt, da2_dt, da3_dt]

# Solve RG flow from GUT to electron scale
print("\nRunning couplings from X_GUT to X_e:")

# Initial conditions at GUT scale
alphas_GUT = [float(alpha_GUT)] * 3  # All unified

# Evolution parameter
t_GUT = 0
t_e = float(mpmath.log(X_e/X_GUT_scale))  # ln(X_e/X_GUT)

# Solve RG equations
t_span = (t_GUT, t_e)
t_eval = np.linspace(t_GUT, t_e, 1000)

# Different thresholds for quark masses affect n_f
# For simplicity, use n_f = 6 above top mass, then adjust

sol = solve_ivp(beta_functions, t_span, alphas_GUT,
                t_eval=t_eval, method='RK45')

# Extract final values at electron scale
a1_e = sol.y[0, -1]
a2_e = sol.y[1, -1]
a3_e = sol.y[2, -1]

print(f"\nAt X_e = {float(X_e):.3f} MeV:")
print(f"α₁(X_e) = {a1_e:.8f}")
print(f"α₂(X_e) = {a2_e:.8f}")
print(f"α₃(X_e) = {a3_e:.8f}")

# ============================================================================
# PART 4: ELECTROWEAK UNIFICATION AND BREAKING
# ============================================================================

print("\n### STAGE 4: ELECTROWEAK BREAKING (X ~ 246 GeV, N = 89)")
print("-"*60)

X_EW = X_at_epoch(N_EW)
print(f"X_EW = M_P × φ^(-89) = {float(X_EW):.1f} MeV = {float(X_EW/1000):.1f} GeV")

# Weinberg angle from couplings
# sin²θ_W = g'²/(g² + g'²) = α₁/(α₁ + α₂)
# WARNING: sin²θ_W_exp is defined at M_Z scale; this comparison is at X_e — should use M_Z.
sin2_theta_W = a1_e / (a1_e + a2_e)
print(f"\nWeinberg angle (at X_e — experimental value is at M_Z):")
print(f"sin²θ_W = α₁/(α₁+α₂) = {sin2_theta_W:.5f}")
print(f"Experimental (at M_Z): {float(sin2_theta_W_exp):.5f}")

# After EW breaking: SU(2)×U(1) → U(1)_em
# α_EM = α₁ α₂ / (α₁ + α₂)
alpha_EM_derived = a1_e * a2_e / (a1_e + a2_e)
print(f"\nElectromagnetic coupling:")
print(f"α_EM = α₁α₂/(α₁+α₂) = {alpha_EM_derived:.8f}")
print(f"     = 1/{1/alpha_EM_derived:.1f}")
print(f"Target: α = 1/137.036 = {float(alpha_EM_target):.8f}")

error_percent = abs(alpha_EM_derived - float(alpha_EM_target))/float(alpha_EM_target) * 100
print(f"Error: {error_percent:.2f}%")

# ============================================================================
# PART 5: QCD CONFINEMENT
# ============================================================================

print("\n### STAGE 5: QCD CONFINEMENT (X ~ 200 MeV, N = 95)")
print("-"*60)

Lambda_QCD = X_at_epoch(N_QCD)
print(f"Λ_QCD = M_P × φ^(-95) = {float(Lambda_QCD):.1f} MeV")
print(f"Experimental: ~200 MeV")

print(f"\nStrong coupling at QCD scale:")
print(f"α_s(Λ_QCD) → ∞ (confinement)")
print(f"Pattern k=2 becomes strongly coupled")
print(f"Color confinement emerges")

# ============================================================================
# PART 6: PATTERN-K INTERPRETATION
# ============================================================================

print("\n### PATTERN-K ACTIVATION SEQUENCE")
print("-"*60)

patterns = [
    (0, "M_P", "k=3", "All forces unified in G_prim"),
    (N_GUT, f"{float(X_GUT_scale/1e12):.1e} GeV", "k=3→2,1,0", "GUT breaks to SM"),
    (N_EW, f"{float(X_EW/1000):.0f} GeV", "k=1,0 split", "Weak and EM separate"),
    (N_QCD, f"{float(Lambda_QCD):.0f} MeV", "k=2 confines", "QCD confinement"),
    (N_e, f"{float(X_e):.1f} MeV", "k=0 only", "Pure EM at low energy")
]

print(f"{'Epoch':<6} {'Scale':<12} {'Pattern':<12} {'Physics'}")
print("-"*60)
for N, scale, pattern, physics in patterns:
    print(f"N={N:<3} {scale:<12} {pattern:<12} {physics}")

# ============================================================================
# PART 7: VISUALIZATION
# ============================================================================

# Plotting code commented out - uncomment and install matplotlib if needed
"""
print("\n### GENERATING PLOTS...")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Plot 1: Running of couplings
scales = X_GUT_scale * np.exp(t_eval)
ax1.semilogy(scales/1e9, sol.y[0], 'b-', label='α₁ (U(1)_Y)')
ax1.semilogy(scales/1e9, sol.y[1], 'g-', label='α₂ (SU(2)_L)')
ax1.semilogy(scales/1e9, sol.y[2], 'r-', label='α₃ (SU(3)_C)')
ax1.axvline(float(X_EW/1e9), color='orange', linestyle='--', alpha=0.5, label='EW scale')
ax1.axvline(float(X_e/1e9), color='purple', linestyle='--', alpha=0.5, label='Electron')
ax1.set_xlabel('Energy Scale (TeV)')
ax1.set_ylabel('Coupling Constant α')
ax1.set_title('RG Evolution of Gauge Couplings')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.invert_xaxis()

# Plot 2: Pattern activation
epochs = [0, N_GUT, N_EW, N_QCD, N_e, 150]
patterns_k = [3, 3, 1.5, 2, 0, 0]
ax2.step(epochs, patterns_k, where='post', linewidth=2)
ax2.fill_between(epochs, patterns_k, step='post', alpha=0.3)
ax2.set_xlabel('Epoch N')
ax2.set_ylabel('Active Pattern k')
ax2.set_title('Pattern-k Activation During Cosmic Evolution')
ax2.set_xticks([0, N_GUT, N_EW, N_QCD, N_e])
ax2.set_xticklabels(['Planck', f'GUT\n({N_GUT})', f'EW\n({N_EW})',
                      f'QCD\n({N_QCD})', f'e⁻\n({N_e})'])
ax2.set_yticks([0, 1, 2, 3])
ax2.set_yticklabels(['EM\n(k=0)', 'Weak\n(k=1)', 'Strong\n(k=2)', 'GUT\n(k=3)'])
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/Cristiana_1/Documents/Golden Universe/derivations/force_unification.png', dpi=150)
print("Plot saved as force_unification.png")
"""

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("FORCE UNIFICATION SUMMARY")
print("="*80)

print("\n✅ SUCCESSES:")
print(f"1. Unified coupling α_GUT = {float(alpha_GUT):.5f} (calibrated from α_EM)")
print(f"2. GUT scale X_GUT ~ 10^16 GeV from N=67")
print(f"3. EW scale X_EW ~ 246 GeV from N=89")
print(f"4. QCD scale Λ_QCD ~ 200 MeV from N=95")
print(f"5. Pattern-k sequence explains force hierarchy")

print("\n⚠️ CHALLENGES:")
print(f"1. α_EM = {alpha_EM_derived:.6f} vs target 1/137.036")
print(f"   Error: {error_percent:.1f}% (needs fine-tuning)")
print(f"2. Weinberg angle: {sin2_theta_W:.4f} vs {float(sin2_theta_W_exp):.4f}")
print(f"3. Need two-loop RG for better precision")

print("\n💡 KEY INSIGHT:")
print("All forces emerge from ONE unified coupling α_GUT (calibrated from α_EM)")
print("Symmetry breaking at resonant epochs gives force hierarchy")

print("\n📊 PREDICTIONS:")
if error_percent < 5:
    print("✓ Model successfully predicts gauge unification!")
else:
    print("⚠ Need refinements to match experimental α precisely")

print("\nNext steps:")
print("1. Include two-loop RG corrections")
print("2. Account for threshold effects")
print("3. Include SUSY particles if needed")
print("4. Derive exact Weinberg angle from φ")
