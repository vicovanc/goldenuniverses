# 04 Device I/O Spec

## Host bridge model

The host bridge runs on macOS and exposes a local API to container services.

## Supported v1 channels

- USB serial instrument streams
- DAQ-style sampling streams over serial adapters
- sensor telemetry (temperature, vibration, EMI)

## Timestamp contract

- `ts_device_ns`: monotonic device timestamp when available
- `ts_host_ns`: host capture monotonic timestamp
- `ts_utc`: wall clock timestamp for audit/reporting

## Quality contract

- packet sequence continuity
- dropped frame count
- jitter statistics
- clock drift estimate

## Required payload fields

- `stream_id`, `run_id`, `sample_idx`
- raw value payload
- quality envelope
