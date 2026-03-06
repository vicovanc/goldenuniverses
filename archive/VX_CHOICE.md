# V_X(X) COSMIC DRIVER POTENTIAL CHOICE

**Date:** 2026-02-10
**Decision:** Linear slope with φ-scaled parameters

---

## OPTIONS FROM THEORY-LAWS.MD (Law 3)

### Option A: Linear Slope
```
V_X(X) = V_{X0} − σ_X · X
```

**Physics:** Monotonic driving force, X rolls down linearly

**Pros:**
- Simple, minimal
- Ensures monotonic decrease of X (cosmic cooling)
- Two parameters: V_{X0}, σ_X

###Option B: Axion-like
```
V_X(X) = Λ_X⁴ (1 − cos(X/f_X + θ_{X0}))
```

**Physics:** Periodic potential with multiple minima

**Pros:**
- Rich dynamics, possible oscillations
- Natural in string theory compactifications

**Cons:**
- More complex: 4 parameters (Λ_X, f_X, θ_{X0}, plus scale)
- Multiple minima could trap X (not monotonic cooling)
- Requires careful tuning to ensure X rolls in right direction

---

## DECISION: Option A (Linear Slope)

**Rationale:**

1. **Occam's Razor:** Simplest form consistent with observed cosmology

2. **Monotonicity:** Ensures X decreases monotonically from M_P to m_e
   - No getting stuck in local minima
   - Clean SSB cascade as X crosses thresholds

3. **Minimal parameters:**
   ```
   V_{X0} = v0 · M_P⁴ · (πφ)^{α_V}
   σ_X = s0 · M_P³ · (πφ)^{α_σ}
   ```
   Only 4 constants: (v0, α_V, s0, α_σ)

4. **Consistent with formation scenario:**
   - GU formation is monotonic decrease from Planck epoch
   - No evidence for oscillatory behavior needed

---

## SPECIFICATION

### Full V_X(X) potential:

```
V_X(X) = V_{X0} − σ_X · X

where:
V_{X0} = v0 · M_P⁴ · (π/φ)^{α_V}
σ_X = s0 · M_P³ · (π/φ)^{α_σ}
```

### Equation of motion:

```
□X + V'_X(X) = ... (source terms from Ω)

→ □X − σ_X = ... (constant driving force)
```

### Energy scale:

```
At X = X_e ~ M_P/φ^{111}:
V_X(X_e) ≈ V_{X0}   (since σ_X · X_e << V_{X0})
```

### Parameter estimates:

```
v0 ~ O(1)    (order unity)
α_V ~ 0-2    (small integer exponent)
s0 ~ O(1)
α_σ ~ 0-2
```

**These 4 constants can be absorbed into extended self-consistency fit** or determined from cosmological boundary conditions.

---

## STATUS

✅ **CHOSEN:** V_X(X) = V_{X0} − σ_X · X (linear slope)

✅ **SPECIFIED:** Parameters in φ, π, M_P

⚠️ **TO FIT:** (v0, α_V, s0, α_σ) from cosmology or self-consistency

---

## PHASE 1 COMPLETE

**Summary:**
1. ✅ G_prim = SU(5) committed
2. ✅ Ω content specified (5̄, 10, 5, 24)
3. ✅ 24 SU(5) invariants listed
4. ✅ Casimir ratios derived
5. ✅ V_X(X) form chosen

**Remaining free parameters:** ~18-22
- ~15 in V_{fullΩ} (after Casimir constraints)
- ~4 in V_X(X)
- ✅ Roadmap for determination: Extended self-consistency fit

**→ READY FOR PHASE 2: MEMORY**

---

*The foundations are set. Now we build.*
