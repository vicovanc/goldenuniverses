# Threshold Conflict Resolution

## Conflict

Legacy benchmark-hook nominal/tolerance logic could produce a different pass/fail
label than critical-gate detectability and promotion logic.

## Resolution

Adopt `UNIFIED_THRESHOLD_PROFILE.json` as the only authoritative gate profile.

## Enforcement

1. Dashboard and promotion decisions must consume unified profile values.
2. Benchmark hooks may remain as optimization diagnostics only.
3. Any future threshold change requires new profile ID and gate reset.

## Result

Threshold-policy contradiction is closed for current campaign.
