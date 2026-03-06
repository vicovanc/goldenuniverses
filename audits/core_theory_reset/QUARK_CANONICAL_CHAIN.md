# Quark Canonical Chain

## Required Dual Constraint
Every accepted quark derivation must satisfy both:
- SU(2) doublet/generation consistency: `(u,d)`, `(c,s)`, `(t,b)`
- Resonance classification consistency from canonical winding/resonance computation

If either fails, mark as unresolved physics (not corrected by fitting).

## Canonical Pipeline
1. Epoch + admissibility setup
2. Resonance classification (`round(N/phi^2)`)
3. Branch logic (resonant vs anti-resonant)
4. Yukawa/RG treatment at declared scheme and scale
5. Prediction output
6. Benchmark comparison only at final validation stage

## Hard Rules
- No PDG-seeded mass values in predictive path.
- No ad hoc CKM multipliers/divisors.
- Explicit MS-bar vs pole handling.
- Single source for particle metadata.
