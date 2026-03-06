# Core Inconsistency Inventory

## Purpose
Track all core derivation issues that block canonical status.

## Severity Scale
- **S0**: hard blocker (invalidates derivation claim)
- **S1**: major inconsistency
- **S2**: moderate issue
- **S3**: minor clarity/documentation issue

## Inventory Template
- **ID**:
- **Severity**:
- **File**:
- **Issue type**: (units / scheme / circularity / hidden fit / metadata drift / claim strength)
- **Description**:
- **Why it matters**:
- **Required fix**:
- **Verification check**:
- **Status**: open / fixed / verified

## Initial Known Items
- **S0**: hardcoded particle metadata drift in gravity scripts versus canonical winding/epoch sources.
- **S0**: predictive paths using benchmark values upstream of predictions in quark scripts.
- **S1**: mixed renormalization scheme comparisons without explicit conversion notes.

## Confirmed Findings (Core Reset Pass 1)

- **ID**: GRAV-S0-001
- **Severity**: S0
- **File**: `derivations/39_GRAVITY/04_seeley_dewitt_calculation.py`
- **Issue type**: metadata drift
- **Description**: Particle metadata (`winding`, `epoch`, `resonant`) is hardcoded inline and conflicts with canonical winding/epoch derivation sources.
- **Why it matters**: The induced-gravity spectrum input can silently diverge from theory truth layer, invalidating reproducibility.
- **Required fix**: Replace inline particle table metadata with canonical loader from shared constants/solver outputs.
- **Verification check**: Script prints metadata source hash/version and all entries match canonical source.
- **Status**: fixed

- **ID**: GRAV-S0-002
- **Severity**: S0
- **File**: `derivations/39_GRAVITY/04_seeley_dewitt_calculation.py`
- **Issue type**: claim strength
- **Description**: Strong “exact/complete unification” language is present while inputs include estimated or non-canonical values.
- **Why it matters**: Overstates derivation authority and obscures unresolved assumptions.
- **Required fix**: Downgrade claim language to evidence-based status until canonical input and closure checks pass.
- **Verification check**: No “exact/complete/perfect” wording unless accompanied by formal proof and consistency gates.
- **Status**: fixed

- **ID**: GRAV-S1-003
- **Severity**: S1
- **File**: `derivations/39_GRAVITY/04_seeley_dewitt_calculation.py`
- **Issue type**: units / circularity
- **Description**: Mixed SI and natural-unit formulas were connected via a solved conversion factor `C` rather than a fully derived dimensional bridge.
- **Why it matters**: Allowed hidden calibration and weakened first-principles interpretation.
- **Required fix**: Introduce explicit dimensional derivation pipeline for every conversion step.
- **Verification check**: Unit-check function passes for each symbolic expression before numeric evaluation.
- **Status**: fixed (Feb 2026 rewrite removed the C factor entirely; G now computed from M_P^2 = 4 pi c_R M_0^2 and G = hbar c / M_P^2 with explicit SI units throughout)

- **ID**: GRAV-S0-004
- **Severity**: S0
- **File**: `derivations/39_GRAVITY/05_dimensional_analysis_complete.py`
- **Issue type**: circularity / tautology
- **Description**: Defined alpha = G_exp * M_P^2 / (hbar c) then "derived" G = alpha * hbar c / M_P^2 = G_exp. Pure tautology.
- **Why it matters**: Presented a circular definition as a derivation.
- **Required fix**: Remove file from derivation chain.
- **Verification check**: File moved to archive/deprecated_gravity/.
- **Status**: fixed (archived Feb 2026)

- **ID**: GRAV-S0-005
- **Severity**: S0
- **File**: `derivations/39_GRAVITY/10_experimental_predictions.py`
- **Issue type**: ruled-out prediction
- **Description**: Predicted tensor-to-scalar ratio r ~ alpha_gravity^2 ~ 1, which is strongly ruled out by Planck/BICEP2 (r < 0.036 at 95% CL).
- **Why it matters**: Falsified prediction undermines theoretical credibility.
- **Required fix**: Remove r ~ 1 prediction; note Planck/BICEP2 constraint.
- **Verification check**: Script no longer prints r ~ 1.
- **Status**: fixed (Feb 2026)

