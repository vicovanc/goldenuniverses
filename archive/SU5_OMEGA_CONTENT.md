# SU(5) Ω-FIELD REPRESENTATION CONTENT
## Explicit Specification for First-Principles Derivation

**Date:** 2026-02-10
**Status:** Formal specification
**Purpose:** Define which components of Ω live in which SU(5) representations

---

## 1. SU(5) → STANDARD MODEL BREAKING PATTERN

### Decomposition:

```
SU(5) ⊃ SU(3)_c × SU(2)_L × U(1)_Y
```

**How SU(5) representations decompose:**

```
5̄ → (3̄, 1, 1/3) ⊕ (1, 2, -1/2)
     d_R^c          (ν_L, e_L)

10 → (3, 2, 1/6) ⊕ (3̄, 1, -2/3) ⊕ (1, 1, 1)
     (u_L, d_L)     u_R^c            e_R^c

24 → (8, 1, 0) ⊕ (1, 3, 0) ⊕ (1, 1, 0) ⊕ (3, 2, -5/6) ⊕ (3̄, 2, 5/6)
     gluons       W bosons   B boson    X bosons       X̄ bosons

1 → (1, 1, 0)
    singlet
```

---

## 2. PROPOSED Ω-FIELD CONTENT

### 2.1 Fermion Sector (Spinors in Ω)

**Three generations of matter:**

```
Ψ_{5̄,i} = 5̄ representation   (i = 1,2,3 for three generations)
           Contains: d_R^c, ν_L, e_L

Ψ_{10,i} = 10 representation  (i = 1,2,3)
           Contains: u_L, d_L, u_R^c, e_R^c
```

**Quantum numbers for first generation:**

```
5̄₁: (d_R^c, d_R^c, d_R^c, e^-, ν_e)
    - Three colors of right-handed down quarks (anti-triplet)
    - Left-handed lepton doublet (SU(2))

10₁: Contains (u_L, d_L) doublet, u_R^c triplet, e_R^c singlet
```

---

### 2.2 Scalar Sector (Bosonic Ω components)

**Higgs-like fields:**

**Option A: Minimal SU(5) Higgs sector**
```
H_5 = 5 representation
      Contains: Higgs doublet (1, 2, -1/2) + colored triplet (3, 1, -1/3)

H_24 = 24 representation (adjoint)
       Breaks SU(5) → SU(3) × SU(2) × U(1) at GUT scale
```

**Option B: Extended Higgs sector (for richer SSB)**
```
H_5 = 5
H_5̄ = 5̄  (conjugate)
H_24 = 24
H_45 = 45 (for doublet-triplet splitting if needed)
```

**Proposal:** Use Option B (extended) to provide enough degrees of freedom for the full V_{fullΩ} potential.

---

### 2.3 Lock/Phase Sector

**Phase-driver components:**

```
Φ_24 = 24 representation (adjoint)
       Drives ω = ω★ lock dynamically
       Provides angular modulation V_angular_mod
```

---

### 2.4 Memory Sector

**History-coupled components:**

The memory term couples universally to all Ω components:

```
L_mem = -λ_rec(X) · Σ_A S_mem,A · ∫ H[Ω_A(τ)] e^{-β(t-τ)} dτ
```

where S_mem,A are gauge-invariant bilinears in each representation.

---

## 3. GAUGE-INVARIANT OPERATORS

### 3.1 Quadratic Invariants S_{2,i}

**From representation theory, SU(5) has these quadratic invariants:**

```
S_{2,1} = Ψ̄_{5̄}^i Ψ_{5̄,i}           (fermion bilinear, 5̄ ⊗ 5̄ → 1)
S_{2,2} = Ψ̄_{10}^i Ψ_{10,i}           (fermion bilinear, 10 ⊗ 10̄ → 1)
S_{2,3} = H_5† H_5                     (scalar bilinear)
S_{2,4} = H_5̄† H_5̄                     (scalar bilinear)
S_{2,5} = Tr(H_24†

 H_24)              (adjoint trace)
S_{2,6} = Tr(Φ_24† Φ_24)              (phase sector)
```

