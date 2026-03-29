# Audit Traceability Index

## Claim-to-Evidence Mapping

| Claim | Source Equation / Rule | Primary Artifact | Verification Artifact |
|---|---|---|---|
| Geometric/topological initialization is defined | corrected resonance + winding mapping | `01_entanglement_geometry_axioms_report.json` | `THEORETICAL_CLOSURE.md` |
| Memory channel dynamics are implemented | `dR/dt + beta*R = rho^4` | `02_memory_channel_equations_report.json` | `THEORETICAL_CLOSURE.md` |
| Channel activation has off/assisted/active modes | `J_theta` activation logic | `03_topological_activation_conditions_report.json` | `DEVICE_ARCHITECTURE.md` |
| Signal control and encoding are stable in simulation | control loop and symbol decoding | `04_signal_encoding_and_control_knobs_report.json` | `sim/03_control_locking_sim_report.json` |
| Causality/guardrail checks pass | guardrail policy set | `05_causality_and_guardrail_checks_report.json` | `reports/AUDIT_PROMOTION_DECISION.md` |
| Detectability is positive in active regime | `active_snr_db > 0` | `06_benchmark_scenarios_report.json` | `reports/AUDIT_METRIC_RECOMPUTE_REPORT.json` |
| Falsification and identifiability pass current threshold | balanced accuracy and matrix | `07_identifiability_and_falsification_report.json` | `reports/AUDIT_METRIC_RECOMPUTE_REPORT.json` |
| Viability is constrained-window not broad | phase map classification | `08_phase_diagram_and_operating_regions_report.json` | `09_final_synthesis_report.md` |
| Aggregated program gate summary is available | dashboard gates | `reports/metrics_dashboard_report.json` | `reports/AUDIT_METRIC_RECOMPUTE_REPORT.json` |

## Provenance Integrity Notes

- All major claims map to script-generated JSON outputs.
- Remaining gap is empirical run provenance for Phase B/C blinded and cross-lab stages.
