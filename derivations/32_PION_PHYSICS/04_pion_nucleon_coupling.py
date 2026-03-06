#!/usr/bin/env python3
"""
PION–NUCLEON COUPLING g_piNN FROM GOLDBERGER–TREIMAN
======================================================

Goldberger–Treiman relation:
    g_piNN = g_A * m_N / f_pi

where:
    g_A   = 1.2754  (axial coupling; experimental, derivable from quark model)
    m_N   = 938.272 MeV (nucleon mass; GU-derived to 0.07%)
    f_pi  = 92.2 MeV (pion decay constant)

Computes:
  - g_piNN from GT with PDG inputs
  - g_piNN^2/(4*pi) vs experiment 13.7 ± 0.2
  - g_piNN with GU-derived f_pi (NJL 109.4 MeV, f_pi = Lambda_QCD/phi)
  - g_A from quark model (NR, SU(6)+QCD, GU alpha_s at proton scale)
  - Goldberger–Treiman discrepancy Delta_GT

Uses numpy only (no mpmath).
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from utils.gu_constants import CODATA

# Local constants (numpy, no mpmath)
phi = (1 + np.sqrt(5)) / 2
M_P = 1.22089e22   # MeV
pi = np.pi
Lambda_QCD = (pi / 3) * M_P * phi**(-95)
Lambda_f = float(Lambda_QCD)

# PDG / experimental inputs
g_A_exp = 1.2754
m_N_pdg = CODATA["proton"]   # MeV
f_pi_pdg = 92.2     # MeV
m_p_gu = 938.0      # MeV (GU-derived, 0.07% of PDG)
f_pi_njl = 109.4    # MeV (GU NJL / Pagels–Stokar)
f_pi_gu = Lambda_f / phi  # 110.6 MeV (GU f_pi = Lambda_QCD/phi)

# Experimental g_piNN^2/(4*pi)
g_piNN_sq_4pi_exp = 13.7
g_piNN_sq_4pi_err = 0.2

# ---------------------------------------------------------------------------
# STEP 1: g_A FROM QUARK MODEL
# ---------------------------------------------------------------------------

print("=" * 80)
print("STEP 1: g_A FROM QUARK MODEL")
print("=" * 80)

# Non-relativistic quark model: g_A = 5/3
g_A_NR = 5.0 / 3.0
print(f"\n  Non-relativistic quark model:  g_A = 5/3 = {g_A_NR:.4f}  (too high)")
print(f"  Experiment (PDG):             g_A = {g_A_exp:.4f}")

# SU(6) with one-loop QCD correction: g_A * (1 - 2*alpha_s/(3*pi)) ~ 1.25
# So g_A_corrected = (5/3) * (1 - 2*alpha_s/(3*pi)); solve for alpha_s that gives ~1.25
# 1.25 = (5/3)*(1 - 2*alpha_s/(3*pi))  =>  1 - 2*alpha_s/(3*pi) = 1.25*3/5 = 0.75  =>  alpha_s = 0.25*3*pi/2 = 1.18 (too large)
# So the formula is phenomenological: use alpha_s at proton scale.
alpha_s_proton = 0.35   # typical at ~1 GeV
g_A_SU6_QCD = (5.0 / 3.0) * (1.0 - 2.0 * alpha_s_proton / (3.0 * pi))
print(f"\n  SU(6) + QCD (alpha_s(m_N) = {alpha_s_proton}):  g_A = (5/3)*(1 - 2*alpha_s/(3*pi)) = {g_A_SU6_QCD:.4f}")

# GU: use alpha_s at proton scale (same formula, GU could fix alpha_s from running)
# For definiteness use alpha_s at 1 GeV from one-loop: alpha_s(mu) ~ 0.35
alpha_s_gu_proton = 0.35
g_A_GU = (5.0 / 3.0) * (1.0 - 2.0 * alpha_s_gu_proton / (3.0 * pi))
print(f"  GU value (alpha_s at proton scale = {alpha_s_gu_proton}):  g_A = {g_A_GU:.4f}")
print(f"\n  → g_A is not derived from GU here; GT uses experimental g_A = {g_A_exp:.4f} for g_piNN.")

# ---------------------------------------------------------------------------
# STEP 2: g_piNN FROM GOLDBERGER–TREIMAN
# ---------------------------------------------------------------------------

print("\n" + "=" * 80)
print("STEP 2: g_piNN FROM GOLDBERGER–TREIMAN")
print("=" * 80)

# GT: g_piNN = g_A * m_N / f_pi
g_piNN_pdg = g_A_exp * m_N_pdg / f_pi_pdg
print(f"\n  g_piNN = g_A * m_N / f_pi")
print(f"  With PDG: g_A = {g_A_exp}, m_N = {m_N_pdg} MeV, f_pi = {f_pi_pdg} MeV")
print(f"  → g_piNN = {g_A_exp} * {m_N_pdg} / {f_pi_pdg} = {g_piNN_pdg:.4f}")

g_piNN_sq_4pi = g_piNN_pdg**2 / (4.0 * pi)
print(f"\n  g_piNN^2 / (4*pi) = {g_piNN_sq_4pi:.2f}")
print(f"  Experimental:      {g_piNN_sq_4pi_exp} ± {g_piNN_sq_4pi_err}")
print(f"  Relative error:    {abs(g_piNN_sq_4pi - g_piNN_sq_4pi_exp) / g_piNN_sq_4pi_exp * 100:.1f}%")

# GU-derived f_pi (NJL) = 109.4 MeV, m_N = 938 MeV
g_piNN_njl = g_A_exp * m_p_gu / f_pi_njl
print(f"\n  With GU-derived f_pi (NJL) = {f_pi_njl} MeV, m_p = {m_p_gu} MeV:")
print(f"  → g_piNN = g_A * m_p / f_pi_NJL = {g_piNN_njl:.4f}")

# f_pi = Lambda_QCD / phi = 110.6 MeV
print(f"\n  With f_pi = Lambda_QCD/phi = {Lambda_f:.1f}/phi = {f_pi_gu:.2f} MeV:")
g_piNN_gu_fpi = g_A_exp * m_p_gu / f_pi_gu
print(f"  → g_piNN = g_A * m_p / (Lambda_QCD/phi) = {g_piNN_gu_fpi:.4f}")

# ---------------------------------------------------------------------------
# STEP 3: GOLDBERGER–TREIMAN DISCREPANCY
# ---------------------------------------------------------------------------

print("\n" + "=" * 80)
print("STEP 3: GOLDBERGER–TREIMAN DISCREPANCY")
print("=" * 80)

# Delta_GT = 1 - g_A * m_N / (g_piNN * f_pi)
# If GT were exact, g_piNN = g_A * m_N / f_pi  =>  g_A * m_N / (g_piNN * f_pi) = 1  =>  Delta_GT = 0.
# Experiment: g_piNN from NN/piN data, so Delta_GT = 1 - (g_A * m_N)/(g_piNN * f_pi).
# Using PDG values: g_A * m_N / f_pi = g_piNN (by definition if we define g_piNN from GT);
# so if we take g_piNN_exp from experiment (e.g. 13.7 -> g_piNN = sqrt(13.7*4*pi) ≈ 13.1):
g_piNN_from_exp = np.sqrt(g_piNN_sq_4pi_exp * 4.0 * pi)
Delta_GT = 1.0 - (g_A_exp * m_N_pdg) / (g_piNN_from_exp * f_pi_pdg)
print(f"\n  Delta_GT = 1 - g_A * m_N / (g_piNN * f_pi)")
print(f"  Using g_piNN from experiment (g_piNN^2/(4*pi) = {g_piNN_sq_4pi_exp}):  g_piNN = {g_piNN_from_exp:.3f}")
print(f"  → Delta_GT = 1 - {g_A_exp}*{m_N_pdg}/({g_piNN_from_exp:.3f}*{f_pi_pdg}) = {Delta_GT:.4f}")
print(f"  Typical quoted value: Delta_GT ≈ 0.015 (chiral symmetry nearly exact).")

# Also with GT-defined g_piNN (then denominator = g_piNN*f_pi = g_A*m_N, so Delta_GT = 0 by definition)
# So the physical discrepancy uses experimentally determined g_piNN (from pi N scattering etc.)
Delta_GT_using_GT_g = 1.0 - (g_A_exp * m_N_pdg) / (g_piNN_pdg * f_pi_pdg)
print(f"  If g_piNN is defined by GT:  g_piNN*f_pi = g_A*m_N  →  Delta_GT = {Delta_GT_using_GT_g:.6f} (exact by definition).")

# ---------------------------------------------------------------------------
# STEP 4: SUMMARY AND HONEST ASSESSMENT
# ---------------------------------------------------------------------------

print("\n" + "=" * 80)
print("STEP 4: SUMMARY")
print("=" * 80)

print(f"""
  Quantities:
    g_A (experimental)     = {g_A_exp}
    m_N (PDG)             = {m_N_pdg} MeV
    f_pi (PDG)            = {f_pi_pdg} MeV
    Lambda_QCD (GU)       = {Lambda_f:.2f} MeV
    f_pi = Lambda_QCD/phi  = {f_pi_gu:.2f} MeV

  Goldberger–Treiman (PDG inputs):
    g_piNN                = {g_piNN_pdg:.4f}
    g_piNN^2/(4*pi)       = {g_piNN_sq_4pi:.2f}  (exp: {g_piNN_sq_4pi_exp} ± {g_piNN_sq_4pi_err})

  With GU-derived f_pi:
    f_pi_NJL = {f_pi_njl} MeV  →  g_piNN = {g_piNN_njl:.4f}
    f_pi = Lambda_QCD/phi     →  g_piNN = {g_piNN_gu_fpi:.4f}

  GT discrepancy (experimental g_piNN):  Delta_GT ≈ {Delta_GT:.3f}
