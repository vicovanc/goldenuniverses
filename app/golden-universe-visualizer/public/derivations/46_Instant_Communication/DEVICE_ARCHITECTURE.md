# Device Architecture (TX/RX Point-to-Point)

## System Blocks

1. Entanglement geometry core
   - computes working topological sector `(N, p, q, nu, L_Omega)`.
2. Topological activation module
   - drives activation setpoint for `grad(theta)` and memory-depth floor.
3. Transmitter node (TX)
   - modulation engine, activation driver, lock controller.
4. Receiver node (RX)
   - phase-state sensing, matched filtering, decoder, confidence estimator.
5. Link manager
   - handshake, alignment, session lock, integrity enforcement.
6. Claim gate engine
   - computes pass/fail metrics and promotion status.

## TX Stack

- `tx_modulator`: PSK/spread/hybrid mode selector
- `tx_activation_driver`: controls phase-gradient actuation profile
- `tx_control`: adaptive loop on lock and gain targets
- `tx_telemetry`: emits pilot symbols and diagnostics

## RX Stack

- `rx_phase_sensor`: acquires phase-memory observable
- `rx_preproc`: denoise and baseline subtraction
- `rx_matched_filter`: code- or symbol-matched detection
- `rx_decoder`: outputs symbols, confidence, and residual error
- `rx_monitor`: tracks BER, lock drift, and anomaly flags

## Synchronization and Control Loops

- coarse sync:
  - pilot-correlation alignment
- fine sync:
  - lock-error feedback to TX and RX control planes
- gain adaptation:
  - online estimate `g_hat` updates modulation depth and threshold
- fail-safe:
  - if lock or integrity fails, drop to conservative fallback mode

## Protocol Layers

1. Physical signaling layer
   - phase-memory symbol generation and detection
2. Framing layer
   - packet boundaries, pilot blocks, sequence counters
3. Error-control layer
   - forward error correction and integrity check
4. Session layer
   - handshake, lock negotiation, keepalive, teardown
5. Validation layer
   - blinded run tags, anti-artifact metadata, operator masking

## Session Handshake

1. `HELLO`: topology profile and protocol version exchange
2. `ALIGN`: pilot-only lock alignment
3. `CAL`: gain/noise calibration in current environment
4. `ARM`: blinded schedule activation
5. `RUN`: payload transmission window
6. `VERIFY`: independent decode and hash comparison
7. `CLOSE`: archive metrics and artifact ledger references

## Required Runtime Telemetry

- lock error trace
- gain estimate trace
- SNR trace
- BER trace
- power/energy proxy trace
- blinded run ID and payload hash
