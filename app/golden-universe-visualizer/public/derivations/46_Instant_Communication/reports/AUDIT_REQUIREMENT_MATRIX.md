# Audit Requirement Matrix

## Coverage Summary

Audit date: current workspace run  
Scope: `derivations/46_Instant_Communication`

## Requirement-to-Artifact Mapping

| Requirement | Artifact(s) | Coverage | Notes |
|---|---|---|---|
| Theory closure equations | `THEORETICAL_CLOSURE.md` | complete | Includes device-state equations and observables |
| TX/RX architecture | `DEVICE_ARCHITECTURE.md` | complete | Includes stack, control loops, protocol layers |
| Materials candidate matrix | `materials/CANDIDATE_MATRIX.md` | complete | Three platform classes and scoring rubric |
| Core stage pipeline 01-08 | `01_*.py` ... `08_*.py` + reports | complete | All scripts and paired reports present |
| Simulation suite | `sim/01_*.py`, `sim/02_*.py`, `sim/03_*.py` + reports | complete | Channel, decoherence, lock simulations |
| Calibration protocol | `protocols/CALIBRATION_PROTOCOL.md` | complete | Abort rules included |
| Blinded protocol | `protocols/BLINDED_MESSAGE_PROTOCOL.md` | complete | Multi-team blinding model defined |
| Instrumentation controls | `instrumentation/INSTRUMENTATION_STACK.md` | complete | Timing, leakage, integrity monitors |
| Experiment stages | `experiments/PHASE_A_BENCH.md`, `PHASE_B_SEPARATED_NODES.md`, `PHASE_C_CROSS_LAB.md` | complete | Staged progression documented |
| Claim promotion template | `reports/CLAIM_PROMOTION_SCORECARD_TEMPLATE.md` | complete | L0-L4 promotion structure |
| Artifact ledger template | `reports/ARTIFACT_LEDGER_TEMPLATE.md` | complete | Confound classification present |
| Dashboard aggregation | `reports/metrics_dashboard.py` + `metrics_dashboard_report.json` | complete | Aggregated gate outputs available |

## Missing Evidence / Gaps

1. No completed Phase B/C raw run datasets yet (protocols exist, evidence not yet generated).
2. No populated artifact ledger from real blinded runs (template only).
3. No finalized BER/packet-success from physical experiments (simulation-only status).
4. No cross-lab operator signoff artifacts yet (Phase C pending execution).

## Coverage Verdict

- Structural coverage: **100% of planned artifact types present**
- Empirical evidence completeness: **partial** (simulation-complete, lab-incomplete)
