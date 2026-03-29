# Phase B Blinded Trial Register

## Trial Design (Preregistered)

- Campaign: `BLUESTEEL_L4_V1`
- Phase: `B`
- Nodes: physically separated TX/RX
- Blinding: Team C tokenized schedule, no labels to ops/analysis teams
- Decode pipelines: Analysis A and Analysis B (independent)

## Trial Blocks

| Block ID | Run Count | Payload Bits | Hidden Null Fraction | Status |
|---|---:|---:|---:|---|
| B1 | 20 | 512 | 0.25 | completed |
| B2 | 20 | 512 | 0.25 | completed |
| B3 | 20 | 1024 | 0.25 | completed |

Total runs: 60

## Registration Hashes

- schedule_hash: `sha256:bphase_schedule_v1_9f7a...`
- protocol_hash: `sha256:bphase_protocol_v1_12cc...`
- threshold_profile_hash: `sha256:thresholds_v1_6ab1...`

## Notes

- All decode outputs were frozen before label reveal.
- Operator actions logged with immutable run IDs.
