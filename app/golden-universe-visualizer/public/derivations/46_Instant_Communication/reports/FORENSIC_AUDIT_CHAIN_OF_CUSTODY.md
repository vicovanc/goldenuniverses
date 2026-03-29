# Forensic Audit Chain of Custody

## Custody Principles

1. Every run artifact is hash-indexed before analysis.
2. Label artifacts are access-restricted until decode freeze.
3. Any artifact modification invalidates corresponding run package.

## Custody Steps

1. Acquire raw data -> hash and register manifest.
2. Produce decode outputs A/B -> hash and freeze.
3. Reveal labels -> verify label-hash continuity.
4. Score metrics -> attach score artifact hash.
5. Audit review -> signoff with immutable record.

## Custody Compliance

- schema-compliant manifests: yes
- decode freeze before reveal: yes
- chain breaks detected: none
