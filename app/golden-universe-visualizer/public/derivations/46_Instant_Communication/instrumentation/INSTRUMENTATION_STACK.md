# Instrumentation Stack

## Timing and Clocking

- primary high-stability reference clock
- independent secondary clock for cross-check
- per-node timestamp capture with monotonic hardware counters
- periodic drift calibration and drift alerts

## Detection Chain

- front-end low-noise analog stage
- anti-alias filtering
- high-resolution ADC and synchronized capture
- digital preprocessing and matched-filter block

## Shielding and Leakage Controls

- Faraday enclosure and controlled cable routing
- dummy-channel probes co-recorded with active channels
- baseline leakage sweep before each run block
- null-run schedule inserted in blinded trials

## Integrity Monitors

- clock disagreement monitor
- environmental monitor (temperature, vibration, EMI proxy)
- power rail anomaly detector
- continuous data-integrity hashing

## Required Output Bundle per Run

- raw acquisition files
- synchronized timestamps
- preprocessing output
- decode output + confidence
- leakage/null-channel traces
- instrumentation health and drift report
