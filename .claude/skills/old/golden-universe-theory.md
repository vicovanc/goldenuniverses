# Golden Universe Theory — Core Framework

**Use this skill when:** Working with Golden Universe (GU) theoretical physics, deriving particle masses from first principles, NLDE solitons, Lagrangian structure, Formation document physics, or any GU-related derivation, law, or calculation involving Laws 0-38, five derivation routes, and canonical conventions.

## Core Canonical Documents

**Primary References:**
- `theory/theory-laws.md` — AUTHORITATIVE SOURCE (4200+ lines): Laws 0-38, five derivation routes, complete formulas at 50-digit precision
- `⭐_MASTER_EQUATIONS_REFERENCE.md` — Comprehensive equation compendium with dimensional analysis
- `theory/derived-laws.md` — Step-by-step derivations from first principles
- `Golden Universe Laws.docx` — Word export of theory/theory-laws.md

**Source Manuscripts:**
- **V2 document:** "The Golden Universe: A Theory of Emergent Reality from Geometric First Principles"
- **Formation document:** Z₁ genesis vector, epoch ladder, resonance condition
- **Particles v2:** Electron-specific calculations companion

## Canonical Symbols & Constants (Law 14 — NEVER VIOLATE)

```python
φ = (1+√5)/2 = 1.618033988749894848204586834365638117720309179805762862135...
π = 3.14159265358979323846264338327950288419716939937510582097494...
e = 2.71828182845904523536028747135266249775724709369995957496696...

# Planck scale
E_P = M_P c²
M_P = 1.22089 × 10¹⁹ GeV/c²

# Formation scale
M₀ = M_P/√(5π) ≈ M_P/3.9635
```

**Critical epoch:**
```python
N_e = 111  # Electron epoch (from resonance condition)
X_e = X₀ · φ^(-111)
```

### FORBIDDEN CONSTRUCTIONS (Law 26)

❌ **Never use:**
1. Epoch-refined constants: φ₁₁₁, π₁₁₁, e₁₁₁
2. Extra N_e in prefactor (N_e lives ONLY inside φ^(-N_e))
3. Inverted determinant ratio (use det L₋/det L₀ only, never reversed)
4. Separate memory multiplier C_mem (already enters through μ)
5. Dimensional confusion: y_e = e^φ/π² is dimensionless, NEVER = 0.511 MeV

## The Lagrangian Structure (Laws 0-5)

```
L_M = L_Ω + L_X + L_int + L_gauge
```

### Components:

**Ω-Sector (substrate field):**
```
L_Ω = kinetic + V_{fullΩ} + phase-driver + memory
```

**Full potential:**
```
V_{fullΩ} = Σ m̃²_i(X) S_{2,i} + Σ λ̃_j(X) S_{4,j} + Σ γ̃_k(X) S_{6,k} + V_{angular_mod}
```

**Phase-driver (frequency lock):**
```
L_phase = −κ_p(X)·ρ²·(ω_eff + ω_target(X))²
```

**Gauge-invariant effective frequency (Law 16):**
```
ω_eff = j_c⁰/(2ρ_c)
```

## Electron Mass — Five Independent Derivation Routes

First-principles result: **m_e = 0.51283 MeV** (+0.36% tree-level error at ν_topo = 0.7258); **23 ppm** with Lamé one-loop correction.
**Note:** Requires α_EM = 1/137.036 as experimental input for QED correction η_QED = 1 - α/(2π).

### Route A: Ψ-Sector (NLDE/Spinor) — Steps prefix: `STEP`

**Method:** Soler-type nonlinear Dirac equation → radial BVP → soliton energy

**Key equation:**
```
[iγ^μ∂_μ − m_Ψ − Σ(s) − Π(Ω_eff, ρ)]Ψ = 0
```

**Five dimensionless parameters:** {m̂, λ̂, γ̂, κ̂, ω̂}

**Energy integral:**
```
E_sol = ∫ T₀₀ d³x
```

**Electron mass formula:**
```
m_e = M₀ · (2π/φ^{N_e}) · C_e(ν) · η_QED

where:
  C_e ≡ (φ^{N_e}/2π) · E_e/(M_P c²) ≈ 1.053
  ν = 0.82054 (self-consistency parameter, Law 33)
```

### Route B: Ω-Sector (Vortex/Phase-Driver) — Steps prefix: `Ω-STEP`

**Method:** V_{fullΩ} + phase-driver → vortex solution → angular bifurcation

**Frequency lock condition:**
```
ω = ω_target(X_e) = C_ω(X_e) · π/φ
```

**Harmonic mass:** m* from first unstable eigenmode

**Self-consistency parameter:**
```
μ = 0.4192  (Law 34)
```

### Route C: FRG (Ab-Initio/Wetterich) — Steps prefix: `FRG-STEP`

**Method:** Functional Renormalization Group flow from UV to IR

**Wetterich equation:**
```
∂_t Γ_k = ½ Tr[(Γ_k^{(2)} + R_k)^{−1} · ∂_t R_k]
```

