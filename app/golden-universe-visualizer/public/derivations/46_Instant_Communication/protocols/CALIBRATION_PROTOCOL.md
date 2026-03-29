# Calibration Protocol

## Goal

Establish reproducible baseline and active-channel calibration before any
messaging run.

## Pre-Run Conditions

- instrumentation self-test pass
- shielding and dummy-channel checks complete
- clock consistency check pass

## Procedure

1. Baseline acquisition
   - channel-off configuration (`grad(theta) = 0`)
   - measure noise floor and leakage signatures
2. Assisted acquisition
   - weak structured gradients, no payload
   - estimate preliminary gain and lock response
3. Active acquisition
   - activation setpoint sweep
   - estimate optimal `A_mod`, threshold, and lock gains
4. Stability hold
   - verify lock stability for `T_hold`
5. Save calibration profile
   - commit profile with run ID, operator ID, environment hash

## Output Metrics

- baseline noise floor
- leakage residual score
- active gain estimate
- lock convergence time
- calibrated threshold and modulation depth

## Abort Rules

- unresolved leakage above threshold
- lock instability during hold
- cross-clock drift above allowable bound
