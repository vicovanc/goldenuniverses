# 10 Run Orchestration Workflow

## Run states

`draft -> preregistered -> armed -> calibrating -> active -> sealing -> closed`

## Workflow

1. Create run and bind protocol version.
2. Execute setup and calibration checklist gates.
3. Start blinded trial blocks (null/assisted/active).
4. Compute real-time quality and lock status.
5. Seal evidence and run benchmark evaluator.
6. Publish closeout report with decision status.

## Hard stops

- sensor out-of-envelope
- clock drift above max bound
- integrity event critical severity
