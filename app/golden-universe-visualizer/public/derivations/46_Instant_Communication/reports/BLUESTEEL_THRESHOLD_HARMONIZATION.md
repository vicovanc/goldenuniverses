# Bluesteel Threshold Harmonization

## Purpose

Resolve threshold inconsistencies between benchmark hooks and audit gates.

## Unified Critical Thresholds

- Detectability gate: `active_snr_db > 0.0`
- Blinded fidelity gate: `balanced_accuracy >= 0.80`
- Operating window gate: `viable_window_fraction > 0.05`
- Lock gate: `session_lock_time_s < 20.0`
- Confound gate: `unresolved_critical_confounds = 0`

## Policy

- These thresholds are authoritative for Bluesteel campaign version.
- Benchmark nominal/tolerance values may exist for optimization, but gate pass/fail
  must use unified critical thresholds above.

## Change Control

- Any threshold update requires new `threshold_profile_id` and campaign reset.
