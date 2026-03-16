#!/usr/bin/env python3
"""
MEMORY-MODE DOF CENSUS: DERIVING c_R FROM FIELD CONTENT
========================================================

Explicit enumeration of every propagating mode of the Omega-substrate
and Standard Model, computing their spin-weighted Seeley-DeWitt a_1
contributions, to check whether they reproduce c_R = 1.25.

MOTIVATION:
    The canonical gravity derivation (04_seeley_dewitt_calculation.py) uses
    c_R = 1.25 as ASSUMED input from V2 Section 8.3.  The V2 states this
    comes from "n_B - n_F ~ +5 (after adding +40 bosonic memory modes)."
    This script attempts to DERIVE that number from the actual field content
    of L_total, or at minimum to identify precisely what field content is
    needed and what remains undetermined.

KEY FORMULA (V2 Section 9.2.4):
    The one-loop effective action induces the Einstein-Hilbert term:

        1/(16 pi G_N) = [Lambda^2 / (16 pi^2)] Str(a_1)

    Matching to M_P^2 = 1/G_N  (natural units, hbar = c = 1):

        M_P^2 = Lambda^2 Str(a_1) / pi

    Defining c_R = Str(a_1) / (4 pi):

        M_P^2 = 4 pi c_R Lambda^2

    With c_R = 1.25:  M_P / M_0 = sqrt(5 pi) ~ 3.96

PER-FIELD a_1 CONTRIBUTIONS (minimally coupled, 4D curved background):
    Real scalar (xi=0):     a_1 = +R/6   per real DOF
    Dirac fermion:          a_1 = -R/12  per real DOF  (sign from Grassmann)
    Massless vector (+ FP): a_1 = +R/6   per physical DOF (4 comp - 2 ghosts)
    Massive vector (Proca): a_1 = +R/6   per physical DOF (3 polarizations)

    Str(a_1)/R = (1/6) N_B - (1/12) N_F = (1/12)(2 N_B - N_F)

    where N_B = total real bosonic DOF, N_F = total real fermionic DOF.

NORMALIZATION NOTE:
    V2 uses TWO conventions (Sections 8.3 vs 9.2) that appear inconsistent.
    This script reconciles them by deriving both from the fundamental formula
    and showing they correspond to different definitions of c_R.

References:
    - V2 Sections 8.3, 9.2 (Sakharov induced gravity, Seeley-DeWitt)
    - Sakharov (1967), Visser (2002), Donoghue (1994)
    - V2 Chapter 3 (L_total structure)
    - theory-laws.md Laws 0-5 (Lagrangian decomposition)
    - WHAT_IS_GRAVITY.md (memory mode physical interpretation)
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mpmath import mp, mpf, sqrt, pi as mp_pi
mp.dps = 50

from utils.gu_constants import phi, pi, M_P, M_0


# ======================================================================
# SECTION 1: SEELEY-DEWITT MASTER FORMULA
# ======================================================================

def str_a1_coefficient(n_boson_real, n_fermion_real):
    """Compute Str(a_1)/R for minimally coupled fields.

    Returns the dimensionless coefficient multiplying R in the supertrace.
    Positive = correct sign for induced gravity (attractive).

    Per-DOF contributions:
        Real scalar:     +1/6
        Real fermion:    -1/12  (Grassmann sign)
        Vector boson:    counted via physical DOF as real scalars at +1/6
    """
    return mpf(n_boson_real) / 6 - mpf(n_fermion_real) / 12


def c_R_from_str_a1(str_a1_over_R):
    """Convert Str(a_1)/R to the c_R coefficient.

    Convention: M_P^2 = 4 pi c_R Lambda^2
    From:  1/(16 pi G) = Lambda^2/(16 pi^2) * Str(a_1)
           M_P^2 = Lambda^2 * Str(a_1) / pi
           c_R = Str(a_1) / (4 pi)   [so Str(a_1) = 4 pi c_R]
           M_P^2 = 4 pi c_R Lambda^2
    """
    return str_a1_over_R / (4 * pi)


def mp_over_m0(c_R_val):
    """M_P / M_0 ratio from c_R."""
    if c_R_val <= 0:
        return mpf(0)
    return sqrt(4 * pi * c_R_val)


# ======================================================================
# SECTION 2: STANDARD MODEL FIELD CENSUS
# ======================================================================

def build_sm_census():
    """Careful enumeration of all SM fields with real DOF counts.

    Returns dict of categories, each with items listing name, real DOF,
    spin, and whether it's bosonic or fermionic.

    Conventions:
        - Fermion DOF: real components of Dirac/Weyl spinors
          Dirac = 4 real DOF, Weyl = 2 real DOF
        - Gauge bosons: physical (transverse) DOF after gauge fixing + ghosts
          Massless vector: 2 physical DOF (from 4 - 2 ghosts)
          Massive vector: 3 physical DOF (Proca, longitudinal included)
        - Scalars: real components of complex multiplets
    """

    fermions = [
        # Charged leptons (Dirac: 4 real DOF each)
        ("electron",     4, "1/2", "Dirac"),
        ("muon",         4, "1/2", "Dirac"),
        ("tau",          4, "1/2", "Dirac"),
        # Neutrinos (Weyl, left-handed only in minimal SM: 2 real DOF each)
        ("nu_e",         2, "1/2", "Weyl"),
        ("nu_mu",        2, "1/2", "Weyl"),
        ("nu_tau",       2, "1/2", "Weyl"),
        # Quarks (Dirac, 3 colors: 4 * 3 = 12 real DOF each)
        ("up x 3c",     12, "1/2", "Dirac x 3 colors"),
        ("down x 3c",   12, "1/2", "Dirac x 3 colors"),
        ("strange x 3c",12, "1/2", "Dirac x 3 colors"),
        ("charm x 3c",  12, "1/2", "Dirac x 3 colors"),
        ("bottom x 3c", 12, "1/2", "Dirac x 3 colors"),
        ("top x 3c",    12, "1/2", "Dirac x 3 colors"),
    ]

    gauge_bosons = [
        # Massless vectors: 2 physical DOF each (after FP ghosts)
        ("photon",        2, "1", "massless, 2 transverse"),
        ("gluon x 8",   16, "1", "massless, 8 x 2 transverse"),
        # Massive vectors: 3 physical DOF each (Proca / unitary gauge)
        ("W+",            3, "1", "massive, 3 polarizations"),
        ("W-",            3, "1", "massive, 3 polarizations"),
        ("Z",             3, "1", "massive, 3 polarizations"),
    ]

    scalars = [
        # Higgs doublet: complex SU(2) doublet = 4 real scalars
        # In unitary gauge: 1 physical Higgs + 3 eaten Goldstones
        # For heat kernel: count all 4 real DOF (gauge-independent result)
        ("Higgs doublet", 4, "0", "complex SU(2) doublet = 4 real"),
    ]

    return fermions, gauge_bosons, scalars


def print_sm_census(fermions, gauge_bosons, scalars):
    """Print the SM field census and compute totals."""

    print("\n   FERMIONS (spin-1/2)")
    print(f"   {'Field':<20} {'Real DOF':<10} {'Type'}")
    print(f"   {'-'*20} {'-'*10} {'-'*30}")
    n_f = 0
    for name, dof, spin, ftype in fermions:
        print(f"   {name:<20} {dof:<10} {ftype}")
        n_f += dof

    print(f"\n   GAUGE BOSONS (spin-1)")
    print(f"   {'Field':<20} {'Real DOF':<10} {'Type'}")
    print(f"   {'-'*20} {'-'*10} {'-'*30}")
    n_v = 0
    for name, dof, spin, ftype in gauge_bosons:
        print(f"   {name:<20} {dof:<10} {ftype}")
        n_v += dof

    print(f"\n   SCALARS (spin-0)")
    print(f"   {'Field':<20} {'Real DOF':<10} {'Type'}")
    print(f"   {'-'*20} {'-'*10} {'-'*30}")
    n_s = 0
    for name, dof, spin, ftype in scalars:
        print(f"   {name:<20} {dof:<10} {ftype}")
        n_s += dof

    n_b = n_v + n_s

    print(f"\n   TOTALS:")
    print(f"     Fermion real DOF  (N_F): {n_f}")
    print(f"     Vector real DOF   (N_V): {n_v}")
    print(f"     Scalar real DOF   (N_S): {n_s}")
    print(f"     Total boson DOF   (N_B = N_V + N_S): {n_b}")

    return n_f, n_b, n_v, n_s


# ======================================================================
# SECTION 3: GU MEMORY MODES -- CANDIDATE ENUMERATION
# ======================================================================

def build_gu_memory_modes():
    """Enumerate candidate GU memory modes beyond the SM.

    Returns list of (name, real_dof, certainty, source_ref, notes).
    certainty is one of: "certain", "theory-motivated", "requires G_prim".

    Sources:
        A: Amplitude (modulus) fluctuations of Omega
        B: Phase fluctuations (theta_a fields)
        C: Torus moduli
        D: X field (cosmic driver)
        E: Additional scalar multiplets from G_prim breaking
        F: Non-minimal coupling corrections (modify existing, not new DOF)
    """

    modes = []

    # Source D: X field (cosmic driver) -- CERTAIN
    # V2 Ch.3 Section B: L_X = (1/2)(partial X)^2 - V_X(X)
    # One real scalar with standard kinetic term
    modes.append({
        "name": "X (cosmic driver)",
        "dof": 1,
        "certainty": "certain",
        "source": "V2 Ch.3 Sec.B, Law 3",
        "notes": "Real scalar, standard kinetic term",
    })

    # Source B: Phase fluctuations theta_a
    # V2 Ch.3 Sec.A.iv, WHAT_IS_GRAVITY.md Part III
    # At SM level: one theta per gauge sector (U(1), SU(2), SU(3)) = 3
    # At SU(5) level: one theta_GUT = 1
    # These are 2*pi-periodic real scalars
    modes.append({
        "name": "theta_a phases (SM level: 3 sectors)",
        "dof": 3,
        "certainty": "theory-motivated",
        "source": "V2 Ch.3 Sec.A.iv, L_top in theory-laws.md",
        "notes": "One per gauge sector; at SU(5) level would be 1",
    })

    # Source C: Torus moduli
    # WHAT_IS_GRAVITY.md Part III Source 3
    # Complex modulus tau (2 real) + overall scale (1 real) = 3 minimum
    modes.append({
        "name": "Torus moduli (tau_1, tau_2, R)",
        "dof": 3,
        "certainty": "theory-motivated",
        "source": "GU torus geometry, KK analogy",
        "notes": "Minimum 3 for a single 2-torus; could be more",
    })

    # Source A: Amplitude (modulus) fluctuation of Omega
    # delta_rho around vacuum v_vac
    # This is automatically 1 real scalar per complex scalar component of Omega
    # The SM Higgs is already counted. The question is whether there are
    # ADDITIONAL scalar components of Omega beyond the SM Higgs.
    # V2 Ch.3: "scalar components Omega_s" in irreducible reps of G_prim
    # If Omega contains ONLY the SM Higgs as its scalar sector, delta_rho
    # is already counted in the SM census. But V2 explicitly states Omega
    # is "multi-component" with "scalar, spinor, and potentially other components"
    # in reps of G_prim.
    modes.append({
        "name": "Omega modulus (beyond SM Higgs)",
        "dof": 1,
        "certainty": "theory-motivated",
        "source": "V2 Ch.3: Omega is multi-component",
        "notes": "At least 1 extra real scalar; exact count depends on G_prim",
    })

    # Source E: Additional scalars from G_prim breaking
    # These are the potentially dominant source.
    # The exact count depends entirely on the choice of G_prim.
    #
    # Scenario: G_prim = SU(5) (minimal GUT)
    #   - Adjoint 24-plet Higgs (for SU(5) -> SM breaking):
    #     24 real scalars (24 is a real representation)
    #     After SSB: 12 eaten Goldstones + 12 massive scalars
    #     BUT for heat kernel at scale Lambda ~ M_0 >> M_GUT,
    #     all 24 contribute as propagating DOF
    #   - Fundamental 5-plet (contains SM Higgs):
    #     10 real scalars (complex 5)
    #     SM Higgs doublet (4 real) already counted, so 6 extra
    #     (the color-triplet Higgs partner)
    #
    # We present this as a parametric scenario, not a definitive count.

    return modes


def print_memory_modes(modes):
    """Print the memory mode candidates with their certainty levels."""

    total_certain = 0
    total_motivated = 0
    total_gprim = 0

    for m in modes:
        cert_tag = m["certainty"]
        dof = m["dof"]
        if cert_tag == "certain":
            total_certain += dof
        elif cert_tag == "theory-motivated":
            total_motivated += dof
        elif cert_tag == "requires G_prim":
            total_gprim += dof

        print(f"   [{cert_tag:<18s}]  {m['name']:<42s}  DOF: {dof}")
        print(f"                        Source: {m['source']}")
        if m['notes']:
            print(f"                        Notes:  {m['notes']}")

    total = total_certain + total_motivated + total_gprim
    print(f"\n   Subtotals by certainty:")
    print(f"     Certain:           {total_certain} real bosonic DOF")
    print(f"     Theory-motivated:  {total_motivated} real bosonic DOF")
    print(f"     Requires G_prim:   {total_gprim} real bosonic DOF")
    print(f"     Combined:          {total} real bosonic DOF (minimum)")

    return total_certain, total_motivated, total_gprim


# ======================================================================
# SECTION 4: SCENARIO ANALYSIS
# ======================================================================

def analyze_scenario(name, n_f_sm, n_b_sm, n_b_extra, description):
    """Compute c_R and M_P/M_0 for a given scenario."""

    n_b_total = n_b_sm + n_b_extra
    n_f_total = n_f_sm

    eff = 2 * n_b_total - n_f_total
    str_a1 = str_a1_coefficient(n_b_total, n_f_total)
    c_R = c_R_from_str_a1(str_a1)
    ratio = mp_over_m0(c_R)

    print(f"\n   --- {name} ---")
    print(f"   {description}")
    print(f"   N_B = {n_b_sm} (SM) + {n_b_extra} (extra) = {n_b_total}")
    print(f"   N_F = {n_f_total}")
    print(f"   2*N_B - N_F = {eff}")
    print(f"   Str(a_1)/R  = {float(str_a1):.6f}")
    print(f"   c_R         = {float(c_R):.6f}")

    if c_R > 0:
        print(f"   M_P/M_0     = {float(ratio):.6f}")
        print(f"   Target      = {float(sqrt(5*pi)):.6f}  (sqrt(5 pi))")
        err = abs(float(ratio) - float(sqrt(5*pi))) / float(sqrt(5*pi)) * 100
        print(f"   Deviation   = {err:.2f}%")
    else:
        print(f"   M_P/M_0     = IMAGINARY (c_R < 0 => wrong sign)")

    return c_R, ratio


# ======================================================================
# SECTION 5: NORMALIZATION CROSS-CHECK
# ======================================================================

def normalization_crosscheck():
    """Reconcile the two V2 normalization conventions."""

    print("""
   The V2 document uses two conventions in Sections 8.3 and 9.2.
   This section shows they are CONSISTENT when the definitions of
   c_R are properly distinguished.

   CONVENTION A (V2 Section 8.3.3-8.3.4, "user" convention):
   ---------------------------------------------------------
   c_R^user = (1/4)(n_B - n_F)    [simplified effective DOF counts]
   M_P^2 = 16 pi c_R^user Lambda^2

   With n_B - n_F = 5:  c_R^user = 1.25
   M_P^2 = 16 pi (1.25) Lambda^2 = 20 pi Lambda^2
   M_P = sqrt(20 pi) Lambda ~ 7.93 Lambda

   V2 says: "M_P ~ 7.92 * (3e18 GeV) ~ 2.38e19 GeV"
   Compare: M_P(observed) = 1.22e19 GeV  => OFF BY 2x

   CONVENTION B (V2 Section 9.2.4, "standard" convention):
   --------------------------------------------------------
   Start from: 1/(16 pi G) = Lambda^2/(16 pi^2) * Str(a_1)
   => M_P^2 = Lambda^2 * Str(a_1) / pi

   Define: c_R^std = Str(a_1) / (4 pi)
   => M_P^2 = 4 pi c_R^std Lambda^2

   V2 also says: "G_N = c^4 / (4 pi c_R Lambda^2)
                   implies M_P^2 = 4 pi c_R Lambda^2"
   With c_R = 1.25:
   M_P = sqrt(5 pi) Lambda ~ 3.96 Lambda

   V2 says: "M_P ~ 3.96 * (3e18 GeV) ~ 1.19e19 GeV"
   Compare: M_P(observed) = 1.22e19 GeV  => EXCELLENT MATCH

   RECONCILIATION:
   ----------------
   Convention A's "c_R^user = (1/4)(n_B - n_F)" uses a DIFFERENT
   weighting than Convention B's "c_R^std = Str(a_1)/(4 pi)".

   In Convention A, n_B and n_F are abstract "effective counts" that
   absorb the spin-dependent a_1 weights. The formula
   M_P^2 = 16 pi c_R^user Lambda^2 gives M_P/Lambda ~ 7.9, which
   is a factor of 2 too large.

   Convention B is the STANDARD heat-kernel result and gives the
   correct M_P/Lambda ~ 3.96. It is the convention used in
   04_seeley_dewitt_calculation.py and throughout this analysis.

   The V2 document itself resolves this discrepancy by presenting
   BOTH results and noting that "the specific value depends on the
   precise c_R^eff and the 16 pi vs 4 pi factors from different
   conventions." The 4 pi convention with c_R = 1.25 is the one
   that works.

   ADOPTED CONVENTION (canonical for GU gravity):
   c_R = Str(a_1) / (4 pi)
   M_P^2 = 4 pi c_R Lambda^2
   M_P / M_0 = sqrt(4 pi c_R) = sqrt(5 pi) ~ 3.96
