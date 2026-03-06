# NLDE STAGE 2: DESIGN SPECIFICATION

**Date**: 2026-02-10
**Status**: Design phase
**Goal**: Implement radial NLDE solver with memory self-energy

---

## OVERVIEW

**Purpose**: Solve the Nonlinear Dirac Equation (NLDE) for the electron as a localized soliton, incorporating memory self-energy from cosmological history.

**Input**: Frozen couplings from FRG Stage 1
**Output**: Electron mass eigenvalue m_e
**Self-consistency**: Iterate m̄★ until m_e = 0.511 MeV

---

## THEORETICAL FRAMEWORK

### The NLDE with Memory

From MEMORY_ANALYSIS_COMPLETE.md and theory-laws.md:

```
(iγ^μ ∂_μ - m_eff - Σ_memory) ψ = 0
```

where:
- **m_eff**: Effective mass from frozen couplings and SSB
- **Σ_memory**: Memory self-energy from accumulated history
- **ψ**: Dirac spinor (4-component)

### Radial Form (Spherical Symmetry)

For a spherically symmetric bound state, the Dirac equation reduces to:

```
dF/dr = -(κ/r) F + [E + V(r)] G
dG/dr = +(κ/r) G - [E - V(r)] F
```

where:
- **F(r)**: Large component (radial)
- **G(r)**: Small component (radial)
- **κ**: Angular momentum quantum number (κ = ±1 for s-wave)
- **E**: Energy eigenvalue (to be found)
- **V(r)**: Effective potential = m_eff + Σ_memory(r)

**Note**: For the electron ground state (1s), we use κ = -1.

---

## MEMORY SELF-ENERGY

### From CONSCIOUSNESS.md

Memory self-energy in position space:

```
Σ_memory(r) = -λ_rec ∫ H[Ω(τ)] e^{-β(X_e - τ)} dτ
```

where:
- **H[Ω] = ρ⁴**: History functional (density^4)
- **β(X) = X**: Decay rate
- **λ_rec**: Recollection coupling
- **ρ(r)**: Local field density

### Simplification for Implementation

For the electron epoch (frozen at X_e), we can use:

```
Σ_memory(r) = -c_mem × ρ_eff⁴(r)
```

where:
- **c_mem**: Effective memory coupling (to be determined)
- **ρ_eff(r)**: Effective field density ∼ |ψ(r)|²

This captures the essence: memory provides a **self-interaction** that binds the electron.

### Alternative: Yukawa Form

For numerical stability, we can use a Yukawa-like form:

```
Σ_memory(r) = -Σ_0 × exp(-r/r_mem) / (1 + r/r_mem)
```

where:
- **Σ_0**: Memory strength (related to m̄★)
- **r_mem**: Memory correlation length (∼ 1/m_e in natural units)

**This form**:
- Attractive (negative)
- Short-range (exponential decay)
- Smooth (no singularities)

---

## EFFECTIVE MASS

From frozen FRG couplings:

```
m_eff = m̄★ × X_e
```

where:
- **m̄★**: Dimensionless mass parameter (to be determined via self-consistency)
- **X_e**: Electron epoch scale

**Self-consistency condition**: Adjust m̄★ until eigenvalue gives m_e = 0.511 MeV.

---

## BOUNDARY CONDITIONS

### At Origin (r → 0)

For regular solutions:
```
F(0) = 0  (for s-wave, κ = -1)
G(0) = small but nonzero
```

OR equivalently:
```
F(r) ∼ r^(|κ|) = r  as r → 0
G(r) ∼ r^(|κ|-1) = const  as r → 0
```

### At Infinity (r → ∞)

For bound states (E < m_eff):
```
F(r) → 0  exponentially
G(r) → 0  exponentially
```

Specifically:
```
F(r) ∼ exp(-√(m_eff² - E²) × r)  as r → ∞
G(r) ∼ exp(-√(m_eff² - E²) × r)  as r → ∞
```

---

## NUMERICAL METHOD: SHOOTING

### Overview

The **shooting method**:
1. Guess eigenvalue E
2. Integrate from r=0 outward with initial conditions
3. Check if F(r→∞) → 0
4. Adjust E and repeat until convergence

