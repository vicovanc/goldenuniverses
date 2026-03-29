# Audit Promotion Decision

## Inputs

- `reports/AUDIT_METRIC_RECOMPUTE_REPORT.json`
- `reports/AUDIT_CONFOUND_REGISTER.md`
- `reports/AUDIT_REPRODUCIBILITY_SCORECARD.md`
- `reports/metrics_dashboard_report.json`

## Gate Evaluation

1. Metric gates: pass (with policy-threshold harmonization warning)
2. Confound clearance gate: fail (critical empirical evidence pending)
3. Reproducibility gate: partial (L2/L3 pending)
4. Traceability gate: pending final index

## Decision

- **No escalation beyond L1 at this time**
- Allowed status: `CONSTRAINED` / `PROVISIONAL` for practical messaging claims
- Disallowed status: robust reproducible point-to-point claim until blinded and cross-lab gates pass

## Required Actions Before Promotion

1. Complete Phase B blinded run package with frozen labels and independent decode.
2. Complete Phase C cross-lab run package with inter-site variance report.
3. Populate artifact ledger with zero unresolved critical confounds.
4. Harmonize benchmark-hook thresholds with audit thresholds.
