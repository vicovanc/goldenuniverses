# Phase D Failure Recovery Scorecard

## Fault Scenarios

| Scenario | Injected Events | Mean Recovery Time (s) | Integrity Loss | Pass |
|---|---:|---:|---:|---|
| transient lock drop | 40 | 2.3 | 0 | yes |
| decoder pipeline restart | 12 | 3.1 | 0 | yes |
| clock drift correction | 18 | 1.7 | 0 | yes |
| noise burst resilience | 25 | 2.9 | 0 | yes |

## Recovery Gates

- max allowed mean recovery time: 5.0 s
- integrity loss tolerance: 0 lost validated packets

## Decision

Phase D failure/recovery gate status: **pass**
