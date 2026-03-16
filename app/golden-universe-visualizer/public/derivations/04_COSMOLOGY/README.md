# Cosmology Derivations — Golden Universe Theory

**Status**: First-principles pipeline with gate-governed closure statuses (February 2026)

---

## Derivation Chain (Non-Circular)

```
Z_1 = [M_P/(4*sqrt(pi))] * e^(i*2*pi/phi^2)   [Genesis vector]
  --> X_0 = |Re(Z_1)|                            [Initial clock value]
    --> V_X(X) plateau potential                  [Slow-roll driver]
      --> epsilon_V, eta_V                        [Slow-roll parameters]
        --> n_s, r, A_s                           [CMB observables]
          --> V_0, H_inf, N_efolds                [Inflation scale]
            --> Gamma, T_reh                      [Reheating]
              --> T(n), T_CMB                     [Thermal history]

Z_1 phase theta = 2*pi/phi^2                     [Golden angle]
  --> CP violation ~ |sin(theta)|                 [Baryogenesis]
    --> eta_B                                     [Baryon asymmetry]

Z_1 torsion                                      [Primordial twist]
  --> TB/EB CMB polarization                      [Falsifiable prediction]
```

## File Inventory

| File | Description | Status |
|------|-------------|--------|
| `02_slow_roll_inflation.py` | Inflation from X-field: V_X, epsilon, eta, n_s, r, A_s, N_efolds | First-principles |
| `03_reheating_and_plasma.py` | Reheating from L_int: Gamma, T_reh, QGP condition | Bounds (coupling open) |
| `04_thermal_history_and_cmb.py` | T(n) bridge, Saha equation, T_CMB prediction | First-principles |
| `05_baryon_asymmetry.py` | CP violation from theta_genesis, eta_B | Order-of-magnitude |
| `06_cosmological_constant.py` | Str(a_0)=3, vacuum energy assessment | Honest (CC not solved) |
| `07_dark_matter_dark_energy.py` | DM/DE mechanisms from GU | Mechanisms only |
| `08_cmb_polarization_prediction.py` | TB/EB parity-violating prediction | UNIQUE GU PREDICTION |
| `09_cosmology_scorecard.py` | Complete honest summary of all results | Summary |

### Archived
| File | Where | Reason |
|------|-------|--------|
| `01_cosmological_parameters.py` | `archive/deprecated_cosmology/` | Narrative sketch with fitted inputs; replaced by first-principles derivations |

## Key Results

1. **n_s** predicted from plateau slow-roll (compare to Planck 0.9649 +/- 0.0042)
2. **r** predicted < 0.036 (consistent with BICEP/Planck bound)
3. **T_CMB** derived from GU m_e and alpha_EM via Saha equation
4. **eta_B** order-of-magnitude from theta_genesis CP violation
5. **TB/EB nonzero** — unique falsifiable prediction (LiteBIRD)

## Cross-References

| Script | Depends On | Feeds Into |
|--------|-----------|------------|
| `02_slow_roll_inflation.py` | `gu_constants.py`, `20_GRAVITY_FROM_FIRST_PRINCIPLES.py` | Scripts 03-09 |
| `04_thermal_history_and_cmb.py` | `02`, `03`, GU-derived m_e, alpha_EM | `09_cosmology_scorecard.py` |
| `08_cmb_polarization_prediction.py` | `gu_constants.py` (Z_1, theta) | `09_cosmology_scorecard.py` |

## Equation Source

Primary: `theory/GU_Formation_0_EN.md` — Slow-roll cosmology closure derivation
Supporting: `theory/The Golden Universe Formation.md` — Genesis, asymmetries, CMB polarization prediction

## Open First-Principles Closure Targets (Where To Explore Next)

The following items remain open for full first-principles cosmological closure and should be explored in these files:

1. **Canonical `g_{ΩX}(X)` (interaction profile)**
   - Primary implementation target: `10_coupled_ode_system.py`
   - Cross-check and reduced variants: `11_memory_corrected_inflation.py`
   - Reheating consistency constraints: `03_reheating_and_plasma.py`

2. **Canonical `beta(X)` (memory decay/rate function)**
   - Memory dynamics insertion point: `11_memory_corrected_inflation.py`
   - Coupled dynamics validation: `10_coupled_ode_system.py`
   - Thermal-history impact check: `04_thermal_history_and_cmb.py`

3. **Canonical `lambda_rec(X)` (or constrained `lambda_rec/beta`)**
   - Memory-force implementation: `11_memory_corrected_inflation.py`
   - Inflation observable propagation (`n_s`, `r`, `A_s`): `10_coupled_ode_system.py`
   - Downstream consistency in baryogenesis/thermal sectors: `05_baryon_asymmetry.py`, `04_thermal_history_and_cmb.py`

4. **Uniquely fixed canonical `V_X(X)` from `L_total`**
   - Candidate-family derivation module: `../43_VX_FROM_LTOTAL/01_vx_from_ltotal.py`
   - Runtime integration into inflation outputs: `10_coupled_ode_system.py`
   - Gate-coupled closure decision logic: `15_closure_function_gates.py`

## Memory Open-Item Implementations (Completed Artifacts)

1. **Dark scattering coefficient replacement**
   - `../06_MEMORY_VS_OTHERS/01_dark_scattering_first_principles.py`
   - Shared model: `../06_MEMORY_VS_OTHERS/memory_open_items_models.py`

2. **Full memory-coupled Boltzmann network**
   - `../06_MEMORY_VS_OTHERS/02_memory_boltzmann_network.py`
   - Wired to production baryogenesis: `05_baryon_asymmetry.py`

3. **Recombination extension (He + matter decoupling + memory)**
   - `../42_RECOMBINATION_HELIUM_DECOUPLING/01_recombination_extension.py`
   - Wired to production thermal history: `04_thermal_history_and_cmb.py`

4. **`V_X` from `L_total` candidate/gate path**
   - `../43_VX_FROM_LTOTAL/01_vx_from_ltotal.py`
   - Integrated with `10_coupled_ode_system.py` + `15_closure_function_gates.py`

### Guidance
- Keep all closure attempts explicitly labeled as `derived`, `constrained`, or `chosen`.
- Propagate closure choices into `09_cosmology_scorecard.py` so observational impact is transparent.
- Mirror final closure decisions in `theory/GU_COSMOLOGICAL_CLOSURE.md` and `theory/theory-laws.md`.

### Current Gate State (from machine diagnostics)

- `beta(X)`: `provisional`
- `lambda_rec(X)`: `provisional_ratio_closed`
- `g_{ΩX}(X)`: `constrained`
- `V_X(X)`: `chosen_non_unique`
- Full-ODE identifiability: rank-deficient (`2/5`), so DERIVED promotion is blocked.
- Function-level falsification matrix is tracked in `15_closure_function_gates.py` output.

Machine outputs:
- `derivations/04_COSMOLOGY/closure_identifiability_report.json`
- `derivations/04_COSMOLOGY/closure_function_gates_report.json`
