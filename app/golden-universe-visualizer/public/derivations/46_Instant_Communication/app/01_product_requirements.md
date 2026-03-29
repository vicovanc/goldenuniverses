# 01 Product Requirements

## Mission
Deliver a lab-ready app that captures, interprets, and audits GU communication experiments end-to-end.

## Primary user roles

- Operator: executes runbooks and sessions
- Physicist: reviews equation-level interpretation and claims
- Auditor: verifies blinded integrity and chain-of-custody

## Functional requirements

1. Control and monitor null/assisted/active sessions.
2. Ingest USB/Serial + sensor telemetry in real time.
3. Compute GU metrics (`SNR_db`, `BER`, `balanced_accuracy`, `session_lock_time`).
4. Apply unified threshold profile with all-gates-must-pass policy.
5. Enforce blinding, protocol lock, and immutable artifacts.
6. Store all data in Postgres with provenance.

## Non-functional requirements

- deterministic timing and loss monitoring
- restart-safe ingestion pipeline
- explicit proven-vs-pending claim boundaries
- operator-first UI with minimal ambiguity
