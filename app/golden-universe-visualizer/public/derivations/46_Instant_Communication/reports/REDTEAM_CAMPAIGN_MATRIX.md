# Red-Team Campaign Matrix

## Attack Campaigns

| Campaign ID | Attack Type | Target Layer | Expected Failure Mode | Outcome |
|---|---|---|---|---|
| RT-01 | leakage spoof injection | physical/channel | false detectability | blocked |
| RT-02 | clock skew manipulation | timing/instrumentation | fake latency residual | blocked |
| RT-03 | operator workflow subversion | protocol/human | label leakage | blocked |
| RT-04 | decode overfit attempt | analysis/model | inflated accuracy | blocked |
| RT-05 | data poison/replay | data provenance | false reproducibility | blocked |

## Summary

No tested red-team path produced a passing false-success condition under
Bluesteel gates.
