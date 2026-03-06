# FRG DIAGNOSTIC: Gauge Coupling Issue

**Date**: 2026-02-10
**Status**: ⚠️ Problem identified

---

## ISSUE

FRG integration shows α_EM evolving in **wrong direction**:

```
τ=0:    1/α_EM = 47.84   (Planck scale)
τ=36.4: 1/α_EM = 31.16   (partial run, 68% to electron scale)
Target: 1/α_EM = 137.036 (electron scale)
```

**Problem**: 1/α_EM is **decreasing** (α_EM getting stronger), but we need it to **increase** from ~50 to ~137.

---

## ANALYSIS

### Beta Function Signs

Standard one-loop RG equation:
```
dα_i/dt = +(b_i/2π) α_i²
```

In τ-time (τ = -t, UV→IR direction):
```
dα_i/dτ = -(b_i/2π) α_i²
```

**Coefficients** (Standard Model):
- b₁ = +41/10  (U(1)_Y, Landau pole)
- b₂ = -19/6   (SU(2)_L, asymptotically free)
- b₃ = -7      (SU(3)_C, asymptotically free)

**In τ-time (UV→IR)**:
- α₁: dα₁/dτ < 0 → α₁ **decreases** → 1/α₁ **increases** ✅
- α₂: dα₂/dτ > 0 → α₂ **increases** → 1/α₂ **decreases** ✅ (correct for weak)
- α₃: dα₃/dτ > 0 → α₃ **increases** → 1/α₃ **decreases** ✅ (correct for strong)

**Electromagnetic**:
```
α_EM = (3/8) α₁ + (5/8) α₂
```

From trajectory:
- α₁ decreases: 1/α₁ goes 67.78 → 91.52 (increasing)
- α₂ increases: 1/α₂ goes 40.67 → 22.32 (decreasing)
- α_EM increases: 1/α_EM goes 47.84 → 31.16 (decreasing)

**Conclusion**: α₂ term (5/8 weight) dominates over α₁ term (3/8 weight), causing α_EM to increase.

---

## ROOT CAUSE

### Initial Condition Problem

**Current**:
```
α_GUT = 1/(8πφ) ≈ 0.0246
→ 1/α_GUT ≈ 40.67
→ 1/α_EM(M_P) ≈ 47.84
```

**Required logic**:
- At M_P (Planck scale): Need 1/α_EM >> 137
- At X_e (electron scale): Need 1/α_EM = 137
- Therefore: α_EM must **decrease** (1/α must increase) from Planck → electron

But currently: 1/α_EM is decreasing (going wrong way)!

---

## POSSIBLE CAUSES

### 1. α_GUT Formula Wrong

The formula α_GUT = 1/(8πφ) gives:
```
1/α_GUT = 8πφ ≈ 40.67
```

But in SU(5) GUT models, typically:
```
1/α_GUT ≈ 24-25  (at M_GUT ~ 10^16 GeV)
```

**Question**: Is α_GUT = 1/(8πφ) valid at M_P or at M_GUT?

---

### 2. Wrong Scale for Initial Conditions

Currently starting at τ=0 → X=M_P (Planck scale).

But SU(5) unification happens at:
- M_GUT ~ 10^16 GeV (lower than M_P ~ 10^19 GeV)
- Maybe should start at M_GUT, not M_P?

---

### 3. Beta Function Sign Errors

Double-check signs in τ-time conversion:
```python
# In t-time (IR→UV, t negative):
dα_i/dt = +(b_i/2π) α_i²

# In τ-time (UV→IR, τ = -t):
dα_i/dτ = -(b_i/2π) α_i²
```

Is this correct? Let me verify:
- t goes from 0 (UV) to negative (IR)
- τ = -t goes from 0 (UV) to positive (IR)
- dτ/dt = -1
- dα/dτ = (dα/dt)(dt/dτ) = (dα/dt)(-1) = -(dα/dt)

Yes, sign flip is correct. ✅

---

### 4. α_EM Combination Wrong at Planck Scale?

Standard electroweak unification:
```
α_EM = (3/8) α₁ + (5/8) α₂
```

This is valid at/below electroweak scale (~100 GeV).

**Question**: Is this combination valid at Planck scale before EW symmetry breaking?

At Planck scale, we might have:
- Pure SU(5) with single α_GUT
- EW breaking happens during RG flow
- α_EM emerges only after breaking

---

## SUSPECTED RESOLUTION

### Theory-Laws.md Check Needed

Need to check:
1. **§EVAL-7**: Initial conditions for gauge couplings
2. **§EVAL-8**: Beta functions and signs
3. **SU(5) breaking scale**: When does SU(5) → SM happen?
4. **α_GUT value**: Is 1/(8πφ) the correct formula?

### Key Questions

1. At Planck scale (τ=0), do we have:
   - Option A: Three separate α₁, α₂, α₃ (already broken to SM)
   - Option B: Unified α_GUT (still in SU(5) phase)

2. If Option B, when does SU(5) → SM breaking occur?
   - At M_GUT ~ 10^16 GeV?
   - During the flow from M_P to m_e?

3. What is the correct initial value?
   - 1/α_GUT = 8πφ ≈ 40.67?
   - Or something else?

---

## NEXT STEPS

1. **Read theory-laws.md §EVAL-7** (Initial conditions)
2. **Read theory-laws.md §EVAL-8** (Beta functions)
3. **Check derived-laws.md** for α_GUT derivation
4. **Understand SU(5) → SM breaking** in GU framework

Then:
5. Correct initial conditions
6. Re-run FRG
7. Verify α_EM → 1/137.036

---

## CURRENT STATUS

✅ **What works**:
- Four-fermion couplings decay to zero ✅
- Mass runaway validates theory (no FRG equilibrium) ✅
- Integration handles overflow gracefully ✅

❌ **What needs fixing**:
- Gauge coupling initial conditions ❌
- α_EM convergence to 1/137.036 ❌

---

**Confidence**: Need to consult theory-laws.md to resolve gauge coupling issue.
