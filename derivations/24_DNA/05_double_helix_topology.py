#!/usr/bin/env python3
"""
DOUBLE HELIX TOPOLOGY FROM GU
=================================

The DNA double helix is a topological structure characterised by:
  - Helical rise (3.4 A per base pair)
  - Helical twist (36 deg per base pair, 10 bp per turn)
  - Linking number Lk = Tw + Wr (topological invariant)

In GU, the linking number is a WINDING NUMBER on the molecular
Omega-torus — the macroscopic analogue of (p,q) = (-41, 70) for
the electron. Supercoiling = deviation from the equilibrium winding.

Upstream: 23_MOLECULAR_BONDS/05_bond_order_from_topology.py
Status:   Standard biophysics with GU topological interpretation

Date: February 2026
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mpmath import mp, mpf, sqrt, pi as mp_pi, exp, cos, sin, atan2
import numpy as np

mp.dps = 30
phi = (mpf('1') + sqrt(mpf('5'))) / 2
pi = mp_pi
alpha_EM = mpf('1') / mpf('137.035999177')
m_e = mpf('0.51099895')
hbar_c = mpf('197.3269804')
a_0_fm = float(hbar_c / (alpha_EM * m_e))
a_0_A = a_0_fm / 1e5

print("=" * 80)
print("DOUBLE HELIX TOPOLOGY FROM GU")
print("Winding numbers and topological invariants of DNA")
print("=" * 80)


# ============================================================================
# PART 1: B-DNA HELICAL PARAMETERS
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 1: B-DNA HELICAL PARAMETERS                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

B-DNA (the standard biological form) has well-defined helical geometry:
""")

rise_A = 3.4            # Angstrom per base pair
twist_deg = 36.0        # degrees per base pair
bp_per_turn = 360.0 / twist_deg
pitch_A = rise_A * bp_per_turn
diameter_A = 20.0       # approximate
radius_A = diameter_A / 2.0
pitch_angle_deg = np.degrees(np.arctan(pitch_A / (2 * np.pi * radius_A)))

print(f"  Rise per base pair:     h = {rise_A} A = {rise_A/a_0_A:.1f} a_0")
print(f"  Twist per base pair:    t = {twist_deg} deg")
print(f"  Base pairs per turn:    n = {bp_per_turn:.1f}")
print(f"  Helical pitch:          P = {pitch_A:.1f} A = {pitch_A/a_0_A:.0f} a_0")
print(f"  Helix diameter:         D = {diameter_A:.0f} A = {diameter_A/a_0_A:.0f} a_0")
print(f"  Helix radius:           R = {radius_A:.0f} A")
print(f"  Pitch angle:            gamma = {pitch_angle_deg:.1f} deg")
print()

print("""  The helix is RIGHT-HANDED (positive twist when viewed from above).
  Two strands wind around the central axis in parallel, offset by
  ~154 degrees (minor groove) or ~206 degrees (major groove).
""")


# ============================================================================
# PART 2: MAJOR AND MINOR GROOVES
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 2: MAJOR AND MINOR GROOVES                                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

The two strands of DNA do NOT divide the surface equally — they create
two grooves of different widths:
""")

major_groove_width_A = 22.0
minor_groove_width_A = 12.0
major_groove_depth_A = 8.5
minor_groove_depth_A = 7.5

minor_angle_deg = 154.0
major_angle_deg = 360.0 - minor_angle_deg

print(f"  Major groove:")
print(f"    Angular span:  {major_angle_deg:.0f} deg")
print(f"    Width:         {major_groove_width_A:.0f} A = {major_groove_width_A/a_0_A:.0f} a_0")
print(f"    Depth:         {major_groove_depth_A:.1f} A")
print()
print(f"  Minor groove:")
print(f"    Angular span:  {minor_angle_deg:.0f} deg")
print(f"    Width:         {minor_groove_width_A:.0f} A = {minor_groove_width_A/a_0_A:.0f} a_0")
print(f"    Depth:         {minor_groove_depth_A:.1f} A")
print()

print("""  The ASYMMETRY between grooves is biologically crucial:
    - Major groove: proteins read the base sequence here
      (H-bond patterns are distinguishable in the major groove)
    - Minor groove: narrower, less information-rich

  GU INTERPRETATION:
    The groove asymmetry arises from the GLYCOSIDIC BOND ANGLE —
    the angle at which each base attaches to the sugar-phosphate backbone.
    This angle breaks the 2-fold symmetry of the base pair.

    In phase topology terms: the phase gradient nabla_theta along the
    pi-stack has a component that winds around the helix, creating
    asymmetric coupling to the two strands. The major groove side
    has MORE accessible phase information (wider, more exposed base edges).
