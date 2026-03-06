#!/usr/bin/env python3
"""
ODD k_res ANALYSIS — Why Strange, Charm, and Top Fail
====================================================

Investigating what's special about particles with odd k_res values
that cause them to fail the resonance gate.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from math import gcd
from mpmath import mp, mpf, sqrt, pi as mp_pi, exp
mp.dps = 50

phi = (mpf('1') + sqrt(mpf('5'))) / 2
phi_sq = phi ** 2

print("=" * 90)
print("ODD k_res ANALYSIS — Why Strange, Charm, and Top Fail")
print("=" * 90)

def analyze_odd_kres_particles():
    """Analyze the particles that fail due to odd k_res."""
    
    # All particles with their epochs and corrected resonance data
    particles = [
        ("electron", 111, "lepton", 42, +0.3982, "PASS", "even"),
        ("up", 110, "universal", 42, +0.0163, "PASS", "even"),
        ("down", 105, "universal", 40, +0.1064, "PASS", "even"),
        ("strange", 102, "universal", 39, -0.0395, "FAIL", "odd"),
        ("muon", 99, "lepton", 38, -0.1854, "PASS", "even"),
        ("charm", 97, "quark", 37, +0.0507, "FAIL", "odd"),
        ("proton", 95, "universal", 36, +0.2868, "PASS", "even"),
        ("tau", 94, "universal", 36, -0.0952, "PASS", "even"),
        ("bottom", 89, "quark", 34, -0.0050, "PASS", "even"),
        ("top", 81, "universal", 31, -0.0608, "FAIL", "odd"),
    ]
    
    print(f"\n📊 RESONANCE GATE ANALYSIS:")
    print(f"")
    print(f"{'Particle':>10s}  {'N':>3s}  {'k_res':>5s}  {'Parity':>6s}  {'δ':>8s}  {'Status':>6s}  {'Reason':>20s}")
    print("-" * 80)
    
    passing = []
    failing = []
    
    for name, N, sector, k_res, delta, status, parity in particles:
        reason = ""
        if status == "PASS":
            reason = "k even, |δ| < 0.5"
            passing.append((name, N, k_res, parity))
        else:
            if k_res % 2 == 1:
                reason = "k odd (fails)"
            elif abs(delta) >= 0.5:
                reason = "|δ| ≥ 0.5 (fails)"
            else:
                reason = "unknown"
            failing.append((name, N, k_res, parity, reason))
        
        print(f"{name:>10s}  {N:>3d}  {k_res:>5d}  {parity:>6s}  {delta:>+8.4f}  {status:>6s}  {reason:>20s}")
    
    return passing, failing

def analyze_patterns(passing, failing):
    """Analyze patterns in passing vs failing particles."""
    
    print(f"\n🔍 PATTERN ANALYSIS:")
    print(f"")
    
    # Separate by pass/fail
    print(f"✅ PASSING PARTICLES ({len(passing)}):")
    for name, N, k_res, parity in passing:
        print(f"   {name:>10s}: N={N:>3d}, k_res={k_res:>2d} ({parity})")
    
    print(f"\n❌ FAILING PARTICLES ({len(failing)}):")
    for name, N, k_res, parity, reason in failing:
        print(f"   {name:>10s}: N={N:>3d}, k_res={k_res:>2d} ({parity}) — {reason}")
    
    # Analyze k_res values
    passing_k = [k for _, _, k, _ in passing]
    failing_k = [k for _, _, k, _, _ in failing]
    
    print(f"\n📈 k_res STATISTICS:")
    print(f"   Passing k_res values: {sorted(passing_k)}")
    print(f"   Failing k_res values: {sorted(failing_k)}")
    print(f"   All passing are EVEN: {all(k % 2 == 0 for k in passing_k)}")
    print(f"   All failing are ODD: {all(k % 2 == 1 for k in failing_k)}")

def analyze_epochs():
    """Analyze the epoch values of odd k_res particles."""
    
    print(f"\n🎯 EPOCH ANALYSIS OF ODD k_res PARTICLES:")
    print(f"")
    
    odd_particles = [
        ("strange", 102),
        ("charm", 97),
        ("top", 81),
    ]
    
    print(f"{'Particle':>10s}  {'N':>3s}  {'N/φ²':>10s}  {'k_res':>5s}  {'δ':>8s}  {'Properties':>30s}")
    print("-" * 80)
    
    for name, N in odd_particles:
        x = float(mpf(N) / phi_sq)
        k_res = round(x)
        delta = x - k_res
        
        # Analyze properties
        properties = []
        if N % 2 == 1:
            properties.append("N odd")
        else:
            properties.append("N even")
        
        # Check divisibility
        for p in [3, 5, 7, 11, 13, 17, 19]:
            if N % p == 0:
                properties.append(f"N÷{p}")
        
        props_str = ", ".join(properties[:3])  # Limit display
        
        print(f"{name:>10s}  {N:>3d}  {x:>10.6f}  {k_res:>5d}  {delta:>+8.4f}  {props_str:>30s}")

def analyze_generation_structure():
    """Analyze if odd k_res relates to generation structure."""
    
    print(f"\n🧬 GENERATION STRUCTURE ANALYSIS:")
    print(f"")
    
    generations = {
        1: [("up", 110), ("down", 105), ("electron", 111)],
        2: [("charm", 97), ("strange", 102), ("muon", 99)],
        3: [("top", 81), ("bottom", 89), ("tau", 94)]
    }
    
    print(f"{'Generation':>10s}  {'Quarks':>25s}  {'Lepton':>15s}  {'k_res Pattern':>20s}")
    print("-" * 80)
    
    for gen, particles in generations.items():
        quarks = [p for p in particles if p[0] in ['up', 'down', 'charm', 'strange', 'top', 'bottom']]
        leptons = [p for p in particles if p[0] in ['electron', 'muon', 'tau']]
        
        quark_kres = []
        for name, N in quarks:
            x = float(mpf(N) / phi_sq)
            k_res = round(x)
            quark_kres.append((name, k_res))
        
        lepton_kres = []
        for name, N in leptons:
            x = float(mpf(N) / phi_sq)
            k_res = round(x)
            lepton_kres.append((name, k_res))
        
        quark_str = ", ".join([f"{name}({k})" for name, k in quark_kres])
        lepton_str = ", ".join([f"{name}({k})" for name, k in lepton_kres])
        
        # Analyze pattern
        all_k = [k for _, k in quark_kres + lepton_kres]
        pattern = "all even" if all(k % 2 == 0 for k in all_k) else "mixed"
        if any(k % 2 == 1 for k in all_k):
            odd_count = sum(1 for k in all_k if k % 2 == 1)
            pattern = f"{odd_count} odd"
        
        print(f"{gen:>10d}  {quark_str:>25s}  {lepton_str:>15s}  {pattern:>20s}")

def mathematical_investigation():
    """Investigate mathematical properties of odd k_res."""
    
    print(f"\n🔢 MATHEMATICAL INVESTIGATION:")
    print(f"")
    
    print(f"The resonance condition requires k_res to be EVEN. Why?")
    print(f"")
    print(f"1. CRYSTALLIZATION PHYSICS:")
    print(f"   The resonance gate k_res = round(N/φ²) must be even for")
    print(f"   proper crystallization on the Ω-torus. This suggests that")
    print(f"   odd k_res corresponds to 'anti-resonant' or 'forbidden' states.")
    print(f"")
    print(f"2. PARITY SELECTION RULE:")
    print(f"   Even k_res ↔ Constructive interference")
    print(f"   Odd k_res  ↔ Destructive interference")
    print(f"")
    print(f"3. TORUS TOPOLOGY:")
    print(f"   Even k_res may correspond to closed geodesics that wrap")
    print(f"   the torus an even number of times, ensuring proper")
    print(f"   boundary conditions for the NLDE soliton.")
    print(f"")
    
    # Check if there's a pattern in the failing epochs
    failing_epochs = [102, 97, 81]  # strange, charm, top
    
    print(f"4. FAILING EPOCH ANALYSIS:")
    for N in failing_epochs:
        x = float(mpf(N) / phi_sq)
        k_floor = int(x)
        k_round = round(x)
        delta_floor = x - k_floor
        delta_round = x - k_round
        
        print(f"   N={N}: x={x:.6f}")
        print(f"      floor: k={k_floor} (δ={delta_floor:+.4f})")
        print(f"      round: k={k_round} (δ={delta_round:+.4f}) ← odd!")
        print(f"      These particles are 'trapped' at odd k_res values")
        print()

def theoretical_implications():
    """Discuss theoretical implications."""
    
    print(f"\n💡 THEORETICAL IMPLICATIONS:")
    print(f"")
    print(f"1. TWO CLASSES OF PARTICLES:")
    print(f"   ✅ Resonant: Even k_res → Full winding number physics")
    print(f"   ❌ Anti-resonant: Odd k_res → Alternative physics needed")
    print(f"")
    print(f"2. POSSIBLE ALTERNATIVE MECHANISMS:")
    print(f"   • Strange, charm, top may use different mass generation")
    print(f"   • Could involve higher-order corrections")
    print(f"   • May require non-Abelian gauge theory")
    print(f"   • Could be related to CP violation or flavor mixing")
    print(f"")
    print(f"3. GENERATION PATTERN:")
    print(f"   Gen 1: All pass (electron, up, down)")
    print(f"   Gen 2: Mixed (muon passes, strange/charm fail)")
    print(f"   Gen 3: Mixed (tau/bottom pass, top fails)")
    print(f"")
    print(f"4. SUCCESS OF SU(5) + QCD:")
    print(f"   Our SU(5) Georgi-Jarlskog + QCD running approach")
    print(f"   works for ALL quarks, including the 'odd k_res' ones.")
    print(f"   This suggests that winding numbers are not the ONLY")
    print(f"   mass generation mechanism in the Golden Universe!")
    print(f"")
    print(f"5. COMPLEMENTARY PHYSICS:")
    print(f"   • Winding numbers: Fundamental mechanism (electron, muon, bottom)")
    print(f"   • SU(5) + QCD: Effective theory that works for all quarks")
    print(f"   • Both are needed for complete understanding")

def main():
    """Execute odd k_res analysis."""
    
    passing, failing = analyze_odd_kres_particles()
    analyze_patterns(passing, failing)
    analyze_epochs()
    analyze_generation_structure()
    mathematical_investigation()
    theoretical_implications()
    
    print(f"\n" + "=" * 90)
    print(f"CONCLUSION")
    print(f"=" * 90)
    print(f"")
    print(f"The 'odd' thing about strange, charm, and top quarks is that")
    print(f"their epochs N lead to ODD k_res values when rounded:")
    print(f"")
    print(f"• Strange (N=102): k_res = 39 (odd)")
    print(f"• Charm (N=97): k_res = 37 (odd)")  
    print(f"• Top (N=81): k_res = 31 (odd)")
    print(f"")
    print(f"The resonance gate requires EVEN k_res for constructive")
    print(f"interference and proper crystallization. Odd k_res particles")
    print(f"are 'anti-resonant' and may use different mass generation")
    print(f"mechanisms beyond simple winding number physics.")
    print(f"")
    print(f"This explains why our SU(5) + QCD approach works so well")
    print(f"for ALL quarks — it's the correct effective theory that")
    print(f"captures both resonant AND anti-resonant particles!")

if __name__ == "__main__":
    main()