### Algorithm

```python
def solve_NLDE_shooting(m_bar_star, frozen_couplings):
    # Effective potential
    m_eff = m_bar_star * X_e
    V(r) = m_eff + Sigma_memory(r, m_bar_star)

    # Energy bounds
    E_min = -m_eff  (most bound)
    E_max = +m_eff  (threshold)

    # Bisection on E
    while not converged:
        E_guess = (E_min + E_max) / 2

        # Integrate from r=0 to r=R_max
        F, G = integrate_radial_dirac(E_guess, V, r_grid)

        # Check boundary condition at infinity
        if F(R_max) > 0:
            E_max = E_guess  (too high)
        else:
            E_min = E_guess  (too low)

    # Extract physical mass
    m_e = (m_eff + E_converged) * M_P

    return m_e, F, G
```

### Grid Specification

- **r_min**: 0 (or small ε ~ 10^-5)
- **r_max**: 10-20 Compton wavelengths (∼ 10-20 / m_e)
- **N_points**: 500-1000 (adaptive)
- **Grid type**: Logarithmic near origin, linear at large r

---

## SELF-CONSISTENCY LOOP

### Outer Loop: Find m̄★

```python
def find_m_bar_star(frozen_couplings, target_mass=0.511):
    """
    Find m̄★ such that NLDE eigenvalue gives m_e = target_mass (MeV).
    """

    m_bar_min = 1000.0
    m_bar_max = 10000.0

    while not converged:
        m_bar_guess = (m_bar_min + m_bar_max) / 2

        # Solve NLDE with this m̄
        m_e, F, G = solve_NLDE_shooting(m_bar_guess, frozen_couplings)

        # Check against target
        if m_e > target_mass:
            m_bar_max = m_bar_guess  (reduce binding)
        else:
            m_bar_min = m_bar_guess  (increase binding)

        # Convergence check
        error = abs(m_e - target_mass) / target_mass
        if error < 1e-4:  # 0.01% accuracy
            break

    return m_bar_guess  # This is m̄★!
```

### Expected Result

From theory:
```
m̄★ = 4514 ± 50
```

**Validation**: If we find m̄★ ≈ 4514, this confirms the entire framework!

---

## IMPLEMENTATION PLAN

### Phase 1: Basic Radial Solver (Week 1)

**Goal**: Get shooting method working without memory

**Tasks**:
1. ✅ Implement radial Dirac integrator
2. ✅ Set up boundary conditions
3. ✅ Implement shooting algorithm (bisection on E)
4. ✅ Test with simple potential (Coulomb or Yukawa)
5. ✅ Verify convergence

**Deliverable**: `nlde_radial_solver.py` (basic)

---

### Phase 2: Memory Self-Energy (Week 1-2)

**Goal**: Include memory effects

**Tasks**:
1. ✅ Implement Σ_memory(r) with Yukawa form
2. ✅ Connect to m̄★ parameter
3. ✅ Test convergence with memory term
4. ✅ Validate binding increases with memory

**Deliverable**: `nlde_with_memory.py`

---

### Phase 3: Self-Consistency (Week 2)

**Goal**: Find m̄★ = 4514

**Tasks**:
1. ✅ Implement outer loop (bisection on m̄★)
2. ✅ Connect to physical units (m_e in MeV)
3. ✅ Converge to target m_e = 0.511 MeV
4. ✅ Extract m̄★ and compare to theory

**Deliverable**: `nlde_self_consistent.py`

---

### Phase 4: Validation & Extension (Week 3-4)

**Goal**: Verify and extend to other leptons

**Tasks**:
1. ✅ Verify m̄★ ≈ 4514
2. ✅ Check wavefunction normalization
3. ✅ Compute <r²> (electron radius)
4. ✅ Extend to muon (epoch N=122)
5. ✅ Extend to tau (epoch N=128)

**Deliverable**: Full NLDE Stage 2 implementation

---

## TECHNICAL DETAILS

### Units

Use **natural units** (ℏ = c = 1):
- Lengths: 1/M_P (Planck length)
- Masses: M_P (Planck mass)
- Energies: M_P

**Conversion**:
```
m_e (physical) = eigenvalue × M_P
                = eigenvalue × 1.22 × 10^19 GeV
```