""")


# ============================================================================
# PART 3: THE LINKING NUMBER THEOREM
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 3: THE LINKING NUMBER THEOREM                                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

For CLOSED circular DNA (found in bacteria, plasmids, mitochondria):

  The LINKING NUMBER Lk is a TOPOLOGICAL INVARIANT.
  It cannot be changed without cutting a strand.

  LINKING NUMBER THEOREM:
    Lk = Tw + Wr

  where:
    Tw = TWIST = number of times the strands wind around each other
         (sum of local helical turns)
    Wr = WRITHE = number of times the helix axis crosses itself
         (supercoiling)
    Lk = INTEGER (for closed DNA, this is exactly quantised)
""")

N_bp_plasmid = 5000
Lk_relaxed = N_bp_plasmid / bp_per_turn
Tw_relaxed = Lk_relaxed
Wr_relaxed = 0.0

print(f"  Example: 5000 bp circular plasmid")
print(f"    Relaxed state:")
print(f"      Lk_0 = N_bp / n = {N_bp_plasmid} / {bp_per_turn:.0f} = {Lk_relaxed:.0f}")
print(f"      Tw_0 = {Tw_relaxed:.0f}")
print(f"      Wr_0 = {Wr_relaxed:.0f}")
print()

sigma_typical = -0.06  # typical superhelical density in bacteria
delta_Lk = sigma_typical * Lk_relaxed
Lk_super = Lk_relaxed + delta_Lk

print(f"    Supercoiled state (sigma = {sigma_typical}):")
print(f"      Delta_Lk = sigma * Lk_0 = {delta_Lk:.0f}")
print(f"      Lk = {Lk_super:.0f}")
print(f"      This deficit is partitioned between Tw and Wr:")
print(f"        If all in Tw: 500 - 30 = 470 turns (underwound)")
print(f"        If all in Wr: 30 negative crossings (plectonemic)")
print(f"        Reality: roughly 75% Wr + 25% Tw change")
print()


# ============================================================================
# PART 4: GU INTERPRETATION — WINDING NUMBER ON THE MOLECULAR TORUS
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 4: GU INTERPRETATION — Lk AS A WINDING NUMBER                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

In GU, the electron is a kink soliton on the Omega-torus with winding
numbers (p, q) = (-41, 70). The linking number Lk of DNA is the
MACROSCOPIC ANALOGUE of this topological quantum number.

  ELECTRON TORUS:
    Winding (p, q) = (-41, 70)
    Torus circumference: l_Omega = 2*pi*sqrt(p^2 + q^2/phi^2) = 374.50
    These are FIXED by the SU(5) lattice and phi geometry.

  DNA MOLECULAR TORUS:
    The two sugar-phosphate backbones wind around the central pi-stack
    axis, like two threads wound around a cylinder.
    Winding: Lk = N_bp / 10 (for relaxed B-DNA)
    This number depends on the DNA LENGTH (not fixed like the electron).
""")

p_e, q_e = -41, 70
l_omega = float(2 * pi * sqrt(mpf(p_e**2) + mpf(q_e**2) / phi**2))

print(f"  COMPARISON TABLE:")
print(f"  {'Property':>25s} | {'Electron':>20s} | {'DNA (5000 bp)':>20s}")
print("  " + "-" * 70)
print(f"  {'Winding numbers':>25s} | {'(p,q) = (-41, 70)':>20s} | {'Lk = 500':>20s}")
print(f"  {'Torus size':>25s} | {'l = 374.5 (dimless)':>20s} | {'P = 34 A (physical)':>20s}")
print(f"  {'Quantised?':>25s} | {'Yes (lattice)':>20s} | {'Yes (Lk integer)':>20s}")
print(f"  {'Fixed?':>25s} | {'Yes (topology)':>20s} | {'No (length-dep.)':>20s}")
print(f"  {'Changed by':>25s} | {'Cannot change':>20s} | {'Topoisomerases':>20s}")
print()

print("""  KEY DIFFERENCE:
    The electron's winding is INTRINSIC — it comes from the SU(5) lattice
    and cannot be changed. The electron IS its winding.

    DNA's linking number is EXTRINSIC — it depends on the length and can
    be changed by topoisomerase enzymes (which cut and rejoin strands).
    But for a given closed molecule at a given time, Lk is EXACTLY
    quantised (integer) and topologically protected.

  KEY SIMILARITY:
    Both are TOPOLOGICAL INVARIANTS: they count the number of times
    one path winds around another. In GU, all such winding numbers
    come from the Omega-field phase theta winding on a torus.
