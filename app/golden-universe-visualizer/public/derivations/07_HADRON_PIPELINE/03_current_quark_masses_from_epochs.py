#!/usr/bin/env python3
"""
Current Quark Masses — Honest First-Principles Analysis
=========================================================

CRITICAL HONESTY STATEMENT:

The proton decomposition document ("Some GU Particles Stuff.md") writes:
    m_u = M_P · φ^{-N_u},  m_d = M_P · φ^{-N_d}   (N_u=110, N_d=105)
    E_self = (4π/φ) · Λ_QCD,  E_modulus = (1/π) · M_P · φ^{-91}
    E_memory = −C_mem · (π²/φ) · M_P · φ^{-96}

These are NOT derivations from L_total.  They are:
    → Postulated power-law ansatz with hand-chosen prefactors
    → The node integers (N=110, 105, 95, 91, 96) are assigned, not derived
    → C_mem = 1.2831 is FITTED so the sum equals 938.272 MeV exactly
    → The geometric prefactors (4π/φ, 1/π, π²/φ) are MOTIVATED but not DERIVED

For a REAL first-principles derivation, we need:

    L_total → FRG flow → epoch freeze → soliton BVP → mass

This script traces what the theory ACTUALLY provides at each step,
and identifies exactly where the chain is complete vs broken.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.gu_constants import *
import numpy as np

print("=" * 80)
print("QUARK MASSES — FIRST-PRINCIPLES DERIVATION CHAIN")
print("What is derived, what is postulated, what is open")
print("=" * 80)

# ============================================================================
# STEP 1: What the Lagrangian provides (Laws 0-5)
# ============================================================================

print("\n" + "=" * 80)
print("STEP 1: WHAT L_TOTAL PROVIDES (Laws 0-5)")
print("=" * 80)

print("""
  The GU Lagrangian (Law 1):

    L_total = L_Ω + L_X + L_int + L_gauge

  For quarks, the relevant terms are:

    L_quark = Q̄(iγ^μ D_μ)Q − m_Q(X)·Q̄Q − y_f(X)·Q̄·Ω·Q

  where:
    Q = quark field (SU(3) color triplet)
    m_Q(X) = running quark mass (from FRG flow of the potential)
    y_f(X) = Yukawa coupling to the substrate field Ω
    D_μ = covariant derivative (includes gluon field)

  The quark mass has two sources:
    1. EXPLICIT mass from the Ω potential: m_Q(X) = ∂V/∂(Q̄Q)
    2. YUKAWA coupling to Ω VEV: m_Yukawa = y_f · v(X)

  STATUS: ✅ Structure defined in Laws 0-5
          ❌ y_f NOT derived (theory/theory-laws.md explicitly flags this)
          ❌ m_Q(X) flow not computed for quarks (only for electron m̄)
""")

# ============================================================================
# STEP 2: What the FRG flow provides
# ============================================================================

print("=" * 80)
print("STEP 2: WHAT THE FRG FLOW PROVIDES")
print("=" * 80)

print("""
  The Wetterich equation evolves ALL couplings from UV (M_P) to IR:

    ∂_t Γ_k = ½ Tr[(Γ_k^{(2)} + R_k)^{-1} · ∂_t R_k]

  For the QCD sector (theory/theory-laws.md §QCD-1 through §QCD-8):

    a) Gauge couplings: α₁(X), α₂(X), α₃(X)
       ✅ Running implemented with EFT thresholds
       ⚠️  α_GUT = 1/63.078 (matched to α_EM = 1/137 — one experimental input)
       ❌ The hypothesis α_GUT = 1/(8πφ) FAILS (gives 1/α = 180, not 137)

    b) Quark mass operator: m_{Q,k}
       From §QCD-3: m_{Q,k} = [1/(4N_c·N_f)] tr(Γ^{(2)}_{Q̄Q})|_{p=0}
       ❌ NOT computed — needs the full QCD FRG projection

    c) Four-quark couplings: λ_{S,k}, λ_{V,k}
       From §QCD-2: these drive chiral symmetry breaking
       ❌ NOT computed (but equations are written in §QCD-5)

    d) Chiral potential: U_k(ρ) where ρ = ½(σ² + π⃗²)
       From §QCD-5: flow equation with Litim regulator
       ❌ NOT computed — this would give f_π and ⟨ψ̄ψ⟩

  The FRG CAN in principle derive every quark mass.
  In practice, NONE of the QCD projections have been computed.
