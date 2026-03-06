# Gravity Canonical Chain

**Updated**: February 2026 (post first-principles rebuild)

## Canonical Derivation Order

```
1. Omega-substrate field content (SM + memory modes)
2. Seeley-DeWitt heat kernel  -->  c_R = 1.25 (V2 Sec 8.3)
3. Induced gravity:  M_P^2 = 4 pi c_R M_0^2
4. G_N = hbar c / M_P^2
5. Graviton coupling:  kappa = sqrt(8 pi G_N)
6. Formation vector Z_1 = [M_P/(4 sqrt(pi))] exp(i 2pi/phi^2)  [consequence]
7. Compare G_derived with G_exp  <--  ONLY place G_exp appears
```

## Non-Negotiable Rules

1. G_exp must NOT appear upstream of step 7.
2. No graviton winding numbers (gravity is spacetime, not a field on spacetime).
3. No "exact/perfect/Nobel Prize" claims unless mathematically proven.
4. Explicit units at every conversion step.
5. Metadata (winding, epoch, resonance) from `utils/gu_constants.py`, not hardcoded.
6. Suppression/FRG/prediction scripts are labeled as speculative.

## Primary Files (canonical chain)

| Step | File | Status |
|------|------|--------|
| 1-5 | `04_seeley_dewitt_calculation.py` | REWRITTEN (Feb 2026) |
| 6 | `01_FORMATION_VECTOR_FOUNDATION.py` | REWRITTEN (context only) |
| 7 | `05_VALIDATION_AND_CONSISTENCY.py` | REWRITTEN (honest scoreboard) |

## Cross-Check (not canonical)

| File | Role | Status |
|------|------|--------|
| `03_NEWTON_CONSTANT_EXACT.py` | Motivated ansatz e^phi/(pi*phi) | Relabeled as cross-check |

## Deprecated (archived)

| File | Reason |
|------|--------|
| `05_dimensional_analysis_complete.py` | Tautological |
| `PHASE_1_TENSOR_TOPOLOGY_FRAMEWORK.md` | q_graviton approach abandoned |

## Acceptance Gates

1. `04_seeley_dewitt_calculation.py` runs with no G_exp upstream of comparison.
2. Validation scoreboard shows 6/9 PASS, 3 OPEN (consistent with current state).
3. All downstream scripts (07-10) labeled as speculative/exploratory.
4. README, GRAVITY_FROM_FIRST_PRINCIPLES, NOBEL docs reflect honest status.
5. No emoji or overclaims in any gravity script output.

## Open Problems

1. c_R = 1.25: derive from explicit Omega QFT mode counting
2. M_0: determine independently of M_P_exp
3. pi/phi factor: derive from torus KK reduction
4. SM wrong-sign: quantify the bosonic memory modes
5. r < 0.036: need mechanism (r ~ 1 ruled out)
