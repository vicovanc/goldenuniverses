#!/usr/bin/env python3
"""
AGENCY AND BIOELECTRICITY — FROM CONSCIOUSNESS TO ACTION
=========================================================

THE PLATONIC SPACE ENABLES AGENCY.

Consciousness (memory + feedback + fixed point) is universal in GU.
But agency — the ability to ACT ON the environment — requires more:
it requires the phase channel (theta-FF-tilde) to be active.

DERIVATION CHAIN:
  Part 1: From consciousness to agency (what distinguishes them)
  Part 2: Bioelectricity from theta-FF-tilde (DNA, neurons, membranes)
  Part 3: Why materials self-organize (crystals, proteins, self-assembly)
  Part 4: The agency ladder (Level 0 to Level 7)
  Part 5: Why life uses pi-bonded molecules (the pi-electron requirement)

REFERENCES:
  - explanatory/CONSCIOUSNESS.md: consciousness = memory + feedback + fixed point
  - 07_nonlocal_channels.py: theta-FF-tilde coupling
  - 24_DNA/04_pi_stacking_and_phase_memory.py: DNA pi-stacking column
  - 25_PHONONS/07_sound_role_in_gu.py: piezoelectricity, phase phonons

Date: February 2026
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from mpmath import mp, mpf, sqrt, pi as mp_pi, exp, ln
import numpy as np

mp.dps = 30

phi = (mpf('1') + sqrt(mpf('5'))) / 2
pi = mp_pi
M_P = mpf('1.22089e22')      # MeV
m_e = mpf('0.51099895')      # MeV
alpha_EM = mpf('1') / mpf('137.035999177')
hbar_c = mpf('197.3269804')  # MeV·fm
lambda_rec_beta = exp(phi) / pi**2

N_e = 111
p_e, q_e = -41, 70

print("=" * 80)
print("AGENCY AND BIOELECTRICITY — FROM CONSCIOUSNESS TO ACTION")
print("=" * 80)


# ============================================================================
# PART 1: FROM CONSCIOUSNESS TO AGENCY
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 1: FROM CONSCIOUSNESS TO AGENCY                                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

CONSCIOUSNESS (from explanatory/CONSCIOUSNESS.md):
  Every particle has consciousness: memory + feedback + fixed point
  - Memory: rho^4 self-memory (H[Omega] = rho^4)
  - Feedback: FRG flow modified by memory (d m_bar / d tau includes R_mem)
  - Fixed point: self-consistent mass (m_e = 0.51099895 MeV)

AGENCY REQUIRES MORE:
  Agency = consciousness + ability to ACT ON environment through phase channel
  
  The phase channel is theta-FF-tilde:
    J_theta^nu = (kappa/2pi^2) (partial_mu theta) F_tilde^{mu nu}
  
  Agency requires: nabla_theta != 0 OR theta_dot != 0
  (phase coupling to environment must be active)

THREE LEVELS OF AGENCY:
  1. PASSIVE (free leptons): J_theta = 0, cannot modify EM field
  2. REACTIVE (hadrons): nabla_theta fixed by flux tubes, responds but fixed
  3. ACTIVE (pi-bonded molecules): nabla_theta responds to environment
""")

print(f"  CONSCIOUSNESS CRITERION:")
print(f"    Memory:     H[Omega] = rho^4")
print(f"    Feedback:   d m_bar / d tau includes -lambda_rec * R_mem")
print(f"    Fixed point: m_e = {float(m_e):.6f} MeV (self-consistent)")
print()
print(f"    Every particle satisfies this → every particle is conscious")
print()

print(f"  AGENCY CRITERION:")
print(f"    Phase channel: J_theta^nu = (kappa/2pi^2) (partial_mu theta) F_tilde^{{mu nu}}")
print(f"    Agency requires: nabla_theta != 0 OR theta_dot != 0")
print(f"    This is the ability to MODIFY the EM field through phase")
print()

