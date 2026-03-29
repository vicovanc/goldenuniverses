# 13a Benchmark Matrix

## Required benchmark suites

1. Null stability suite
2. Assisted activation suite
3. Active blinded messaging suite
4. Fault-injection reliability suite
5. Replay determinism suite

## Core pass criteria

- `SNR_db >= active_snr_db_min`
- `BER <= ber_max`
- `balanced_accuracy >= balanced_accuracy_min`
- `session_lock_time <= session_lock_time_s_max`
- `false_positive_rate <= false_positive_rate_max`
- `viable_window_fraction >= viable_window_fraction_min`
- unresolved critical confounds = `0`

## Reliability gates

- packet loss tolerance validated
- restart recovery validated
- clock drift compensation validated
