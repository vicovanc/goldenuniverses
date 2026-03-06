#!/usr/bin/env python3
"""
GENERAL WINDING NUMBER SOLVER — 4-LAYER SELECTION ALGORITHM
=============================================================

Derives the optimal winding numbers (p, q) for any epoch N on the SU(5) Omega-torus.

SOURCE: "GU next in line.docx", Sections A–E, validated against the electron at N=111.

THE 4-LAYER ALGORITHM:
  Layer 1 — Admissibility lattice (sector-specific gauge congruences)
            Charged-lepton Yukawa:  q = 10b, p = 2a + b       generators (2,0), (1,10)
            Quark Yukawa:           q = 30s, p = 2t − s       generators (2,0), (−1,30)
  Layer 2 — Resonance closure (discrete crystallization gate)
            k_res = round(N/φ²), δ = N/φ² − k_res  [CORRECTED Feb 2026]
            Accept iff k_res is even AND |δ| < 1/2
  Layer 3 — Primitive winding
            gcd(|p|, |q|) = 1  (primitive geodesic on the torus)
  Layer 4 — Ω-variational minimization (cheapest representative)
            Minimize  L_Ω(p,q) = 2π √(p² + q²/φ²)
            among all candidates surviving Layers 1–3.

VALIDATION: Reproduces (p, q) = (−41, 70) for the electron at N = 111
            via the lepton lattice + L_Ω minimization.

KEY FINDING: N=95 (proton/QCD) has NO primitive winding in any fermion lattice.
             95 = 5 × 19, and all lattice candidates have gcd divisible by 5.
             This means the proton's winding structure (if applicable) comes from
             a different topological sector (gluonic/confining) — an open question.

Date: February 2026
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
# LAYER 1: ADMISSIBILITY LATTICES
# ============================================================================

class AdmissibilityLattice:
    """Base class for sector-specific gauge-congruence lattices."""
    name = "base"

    def generate_candidates(self, N):
        """Yield all (p, q) in this lattice with |p| + |q| = N."""
        raise NotImplementedError


class LeptonLattice(AdmissibilityLattice):
    """
    Charged-lepton admissible winding lattice.

    From the SM Yukawa coupling L × e_R with gauge quantum numbers:
      Left  (L):   T=1/2, Y=−1  →  I_W=1/2,  I_B=(3/5)(Y/2)² = 3/20
      Right (e_R): T=0,   Y=−2  →  I_B=(3/5)(Y/2)² = 3/5

    Congruences (with κ_W = κ_B = κ_GUT from SU(5)):
      Left:  (1/2)p + (3/20)q ∈ Z
      Right: (3/5)q ∈ Z

    Solution: q = 10b, p = 2a + b, for a, b ∈ Z.
    Generators: (2, 0) and (1, 10).
    """
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
    """
    Quark admissible winding lattice.

    From the SM Yukawa couplings Q_L × u_R and Q_L × d_R:
      Q_L:  T=1/2, Y=1/3   →  I_W=1/2,  I_B=(3/5)(1/6)² = 1/60
      u_R:  T=0,   Y=4/3   →  I_B=(3/5)(2/3)² = 4/15
      d_R:  T=0,   Y=−2/3  →  I_B=(3/5)(1/3)² = 1/15

    Up-type congruences:
      Right: (4/15)q ∈ Z  →  q = 15n/4  →  (need integer q)  →  q = 30s
      Left:  30p + 15(2s) ≡ 0 (mod 60)  →  p + s ≡ 0 (mod 2)  →  p = 2t − s

    Down-type gives the same lattice structure.
    Solution: q = 30s, p = 2t − s, for s, t ∈ Z.
    Generators: (2, 0) and (−1, 30).
    """
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
    """
    Universal geometric mode — no gauge-congruence restriction.

    Used as a fallback when the sector-specific lattice is unknown
    (e.g., gluonic/confining sector for composite particles).
    Searches ALL integer (p, q) with |p| + q = N, q > 0.
    """
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
# LAYER 2: RESONANCE CLOSURE FILTER
# ============================================================================

def resonance_filter(N):
    """
    CORRECTED resonance crystallization gate using proper rounding.

    x = N/φ²,  k_res = round(x),  δ = x − k_res
    Accept iff  k_res is even  AND  |δ| < 1/2.

    CRITICAL FIX (Feb 2026): Uses round() instead of floor() to minimize |δ|.
    This fixes resonance failures for particles with δ close to 1.0.

    Returns (passes, k_res, delta).
    """
    x = float(mpf(N) / phi_sq)
    k_res = round(x)  # CORRECTED: use round() instead of int(x)
    delta = x - k_res
    passes = (k_res % 2 == 0) and (abs(delta) < 0.5)  # CORRECTED: use |δ|
    return passes, k_res, delta


# ============================================================================
# LAYER 3: PRIMITIVE WINDING (coprimality)
# ============================================================================

def is_primitive(p, q):
    """gcd(|p|, |q|) = 1 — primitive geodesic on the torus."""
    return gcd(abs(p), abs(q)) == 1


# ============================================================================
# LAYER 4: Ω-VARIATIONAL MINIMIZATION
# ============================================================================

def L_Omega(p, q):
    """
    Ω-geodesic length on the anisotropic torus:
      L_Ω(p,q) = 2π √(p² + q²/φ²)

    The system selects the minimum L_Ω among surviving candidates
    (cheapest / lowest-tension configuration).
    """
    return 2 * pi * sqrt(mpf(p)**2 + (mpf(q) / phi)**2)


# ============================================================================
# WINDING RESULT
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

        k_res_exact = mpf(N) / phi_sq
        self.k_res = round(float(k_res_exact))  # CORRECTED: use round() not floor()
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
# MAIN SOLVER
# ============================================================================

def find_winding_numbers(N, sector='lepton', require_primitive=True, verbose=False):
    """
    Find the optimal winding numbers (p, q) for epoch N using the 4-layer algorithm.

    Layer 1: Generate candidates from sector-specific admissibility lattice.
    Layer 2: Check resonance closure (informational — does not filter candidates).
    Layer 3: Require gcd(|p|, |q|) = 1 (primitive winding) if require_primitive=True.
    Layer 4: Among survivors, select the (p, q) with minimum L_Ω.

    Args:
        N:       epoch number (positive integer)
        sector:  'lepton', 'quark', or 'universal'
        require_primitive: if True, enforce gcd(|p|, q) = 1
        verbose: print candidate evaluation details

    Returns:
        WindingResult with all derived quantities, or None if no candidate found.
    """
    lattice = LATTICES[sector]

    res_passes, k_res, delta = resonance_filter(N)

    if verbose:
        print(f"\n  Epoch N = {N},  sector = {sector}")
        print(f"  Resonance: x = N/φ² = {N/float(phi_sq):.6f},  k_res = {k_res},  "
              f"δ = {delta:.6f}")
        print(f"  Resonance gate: k_res even = {k_res % 2 == 0},  δ < 0.5 = {delta < 0.5}"
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


def find_winding_universal(N, verbose=False):
    """
    Fallback: find winding numbers using universal geometric mode.
    Searches ALL coprime (p, q) with |p| + q = N, minimizes L_Ω.
    """
    return find_winding_numbers(N, sector='universal', require_primitive=True, verbose=verbose)


# ============================================================================
# DISPLAY
# ============================================================================

def print_result(result, indent=""):
    """Print a WindingResult with full detail."""
    if result is None:
        print(f"{indent}No winding numbers found.")
        return

    r = result
    print(f"{indent}Epoch N = {r.N}  (lattice: {r.lattice_name})")
    print(f"{indent}  Winding numbers:  (p, q) = ({r.p}, {r.q})")
    print(f"{indent}  Coprime:          gcd(|p|,q) = {gcd(r.abs_p, r.abs_q)}  "
          f"({'primitive' if r.coprime else 'NOT primitive'})")
    print(f"{indent}  Resonance:        k_res = {r.k_res},  δ = {r.delta:.6f}")
    k_even = r.k_res % 2 == 0
    d_ok = r.delta < 0.5
    print(f"{indent}  Resonance gate:   k_res even = {k_even},  δ < 0.5 = {d_ok}  "
          f"→  {'PASS' if k_even and d_ok else 'FAIL'}")
    print(f"{indent}  Topological modulus:  ν = {float(r.nu):.10f}")
    print(f"{indent}  Ω-geodesic length:   L_Ω = {float(r.l_Omega):.6f}")
    print(f"{indent}  Torus radius:        R = {float(r.R):.6f}")
    print(f"{indent}  Kink amplitude:      Λ₁ = {float(r.Lambda1):.6e}")
    print(f"{indent}  Instanton action:    S_topo = {r.S_topo:.6f}")
    print(f"{indent}  Closure parameter:   μ = 4K(ν)/L_Ω = {float(r.mu_closure):.10f}")
    print(f"{indent}  Elliptic K(ν):       {float(r.K_nu):.10f}")
    print(f"{indent}  Elliptic E(ν):       {float(r.E_nu):.10f}")
    print(f"{indent}  Modular defect:      1 − E/K = {r.mod_defect:.10f}")


# ============================================================================
# EPOCH REGISTRY
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
# MAIN: VALIDATION AND FULL EPOCH SCAN
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("GENERAL WINDING NUMBER SOLVER — 4-LAYER ALGORITHM")
    print("Source: GU next in line.docx")
    print("=" * 80)

    # ------------------------------------------------------------------
    # VALIDATION: Electron at N = 111 via lepton lattice
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("VALIDATION: ELECTRON (N = 111) via LEPTON LATTICE")
    print("Must reproduce (p, q) = (-41, 70) by L_Ω minimization")
    print("=" * 80)

    electron = find_winding_numbers(111, sector='lepton', verbose=True)
    print()
    print_result(electron)

    assert electron is not None, "VALIDATION FAILED: no candidate found"
    assert electron.p == -41 and electron.q == 70, \
        f"VALIDATION FAILED: got ({electron.p}, {electron.q}), expected (-41, 70)"
    print(f"\n  *** VALIDATION PASSED: (p, q) = ({electron.p}, {electron.q}) ***")

    nu_expected = 0.725777
    l_Omega_expected = 374.50
    assert abs(float(electron.nu) - nu_expected) < 0.001, \
        f"nu mismatch: {float(electron.nu)} vs {nu_expected}"
    assert abs(float(electron.l_Omega) - l_Omega_expected) < 0.1, \
        f"l_Omega mismatch: {float(electron.l_Omega)} vs {l_Omega_expected}"
    print(f"  Cross-checks passed: ν ≈ {nu_expected}, L_Ω ≈ {l_Omega_expected}")

    # ------------------------------------------------------------------
    # PROTON at N = 95: demonstrate the lattice obstruction
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("PROTON / QCD (N = 95): LATTICE OBSTRUCTION ANALYSIS")
    print("=" * 80)

    passes, k_res, delta = resonance_filter(95)
    print(f"\n  Resonance filter for N=95: k_res={k_res}, δ={delta:.6f}")
    print(f"  k_res even = {k_res % 2 == 0}, δ < 0.5 = {delta < 0.5}  →  {'PASS' if passes else 'FAIL'}")

    print(f"\n  --- Lepton lattice at N=95 ---")
    lep_95 = find_winding_numbers(95, sector='lepton', require_primitive=True, verbose=True)
    if lep_95 is None:
        print("  RESULT: No primitive winding in lepton lattice at N=95")

    print(f"\n  --- Quark lattice at N=95 ---")
    qrk_95 = find_winding_numbers(95, sector='quark', require_primitive=True, verbose=True)
    if qrk_95 is None:
        print("  RESULT: No primitive winding in quark lattice at N=95")

    print(f"\n  95 = 5 × 19.  Both lattices force q ∈ {{10k}} or {{30k}},")
    print(f"  so all candidates have gcd(|p|, q) divisible by 5.")
    print(f"  => N=95 is NOT accessible as a primitive winding in any fermion lattice.")

    print(f"\n  --- Universal geometric fallback at N=95 ---")
    proton_univ = find_winding_universal(95, verbose=True)
    print()
    print_result(proton_univ, indent="  ")

    # ------------------------------------------------------------------
    # FULL EPOCH TABLE
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("FULL EPOCH TABLE — All known particle epochs")
    print("=" * 80)
    print(f"\n  {'Particle':>10s}  {'N':>4s}  {'Sector':>9s}  {'(p, q)':>12s}  "
          f"{'gcd':>4s}  {'prim':>5s}  {'L_Ω':>10s}  {'ν':>10s}  "
          f"{'k_res':>5s}  {'δ':>8s}  {'res':>4s}")
    print("  " + "-" * 105)

    results_table = {}
    for name, (N, sector) in sorted(PARTICLE_EPOCHS.items(), key=lambda x: -x[1][0]):
        r = find_winding_numbers(N, sector=sector)
        if r is None:
            r = find_winding_universal(N)
        results_table[name] = r

        if r is not None:
            passes_r, _, _ = resonance_filter(N)
            g = gcd(r.abs_p, r.abs_q)
            print(f"  {name:>10s}  {N:>4d}  {r.lattice_name:>9s}  "
                  f"({r.p:+4d}, {r.q:3d})  {g:>4d}  "
                  f"{'Y' if r.coprime else 'N':>5s}  {float(r.l_Omega):>10.4f}  "
                  f"{float(r.nu):>10.6f}  {r.k_res:>5d}  {r.delta:>+8.4f}  "
                  f"{'PASS' if passes_r else 'FAIL':>4s}")
        else:
            print(f"  {name:>10s}  {N:>4d}  {sector:>9s}  {'NONE':>12s}")

    # ------------------------------------------------------------------
    # SHAPE FACTOR COMPARISON (electron vs proton)
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("SHAPE FACTOR COMPARISON (Route A elliptic formula)")
    print("=" * 80)

    def Ce_route_A(nu, delta_val):
        """Route A elliptic formula (Law 33) applied at any epoch."""
        K = ellipk(nu)
        E = ellipe(nu)
        return abs(delta_val) * K + nu / 2 - lambda_rec_beta * (K - E) / 3 + alpha_EM / (2 * pi)

    if electron is not None and proton_univ is not None:
        C_e = Ce_route_A(electron.nu, electron.delta)
        C_h = Ce_route_A(proton_univ.nu, proton_univ.delta)
        print(f"\n  C_e(ν_e, δ_e) = {float(C_e):.10f}  (electron)")
        print(f"  C_h(ν_h, δ_h) = {float(C_h):.10f}  (proton, universal fallback)")
        print(f"  C_mem (fitted) = 1.2833")
        print(f"  C_h / C_mem    = {float(C_h) / 1.2833:.6f}")

    # ------------------------------------------------------------------
    # STEP VECTOR ANALYSIS: Why exactly ΔN = 11 and 17
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP VECTOR ANALYSIS — Why only ΔN ∈ {11, 17}")
    print("from the lepton lattice ladder {11, 13, 15, 17, 19, ...}")
    print("=" * 80)

    print("\n  Lepton lattice step vectors: (Δp, Δq) = (2a±1, 10)")
    print("  ΔN = |2a±1| + 10 ∈ {11, 13, 15, 17, 19, ...}")
    print()
    print(f"  {'ΔN':>4s}  {'(Δp,10)':>10s}  {'gcd':>4s}  "
          f"{'k_res':>5s}  {'even':>5s}  {'δ':>8s}  {'δ<½':>5s}  "
          f"{'prim':>5s}  {'result':>10s}")
    print("  " + "-" * 70)

    for a in range(10):
        dp = 2 * a + 1
        dN = dp + 10
        x = float(mpf(dN) / phi_sq)
        k = int(x)
        d = x - k
        g = gcd(dp, 10)
        k_even = k % 2 == 0
        d_ok = d < 0.5
        prim = g == 1
        survives = k_even and d_ok and prim
        print(f"  {dN:>4d}  ({dp:>3d}, 10)  {g:>4d}  "
              f"{k:>5d}  {str(k_even):>5s}  {d:>8.4f}  {str(d_ok):>5s}  "
              f"{str(prim):>5s}  {'SURVIVES' if survives else '':>10s}")

    print()
    print("  RESULT: First two surviving steps are ΔN = 11 and ΔN = 17.")
    print("    ΔN=13: killed by resonance (δ = 0.97 > 0.5)")
    print("    ΔN=15: killed by coprimality (gcd(5,10) = 5)")
    print("    ΔN=19: killed by resonance (k_res = 7, odd)")
    print("  Third survivor: ΔN = 21 → hypothetical 4th lepton family.")
    print("  The kink spectral filter (only 3 Pöschl-Teller bound states")
    print("  exist for ν ∈ {1, 3/2, 2}) prevents the 4th family.")

    # ------------------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("""
  4-LAYER SELECTION ALGORITHM (from source document):
    Layer 1: Admissibility lattice (gauge congruences → sector-specific)
    Layer 2: Resonance closure (k_res even, δ < 1/2)
    Layer 3: Primitive winding (gcd(|p|, |q|) = 1)
    Layer 4: Ω-variational minimization (min L_Ω = 2π√(p² + q²/φ²))

  ELECTRON (N=111, lepton lattice):
    Lepton lattice + min L_Ω  →  (−41, 70)   VALIDATED

  STEP VECTORS (lepton family structure):
    Resonance + coprimality selects ΔN ∈ {11, 17} from {11,13,15,17,...}
    Kink spectral filter (3 Pöschl-Teller modes) prevents 4th family (ΔN=21)

  PROTON (N=95):
    Neither lepton nor quark lattice admits a primitive winding at N=95.
    95 = 5 × 19; all lattice candidates have gcd divisible by 5.
    The proton is composite — its mass comes from QCD confinement (α_s running),
    not from winding numbers on the Ω-torus. The 4-layer algorithm applies to
    fundamental fermions through their Yukawa couplings, not to hadrons.
""")
