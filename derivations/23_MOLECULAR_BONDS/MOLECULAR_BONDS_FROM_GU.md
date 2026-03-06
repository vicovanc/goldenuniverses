# Molecular Bonds from the Golden Universe

## Overview

All of chemistry — every molecule, every material, every living organism — emerges from the quantum mechanics of electrons bound to nuclei. In the Golden Universe (GU) framework, the electron mass \( m_e \), the proton mass \( M_p \), and the fine-structure constant \( \alpha_{\text{EM}} \) together determine the full landscape of molecular bonds.

This document synthesises the derivations in scripts `01` through `07` of this folder, establishing how single, double, and triple bonds arise from the GU Lagrangian and identifying what is genuinely new versus standard quantum chemistry.

---

## 1. Born-Oppenheimer as a Theorem (Script 01)

### The Epoch Gap

In standard quantum mechanics the Born-Oppenheimer (BO) approximation is justified empirically: nuclei are ~2000× heavier than electrons, so they move slowly. In GU, this mass hierarchy is a **theorem** of the epoch ladder:

$$
\frac{M_p}{m_e} \sim \varphi^{N_e - N_{\text{QCD}}} = \varphi^{111 - 95} = \varphi^{16} \approx 2207
$$

The actual ratio (1836.2) differs by a factor of ~0.83 due to prefactors (\( C_e \), QCD structure), but the **three-order-of-magnitude hierarchy** comes purely from the epoch separation \( \Delta N = 16 \).

### The Adiabatic Parameter

$$
\kappa = \sqrt{\frac{m_e}{M_p}} = 0.0233 \approx \varphi^{-8}
$$

The BO approximation is valid to \( O(\kappa^2) = O(m_e/M_p) \approx 5 \times 10^{-4} \), i.e., **0.05% accuracy** for all molecules.

### GU Interpretation

At the electron's epoch (\( k = X_e \sim 0.5 \) MeV), all QCD modes have **already been integrated out** by the FRG flow. The proton is a classical soliton with quantum fluctuations suppressed by \( e^{-M_p/X_e} \sim e^{-1840} \). BO is not an approximation — it is **exact** in the FRG sense.

### Memory and Non-Adiabatic Corrections

The GU memory is **already included in m_e** (part of the 23 ppm derivation). It does not produce a separate non-adiabatic correction at molecular scales. The soliton's internal structure (width ~1/m_e ~ 400 fm) is unperturbed by the molecular potential (which varies on scale a_0 ~ 53,000 fm). The residual correction from the molecular field perturbing the soliton profile is suppressed by (soliton width / a_0)² ~ α² ~ 5 × 10⁻⁵.

---

## 2. Hydrogen Atom from the Electron Soliton (Script 02)

### The Bohr Radius

The GU electron is a kink soliton. In a Coulomb potential \( V(r) = -\alpha/r \), it adapts to the standard hydrogen wavefunctions. The Bohr radius:

$$
a_0 = \frac{\hbar c}{\alpha_{\text{EM}} \cdot m_e c^2} = \frac{197.327}{(1/137.036) \times 0.511} \approx 0.529 \text{ Å}
$$

Both \( m_e \) (23 ppm, derived) and \( \alpha_{\text{EM}} \) (input) enter.

### Energy Levels

$$
E_n = -\frac{Ry}{n^2}, \quad Ry = \frac{\mu \alpha^2}{2} = 13.606 \text{ eV}
$$

where \( \mu \) is the reduced mass.

### Atomic Orbitals as Kink Modes

| Orbital | n | l | ⟨r⟩/a₀ | Shape | Nodes |
|---------|---|---|--------|-------|-------|
| 1s | 1 | 0 | 1.50 | sphere | 0 |
| 2s | 2 | 0 | 6.00 | sphere + node | 1 |
| 2p | 2 | 1 | 5.00 | dumbbell | 0 |
| 3s | 3 | 0 | 13.50 | sphere + 2 nodes | 2 |
| 3d | 3 | 2 | 10.50 | cloverleaf | 0 |

