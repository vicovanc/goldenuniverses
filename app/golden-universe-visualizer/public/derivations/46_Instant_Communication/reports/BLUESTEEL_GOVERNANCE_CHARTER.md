# Bluesteel Governance Charter

## Purpose

Define immutable governance rules for L4 claim qualification under maximum rigor.

## Roles and Separation of Duties

- Operations Team: executes runs, cannot access truth labels.
- Label Authority Team: controls randomized truth mapping, cannot operate hardware.
- Analysis Team A: primary decoding/metrics pipeline.
- Analysis Team B: independent decoding/metrics pipeline.
- Audit Team: verifies protocol compliance and gate decisions.
- Red Team: adversarial testing independent of all above.

## Governance Rules

1. No metric threshold edits after preregistration freeze.
2. No run inclusion/exclusion after label reveal without audit signoff.
3. No claim promotion with unresolved critical confounds.
4. Any failed critical gate triggers automatic rollback to last passing level.
5. All run artifacts require hash-linked manifests before scoring.

## Decision Authority

- Gate decisions require majority signoff by Audit Team plus one independent verifier.
- L4 public claim requires unanimous final signoff by Audit + Independent Auditor.

## Escalation Policy

- Critical protocol breach -> run invalidation + incident report.
- Repeated breach -> freeze program until governance remediation is accepted.