""")


# ============================================================================
# PART 5: THE 36-DEGREE TWIST — IS THERE A PHI CONNECTION?
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 5: THE 36-DEGREE TWIST — GOLDEN ANGLE INVESTIGATION                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

The DNA twist is 36 degrees per base pair. This gives 10 bp per turn.
Is there a connection to the golden ratio phi?
""")

golden_angle = float(360.0 / phi**2)
twist_dna = 36.0
ratio_twist_golden = twist_dna / golden_angle

print(f"  Golden angle:        360/phi^2 = {golden_angle:.3f} deg")
print(f"  DNA twist:           {twist_dna:.1f} deg per bp")
print(f"  Ratio:               {ratio_twist_golden:.4f}")
print()

complement_golden = 360.0 - golden_angle
factor_36_360 = 360.0 / twist_dna
print(f"  360 / 36 = {factor_36_360:.0f}  (10 bp per turn)")
print(f"  36 = 360/10  (simply 1/10 of a full turn)")
print()

print(f"  Related angles in geometry:")
print(f"    Interior angle of regular pentagon: 108 deg = 3 * 36")
print(f"    Exterior angle of regular pentagon:  72 deg = 2 * 36")
print(f"    36 deg = pi/5 radians")
print()

print("""  HONEST ASSESSMENT:
    36 degrees IS related to phi through the regular pentagon:
      cos(36 deg) = cos(pi/5) = phi/2 = 0.809
      cos(72 deg) = cos(2*pi/5) = (phi-1)/2 = 0.309

    And 36 = 360/10 where 10 = 2 * 5 involves the pentagon number.

    BUT: the DNA twist of ~36 degrees is set by the SUGAR-PHOSPHATE
    BACKBONE GEOMETRY — bond angles, steric constraints, and the
    torsion angles of the backbone atoms. It is NOT directly set by
    phi at the fundamental level.

    The connection 36 = pi/5 → cos(36) = phi/2 is NUMEROLOGICAL
    at this stage. It would need to be derived from the backbone
    torsion potential (which itself comes from m_e and alpha_EM)
    to be a genuine GU prediction.

    We note the connection but do NOT claim it as a derivation.
""")


# ============================================================================
# PART 6: SUPERCOILING AS TOPOLOGICAL STRAIN
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 6: SUPERCOILING — TOPOLOGICAL STRAIN ENERGY                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

When Lk differs from the relaxed value Lk_0 = N/10, the DNA is
SUPERCOILED. This stores elastic energy:

  Delta_Lk = Lk - Lk_0 = sigma * Lk_0

  sigma = superhelical density (typically -0.06 for bacterial DNA)
  Negative sigma → underwound → DNA tends to unwind locally

  Elastic energy:
    E_sc = (C * 2*pi^2 / L) * Delta_Lk^2

  where C ~ 3 × 10^(-19) J·m is the torsional rigidity
  and L is the DNA length.
