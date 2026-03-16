#!/usr/bin/env python3
"""
STATUS: hypothesis
Quark analysis experiment with Phase-17-style epochs/resonance heuristics.
Includes exploratory phase-transition-style constructions and k_res analysis.

WARNING: Quark C-factors have NOT been derived from first principles.
Errors: Up 63%, Down 68%, Strange 61%, Charm 67%, Bottom 280%, Top 430%.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.gu_constants import *
import numpy as np

print("="*80)
print("PHASE-17 QUARK EPOCH/RESONANCE EXPLORATION")
print("Exploratory analysis including phase-transition heuristics")
print("="*80)

# ============================================================================
# QUARK EPOCHS AND RESONANCES
# ============================================================================

# Exploratory phase-epoch assumptions used in this script.
N_u_phase = 110 + 41  # Up quark phase transition?
N_d_phase = 105 + 41  # Down quark phase transition?

epochs_data = [
    ('u-quark', N_u, 36),
    ('d-quark', N_d, 35),
    ('s-quark', N_s, 35),
    ('u-phase', N_u_phase, 41),
    ('d-phase', N_d_phase, 41),
    ('c-quark', N_c, None),
    ('b-quark', N_b, None),
    ('t-quark', N_t, None)
]

print("\n### RESONANCE ANALYSIS")
print("-"*60)

print(f"{'Epoch':<12} {'N':<5} {'k_res':<7} {'N/φ²':<10} {'Residual':<10} {'Status'}")
print("-"*70)

for name, N, k_given in epochs_data:
    ratio = N / float(phi)**2
    k_calc = round(ratio)
    residual = ratio - k_calc

    # Check if given k matches calculated
    if k_given is not None:
        match = "✓" if k_given == k_calc else f"❌ (calc={k_calc})"
    else:
        k_given = k_calc
        match = "computed"

    quality = abs(residual / k_calc) * 100 if k_calc > 0 else 100

    print(f"{name:<12} {N:<5} {k_given:<7} {ratio:<10.4f} {residual:<+10.4f} {match}")

# ============================================================================
# QUARK MASS CALCULATION WITH PHASES
# ============================================================================

print("\n### QUARK MASSES WITH PHASE TRANSITIONS")
print("-"*60)

# All quarks with standard and phase epochs
QUARKS_COMPLETE = [
    ("up", N_u, 2.16, "current"),
    ("up-constituent", N_u, 336, "constituent"),
    ("up-phase", N_u_phase, 336, "phase"),
    ("down", N_d, 4.67, "current"),
    ("down-constituent", N_d, 340, "constituent"),
    ("down-phase", N_d_phase, 340, "phase"),
    ("strange", N_s, 93, "current"),
    ("strange-const", N_s, 486, "constituent"),
    ("charm", N_c, 1270, "current"),
    ("bottom", N_b, 4180, "current"),
    ("top", N_t, 172760, "current")
]

def calculate_quark_mass(N, k_res, mass_type="current"):
    """
    Exploratory quark-mass formula for this hypothesis script.
    """
    # Detuning from resonance
    delta = N / float(phi)**2 - k_res

    # C factor depends on resonance quality
    if abs(delta) < 0.01:  # Very close to resonance
        C = 1.0
    else:
        C = 1.0 / (1 + 10 * delta**2)  # Suppression away from resonance

    # Phase transition effects
    if "phase" in mass_type:
        C *= np.exp(-0.1 * abs(N - 110))  # Suppression from standard epoch

    # Base mass
    mass = float(M_P) * 2 * float(pi) * C / float(phi)**N

    # Constituent mass gets QCD contribution
    if "constituent" in mass_type:
        mass += 300  # MeV from chiral symmetry breaking

    return mass, C

print("\nQuark mass calculations:")
print(f"{'Quark':<20} {'N':<5} {'Type':<12} {'Calc (MeV)':<12} {'Exp (MeV)':<12} {'Error %'}")
print("-"*80)

for name, N, exp_mass, mass_type in QUARKS_COMPLETE:
    # Get k_res for this epoch
    k_res = round(N / float(phi)**2)

    # Calculate mass
    calc_mass, C = calculate_quark_mass(N, k_res, mass_type)

    # Apply QCD corrections for current masses
    if mass_type == "current" and N < 100:
        alpha_s = 0.118
        calc_mass *= (1 + 4*alpha_s/(3*np.pi))

    error = abs(calc_mass - exp_mass) / exp_mass * 100

    status = "✓" if error < 10 else "⚠" if error < 50 else "✗"

    print(f"{name:<20} {N:<5} {mass_type:<12} {calc_mass:<12.3f} {exp_mass:<12.3f} {error:>6.1f} {status}")

# ============================================================================
# WINDING NUMBER DERIVATION FOR QUARKS
# ============================================================================

print("\n### WINDING NUMBERS FOR QUARKS")
print("-"*60)

def derive_winding_numbers(N):
    """
    Derive optimal (p,q) for epoch N
    Constraint: |p| + |q| = N
    """
    best_energy = float('inf')
    best_p, best_q = 0, 0

    # Search over allowed values
    for p in range(-N, 0):
        q = N - abs(p)

        # Energy functional (simplified)
        q_eff = q / float(phi)
        energy = p**2 + q_eff**2

        if energy < best_energy:
            best_energy = energy
            best_p, best_q = p, q

    return best_p, best_q

print("Derived winding numbers for quarks:")
print(f"{'Quark':<10} {'N':<5} {'(p,q) derived':<15} {'|p|+|q|':<10}")
print("-"*50)

for name in ['up', 'down', 'strange', 'charm', 'bottom', 'top']:
    if name == 'up':
        N = N_u
    elif name == 'down':
        N = N_d
    elif name == 'strange':
        N = N_s
    elif name == 'charm':
        N = N_c
    elif name == 'bottom':
        N = N_b
    elif name == 'top':
        N = N_t

    p, q = derive_winding_numbers(N)
    check = abs(p) + abs(q)

    print(f"{name:<10} {N:<5} ({p:>3}, {q:>3}){'':<5} {check:<10}")

# ============================================================================
# MASS HIERARCHY ANALYSIS
# ============================================================================

print("\n### MASS HIERARCHY FROM EPOCHS")
print("-"*60)

print("Generation structure:")
print("\nGeneration 1 (lightest):")
print(f"  up: N={N_u}, m ~ φ^(-{N_u})")
print(f"  down: N={N_d}, m ~ φ^(-{N_d})")
print(f"  electron: N={N_e}, m ~ φ^(-{N_e})")

print("\nGeneration 2:")
print(f"  charm: N={N_c}, m ~ φ^(-{N_c})")
print(f"  strange: N={N_s}, m ~ φ^(-{N_s})")
print(f"  muon: N=100, m ~ φ^(-100)")

print("\nGeneration 3 (heaviest):")
print(f"  top: N={N_t}, m ~ φ^(-{N_t})")
print(f"  bottom: N={N_b}, m ~ φ^(-{N_b})")
print(f"  tau: N={N_tau}, m ~ φ^(-{N_tau})")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("QUARK ANALYSIS SUMMARY")
print("="*80)

print("\n💡 KEY FINDINGS:")
print("1. Quarks have resonance conditions N/φ² ≈ k (integer)")
print("2. Phase transitions occur at N_phase = N + Δk×φ²")
print("3. Current vs constituent mass from QCD")
print("4. Winding numbers follow |p| + |q| = N constraint")

print("\n📊 RESONANCE PATTERN:")
print("Light quarks: k ~ 35-36")
print("Heavy quarks: k ~ 30-34")
print("Phase shifts: Δk ~ 5-6")

print("\n🎯 IMPLICATIONS:")
print("1. Mass hierarchy from N (epoch)")
print("2. Generation structure from k (resonance)")
print("3. QCD effects from phase transitions")
print("4. Framework motivated by golden ratio; quark C-factors NOT derived")