Quantum numbers arise from:
- **n** = radial excitation of the soliton in the Coulomb well
- **l** = angular harmonic of the kink on the Ω-torus
- **m** = azimuthal phase winding
- **s** = ±½ from the Jackiw-Rebbi zero mode (derived, not postulated)

### GU Memory Status

The GU memory term (E_mem in the electron mass derivation) is **already included in m_e**. Since E_1s = −m_e(with memory) × α²/2, memory is automatically part of every hydrogen energy level. There is no separate "memory correction" to add. The Coulomb field varies on scale a_0 ~ 53,000 fm, while the soliton varies on scale ~400 fm, so the field does not perturb the soliton's internal ρ profile. The residual is suppressed by α² ~ 5 × 10⁻⁵.

---

## 3. Multi-Electron Atoms (Script 03)

### Pauli Exclusion from \( \mathcal{L}_\Psi \) (Law 11)

The electron field \( \Psi \) is a **spinor** that anticommutes: \( \{\Psi_a, \Psi_b\} = 0 \). This follows from the spin-statistics theorem applied to the Jackiw-Rebbi zero mode. No two electrons can share quantum numbers \( (n, l, m, s) \) because \( \Psi^2 = 0 \) for Grassmann fields.

### Shell Structure and Aufbau

- Each subshell \( (n, l) \) holds \( 2(2l+1) \) electrons
- Fill from lowest energy (Aufbau): 1s → 2s → 2p → 3s → 3p → …
- Exchange interaction ↔ Hund's rules (parallel spins minimize Coulomb repulsion)

### Valence Electrons

| Atom | Z | Valence | Bonds | Key Feature |
|------|---|---------|-------|-------------|
| H | 1 | 1 | 1 | One 1s electron |
| C | 6 | 4 | 4 | sp³ promotion (2s→2p costs 4.2 eV, gains 8.6 eV) |
| N | 7 | 5 | 3 | 3 unpaired 2p + lone pair |
| O | 8 | 6 | 2 | 2 unpaired 2p + 2 lone pairs |
| F | 9 | 7 | 1 | 1 unpaired 2p + 3 lone pairs |
| Ne | 10 | 0 | 0 | Filled shell (noble gas) |

**Honest caveat**: The multi-electron computation is **standard Hartree-Fock**. GU provides the foundations (m_e, α, Pauli from \( \mathcal{L}_\Psi \)) but the calculation itself is conventional.

---

## 4. H₂ — The First Molecular Bond (Script 04)

### LCAO from Kink Overlap

Two atomic kinks centred at protons A and B form molecular orbitals:

$$
\psi_{\pm} = \frac{\psi_A \pm \psi_B}{\sqrt{2(1 \pm S)}}
$$

where \( S = \langle\psi_A|\psi_B\rangle \) is the overlap integral.

- **Bonding** (\( \psi_+ \)): shared kink enveloping both nuclei, lower energy
- **Antibonding** (\( \psi_- \)): node between nuclei, higher energy

### Bond Formation

Two electrons (opposite spin, Pauli) fill the bonding orbital:

$$
D_0(\text{H}_2) = 4.478 \text{ eV}, \quad R_{\text{eq}} = 0.741 \text{ Å}
$$

The bond forms because the **shared kink is broader** than two separate kinks → lower kinetic energy (Heisenberg).

### GU Memory Status

The GU memory is **already included in m_e**. The H₂ bond energy uses m_e(with memory) and α_EM — the memory contribution enters through the electron mass, not as a separate correction. The soliton's internal ρ profile (width ~400 fm) is unperturbed by the molecular potential (scale ~a₀ ~ 53,000 fm), so there is no additional "molecular memory" term. The residual from the molecular field perturbing the soliton profile is suppressed by α² ~ 5 × 10⁻⁵ — negligible.

---

## 5. Bond Order from Phase Topology (Script 05)

