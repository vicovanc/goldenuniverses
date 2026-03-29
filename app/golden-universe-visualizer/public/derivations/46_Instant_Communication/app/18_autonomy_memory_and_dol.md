# 18 Autonomy Memory and DOL

## DOL role

`dol.md` is the local domain operating ledger that summarizes:

- GU physics rules and canonical equations
- current experiment objective
- active constraints and hard gates
- last validated recommendations and rejected paths

## Memory hierarchy

- short-term run memory: per-session state transitions and rationale
- medium-term lab memory: recurring artifacts and fixes
- long-term GU memory: equation provenance and protocol evolution

## Automatic improvement loop

1. observe run outcomes
2. score decision quality against benchmarks
3. store deltas in memory tables
4. update next-step recommendations with explicit confidence

All improvements remain auditable and reversible.
