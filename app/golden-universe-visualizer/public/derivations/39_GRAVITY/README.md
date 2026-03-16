# Gravity Derivations - Golden Universe Theory

**Status**: Non-circular derivation achieved (G_N from m_e, 47 ppm)

---

## Canonical Derivation Chain (Non-Circular)

```
m_e (measured, sole dimensionful input)
  --> C_e from Route-A elliptic formula (topology + Lame one-loop)
    --> M_P = m_e * phi^111 / (2*pi * C_e * eta_QED)   [Law 12 inverted]
      --> G_N = hbar*c / M_P^2                          [47 ppm error]
        --> M_0 = M_P / sqrt(4*pi*c_R)                  [requires G_prim]
```

### What is derived
- **M_P** from m_e alone, with 23 ppm accuracy (Lame-corrected first-principles)
- **G_N** from M_P, with 47 ppm accuracy — ZERO fitted parameters
- G_N is **independent of c_R** and the G_prim choice
- c_R determines only M_0 (the UV cutoff scale)
- Cosmology closure gates (`beta`, `lambda_rec`, `g_{OmegaX}`, `V_X`) are managed in `derivations/04_COSMOLOGY/` and do not alter the direct `m_e -> M_P -> G_N` chain.

### What is assumed / open
- G_prim = SU(5) is the working assumption (from Formation document and theory-laws.md)
- SUSY at some scale is required (for Str(a_0) ~ 0, CC suppression)
- GU memory modes (X, theta, moduli) are **classical backgrounds**, not propagating quantum DOF — correctly excluded from the heat kernel
- The 0.26% residual in c_R (1.247 vs 1.25) may come from threshold corrections or non-minimal couplings

---

## File Inventory

### Core derivation
| File | Description | Status |
|------|-------------|--------|
| `20_GRAVITY_FROM_FIRST_PRINCIPLES.py` | **Non-circular G_N derivation**: m_e -> M_P -> G_N (47 ppm) | First-principles; ZERO fitted params |
| `04_seeley_dewitt_calculation.py` | Induced gravity: c_R -> M_P/M_0 ratio | c_R = 1.25 assumed; determines M_0 only |
| `11_memory_mode_counting.py` | **Memory-mode DOF census**: SM + GU field content -> c_R | ~108 extra bosonic DOF needed; V2 "+40" inconsistent |
| `12_g_prim_field_content.py` | **G_prim field content census**: SUSY + dark + GUT chiral multiplets | Dual constraint: N_B ~ N_F ~ 189; SUSY essential |
| `05_VALIDATION_AND_CONSISTENCY.py` | Consistency checks and scoreboard | 6/9 checks pass, 3 open |

### Supporting / context
| File | Description | Status |
|------|-------------|--------|
| `01_FORMATION_VECTOR_FOUNDATION.py` | Z_1 as consequence of induced G (not derivation) | Context |
| `02_SPACETIME_GEOMETRY_DERIVATION.py` | Torus -> 4D geometry (qualitative) | Context |
| `03_NEWTON_CONSTANT_EXACT.py` | Motivated ansatz alpha = e^phi/(pi*phi) | Cross-check (~0.8% by construction) |
| `04_TENSOR_WINDING_ANALYSIS.py` | When tensor fields can have winding numbers | Clarification |

### Downstream / exploratory
| File | Description | Status |
|------|-------------|--------|
| `07_frg_uv_completion.py` | FRG / asymptotic safety exploration | Speculative; FP values from literature |
| `08_spacetime_emergence.py` | Spacetime emergence from Omega substrate | Qualitative / conceptual |
| `09_cosmological_constant_resolution.py` | CC suppression mechanisms | Order-of-magnitude |
| `10_experimental_predictions.py` | Experimental signatures | Speculative; inflation limits now tracked in `derivations/04_COSMOLOGY/09_cosmology_scorecard.py` |

### Graviton subfolder
| File | Description | Status |
|------|-------------|--------|
| `graviton/` | Standard GR graviton properties (spin-2, massless, etc.) | Established physics |

### Archived (deprecated)
| File | Where | Reason |
|------|-------|--------|
| `05_dimensional_analysis_complete.py` | `archive/deprecated_gravity/` | Tautological (G_exp -> alpha -> G_exp) |
| `PHASE_1_TENSOR_TOPOLOGY_FRAMEWORK.md` | `archive/deprecated_gravity/` | Superseded; q_graviton approach abandoned |

---

## Key Results

1. **G_N predicted from m_e** with 47 ppm precision, ZERO fitted parameters (`20_GRAVITY_FROM_FIRST_PRINCIPLES.py`)
2. **M_P/m_e ratio** = phi^111 / (2pi * C_e * eta_QED) — all quantities derived from first principles
3. **G_N is independent of c_R** — the field content (G_prim choice) affects only M_0, not gravity itself
4. **c_R = 1.247 derived from SU(5) + SUSY** — only 0.26% from V2's c_R = 1.25, with Str(a_0) = 3 (CC satisfied)
5. **GU memory modes are classical backgrounds**, not propagating quantum DOF — excluding them resolves both the c_R value and the CC constraint simultaneously

## Key Open Problems

1. **c_R residual**: SU(5)+SUSY gives c_R = 1.247 vs target 1.25 — gap is 0.5 DOF (possibly from threshold/non-minimal coupling effects)
2. **Inflation-sector status (moved to cosmology)**: Derived regime is canonical **slow-roll inflation with finite end** (`epsilon -> 1` termination in the coupled ODE). Linear V_X is ruled out (r = 0.057 > 0.036), while Plateau/Axion remain viable; alpha-attractor sub-band resolves Plateau n_s tension. Eternal-inflation diagnostic is now implemented in `04_COSMOLOGY/10_coupled_ode_system.py` using `delta X_quantum / delta X_classical`; for tested potentials (Plateau/Axion/Linear), no eternal region appears (`max ~ 5e-5 << 1`).
3. **M_0 = 3.08 × 10^18 GeV** from the SU(5)+SUSY scenario — awaits independent confirmation

---

## Cross-References

| Script | Depends On | Feeds Into |
|--------|-----------|------------|
| `20_GRAVITY_FROM_FIRST_PRINCIPLES.py` | `theory-laws.md` (Law 12, Law 33), `gu_constants.py` | **Final G_N prediction** |
| `11_memory_mode_counting.py` | V2 Sections 8.3, 3.5 | `12_g_prim_field_content.py` |
| `12_g_prim_field_content.py` | `11_memory_mode_counting.py`, V2 Sections 3.5, 9.2, 10.5 | `20_GRAVITY_FROM_FIRST_PRINCIPLES.py` (c_R values) |
| `04_seeley_dewitt_calculation.py` | `gu_constants.py` | Historical; superseded by script 20 for G_N |

## Documentation
- `GRAVITY_FROM_FIRST_PRINCIPLES.md` - Theoretical exposition (reflects current honest status)
- `NOBEL_GRAVITY_DERIVATION_COMPLETE.md` - Summary of what has been achieved and what remains