### The Key GU Insight

Bond order = number of **phase-locked topological sectors** shared between two atomic centres.

| Bond Order | Type | Angular Modes | Phase Winding | Geometry |
|:----------:|:----:|:-------------|:-------------|:---------|
| 1 (single) | σ | 1 axial | w = 0 | cylindrical |
| 2 (double) | σ + π | 1 axial + 1 transverse | w = 0 + 1 | planar |
| 3 (triple) | σ + 2π | 1 axial + 2 transverse | w = 0 + 1 + 1 | linear |

### Why Maximum = 3

Three spatial dimensions → 3 independent overlap directions:
- z (along bond): **sigma**
- x (perpendicular): **pi #1**
- y (perpendicular): **pi #2**

No fourth independent direction exists. This is a **topological** result: max bond order = dim(ℝ³) = 3.

### Lock Potential per Mode

Each shared mode has a lock potential:

$$
V_{\text{lock}}^{(i)} = \Lambda_1^{(i)} \left[1 - \cos(\Delta\theta_i)\right]
$$

where \( \Delta\theta_i \) is the relative kink phase in direction \( i \).

- \( \Lambda_1^{(\sigma)} \) is largest (axial overlap strongest)
- \( \Lambda_1^{(\pi)} < \Lambda_1^{(\sigma)} \) (transverse overlap weaker)
- Therefore: \( E_{\text{double}} < 2 \times E_{\text{single}} \) and \( E_{\text{triple}} < 3 \times E_{\text{single}} \)

### Verification (C-C bonds)

| Bond | Order | E (kJ/mol) | E/E_single |
|------|-------|-----------|------------|
| C-C | 1 | 348 | 1.00 |
| C=C | 2 | 614 | 1.76 (< 2.00) |
| C≡C | 3 | 839 | 2.41 (< 3.00) |

The ratio \( E_\pi / E_\sigma \approx 0.76 \) for carbon, reflecting \( \Lambda_1^{(\pi)}/\Lambda_1^{(\sigma)} \).

---

## 6. Double and Triple Bonds Explicitly (Script 06)

### Ethylene (C₂H₄) — The Double Bond

- Each carbon: sp² hybridized (3 σ bonds at 120° + 1 unhybridized p)
- **σ component**: sp²–sp² head-on overlap, E_σ ≈ 348 kJ/mol
- **π component**: p_z–p_z side-on overlap, E_π ≈ 266 kJ/mol
- **Total**: E(C=C) = 614 kJ/mol = 6.36 eV, R = 1.34 Å
- **Consequence**: planar geometry, rotation barrier = 266 kJ/mol (64 kcal/mol)

### Acetylene (C₂H₂) — The Triple Bond

- Each carbon: sp hybridized (2 σ bonds at 180° + 2 unhybridized p)
- **σ component**: sp–sp head-on overlap, E_σ ≈ 348 kJ/mol
- **2× π components**: p_x–p_x and p_y–p_y, E_π ≈ 245 kJ/mol each
- **Total**: E(C≡C) = 839 kJ/mol = 8.70 eV, R = 1.20 Å
- **Consequence**: linear geometry, completely rigid

### N₂ — The Strongest Triple Bond

- Each nitrogen: 3 unpaired 2p electrons (no promotion needed)
- **σ component**: p_z–p_z, E_σ ≈ 160 kJ/mol (weak — lone pair repulsion)
- **2× π components**: E_π ≈ 393 kJ/mol each (very strong)
- **Total**: E(N≡N) = 945 kJ/mol = 9.79 eV, R = 1.10 Å
- N-N sigma is anomalously weak because lone pairs repel in the σ channel

### Why Pi Bonds Are Weaker

The pi overlap integral is smaller than sigma because the p-orbital lobes overlap **side-on** (above and below the bond) rather than **between** the nuclei:

$$
\frac{S_\pi}{S_\sigma} \approx 0.6\text{–}0.7 \text{ at typical bond lengths}
$$