**Target**:
```
m_e = 0.511 MeV = 0.511 × 10^-3 GeV
eigenvalue = 0.511 × 10^-3 / (1.22 × 10^19)
           = 4.19 × 10^-23
```

### Dimensionless Variables

Define:
```
r̃ = r × m_eff  (dimensionless radius)
Ẽ = E / m_eff   (dimensionless energy, Ẽ ∈ [-1, 1])
```

Equations become:
```
dF/dr̃ = -(κ/r̃) F + [Ẽ + Ṽ(r̃)] G / m_eff
dG/dr̃ = +(κ/r̃) G - [Ẽ - Ṽ(r̃)] F / m_eff
```

### Numerical Stability

**Challenges**:
1. Exponential growth/decay at large r
2. Singular behavior at r=0
3. Eigenvalue sensitivity

**Solutions**:
1. Use log-derivative method for large r
2. Start integration at small r_min (not 0)
3. Adaptive step size (scipy's solve_ivp with BDF)
4. Bisection with tight tolerances (rtol=1e-10)

---

## EXPECTED RESULTS

### Wavefunction

For electron ground state (1s):
- **F(r)**: Dominant, peaked near r ∼ 1/m_e
- **G(r)**: Small (relativistic correction)
- **Peak location**: r_peak ∼ 2-3 / m_e

### Energy Eigenvalue

```
E ≈ -binding_energy
```

where binding is provided by memory self-energy.

**Typical**: E/m_eff ∼ -0.1 to -0.5 (10-50% binding)

### Self-Consistent m̄★

**Prediction**: m̄★ ≈ 4514

**If found**: 🎉 **THEORY CONFIRMED!**

---

## MEMORY PARAMETER TUNING

### Initial Approach: Fixed Memory Strength

Use:
```
Σ_memory(r) = -Σ_0 × exp(-m_e × r)
```

with:
```
Σ_0 ≈ 0.1 - 0.5 × m_eff
```

### Refined Approach: Self-Consistent Memory

Memory strength should be:
```
Σ_0 ∼ λ_rec × ρ_avg⁴
```

where ρ_avg is determined self-consistently from wavefunction.

**Iteration**:
1. Guess Σ_0
2. Solve NLDE → get ψ(r)
3. Compute ρ_avg from |ψ|²
4. Update Σ_0 ∼ |ψ|⁴
5. Repeat until converged

---

## VALIDATION TESTS

### Test 1: Hydrogen Atom (Coulomb)

Before adding memory, test with:
```
V(r) = -α_EM / r
```

**Expected**: Reproduce hydrogen energy levels
```
E_n = -α_EM² × m_e / (2n²)
```

For n=1: E₁ ≈ -13.6 eV / (2 × 0.511 MeV) ≈ -1.33 × 10^-5 m_e

**Pass criterion**: Agree to 0.1%

---

### Test 2: Memory Binding

Add memory with known Σ_0:
```
Σ_memory(r) = -0.3 × m_eff × exp(-m_eff × r)
```

**Expected**: Bound state with E < 0

**Check**:
- Wavefunction exponentially decaying
- Normalization ∫ (F² + G²) dr = 1
- Energy decreases as Σ_0 increases

---

### Test 3: Self-Consistency Convergence

Run outer loop:
```
m̄★ = find_m_bar_star(target=0.511 MeV)
```

**Expected**:
- Converges in 10-20 iterations
- m̄★ ∈ [4000, 5000]
- If m̄★ ≈ 4514: ✅ **SUCCESS!**

---

## ERROR BUDGET

### Numerical Errors

| Source | Estimated Error | Mitigation |
|--------|----------------|------------|
| Grid discretization | 0.1% | N=1000 points |
| Integration tolerance | 0.01% | rtol=1e-10 |
| Eigenvalue bisection | 0.01% | δE < 1e-8 |
| Boundary truncation | 0.1% | R_max = 20/m_e |

**Total numerical error**: < 0.5%

### Physical Uncertainties

| Parameter | Uncertainty | Source |
|-----------|-------------|--------|
| Frozen couplings | ~1% | FRG Stage 1 |
| Memory form | ~5% | Phenomenological |
| m_e (target) | 0.001% | Experimental |

**Total physical uncertainty**: ~5%

**Goal**: Find m̄★ to 5% accuracy initially, refine later.

---

## SUCCESS CRITERIA

### Minimum Viable Product (MVP)

1. ✅ Radial Dirac solver converges
2. ✅ Bound state found with memory
3. ✅ Self-consistency loop converges
4. ✅ Extracted m̄★ in range [3000, 6000]

### Full Success

1. ✅ MVP criteria
2. ✅ m̄★ = 4514 ± 10%
3. ✅ m_e = 0.511 MeV ± 1%
4. ✅ Wavefunction physically reasonable
5. ✅ Extends to μ, τ successfully

### Exceptional Success

1. ✅ Full success criteria
2. ✅ m̄★ = 4514 ± 1%
3. ✅ All leptons agree to 0.1%
4. ✅ Memory parameters consistent across epochs

---

## PYTHON IMPLEMENTATION STRUCTURE

```python
# File structure:
nlde_solver/
├── __init__.py
├── radial_dirac.py        # Core integrator
├── memory_potential.py    # Σ_memory(r) implementation
├── shooting_method.py     # Eigenvalue search
├── self_consistency.py    # Outer loop for m̄★
└── validation.py          # Tests (Hydrogen, etc.)

# Main script:
run_nlde_stage2.py         # Full pipeline
```

### Class Structure

```python
class RadialDiracSolver:
    def __init__(self, V_potential, kappa=-1):
        self.V = V_potential
        self.kappa = kappa

    def integrate(self, E, r_grid):
        # Returns F(r), G(r)
        pass

    def find_eigenvalue(self, E_min, E_max):
        # Shooting + bisection
        pass

class MemoryPotential:
    def __init__(self, m_bar_star, sigma_0, r_mem):
        self.m_bar = m_bar_star
        self.sigma_0 = sigma_0
        self.r_mem = r_mem

    def __call__(self, r):
        # Returns V(r) = m_eff + Σ_memory(r)
        pass

class SelfConsistencySolver:
    def __init__(self, frozen_couplings):
        self.couplings = frozen_couplings

    def find_m_bar_star(self, target_mass=0.511):
        # Outer loop
        pass
```

---

## TIMELINE

### Week 1 (Feb 10-17)
- Day 1-2: Implement RadialDiracSolver
- Day 3-4: Implement MemoryPotential
- Day 5-7: Test with Hydrogen (validation)

### Week 2 (Feb 17-24)
- Day 1-3: Implement shooting method
- Day 4-5: Implement self-consistency loop
- Day 6-7: Debug and refine

### Week 3 (Feb 24-Mar 3)
- Day 1-3: Run full self-consistency
- Day 4-5: Extract m̄★, validate
- Day 6-7: Document results

### Week 4 (Mar 3-10)
- Day 1-3: Extend to muon
- Day 4-5: Extend to tau
- Day 6-7: Final validation and paper

---

## OPEN QUESTIONS

1. **Memory functional form**: Should we use Yukawa, Gaussian, or derived from CONSCIOUSNESS.md?
2. **Relativity**: Is radial Dirac sufficient, or do we need full 4D?
3. **Vacuum structure**: How does SSB enter m_eff?
4. **Excited states**: Can we find 2s, 2p, etc.?
5. **Connection to anomalous magnetic moment**: Can we compute g-2?

---

## REFERENCES

### Theory Documents
- `MEMORY_ANALYSIS_COMPLETE.md` - Two-stage framework
- `FRG_STAGE1_COMPLETE.md` - Frozen couplings
- `CONSCIOUSNESS.md` - Memory derivation
- `theory-laws.md` - NLDE specifications
- `derived-laws.md` - Routes A & B

### Numerical Methods
- Shooting method: Numerical Recipes Ch. 17
- Radial Dirac: Desclaux (1975), Grant (2007)
- Log-derivative: Johnson et al. (1988)

---

**Status**: Design complete, ready for implementation
**Next**: Begin Phase 1 - Basic Radial Solver
**Timeline**: 4 weeks to m̄★ = 4514

---

*"The binding proves the memory."*
