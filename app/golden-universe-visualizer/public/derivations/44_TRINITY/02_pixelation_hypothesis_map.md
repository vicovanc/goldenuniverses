# Pixelation Hypothesis Map

## Scope

This map separates physical discreteness candidates from numerical artifacts for the Trinity program (`pi`, `phi`, `e`) and ties each candidate to concrete GU observables.

## Hypotheses

- `H0` artifact-dominant: observed discreteness signatures mostly come from rounding, finite grids, solver choices, or proxy truncations.
- `H1` physical-dominant: discreteness is a real structural layer (topology/resonance/quantization) and yields stable predictive corrections.
- `H2` mixed: physical discreteness exists, but currently measured observables are weakly sensitive and/or degenerate with existing closure dials.

## Classification Table

| Candidate | Class | Why likely physical/artifact | First impacted observables | Current confidence |
|---|---|---|---|---|
| Integer winding numbers `(p,q)` | Physical | Topological sector labels are integer-valued by construction, not numerical rounding products | mass residuals, resonance class splits | High |
| Resonance integer gate `k_res` | Mixed | Integer rule is physical, but boundary behavior depends on rounding prescription | particle class assignment, correction on/off switching | Medium |
| Torus finite-size modular defect `(1-E/K)` | Physical | Explicit finite-geometry effect with analytic structure | electron residual correction scale | High |
| Gauge-topological quantization (`kappa_a in Z`) | Physical | Quantization from large-gauge invariance class | phase channel constraints, allowed sectors | Medium |
| Epoch integerization (`n_today`, node labels) | Mixed | Discrete epoch language is structural, but operational mapping may include convention choices | timeline labels, threshold indexing | Medium |
| Lattice circle count (`pi` estimation) | Artifact-to-physical bridge | Pixelation error vanishes with refinement; convergence itself is diagnostic | `pi` convergence diagnostics | High (as diagnostic) |
| Finite denominator window in irrational tests | Artifact-to-physical bridge | `q_max` window controls finite-sample score, but extremal ordering can be robust | `phi` bad-approximability ranking | Medium |
| ODE step-size / implicit solver settings | Artifact | Numerical discretization of continuous equations | `z_rec`, stiffness-sensitive quantities | High |
| Reduced model proxies in open-item modules | Artifact | Proxy structures can absorb/tune effects not unique to physics | `eta_B`, `sigma/m` details | High |

## Where pixelation would first appear if physical

1. In small residual correction terms (not leading-order terms), especially finite-size/topological residuals.
2. Near resonance-boundary sectors (classification flips at integer thresholds).
3. In quantized parity/channel selection rules (forbidden/allowed sectors), not in smooth broadband shifts.

## Where pixelation would first appear if artifact

1. Strong sensitivity to `round/floor`, step size, or finite-window cutoffs.
2. Large shifts that vanish or move when numerical resolution changes.
3. Apparent improvements that can be reabsorbed by existing closure dials (`g0`, `beta_scale`, `lambda_ratio`, potential family choice).

## Measurable discriminator rules

- **Resolution stability rule:** if effect is physical, its sign/magnitude should remain stable under refinement.
- **Dial-independence rule:** if effect is physical, it should not disappear under modest retuning of non-trinity dials.
- **Boundary localization rule:** threshold-concentrated corrections are more credible than uniform offsets.
- **Rank contribution rule:** genuine channels should add independent information to observable Jacobians.

## Electron Terminal Anchor Map

- **Terminal formula:** `deltaC_e = (1-E/K)/N_e`.
- **Interpretation class:** physical finite-size torus residual (not solver artifact).
- **Before correction:** electron tree-level error is about `+0.36%` (`~+3583 ppm` vs CODATA).
- **After correction:** electron reaches ppm-level agreement (about `-17.5 ppm` with rounded print value).
- **Map implication:** this is a residual-layer correction with high local impact (electron precision), not evidence of universal pixelation dominance.

Map-sync endpoints for this anchor:

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

