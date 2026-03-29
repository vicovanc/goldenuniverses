# Audit Confound Register

## Sources Reviewed

- `instrumentation/INSTRUMENTATION_STACK.md`
- `protocols/CALIBRATION_PROTOCOL.md`
- `protocols/BLINDED_MESSAGE_PROTOCOL.md`
- `reports/ARTIFACT_LEDGER_TEMPLATE.md`
- `experiments/PHASE_A_BENCH.md`
- `experiments/PHASE_B_SEPARATED_NODES.md`
- `experiments/PHASE_C_CROSS_LAB.md`

## Confound Classification

| ID | Confound Category | Evidence Present | Residual Risk | Severity | Status |
|---|---|---|---|---|---|
| C1 | Electromagnetic leakage | yes (protocol + instrumentation controls) | no measured leakage logs yet | high | open |
| C2 | Timing drift / clock mismatch | yes (dual clocks specified) | no run-time drift dataset | high | open |
| C3 | Operator bias | yes (blinded protocol roles) | no completed blinded run audit | high | open |
| C4 | Decoder overfit | partial (holdout concept in reports) | no independent holdout dataset from experiments | medium | open |
| C5 | Calibration drift | yes (calibration protocol + abort rules) | no longitudinal calibration history | medium | open |
| C6 | Environmental interference | yes (monitoring specified) | no environment trace bundle yet | medium | open |

## Anti-Artifact Strength

- Policy and controls are **well specified** at protocol level.
- Empirical anti-artifact proof is **not yet complete** because no populated
  artifact ledger from real blinded runs is present.

## Critical Unresolved Risks

1. No completed leakage/null evidence bundle from Phase B/C.
2. No frozen blind-run operator logs with revealed labels.
3. No completed artifact ledger showing zero unresolved critical issues.

## Confound Audit Status

`not cleared_for_promotion_without_new_evidence`
