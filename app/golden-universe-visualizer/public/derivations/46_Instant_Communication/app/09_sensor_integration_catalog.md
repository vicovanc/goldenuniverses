# 09 Sensor Integration Catalog

## Required v1 sensors

- temperature probes
- vibration/accelerometer channel
- EMI/noise floor monitor
- optional humidity/pressure channel

## Adapter contract

- `sensor_id`, `sensor_type`, `units`
- `sampling_hz`, `calibration_id`
- stream health and dropout flags

## Calibration policy

- calibration record required before active runs
- invalid calibration blocks run arming
