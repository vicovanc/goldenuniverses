# 10 Interface Control Document (ICD)

## Electrical/Signal Interfaces

- `IF-TX-001`: TX control input (setpoint, waveform ID, amplitude)
- `IF-RX-001`: RX data output (symbol, confidence, timestamp)
- `IF-SYNC-001`: timing sync channel (reference epoch markers)
- `IF-ENV-001`: environmental telemetry stream

## Data Fields

- run_id
- trial_id
- blinded_label_hash
- tx_profile_id
- rx_decode
- confidence
- timestamp_utc

## Interface Limits

- max update jitter: <= 2 ms
- clock drift between nodes: <= 1 ppm over run interval
