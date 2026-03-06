#!/usr/bin/env python3
"""
CORRECTED RESONANCE ANALYSIS
============================

The user is absolutely right! When δ is very close to 1.0, we should round
to the NEAREST k_res, not just take the floor. This could fix the resonance
failures for strange, bottom, and other particles.

Let's recompute the resonance conditions with proper rounding.
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np

print("=" * 90)
print("CORRECTED RESONANCE ANALYSIS")
print("=" * 90)
print("Using proper rounding instead of just floor(N/φ²)")

# ============================================================================
# RESONANCE ANALYSIS WITH PROPER ROUNDING
# ============================================================================

def analyze_corrected_resonance():
    """Analyze resonance with proper rounding to nearest k_res."""
    
    phi = (1 + np.sqrt(5)) / 2
    phi_sq = phi**2
    
    particles = [
        ('electron', 111),
        ('up', 110),
        ('down', 105),
        ('strange', 102),
        ('muon', 99),
        ('charm', 97),
        ('proton', 95),
        ('tau', 94),
        ('bottom', 89),
        ('top', 81),
    ]
    
    print(f"\nResonance condition analysis:")
    print(f"x = N/φ² where φ² = {phi_sq:.6f}")
    print(f"")
    print(f"{'Particle':>10s}  {'N':>4s}  {'x=N/φ²':>8s}  {'floor(x)':>8s}  {'round(x)':>9s}  {'δ_floor':>8s}  {'δ_round':>8s}  {'Better':>8s}")
    print("-" * 85)
    
    corrected_results = []
    
    for name, N in particles:
        x = N / phi_sq
        k_floor = int(np.floor(x))  # Original method
        k_round = int(np.round(x))  # Corrected method
        
        delta_floor = x - k_floor
        delta_round = x - k_round
        
        # Which gives smaller |δ|?
        better_method = "round" if abs(delta_round) < abs(delta_floor) else "floor"
        
        print(f"{name:>10s}  {N:>4d}  {x:>8.3f}  {k_floor:>8d}  {k_round:>9d}  {delta_floor:>+8.4f}  {delta_round:>+8.4f}  {better_method:>8s}")
        
        corrected_results.append((name, N, k_round, delta_round))
    
    return corrected_results

# ============================================================================
# CORRECTED RESONANCE GATE
# ============================================================================

def apply_corrected_resonance_gate(corrected_results):
    """Apply resonance gate with corrected k_res values."""
    
    print(f"\n" + "-" * 80)
    print("CORRECTED RESONANCE GATE")
    print("-" * 80)
    
    print(f"Resonance condition: k_res must be EVEN AND |δ| < 0.5")
    print(f"Using k_res = round(N/φ²) instead of floor(N/φ²)")
    print(f"")
    print(f"{'Particle':>10s}  {'N':>4s}  {'k_res':>6s}  {'Even?':>6s}  {'δ':>8s}  {'|δ|<0.5?':>9s}  {'Result':>8s}")
    print("-" * 70)
    
    passes = []
    fails = []
    
    for name, N, k_res, delta in corrected_results:
        k_even = k_res % 2 == 0
        delta_ok = abs(delta) < 0.5
        passes_gate = k_even and delta_ok
        
        result = "PASS" if passes_gate else "FAIL"
        
        print(f"{name:>10s}  {N:>4d}  {k_res:>6d}  {str(k_even):>6s}  {delta:>+8.4f}  {str(delta_ok):>9s}  {result:>8s}")
        
        if passes_gate:
            passes.append(name)
        else:
            fails.append(name)
    
    print(f"\n🎯 CORRECTED RESONANCE RESULTS:")
    print(f"   PASS: {', '.join(passes)}")
    print(f"   FAIL: {', '.join(fails)}")
    
    return passes, fails

# ============================================================================
# COMPARISON WITH ORIGINAL METHOD
# ============================================================================

def compare_methods():
    """Compare original vs corrected resonance method."""
    
    print(f"\n" + "=" * 80)
    print("COMPARISON: ORIGINAL vs CORRECTED METHOD")
    print("=" * 80)
    
    # Original results (from winding number analysis)
    original_passes = ['electron', 'up', 'down', 'proton']
    original_fails = ['strange', 'muon', 'charm', 'tau', 'bottom', 'top']
    
    # Get corrected results
    corrected_results = analyze_corrected_resonance()
    corrected_passes, corrected_fails = apply_corrected_resonance_gate(corrected_results)
    
    print(f"\n📊 COMPARISON:")
    print(f"{'Method':>15s}  {'Passes':>8s}  {'Particles':>50s}")
    print("-" * 80)
    print(f"{'Original (floor)':>15s}  {len(original_passes):>8d}  {', '.join(original_passes)}")
    print(f"{'Corrected (round)':>15s}  {len(corrected_passes):>8d}  {', '.join(corrected_passes)}")
    
    # Find differences
    newly_passing = set(corrected_passes) - set(original_passes)
    newly_failing = set(original_passes) - set(corrected_passes)
    
    print(f"\n🔄 CHANGES:")
    if newly_passing:
        print(f"   ✅ Now PASSING: {', '.join(newly_passing)}")
    if newly_failing:
        print(f"   ❌ Now FAILING: {', '.join(newly_failing)}")
    if not newly_passing and not newly_failing:
        print(f"   ➡️ No changes in pass/fail status")
    
    return newly_passing, newly_failing

# ============================================================================
# DETAILED ANALYSIS OF KEY CASES
# ============================================================================

def analyze_key_cases():
    """Analyze the key cases where rounding makes a difference."""
    
    print(f"\n" + "-" * 80)
    print("DETAILED ANALYSIS OF KEY CASES")
    print("-" * 80)
    
    phi = (1 + np.sqrt(5)) / 2
    phi_sq = phi**2
    
    # Focus on particles with δ close to 1.0
    key_cases = [
        ('strange', 102),  # δ = +0.9605
        ('bottom', 89),    # δ = +0.9950  
        ('muon', 99),      # δ = +0.8146
        ('top', 81),       # δ = +0.9392
    ]
    
    print(f"Cases where δ is close to 1.0 (should round up to next k_res):")
    print(f"")
    
    for name, N in key_cases:
        x = N / phi_sq
        k_floor = int(np.floor(x))
        k_round = int(np.round(x))
        
        delta_floor = x - k_floor
        delta_round = x - k_round
        
        print(f"{name.upper()} (N={N}):")
        print(f"   x = N/φ² = {x:.6f}")
        print(f"   Original: k_res = floor({x:.3f}) = {k_floor}, δ = {delta_floor:+.4f}")
        print(f"   Corrected: k_res = round({x:.3f}) = {k_round}, δ = {delta_round:+.4f}")
        print(f"   Improvement: |δ| goes from {abs(delta_floor):.4f} to {abs(delta_round):.4f}")
        
        # Check resonance conditions
        floor_even = k_floor % 2 == 0
        round_even = k_round % 2 == 0
        floor_delta_ok = abs(delta_floor) < 0.5
        round_delta_ok = abs(delta_round) < 0.5
        
        floor_pass = floor_even and floor_delta_ok
        round_pass = round_even and round_delta_ok
        
        print(f"   Original resonance: k_even={floor_even}, |δ|<0.5={floor_delta_ok} → {floor_pass}")
        print(f"   Corrected resonance: k_even={round_even}, |δ|<0.5={round_delta_ok} → {round_pass}")
        
        if round_pass and not floor_pass:
            print(f"   🎉 FIXED! Now passes resonance gate")
        elif floor_pass and not round_pass:
            print(f"   ⚠️ BROKEN! Now fails resonance gate")
        else:
            print(f"   ➡️ No change in resonance status")
        
        print()

# ============================================================================
# IMPLICATIONS FOR PARTICLE PHYSICS
# ============================================================================

def implications_for_physics():
    """Analyze implications of corrected resonance for particle physics."""
    
    print(f"\n" + "=" * 80)
    print("IMPLICATIONS FOR PARTICLE PHYSICS")
    print("=" * 80)
    
    print(f"\n🔬 THEORETICAL SIGNIFICANCE:")
    print(f"   The user's insight about proper rounding is mathematically correct.")
    print(f"   When δ ≈ 1.0, we're much closer to the NEXT k_res than the current one.")
    print(f"   The resonance condition should minimize |δ|, not just use floor.")
    
    print(f"\n📐 MATHEMATICAL JUSTIFICATION:")
    print(f"   Resonance means the system 'locks onto' the nearest integer k_res.")
    print(f"   If δ = 0.96, we're only 0.04 away from k_res + 1.")
    print(f"   It makes physical sense to round to the nearest resonance.")
    
    print(f"\n🎯 POTENTIAL FIXES:")
    print(f"   If corrected rounding fixes strange and bottom resonance,")
    print(f"   then these particles might have proper winding numbers after all!")
    print(f"   This could resolve the apparent inconsistency.")
    
    print(f"\n⚡ NEXT STEPS:")
    print(f"   1. Recompute winding numbers with corrected resonance")
    print(f"   2. Check if strange/bottom now have sector-specific windings")
    print(f"   3. Verify consistency with mass derivation")
    print(f"   4. Update the winding number solver with proper rounding")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Execute corrected resonance analysis."""
    
    compare_methods()
    analyze_key_cases()
    implications_for_physics()

if __name__ == "__main__":
    main()