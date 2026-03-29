# Claim Promotion Scorecard Template

## Promotion Levels

- `L0`: simulated viability
- `L1`: bench detectability
- `L2`: blinded point-to-point reproducibility
- `L3`: cross-lab reproducibility
- `L4`: operational messaging profile

## Required Gates

| Gate | Metric | Threshold | Status |
|---|---|---:|---|
| Detectability | active SNR | > 0 dB | pending |
| Decode quality | BER | <= target | pending |
| Blinded fidelity | balanced accuracy | >= target | pending |
| Stability | session lock time | <= target | pending |
| Reproducibility | inter-site variance | <= target | pending |
| Artifact integrity | unresolved confounds | 0 | pending |

## Decision Rule

- promote only if all gates pass at current level
- downgrade if any critical gate regresses
- keep explicit limitations even at highest achieved level
