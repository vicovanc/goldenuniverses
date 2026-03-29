# 13 Test Validation Plan

## Test layers

- unit tests: equation transforms and threshold checks
- integration tests: service-to-service contracts
- hardware-in-loop tests: host bridge with simulated and real streams
- reliability tests: drift, packet loss, clock skew, restart behavior

## Validation bundles

- baseline null bundle
- assisted activation bundle
- active blinded bundle
- failure injection bundle

## Exit criteria

- all critical tests green
- gate engine deterministic on replay data
- no unresolved critical integrity defects
