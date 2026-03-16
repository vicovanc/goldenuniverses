#!/usr/bin/env python3
"""
Golden Universe Constants and Utilities
All fundamental constants derived from π, φ, e
"""

import mpmath
import numpy as np

# Set 50-decimal precision
mpmath.mp.dps = 50

# ============================================================================
# FUNDAMENTAL MATHEMATICAL CONSTANTS
# ============================================================================

# Golden ratio (exact)
phi = mpmath.mpf('1.6180339887498948482045868343656381177203091798057628621354486227')
phi_sq = phi * phi

# Pi (high precision)
pi = mpmath.pi

# Euler's number
e = mpmath.e

# ============================================================================
# DERIVED GU CONSTANTS
# ============================================================================

# Planck mass in MeV
M_P = mpmath.mpf('1.22089e22')  # MeV

# Seeley-DeWitt coefficient from SU(5)+SUSY DOF counting
# Source: derivations/39_GRAVITY/12_g_prim_field_content.py
# n_B - n_F = 188/48 propagating DOF, c_R = (n_B - n_F)/(48*pi) * 48 = 188/(48*pi)
c_R = mpmath.mpf('188') / (48 * pi)  # ≈ 1.2470 (from SU(5)+SUSY, NOT the V2 value 1.25)

# Natural mass unit from induced gravity: M_P^2 = 4*pi*c_R * M_0^2
M_0 = M_P / mpmath.sqrt(4 * pi * c_R)

# FRG initial seed mass
m_0 = M_P / phi_sq  # M_P/φ²

# Genesis mass (White Hole)
Z1_magnitude = M_P / (4 * mpmath.sqrt(pi))

# Genesis phase (Golden angle)
theta_genesis = 2 * pi / phi_sq  # 137.508° in radians

# Memory coupling (CRITICAL - from theory)
lambda_rec_beta = mpmath.exp(phi) / (pi * pi)  # e^φ/π² = 0.51098...

# Proton memory coefficient (DERIVED from Y-junction color-geometry)
# C_mem = π/√(2N_c) where N_c = 3 (SU(3) color)
# Origin: π from flux tube angular integration, √(2N_c) from Wilson loop color averaging
# Matches fitted value 1.2831 to 0.04% (440 ppm)
C_mem_derived = pi / mpmath.sqrt(6)  # = 1.28254983...
C_mem_fitted = mpmath.mpf('1.28311550456561900578958944169171463361276795387243')

# ============================================================================
# PARTICLE EPOCHS (from resonance conditions)
# ============================================================================

# Leptons
N_e = 111   # Electron
N_mu = 99   # Muon
N_tau = 94  # Tau

# Quarks
N_u = 110   # Up
N_d = 105   # Down
N_s = 102   # Strange
N_c = 97    # Charm
N_b = 89    # Bottom
N_t = 81    # Top

# Force unification scales
N_GUT = 67  # Grand unification
N_EW = 89   # Electroweak
N_QCD = 95  # QCD confinement

# Cosmological epochs (from Formation document)
N_BBN = 100       # Big Bang Nucleosynthesis
N_rec = 128       # Recombination (T ~ 1 eV onset)
N_today = 143     # Present epoch (derived from kappa=1.746 + T_CMB, NOT 200)

# Inflationary e-folds (from Topoknot DM dilution, Demonstration Ch.3)
N_efolds = mpmath.mpf('70.5')

# Tick rate (calibrated from QCD and recombination anchors)
# kappa = (n_rec - n_QCD) / ln(T_QCD / T_rec) = 33 / ln(0.16 GeV / 1 eV) ≈ 1.746
kappa_0 = mpmath.mpf('1.746')

# ============================================================================
# WINDING NUMBERS (from energy minimization)
# ============================================================================

# Electron winding (DERIVED, not fitted!)
p_e, q_e = -41, 70  # |p| + |q| = 111

# Topological modulus
nu_topo_e = abs(q_e/phi) / mpmath.sqrt(p_e**2 + (q_e/phi)**2)  # 0.7258...

