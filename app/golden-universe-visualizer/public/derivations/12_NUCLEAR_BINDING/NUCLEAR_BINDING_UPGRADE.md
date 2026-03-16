# Nuclear Binding Upgrade -- Status Report

## Executive Summary
- 3 new scripts (07, 08, 09) upgrading the nuclear binding with GU-derived pion parameters
- OPEP implemented with full central + tensor structure
- Complete NN potential: V_OPEP + V_short(bag) + V_memory(Wilson loop)
- Light nuclei variational calculations attempted (d, He-3, He-4)
- Current limitation: simple variational ansatz doesn't bind nuclei because the GU short-range repulsion is too strong for S-wave-only calculation; tensor force and full coupled-channel treatment needed

## New Scripts
- 07_opep_from_derived_pion.py -- OPEP with GU m_pi=90 MeV, g_piNN=10.94, f_pi=109
- 08_nuclear_potential_complete.py -- full V_NN = OPEP + short + memory
- 09_light_nuclei_ab_initio.py -- variational calculations for d, He-3, He-4

## GU-Derived Potential Parameters
| Parameter | Value | Source |
|---|---|---|
| Lambda_QCD | 179 MeV | GU (zero free params) |
| R_bag | 0.4675 fm | Omega-torus bag model |
| C_mem | 1.283 | Y-junction color geometry |
| sigma | 2*pi*Lambda_QCD^2 | GU string tension |
| V_0 (short) | 1390 MeV | (4*pi/phi)*Lambda_QCD |

## Current Status
- OPEP: Fully implemented with correct tensor structure
- Short-range: Gaussian repulsion from bag overlap
- Memory: Linear confinement + exponential screening
- Deuteron: Does not bind with simple variational (needs tensor force)
- He-3, He-4: Same issue

## Next Steps
1. Implement tensor force in deuteron calculation (3S1-3D1 coupling)
2. Solve coupled-channel Schrodinger equation
3. Soften short-range repulsion (finite-size nucleon form factors)
4. Add three-body forces for A >= 3
5. Tune memory kernel with proper spin-isospin structure

## Date
February 2026