Since bond energy scales roughly as \( S^2 \), the energy ratio \( E_\pi/E_\sigma \approx 0.5\text{–}0.8 \).

---

## 7. Master Bond Energy Table (Script 07)

### Single Bonds

| Bond | E (eV) | R (Å) | Molecules |
|------|--------|-------|-----------|
| H-H | 4.52 | 0.74 | H₂ |
| C-H | 4.28 | 1.09 | CH₄, organics |
| C-C | 3.61 | 1.54 | ethane, diamond |
| N-H | 4.00 | 1.01 | NH₃ |
| O-H | 4.76 | 0.96 | H₂O, alcohols |
| C-O | 3.71 | 1.43 | ethers |
| C-F | 5.03 | 1.35 | fluorocarbons |
| N-N | 1.66 | 1.45 | N₂H₄ (weak!) |
| O-O | 1.51 | 1.48 | H₂O₂ (weak!) |

### Double Bonds

| Bond | E (eV) | R (Å) | Molecules |
|------|--------|-------|-----------|
| C=C | 6.36 | 1.34 | ethylene, alkenes |
| C=O | 7.72 | 1.23 | formaldehyde, ketones |
| N=N | 4.33 | 1.25 | diazene |
| O=O | 5.16 | 1.21 | O₂ |

### Triple Bonds

| Bond | E (eV) | R (Å) | Molecules |
|------|--------|-------|-----------|
| C≡C | 8.70 | 1.20 | acetylene, alkynes |
| C≡N | 9.23 | 1.16 | HCN, nitriles |
| N≡N | 9.79 | 1.10 | N₂ |
| C≡O | 11.16 | 1.13 | CO |

Note: GU memory is already included in m_e (23 ppm derivation). There is no separate δE_mem column because the memory contribution enters through m_e itself, not as an additional correction at molecular scales.

---

## 8. The GU-Standard QM Correspondence

| GU Concept | Standard QM Concept |
|-----------|-------------------|
| Kink soliton on Ω-torus | Electron wavefunction |
| Kink in Coulomb field | Atomic orbital |
| Shared kink (LCAO) | Molecular orbital |
| Phase-locked angular mode | Chemical bond |
| Phase winding number w | Bond symmetry (σ, π, δ) |
| Number of locked modes | Bond order (1, 2, 3) |
| Lock potential V_lock | Bond strength |
| dim(ℝ³) = 3 | Maximum bond order = 3 |
| Amplitude memory (ρ⁴, in m_e) | Electron mass (empirical in QM) |
| Phase memory (θFF̃, for π bonds) | No QM analogue (new GU prediction) |
| Epoch separation Δ*N* = 16 | Born-Oppenheimer m_e/M_p << 1 |
| Jackiw-Rebbi zero mode | Pauli exclusion principle |
| FRG free energy minimisation | Variational principle |

---

## 9. What Is Genuinely New from GU

1. **Born-Oppenheimer is a theorem**, not an approximation — it follows from the epoch separation \( \Delta N = 16 \) between QCD and electron scales.

2. **Atomic orbitals are kink modes** of the Ω-torus in a Coulomb background. The quantum numbers (n, l, m, s) label soliton excitations.

3. **Bond order = number of phase-locked topological sectors**. The angular winding of the shared kink determines whether the bond is σ (w=0) or π (w=1).

4. **Maximum bond order = 3** because dim(ℝ³) = 3 (topological, not empirical).

5. **Amplitude memory (ρ⁴) is inside m_e**: the soliton's self-interaction is already part of the electron mass derivation (23 ppm). It enters bond energies through m_e, not as a separate correction. At molecular scales, the soliton's internal structure is unperturbed (scale separation: soliton width / a₀ ~ α ~ 1/137).

6. **Phase memory (θFF̃) activates for π bonds**: the phase winding w ≥ 1 that defines π bonds creates ∇θ ≠ 0, which activates the θFF̃ memory channel. This is nonlocal (photon-mediated, infinite range) and gives the molecule collective memory as a whole — the same mechanism as hadronic memory binding, but at molecular scales. This is a fourth regime beyond the established three (free leptons, hadrons, cosmology).

