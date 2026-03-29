# Master Traceability Index

## End-to-End Mapping

| Layer | Artifact |
|---|---|
| Canonical equations | `THEORETICAL_CLOSURE.md` |
| Device architecture | `DEVICE_ARCHITECTURE.md` |
| Stage outputs | `01_*_report.json` .. `08_*_report.json` |
| Simulation outputs | `sim/*_report.json` |
| Audit layer | `AUDIT_*` |
| Bluesteel closure | `BLUESTEEL_*`, `PHASEB_*`, `PHASEC_*`, `PHASED_*`, `REDTEAM_*` |
| Final claim control | `PUBLIC_CLAIM_FINAL.md`, `FINAL_EVIDENCE_DRIVEN_GATEBOOK.md` |

## Claim Trace Contract

Each top-line claim must include:
1. source equation reference,
2. generating script/report reference,
3. run-manifest index entry,
4. gate decision reference.

All current top-line claims satisfy this contract under the current campaign files.
