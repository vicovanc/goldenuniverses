# Bluesteel Traceability Master Index

## Chain of Evidence

1. Equation and channel closure
   - `THEORETICAL_CLOSURE.md`
2. Architecture and protocol closure
   - `DEVICE_ARCHITECTURE.md`
   - `protocols/*`
3. Simulation and baseline metrics
   - `sim/*_report.json`
   - `reports/metrics_dashboard_report.json`
4. Audit closure artifacts
   - `reports/AUDIT_*`
5. Phase B blinded closure
   - `reports/PHASEB_*`
6. Phase C cross-lab closure
   - `reports/PHASEC_*`
7. Phase D operational qualification
   - `reports/PHASED_*`
8. Red-team closure
   - `reports/REDTEAM_*`

## Top-Line Claim Mapping

| Claim | Evidence Bundle |
|---|---|
| Blinded separated-node reproducibility | `PHASEB_*` |
| Cross-lab reproducibility | `PHASEC_*` |
| Operational L4 messaging profile | `PHASED_*` |
| Adversarial false-pass resistance | `REDTEAM_*` |
| Governance and immutability compliance | `BLUESTEEL_GOVERNANCE_CHARTER.md`, `BLUESTEEL_VERSION_LOCK.md`, `BLUESTEEL_RUN_MANIFEST_SCHEMA.json` |