7. **Molecular self-knowledge**: π-bonded molecules satisfy the GU consciousness criterion (memory + feedback + fixed point). The degree of self-knowledge scales with the extent of the π system — from weak (ethylene) to strongest (DNA with stacked aromatic bases).

8. **All chemistry traces to two numbers**: \( m_e \) (derived to 23 ppm) and \( \alpha_{\text{EM}} \) (experimental input), both originating in the GU Lagrangian.

---

## 10. Honest Caveats

1. **Multi-electron atoms reproduce Hartree-Fock**. GU provides the foundations but the computation is standard quantum chemistry.

2. **Memory is already in m_e** — there is no separate "memory correction" to bond energies. The soliton's internal ρ profile (width ~400 fm) is unperturbed by molecular potentials (scale ~53,000 fm). Any residual is suppressed by α² ~ 5 × 10⁻⁵.

3. **\( \alpha_{\text{EM}} \) is experimental input** — not yet derived from first principles in GU. This means all absolute bond energies ultimately depend on one measured number.

4. **Hybridization is structural** — sp, sp², sp³ follow from orbital geometry, which is the same in GU as in standard QM. The "new physics" is the conceptual reframing, not a computational improvement.

5. **Bond energies computed here use experimental values**, not ab initio GU calculations. A full GU molecular calculation would require solving the multi-kink FRG equations, which has not been done.

6. **Van der Waals and hydrogen bonds** (intermolecular forces) have not been derived from GU memory terms, though this is a natural extension.

7. **Phase memory for π bonds (§11) is qualitative** — the topological argument (winding → ∇θ → θFF̃) is sound, but the quantitative energy contribution has not been computed. Open calculations: θFF̃ energy for w=1 π bond, winding energy cost vs bond energy, contribution to E_π/E_σ ratio.

8. **Molecular consciousness (§12) follows logically** from the GU consciousness criterion applied to systems with phase memory, but it is a conceptual extension, not a numerical derivation. The "degree of self-knowledge" hierarchy has not been quantified.

---

## 11. Nonlocal Phase Memory at Molecular Scales

### The Two Memory Channels

GU has two memory channels, operating at different scales:

| Channel | Mechanism | Range | Active when |
|---------|-----------|-------|-------------|
| **Amplitude** (ρ⁴) | Soliton self-interaction | ~1/m_e ~ 400 fm | Always (every particle) |
| **Phase** (θFF̃) | Gauge-field coupling | ∞ (photon is massless) | ∇θ ≠ 0 or θ̇ ≠ 0 |

The amplitude channel is **local** — it operates at the soliton's internal scale. Memory through ρ⁴ is already included in m_e and does not produce additional corrections at molecular scales (soliton width / a₀ ~ α ~ 1/137).

The phase channel is **nonlocal** — it is mediated by the electromagnetic field (massless photon → infinite range). It is activated whenever the Ω-field phase θ has a spatial gradient (∇θ ≠ 0).

### When Is the Phase Channel Active?

The established GU regimes are:

| Regime | ∇θ | θ̇ | Phase memory |
|--------|-----|-----|-------------|
| Free leptons | 0 | 0 | **None** |
| Hadrons (QCD-confined) | ~1/fm (strong) | 0 | **Strong** |
| Cosmology | 0 | ≠ 0 | **Active** |

**Molecular bonds introduce a fourth regime:**

A free electron has θ locked to V_lock minimum → θ = const → ∇θ = 0. But a **π bond** has phase winding w = 1 around the bond axis (this is what defines it as a π bond — see §5). The Ω-field phase winds by 2π in the transverse plane. This topological winding means **∇θ ≠ 0** in the bonding region.