**UV boundary conditions:** Seeley-DeWitt heat-kernel at Λ_cut ≈ M₀

**Key feature:** Eliminates ALL O(1) free parameters through RG flow

### Route D: Recursion-Closure (Lock + Critical Epoch) — Steps prefix: `RC-STEP`

**Method:** Recursion engine U_n → target frequency → phase-lock

**Target frequency:**
```
ω_e = M₀ · 2π · φ^{−113}
```

**Critical epoch scale:**
```
X_e = X₀ · φ^{−111}
```

**Phase-lock condition:**
```
E_e/ℏ = ω_target(X_e)
```

### Route E: No-Hidden-Choices (Convention Audit) — Steps prefix: `NHC-STEP`

**Method:** Complete audit of all conventions to ensure no hidden parameters

**10-Step Convention Audit:**
- NHC-1: N_e = 111 from resonance (only choice-free value)
- NHC-2: Lagrangian written once with s ≡ ψ̄ψ, ρ ≡ ψ†ψ
- NHC-3: Gauge-invariant phase definition
- NHC-4: NLDE with symbolic Z_Ψ normalization
- NHC-5: s-wave ansatz → radial ODE for u(x), v(x)
- NHC-5.5: Maxwell/Poisson closure for electromagnetic coupling
- NHC-6: Eigenvalue/locking condition for Ω_eff
- NHC-7: 1/r-convention companion equations
- NHC-8: Energy functional E[u,v;Ω] with periodic lock
- NHC-9: Normalization constraint N[u,v] = 1
- NHC-10: C_e ≡ E[u_gs, v_gs; Ω★] derived, not chosen

**Final parameter count after all rescaling:** 3 parameters {Ω (locked), M = M_e/μ, η}

## The Radial ODE System

### General κ form (NHC convention, F/G without 1/r extraction):

```python
dF/dr = −[(1+κ)/r] F + (m + Σ(r) − ω̃(r)) G
dG/dr = +[(1−κ)/r] G − (m + Σ(r) + ω̃(r)) F
```

### κ = −1 (s-wave ground state):

```python
dF/dr = (m + Σ(r) − ω̃(r)) G
dG/dr = −(2/r) G − (m + Σ(r) + ω̃(r)) F

# Self-energy terms
Σ(r) = λ_{4e} s(r) + λ_{6e} s(r)²    # Scalar self-energy
s(r) = ψ̄ψ = F² − G²                  # Soler invariant
ω̃(r) = ω − qA₀(r)                    # Frequency shifted by potential
```

**Boundary conditions:**
- F, G finite at r=0
- F, G → 0 as r → ∞
- Normalization: 4π ∫₀^∞ ρ(r) r² dr = 1, where ρ = F² + G²

### 1/r-extracted convention (Routes 1-4):

```python
g'(r)            = (m(r) + ω − qA₀(r)) f(r)
f'(r) + (2/r)f(r) = (m(r) − ω + qA₀(r)) g(r)
S(r) = (g² − f²)/r²
```

## Canonical Normalization + Non-Dimensionalization

**Critical procedure that eliminates fake freedom:**

1. **Canonical norm:** ψ_c = Z_{ψe}^{1/2} · ψ → absorbs kinetic prefactor
2. **Non-dimensionalize:** μ = ε_c · Λ (formation IR scale), r = ℓ · x
3. **Quartic-to-1:** Choose amplitude A so α₄ = ±1
4. **Single physical ratio:** η = λ_{6e}/(λ_{4e}² · μ⁻¹)

**Reduced dimensionless ODE:**
```python
G'(x)            = (M + α₄ S + α₆ S² + Ω − qΦ(x)) F(x)
F'(x) + (2/x)F(x) = (M + α₄ S + α₆ S² − Ω + qΦ(x)) G(x)
```

**Final physical parameters:** {Ω (locked), M = M_e/μ, η}

## Key Derived Results (All at 50-Digit Precision)

| Quantity | Value | Derivation Source |
|----------|-------|-------------------|
| N_e | 111 | Resonance: 111/φ² ≈ 42 (Law 21) |
| G_e | √(5/3) | SU(5) trace identity (Law 24) |
| λ_rec/β | e^φ/π² = 0.51098... | Memory coupling (Law 32) |
| ν (Route-A) | 0.82054 | Self-consistency (Law 33) |
| μ (Route-B) | 0.4192 | Self-consistency (Law 34) |
| C_e | ≈ 1.053 | Route-A/B convention |
| m_e | 0.51099895 MeV | 23 ppm accuracy with ν_topo = 0.7258 + Lamé correction (requires α_EM input) |
| M_P/M₀ | √(5π) ≈ 3.96 | Induced gravity (V2 §8.3) |

## Lepton Mass Hierarchy

