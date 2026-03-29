# 06 Benchmark and Gate Engine

## Threshold source

Load profile from:

- `../reports/UNIFIED_THRESHOLD_PROFILE.json`

## Critical metrics

- `active_snr_db_min`
- `balanced_accuracy_min`
- `ber_max`
- `false_positive_rate_max`
- `session_lock_time_s_max`
- `viable_window_fraction_min`
- `unresolved_critical_confounds_max`

## Gate policy

- all critical thresholds must pass
- unresolved critical confounds force `hold`
- integrity breaches force `invalid_due_to_integrity`

## Outputs

- machine-readable decision packet
- human-readable gate rationale
- promotion eligibility status
