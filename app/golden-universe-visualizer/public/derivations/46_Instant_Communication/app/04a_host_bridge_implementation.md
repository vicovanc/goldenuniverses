# 04a Host Bridge Implementation

## Process model

- macOS host process (outside Docker)
- discovers serial ports and approved sensor endpoints
- normalizes frames and forwards to API gateway

## Plugin interface

- `probe() -> capability descriptor`
- `open(config) -> session handle`
- `read() -> frame batch`
- `health() -> status`
- `close()`

## Frame envelope

- `stream_id`, `run_id`, `sample_idx`
- `payload` (raw values)
- `ts_device_ns`, `ts_host_ns`, `ts_utc`
- `quality` (`jitter_ns`, `drop_count`, `clock_drift_ppm`)

## Bridge safeguards

- strict allowlist for device IDs
- per-stream rate limits
- retry with circuit breaker
- local spool fallback if API unavailable
