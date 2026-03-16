# 46_BIOCHEMICAL_REALISM

Phase 2 implements full biochemical realism with Nobel-grade validation gates.

## Module Map

- `01_species_reaction_registry.py`
- `02_reaction_kinetics_engine.py`
- `03_membrane_transport_engine.py`
- `04_metabolic_redox_engine.py`
- `05_gene_regulatory_engine.py`
- `06_cell_state_integrator.py`
- `07_population_selection_dynamics.py`
- `08_multicellular_transition.py`
- `09_proto_neural_tissue.py`
- `10_neural_circuit_emergence.py`
- `11_bio_identifiability.py`
- `12_bio_falsification_gates.py`
- `13_bio_promotion_rules.py`
- `14_bio_scorecard.py`
- `15_benchmark_membrane_dynamics.py`
- `16_benchmark_metabolism.py`
- `17_benchmark_gene_response.py`
- `18_benchmark_tissue_excitation.py`
- `19_benchmark_neural_metrics.py`
- `20_phase1_phase2_gap_audit.py`
- `21_claim_relabeling.py`
- `22_phase2_final_report.md`

## Shared Contracts

- All reports use `model`, `config`, `summary`, `assumptions`, `units`, `parameter_provenance`, `diagnostics`.
- Falsification-aware modules add `falsification_matrix` and `gate_status`.
- Deterministic seeds are mandatory for stochastic modules.

## Directories

- `data_manifest/`: dataset source/license/hash declarations.
- `benchmark_protocols/`: pass/fail rules for benchmark scripts.
- `reference_targets/`: canonical target ranges used in gate checks.

## Execution Order

1. Run `01` -> `10` to generate mechanistic + evolution outputs.
2. Run `11` -> `14` to compute identifiability, falsification, promotion, scorecard.
3. Run `15` -> `19` for benchmark checks.
4. Run `20`, `21`, then inspect `22_phase2_final_report.md`.