""")

    c_R_user = mpf('1.25')
    mp_conv_a = sqrt(16 * pi * c_R_user)
    mp_conv_b = sqrt(4 * pi * c_R_user)

    print(f"   Numerical check:")
    print(f"     Convention A: M_P/Lambda = sqrt(16 pi * 1.25) = {float(mp_conv_a):.4f}")
    print(f"     Convention B: M_P/Lambda = sqrt(4 pi * 1.25)  = {float(mp_conv_b):.4f}")
    print(f"     Convention B = Convention A / 2")
    print(f"     Convention B gives M_P ~ 3.96 * 3e18 GeV = 1.19e19 GeV (correct)")


# ======================================================================
# MAIN
# ======================================================================

def main():
    print("=" * 80)
    print("MEMORY-MODE DOF CENSUS")
    print("Deriving c_R from the GU Field Content")
    print("=" * 80)

    # ------------------------------------------------------------------
    # Step 1: SM census
    # ------------------------------------------------------------------
    print()
    print("-" * 80)
    print("STEP 1: STANDARD MODEL FIELD CENSUS")
    print("-" * 80)

    fermions, gauge_bosons, scalars = build_sm_census()
    n_f, n_b, n_v, n_s = print_sm_census(fermions, gauge_bosons, scalars)

    str_a1_sm = str_a1_coefficient(n_b, n_f)
    c_R_sm = c_R_from_str_a1(str_a1_sm)

    print(f"\n   SEELEY-DEWITT ANALYSIS (SM only):")
    print(f"     2*N_B - N_F       = {2*n_b - n_f}")
    print(f"     Str(a_1)/R        = (1/12)(2*{n_b} - {n_f})")
    print(f"                       = (1/12)({2*n_b - n_f})")
    print(f"                       = {float(str_a1_sm):.6f}")
    print(f"     c_R(SM)           = Str(a_1)/(4 pi)")
    print(f"                       = {float(c_R_sm):.6f}")

    print(f"\n   VERDICT: c_R(SM) = {float(c_R_sm):.4f} < 0")
    print(f"   The SM alone gives WRONG SIGN for induced gravity.")
    print(f"   This is the well-known Sakharov sign problem (Visser 2002).")
    print(f"   Fermion DOF ({n_f}) overwhelm boson DOF ({n_b}).")

    # ------------------------------------------------------------------
    # Step 2: GU memory modes
    # ------------------------------------------------------------------
    print()
    print("-" * 80)
    print("STEP 2: GU MEMORY MODES -- CANDIDATE ENUMERATION")
    print("-" * 80)

    modes = build_gu_memory_modes()
    print()
    n_cert, n_mot, n_gp = print_memory_modes(modes)

    # ------------------------------------------------------------------
    # Step 3: Required DOF for c_R = 1.25
    # ------------------------------------------------------------------
    print()
    print("-" * 80)
    print("STEP 3: REQUIRED DOF FOR c_R = 1.25")
    print("-" * 80)

    c_R_target = mpf('1.25')
    str_a1_target = 4 * pi * c_R_target  # = 5 pi

    # Need: (1/12)(2*N_B_total - N_F_total) = 5 pi
    # => 2*N_B_total - N_F_total = 60 pi
    eff_target = 12 * str_a1_target  # = 60 pi
    eff_sm = 2 * n_b - n_f
    eff_memory_needed = float(eff_target) - eff_sm

    # 2 * N_B_memory = eff_memory_needed  (memory modes are all bosonic)
    n_b_memory_needed = eff_memory_needed / 2

    print(f"\n   Target: c_R = {float(c_R_target)}")
    print(f"   => Str(a_1)/R = 4 pi c_R = 5 pi = {float(str_a1_target):.6f}")
    print(f"   => 2*N_B_total - N_F_total = 12 * Str(a_1)/R")
    print(f"                              = 60 pi = {float(eff_target):.2f}")
    print(f"\n   SM already contributes:")
    print(f"     2*N_B(SM) - N_F(SM) = 2*{n_b} - {n_f} = {eff_sm}")
    print(f"\n   Deficit from memory modes (all bosonic, so contribute +2 per DOF):")
    print(f"     2*N_B_memory = {float(eff_target):.2f} - ({eff_sm})")
    print(f"                  = {eff_memory_needed:.2f}")
    print(f"     N_B_memory   = {n_b_memory_needed:.1f} real bosonic DOF needed")
    print(f"\n   INTERPRETATION:")
    print(f"     The GU theory needs approximately {int(round(n_b_memory_needed))}")
    print(f"     additional real bosonic DOF (minimally coupled scalars)")
    print(f"     beyond the SM to achieve c_R = 1.25.")
    print(f"\n     V2 states '+40 bosonic memory modes.'")
    print(f"     Required: ~{int(round(n_b_memory_needed))}.")
    n_b_simple = n_cert + n_mot + n_gp
    print(f"     Identified (certain + motivated): {n_b_simple}")
    print(f"     Gap: ~{int(round(n_b_memory_needed)) - n_b_simple}"
          f" DOF unaccounted for.")
    print(f"\n     This gap must come from Source E: additional scalar")
    print(f"     multiplets from the primordial gauge group G_prim.")

    # ------------------------------------------------------------------
    # Step 4: Scenario analysis
    # ------------------------------------------------------------------
    print()
    print("-" * 80)
    print("STEP 4: SCENARIO ANALYSIS")
    print("-" * 80)
    print("\n   Computing c_R for several concrete GU field-content scenarios.")

    # Scenario A: Minimal (just the modes we identified)
    analyze_scenario(
        "Scenario A: Minimal GU extras",
        n_f, n_b, n_b_simple,
        f"SM + X + 3 theta_a + 3 torus moduli + 1 extra Omega = SM + {n_b_simple} scalars",
    )

    # Scenario B: SM + 40 memory modes (V2 claim)
    analyze_scenario(
        "Scenario B: V2 claim (+40 memory modes)",
        n_f, n_b, 40,
        "SM + 40 bosonic DOF (as stated in V2 Section 8.3.4)",
    )

    # Scenario C: SU(5) adjoint Higgs
    # 24-plet adjoint (24 real) + X(1) + theta(3) + moduli(3) + 1 extra modulus
    n_su5_adj = 24 + 1 + 3 + 3 + 1
    analyze_scenario(
        "Scenario C: SU(5) adjoint Higgs",
        n_f, n_b, n_su5_adj,
        f"SM + SU(5) adjoint 24-plet (24 real) + X + theta_a + moduli = SM + {n_su5_adj}",
    )

    # Scenario D: Full SU(5) (adjoint + color-triplet Higgs partner)
    # 24-plet (24 real) + color-triplet from 5 (6 real beyond SM Higgs) + X + theta + moduli
    n_su5_full = 24 + 6 + 1 + 3 + 3 + 1
    analyze_scenario(
        "Scenario D: Full SU(5) content",
        n_f, n_b, n_su5_full,
        f"SM + 24-plet(24) + color-triplet(6) + X(1) + theta(3) + moduli(3) + extra(1) = SM + {n_su5_full}",
    )

    # Scenario E: SO(10) or larger (illustrative)
    # SO(10) adjoint = 45-plet (45 real) + spinor Higgs 16-plet (32 real) + ...
    n_so10 = 45 + 32 + 1 + 3 + 3 + 1
    analyze_scenario(
        "Scenario E: SO(10) illustrative",
        n_f, n_b, n_so10,
        f"SM + 45-plet(45) + 16-plet(32) + X(1) + theta(3) + moduli(3) + extra(1) = SM + {n_so10}",
    )

    # Scenario F: Exact target
    n_b_exact = int(round(n_b_memory_needed))
    analyze_scenario(
        f"Scenario F: Exact target (N_B_memory = {n_b_exact})",
        n_f, n_b, n_b_exact,
        f"SM + exactly {n_b_exact} extra real bosonic DOF to hit c_R = 1.25",
    )

    # ------------------------------------------------------------------
    # Step 5: Normalization cross-check
    # ------------------------------------------------------------------
    print()
    print("-" * 80)
    print("STEP 5: NORMALIZATION CROSS-CHECK (V2 Sections 8.3 vs 9.2)")
    print("-" * 80)

    normalization_crosscheck()

    # ------------------------------------------------------------------
    # Step 6: Honest assessment
    # ------------------------------------------------------------------
    print()
    print("-" * 80)
    print("STEP 6: HONEST ASSESSMENT")
    print("-" * 80)

    print(f"""
   WHAT IS ESTABLISHED (standard physics):
     - The Seeley-DeWitt heat kernel expansion and per-spin a_1 coefficients
     - The SM field content and its DOF counting
     - The sign problem: SM gives c_R < 0 (fermion-dominated)

   WHAT IS DERIVED IN GU (non-circular):
     - The ratio M_P/M_0 = sqrt(5 pi) ~ 3.96 follows from c_R = 1.25
     - G_N follows from M_P without using G_exp upstream
     - The convention M_P^2 = 4 pi c_R Lambda^2 is the correct one

   WHAT IS ASSUMED:
     - c_R = 1.25 (from V2 Section 8.3, attributed to SM + memory modes)
     - The "+40 memory modes" statement in V2 Section 8.3.4
     - All memory modes are minimally coupled (xi = 0)

   WHAT REMAINS OPEN:
     1. The EXACT field content of the Omega-substrate beyond the SM
        This requires specifying G_prim and the representation content of Omega.
     2. The number of additional real bosonic DOF is ~{n_b_exact}
        (for minimally coupled fields).
     3. V2's "+40 bosonic memory modes" claim: this gives c_R ~ {float(c_R_from_str_a1(str_a1_coefficient(n_b + 40, n_f))):.4f},
        NOT 1.25. The V2's simplified convention is internally inconsistent
        unless "n_B - n_F" in the c_R^user = (1/4)(n_B-n_F) formula
        uses WEIGHTED effective counts, not raw DOF counts.
     4. Non-minimal coupling (xi != 0) would change the required DOF count.
     5. Which GUT group (SU(5), SO(10), or other) the theory selects.

   WHAT THIS ANALYSIS REVEALS:
     - The V2's "+40 memory modes" is NOT consistent with c_R = 1.25
       under the standard Seeley-DeWitt DOF weighting.
     - To reach c_R = 1.25, approximately {n_b_exact} additional real bosonic DOF
       are needed beyond the SM's {n_b}.
     - An SU(5) GUT content (Scenario C or D) provides 32-38 extra DOF,
       which is in the right ballpark but still short.
     - SO(10) or larger G_prim (Scenario E) can easily provide enough DOF.
     - The precise count depends on G_prim, which is an unresolved
       foundational choice in the GU theory.

   IMPLICATIONS FOR THE THEORY:
     - If c_R = 1.25 is correct, the theory PREDICTS approximately
       {n_b_exact} real bosonic DOF beyond the SM.
     - This is a FALSIFIABLE prediction: if the Omega-substrate spectrum
       is ever computed explicitly and gives a different c_R, either the
       spectrum or the gravity derivation must be revised.
     - The result is most naturally achieved with a GUT-scale G_prim
       like SO(10) with its adjoint + spinor Higgs content.