# Loop length
l_Omega = 2 * pi * mpmath.sqrt(p_e**2 + (q_e/phi)**2)  # 374.503...

# ============================================================================
# COUPLING CONSTANTS
# ============================================================================

# Fine structure constant (ONE required experimental input for calibration)
alpha_EM = mpmath.mpf('1') / mpmath.mpf('137.035999084')  # CODATA 2022

# GUT coupling — calibrated from α_EM via RG running (NOT from first principles)
# WARNING: The hypothesis α_GUT = 1/(8πφ) ≈ 0.02478 FAILS — gives α_EM ≈ 1/180
# (24% wrong). The correct α_GUT must be obtained by running α_EM upward through
# SM thresholds. The value below is from SU(5) one-loop matching:
alpha_GUT = mpmath.mpf('1') / mpmath.mpf('42.0')  # ≈ 0.0238, calibrated from α_EM
_alpha_GUT_HYPOTHESIS = 1 / (8 * pi * phi)  # ≈ 0.02478 — FALSIFIED, kept for reference

# Backward-compatible alias (many scripts import alpha_EM_target)
alpha_EM_target = alpha_EM

# Strong coupling at Z mass (experimental benchmark)
alpha_s_MZ = mpmath.mpf('0.1179')  # CODATA/PDG benchmark

# Weinberg angle at M_Z (experimental benchmark)
sin2_theta_W_exp = mpmath.mpf('0.23122')  # At M_Z scale, experimental

# ============================================================================
# SCALES AND ENERGIES
# ============================================================================

def X_at_epoch(N):
    """Cosmic clock value at epoch N"""
    return M_P * phi**(-N)

# Key scales
X_GUT = X_at_epoch(N_GUT)   # ~ 10^16 GeV
X_EW = X_at_epoch(N_EW)     # ~ 246 GeV
X_QCD = X_at_epoch(N_QCD)   # ~ 200 MeV
X_e = X_at_epoch(N_e)       # ~ 0.511 MeV

# ============================================================================
# PATTERN-K EPOCH LABELS (NOT multiplicative pi^k factors)
# ============================================================================
# Pattern-k is an EPOCH TRIGGER for phase transitions, not a multiplicative
# L_eff = L_0 * pi^k factor. See derivations/33_PATTERN_K/ for full analysis.
# These labels indicate WHICH force activates at which epoch, nothing more.

PATTERN_EM = 0     # Electromagnetic (k=0: U(1)_EM, always active)
PATTERN_WEAK = 1   # Weak force (k=1: SU(2)_L x U(1)_Y -> EWSB at N~80)
PATTERN_STRONG = 2 # Strong force (k=2: SU(3)_c confines at N=95)
PATTERN_GUT = 3    # Grand unified (k=3: SU(5) breaks at N=67)

# DEPRECATED: pi^k is not a derived multiplicative factor.
# Kept for backward compatibility only. Do not use in new code.
def pattern_factor(k):
    """DEPRECATED: Pattern-k is an epoch label, not a multiplicative factor."""
    import warnings
    warnings.warn("pattern_factor(k) is deprecated. Pattern-k is an epoch label, "
                  "not pi^k. See 33_PATTERN_K/.", DeprecationWarning, stacklevel=2)
    return pi**k

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def resonance_quality(N):
    """
    Check resonance N/φ² ≈ integer using CORRECTED rounding.
    
    CRITICAL UPDATE (Feb 2026): Uses round(N/φ²) instead of floor(N/φ²)
    to minimize |δ| as suggested by user insight. This fixes resonance
    failures for particles with δ close to 1.0.
    """
    ratio = N / phi_sq
    k_nearest = round(float(ratio))  # CORRECTED: use round() not floor()
    deviation = abs(ratio - k_nearest)
    quality = float(deviation / k_nearest) if k_nearest > 0 else float('inf')
    return k_nearest, quality