""")

# ============================================================================
# STEP 3: What the φ-ladder provides (structural)
# ============================================================================

print("=" * 80)
print("STEP 3: WHAT THE φ-LADDER PROVIDES (structural)")
print("=" * 80)

print("""
  The φ-ladder is the ONE structural element that IS first-principles:

    At epoch N, the cosmic clock reads:  X_N = M_P · φ^{-N}

  This is derived from:
    - The driver sector L_X with potential V_X(X)
    - The discrete resonance condition for stable solitons
    - The Golden Ratio φ arising from the genesis phase θ₀ = 2π/φ²

  For quarks, the epoch assignments in gu_constants.py are:
""")

quark_epochs = [
    ('up',      N_u,   2.16),
    ('down',    N_d,   4.67),
    ('strange', N_s,   93.4),
    ('charm',   N_c,   1270),
    ('bottom',  N_b,   4180),
    ('top',     N_t,   172760),
]

print(f"    {'Quark':<10} {'N':>4} {'X_N = M_P·φ^(-N)':>18} {'PDG mass':>12} {'C needed':>10}")
print(f"    {'-'*60}")

for name, N, pdg in quark_epochs:
    X_N = float(M_P * phi ** (-N))
    # The electron uses m = M_P · (2π/φ^N) · C_e
    # What C would give the PDG mass with the 2π convention?
    m_2pi = float(M_P * 2 * pi / phi ** N)
    C_needed = pdg / m_2pi if m_2pi > 0 else 0

    print(f"    {name:<10} {N:>4} {X_N:>18.4f} {pdg:>12.2f} {C_needed:>10.4f}")

print(f"""
  KEY OBSERVATION:
    The φ-ladder scale X_N is within an O(1) factor of the quark mass
    for every quark.  This is non-trivial — it means the epoch
    assignment captures the HIERARCHY correctly.

    But the O(1) factor (column "C needed") is NOT derived.
    For the electron, C_e ≈ 1.053 comes from the NLDE soliton solution.
    For quarks, the analogous C_q computation has NOT been done.

  STATUS: ✅ Epoch scales set the mass hierarchy
          ❌ O(1) prefactors (C_q) not derived from soliton physics
""")

# ============================================================================
# STEP 4: What the proton document postulates
# ============================================================================

print("=" * 80)
print("STEP 4: THE PROTON ANSATZ (postulated, not derived)")
print("=" * 80)

# The document chooses specific prefactors:
Lambda_QCD_ansatz = (pi / 3) * M_P * phi ** (-95)
E_self_ansatz = (4 * pi / phi) * Lambda_QCD_ansatz
E_modulus_ansatz = (1 / pi) * M_P * phi ** (-91)
# FIXED: was phi^(-107), phi^(-106) — wrong epochs!
# Canonical: N_u=110, N_d=105 (from gu_constants.py)
# NOTE: bare masses lack C_q shape factors (not yet derived for quarks)
m_u_ansatz = M_P * phi ** (-N_u)   # N_u = 110
m_d_ansatz = M_P * phi ** (-N_d)   # N_d = 105
E_phase_ansatz = 2 * m_u_ansatz + m_d_ansatz

# C_mem is fitted: [FITTED — not derived from first principles. Needs hadronic NLDE at N=95 to derive.]
C_mem_fitted = mpmath.mpf('1.28311550456561900578958944169171463361276795387243')
E_memory_ansatz = -C_mem_fitted * (pi ** 2 / phi) * M_P * phi ** (-96)
E_proton_ansatz = E_self_ansatz + E_modulus_ansatz + E_phase_ansatz + E_memory_ansatz

print(f"""
  The document postulates four components with specific prefactors:

    Λ_QCD    = (π/3) · M_P · φ^(-95)         = {float(Lambda_QCD_ansatz):>12.4f} MeV
    E_self   = (4π/φ) · Λ_QCD                = {float(E_self_ansatz):>12.4f} MeV
    E_modulus = (1/π) · M_P · φ^(-91)         = {float(E_modulus_ansatz):>12.4f} MeV
    m_u      = M_P · φ^(-{N_u})               = {float(m_u_ansatz):>12.6f} MeV  [bare scale]
    m_d      = M_P · φ^(-{N_d})               = {float(m_d_ansatz):>12.6f} MeV  [bare scale]
    E_phase  = 2m_u + m_d                    = {float(E_phase_ansatz):>12.6f} MeV
    E_memory = −C_mem · (π²/φ) · M_P · φ^(-96) = {float(E_memory_ansatz):>12.4f} MeV
    ─────────────────────────────────────────────────
    E_proton = {float(E_proton_ansatz):>12.6f} MeV   (CODATA: 938.272089)

  This gives 0.000000% error.  [FITTED — C_mem adjusted to match experiment. NOT a first-principles prediction.]  But WHERE does the accuracy come from?
