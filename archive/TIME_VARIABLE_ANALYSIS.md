# TIME VARIABLE ANALYSIS FOR FRG

## The Sign Confusion Problem

### Original RG Time (t):
```
X evolves: X₀ (Planck) → X_e (electron)
RG time:   t = ln(X/X₀)
Range:     t ∈ [0, -53.4]  (NEGATIVE!)
```

### Why This Creates Problems:

**Original beta functions (from theory):**
```python
dm̄/dt = -(1-η_ψ) m̄ + ...
```

Since η_ψ ~ 0.002 << 1:
```
dm̄/dt ≈ -0.998 m̄
```

With t going from 0 to **negative** values:
```
m̄(t) ∝ e^{-(-0.998)t} = e^{+0.998|t|} → GROWS!
```

This is **physically correct** for the UV→IR flow (mass grows as X decreases).

But **numerically problematic** because:
1. Memory accumulator R̄ should accumulate positively
2. Negative time confuses sign conventions
3. Integration stiffness from decreasing t

---

## Solution: Use Positive Time τ = -t

### New Time Variable:
```
τ = -t
dτ = -dt
τ ∈ [0, +53.4]  (POSITIVE!)
```

### How To Transform Beta Functions:

**Chain rule:**
```
df/dτ = df/dt · dt/dτ = df/dt · (-1) = -df/dt
```

So **multiply ALL beta functions by -1**.

---

## The CRITICAL Subtlety: Memory Integral

### Memory Definition (always in terms of PAST):
```
R̄(τ) = ∫_{past}^{present} m̄⁴(τ') e^{-β(present - τ')} dτ'
```

In **both** time conventions:
- Past = earlier values = smaller absolute values
- Present = current τ or t

### In Original t (negative):
```
t ∈ [0, -53.4]
Past: t' closer to 0
Present: current t (more negative)

R̄(t) = ∫_0^t m̄⁴(t') e^{-β(t - t')} dt'  (t' from 0 to t)
```

Since t < 0, we're integrating **backward**.

### In New τ (positive):
```
τ ∈ [0, +53.4]
Past: τ' closer to 0
Present: current τ (more positive)

R̄(τ) = ∫_0^τ m̄⁴(τ') e^{-β(τ - τ')} dτ'  (τ' from 0 to τ)
```

Now integrating **forward**.

### The Key Insight:

**The memory integral DIRECTION is naturally forward in both cases!**

In t: integrating from t'=0 to t'=t (where t<0) is numerically "backward"
In τ: integrating from τ'=0 to τ'=τ (where τ>0) is numerically "forward"

**But the ACCUMULATION is the same!**

### Local Form (Law 28):

**In original t:**
```
dR̄/dt = m̄⁴ - R̄  [accumulates as t increases]
```

**Wait! t DECREASES (goes toward -53.4)!**

So actually:
```
dR̄/dt = m̄⁴ - R̄
```
means R̄ accumulates as we integrate forward (t → more negative).

**In new τ:**
```
dR̄/dτ = -dR̄/dt = -(m̄⁴ - R̄) = -m̄⁴ + R̄  ❌ WRONG!
```

This makes R̄ DECREASE!

---

## The Fix: Redefine Memory In Terms of τ From The Start

Instead of blindly flipping signs, **redefine** the memory accumulator for positive time:

```
R̄(τ) = ∫_0^τ m̄⁴(τ') e^{-β(τ - τ')} dτ'
```

Take derivative:
```
dR̄/dτ = m̄⁴(τ) + ∫_0^τ m̄⁴(τ') e^{-β(τ - τ')} · (-(-β)) dτ'
      = m̄⁴(τ) - β ∫_0^τ m̄⁴(τ') e^{-β(τ - τ')} dτ'
      = m̄⁴(τ) - β R̄(τ)
```

**With β=1 (our choice):**
```
dR̄/dτ = m̄⁴ - R̄  [SAME FORM! No sign flip!]
```

---

## Correct Transformation Table

| Original (t) | Transform | New (τ=−t) |
|--------------|-----------|------------|
| dm̄/dt | × (−1) | dm̄/dτ |
| dλ̄/dt | × (−1) | dλ̄/dτ |
| dα/dt | × (−1) | dα/dτ |
| **dR̄/dt** | **NO CHANGE!** | **dR̄/dτ** |

**Memory accumulator is SPECIAL: it's defined by an integral over the past, not a differential equation subject to chain rule!**

---

## Correct Beta Functions (τ = -t)

```python
# RG time: τ ∈ [0, 53.4]

# MASS (sign flipped)
dm̄/dτ = +(1 - η_ψ) m̄
        - (1/π²) λ̄_S m̄/(1+m̄²)
        + λ_rec R̄/(1+m̄²)  # Memory damping (positive in τ-time)

# FOUR-FERMION (signs flipped)
dλ̄_S/dτ = -(2 + 2η_ψ) λ̄_S + ...
dλ̄_V/dτ = -(2 + 2η_ψ) λ̄_V + ...

# GAUGE (signs flipped)
dα_i/dτ = -(b_i/2π) α_i²

# MEMORY ACCUMULATOR (NO SIGN FLIP!)
dR̄_mem/dτ = m̄⁴ - R̄_mem  [SAME AS ORIGINAL!]
```

---

## Physical Interpretation

**In τ-time (forward):**
- τ increases from 0 to 53.4
- m̄ grows from 0.01 toward large value
- R̄_mem accumulates: starts at 0, grows toward m̄⁴
- When R̄_mem ~ m̄⁴, damping term ~ λ_rec m̄²
- Equilibrium: growth = damping → m̄ stabilizes

**Without memory:**
- m̄ grows exponentially: m̄ ∝ e^{τ}
- At τ=53.4: m̄ ~ e^{53} ~ 10²³ (runaway!)

**With memory:**
- R̄_mem builds up
- Eventually R̄_mem ~ m̄⁴
- Damping term ~ λ_rec m̄² balances growth
- m̄ saturates at equilibrium value

---

## Bottom Line

**The confusion was:**
Blindly applying chain rule to ALL equations, including the memory accumulator.

**The resolution:**
Memory accumulator is defined by a forward-time integral in BOTH conventions.
Its differential form is the SAME: `dR̄/dτ = m̄⁴ - R̄`.

Only the OTHER beta functions flip sign when changing from t to τ.

---

**Next:** Implement with correct signs!
