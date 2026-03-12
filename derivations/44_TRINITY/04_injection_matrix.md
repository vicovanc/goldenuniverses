# Trinity Injection Matrix

This matrix specifies where first-order Trinity correction channels should enter each existing pipeline.

## Matrix

| Pipeline | File | Entry points | Primary channel | Notes |
|---|---|---|---|---|
| Inflation / memory ODE | `derivations/04_COSMOLOGY/10_coupled_ode_system.py` | `beta_X`, `lambda_rec_X`, `V_eff`, `F_mem`, `compute_slow_roll` | `delta_phi`, `delta_e` | `delta_phi` on ladder/resonance-like scale terms; `delta_e` on compounding/kernel response |
| Recombination / thermal | `derivations/04_COSMOLOGY/04_thermal_history_and_cmb.py` | `peebles_coefficients`, `peebles_rhs`, implicit update loop | `delta_e`, `delta_pi` | kernel/exp-like rates by `delta_e`; geometry/cross-section-like normalization by `delta_pi` |
| Baryogenesis network | `derivations/06_MEMORY_VS_OTHERS/memory_open_items_models.py` | `BoltzmannConfig`, `solve_memory_coupled_boltzmann` (`rhs`) | `delta_e`, `delta_phi` | source/washout couplings and memory decay channel |
| Dark scattering | `derivations/06_MEMORY_VS_OTHERS/memory_open_items_models.py` and `derivations/04_COSMOLOGY/13_dark_matter_abundance.py` | `gu_dark_scattering_coefficient`, `sigma_over_m_velocity_profile` | `delta_pi`, `delta_phi` | geometric contact estimate (`pi`) and hierarchy/resonance suppressions (`phi`) |
| Identifiability / gates | `derivations/04_COSMOLOGY/14_closure_identifiability.py`, `15_closure_function_gates.py` | `_patched_observables`, Jacobian rank logic, falsification matrix | all | evaluate whether Trinity channels add independent rank or only degeneracy |

## Observable mapping

| Observable | First target module | Trinity channel sensitivity expectation |
|---|---|---|
| `n_s`, `r` | `10_coupled_ode_system.py` | medium `delta_phi`, low `delta_pi`, medium `delta_e` |
| `z_rec` | `04_thermal_history_and_cmb.py` | low-medium `delta_e`, low `delta_pi`, low `delta_phi` |
| `eta_B` | `memory_open_items_models.py` | medium-high `delta_e`, medium `delta_phi`, low `delta_pi` |
| `sigma/m` | `memory_open_items_models.py` + `13_dark_matter_abundance.py` | high `delta_pi` and `delta_phi`, low `delta_e` |

## Minimal implementation order

1. Add channel sensitivity wrappers in Trinity scripts first (no core patching).
2. Run baseline vs one-channel scans.
3. Add pairwise channels and confounder controls.
4. Only after robust signal, consider code-level channel hooks in core cosmology modules.

## Electron-Focused Injection Note (Current Scope)

- Primary active injection in this narrowed pass is the electron residual channel:
  - `deltaC_e = (1-E/K)/N_e` in `derivations/10_RHO_FIELD_COMPUTATION/`.
- Trinity role here is interpretive/supportive:
  - `pi`, `phi`, `e` appear as continuum-limit structural constants that stabilize the meaning of the residual channel,
  - the operational particle effect is the large reduction of electron ppm error versus tree-level.

## Map Synchronization Targets (Required)

Use the same electron terminal anchor statement in:

1. `explanatory/WHAT_IS_THE_ELECTRON.md`
2. `app/golden-universe-visualizer/public/data/theory/WHAT_IS_THE_ELECTRON.md`
3. `explanatory/CONSCIOUSNESS.md`
4. `app/golden-universe-visualizer/public/data/theory/CONSCIOUSNESS.md`
5. `explanatory/README_GU_CONSCIOUSNESS.md`
6. `app/golden-universe-visualizer/public/data/theory/README_GU_CONSCIOUSNESS.md`
7. `theory/GU_MEMORY_REGIME_MAP.md`
8. `app/golden-universe-visualizer/public/data/theory/GU_MEMORY_REGIME_MAP.md`
9. `theory/GU_COSMOLOGICAL_CLOSURE.md`
10. `app/golden-universe-visualizer/public/data/theory/GU_COSMOLOGICAL_CLOSURE.md`

