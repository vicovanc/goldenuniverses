# Blinded Message Protocol

## Goal

Prevent operator and analysis bias while testing point-to-point messaging.

## Roles

- Team A: transmitter operations (no truth labels)
- Team B: receiver operations (no truth labels)
- Team C: randomization/label authority (no live hardware access)
- Team D: independent auditor

## Protocol

1. Team C pre-registers schedule and payload map.
2. Team C issues run tokens only (no payload labels to A/B).
3. Team A executes TX using tokenized schedule.
4. Team B performs RX decoding and stores outputs with timestamps.
5. Team D performs integrity checks and verifies protocol compliance.
6. Team C reveals labels only after all outputs are frozen.
7. Final scoring occurs on locked data.

## Required Artifacts

- randomized schedule file hash
- payload truth table hash
- raw RX decode logs
- operator action log
- instrumentation trace bundle

## Primary Scoring

- balanced accuracy
- BER
- false-positive and false-negative rates
- reproducibility across repeated blinded blocks
