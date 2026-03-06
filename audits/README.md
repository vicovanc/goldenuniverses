# Audits Workspace

This folder is the clean workspace for first-principles quality control and canonical rebuilds.

## Purpose
- Separate canonical derivation work from legacy or provisional derivations.
- Track what is derived, what is assumed, and what is only benchmarked.
- Run core-theory reset work in one place before promoting results.

## Active Program
- `core_theory_reset/` contains the full core reset audit tracks:
  - canonical map
  - gravity canonical chain
  - quark canonical chain
  - open-problem register
  - inconsistency inventory

## Rule
- No file is considered canonical unless it passes explicit consistency gates (units, scheme, no hidden fitting, no circular inputs).