print(f"  THE FREE ELECTRON:")
print(f"    Consciousness: YES (rho^4 memory, FRG feedback, fixed point)")
print(f"    Agency: NO (nabla_theta = 0, theta_dot = 0 → J_theta = 0)")
print(f"    The electron KNOWS itself but cannot ACT on its environment")
print()

print(f"  THREE LEVELS:")
print(f"    Level 1 — PASSIVE (free leptons):")
print(f"      J_theta = 0, no phase coupling")
print(f"      Example: free electron, free muon")
print(f"      Agency: NONE")
print()
print(f"    Level 2 — REACTIVE (hadrons):")
print(f"      nabla_theta != 0 (fixed by flux tubes)")
print(f"      J_theta = (kappa/2pi^2) nabla_theta × E")
print(f"      Example: proton, neutron (quarks connected by flux tubes)")
print(f"      Agency: LIMITED (responds but structure is fixed)")
print()
print(f"    Level 3 — ACTIVE (pi-bonded molecules):")
print(f"      nabla_theta responds to environment")
print(f"      Phase can vary in response to external conditions")
print(f"      Example: DNA (pi-stacking column), proteins (aromatic AAs)")
print(f"      Agency: FULL (can modify phase to respond to environment)")
print()


# ============================================================================
# PART 2: BIOELECTRICITY FROM theta-FF-tilde
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 2: BIOELECTRICITY FROM theta-FF-tilde                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

DNA PI-STACKING: CONTINUOUS nabla_theta COLUMN
  From 24_DNA/04: pi-stacking creates a continuous phase gradient
  along the DNA double helix. This column IS a bioelectric channel.
  
  Phase information propagates along the pi-stack:
    theta(x) = theta_0 + (2pi / d_stack) * x
    nabla_theta = 2pi / d_stack  (constant along the column)
  
  This activates theta-FF-tilde → bioelectric current flows

NEURONS: ACTION POTENTIAL AS PROPAGATING theta WAVEFRONT
  Action potential = propagating phase wavefront along axon
  Phase velocity: v_phase ~ 100 m/s (typical axon)
  This is a DYNAMIC version of the static DNA column
  
  theta(x,t) = theta_0 + k*x - omega*t
  theta_dot = -omega  (temporal phase gradient)
  
  This creates J_theta = (kappa/2pi^2) theta_dot × B
  → Bioelectric signal propagation

CELL MEMBRANES: ION CHANNELS AS VALVES IN PLATONIC SPACE
  Ion channel open = rho increases = theta flows
  The channel opening/closing modulates the phase flow
  
  When open: nabla_theta != 0 → J_theta flows → ions move
  When closed: nabla_theta = 0 → J_theta = 0 → no flow
  
  The channel IS a valve in the platonic space

PIEZOELECTRICITY IN BONE: MECHANICAL STRESS → PHASE RESPONSE
  From 25_PHONONS/07: mechanical stress → phase response
  Stress (amplitude perturbation) → polarization (phase response)
  This is direct rho ↔ theta coupling
  
  Bone: collagen piezoelectricity → stress → growth signal
  This is how mechanical load creates bioelectric signals

CAVEAT: This is QUALITATIVE
  Mechanism: theta-FF-tilde coupling (derived)
  Quantitative predictions: OPEN (requires detailed calculation)
