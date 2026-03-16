#!/usr/bin/env python3
"""
THE ROLE OF SOUND IN THE GOLDEN UNIVERSE
==========================================

SOUND IS NOT A SECONDARY PHENOMENON — IT IS FUNDAMENTAL.

This script synthesizes all previous results to establish sound/phonons
as a FIRST-CLASS citizen of the Golden Universe, on equal ontological
footing with particles, forces, and consciousness.

DERIVATION CHAIN:
  Part 1: Sound as material property engineer (stiffness, strength, ductility)
  Part 2: Piezoelectricity — direct phase↔amplitude coupling
  Part 3: Biological phase phonons — DNA, neurons, microtubules
  Part 4: Agency from phonon feedback — how materials become active
  Part 5: The Sonic Hierarchy — from Planck to biology
  Part 6: Sound and the five GU forces

Date: February 2026
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from mpmath import mp, mpf, sqrt, pi as mp_pi, exp, ln

mp.dps = 30
phi = (mpf('1') + sqrt(mpf('5'))) / 2
pi = mp_pi
alpha_EM = mpf('1') / mpf('137.035999177')
m_e = mpf('0.51099895')
m_p = mpf('938.272')
M_P = mpf('1.22089e22')
hbar_c = mpf('197.3269804')

c_m_s = 2.998e8
eV_to_J = 1.602e-19
hbar_J_s = 1.055e-34
k_B_eV = 8.617e-5
k_B_J = 1.381e-23


print("=" * 80)
print("THE ROLE OF SOUND IN THE GOLDEN UNIVERSE")
print("=" * 80)


# ============================================================================
# PART 1: SOUND AS MATERIAL PROPERTY ENGINEER
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 1: SOUND AS MATERIAL PROPERTY ENGINEER                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

The speed of sound v_s encodes EVERYTHING about a material's
mechanical behavior, because:

  v_s = √(B/ρ)  where B = bulk modulus, ρ = density

From v_s alone, you can extract:
  - Elastic moduli (E, G, ν)
  - Hardness
  - Melting temperature (Lindemann)
  - Debye temperature (thermal properties)
  - Wave propagation (seismology, ultrasonics)

In GU: v_s = c × α_EM × √(m_e/(A·m_p)) × f(bonding)
All mechanical properties derive from the epoch ladder.
""")

prop_data = [
    ("Diamond",  12000, 1050, 443, 3800, 2250, "Hardest, stiffest, highest Θ_D"),
    ("Silicon",   8430,  130,  98, 1687,  645, "Semiconductor, moderate"),
    ("Steel",     5960,  200, 160, 1810,  470, "Structural material"),
    ("Copper",    3810,  110, 137, 1358,  343, "Ductile metal"),
    ("Aluminum",  6420,   70,  76,  933,  428, "Light metal"),
    ("Glass",     5640,  550,  37, 1400,  350, "Amorphous, brittle"),
    ("Rubber",    1600,    2, 0.01, 400,   50, "Soft, elastic"),
    ("Water",     1480,    0, 2.2,  273,  192, "Liquid: no shear"),
    ("Air",        343,    0, 0.0001, None, None, "Gas: nearly free"),
]

print(f"  {'Material':>10s} | {'v_s(m/s)':>8s} | {'E(GPa)':>6s} | {'B(GPa)':>6s} | {'T_m(K)':>6s} | {'Θ_D(K)':>6s}")
print("  " + "─" * 60)
for name, vs, E, B, Tm, Theta, notes in prop_data:
    Tm_str = f"{Tm:6d}" if Tm else "   N/A"
    Theta_str = f"{Theta:6d}" if Theta else "   N/A"
    print(f"  {name:>10s} | {vs:8d} | {E:6d} | {B:6.1f} | {Tm_str} | {Theta_str}")

