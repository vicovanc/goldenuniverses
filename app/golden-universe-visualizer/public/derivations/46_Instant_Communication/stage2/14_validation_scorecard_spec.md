# 14 Validation Scorecard Spec

## Required Metrics

- `SNR_db` (active vs null)
- `BER`
- `balanced_accuracy`
- `t_lock`
- run reproducibility delta across operators

## Gate Logic

- all core metrics must satisfy unified thresholds
- no unresolved critical confounds
- blinded decode consistency required

## Evidence Contracts

- run manifest per session
- trial-level result table
- immutable hash log
- dual-analysis comparison report