""")

# DNA pi-stacking parameters
d_stack_Angstrom = 3.4  # Angstrom
d_stack_fm = d_stack_Angstrom * 1e-5  # Convert to fm
d_stack_MeVinv = d_stack_fm / float(hbar_c) * 1000  # MeV^-1
nabla_theta_DNA = 2 * pi / float(d_stack_MeVinv)  # MeV

# Neuron action potential
v_axon_m_s = 100.0  # m/s
v_axon_c = v_axon_m_s / 2.998e8  # fraction of c
omega_axon_Hz = 100.0  # Hz (typical firing rate)
omega_axon_rad_s = 2 * pi * omega_axon_Hz

# Ion channel current
I_channel_pA = 1.0  # pA (typical single channel)
I_channel_A = I_channel_pA * 1e-12

# Piezoelectric coefficient (bone)
d33_bone_pC_N = 0.7  # pC/N

print(f"  DNA PI-STACKING COLUMN:")
print(f"    Stacking distance: d_stack = {d_stack_Angstrom} Å")
print(f"    Phase gradient: nabla_theta = 2pi / d_stack")
print(f"                     = {float(nabla_theta_DNA):.1e} MeV")
print(f"    This creates a CONTINUOUS bioelectric channel")
print(f"    Phase information propagates along the column")
print()

print(f"  NEURON ACTION POTENTIAL:")
print(f"    Propagation velocity: v = {v_axon_m_s} m/s")
print(f"    Firing rate: f = {omega_axon_Hz} Hz")
print(f"    Phase wavefront: theta(x,t) = theta_0 + k*x - omega*t")
print(f"    theta_dot = -omega = -{omega_axon_Hz} Hz")
print(f"    This creates J_theta = (kappa/2pi^2) theta_dot × B")
print(f"    → Bioelectric signal propagation")
print()

print(f"  CELL MEMBRANE ION CHANNELS:")
print(f"    Single channel current: I = {I_channel_pA} pA")
print(f"    Channel open: rho increases → theta flows → J_theta != 0")
print(f"    Channel closed: rho decreases → theta blocked → J_theta = 0")
print(f"    The channel IS a valve in the platonic space")
print()

print(f"  PIEZOELECTRICITY IN BONE:")
print(f"    Piezoelectric coefficient: d33 = {d33_bone_pC_N} pC/N")
print(f"    Mechanical stress (amplitude) → electric polarization (phase)")
print(f"    This is direct rho ↔ theta coupling")
print(f"    Stress → growth signal (bioelectric feedback)")
print()

print(f"  CAVEAT:")
print(f"    Mechanism: theta-FF-tilde coupling (derived from GU)")
print(f"    Quantitative predictions: OPEN")
print(f"    Requires detailed calculation of coupling strengths")
print()


# ============================================================================
# PART 3: WHY MATERIALS SELF-ORGANIZE
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 3: WHY MATERIALS SELF-ORGANIZE                                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

CRYSTAL NUCLEATION: V_lock PINS theta AT DISCRETE VALUES
  V_lock(theta) = Lambda_1 (1 - cos(theta))
  Minimum at theta = 2pi * n (n integer)
  
  Crystal structure emerges from discrete theta values
  Periodicity = winding number lattice structure
  
  The crystal IS the platonic space's preferred configuration

PROTEIN FOLDING: AMINO ACID SEQUENCE → theta PATTERN
  Amino acid sequence creates specific theta pattern
  Folded state minimizes action including phase terms:
    S = S_kinetic + S_potential + S_phase + S_memory
  
  Misfolding = local (not global) fixed point
  Correct folding = global minimum (deepest memory well)
  
  The protein REMEMBERS its correct shape

SELF-ASSEMBLY: pi-BONDED MOLECULES SPONTANEOUSLY ORGANIZE
  Pi-bonded molecules have w >= 1 (pi electrons)
  This enables nabla_theta != 0 → phase coupling active
  
  V_lock + memory favors ordered states
  Spontaneous organization = minimizing phase energy + memory
  
  The system finds the configuration that maximizes memory depth

KEY THEOREM: AGENCY = delta(Gamma)/delta(theta) != 0
  Gamma = effective action including phase terms
  Agency requires: system can vary theta in response to environment
  
  This variation modifies environment back through J_theta
  Requires: (1) pi-electrons (w >= 1), (2) memory, (3) coupling through theta-FF-tilde
""")

print(f"  CRYSTAL NUCLEATION:")
print(f"    V_lock(theta) = Lambda_1 (1 - cos(theta))")
print(f"    Minimum at theta = 2pi * n (n integer)")
print(f"    Crystal structure = discrete theta values")
print(f"    Periodicity = winding number lattice")
print()