""")

C_torsion = 3e-19  # J·m
L_plasmid = N_bp_plasmid * rise_A * 1e-10  # meters

E_sc_J = C_torsion * 2 * np.pi**2 / L_plasmid * delta_Lk**2
E_sc_eV = E_sc_J / 1.602e-19
E_sc_per_bp = E_sc_eV / N_bp_plasmid

print(f"  For a 5000 bp plasmid with sigma = {sigma_typical}:")
print(f"    Length:        L = {L_plasmid*1e6:.2f} um")
print(f"    Delta_Lk:      {delta_Lk:.0f}")
print(f"    E_supercoil:   {E_sc_eV:.1f} eV total")
print(f"    Per base pair: {E_sc_per_bp:.4f} eV")
print()

print("""  GU INTERPRETATION:
    Supercoiling is analogous to winding the Omega-field phase AWAY
    from the V_lock minimum:

      V_lock = Lambda_1 [1 - cos(Delta_theta)]

    In the equilibrium helix (Lk = Lk_0), the phase sits at the
    minimum of V_lock. When Delta_Lk != 0, the phase is displaced
    from the minimum, storing energy:

      E ~ Lambda_1 * (Delta_theta)^2 / 2   (harmonic approximation)

    where Delta_theta = 2*pi * Delta_Lk / N_bp.

    This is the SAME physics as the lock potential for molecular bonds
    (23_MOLECULAR_BONDS/05_bond_order_from_topology.py), but applied
    to the macroscopic helical winding.

    Topoisomerase enzymes that change Lk are performing TOPOLOGICAL
    SURGERY — cutting the Omega-field phase path and reconnecting it
    with a different winding number. This is the molecular analogue
    of creating/destroying vortices.
""")


# ============================================================================
# PART 7: DNA FORMS — A, B, Z
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 7: DNA STRUCTURAL FORMS — A, B, Z                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

DNA can adopt several helical forms depending on conditions:
""")

forms = [
    ('B-DNA', 'right', 10.0, 3.4, 36.0, 20.0, 'physiological, most common'),
    ('A-DNA', 'right', 11.0, 2.6, 32.7, 23.0, 'dehydrated, RNA duplexes'),
    ('Z-DNA', 'left',  12.0, 3.7, -30.0, 18.0, 'alternating purine/pyrimidine'),
]

print(f"  {'Form':>6s} | {'Hand':>5s} | {'bp/turn':>7s} | {'Rise(A)':>7s} | {'Twist':>6s} | {'D(A)':>5s} | {'Condition'}")
print("  " + "-" * 75)
for form, hand, bpt, rise, tw, diam, cond in forms:
    print(f"  {form:>6s} | {hand:>5s} | {bpt:>7.1f} | {rise:>7.1f} | {tw:>6.1f} | {diam:>5.0f} | {cond}")

print()

print("""  GU NOTE ON Z-DNA:
    Z-DNA is LEFT-HANDED — the twist has OPPOSITE SIGN to B-DNA.
    In topological terms, Z-DNA has NEGATIVE winding relative to B-DNA.

    A B-to-Z transition changes the local twist by ~66 degrees per
    base pair, which is a LARGE topological rearrangement.

    In GU phase language, B-to-Z is a transition between two
    different V_lock minima — one with positive winding, one with
    negative winding. The transition requires passing over the
    lock-potential barrier.

    Z-DNA segments in otherwise B-DNA create PHASE DOMAIN WALLS —
    boundaries where the winding direction changes. These are
    topological defects in the phase field, analogous to domain
    walls in ferromagnets.
""")


# ============================================================================
# SUMMARY
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  SUMMARY: DOUBLE HELIX TOPOLOGY FROM GU                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

HELICAL PARAMETERS:
  Rise = 3.4 A, Twist = 36 deg/bp, 10 bp/turn, Pitch = 34 A
  Diameter = 20 A, Major groove = 22 A, Minor groove = 12 A

TOPOLOGICAL INVARIANT:
  Linking number Lk = Tw + Wr (integer for closed DNA)
  Analogous to electron winding (p,q) = (-41, 70) on the Omega-torus
  Lk is EXACTLY QUANTISED and topologically protected

GU INTERPRETATION:
  1. Lk is a winding number on the molecular Omega-torus
  2. Supercoiling (Delta_Lk != 0) = topological strain energy
     (phase displaced from V_lock minimum)
  3. Topoisomerases = topological surgery (change winding number)
  4. B-to-Z transition = phase domain wall (winding sign flip)
  5. The 36 deg = pi/5 connection to phi is NOTED but NOT CLAIMED
     as a derivation (backbone geometry needs explicit calculation)

KEY DISTINCTION FROM ELECTRON:
  Electron winding: intrinsic, fixed by SU(5) lattice
  DNA winding: extrinsic, length-dependent, enzyme-modifiable
  Both: topologically quantised (integer), from Omega-field phase

CONNECTIONS:
  -> Script 04: Pi-stacking creates the column that winds
  -> Script 06: Supercoiling energy in the stability budget
  -> Script 07: Topological protection → information persistence
""")
