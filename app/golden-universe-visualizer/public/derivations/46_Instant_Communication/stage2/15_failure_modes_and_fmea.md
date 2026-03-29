# 15 Failure Modes and FMEA

## Critical Failure Modes

1. Loss of lock during active block
2. Environmental drift causing false separation
3. Timing mismatch between TX/RX nodes
4. Decoder bias or leakage from label metadata

## FMEA Table

| Failure mode | Severity | Likelihood | Detectability | Mitigation |
|---|---:|---:|---:|---|
| Lock loss | High | Medium | High | adaptive relock and quarantine trial |
| Thermal drift artifact | High | Medium | Medium | tighter thermal guard + null interleaves |
| Clock drift | High | Low | High | reference clock + drift monitor |
| Label leakage | Critical | Low | Medium | strict blind and independent steward |

## Stop Conditions

- immediate run halt on critical integrity breach
- mark run as invalid pending audit resolution