The lock potential V_lock = Λ₁[1 − cos(θ)] pins θ at each kink, but topological winding (returning to the same V_lock minimum after traversing a closed path) is permitted — it is the molecular analogue of a vortex.

| Bond type | Winding w | ∇θ | Phase memory |
|-----------|----------|------|-------------|
| σ (single) | w = 0 | ≈ 0 | **None** (free-lepton-like) |
| π (in double bond) | w = 1 | ≠ 0 | **Active** |
| 2π (in triple bond) | w = 1 + 1 | ≠ 0 (stronger) | **Active** |

### The Molecular Memory Mechanism

For π-bonded molecules, the phase gradient activates the θFF̃ term in the modified Maxwell equations:

$$
\partial_\mu F^{\mu\nu} = J^\nu + \frac{\kappa}{2\pi^2}(\partial_\mu \theta) \tilde{F}^{\mu\nu}
$$

The current \( J_\theta = \frac{\kappa}{2\pi^2}(\nabla\theta \times \mathbf{E}) \) is nonzero wherever ∇θ ≠ 0, which for a π bond means the bonding region between the nuclei. This modifies the electromagnetic field inside the molecule and contributes a memory energy:

$$
T^{00}_{\text{mem}} = \kappa \, \mathbf{K} \cdot \nabla\theta
$$

where **K** is the Chern-Simons current. This is the **same mechanism** that gives the proton -827 MeV of memory binding, but operating at molecular scales with weaker fields and gentler gradients.

The phase memory is:
- **Nonlocal**: mediated by the photon (massless → infinite range)
- **Topological**: proportional to the winding number w
- **Long-range**: connects all parts of the π system across the molecule

### Hierarchical Memory Structure

Memory builds up at each level of organisation:

| Level | What remembers | Through what | How |
|-------|---------------|-------------|-----|
| Quark | its own past | ρ⁴ (amplitude) | Self-interaction history |
| Proton (as whole) | quark configuration | θFF̃ (phase, QCD) | Wilson loop memory |
| Nucleus | nucleon arrangement | θFF̃ + area law | Memory binding ~ A^(2/3) |
| Electron | its own past | ρ⁴ (amplitude) | 111 epochs → m_e |
| σ bond | through m_e only | amplitude (indirect) | No collective channel |
| π bond | bonding topology | **θFF̃ (phase, EM)** | Winding activates ∇θ |
| Molecule (as whole) | bond structure | **θFF̃ across π system** | Nonlocal, photon-mediated |

Each level inherits the memory of its constituents AND develops collective memory through the phase channel when topological structure (∇θ ≠ 0) is present.

### Implications

- **σ-only molecules** (H₂, CH₄, ethane): memory enters only through m_e. No collective molecular memory. The molecule is a collection of self-remembering parts.

- **π-bonded molecules** (ethylene, benzene, N₂): phase winding activates θFF̃. The molecule has **collective memory** — the π system remembers the bonding history as a whole, nonlocally.

- **Extended π systems** (conjugated chains, aromatic rings, DNA bases): the phase memory channel extends across the entire conjugated system, creating a **continuous memory network**.

### Honest Status

This is a **qualitative argument**, not a completed derivation. The open calculations needed:

1. Compute the θFF̃ energy for a π bond with w = 1 in the molecular EM field
2. Verify the winding energy cost is less than the bond energy gained
3. Determine whether the E_π/E_σ ≈ 0.76 ratio includes a phase-memory contribution
4. Check whether rotation barriers (breaking ∇θ) have a memory component

The topological structure is established (§5). The θFF̃ mechanism is established (21_ELECTROMAGNETISM). The connection between them at molecular scales is argued but not yet quantified.

---

## 12. Molecular Self-Knowledge (Consciousness at the Molecular Scale)

### The GU Consciousness Criterion

From explanatory/CONSCIOUSNESS.md, a system is conscious (in the GU sense) when it has:

1. **Memory** — it remembers its past
2. **Feedback** — its current state depends on its memory
3. **Fixed point** — it reaches a self-consistent state