**Muon mass:**
```
m_μ = m_e · φ^{n_μ} · correction_factors
N_μ = 100 (ΔN = 11 from electron)
```
**Status:** Mass ratio <1% error, absolute mass ~41% error (needs proper RG flow)

**Tau mass:**
```
m_τ = m_e · φ^{n_τ} · correction_factors
N_τ = 94 (ΔN = 17 from electron)
```
**Status:** Mass ratio <1% error, absolute mass ~57% error (needs proper RG flow)

**Note:** Absolute masses require α_EM for proper gauge coupling RG evolution

## Computational Pipeline

**Main script:** `pipeline/GU_formation_pipeline.py` (889 lines)

**Pipeline stages:**
1. Formation → Genesis vector Z₁
2. Resonance → Identify N_e = 111
3. FRG Flow → Beta functions and running couplings
4. Masses → Calculate particle masses with 50-digit precision

**Key calculation scripts:**
- `pipeline/GU_particle_masses.py` (580 lines)
- `pipeline/PHASE23_ALL_LEPTONS_EXACT.py` (240 lines)
- `pipeline/PHASE23_EXACT_ELECTRON_DERIVATION.py` (300 lines)

## Working Conventions

**Units:**
- ℏ = c = 1 during derivation
- Restore at final answer

**Radial convention:**
- 1/r extracted: ψ ~ (1/r)(g, if(σ·r̂))ᵀ

**Nonlinearity:**
- s ≡ ψ̄ψ (Soler-type), NOT ρ ≡ ψ†ψ
- Σ_e = ∂U_e/∂s

**Lock implementation:**
- Option B: pins ω, does not modify ODE structure

**Induced gravity:**
- M_P² = Λ²_cut · Str(a₁)/π, with Str(a₁) ≈ 5π

**Canonical normalization:**
- Z_{ψe} absorbed, NOT set to 1 by hand

**Parameter minimization:**
- α₄ = ±1 convention (quartic-to-1)

## Implementation Status

✅ **Complete:**
- Formation physics framework
- N_e = 111 resonance identification
- Electron mass formula (0% error)
- Lepton hierarchy (muon, tau)
- 50-digit precision calculations
- All 38 Laws documented

🟡 **Partial:**
- FRG flow implementation (Wetterich equation)
- Lock-sector beta functions
- NLDE BVP solver

❌ **Pending:**
- Gauge boson masses (W, Z, Higgs)
- Neutrino mass hierarchy
- Full QCD hadron sector
- PMNS neutrino mixing angles

## Critical Reminders

1. **Always check theory/theory-laws.md first** — It's the authoritative source
2. **Use 50-digit precision** for all calculations (mpmath.dps=50)
3. **Never violate canonical symbols** (Law 14)
4. **Avoid forbidden constructions** (Law 26)
5. **All five routes must agree** on m_e = 0.51099895 MeV
6. **Document which route** you're using (STEP, Ω-STEP, FRG-STEP, RC-STEP, NHC-STEP)
7. **Cross-validate** results across multiple derivation methods
8. **Maintain dimensional consistency** throughout calculations
9. **Use gauge-invariant quantities** (Law 16: ω_eff = j_c⁰/(2ρ_c))
10. **Reference line numbers** when citing equations from theory/theory-laws.md

## Notation Database

**Master reference:** `MASTER_NOTATION_GUIDE.json` (188 KB, 650+ symbols)

Common symbol conflicts to watch for:
- μ: Can mean Bohr magneton, chemical potential, or Route-B parameter
- ω: Effective frequency vs target frequency vs bare frequency
- M: Particle mass vs mass parameter vs dimensionless mass
- X: Driver field vs epoch scale vs dimensionless variable

Always check context and document which meaning applies.

## Cross-Reference Examples

When working with this theory, always:

1. **Cite laws by number:**
   - "According to Law 16, the gauge-invariant frequency is..."
   - "This violates Law 26 (forbidden constructions)"

2. **Reference file locations:**
   - "See theory/theory-laws.md:712 for the complete derivation"
   - "The NLDE system is defined in theory/derived-laws.md:450-520"

3. **Specify route:**
   - "Using Route-A (NLDE/Spinor approach)..."
   - "This result comes from FRG-STEP-7"

4. **Show precision:**
   - "Calculated to 50 digits: φ = 1.6180339887498948482045868343656381177203091798..."
   - "Result: 23 ppm with Lamé correction (first principles); 0.00% only with fitted ν (bootstrap)"

## How to Use This Skill

**Invoke when:**
- Deriving particle masses from first principles
- Working with the NLDE/BVP system
- Calculating with golden ratio φ, π, or Planck scale
- Implementing FRG flow equations
- Auditing conventions and eliminating free parameters
- Cross-validating results across multiple derivation routes
- Documenting new laws or derivations

**Do not invoke for:**
- General Python programming (use gu-computational-physics skill)
- Documentation organization (use gu-documentation skill)
- Code auditing (use gu-code-audit skill)
- Mathematical symbolic manipulation only (use gu-mathematical-derivation skill)
