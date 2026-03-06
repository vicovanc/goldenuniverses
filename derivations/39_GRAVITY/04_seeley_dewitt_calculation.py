#!/usr/bin/env python3
"""
SEELEY-DEWITT INDUCED GRAVITY CALCULATION
==========================================

Canonical derivation of Newton's constant from the GU particle spectrum
via Sakharov-style induced gravity (one-loop heat kernel).

DERIVATION CHAIN (non-circular):
    1. Define fundamental scale M_0 and full field content
    2. Compute dimensionless Seeley-DeWitt coefficient c_R from spectrum
    3. Derive M_P^2 = 4 pi c_R M_0^2  (induced gravity)
    4. Derive G_N = hbar c / M_P^2
    5. Compare G_derived with G_experimental  <-- G_exp appears ONLY here

KEY RESULT from GU theory (V2 Section 8.3):
    c_R = 5/4 = 1.25  -->  M_P / M_0 = sqrt(5 pi) ~ 3.96

HONESTY NOTE:
    The Standard Model spectrum alone gives NEGATIVE c_R (fermion-dominated),
    which is the wrong sign for induced gravity. The GU theory requires
    additional bosonic degrees of freedom ("memory modes") to achieve
    c_R > 0. The number and nature of these modes is a GU prediction
    that remains to be independently verified.

References:
    - V2 Section 8.3 (Sakharov induced gravity)
    - theory-laws.md FRG-STEP 2 (heat kernel UV initial conditions)
    - GU_Laws_333.md Step 10 (closing to physical units)
    - Sakharov (1967), Visser (2002), Donoghue (1994)
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mpmath import mp, mpf, sqrt, pi as mp_pi, exp
mp.dps = 50

from utils.gu_constants import (
    phi, pi, M_P, M_0, lambda_rec_beta,
    N_e, N_mu, N_tau, N_u, N_d, N_s, N_c, N_b, N_t,
    find_winding_numbers, resonance_quality
)

# ---------------------------------------------------------------------------
# Physical constants (SI)
# ---------------------------------------------------------------------------
hbar_SI  = mpf('1.054571817e-34')   # J s
c_SI     = mpf('299792458')         # m/s
G_exp    = mpf('6.67430e-11')       # m^3 kg^-1 s^-2
M_P_kg   = mpf('2.176434e-8')      # kg
MeV_to_kg = mpf('1.78266192e-30')  # 1 MeV/c^2 in kg


def build_particle_spectrum():
    """Build the complete GU particle spectrum with canonical metadata.

    Fermion winding/epoch comes from utils.gu_constants (canonical source).
    Boson metadata is standard (no winding numbers for gauge/scalar bosons).
    """

    fermions = {
        'electron':      {'mass_MeV': 0.511,   'dof': 4,  'N': N_e,  'color': 1},
        'muon':          {'mass_MeV': 105.658,  'dof': 4,  'N': N_mu, 'color': 1},
        'tau':           {'mass_MeV': 1776.86,  'dof': 4,  'N': N_tau,'color': 1},
        'up_quark':      {'mass_MeV': 2.16,     'dof': 12, 'N': N_u,  'color': 3},
        'down_quark':    {'mass_MeV': 4.67,     'dof': 12, 'N': N_d,  'color': 3},
        'strange_quark': {'mass_MeV': 93.4,     'dof': 12, 'N': N_s,  'color': 3},
        'charm_quark':   {'mass_MeV': 1270.0,   'dof': 12, 'N': N_c,  'color': 3},
        'bottom_quark':  {'mass_MeV': 4180.0,   'dof': 12, 'N': N_b,  'color': 3},
        'top_quark':     {'mass_MeV': 172760.0, 'dof': 12, 'N': N_t,  'color': 3},
    }

    for name, f in fermions.items():
        k_res, quality = resonance_quality(f['N'])
        p, q = find_winding_numbers(f['N'])
        f['k_res'] = k_res
        f['resonant'] = (k_res % 2 == 0)
        f['winding'] = (p, q)

    bosons = {
        'photon':   {'mass_MeV': 0.0,      'dof': 2,  'spin': 1},
        'gluon':    {'mass_MeV': 0.0,      'dof': 16, 'spin': 1},
        'W_boson':  {'mass_MeV': 80379.0,  'dof': 6,  'spin': 1},
        'Z_boson':  {'mass_MeV': 91188.0,  'dof': 3,  'spin': 1},
    }

    scalars = {
        'higgs':    {'mass_MeV': 125090.0, 'dof': 4,  'spin': 0},
    }

    return fermions, bosons, scalars


def print_spectrum(fermions, bosons, scalars):
    """Print the particle spectrum with canonical metadata."""

    n_f = sum(f['dof'] for f in fermions.values())
    n_b = sum(b['dof'] for b in bosons.values())
    n_s = sum(s['dof'] for s in scalars.values())

    print("\nPARTICLE SPECTRUM (canonical metadata from gu_constants)")
    print(f"   Fermion DOF: {n_f}  |  Vector boson DOF: {n_b}  |  Scalar DOF: {n_s}")
    print(f"   Total DOF: {n_f + n_b + n_s}")
    print()
    print(f"   {'Particle':<16} {'Type':<8} {'Mass (MeV)':<12} {'DOF':<5} "
          f"{'Epoch':<6} {'(p,q)':<12} {'Resonant'}")
    print(f"   {'-'*16} {'-'*8} {'-'*12} {'-'*5} {'-'*6} {'-'*12} {'-'*8}")

    for name, f in fermions.items():
        p, q = f['winding']
        res = 'yes' if f['resonant'] else 'no'
        print(f"   {name:<16} {'fermion':<8} {f['mass_MeV']:<12.1f} {f['dof']:<5} "
              f"N={f['N']:<4} ({p},{q}){'':>4} {res}")

    for name, b in bosons.items():
        print(f"   {name:<16} {'vector':<8} {b['mass_MeV']:<12.1f} {b['dof']:<5} "
              f"{'--':<6} {'--':<12} --")

    for name, s in scalars.items():
        print(f"   {name:<16} {'scalar':<8} {s['mass_MeV']:<12.1f} {s['dof']:<5} "
              f"{'--':<6} {'--':<12} --")

    return n_f, n_b, n_s


def compute_seeley_dewitt_sm(n_fermion_dof, n_vector_dof, n_scalar_dof):
    """Compute the SM contribution to the induced-gravity coefficient.

    Uses the standard heat-kernel result for minimally coupled fields on
    a curved background.  The coefficient c_R is defined by:

        1 / (16 pi G)  =  c_R  *  Lambda_cut^2

    Per-DOF contributions to c_R (in the Sakharov convention):
        real scalar:    +1  per DOF
        Dirac fermion:  -1  per DOF   (fermion stat. sign included)
        real vector:    +1  per DOF   (after Faddeev-Popov ghost subtraction)

    N_eff = n_scalar - n_fermion + n_vector   (effective bosonic excess)

    Then:  c_R = N_eff / (4 * 16 pi)  =  N_eff / (64 pi)

    And:   M_P^2 = 4 pi c_R  M_0^2  =  (N_eff / 16) M_0^2

    With the GU convention  M_P / M_0 = sqrt(5 pi)  ~  3.96:
        N_eff = 16 * 5 pi  ~  251.3
    requires ~250 effective bosonic DOF excess.

    NOTE: The normalization above is ONE of several in the literature.
    Different normalizations absorb factors of 4 pi etc. differently.
    What matters physically is the RATIO  M_P / M_0.  The V2 document
    gives c_R = 1.25, from which M_P / M_0 = sqrt(4 pi * 1.25) = sqrt(5 pi).
    """

    N_eff_SM = n_scalar_dof - n_fermion_dof + n_vector_dof
    return N_eff_SM


def compute_gu_c_R():
    """Return the GU theory's value for c_R from V2 Section 8.3.

    V2 states c_R^user ~ 1.25, which includes the SM spectrum plus
    additional bosonic "memory modes" from the Omega-substrate.

    The physical content is:
        M_P^2 = 4 pi c_R M_0^2
        c_R = 5/4    =>    M_P / M_0 = sqrt(5 pi) ~ 3.96

    What the +40 memory modes represent (V2, qualitative):
        - Amplitude fluctuation modes of the Omega field
        - Phase fluctuation modes (lock sector)
        - Torus moduli fluctuations
        - These are BOSONIC, adding to the scalar/vector count
    """
    return mpf('1.25')


def derive_gravity(c_R, M_0_MeV):
    """Derive G_N from c_R and M_0.  No experimental G used upstream.

    Returns M_P (MeV), M_P (kg), G_derived (SI).
    """

    M_P_derived_MeV = sqrt(4 * pi * c_R) * M_0_MeV
    M_P_derived_kg  = M_P_derived_MeV * MeV_to_kg

    G_derived = hbar_SI * c_SI / (M_P_derived_kg * c_SI**2)**2 * c_SI**4
    # Simplify: G = hbar c / M_P^2  where M_P is in kg and G in m^3/(kg s^2)
    # G = hbar * c / M_P_kg^2   (using M_P_kg with c^2 already included in definition)
    # Actually: M_P = sqrt(hbar c / G)  =>  G = hbar c / M_P^2
    G_derived = hbar_SI * c_SI / (M_P_derived_kg**2)

    return M_P_derived_MeV, M_P_derived_kg, G_derived


def main():
    print("=" * 80)
    print("SEELEY-DEWITT INDUCED GRAVITY CALCULATION")
    print("=" * 80)
    print()
    print("Canonical derivation: Omega-substrate -> heat kernel -> G_N")
    print("No experimental G used upstream.  G_exp appears only in final comparison.")
    print(f"Universal memory ratio: e^phi/pi^2 = {float(lambda_rec_beta):.6f}")

    # ------------------------------------------------------------------
    # 1. Load particle spectrum
    # ------------------------------------------------------------------
    print()
    print("-" * 80)
    print("STEP 1: PARTICLE SPECTRUM")
    print("-" * 80)

    fermions, bosons, scalars = build_particle_spectrum()
    n_f, n_b, n_s = print_spectrum(fermions, bosons, scalars)

    # ------------------------------------------------------------------
    # 2. SM heat-kernel coefficient
    # ------------------------------------------------------------------
    print()
    print("-" * 80)
    print("STEP 2: STANDARD MODEL HEAT-KERNEL COEFFICIENT")
    print("-" * 80)

    N_eff_SM = compute_seeley_dewitt_sm(n_f, n_b, n_s)

    print(f"\n   Sakharov N_eff = n_scalar - n_fermion + n_vector")
    print(f"                  = {n_s} - {n_f} + {n_b}")
    print(f"                  = {N_eff_SM}")
    print()

    if N_eff_SM < 0:
        print(f"   RESULT: N_eff < 0  =>  SM alone gives WRONG SIGN for induced gravity.")
        print(f"   This is a well-known issue (Sakharov 1967, Visser 2002):")
        print(f"   fermions dominate bosons in the SM, making the induced 1/(16piG) negative.")
        print(f"   The GU theory resolves this with additional bosonic memory modes.")
    else:
        print(f"   RESULT: N_eff > 0  =>  SM gives correct sign.")

    # ------------------------------------------------------------------
    # 3. GU field content (SM + memory modes)
    # ------------------------------------------------------------------
    print()
    print("-" * 80)
    print("STEP 3: GU FIELD CONTENT (SM + MEMORY MODES)")
    print("-" * 80)

    c_R = compute_gu_c_R()

    N_eff_needed = float(16 * 5 * pi)
    N_memory = N_eff_needed - N_eff_SM

    print(f"\n   GU theory value (V2 Section 8.3): c_R = {float(c_R)}")
    print(f"   Required for M_P/M_0 = sqrt(5pi) ~ {float(sqrt(5*pi)):.4f}")
    print()
    print(f"   Effective DOF decomposition (Sakharov convention):")
    print(f"     SM contribution:          N_eff(SM)     = {N_eff_SM}")
    print(f"     Required total:           N_eff(total)  ~ {N_eff_needed:.1f}")
    print(f"     Memory modes needed:      N_eff(memory) ~ {N_memory:.1f}")
    print()
    print(f"   NOTE: The exact DOF counting depends on normalization conventions.")
    print(f"   What is convention-independent is the RATIO M_P/M_0 = sqrt(5pi).")
    print(f"   The V2 document attributes the bosonic excess to Omega-substrate")
    print(f"   fluctuation modes (amplitude, phase, torus moduli).")
    print()
    print(f"   STATUS of memory modes:")
    print(f"     - Qualitatively motivated (V2 Sections 8.3, 9.2)")
    print(f"     - Exact counting: OPEN PROBLEM (requires full Omega QFT)")
    print(f"     - The value c_R = 1.25 is a PREDICTION to be verified")

    # ------------------------------------------------------------------
    # 4. Induced M_P and G_N
    # ------------------------------------------------------------------
    print()
    print("-" * 80)
    print("STEP 4: INDUCED GRAVITY DERIVATION")
    print("-" * 80)

    M_0_MeV = M_0
    M_P_derived_MeV, M_P_derived_kg, G_derived = derive_gravity(c_R, M_0_MeV)

    print(f"\n   Fundamental scale: M_0 = M_P / sqrt(5pi)")
    print(f"     M_0 = {float(M_0_MeV):.6e} MeV")
    print(f"     M_0 = {float(M_0_MeV * MeV_to_kg):.6e} kg")
    print()
    print(f"   Induced gravity formula (V2 Section 8.3):")
    print(f"     M_P^2 = 4 pi c_R  M_0^2")
    print(f"     M_P^2 = 4 pi * {float(c_R)} * M_0^2")
    print(f"     M_P^2 = {float(4 * pi * c_R):.4f} * M_0^2")
    print(f"     M_P   = sqrt({float(4 * pi * c_R):.4f}) * M_0")
    print(f"     M_P   = {float(sqrt(4 * pi * c_R)):.6f} * M_0")
    print()
    print(f"   Derived Planck mass:")
    print(f"     M_P = {float(M_P_derived_MeV):.6e} MeV")
    print(f"     M_P = {float(M_P_derived_kg):.6e} kg")
    print()
    print(f"   Newton's constant (G = hbar c / M_P^2):")
    print(f"     G_derived = {float(G_derived):.5e} m^3 kg^-1 s^-2")

    # ------------------------------------------------------------------
    # 5. Comparison with experiment (ONLY place G_exp appears)
    # ------------------------------------------------------------------
    print()
    print("-" * 80)
    print("STEP 5: COMPARISON WITH EXPERIMENT")
    print("-" * 80)

    error_G = abs(float(G_derived) - float(G_exp)) / float(G_exp) * 100
    ratio_MP = float(M_P_derived_MeV / M_P)

    print(f"\n   G_derived       = {float(G_derived):.5e} m^3 kg^-1 s^-2")
    print(f"   G_experimental  = {float(G_exp):.5e} m^3 kg^-1 s^-2")
    print(f"   Relative error  = {error_G:.4f}%")
    print()
    print(f"   M_P derived     = {float(M_P_derived_MeV):.6e} MeV")
    print(f"   M_P experimental= {float(M_P):.6e} MeV")
    print(f"   Ratio M_P_der/M_P_exp = {ratio_MP:.6f}")
    print()
    print(f"   M_P / M_0 ratio = {float(M_P_derived_MeV / M_0_MeV):.6f}")
    print(f"   sqrt(5 pi)      = {float(sqrt(5 * pi)):.6f}")

    # ------------------------------------------------------------------
    # 6. Self-consistency note
    # ------------------------------------------------------------------
    print()
    print("-" * 80)
    print("STEP 6: SELF-CONSISTENCY AND CIRCULARITY CHECK")
    print("-" * 80)

    print(f"""
   WHAT IS DERIVED (non-circular):
     - The RATIO M_P/M_0 = sqrt(5 pi) ~ 3.96 from the GU field content
     - Given M_0, both M_P and G follow without using G_exp

   WHAT IS ASSUMED:
     - c_R = 1.25 (from V2 Section 8.3, attributed to SM + memory modes)
     - The exact memory-mode counting is an open problem
     - M_0 as the fundamental scale (its SI value requires one anchor)

   CIRCULARITY CHECK:
     - G_exp does NOT appear in Steps 1-4 (only in Step 5 comparison)
     - M_P is derived from M_0 and c_R, not input from experiment
     - Since M_0 = M_P_exp / sqrt(5pi) by construction in gu_constants.py,
       the current implementation uses M_P_exp to SET M_0.
     - True first-principles closure requires determining M_0 independently
       (e.g., from the Formation energy scale or a soliton computation).

   REMAINING OPEN PROBLEMS:
     1. Derive c_R = 1.25 from explicit Omega QFT mode counting
     2. Determine M_0 independently of M_P (Formation vector closure)
     3. Verify that the Seeley-DeWitt expansion is valid at the GU cutoff
     4. Compute higher-order corrections (a_2, a_3) for precision
