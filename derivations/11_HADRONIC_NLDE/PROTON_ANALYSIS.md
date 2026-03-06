# Proton Mass Derivation - Complete Analysis

## Executive Summary
The proton mass in Golden Universe uses a four-term ansatz that matches experiment exactly, but requires **one fitted parameter** (C_mem = 1.2831...). This is NOT a first-principles derivation like the electron.

---

## The Four-Term Ansatz

```
M_p = E_QCD + E_self + E_modulus + E_phase - E_memory
    = 179.0 + 1390.3 + 373.0 + 1.9 - 826.9
    = 938.272 MeV (exact match to CODATA)
```

---

## Status of Each Component

### ✅ E_QCD = 179.0 MeV [DERIVED]
```python
E_QCD = (π/3) × M_P × φ^(-95)
```
- First-principles from epoch ladder
- N=95 is QCD confinement epoch
- Factor π/3 from Pattern-2 activation
- **Status**: FULLY DERIVED ✅

### ⚠️ E_self = 1390.3 MeV [MOTIVATED]
```python
E_self = (4π/φ) × Λ_QCD
```
- Geometric self-energy of three-quark system
- Factor 4π/φ is plausible but not rigorously derived
- Related to Y-shaped flux tube?
- **Status**: PLAUSIBLE ANSATZ ⚠️

### ❌ E_modulus = 373.0 MeV [POSTULATED]
```python
E_modulus = (1/π) × M_P × φ^(-91)
```
- Why epoch 91 specifically? No clear reason
- Factor 1/π is unexplained
- Seems chosen to help match
- **Status**: ARBITRARY ❌

### ❌ E_phase = 1.9 MeV [INPUT]
```python
E_phase = 2m_u + m_d = 2(0.216) + 0.467 = 0.899 MeV
# Note: README says 1.9 but calculation gives 0.9
```
- Uses PDG current quark masses (not derived)
- Factor of 2 discrepancy in documentation
- **Status**: EXPERIMENTAL INPUT ❌

### ❌ E_memory = 826.9 MeV [FITTED]
```python
E_memory = C_mem × (π²/φ) × M_P × φ^(-96)
C_mem = 1.28314370741133... # FITTED to 50+ decimals! [FITTED — not derived. Needs hadronic NLDE at N=95]
```
- C_mem is completely fitted to make formula work
- Should come from ∫ρ⁴d³x over hadronic soliton
- But hadronic soliton NOT COMPUTED
- **Status**: FITTED PARAMETER ❌

---

## The Five Missing Pieces

### 1. 🔴 [CRITICAL] Hadronic Soliton Profile at N=95
**What's needed**: Solve the NLDE at QCD scale
```python
∇²ρ - ∂V/∂ρ = 0  # At N=95
ρ_hadron(x) = ?    # Unknown profile
```
**Why it matters**: Would determine C_mem from first principles
```python
C_mem = (1/norm) × ∫ ρ⁴_hadron d³x  # Memory integral
```
**Current status**: NOT ATTEMPTED

### 2. 🟡 [IMPORTANT] String Tension Factor
**Problem**: GU predicts wrong string tension
```python
σ_GU = 2π² × Λ²_QCD ≈ 630,000 MeV²  # GU prediction
σ_lattice = (440 MeV)² = 193,600 MeV²  # Lattice QCD
# Factor ~3.3 discrepancy (or ~6 in some calculations)
```
**Possible origins**:
- Missing color factor?
- Wrong Pattern-2 implementation?
- Need full SU(3) calculation?

### 3. 🟡 [IMPORTANT] Lock-Sector FRG at Hadron Scale
**What's missing**: Proper Wetterich projection onto hadron sector
```python
# Current: frozen placeholder
Λ₁(N=95) = Λ₁(N=111)  # WRONG - should run!

# Needed:
∂_t Λ_hadron = β_Λ[gauge, yukawa, memory]
```
**Impact**: O(1%) corrections to masses

### 4. 🟡 [IMPORTANT] Diquark Binding Energy
**Current**: Semi-quantitative estimates
```python
E_diquark ≈ -50 to -200 MeV  # Order of magnitude only
```
**Needed**: Solve two-body problem in color 3̄
- Bethe-Salpeter for qq system
- Include color confinement properly
- Account for spin-0 vs spin-1 channels