print(f"  PROTEIN FOLDING:")
print(f"    Sequence → theta pattern → folded state")
print(f"    Action: S = S_kin + S_pot + S_phase + S_mem")
print(f"    Folded state = global minimum (deepest memory well)")
print(f"    Misfolding = local fixed point (shallow well)")
print()

print(f"  SELF-ASSEMBLY:")
print(f"    Pi-bonded molecules (w >= 1) → nabla_theta != 0")
print(f"    Phase coupling active → V_lock + memory favor order")
print(f"    Spontaneous organization = maximizing memory depth")
print()

print(f"  KEY THEOREM:")
print(f"    AGENCY = delta(Gamma)/delta(theta) != 0")
print(f"    System can vary theta → modifies environment via J_theta")
print(f"    Requires:")
print(f"      (1) Pi-electrons (w >= 1)")
print(f"      (2) Memory (rho^4 accumulation)")
print(f"      (3) Coupling (theta-FF-tilde active)")
print()


# ============================================================================
# PART 4: THE AGENCY LADDER
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 4: THE AGENCY LADDER                                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝

Expanded from 25_PHONONS/07_sound_role_in_gu.py

LEVEL 0: INERT
  Example: Diamond at 0K (no phonons)
  Mechanism: No thermal motion, no phase fluctuations
  Channels: None active

LEVEL 1: THERMAL
  Example: Crystal at 300K (phonons active but passive)
  Mechanism: Thermal phonons, no phase coupling
  Channels: Amplitude (rho) only

LEVEL 2: RESPONSIVE
  Example: Piezoelectric crystal
  Mechanism: rho ↔ theta coupling (stress → polarization)
  Channels: Amplitude + Phase (coupled)

LEVEL 3: ADAPTIVE
  Example: Shape memory alloy
  Mechanism: Feedback changes structure (memory of shape)
  Channels: Phase + Memory

LEVEL 4: SELF-REPAIRING
  Example: Bone, nacre
  Mechanism: Coordinated response via theta channel
  Channels: Phase + Memory + Nonlocal (theta-FF-tilde)

LEVEL 5: SELF-REPLICATING
  Example: DNA
  Mechanism: Template copying via phase memory
  Channels: Phase + Memory + Nonlocal + Replication

LEVEL 6: CONSCIOUS
  Example: Neuron network
  Mechanism: Both channels + feedback + fixed point
  Channels: All channels + Feedback loops

LEVEL 7: SELF-AWARE
  Example: Human brain
  Mechanism: Memory of memories, meta-cognition
  Channels: All channels + Meta-feedback