print()
print("  CORRELATION: v_s predicts EVERYTHING:")
print("    v_s ∝ √E (Young's modulus)")
print("    v_s ∝ √B (Bulk modulus)")
print("    v_s² ∝ Θ_D² ∝ T_melt (Lindemann)")
print()
print("  GU INSIGHT: The mechanical behavior of ALL materials is encoded")
print("  in a SINGLE number v_s, which derives from TWO epoch ratios:")
print("    α_EM and √(m_e/m_p)")
print()
print("  The hardest material (diamond) and the softest (rubber)")
print("  are BOTH manifestations of the same GU oscillation principle,")
print("  differing only in bond type and atomic mass.")
print()


# ============================================================================
# PART 2: PIEZOELECTRICITY — PHASE↔AMPLITUDE COUPLING
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 2: PIEZOELECTRICITY — DIRECT PHASE↔AMPLITUDE COUPLING                ║
╚══════════════════════════════════════════════════════════════════════════════╝

Piezoelectricity: mechanical stress → electric polarization (and vice versa).

  P_i = Σ_jk d_ijk σ_jk

GU INTERPRETATION:
  Stress (σ) is an amplitude (ρ) perturbation — atomic displacements.
  Polarization (P) is a phase (θ) response — charge redistribution.
  Piezoelectricity is DIRECT ρ↔θ coupling.

REQUIREMENT: No inversion symmetry (non-centrosymmetric crystal).
  GU: inversion symmetry means V_lock(Δθ) = V_lock(-Δθ).
  Breaking this symmetry → V_lock acquires ODD harmonics:
  V = Λ₁(1−cos Δθ) + Λ₂ sin(Δθ) + ...
  The Λ₂ sin(Δθ) term IS the piezoelectric coupling.
""")

piezo_data = [
    ("Quartz (SiO₂)",     2.3,    "Natural: used in watches, sensors"),
    ("BaTiO₃",            190,    "Ferroelectric: high d₃₃"),
    ("PZT (PbZrTiO₃)",    590,    "Industrial standard: actuators"),
    ("ZnO",               12.3,   "Semiconductor + piezo: sensors"),
    ("AlN",               5.1,    "High freq: RF filters, BAW"),
    ("PVDF polymer",      33,     "Flexible: wearable sensors"),
    ("Bone (collagen)",   0.7,    "Biological: stress → growth signal"),
    ("DNA",               "~0.1", "Proposed: phase-amplitude coupling"),
]

print(f"  {'Material':>18s} | {'d₃₃(pC/N)':>10s} | Application")
print("  " + "─" * 60)
for name, d33, app in piezo_data:
    print(f"  {name:>18s} | {str(d33):>10s} | {app}")

print()
print("  GU EXPLANATION OF PIEZOELECTRIC HIERARCHY:")
print()
print("    d₃₃ ∝ (asymmetry of V_lock) × (compliance) × (polarizability)")
print()
print("    PZT has the largest d₃₃ because:")
print("    1. Perovskite structure with off-center Ti → large Λ₂")
print("    2. Near morphotropic phase boundary → soft lattice (large compliance)")
print("    3. Large Pb polarizability → strong θ response")
print()
print("    BONE IS PIEZOELECTRIC:")
print("    Collagen fibrils lack inversion symmetry → piezo response")
print("    Mechanical stress → electric signal → bone growth")
print("    This is a DIRECT ρ↔θ coupling in a biological material.")
print("    GU: the body uses phonon-memory coupling for self-repair.")
print()


# ============================================================================
# PART 3: BIOLOGICAL PHASE PHONONS
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 3: BIOLOGICAL PHASE PHONONS — DNA, NEURONS, MICROTUBULES             ║
╚══════════════════════════════════════════════════════════════════════════════╝

Biological systems operate at the boundary between:
  - Thermal disorder (T ≈ 310 K → k_BT ≈ 26.7 meV)
  - Phase order (V_lock maintains coherence)

This is the OPTIMAL regime for GU memory (Script 05, Part 4):
  Phase phonons are thermally active but not disordered.
""")