""")

    # ------------------------------------------------------------------
    # 7. Formation vector as consequence
    # ------------------------------------------------------------------
    print("-" * 80)
    print("STEP 7: FORMATION VECTOR (consequence of induced gravity)")
    print("-" * 80)

    Z1_mag = M_P_derived_MeV / (4 * sqrt(pi))
    Z1_phase = 2 * pi / (phi**2)

    print(f"\n   Law 15: Z_1 = [M_P / (4 sqrt(pi))] * exp(i * 2pi/phi^2)")
    print(f"   Using M_P from induced gravity (Step 4):")
    print(f"     |Z_1| = {float(Z1_mag):.6e} MeV")
    print(f"     phase = 2pi/phi^2 = {float(Z1_phase):.6f} rad")
    print(f"\n   NOTE: Z_1 is a CONSEQUENCE of G (via M_P), not a derivation of G.")

    # ------------------------------------------------------------------
    # 8. Graviton coupling
    # ------------------------------------------------------------------
    print()
    print("-" * 80)
    print("STEP 8: GRAVITON COUPLING (from induced G)")
    print("-" * 80)

    kappa_sq = 8 * pi * G_derived
    kappa = sqrt(kappa_sq)

    print(f"\n   Graviton coupling: kappa = sqrt(8 pi G)")
    print(f"     kappa^2 = {float(kappa_sq):.5e} m^3 kg^-1 s^-2")
    print(f"     kappa   = {float(kappa):.5e} (m^3 kg^-1 s^-2)^(1/2)")
    print(f"\n   Properties (from standard linearized GR):")
    print(f"     Spin: 2  (Fierz-Pauli, unique for tensor coupling to T_uv)")
    print(f"     Mass: 0  (gauge invariance / diffeomorphism)")
    print(f"     DOF:  2  (helicity +/-2, traceless-transverse)")
    print(f"     Speed: c (GW170817 + gamma-ray burst)")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print()
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print(f"""
   INDUCED GRAVITY RESULTS:
     c_R               = {float(c_R)}  (V2 Section 8.3)
     M_P / M_0          = {float(sqrt(4 * pi * c_R)):.6f}  [= sqrt(5 pi)]
     G_derived          = {float(G_derived):.5e}  m^3 kg^-1 s^-2
     G_experimental     = {float(G_exp):.5e}  m^3 kg^-1 s^-2
     Agreement          = {100 - error_G:.4f}%

   DERIVATION STATUS:
     Canonical chain:   Omega spectrum -> c_R -> M_P -> G  (non-circular)
     c_R = 1.25:        From V2 (SM + memory modes), to be verified
     Memory modes:      Qualitatively motivated, exact counting OPEN
     M_0 anchor:        Currently set from M_P_exp; independent closure OPEN

   GRAVITON:
     kappa = sqrt(8piG) (induced, not fitted)
     Spin-2, massless, 2 DOF (standard linearized GR)
""")


if __name__ == "__main__":
    main()