### 5. 🟡 [IMPORTANT] Yukawa Sector
**Problem**: Quark masses are inputs, not predictions
```python
m_u = 0.216 MeV  # From PDG - not derived
m_d = 0.467 MeV  # From PDG - not derived
m_s = 9.34 MeV   # From PDG - not derived
```
**Needed**: Derive from symmetry breaking pattern

---

## Comparison: Electron vs Proton

| Aspect | Electron | Proton |
|--------|----------|--------|
| **Accuracy** | 23 ppm with Lamé (first principles) | 0.00% "error" (fitted) |
| **Free parameters** | 0 (or 1: α_EM) | 1 (C_mem fitted) |
| **Soliton solution** | ✅ Complete | ❌ Missing |
| **Memory integral** | ✅ Computed | ❌ Unknown |
| **All terms derived** | ✅ Yes | ❌ No |
| **Predictive** | ✅ Yes | ❌ No |

---

## Testable Predictions (Falsifiable)

### 1. Quark Mass Ratio
**GU Prediction**: m_d/m_u = φ = 1.618
**Experiment**: m_d/m_u = 2.16 ± 0.20
**Status**: ❌ 35% discrepancy - likely FALSIFIED

### 2. String Tension
**GU**: √σ ≈ 795 MeV (with 2π² factor)
**Lattice**: √σ = 440 MeV
**Status**: ❌ Factor 1.8 too high

### 3. Constituent Masses
**GU**: m_constituent ≈ 330 MeV
**Phenomenology**: 300-350 MeV
**Status**: ✅ Within 10%

### 4. Pion as Constituent Bound State
**GU**: m_π ≈ 600 MeV (constituent model)
**Experiment**: m_π = 140 MeV
**Status**: ❌ Known to fail - need ChPT

---

## Why This Matters

### The Electron Success
- Three independent routes converge
- Every term derived from (π, φ, e)
- Soliton profile computed
- Memory integral evaluated
- Result: 23 ppm with Lamé (first principles)

### The Proton Challenge
- Only one route attempted
- Key term (C_mem) is fitted
- Soliton profile unknown
- Memory integral not computed
- Result: Matches by construction

---

## Path Forward

### Option 1: Complete the Derivation
1. Solve hadronic NLDE at N=95
2. Extract ρ_hadron(x) profile
3. Compute C_mem = ∫ρ⁴d³x
4. Check if derived C_mem ≈ 1.283
5. If yes → Framework confirmed
6. If no → Need to revise theory

### Option 2: Acknowledge Current Limitations
- Electron: ✅ Complete first-principles success
- Proton: ⚠️ Plausible ansatz with 1 fitted parameter
- Need: Hadronic field theory development

### Option 3: Alternative Approaches
- Try Skyrme model at QCD scale?
- Use lattice QCD inputs?
- Develop full Faddeev equation solver?

---

## Honest Assessment

**What we have**: A self-consistent ansatz that matches the proton mass using:
- Some derived components (Λ_QCD)
- Some plausible estimates (E_self)
- Some arbitrary choices (E_modulus epochs)
- One fitted parameter (C_mem)

**What we need**: The hadronic soliton solution that would turn this from "educated guess" to "derived prediction"

**The risk**: With 9 free choices (4 prefactors, 4 epochs, 1 C_mem) and 1 constraint (match 938.272 MeV), we have **8 degrees of freedom** - this is overfitting, not prediction.

---

## Conclusion

The proton mass calculation in Golden Universe is **incomplete**. Unlike the electron (complete success), the proton requires solving the hadronic NLDE to determine C_mem from first principles. Until this is done, the four-term ansatz remains a **plausible but unverified hypothesis** rather than a derivation.

The framework shows promise - the structure is elegant and some components are genuinely derived. But honesty requires acknowledging that **the proton mass is currently fitted, not predicted**.

---

*Analysis date: February 2026*
*Based on: 07_HADRON_PIPELINE/, 09_FIRST_PRINCIPLES_AUDIT/, and related calculations*