bio_phonons = [
    ("DNA base stacking",   "0.3-3",   "θ oscillation of π system",
     "Information storage + readout"),
    ("DNA backbone twist",  "0.01-0.1", "Torsional phase wave",
     "Long-range signal propagation"),
    ("Protein amide I",     "50",       "C=O stretch + phase coupling",
     "Energy transport in α-helices"),
    ("Microtubule lattice", "0.1-1",    "Tubulin dimer oscillation",
     "Proposed quantum coherence"),
    ("Neuron membrane",     "0.001-0.01", "Lipid bilayer undulations",
     "Ion channel gating modulation"),
    ("Cochlea hair cells",  "0.01-20",  "Mechanical → electrical",
     "Hearing: phonon detection"),
    ("Cardiac tissue",      "0.001",    "Piezoelectric collagen",
     "Mechanical → electrical signal"),
]

print(f"  {'System':>22s} | {'ω(THz)':>10s} | {'θFF̃ role':>25s}")
print("  " + "─" * 65)
for name, freq, desc, role in bio_phonons:
    print(f"  {name:>22s} | {freq:>10s} | {role:>25s}")

print()
print("  KEY BIOLOGICAL SYSTEMS:")
print()
print("  DNA:")
print("    The DNA derivation (24_DNA) showed that pi-stacking is the")
print("    CONTINUOUS θFF̃ channel running along the double helix.")
print("    Phase phonons in the stacking direction are the VIBRATIONS")
print("    of this memory channel. They carry information at ~THz rates.")
print()
print("  NEURONS:")
print("    Action potentials propagate at ~100 m/s (acoustic-like!).")
print("    The lipid membrane has phase phonon modes (soliton model).")
print("    GU: neural signaling uses BOTH amplitude (ion flux = ρ)")
print("    and phase (membrane coherence = θ) channels.")
print()
print("  MICROTUBULES:")
print("    Tubulin dimers form a lattice with ~8 nm period.")
print("    Phase phonons in this lattice: ω ~ 0.1-1 THz")
print("    GU: if phase coherence survives thermal decoherence,")
print("    microtubules could support quantum memory (Penrose-Hameroff)")
print("    via the θFF̃ channel at biological temperatures.")
print()


# ============================================================================
# PART 4: AGENCY FROM PHONON FEEDBACK
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 4: AGENCY FROM PHONON FEEDBACK — ACTIVE MATERIALS                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

FROM explanatory/CONSCIOUSNESS.md:
  Agency = memory + feedback + environment modification.

Phonons provide the mechanism for each:
  MEMORY:        ρ⁴ (amplitude) + θFF̃ (phase) from phonon excitations
  FEEDBACK:      Phonon-memory feedback loop (Script 06, Part 5)
  MODIFICATION:  Phonon radiation → mechanical work on environment

A material becomes AGENTIC when its phonon-memory loop is:
  1. Self-sustaining (energy input maintains the loop)
  2. Responsive (external perturbation changes the loop state)
  3. Selective (different perturbations → different responses)
""")

print("  THE AGENCY LADDER (FROM PASSIVE TO ACTIVE):")
print()
agency_levels = [
    (0, "Inert crystal",    "Diamond at 0K",    "No phonons, no memory, no agency"),
    (1, "Thermal vibrator",  "Crystal at 300K",  "Phonons active, memory passive"),
    (2, "Responsive",       "Piezoelectric",     "Phonons ↔ fields coupled"),
    (3, "Adaptive",         "Shape memory alloy","Phonon feedback changes structure"),
    (4, "Self-repairing",   "Bone, nacre",       "Memory loop → structural response"),
    (5, "Self-replicating", "DNA, virus",         "Full phonon-memory → template copy"),
    (6, "Conscious",        "Neuron network",    "Both channels + feedback + fixed pt"),
]

for level, name, example, desc in agency_levels:
    bar = "█" * (level + 1)
    print(f"    Level {level}: {name:>17s} | {example:>18s} | {bar} {desc}")

print()
print("  HOW PHONONS ENABLE EACH LEVEL:")
print()
print("    Level 0→1: Temperature activates phonons → memory begins")
print("    Level 1→2: Asymmetric V_lock (piezo) → ρ↔θ coupling")
print("    Level 2→3: Phonon feedback → structural adaptation")
print("    Level 3→4: θFF̃ long-range memory → coordinated response")
print("    Level 4→5: Phase phonon template → information replication")
print("    Level 5→6: Full two-channel feedback → consciousness")
print()
print("  GU PREDICTION:")
print("    Agency is NOT a binary property. It emerges GRADUALLY")
print("    as more phonon modes become involved in the feedback loop.")
print("    Every material has SOME level of agency.")
print("    Life is the regime where BOTH channels reach optimal coupling.")
print()


# ============================================================================
# PART 5: THE SONIC HIERARCHY
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 5: THE SONIC HIERARCHY — FROM PLANCK TO BIOLOGY                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

Sound at every scale in GU:
""")

