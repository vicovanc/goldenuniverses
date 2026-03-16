#!/usr/bin/env python3
"""
STATUS: hypothesis
Quarks from QCD Regime - Different Physics
Quarks emerge from strong/weak nuclear force regime, NOT electromagnetic

WARNING: Quark C-factors/Yukawas have NOT been derived from first principles.
Errors: Up 63%, Down 68%, Strange 61%, Charm 67%, Bottom 280%, Top 430%.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.gu_constants import *
import numpy as np

print("="*80)
print("QUARKS FROM QCD/WEAK NUCLEAR REGIME")
print("Different physics from leptons - strong and weak forces dominate")
print("="*80)

# ============================================================================
# FUNDAMENTAL DIFFERENCE: QUARKS vs LEPTONS
# ============================================================================

print("\n### REGIME SEPARATION")
print("-"*60)

print("LEPTONS (QED regime):")
print("  - Feel electromagnetic force primarily")
print("  - No color charge")
print("  - Can exist as free particles")
print("  - Mass from Yukawa coupling to Higgs")
print("  - Formula: m = M_P × (2πC/φ^N) × η_QED")

print("\nQUARKS (QCD/Weak regime):")
print("  - Feel strong force primarily")
print("  - Carry color charge")
print("  - CONFINED - never free")
print("  - Mass from QCD condensate + Higgs")
print("  - Need DIFFERENT formula!")

# ============================================================================
# QCD REGIME PHYSICS
# ============================================================================

print("\n### QCD CONDENSATE AND CONFINEMENT")
print("-"*60)

# QCD scale
Lambda_QCD = float(X_at_epoch(N_QCD))  # ~200 MeV
print(f"Λ_QCD = {Lambda_QCD:.1f} MeV (confinement scale)")

# Quark condensate
# <ψ̄ψ> = -(250 MeV)³ phenomenologically
condensate = -250**3  # MeV³
print(f"Quark condensate: <ψ̄ψ> = {condensate/1e6:.1f} × 10^6 MeV³")

# This generates constituent mass
m_constituent_QCD = (-condensate)**(1/3)
print(f"Constituent mass from QCD: ~{m_constituent_QCD:.0f} MeV")

# ============================================================================
# PATTERN-K FOR NUCLEAR FORCES
# ============================================================================

print("\n### PATTERN-K ACTIVATION FOR QUARKS")
print("-"*60)

def pattern_k_nuclear(particle_type):
    """
    Pattern-k determines which force dominates
    """
    if particle_type == "lepton":
        return 0  # k=0: electromagnetic
    elif particle_type == "light_quark":
        return 2  # k=2: strong force (QCD)
    elif particle_type == "heavy_quark":
        return 1  # k=1: weak force matters more

# Pattern factors
pattern_factors = {
    0: 1,           # EM
    1: float(pi),   # Weak
    2: float(pi)**2 # Strong
}

print("Pattern assignments:")
print("  k=0 (EM): Leptons - photon exchange")
print("  k=1 (Weak): Heavy quarks - W/Z important")
print("  k=2 (Strong): Light quarks - gluon dominated")

# ============================================================================
# QUARK MASS FORMULA (QCD REGIME)
# ============================================================================

print("\n### QUARK MASS DERIVATION")
print("-"*60)

def calculate_quark_mass_qcd(name, N):
    """
    Quark mass from QCD/weak regime
    DIFFERENT from lepton formula!
    """

    # Determine quark type
    if N > 100:  # Light quarks (u, d, s)
        regime = "light"
        k = 2  # Strong force dominated
    elif N > 85:  # Medium (c)
        regime = "medium"
        k = 1.5  # Mixed
    else:  # Heavy (b, t)
        regime = "heavy"
        k = 1  # Weak force important

    # Base scale from epoch (but different meaning)
    X_scale = float(X_at_epoch(N))

    # For quarks, mass comes from:
    # 1. Current mass (Higgs/Yukawa)
    # 2. QCD dressing
    # 3. Confinement effects

    if regime == "light":
        # Light quarks: dominated by QCD
        # Current mass is tiny, constituent mass from condensate

        # Current mass from Yukawa
        y_quark = X_scale / float(X_EW)  # Yukawa ~ m/v
        m_current = y_quark * float(X_EW)

        # Constituent mass from QCD
        # Uses Gell-Mann-Oakes-Renner relation
        f_pi = 93  # MeV (pion decay constant)
        m_constituent = np.sqrt(m_current * abs(condensate)**(1/3))

        # But empirically, light quarks get ~300-350 MeV
        m_constituent = 300 + m_current * 10  # Phenomenological

        return m_current, m_constituent

    elif regime == "medium":
        # Charm: transitional
        # Both Yukawa and QCD matter

        # Yukawa gives most of mass
        y_charm = 0.01  # Charm Yukawa coupling
        m_current = y_charm * float(X_EW)

        # QCD corrections
        alpha_s = 0.2  # Stronger at charm scale
        m_pole = m_current * (1 + 4*alpha_s/(3*np.pi))

        return m_current, m_pole

    else:  # Heavy
        # Bottom and top: Yukawa dominated
        # These couple strongly to Higgs

        if name == "top":
            y_top = 1.0  # Top Yukawa ~ 1 (!!)
        else:
            y_bottom = 0.02  # Bottom Yukawa

        m_current = y_top * float(X_EW) if name == "top" else y_bottom * float(X_EW)

        # Small QCD correction
        alpha_s = 0.118
        m_pole = m_current * (1 + 4*alpha_s/(3*np.pi))

        return m_current, m_pole

# ============================================================================
# CALCULATE ALL QUARKS
# ============================================================================

print("\nQuark masses from QCD/Weak regime:")
print("-"*60)

quarks_qcd = [
    ("up", N_u, 2.16, 336),
    ("down", N_d, 4.67, 340),
    ("strange", N_s, 93, 486),
    ("charm", N_c, 1270, 1500),
    ("bottom", N_b, 4180, 4730),
    ("top", N_t, 172760, None)
]

print(f"{'Quark':<10} {'N':<5} {'Current (MeV)':<15} {'Constituent':<15} {'PDG current':<15} {'PDG constit':<15}")
print("-"*85)

for name, N, pdg_current, pdg_constituent in quarks_qcd:
    m_current, m_other = calculate_quark_mass_qcd(name, N)

    # Display appropriate comparison
    if N > 100:  # Light quarks
        current_str = f"{m_current:.2f}"
        other_str = f"{m_other:.1f}"
        pdg_other_str = f"{pdg_constituent:.0f}" if pdg_constituent else "--"

        # Error on constituent mass (more relevant)
        if pdg_constituent:
            error = abs(m_other - pdg_constituent) / pdg_constituent * 100
        else:
            error = abs(m_current - pdg_current) / pdg_current * 100

    else:  # Heavy quarks
        current_str = f"{m_current:.0f}"
        other_str = f"{m_other:.0f}"
        pdg_other_str = "--"

        # Error on pole mass
        error = abs(m_other - pdg_current) / pdg_current * 100

    status = "✓" if error < 20 else "⚠" if error < 50 else "✗"

    print(f"{name:<10} {N:<5} {current_str:<15} {other_str:<15} {pdg_current:<15.2f} {pdg_other_str:<15} {error:>5.1f}% {status}")

# ============================================================================
# YUKAWA HIERARCHY
# ============================================================================

print("\n### YUKAWA COUPLING HIERARCHY")
print("-"*60)

print("The real question: Why do quarks have these Yukawa couplings?")
print("\nYukawa hierarchy (phenomenological):")
yukawas = [
    ("electron", 3e-6),
    ("up", 1.3e-5),
    ("down", 2.7e-5),
    ("strange", 5.4e-4),
    ("muon", 6.1e-4),
    ("charm", 7.3e-3),
    ("tau", 1.0e-2),
    ("bottom", 2.4e-2),
    ("top", 1.0)
]

print(f"{'Particle':<10} {'Yukawa':<10} {'log(y)':<10}")
for particle, y in yukawas:
    print(f"{particle:<10} {y:<10.2e} {np.log10(y):<10.1f}")

print("\nPattern: Yukawas span 6 orders of magnitude!")
print("This is the REAL hierarchy problem")

# ============================================================================
# GOLDEN RATIO PATTERN IN YUKAWAS?
# ============================================================================

print("\n### GOLDEN RATIO IN YUKAWA HIERARCHY")
print("-"*60)

print("Hypothesis: Yukawa couplings follow golden ratio pattern")

# Check ratios
y_values = [y for _, y in yukawas]
for i in range(1, len(y_values)):
    ratio = y_values[i] / y_values[i-1]
    phi_power = np.log(ratio) / np.log(float(phi))
    print(f"y_{i}/y_{i-1} = {ratio:.2f} ~ φ^{phi_power:.1f}")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("QCD REGIME INSIGHTS")
print("="*80)

print("\n✅ KEY REALIZATIONS:")
print("1. Quarks are NOT like leptons - different physics!")
print("2. Light quarks: mass from QCD condensate (~300 MeV)")
print("3. Heavy quarks: mass from Yukawa coupling to Higgs")
print("4. Pattern k=2 (strong) for light, k=1 (weak) for heavy")

print("\n💡 THE REAL PROBLEM:")
print("We need to derive Yukawa couplings from first principles")
print("These span 6 orders of magnitude (10^-6 to 1)")
print("Top quark: y_t ≈ 1 (special - non-perturbative)")
print("Electron: y_e ≈ 10^-6 (highly suppressed)")

print("\n🎯 NEW APPROACH NEEDED:")
print("Don't try to force quark formula to be like leptons")
print("Quarks come from QCD/weak regime with:")
print("  - Color confinement")
print("  - Chiral symmetry breaking")
print("  - Strong CP problem")
print("  - Yukawa hierarchy")

print("\nThe Golden Universe must explain WHY:")
print("  - Top Yukawa = 1")
print("  - Hierarchy spans 10^6")
print("  - Three generations exist")
print("  - Quarks are confined")