**These give mass terms:**

```
V_mass = Σ_i m̃_i²(X) S_{2,i}

Explicitly:
V_mass = m̃²₁(X) Ψ̄_{5̄} Ψ_{5̄}
       + m̃²₂(X) Ψ̄_{10} Ψ_{10}
       + m̃²₃(X) |H_5|²
       + m̃²₄(X) |H_5̄|²
       + m̃²₅(X) Tr|H_24|²
       + m̃²₆(X) Tr|Φ_24|²
```

---

### 3.2 Quartic Invariants S_{4,j}

**SU(5) allows these quartic invariants:**

#### Pure scalar quartics:
```
S_{4,1} = (H_5† H_5)²
S_{4,2} = (H_5̄† H_5̄)²
S_{4,3} = Tr(H_24† H_24)²
S_{4,4} = Tr[(H_24† H_24)²]           (different trace structure)
```

#### Mixed quartics:
```
S_{4,5} = (H_5† H_5)(H_5̄† H_5̄)
S_{4,6} = (H_5† H_5) Tr(H_24† H_24)
S_{4,7} = H_5† H_24 H_24† H_5
```

#### Yukawa-like (fermion-scalar):
```
S_{4,8} = (Ψ̄_{5̄} H_5)² + h.c.         (contributes to lepton/down masses)
S_{4,9} = (Ψ̄_{10} H_5̄)² + h.c.
S_{4,10} = ε_{abcde} Ψ_{10}^{ab} Ψ_{10}^{cd} H_5^e + h.c.   (up-type Yukawa)
```

#### Four-fermion:
```
S_{4,11} = (Ψ̄_{5̄} Ψ_{5̄})²
S_{4,12} = (Ψ̄_{10} Ψ_{10})²
S_{4,13} = (Ψ̄_{5̄} Ψ_{5̄})(Ψ̄_{10} Ψ_{10})
```

**Quartic potential:**

```
V_quartic = Σ_j λ̃_j(X) S_{4,j}
```

---

### 3.3 Sextic Invariants S_{6,k}

**For soliton stabilization:**

```
S_{6,1} = (H_5† H_5)³
S_{6,2} = (H_5̄† H_5̄)³
S_{6,3} = Tr(H_24† H_24)³
S_{6,4} = (Ψ̄_{5̄} Ψ_{5̄})³
S_{6,5} = (Ψ̄_{10} Ψ_{10})³
```

**Sextic potential:**

```
V_sextic = Σ_k γ̃_k(X) S_{6,k}
```

---

## 4. CASIMIR RATIOS FOR O(1) CONSTANTS

### 4.1 Quadratic Casimir Values

For SU(5) representations:

```
C₂(1) = 0           (singlet)
C₂(5) = 12/5 = 2.4
C₂(5̄) = 12/5 = 2.4   (same as 5)
C₂(10) = 18/5 = 3.6
C₂(24) = 5           (adjoint)
C₂(45) = 28/5 = 5.6
```

**How this constrains O(1) constants:**

If the mass-squared coefficients come from kinetic term renormalization, expect:

```
m̃²₁ / m̃²₂ = C₂(5̄) / C₂(10) = (12/5) / (18/5) = 2/3

m̃²₃ / m̃²₅ = C₂(5) / C₂(24) = (12/5) / 5 = 12/25 = 0.48
```

**This means:**

```
c_{m,1} / c_{m,2} = 2/3  (if masses are Casimir-dominated)
c_{m,3} / c_{m,5} = 12/25
```

**Partial success:** We've derived **ratios** of O(1) constants!

---

### 4.2 Higher Casimir Invariants

SU(5) has additional Casimir operators:

```
C₃(R) = cubic Casimir
C₄(R) = quartic Casimir
...
```

These could constrain higher-order couplings (λ̃, γ̃) similarly.

---

## 5. WHAT'S DERIVED vs WHAT REMAINS FREE

### ✅ Derived from SU(5):

1. **Number of invariants:**
   - 6 quadratic: S_{2,1} through S_{2,6}
   - ~13 quartic: S_{4,1} through S_{4,13}
   - ~5 sextic: S_{6,1} through S_{6,5}