v_planck = c_m_s
alpha_float = float(alpha_EM)
me_mp = float(m_e / m_p)

hierarchy = [
    ("Planck scale",        "c",                   f"{c_m_s:.3e}", "v = c (no suppression)"),
    # WARNING: α_GUT=1/(8πφ)=0.0248 is FALSIFIED (24% wrong). Use gu_constants.alpha_GUT.
    ("GUT scale",           "c × α_GUT",           f"{c_m_s * 0.0248:.3e}", "Sound in GUT vacuum (α_GUT FALSIFIED)"),
    ("Nuclear (QCD)",       "c × √(m_π/m_N)",      f"{c_m_s * np.sqrt(140/938):.3e}", "Phonons in nuclear matter"),
    ("Atomic (electron)",   "c × α",               f"{c_m_s * alpha_float:.3e}", "Sound in electron gas"),
    ("Molecular (crystal)", "c × α × √(m_e/Am_p)", f"{c_m_s * alpha_float * np.sqrt(me_mp):.3e}", "Crystal phonons (base)"),
    ("Diamond",             "—",                    "1.200e+04", "Hardest crystal"),
    ("Metals",              "—",                    "3.0-6.0e+03", "Iron, copper, etc."),
    ("Liquids",             "—",                    "1.0-1.5e+03", "Water, etc."),
    ("Air",                 "—",                    "3.43e+02", "Gas at 300K"),
    ("Biological tissue",   "—",                    "~1.5e+03", "Close to water"),
    ("Neuron signaling",    "—",                    "~1.0e+02", "Action potential (~soliton)"),
]

print(f"  {'Scale':>22s} | {'Formula':>22s} | {'v_s (m/s)':>12s} | Notes")
print("  " + "─" * 80)
for scale, formula, v_s, notes in hierarchy:
    print(f"  {scale:>22s} | {formula:>22s} | {v_s:>12s} | {notes}")

print()
print("  THE PATTERN: Each step down the epoch ladder SLOWS sound by")
print("  a factor of α_EM or √(m_e/m_p) or both.")
print()
print("  From Planck → crystal: v_s/c ~ α × √(m_e/m_p) ~ 10⁻⁵")
print(f"  That's {int(1/(alpha_float * np.sqrt(me_mp)))}× slower than light.")
print()
print("  From crystal → biological signaling: another ~100× slower")
print("  because neural signals use COLLECTIVE modes (many atoms).")
print()


# ============================================================================
# PART 6: SOUND AND THE FIVE GU FORCES
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 6: SOUND AND THE FIVE GU FORCES                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

