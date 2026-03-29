# Phase B Gate Scorecard

## Critical Gates

| Gate | Threshold | Observed | Pass |
|---|---|---:|---|
| Blinded balanced accuracy | >= 0.80 | 0.8385 | yes |
| BER | <= 0.01 | 0.00805 | yes |
| False positive rate | <= 0.05 | 0.0325 | yes |
| Decode consistency | >= 0.95 | 0.966667 | yes |
| Freeze integrity | exact hash stability | true | yes |
| Critical confounds unresolved | must be 0 | 0 | yes |

## Decision

Phase B gate status: **pass**

## Notes

- Dual pipelines converged within tolerance.
- Label freeze and reveal integrity checks passed.