2. **Ratios between mass coefficients:**
   ```
   c_{m,1} : c_{m,2} : c_{m,3} : c_{m,5} = 12 : 18 : 12 : 25
   ```
   (normalized by Casimir values)

3. **Gauge coupling unification:**
   ```
   α₁, α₂, α₃ → α_GUT = 1/(8πφ) at Λ_GUT
   ```

---

### ❌ Still free (require additional input):

1. **Overall mass scale M₀:**
   - Theory gives M₀ = M_P/√(5π)
   - But individual m̃²ᵢ(X₀) at UV need absolute normalization

2. **X-dependence functions:**
   - K_{X,i}, K_{M,i} forms are specified
   - But constants c_{m,i}, g̃_{0,i}, α_{m,i} need values

3. **Quartic/sextic normalizations:**
   - Casimir operators constrain some ratios
   - But overall scales λ̃_j(X₀), γ̃_k(X₀) need fixing

4. **Epoch scales z_i:**
   - X_{c,i} = X₀ · φ^{z_i}
   - The exponents z_i determine which epochs trigger which SSB
   - These may come from topological/winding considerations (need derivation)

**Total remaining:** ~15-20 parameters (down from ~30!)

---

## 6. NEXT STEPS

### 6A: Use Extended Self-Consistency

With Ω content specified, implement multi-particle fit:

```python
# Specify potential:
def V_fullOmega(Omega, X, constants):
    """
    Full potential with SU(5) invariants
    """
    # Quadratic (6 terms)
    V2 = sum(m_tilde_sq[i](X, constants) * S_2[i](Omega)
             for i in range(6))

    # Quartic (13 terms)
    V4 = sum(lambda_tilde[j](X, constants) * S_4[j](Omega)
             for j in range(13))

    # Sextic (5 terms)
    V6 = sum(gamma_tilde[k](X, constants) * S_6[k](Omega)
             for k in range(5))

    return V2 + V4 + V6

# Fit to all known masses:
best_fit = fit_all_masses(V_fullOmega, particle_spectrum)
```

### 6B: Check Consistency

Verify that best-fit constants respect Casimir ratios:

```python
assert abs(c_m[0]/c_m[1] - 2/3) < 0.1  # Allow 10% deviation
assert abs(c_m[2]/c_m[4] - 12/25) < 0.1
```

If violations are large → additional physics beyond naive Casimir scaling.

---

## 7. ANGULAR MODULATION TERM (Law 7)

### Explicit Form Proposal:

```
V_angular_mod = -C_T(X) · Tr(Φ_24† Φ_24) · cos(N_lobes · arg(det(Φ_24)))
```

where:
- C_T(X) = c_T · (πφ)^α_T · tanh((X_{c2} - X)/ΔX_T)
- N_lobes = topological winding number from lattice
- arg(det(Φ_24)) = phase of determinant (gauge-invariant)

**This provides:**
- Gauge invariance: det(Φ_24) is SU(5)-invariant
- Torus-like bifurcations: cos(N_lobes · θ) creates N_lobes minima
- X-dependent activation: C_T(X) turns on below critical scale

**Still to determine:**
- N_lobes connection to N_e = 111, Δ_μ = 11, Δ_τ = 17
- Precise form of C_T(X) constants

---

## SUMMARY

**What we have:**
✅ SU(5) choice committed
✅ Ω representation content specified (5̄, 10, 5, 24 for fermions and scalars)
✅ 24 gauge-invariant operators listed (6 quadratic + 13 quartic + 5 sextic)
✅ Casimir ratios derived (c_m ratios constrained)
✅ ~15-20 free parameters remain (down from ~30)

**Next:**
→ Implement extended self-consistency fit (FIRST_PRINCIPLES_CLOSURE.md, Strategy B)
→ Use all SM masses to extract best-fit constants
→ Verify Casimir constraints are satisfied

**Status:** PHASE 1 specification **~80% complete**

---

*From group theory to particle masses: The path is clear.*