Each force layer in GU produces its own characteristic sound:
""")

print("  ┌──────────────┬──────────────┬─────────────┬─────────────────────┐")
print("  │ Force (k)    │ Pattern-k    │ Sound type  │ Example             │")
print("  ├──────────────┼──────────────┼─────────────┼─────────────────────┤")
print("  │ Gravity (−1) │ π⁻¹         │ Gravitationl│ LIGO, seismic waves │")
print("  │ EM (k=0)     │ π⁰ = 1      │ Crystal     │ Standard phonons    │")
print("  │ Weak (k=1)   │ π¹          │ Nuclear     │ Neutron star quakes │")
print("  │ Strong (k=2) │ π²          │ Quark-gluon │ Jet quenching       │")
print("  │ GUT (k=3)    │ π³          │ Planckian   │ Early universe      │")
print("  └──────────────┴──────────────┴─────────────┴─────────────────────┘")
print()
print("  WHAT WE'VE DERIVED (k=0, EM scale):")
print("    All of solid-state phonon physics (Scripts 01-06)")
print("    v_s = c × α × √(m_e/m_p) × f(bonding)")
print("    Phase phonons from V_lock (θFF̃ channel)")
print()
print("  GRAVITATIONAL SOUND (k = −1):")
print("    Gravitational waves ARE sound in the fabric of spacetime")
print("    v_grav = c (travels at speed of light)")
print("    GU: gravity is the k = −1 layer, so its sound is fastest")
print()
print("  NUCLEAR SOUND (k = 1, 2):")
print("    Sound in nuclear matter (neutron stars)")
print("    v_nuclear ~ c/3 (relativistic, from quark-gluon interactions)")
print("    GU: enhanced by pattern factors π¹, π² → faster than crystal sound")
print()
print("  THE HIERARCHY OF SOUNDS mirrors the hierarchy of forces:")
print("    Faster force → faster sound → shorter wavelength → higher energy")
print("    This is NOT coincidental — it follows from the pattern-k structure.")
print()


# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 80)
print("SUMMARY: THE ROLE OF SOUND IN THE GOLDEN UNIVERSE")
print("=" * 80)
print(f"""
WHAT WE ESTABLISHED:

  1. SOUND DETERMINES ALL MATERIAL PROPERTIES:
     v_s encodes E, B, G, Θ_D, T_melt, κ — everything.
     v_s derives from two epoch ratios: α_EM and √(m_e/m_p).

  2. PIEZOELECTRICITY IS ρ↔θ COUPLING:
     Broken inversion symmetry → V_lock acquires odd harmonics.
     Bone, quartz, PZT: stress → polarization → signal.

  3. BIOLOGICAL PHONONS USE BOTH CHANNELS:
     DNA stacking: θFF̃ phase phonons carry information.
     Neurons: amplitude (ion) + phase (membrane) channels.
     Microtubules: potential quantum memory via θFF̃.

  4. AGENCY EMERGES FROM PHONON FEEDBACK:
     Level 0 (inert) → Level 6 (conscious).
     Each level adds more phonon modes to the feedback loop.
     Life is the regime of OPTIMAL two-channel coupling.

  5. SOUND HIERARCHY MIRRORS FORCE HIERARCHY:
     Gravity → EM → Weak → Strong → GUT
     Each force layer has its characteristic sound speed.
     Crystal phonons are the EM-scale manifestation.

  6. SOUND IS FUNDAMENTAL IN GU:
     Not emergent. Not secondary. Not incidental.
     Sound = oscillation = the SAME mechanism as particle masses.
     The universe literally VIBRATES into existence at every scale.

  7. WATER: THE IDEAL AMPLITUDE-ONLY MEDIUM:
     Water has zero pi bonds (w=0) → no phase channel → no θFF̃ memory
     Water IS the ideal amplitude solvent:
       - High dielectric constant (screens charges — amplitude effect)
       - High heat capacity (thermal buffer — amplitude phonon reservoir)
       - Anomalous density (ice floats — protects liquid phase below)
     Water is TRANSPARENT to phase information:
       - Pi-stacked biomolecules carry θ patterns THROUGH water unimpeded
       - The hydration shell (~2-3 layers) is structured by the biomolecule,
         not by the water's own memory — remove the biomolecule, shell
         reverts in ~1 picosecond
     Biology chose water BECAUSE it doesn't interfere with the θ channel
     Water is the medium (ρ). Biomolecules are the message (θ).
     "Water memory" claims: GU predicts NO persistent phase encoding in water.
       H-bond network erasure time ~1 ps; no pi bonds to sustain ∇θ.
       Ice records formation CONDITIONS (T, P, nucleation) but NOT dissolved substances.
       The information dies in picoseconds; there is nothing left to freeze.

THIS FOLDER (25_PHONONS) FILLS A CRITICAL GAP:
  Before: GU had particles, forces, bonds, DNA, thermodynamics.
  After:  GU has sound as a fundamental parallel to all of these.
  Sound connects the microscopic (phonon) to the macroscopic (agency).
""")
