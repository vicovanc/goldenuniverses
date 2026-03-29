# 12 Calibration and Commissioning Runbook

## Pre-Run

- verify hardware integrity
- verify environmental envelope
- load protocol version and lock config hash

## Calibration Steps

1. Null baseline capture (no active phase drive)
2. Assisted-mode sweep to estimate `g_hat`
3. Active-mode lock tuning (`K_p`, `K_i`, `K_d`)
4. Symbol separation check and BER pre-test

## Commissioning Gate

Pass if:
- lock success rate meets threshold
- baseline drift below threshold
- BER pre-test at or below threshold