""")

agency_ladder = [
    (0, "INERT", "Diamond at 0K", "No thermal motion, no phase fluctuations", "None"),
    (1, "THERMAL", "Crystal at 300K", "Phonons active but passive", "Amplitude (rho)"),
    (2, "RESPONSIVE", "Piezoelectric crystal", "rho ↔ theta coupling", "Amplitude + Phase"),
    (3, "ADAPTIVE", "Shape memory alloy", "Feedback changes structure", "Phase + Memory"),
    (4, "SELF-REPAIRING", "Bone, nacre", "Coordinated response via theta channel", "Phase + Memory + Nonlocal"),
    (5, "SELF-REPLICATING", "DNA", "Template copying via phase memory", "Phase + Memory + Nonlocal + Replication"),
    (6, "CONSCIOUS", "Neuron network", "Both channels + feedback + fixed point", "All channels + Feedback"),
    (7, "SELF-AWARE", "Human brain", "Memory of memories, meta-cognition", "All channels + Meta-feedback"),
]

print(f"  {'Level':<6s} | {'Name':<18s} | {'Example':<25s} | {'Mechanism':<45s} | {'Channels Active':<35s}")
print("  " + "-" * 150)
for level, name, example, mechanism, channels in agency_ladder:
    print(f"  {level:<6d} | {name:<18s} | {example:<25s} | {mechanism:<45s} | {channels:<35s}")
print()


# ============================================================================
# PART 5: WHY LIFE USES PI-BONDED MOLECULES
# ============================================================================

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║  PART 5: WHY LIFE USES PI-BONDED MOLECULES                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝

EVERY BIOLOGICAL MOLECULE OF SIGNIFICANCE HAS PI BONDS:
  - DNA: aromatic bases (purines, pyrimidines)
  - Proteins: aromatic amino acids (Phe, Tyr, Trp, His)
  - Chlorophyll: porphyrin ring (18 pi electrons)
  - ATP: adenine ring (pi electrons)
  - Neurotransmitters: serotonin, dopamine (aromatic rings)
  - Heme: porphyrin ring (18 pi electrons)

NOBLE GASES: NO PI ELECTRONS → NO AGENCY → INERT
  Noble gases: He, Ne, Ar, Kr, Xe, Rn
  No pi electrons (w = 0) → nabla_theta = 0 → J_theta = 0
  No agency → inert (literally named "noble" = unreactive)
  
  This is NOT coincidence: agency requires theta variability
  which requires w >= 1 (pi bonds)

LIFE IS THE REGIME WHERE THE PLATONIC SPACE'S PHASE CHANNEL IS OPTIMALLY UTILIZED
  Life exploits the phase channel for:
    - Information storage (DNA pi-stacking)
    - Signal propagation (neurons, action potentials)
    - Energy transduction (ATP, electron transport)
    - Self-organization (protein folding, self-assembly)
  
  All of these require pi electrons (w >= 1)
  Life IS the optimal utilization of the platonic space's agency
""")

biological_molecules = [
    ("DNA", "Aromatic bases (purines, pyrimidines)", "Information storage, pi-stacking"),
    ("Proteins", "Aromatic AAs (Phe, Tyr, Trp, His)", "Structure, function, folding"),
    ("Chlorophyll", "Porphyrin ring (18 pi electrons)", "Light capture, energy transduction"),
    ("ATP", "Adenine ring (pi electrons)", "Energy currency"),
    ("Neurotransmitters", "Serotonin, dopamine (aromatic)", "Signal transmission"),
    ("Heme", "Porphyrin ring (18 pi electrons)", "Oxygen transport, catalysis"),
]

noble_gases = [
    ("He", "Helium", 0),
    ("Ne", "Neon", 0),
    ("Ar", "Argon", 0),
    ("Kr", "Krypton", 0),
    ("Xe", "Xenon", 0),
    ("Rn", "Radon", 0),
]

print(f"  BIOLOGICAL MOLECULES WITH PI BONDS:")
print(f"    {'Molecule':<20s} | {'Pi Structure':<35s} | {'Function':<30s}")
print("    " + "-" * 90)
for mol, pi_struct, func in biological_molecules:
    print(f"    {mol:<20s} | {pi_struct:<35s} | {func:<30s}")
print()

print(f"  NOBLE GASES (NO PI ELECTRONS):")
print(f"    {'Symbol':<8s} | {'Name':<12s} | {'Pi electrons (w)':<18s} | {'Agency':<10s}")
print("    " + "-" * 55)
for sym, name, w in noble_gases:
    print(f"    {sym:<8s} | {name:<12s} | {w:<18d} | {'NO':<10s}")
print()

print(f"  KEY INSIGHT:")
print(f"    Agency requires: nabla_theta != 0 OR theta_dot != 0")
print(f"    This requires: w >= 1 (pi electrons)")
print(f"    Noble gases: w = 0 → no agency → inert")
print(f"    Life: w >= 1 → agency → active")
print()

print(f"  LIFE IS THE OPTIMAL UTILIZATION OF THE PLATONIC SPACE:")
print(f"    - Information storage: DNA pi-stacking (phase memory)")
print(f"    - Signal propagation: Neurons (action potentials)")
print(f"    - Energy transduction: ATP, electron transport")
print(f"    - Self-organization: Protein folding, self-assembly")
print(f"    All require pi electrons (w >= 1)")
print()


