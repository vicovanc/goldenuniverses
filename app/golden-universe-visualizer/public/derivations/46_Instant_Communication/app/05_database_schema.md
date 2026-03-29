# 05 Database Schema

## Primary entities

- `runs`: immutable run manifests and protocol lock data
- `trials`: trial schedule and decode outcomes
- `telemetry_frames`: environment and quality channels
- `equation_states`: computed physics state snapshots
- `benchmark_results`: metric results by run/trial
- `gate_decisions`: pass/hold/invalid decisions with reasons
- `blinding_records`: label hash and reveal lifecycle
- `artifact_ledger`: evidence hash chain and provenance
- `anomaly_log`: integrity and hardware anomalies

## Design rules

- every row is traceable to `run_id`
- foreign keys enforce chain consistency
- write-once policy for immutable artifacts
- append-only revisions for corrected analyses
