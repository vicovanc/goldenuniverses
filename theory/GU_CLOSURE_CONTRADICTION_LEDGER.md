# GU Closure Contradiction Ledger

Purpose: track and resolve status-claim conflicts for cosmology closure functions and gravity boundary conditions.

## Canonical Status Authority

The authoritative status source is:

1. `theory/GU_COSMOLOGICAL_CLOSURE.md` (Closure Status Freeze section)
2. `theory/theory-laws.md` (Cosmology Closure Freeze block)
3. Machine reports:
   - `derivations/04_COSMOLOGY/closure_identifiability_report.json`
   - `derivations/04_COSMOLOGY/closure_function_gates_report.json`

Current authority state:

- `beta(X)`: provisional
- `lambda_rec(X)`: provisional at absolute level (ratio-level closed)
- `g_{OmegaX}(X)`: constrained
- `V_X(X)`: chosen non-unique

## Resolved Contradictions

1. `derivations/04_COSMOLOGY/10_coupled_ode_system.py`
   - Old wording: "with all functions CLOSED"
   - Resolved to: closure API with provisional runtime mode and gate-governed promotion.

2. `derivations/04_COSMOLOGY/09_cosmology_scorecard.py`
   - Old wording: "Previously undetermined functions -- NOW CLOSED"
   - Resolved to: "closure states after gate evaluation" using explicit gate outputs.

3. `theory/GU_COSMOLOGICAL_CLOSURE.md`
   - Old wording in early section implied Closure-1 fully closed with no caveats.
   - Resolved to explicitly note this is canonical working closure pending uniqueness promotion gates.

## Open Contradictions (Pending Full Sync)

1. Legacy gravity files still carry older `c_R = 1.25` assumptions and memory-mode counting narratives:
   - `derivations/39_GRAVITY/GRAVITY_FROM_FIRST_PRINCIPLES.md`
   - `derivations/39_GRAVITY/04_seeley_dewitt_calculation.py`
   - `derivations/39_GRAVITY/05_VALIDATION_AND_CONSISTENCY.py`
   - `derivations/39_GRAVITY/11_memory_mode_counting.py`
   - `derivations/39_GRAVITY/12_g_prim_field_content.py`

2. Gravity-cosmology boundary must stay explicit:
   - `G_N` claim remains from `m_e -> M_P -> G_N`.
   - `c_R` governs `M_0`/UV normalization and supertrace context, not the direct `G_N` prediction chain.

## Promotion Rule (Non-negotiable)

No function can be labeled `DERIVED` unless:

1. full-ODE identifiability diagnostics pass,
2. per-function falsification gates pass,
3. no residual hidden free knob remains in production mode.