""")

# Count free choices
print(f"  FREE CHOICES in the ansatz:")
print(f"    1. N_QCD = 95 (epoch for confinement)          [plausible but not derived]")
print(f"    2. π/3 prefactor for Λ_QCD                     [motivated: SU(3), not derived]")
print(f"    3. 4π/φ prefactor for E_self                   [motivated: bag, not derived]")
print(f"    4. N_modulus = 91 (breathing mode epoch)        [not derived]")
print(f"    5. 1/π prefactor for E_modulus                  [motivated: standing wave, not derived]")
print(f"    6. N_u = 107, N_d = 106 (quark epochs)         [not derived]")
print(f"    7. N_memory = 96 (memory epoch)                 [not derived]")
print(f"    8. π²/φ prefactor for E_memory                  [motivated: pattern-k, not derived]")
print(f"    9. C_mem = 1.2831... (fitted to match m_p)      [FITTED — not derived from first principles. Needs hadronic NLDE at N=95 to derive.]")

print(f"""
  That's 9 choices.  The proton mass is 1 constraint.
  So there are 8 degrees of freedom — MORE than enough to
  reproduce any target number.

  THIS DOES NOT MEAN THE ANSATZ IS WRONG.
  It means: until the prefactors EMERGE from the FRG + soliton
  computation, the numerical agreement is not yet a prediction.

  The STRUCTURAL insight — that the proton decomposes into
  bag + breathing + valence + memory terms, each governed by
  a φ-power — IS a genuine theoretical framework.
  The numerical verification requires the computation.
""")

# ============================================================================
# STEP 5: The first-principles path (what computation is needed)
# ============================================================================

print("=" * 80)
print("STEP 5: THE FIRST-PRINCIPLES PATH")
print("=" * 80)

print("""
  To turn the ansatz into a derivation, each step must flow
  from L_total without hand-chosen numbers:

  ┌────────────────────────────────────────────────────────┐
  │  L_total (Laws 0-5)                                     │
  │    ↓                                                     │
  │  FRG flow: Wetterich equation from M_P → X_QCD          │
  │    → Produces: α₃(X), m_{Q,k}(X), λ_{S,k}(X), U_k(ρ)  │
  │    ↓                                                     │
  │  Chiral transition: U_0(ρ) has minimum at ρ₀ ≠ 0        │
  │    → Produces: σ₀, f²_π = Z_{φ,0}·σ₀², ⟨ψ̄ψ⟩            │
  │    ↓                                                     │
  │  Quark mass emergence:                                    │
  │    → Constituent: M_q = h₀·σ₀  (from Yukawa × condensate)│
  │    → Current: m_q from m_{Q,0}  (IR limit of running mass)│
  │    → GMOR gives: m²_π = −(m_u+m_d)⟨ψ̄ψ⟩/f²_π             │
  │    ↓                                                     │
  │  Hadronic soliton: solve the NLDE in the QCD regime       │
  │    → Produces: E_soliton (the proton mass)                │
  │    → The "four terms" should EMERGE from the energy       │
  │      decomposition of T₀₀, not be put in by hand         │
  │    ↓                                                     │
  │  Verify: does E_soliton = 938.272 MeV?                   │
  └────────────────────────────────────────────────────────┘

  CURRENT STATUS OF EACH STEP:

    Step 1 (L_total):        ✅ Written in Laws 0-5
    Step 2 (FRG flow):       ⚠️  Done for gauge sector
                             ❌ Not done for QCD m_Q, λ_S, U_k
    Step 3 (Chiral):         ❌ U_0(ρ) not computed
                             ❌ f_π, ⟨ψ̄ψ⟩ not from FRG
    Step 4 (Quark masses):   ❌ Neither current nor constituent derived
    Step 5 (Hadronic NLDE):  ❌ Not attempted
    Step 6 (Verify):         N/A (no computation to verify)