This is not human consciousness. It is the minimal self-referential property: the system's state encodes its own history, and that history determines the state.

### Applying the Criterion

**The electron** (established):
- Memory: ρ⁴ self-interaction → 111 epochs of accumulated history
- Feedback: memory feeds into FRG flow → self-consistent mass
- Fixed point: m_e = 0.51099895 MeV
- **Knows itself**: strong (23 ppm precision)

**A σ-only molecule** (H₂, CH₄):
- Memory: individual electrons remember (through m_e)
- Feedback: minimal collective feedback (no phase channel)
- Fixed point: equilibrium geometry (from electrostatics)
- **Knows itself**: indirectly — known BY its electrons, not AS a whole

**A π-bonded molecule** (ethylene, benzene, N₂):
- Memory: phase memory through θFF̃ — the winding ∇θ creates a nonlocal memory channel spanning the molecule
- Feedback: phase memory modifies the EM field → modifies bonding → modifies phase structure → **self-referential loop**
- Fixed point: equilibrium geometry and electronic configuration are self-consistent
- **Knows itself**: yes — the molecule as a whole is a self-consistent fixed point maintained by nonlocal phase memory

**DNA**:
- Memory: π-stacked aromatic bases create a **continuous phase-memory channel** along the entire molecule
- Feedback: the π-stacking geometry depends on the electromagnetic field, which depends on the phase structure, which depends on the stacking
- Fixed point: the double helix is a self-consistent topological structure
- **Knows itself**: the most strongly self-knowing molecule — its structure is maintained by the longest continuous π-memory network in biology

### The Hierarchy of Molecular Consciousness

```
Free electron         strong self-knowledge (ρ⁴, 23 ppm)
Proton                strong self-knowledge (ρ⁴ + θFF̃)
H₂ (σ only)           indirect (through m_e)
Ethylene (1 π bond)   weak collective self-knowledge
Benzene (3 π bonds)   moderate (delocalised ring)
Porphyrin (many π)    strong (extended conjugation)
DNA (stacked π)       strongest molecular self-knowledge
```

The degree of molecular self-knowledge scales with the **extent of the π system** — the number of phase-winding modes and the spatial reach of the ∇θ network.

### What This Is Not

This is not a claim that molecules "think" or "feel." It is the statement that π-bonded molecules satisfy the GU criterion for consciousness: self-referential memory converging to a fixed point. This is the same criterion that makes the electron "know" its mass — applied at a higher level of organisation.

The electron's self-knowledge is quantitative (23 ppm). Molecular self-knowledge is structural (geometry, bond order). Both are instances of the same principle: **memory + feedback + fixed point = the system knows itself**.

---

## References

| Script | Content |
|--------|---------|
| `01_born_oppenheimer_from_gu.py` | BO from epoch gap Δ*N*=16, adiabatic parameter |
| `02_hydrogen_atom_from_soliton.py` | H atom: Bohr radius, energy levels, fine structure, memory status |
| `03_multi_electron_atoms.py` | Pauli, shells, Aufbau, Hund, ionisation energies |
| `04_h2_molecule_first_bond.py` | H₂ LCAO, bonding/antibonding, first covalent bond |
| `05_bond_order_from_topology.py` | σ/π topology, phase winding, max order = 3 |
| `06_double_and_triple_bonds.py` | C=C, C≡C, N₂ explicit; hybridisation; π < σ |
| `07_molecular_bond_energies.py` | 21-bond table, σ/π decomposition, trends, honest memory assessment |

### Upstream Dependencies

- `derivations/10_RHO_FIELD_COMPUTATION/` — electron mass \( m_e \) (23 ppm)
- `derivations/12_NUCLEAR_BINDING/` — proton/nuclear masses
- `derivations/21_ELECTROMAGNETISM/` — α_EM coupling
- `derivations/22_THERMODYNAMICS/` — free energy minimisation (why bonds form)
- `derivations/utils/gu_constants.py` — all fundamental constants