""")

print("-" * 80)
print("HONEST ASSESSMENT: DERIVED VS CALIBRATED")
print("-" * 80)
print("""
  Derived in this script:
    - Lambda_QCD from GU: (pi/3)*M_P*phi^(-95).
    - f_pi_gu = Lambda_QCD/phi (one GU route to f_pi).
    - g_piNN from the Goldberger–Treiman formula given g_A, m_N, f_pi (algebra).
    - g_A estimates from quark model (5/3, SU(6)+QCD correction); not a GU derivation.
    - Delta_GT from definition using experimental g_piNN.

  Calibrated / experimental inputs:
    - g_A = 1.2754 (experimental; quark-model corrections use alpha_s at proton scale).
    - m_N = 938.272 MeV (PDG; GU derives nucleon mass to ~0.07% elsewhere).
    - f_pi = 92.2 MeV (PDG) for the main g_piNN comparison.
    - g_piNN^2/(4*pi) = 13.7 ± 0.2 (experiment) for comparison.

  Conclusion:
    g_piNN is computed from the Goldberger–Treiman relation, not derived from first
    principles here. GU provides Lambda_QCD and hence f_pi = Lambda_QCD/phi and
    NJL-style f_pi; using those gives different g_piNN values because GU f_pi is
    larger than PDG f_pi. The small Delta_GT shows that chiral symmetry is very
    close to exact in the GT relation.
""")