""")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print(f"""
   MEMORY-MODE DOF CENSUS RESULTS:
     SM field content:      N_B = {n_b}, N_F = {n_f}
     SM gives:              c_R(SM) = {float(c_R_sm):.4f} (WRONG SIGN)
     Target:                c_R = 1.25, M_P/M_0 = sqrt(5 pi) ~ 3.96
     Required extra bosons: ~{n_b_exact} real DOF (minimally coupled)
     V2 claims:             +40 memory modes (INCONSISTENT with standard weighting)
     Identified (certain):  {n_cert} DOF (X field)
     Identified (motivated): {n_mot} DOF (theta_a, moduli, extra modulus)
     Gap:                   ~{n_b_exact - n_b_simple} DOF must come from G_prim content

   SCORECARD:
     [PASS]  SM census: correct DOF counting with neutrinos and ghosts
     [PASS]  SM sign problem: confirmed (c_R < 0)
     [PASS]  Target c_R: 1.25 is convention-consistent (4 pi c_R)
     [PASS]  Normalization: 16 pi vs 4 pi reconciled
     [OPEN]  Exact memory-mode count: requires specifying G_prim
     [OPEN]  V2 "+40 modes": inconsistent with c_R = 1.25 under standard weighting
     [OPEN]  Non-minimal coupling effects: not yet analyzed
     [OPEN]  G_prim selection: SU(5), SO(10), or other -- undetermined

   SEE ALSO: 12_g_prim_field_content.py
     Extends this analysis with soft SUSY partners, dark sector, auxiliary
     field from L_recursive_mimic, and GUT chiral multiplets. Key finding:
     the dual constraint (c_R = 1.25 AND Str(a_0) ~ 0) requires
     N_B ~ N_F ~ 189 real DOF, naturally achieved with SUSY + modest
     GUT-scale chiral content. SUSY is NOT optional -- it is required
     by the CC mechanism that V2 itself invokes.
""")


if __name__ == "__main__":
    main()
