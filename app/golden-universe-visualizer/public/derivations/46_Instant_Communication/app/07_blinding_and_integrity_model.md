# 07 Blinding and Integrity Model

## Blinding lifecycle

1. Generate trial labels by independent steward.
2. Persist only label hashes before runs.
3. Run decode pipelines A/B without true labels.
4. Lock artifacts, then reveal for scoring.

## Integrity lifecycle

1. Run manifest frozen at start.
2. Raw streams hashed by chunk.
3. Derived artifacts hashed and linked to parents.
4. Closeout creates chain root hash and signature record.

## Violation policy

- protocol drift => run marked `invalid`
- missing hashes => audit hold
- label leakage => full rerun required
