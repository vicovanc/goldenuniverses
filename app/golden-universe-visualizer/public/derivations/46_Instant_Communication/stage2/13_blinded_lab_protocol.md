# 13 Blinded Lab Protocol

## Blinding Design

- randomize TX symbol schedule by independent steward
- freeze label mapping before runs
- perform dual decode pipelines without label access

## Trial Blocks

- block A: null control
- block B: assisted regime
- block C: active regime

## Anti-Bias Rules

- no operator access to true labels during run
- decode hashes stored prior to reveal
- reveal only after immutable data lock
