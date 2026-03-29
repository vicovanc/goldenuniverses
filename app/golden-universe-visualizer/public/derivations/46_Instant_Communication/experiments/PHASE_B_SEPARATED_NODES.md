# Phase B - Separated Nodes (Blinded)

## Objective

Validate point-to-point messaging performance with physically separated nodes
under blinded randomized schedules.

## Setup

- TX and RX in separate rooms/labs
- independent operators
- Team C controlled randomization tokens

## Trial Design

- pre-registered run count and payload budget
- randomized token schedule with hidden null windows
- fixed decoding pipeline before label reveal

## Metrics

- balanced accuracy
- BER and packet success rate
- blind null-window false-positive rate
- run-to-run repeatability

## Pass Gate

- balanced accuracy >= target threshold
- BER below threshold on holdout trials
- no protocol violations or leakage confounds
