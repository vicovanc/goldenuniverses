# Core Theory Canonical Map

## Scope
Core sectors only: laws, constants, leptons, quarks, bosons, gravity.

## Classification Rules
- **Canonical**: first-principles, reproducible, consistent conventions, no hidden fitting.
- **Provisional**: physically plausible but incomplete derivation chain.
- **Deprecated Path**: fit-driven, circular, inconsistent units/schemes, or contradictory metadata.

## Canonical Sources (Truth Layer)
- `theory/theory-laws.md`
- `derivations/utils/gu_constants.py`
- `derivations/30_WINDING_NUMBERS/WINDING_NUMBER_THEORY.md`
- `derivations/30_WINDING_NUMBERS/01_winding_number_solver.py`
- `derivations/30_WINDING_NUMBERS/02_corrected_winding_solver.py`

## File Status Inventory (To Fill)

### Gravity
- Status: **Provisional**
- Blocking issues:
  - mixed-unit bridge via solved conversion factor instead of explicit dimensional closure
  - explicit dimensional closure proof still missing in induced bridge
- Promotion criteria:
  - canonical metadata loader only
  - explicit unit-closure checks
  - induced-primary chain retained and evidence-calibrated wording

### Quarks
- Status: **Provisional**
- Blocking issues:
  - predictive paths seeded with benchmark-like mass values
  - ad hoc CKM factors in predictive formulas
  - local in-script metadata tables diverging from canonical source
  - mixed-scheme comparisons without strict conversion tagging
- Promotion criteria:
  - strict predictive vs validation split
  - one shared canonical metadata source
  - dual acceptance constraint: SU(2) doublet consistency + resonance consistency
  - scheme-tagged reporting for every comparison

### Bosons
- Status: **Provisional**
- Blocking issues:
  - dependency on upstream quark/gravity canonicalization still incomplete
- Promotion criteria:
  - upstream canonical inputs locked
  - no benchmark seeding in predictive couplings/masses

### Leptons
- Status: **Canonical (baseline reference), with integration checks pending**
- Blocking issues:
  - cross-sector metadata propagation consistency not yet fully enforced
- Promotion criteria:
  - shared metadata import path used by all dependent sectors

### Constants / Conventions
- Status: **Provisional (governance layer being enforced)**
- Blocking issues:
  - constant/scheme conventions are duplicated across scripts
- Promotion criteria:
  - single conventions module + lint-style integrity checks for forbidden constructs
