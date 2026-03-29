# 09 Device Architecture Spec

## TX Node

- phase actuation driver
- memory-bias conditioning stage
- control processor for lock and symbol scheduling

## RX Node

- phase-sensitive detection front-end
- lock-state estimator
- symbol decoder with confidence output

## Shared Services

- timing reference unit
- immutable run logger
- environment monitor (temperature, vibration, EMI)

## Timing Contract

- epoch window `T_sym`
- guard interval `T_guard`
- lock refresh interval `T_lock_refresh`
