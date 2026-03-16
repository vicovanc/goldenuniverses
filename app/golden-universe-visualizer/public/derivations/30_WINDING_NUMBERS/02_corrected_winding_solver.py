#!/usr/bin/env python3
"""
CORRECTED WINDING NUMBER SOLVER — PROPER RESONANCE ROUNDING
===========================================================

CRITICAL FIX: Uses round(N/φ²) instead of floor(N/φ²) for resonance condition.
This fixes the resonance gate for particles with δ close to 1.0.

Based on user insight: when δ ≈ 1.0, we should round to the NEAREST k_res
to minimize |δ|, not just take the floor.

EXPECTED FIXES:
- Bottom (N=89): δ = +0.9950 → -0.0050 (now passes!)
- Muon (N=99): δ = +0.8146 → -0.1854 (now passes!)
- Tau (N=94): δ = +0.9048 → -0.0952 (now passes!)
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from math import gcd
from mpmath import mp, mpf, sqrt, pi as mp_pi, exp, ellipk, ellipe, ln
mp.dps = 50

phi = (mpf('1') + sqrt(mpf('5'))) / 2
phi_sq = phi ** 2
pi = mp_pi
alpha_EM = mpf('1') / mpf('137.035999084')
M_P = mpf('1.22089e22')  # MeV
lambda_rec_beta = exp(phi) / pi**2

# ============================================================================
# LAYER 1: ADMISSIBILITY LATTICES (unchanged)
# ============================================================================

class AdmissibilityLattice:
    """Base class for sector-specific gauge-congruence lattices."""
    name = "base"

    def generate_candidates(self, N):
        """Yield all (p, q) in this lattice with |p| + |q| = N."""
        raise NotImplementedError

class LeptonLattice(AdmissibilityLattice):
    """Charged-lepton admissible winding lattice."""
    name = "lepton"

    def generate_candidates(self, N):
        for b in range(1, N // 10 + 1):
            q = 10 * b
            abs_p = N - q
            if abs_p <= 0:
                continue
            for sign in [+1, -1]:
                p = sign * abs_p
                if (p - b) % 2 == 0:
                    yield (p, q)

class QuarkLattice(AdmissibilityLattice):
    """Quark admissible winding lattice."""
    name = "quark"

    def generate_candidates(self, N):
        for s in range(1, N // 30 + 1):
            q = 30 * s
            abs_p = N - q
            if abs_p <= 0:
                continue
            for sign in [+1, -1]:
                p = sign * abs_p
                if (p + s) % 2 == 0:
                    yield (p, q)

class UniversalLattice(AdmissibilityLattice):
    """Universal geometric mode — no gauge-congruence restriction."""
    name = "universal"

    def generate_candidates(self, N):
        for abs_p in range(1, N):
            q = N - abs_p
            yield (-abs_p, q)

LATTICES = {
    'lepton': LeptonLattice(),
    'quark': QuarkLattice(),
    'universal': UniversalLattice(),
}

# ============================================================================
# LAYER 2: CORRECTED RESONANCE CLOSURE FILTER
# ============================================================================

def resonance_filter_corrected(N):
    """
    CORRECTED resonance filter using proper rounding.
    
    x = N/φ²,  k_res = round(x),  δ = x − k_res
    Accept iff  k_res is even  AND  |δ| < 1/2.
    
    Returns (passes, k_res, delta).
    """
    x = float(mpf(N) / phi_sq)
    k_res = round(x)  # CORRECTED: use round() instead of int(x)
    delta = x - k_res
    passes = (k_res % 2 == 0) and (abs(delta) < 0.5)
    return passes, k_res, delta

# ============================================================================
# LAYER 3: PRIMITIVE WINDING (unchanged)
# ============================================================================

def is_primitive(p, q):
    """gcd(|p|, |q|) = 1 — primitive geodesic on the torus."""
    return gcd(abs(p), abs(q)) == 1

# ============================================================================
# LAYER 4: Ω-VARIATIONAL MINIMIZATION (unchanged)
# ============================================================================

def L_Omega(p, q):
    """Ω-geodesic length on the anisotropic torus."""
    return 2 * pi * sqrt(mpf(p)**2 + (mpf(q) / phi)**2)

# ============================================================================
# WINDING RESULT (updated with corrected resonance)
# ============================================================================

class WindingResult:
    """Complete set of derived quantities from winding numbers at epoch N."""

    def __init__(self, N, p, q, lattice_name="unknown"):
        self.N = N
        self.p = p
        self.q = q
        self.abs_p = abs(p)
        self.abs_q = abs(q)
        self.lattice_name = lattice_name

        q_over_phi = mpf(q) / phi
        R_sq = mpf(p)**2 + q_over_phi**2
        self.R = sqrt(R_sq)
        self.l_Omega = 2 * pi * self.R
        self.nu = abs(q_over_phi) / self.R

        # CORRECTED: use proper rounding for resonance
        k_res_exact = mpf(N) / phi_sq
        self.k_res = round(float(k_res_exact))  # CORRECTED
        self.delta = float(k_res_exact - self.k_res)

        self.K_nu = ellipk(self.nu)
        self.E_nu = ellipe(self.nu)

        self.Lambda1 = 16 * self.K_nu**2 / self.l_Omega**4
        self.S_topo = float(-ln(self.Lambda1))

        self.mu_closure = 4 * self.K_nu / self.l_Omega
        self.mod_defect = float(1 - self.E_nu / self.K_nu)
        self.resonance_quality = abs(self.delta) / self.k_res if self.k_res > 0 else float('inf')
        self.coprime = gcd(self.abs_p, self.abs_q) == 1

    def __repr__(self):
        return (f"WindingResult(N={self.N}, p={self.p}, q={self.q}, "
                f"nu={float(self.nu):.6f}, l_Omega={float(self.l_Omega):.4f}, "
                f"lattice={self.lattice_name})")

# ============================================================================
# MAIN CORRECTED SOLVER
# ============================================================================

def find_winding_numbers_corrected(N, sector='lepton', require_primitive=True, verbose=False):
    """
    CORRECTED winding number solver with proper resonance rounding.
    """
    lattice = LATTICES[sector]

    res_passes, k_res, delta = resonance_filter_corrected(N)

    if verbose:
        print(f"\n  Epoch N = {N},  sector = {sector}")
        print(f"  CORRECTED Resonance: x = N/φ² = {N/float(phi_sq):.6f},  k_res = {k_res} (ROUNDED),  "
              f"δ = {delta:.6f}")
        print(f"  Resonance gate: k_res even = {k_res % 2 == 0},  |δ| < 0.5 = {abs(delta) < 0.5}"
              f"  →  {'PASS' if res_passes else 'FAIL'}")
        print(f"  Searching {lattice.name} lattice for candidates...")
        print(f"  {'(p, q)':>14s} {'gcd':>5s} {'prim':>5s} {'L_Omega':>12s} {'nu':>10s}")
        print("  " + "-" * 55)

    best_L = mpf('inf')
    best_p, best_q = None, None
    n_candidates = 0
    n_primitive = 0

    for p, q in lattice.generate_candidates(N):
        n_candidates += 1
        prim = is_primitive(p, q)
        if prim:
            n_primitive += 1

        if require_primitive and not prim:
            if verbose:
                L = L_Omega(p, q)
                print(f"  ({p:+4d}, {q:3d})   {gcd(abs(p),q):>3d}     {'N':>3s}  "
                      f"{float(L):>12.4f}   -- skipped (not primitive)")
            continue

        L = L_Omega(p, q)

        if verbose:
            q_over_phi = mpf(q) / phi
            R = sqrt(mpf(p)**2 + q_over_phi**2)
            nu = abs(q_over_phi) / R
            marker = " <-- best" if L < best_L else ""
            print(f"  ({p:+4d}, {q:3d})   {gcd(abs(p),q):>3d}     {'Y':>3s}  "
                  f"{float(L):>12.4f}  {float(nu):>10.6f}{marker}")

        if L < best_L:
            best_L = L
            best_p, best_q = p, q

    if verbose:
        print(f"\n  Total candidates in lattice: {n_candidates}")
        print(f"  Primitive (coprime) candidates: {n_primitive}")
        if best_p is not None:
            print(f"  Selected: ({best_p}, {best_q}) with L_Ω = {float(best_L):.4f}")
        else:
            print(f"  NO candidate found (primitive={require_primitive})")

    if best_p is None:
        return None

    # Standard GU orientation convention: w* = (-|p|, q)
    if best_p > 0:
        best_p = -best_p

    return WindingResult(N, best_p, best_q, lattice.name)

# ============================================================================
# EPOCH REGISTRY (unchanged)
# ============================================================================

PARTICLE_EPOCHS = {
    'electron':  (111, 'lepton'),
    'muon':      (99,  'lepton'),
    'tau':       (94,  'lepton'),
    'up':        (110, 'quark'),
    'down':      (105, 'quark'),
    'strange':   (102, 'quark'),
    'charm':     (97,  'quark'),
    'bottom':    (89,  'quark'),
    'top':       (81,  'quark'),
    'proton':    (95,  'universal'),
}

# ============================================================================
# CORRECTED ANALYSIS
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("CORRECTED WINDING NUMBER SOLVER — PROPER RESONANCE ROUNDING")
    print("=" * 80)

    # ------------------------------------------------------------------
    # CORRECTED FULL EPOCH TABLE
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("CORRECTED FULL EPOCH TABLE")
    print("=" * 80)
    print(f"\n  {'Particle':>10s}  {'N':>4s}  {'Sector':>9s}  {'(p, q)':>12s}  "
          f"{'gcd':>4s}  {'prim':>5s}  {'L_Ω':>10s}  {'ν':>10s}  "
          f"{'k_res':>5s}  {'δ':>8s}  {'res':>4s}")
    print("  " + "-" * 105)

    results_table = {}
    for name, (N, sector) in sorted(PARTICLE_EPOCHS.items(), key=lambda x: -x[1][0]):
        r = find_winding_numbers_corrected(N, sector=sector)
        if r is None:
            # Try universal fallback
            r = find_winding_numbers_corrected(N, sector='universal')
        results_table[name] = r

        if r is not None:
            passes_r, _, _ = resonance_filter_corrected(N)
            g = gcd(r.abs_p, r.abs_q)
            print(f"  {name:>10s}  {N:>4d}  {r.lattice_name:>9s}  "
                  f"({r.p:+4d}, {r.q:3d})  {g:>4d}  "
                  f"{'Y' if r.coprime else 'N':>5s}  {float(r.l_Omega):>10.4f}  "
                  f"{float(r.nu):>10.6f}  {r.k_res:>5d}  {r.delta:>+8.4f}  "
                  f"{'PASS' if passes_r else 'FAIL':>4s}")
        else:
            print(f"  {name:>10s}  {N:>4d}  {sector:>9s}  {'NONE':>12s}")

    # ------------------------------------------------------------------
    # COMPARISON WITH ORIGINAL
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("COMPARISON: ORIGINAL vs CORRECTED RESONANCE")
    print("=" * 80)
    
    original_passes = ['electron', 'up', 'down', 'proton']
    
    corrected_passes = []
    for name, (N, sector) in PARTICLE_EPOCHS.items():
        passes, _, _ = resonance_filter_corrected(N)
        if passes:
            corrected_passes.append(name)
    
    print(f"\n  Original (floor):   {len(original_passes)} particles pass")
    print(f"  Corrected (round):  {len(corrected_passes)} particles pass")
    print(f"")
    print(f"  Original PASS:  {', '.join(original_passes)}")
    print(f"  Corrected PASS: {', '.join(corrected_passes)}")
    
    newly_passing = set(corrected_passes) - set(original_passes)
    if newly_passing:
        print(f"\n  🎉 NOW PASSING: {', '.join(newly_passing)}")
    
    # ------------------------------------------------------------------
    # KEY PARTICLE ANALYSIS
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("KEY PARTICLE DETAILED ANALYSIS")
    print("=" * 80)
    
    key_particles = ['bottom', 'muon', 'tau', 'strange']
    
    for name in key_particles:
        if name in PARTICLE_EPOCHS:
            N, sector = PARTICLE_EPOCHS[name]
            print(f"\n{name.upper()} (N={N}, {sector} sector):")
            
            # Try sector-specific first
            result = find_winding_numbers_corrected(N, sector=sector, verbose=True)
            if result is None:
                print(f"\n  No primitive winding in {sector} lattice, trying universal...")
                result = find_winding_numbers_corrected(N, sector='universal', verbose=True)
            
            if result is not None:
                passes, k_res, delta = resonance_filter_corrected(N)
                print(f"\n  FINAL RESULT:")
                print(f"    Winding: ({result.p}, {result.q}) from {result.lattice_name} lattice")
                print(f"    Resonance: k_res={k_res}, δ={delta:+.4f} → {'PASS' if passes else 'FAIL'}")
                print(f"    Primitive: gcd={gcd(result.abs_p, result.abs_q)} → {'YES' if result.coprime else 'NO'}")
                print(f"    Status: {'✅ FULL SUCCESS' if passes and result.lattice_name == sector else '⚠️ PARTIAL' if passes else '❌ FAIL'}")