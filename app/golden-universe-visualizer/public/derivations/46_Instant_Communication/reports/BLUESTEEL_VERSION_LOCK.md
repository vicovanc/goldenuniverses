# Bluesteel Version Lock

## Freeze Scope

The following artifacts are version-locked for L4 evaluation:

- `THEORETICAL_CLOSURE.md`
- `DEVICE_ARCHITECTURE.md`
- `protocols/CALIBRATION_PROTOCOL.md`
- `protocols/BLINDED_MESSAGE_PROTOCOL.md`
- `instrumentation/INSTRUMENTATION_STACK.md`
- `experiments/PHASE_A_BENCH.md`
- `experiments/PHASE_B_SEPARATED_NODES.md`
- `experiments/PHASE_C_CROSS_LAB.md`
- `reports/CLAIM_PROMOTION_SCORECARD_TEMPLATE.md`
- `reports/ARTIFACT_LEDGER_TEMPLATE.md`

## Lock Rules

- Any content change requires:
  1. change request ID,
  2. impact analysis,
  3. re-preregistration,
  4. explicit gate reset notice.

## Hash-Lock Procedure

1. Compute file hashes pre-run.
2. Store in run manifest.
3. Verify identical hashes before scoring.
4. If mismatch found, mark run invalid.

## Threshold Immutability

- Threshold values are locked by manifest.
- Threshold harmonization updates are only allowed in new campaign versions.