def detuning(N):
    """
    Resonance detuning parameter using CORRECTED rounding.
    Returns δ = N/φ² - round(N/φ²) instead of δ = N/φ² - floor(N/φ²).
    """
    k_res, _ = resonance_quality(N)
    return float(N / phi_sq - k_res)

def find_winding_numbers(N, sector=None):
    """
    Find optimal (p,q) for epoch N using the 4-layer selection algorithm.

    Source: "GU next in line.docx" — 4-layer selection principle:
      Layer 1: Admissibility lattice (sector-specific gauge congruences)
      Layer 2: Resonance closure gate (k_res even, δ < 1/2)
      Layer 3: Primitive winding (gcd(|p|, |q|) = 1)
      Layer 4: Ω-variational minimization (min L_Ω = 2π√(p² + q²/φ²))

    The sector parameter selects which admissibility lattice to use:
      'lepton':    q = 10b, p = 2a + b  (charged-lepton Yukawa congruences)
      'quark':     q = 30s, p = 2t − s  (quark Yukawa congruences)
      'universal': all coprime (p,q) with |p|+q = N  (no lattice restriction)
      None:        auto-select from EPOCH_SECTORS registry

    VALIDATED: Electron (N=111, lepton) → (−41, 70) via lepton lattice + min L_Ω.
    OBSTRUCTION: N=95 (proton) has no primitive winding in any fermion lattice
                 (95=5×19, all lattice candidates have gcd divisible by 5).
    """
    from math import gcd as _gcd

    if sector is None:
        sector = EPOCH_SECTORS.get(N, 'universal')

    def _L_Omega_sq(p, q):
        return float(p)**2 + (float(q) / float(phi))**2

    def _lepton_candidates(N_val):
        for b in range(1, N_val // 10 + 1):
            q = 10 * b
            abs_p = N_val - q
            if abs_p <= 0:
                continue
            for sign in [+1, -1]:
                p = sign * abs_p
                if (p - b) % 2 == 0:
                    yield (p, q)

    def _quark_candidates(N_val):
        for s in range(1, N_val // 30 + 1):
            q = 30 * s
            abs_p = N_val - q
            if abs_p <= 0:
                continue
            for sign in [+1, -1]:
                p = sign * abs_p
                if (p + s) % 2 == 0:
                    yield (p, q)

    def _universal_candidates(N_val):
        for abs_p in range(1, N_val):
            yield (-abs_p, N_val - abs_p)

    generators = {
        'lepton': _lepton_candidates,
        'quark': _quark_candidates,
        'universal': _universal_candidates,
    }

    def _search(sec):
        gen = generators[sec]
        best_L_sq = float('inf')
        best_p, best_q = None, None
        for p, q in gen(N):
            if _gcd(abs(p), abs(q)) != 1:
                continue
            L_sq = _L_Omega_sq(p, q)
            if L_sq < best_L_sq:
                best_L_sq = L_sq
                best_p, best_q = p, q
        if best_p is not None and best_p > 0:
            best_p = -best_p
        return best_p, best_q

    p, q = _search(sector)

    if p is None and sector != 'universal':
        p, q = _search('universal')

    if p is None:
        raise ValueError(f"No valid winding numbers for N={N}")

    return p, q


EPOCH_SECTORS = {
    111: 'lepton',   # electron
    99:  'lepton',   # muon
    94:  'lepton',   # tau
    110: 'quark',    # up
    105: 'quark',    # down
    102: 'quark',    # strange
    97:  'quark',    # charm
    89:  'quark',    # bottom
    81:  'quark',    # top
    95:  'universal', # proton/QCD — no primitive winding in fermion lattices
}

def calculate_nu(p, q):
    """Topological modulus from winding numbers"""
    return abs(q/phi) / mpmath.sqrt(p**2 + (q/phi)**2)

# ============================================================================
# MEMORY FUNCTIONS (CLOSED — see theory/GU_COSMOLOGICAL_CLOSURE.md)
# ============================================================================

def beta_X(X):
    """Memory decay rate: beta(X) = X (the running scale).
    Canonical throughout the codebase — tau_mem = 1/X = Compton time."""
    return X

def lambda_rec_X(X):
    """Recursive coupling: lambda_rec(X) = X * e^phi/pi^2 (Law 32 + beta=X)."""
    return X * lambda_rec_beta

def tau_mem(X):
    """Memory relaxation time: tau = 1/beta = 1/X."""
    return 1 / X

def memory_kernel(t, X):
    """Memory decay kernel G(X; t, tau) = exp(-beta(X) * t) = exp(-X * t)."""
    return mpmath.exp(-beta_X(X) * t)

def memory_accumulation(m_bar_history, dt):
    """Calculate accumulated memory"""
    R_mem = 0
    for i, m in enumerate(m_bar_history):
        R_mem += m**4 * dt
    return R_mem

# ============================================================================
# CODATA REFERENCE VALUES (for validation)
# ============================================================================

CODATA = {
    'electron': 0.51099895069,    # MeV
    'muon': 105.6583755,          # MeV
    'tau': 1776.86,               # MeV
    'proton': 938.27208816,       # MeV
    'neutron': 939.56542052,      # MeV
    'W': 80379,                   # MeV
    'Z': 91187.6,                 # MeV
    'Higgs': 125100,              # MeV
    'top': 172760,                # MeV
    'alpha': 0.0072973525693,     # Fine structure
    'sin2_theta_W': 0.23122,      # Weinberg angle
}

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def print_constants():
    """Display all fundamental constants"""
    print("="*60)
    print("GOLDEN UNIVERSE FUNDAMENTAL CONSTANTS")
    print("="*60)

    print("\n### Mathematical Constants:")
    print(f"φ = {float(phi):.10f}")
    print(f"π = {float(pi):.10f}")
    print(f"e = {float(e):.10f}")

    print("\n### Mass Scales:")
    print(f"M_P = {float(M_P):.3e} MeV")
    print(f"c_R = 188/(48π) = {float(c_R):.6f}  (SU(5)+SUSY DOF)")
    print(f"M_0 = M_P/√(4πc_R) = {float(M_0):.3e} MeV")
    print(f"m_0 = M_P/φ² = {float(m_0):.3e} MeV")

    print("\n### Electron Parameters:")
    print(f"N_e = {N_e}")
    print(f"(p,q) = ({p_e}, {q_e})")
    print(f"ν_topo = {float(nu_topo_e):.6f}")
    print(f"l_Ω = {float(l_Omega):.3f}")

    print("\n### Coupling Constants:")
    print(f"α_EM = 1/137.036 = {float(alpha_EM):.8f}  (ONE experimental input)")
    print(f"α_GUT = {float(alpha_GUT):.6f}  (calibrated from α_EM via RG)")
    print(f"  [FALSIFIED hypothesis: 1/(8πφ) = {float(_alpha_GUT_HYPOTHESIS):.6f} → α_EM ≈ 1/180]")

    print("\n### Key Epochs:")
    print(f"N_GUT = {N_GUT} → X = {float(X_GUT):.3e} MeV")
    print(f"N_EW = {N_EW} → X = {float(X_EW):.3e} MeV")
    print(f"N_QCD = {N_QCD} → X = {float(X_QCD):.3f} MeV")
    print(f"N_e = {N_e} → X = {float(X_e):.3f} MeV")
    print(f"N_today = {N_today} (derived from κ={float(kappa_0)}, T_CMB)")
    print(f"N_efolds = {float(N_efolds)} (from TK DM dilution)")
    print(f"κ₀ = {float(kappa_0)}")

if __name__ == "__main__":
    print_constants()

    print("\n### Resonance Check:")
    for name, N in [('electron', 111), ('GUT', 67), ('QCD', 95)]:
        k, quality = resonance_quality(N)
        print(f"{name:8s}: N={N:3d} → {N}/φ² = {k} + {quality:.1%}")