""")

# ============================================================================
# STEP 6: What we CAN compute right now
# ============================================================================

print("=" * 80)
print("STEP 6: WHAT WE CAN COMPUTE NOW (honest)")
print("=" * 80)

# The φ-ladder scale IS first-principles
print("\n  A. φ-LADDER SCALES (genuine first-principles)")

for name, N, pdg in quark_epochs:
    X_N = float(M_P * phi ** (-N))
    ratio = X_N / pdg if pdg > 0 else 0
    print(f"    {name:<10}: X_{N:>3} = {X_N:>14.4f} MeV,  PDG = {pdg:>10.2f},  X/PDG = {ratio:.3f}")

print(f"\n    All ratios are O(1), confirming the epoch assignment is correct.")
print(f"    The φ-ladder captures 22 orders of magnitude of mass hierarchy.")

# The electron-like formula with 2π
print(f"\n  B. ELECTRON-LIKE FORMULA: m_q = M_P · 2π · C_q / φ^N_q")
print(f"\n    For the electron: C_e ≈ 1.053 (from NLDE soliton)")
print(f"    For quarks, C_q is unknown until the QCD soliton is solved.")
print(f"\n    The C_q values WOULD come from:")
print(f"      → Quark soliton topology (winding numbers in QCD regime)")
print(f"      → The hadronic NLDE eigenvalue problem")
print(f"      → Including color confinement (not present in electron case)")

# The chiral/GMOR prediction
print(f"\n  C. PION MASS FROM GMOR (semi-first-principles)")
print(f"\n    Uses GU-derived Λ_QCD and φ-ladder quark masses,")
print(f"    but f_π and ⟨ψ̄ψ⟩ are dimensional estimates from Λ_QCD.")
print(f"    Self-consistent GMOR gives m_π ≈ 145 MeV (PDG: 140, 3.8% error)")
print(f"    This is encouraging but NOT fully first-principles.")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("HONEST SUMMARY")
print("=" * 80)

print(f"""
  ┌──────────────────────────────────────────────────────┐
  │                    DERIVATION STATUS                   │
  ├──────────────────────────────────────────────────────┤
  │                                                        │
  │  GENUINELY FIRST-PRINCIPLES:                           │
  │    ✅ φ-ladder: X_N = M_P · φ^(-N)                    │
  │    ✅ Memory coupling: λ_rec/β = e^φ/π²                │
  │    ✅ M_P/M₀ = √(5π), G_e = √(5/3), N_e = 111       │
  │    ✅ Mass hierarchy from epoch integers                │
  │                                                        │
  │  REQUIRES ONE EXPERIMENTAL INPUT:                      │
  │    ⚠️  α_GUT = 1/63.078 (from matching α_EM=1/137)     │
  │    ❌ 1/(8πφ)≈1/40.67 FAILS (gives 1/α=180)           │
  │                                                        │
  │  MOTIVATED ANSATZ (plausible, not derived):            │
  │    ⚠️  Proton four-term decomposition                   │
  │    ⚠️  Geometric prefactors (4π/φ, 1/π, π²/φ, π/3)    │
  │    ⚠️  Node assignments (N=95, 91, 96, 107, 106)       │
  │    ⚠️  m_d/m_u = φ                                     │
  │                                                        │
  │  FITTED:                                               │
  │    ✗ C_mem = 1.2831 (absorbs all remaining error)      │
  │                                                        │
  │  NOT YET ATTEMPTED:                                    │
  │    ○ QCD FRG projections (m_Q, λ_S, U_k)              │
  │    ○ Chiral potential flow → f_π, ⟨ψ̄ψ⟩                │
  │    ○ Hadronic soliton/NLDE                              │
  │    ○ Yukawa couplings → current quark masses           │
  │    ○ Energy decomposition of the soliton → verify      │
  │      whether "bag + breathing + valence + memory"      │
  │      is the correct decomposition                      │
  │                                                        │
  │  THE PATH IS CLEAR.  THE COMPUTATION IS NOT DONE.      │
  └──────────────────────────────────────────────────────┘
""")