- **ID**: GRAV-S1-006
- **Severity**: S1
- **File**: Multiple gravity files (07, 08, 09, 10, docs)
- **Issue type**: claim strength
- **Description**: "Nobel Prize Achievement", "Complete Quantum Gravity", "UV Completion Proven" and similar overclaims throughout.
- **Why it matters**: Misrepresents speculative/exploratory work as established results.
- **Required fix**: Downgrade all claims to match actual derivation status.
- **Verification check**: No "Nobel Prize", "exactly/perfectly/proven" in speculative files.
- **Status**: fixed (Feb 2026)

### Pass 2 Notes (Feb 2026 First-Principles Rebuild)
- `04_seeley_dewitt_calculation.py` completely rewritten: non-circular induced gravity chain, G_exp only in comparison step.
- `05_dimensional_analysis_complete.py` archived (tautological).
- `PHASE_1_TENSOR_TOPOLOGY_FRAMEWORK.md` archived (q_graviton approach abandoned).
- `03_NEWTON_CONSTANT_EXACT.py` relabeled as "motivated ansatz cross-check".
- `01`, `02` rewritten to reflect Z_1 as consequence (not derivation) of G.
- `05_VALIDATION_AND_CONSISTENCY.py` rewritten with honest 6/9 scoreboard.
- Scripts 07-10 fixed: overclaims removed, FP values labeled as from literature, r~1 removed.
- All three markdown docs (README, GRAVITY_FROM_FIRST_PRINCIPLES, NOBEL) rewritten.
- All GRAV issues now fixed. Remaining gravity open problems: c_R derivation, M_0 closure, pi/phi derivation.

- **ID**: QRK-S0-001
- **Severity**: S0
- **File**: `derivations/31_QUARK_MASSES/25_corrected_quark_derivations.py`
- **Issue type**: hidden fit / circularity
- **Description**: “Predicted” masses are seeded by benchmark-scale base values (`m_d_base`, `m_u_base`, `m_c_base`) and then lightly corrected.
- **Why it matters**: Predictive path is contaminated by target-like inputs.
- **Required fix**: Enforce separate predictive and validation paths; no benchmark values allowed upstream.
- **Verification check**: Static audit reports zero benchmark seeds in predictive call graph.
- **Status**: open

- **ID**: QRK-S0-002
- **Severity**: S0
- **File**: `derivations/31_QUARK_MASSES/25_corrected_quark_derivations.py`
- **Issue type**: hidden fit
- **Description**: CKM block uses ad hoc empirical factors (e.g., divisors like `22`, `10`) and benchmark masses in CKM expressions.
- **Why it matters**: CKM outputs are not first-principles predictions.
- **Required fix**: Rebuild CKM strictly from cleaned mass-sector outputs and explicit theoretical mixing structure.
- **Verification check**: No unexplained numeric multipliers/divisors in predictive CKM module.
- **Status**: open

- **ID**: QRK-S1-003
- **Severity**: S1
- **File**: `derivations/31_QUARK_MASSES/25_corrected_quark_derivations.py`
- **Issue type**: metadata drift
- **Description**: Local `corrected_windings` table redefines canonical particle metadata in-script (including sector assignment), risking divergence from canonical source.
- **Why it matters**: Branch logic can change per file and break theory consistency.
- **Required fix**: Consume shared canonical metadata only.
- **Verification check**: One authoritative metadata source imported across all quark scripts.
- **Status**: open

- **ID**: QRK-S0-004
- **Severity**: S0
- **File**: `derivations/31_QUARK_MASSES/10_corrected_quark_derivation.py`
- **Issue type**: circularity
- **Description**: Up-quark path uses empirical ratio from benchmark masses as a fallback derivation path.
- **Why it matters**: Circular dependence blocks first-principles status.
- **Required fix**: Remove empirical fallback from predictive path; keep only in validation notebook/report if needed.
- **Verification check**: Predictive mode does not reference benchmark mass ratio.
- **Status**: open

- **ID**: QRK-S1-005
- **Severity**: S1
- **File**: `derivations/31_QUARK_MASSES/10_corrected_quark_derivation.py`
- **Issue type**: scheme
- **Description**: Script compares values across mixed renormalization contexts without strict conversion protocol.
- **Why it matters**: Numeric agreement claims become ambiguous.
- **Required fix**: Declare target scheme per quantity and enforce conversion at compare step.
- **Verification check**: Every reported comparison line includes explicit scheme tag.
- **Status**: open