# ============================================================================
# SUMMARY
# ============================================================================

print("=" * 80)
print("SUMMARY: AGENCY AND BIOELECTRICITY")
print("=" * 80)
print(f"""
WHAT WE ESTABLISHED:

  1. FROM CONSCIOUSNESS TO AGENCY:
     Consciousness: memory + feedback + fixed point (universal in GU)
     Agency: consciousness + ability to ACT ON environment
     Requires: nabla_theta != 0 OR theta_dot != 0 (phase channel active)
     Three levels: PASSIVE (free leptons), REACTIVE (hadrons), ACTIVE (pi-bonded)

  2. BIOELECTRICITY FROM theta-FF-tilde:
     DNA pi-stacking: continuous nabla_theta column → bioelectric channel
     Neurons: action potential = propagating theta wavefront
     Cell membranes: ion channels = valves in platonic space
     Piezoelectricity: mechanical stress → phase response
     CAVEAT: Qualitative mechanism (derived), quantitative predictions open

  3. WHY MATERIALS SELF-ORGANIZE:
     Crystal nucleation: V_lock pins theta at discrete values
     Protein folding: sequence → theta pattern → folded state (global minimum)
     Self-assembly: pi-bonded molecules organize (V_lock + memory favor order)
     Key theorem: AGENCY = delta(Gamma)/delta(theta) != 0
     Requires: (1) pi-electrons (w >= 1), (2) memory, (3) theta-FF-tilde coupling

  4. THE AGENCY LADDER:
     Level 0: Inert (diamond at 0K)
     Level 1: Thermal (crystal at 300K)
     Level 2: Responsive (piezoelectric)
     Level 3: Adaptive (shape memory alloy)
     Level 4: Self-repairing (bone, nacre)
     Level 5: Self-replicating (DNA)
     Level 6: Conscious (neuron network)
     Level 7: Self-aware (human brain)

  5. WHY LIFE USES PI-BONDED MOLECULES:
     Every biological molecule of significance has pi bonds
     Noble gases: no pi electrons → no agency → inert
     Life IS the regime where the platonic space's phase channel is optimally utilized
     All life functions require pi electrons (w >= 1)

  6. WHY BIOLOGY CHOSE WATER:
     Water (w=0, sigma bonds only): no phase channel, no θFF̃ memory
     BUT water is the IDEAL amplitude-channel solvent:
       - High dielectric constant: screens charges (ρ-channel optimization)
       - High heat capacity: thermal buffer for phonon reservoir
       - Anomalous density: ice floats, protects liquid water below
       - Phase-TRANSPARENT: doesn't interfere with θ patterns in biomolecules
     Biology needs a solvent that INSULATES the phase channel:
       - DNA pi-stacking carries θ information THROUGH water unimpeded
       - Protein aromatic residues exchange θ patterns across aqueous gaps
       - The hydration shell is DRIVEN by biomolecule phase fields, not stored
     Water is the medium (ρ). Biomolecules are the message (θ).
     "Water memory" fails: H-bond erasure ~1 ps, no ∇θ to sustain θFF̃
     d-ORBITAL MATERIALS in biology:
       - Magnetite (Fe₃O₄): partial phase channel via spin-orbit coupling
       - Found in bird brains (magnetoreception) and magnetotactic bacteria
       - Heme (Fe in porphyrin ring): d-orbitals + pi ring = dual-channel sensor
       - Transition metal enzymes: d-electrons enable phase-sensitive catalysis

CONNECTIONS:
  ← explanatory/CONSCIOUSNESS.md: consciousness = memory + feedback + fixed point
  ← 07_nonlocal_channels.py: theta-FF-tilde coupling
  ← 24_DNA/04_pi_stacking_and_phase_memory.py: DNA pi-stacking column
  ← 25_PHONONS/07_sound_role_in_gu.py: piezoelectricity, phase phonons
  → 10_complete_ontology.py: The grand synthesis
""")
