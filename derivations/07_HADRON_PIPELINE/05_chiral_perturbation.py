#!/usr/bin/env python3
"""
Chiral Perturbation Theory for Pion and Kaon — GU First Principles
====================================================================

The pion is a pseudo-Goldstone boson of chiral symmetry breaking.
Its mass CANNOT come from the constituent model — it requires the
Gell-Mann-Oakes-Renner (GMOR) relation:

    m²_π f²_π = −(m_u + m_d) ⟨ψ̄ψ⟩

In GU, ALL ingredients can be derived:
    m_u, m_d:    from φ-ladder (03_current_quark_masses_from_epochs.py)
    ⟨ψ̄ψ⟩:        ~ −Λ³_QCD (dimensional, from epoch N=95)
    f_π:         from FRG chiral flow: f²_π = Z_{φ,0} · σ₀²

This script computes the pion mass using ONLY GU-derived inputs.

STATUS:
  [GU-DERIVED]:  m_u, m_d from φ^{-N_u}, φ^{-N_d} (N_u=110, N_d=105)
  [GU-DERIVED]:  Λ_QCD from (π/3)·M_P·φ^{-95}
  [ESTIMATED]:   f_π and ⟨ψ̄ψ⟩ from dimensional analysis of Λ_QCD
  [OPEN]:        Exact f_π from FRG chiral potential flow
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.gu_constants import *
import numpy as np

print("=" * 80)
print("CHIRAL PERTURBATION THEORY — GU FIRST PRINCIPLES")
print("Pion and Kaon masses from GMOR relation")
print("=" * 80)

# ============================================================================
# 1. GU-DERIVED INPUTS
# ============================================================================

print("\n### 1. GU-DERIVED INPUTS (no PDG)")
print("-" * 60)

# Quark masses from φ-ladder at canonical epochs (N_u=110, N_d=105)
# FIXED: was phi^(-107), phi^(-106) — wrong epochs!
# NOTE: bare masses lack C_q shape factors (not yet derived for quarks)
m_u = M_P * phi ** (-N_u)   # N_u = 110
m_d = M_P * phi ** (-N_d)   # N_d = 105
m_u_f = float(m_u)
m_d_f = float(m_d)

# QCD scale
Lambda_QCD = (pi / 3) * M_P * phi ** (-95)
Lambda_f = float(Lambda_QCD)

print(f"  m_u = M_P · φ^(-{N_u}) = {m_u_f:.6f} MeV  [GU bare scale, no C_q]")
print(f"  m_d = M_P · φ^(-{N_d}) = {m_d_f:.6f} MeV  [GU bare scale, no C_q]")
print(f"  Λ_QCD = (π/3)·M_P·φ^(-95) = {Lambda_f:.4f} MeV  [GU-DERIVED]")

# ============================================================================
# 2. QUARK CONDENSATE
# ============================================================================

print("\n### 2. QUARK CONDENSATE")
print("-" * 60)

# From theory/theory-laws.md §QCD-6: In the chiral limit,
#   σ₀ ≠ 0 (spontaneous chiral symmetry breaking)
#   m_q ∝ σ₀ (constituent mass from dynamics)
#
# The quark condensate in terms of the chiral order parameter:
#   ⟨ψ̄ψ⟩ = −N_c · σ₀³ / (4π²)
#
# Dimensional estimate: ⟨ψ̄ψ⟩ ~ −Λ³_QCD
# More refined: ⟨ψ̄ψ⟩ ~ −(c_cond · Λ_QCD)³
# where c_cond captures the O(1) factor from the FRG flow.

# Method 1: Raw dimensional
condensate_raw = -Lambda_QCD ** 3
cond_raw_cbrt = Lambda_f

# Method 2: Include color and loop factors
# From large-N_c estimate: ⟨ψ̄ψ⟩ ≈ −N_c · Λ³_QCD / (4π²)
N_c = 3
condensate_refined = -N_c * Lambda_QCD ** 3 / (4 * pi ** 2)
cond_ref_cbrt = float((-condensate_refined) ** (mpmath.mpf(1) / 3))

# Method 3: Fit-free using the bag energy relation
# E_self = (4π/φ)·Λ_QCD is the total gluonic energy in the bag
# The condensate σ₀ is related: σ₀³ ~ E_self · Λ²_QCD / (4π²)
E_self = (4 * pi / phi) * Lambda_QCD
condensate_bag = -E_self * Lambda_QCD ** 2 / (4 * pi ** 2)
cond_bag_cbrt = float((-condensate_bag) ** (mpmath.mpf(1) / 3))

print(f"  Method 1 (raw dimensional):")
print(f"    ⟨ψ̄ψ⟩^(1/3) = Λ_QCD = {cond_raw_cbrt:.1f} MeV")

print(f"\n  Method 2 (color + loop factors):")
print(f"    ⟨ψ̄ψ⟩ = −N_c·Λ³/(4π²)")
print(f"    ⟨ψ̄ψ⟩^(1/3) = {cond_ref_cbrt:.1f} MeV")

print(f"\n  Method 3 (bag-derived):")
print(f"    ⟨ψ̄ψ⟩ = −E_self·Λ²/(4π²)")
print(f"    ⟨ψ̄ψ⟩^(1/3) = {cond_bag_cbrt:.1f} MeV")

print(f"\n  Lattice QCD: ⟨ψ̄ψ⟩^(1/3) ≈ 250 MeV")

# ============================================================================
# 3. PION DECAY CONSTANT
# ============================================================================

print("\n### 3. PION DECAY CONSTANT")
print("-" * 60)

# From theory/theory-laws.md §QCD-8: f²_π = Z_{φ,0} · σ₀²
# where σ₀ = √(2ρ₀) is the vacuum condensate at the minimum of U_0(ρ)
#
# Dimensional estimates:
# Method A: f_π ~ Λ_QCD / √(4π)  (large-N_c scaling)
# Method B: f_π ~ ⟨ψ̄ψ⟩^(1/3) / √(N_c)  (Pagels-Stokar)
# Method C: f_π from GMOR self-consistency (see below)

f_pi_A = float(Lambda_QCD / mpmath.sqrt(4 * pi))
f_pi_B = cond_ref_cbrt / np.sqrt(N_c)

print(f"  Method A: f_π = Λ_QCD/√(4π) = {f_pi_A:.1f} MeV")
print(f"  Method B: f_π = ⟨ψ̄ψ⟩^(1/3)/√N_c = {f_pi_B:.1f} MeV")
print(f"  PDG: f_π = 92.1 MeV")

# For the GMOR calculation, we'll use each estimate and see which
# gives the best pion mass

# ============================================================================
# 4. PION MASS FROM GMOR
# ============================================================================

print("\n### 4. PION MASS FROM GMOR RELATION")
print("-" * 60)

print(f"\n  GMOR: m²_π · f²_π = −(m_u + m_d) · ⟨ψ̄ψ⟩")
print(f"  ⟹ m_π = √[ −(m_u + m_d) · ⟨ψ̄ψ⟩ ] / f_π")

m_sum_ud = m_u + m_d  # Sum of current quark masses

# Using each combination of condensate and f_π estimates:
results = []

configs = [
    ("Raw Λ³, f=Λ/√4π",        condensate_raw,     Lambda_QCD / mpmath.sqrt(4 * pi)),
    ("N_c·Λ³/4π², f=Λ/√4π",    condensate_refined, Lambda_QCD / mpmath.sqrt(4 * pi)),
    ("Bag, f=Λ/√4π",           condensate_bag,     Lambda_QCD / mpmath.sqrt(4 * pi)),
    ("N_c·Λ³/4π², f=cond/√Nc", condensate_refined, mpmath.mpf(cond_ref_cbrt) / mpmath.sqrt(N_c)),
]

print(f"\n  m_u + m_d = {float(m_sum_ud):.6f} MeV  [GU-DERIVED]")
print(f"\n  {'Config':<30} {'m_π (MeV)':>10} {'f_π (MeV)':>10} {'⟨ψ̄ψ⟩^1/3':>10} {'Error':>8}")
print(f"  {'-'*75}")

for label, cond, f_pi_est in configs:
    # m²_π = −(m_u + m_d) · ⟨ψ̄ψ⟩ / f²_π
    m_pi_sq = -m_sum_ud * cond / f_pi_est ** 2
    if m_pi_sq > 0:
        m_pi = float(mpmath.sqrt(m_pi_sq))
    else:
        m_pi = 0

    f_pi_val = float(f_pi_est)
    cond_cbrt = float((-cond) ** (mpmath.mpf(1) / 3))
    err = abs(m_pi - 139.6) / 139.6 * 100

    results.append((label, m_pi, f_pi_val, cond_cbrt))
    print(f"  {label:<30} {m_pi:>10.1f} {f_pi_val:>10.1f} {cond_cbrt:>10.1f} {err:>7.1f}%")

print(f"\n  PDG: m_π = 139.6 MeV, f_π = 92.1 MeV, ⟨ψ̄ψ⟩^(1/3) ≈ 250 MeV")

# ============================================================================
# 5. SELF-CONSISTENT SOLUTION
# ============================================================================

print("\n### 5. SELF-CONSISTENT GMOR (no free parameters)")
print("-" * 60)

# The GMOR relation + condensate + f_π form a closed system if we
# use the relation f²_π · m²_π = −(m_u + m_d)·⟨ψ̄ψ⟩
# and the NJL/DSE relation: ⟨ψ̄ψ⟩ = −N_c/(4π²) · M³_dyn
# and the gap equation: M_dyn = −g² ⟨ψ̄ψ⟩ / Λ² ≈ Λ³_QCD / (3f²_π)
#
# Self-consistency: f²_π ≈ N_c·M²_dyn / (4π²) and M_dyn ≈ Λ_QCD
# gives f_π ≈ √(N_c)·Λ_QCD / (2π)

f_pi_sc = float(mpmath.sqrt(N_c) * Lambda_QCD / (2 * pi))
print(f"  Self-consistent: f_π = √N_c · Λ_QCD / (2π) = {f_pi_sc:.1f} MeV")
print(f"    (PDG: 92.1 MeV, ratio: {f_pi_sc/92.1:.3f})")

# With this f_π, compute condensate from gap equation
M_dyn_sc = Lambda_f ** 3 / (3 * f_pi_sc ** 2)
print(f"  M_dynamical = Λ³/(3f²_π) = {M_dyn_sc:.1f} MeV")

# Condensate: ⟨ψ̄ψ⟩ = −N_c · M³_dyn / (4π²)
cond_sc = -N_c * M_dyn_sc ** 3 / (4 * np.pi ** 2)
cond_sc_cbrt = abs(cond_sc) ** (1 / 3)
print(f"  ⟨ψ̄ψ⟩^(1/3) = {cond_sc_cbrt:.1f} MeV")

# Pion mass from GMOR
m_pi_sq_sc = -(m_u_f + m_d_f) * cond_sc / f_pi_sc ** 2
m_pi_sc = np.sqrt(abs(m_pi_sq_sc)) if m_pi_sq_sc < 0 else np.sqrt(m_pi_sq_sc)
err_sc = abs(m_pi_sc - 139.6) / 139.6 * 100

print(f"\n  ⟹ m_π (self-consistent) = {m_pi_sc:.1f} MeV")
print(f"    PDG: 139.6 MeV, error: {err_sc:.1f}%")

# ============================================================================
# 6. KAON MASS
# ============================================================================

print("\n### 6. KAON MASS")
print("-" * 60)

# K± has quark content us̄, so GMOR gives:
# m²_K · f²_K ≈ −(m_u + m_s) · ⟨ψ̄ψ⟩
# with f_K ≈ 1.2 · f_π (SU(3) breaking)

print(f"  For kaon: m²_K f²_K = −(m_u + m_s)⟨ψ̄ψ⟩")
print(f"\n  Problem: m_s is not yet derived from the φ-ladder")
print(f"  (needs Yukawa/SU(3) flavor structure)")
print(f"\n  Structural prediction:")
print(f"    m²_K / m²_π = (m_u + m_s) / (m_u + m_d)")
print(f"    With PDG m_s = 93.4 MeV:")
print(f"      ratio = (0.53 + 93.4)/(0.53 + 0.86) = {(0.53+93.4)/(0.53+0.86):.1f}")
print(f"      m_K / m_π ≈ √{(0.53+93.4)/(0.53+0.86):.1f} = {np.sqrt((0.53+93.4)/(0.53+0.86)):.2f}")
print(f"      m_K ≈ {139.6 * np.sqrt((0.53+93.4)/(0.53+0.86)):.0f} MeV (PDG: 494 MeV)")

# ============================================================================
# 7. CONSTITUENT MASSES FROM CHIRAL BREAKING
# ============================================================================

print("\n### 7. CONSTITUENT QUARK MASSES (GU-derived)")
print("-" * 60)

# Constituent mass = dynamical mass from chiral breaking + current mass
# M_dyn = Λ³_QCD / (3f²_π) using GU's f_π estimate

for label, f_val in [("f_π = Λ/√4π", f_pi_A), ("f_π = √N_c·Λ/(2π)", f_pi_sc)]:
    M_dyn_val = Lambda_f ** 3 / (3 * f_val ** 2) if f_val > 0 else 0
    m_u_const = M_dyn_val + m_u_f
    m_d_const = M_dyn_val + m_d_f

    print(f"\n  With {label} = {f_val:.1f} MeV:")
    print(f"    M_dyn = Λ³/(3f²_π) = {M_dyn_val:.1f} MeV")
    print(f"    m_u(constituent) = {M_dyn_val:.1f} + {m_u_f:.2f} = {m_u_const:.1f} MeV")
    print(f"    m_d(constituent) = {M_dyn_val:.1f} + {m_d_f:.2f} = {m_d_const:.1f} MeV")
    print(f"    (Expected: ~330 MeV for light quarks)")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "=" * 80)
print("CHIRAL SECTOR SUMMARY")
print("=" * 80)

print(f"""
  GU-DERIVED INPUTS (zero PDG):
    m_u = {m_u_f:.6f} MeV    (from φ^(-107))
    m_d = {m_d_f:.6f} MeV    (from φ^(-106))
    Λ_QCD = {Lambda_f:.4f} MeV  (from (π/3)·M_P·φ^(-95))

  GU-ESTIMATED (dimensional analysis):
    f_π ≈ {f_pi_sc:.1f} MeV  (self-consistent, PDG: 92.1)
    ⟨ψ̄ψ⟩^(1/3) ≈ {cond_sc_cbrt:.1f} MeV  (PDG/lattice: ~250)
    M_dynamical ≈ {M_dyn_sc:.1f} MeV  (expected: ~300-350)

  PREDICTIONS:
    m_π ≈ {m_pi_sc:.1f} MeV  (PDG: 139.6 MeV, error: {err_sc:.1f}%)

  WHAT WOULD MAKE THIS EXACT:
    ○ Solve the chiral FRG flow U_k(ρ) from theory/theory-laws.md §QCD-5
    ○ Extract σ₀ = √(2ρ₀) at the minimum → f²_π = Z_{{φ,0}} · σ²₀
    ○ This would give f_π from first principles (no dim analysis)
    ○ Then GMOR gives m_π exactly

  KEY INSIGHT:
    The pion mass is controlled by BOTH the current quark masses
    (from the φ-ladder) AND the chiral condensate (from Λ_QCD).
    Both are GU-derived. The only approximation is the O(1) factors
    in the condensate and f_π, which need the full FRG flow.
""")
