# 03_PARTICLE_MASSES (Orchestrator Layer)

This folder is kept active as an integration and reporting layer.

It does not replace canonical mass closure work in `31_QUARK_MASSES`; it
combines selected local outputs with canonical upstream scripts and makes
derivation status explicit.

## Folder Contract

- Role: orchestrator and honest status reporter for particle-mass outputs
- Theory alignment: `0 free parameters + 1 boundary condition (m_e)` for mass closure wording
- Provenance rule: every reported number must show source script/folder
- Honesty rule: no hidden fits labeled as first-principles derivations

## Status Tags

- `canonical_integration`: entrypoint used to unify and report results
- `leptons_derived_local`: local lepton calculations used as legacy local source
- `quarks_not_derived_local`: local quark outputs where C/Yukawa are not first-principles
- `hypothesis`: exploratory physical mechanism under test
- `phenomenological`: ansatz or inverse-fit workflow
- `reference_legacy`: useful reference, not canonical closure
- `bug_known_fixed`: known bug was present and has been patched

## Script Index

| Script | Status | Purpose |
|---|---|---|
| `03_run_particle_masses_orchestrator.py` | `canonical_integration` | Main runner: local leptons + canonical quark script summary |
| `01_all_particle_masses.py` | `reference_legacy` | Legacy all-in-one mass report with explicit quark warning |
| `02_quark_masses_qcd.py` | `bug_known_fixed` + `quarks_not_derived_local` | QCD-style quark mass comparison (exploratory, non-canonical closure) |
| `03_correct_unified_masses.py` | `reference_legacy` | Legacy unified script with corrected wording for bootstrap vs transported C |
| `04_heavy_quark_fix.py` | `hypothesis` | Heavy-quark correction hypotheses (phase transition/memory ideas) |
| `05_correct_phase17_masses.py` | `reference_legacy` | Phase-17-based mass-ratio exploration with explicit limits |
| `06_complete_phase17_quarks.py` | `hypothesis` | Resonance/phase-epoch exploration (non-canonical) |
| `07_quark_derivation_systematic.py` | `phenomenological` | Inverse-search for quark winding/C patterns (fit-like) |
| `08_quarks_qcd_regime.py` | `hypothesis` | Regime-separation narrative and exploratory formulas |
| `09_yukawa_golden_hierarchy.py` | `phenomenological` | Yukawa hierarchy ansatz exploration |

## Canonical Upstream Sources

- Quark mass closure and corrected resonance workflow: `derivations/31_QUARK_MASSES/25_corrected_quark_derivations.py`
- Coupling-side context: `derivations/34_GAUGE_BOSONS/`
- Composite coupling context: `derivations/40_COMPOSITE_COUPLINGS/`
- Pattern-k constraints and anti-pattern warnings: `derivations/33_PATTERN_K/`

## How To Run

From project root:

```bash
python derivations/03_PARTICLE_MASSES/03_run_particle_masses_orchestrator.py
```

This prints:
- local lepton summary (from `01_all_particle_masses.py`),
- canonical quark script availability and output tail,
- explicit provenance and status labels.
