# Pion Physics Derivation -- Status Report

## Executive Summary
- 5 scripts implementing the pion physics pipeline
- Key results: chiral condensate (-243 MeV)^3 (NJL, vs lattice -250), f_pi ~ 109 MeV (NJL, vs PDG 92.2, 18% off), m_pi ~ 90 MeV from GMOR with NJL inputs (vs PDG 140, 35% off with PDG quark masses)
- g_piNN from Goldberger-Treiman: 10.94 (GU) vs 12.97 (PDG)
- Chiral Lagrangian predictions: pion scattering lengths computed

## Scripts
- 01_chiral_condensate_from_frg.py -- 5 methods for condensate, NJL best at 243 MeV
- 02_fpi_from_gu.py -- 5 routes to f_pi, NJL/Pagels-Stokar best at 109 MeV
- 03_gmor_proper.py -- systematic GMOR scan, sensitivity analysis
- 04_pion_nucleon_coupling.py -- g_piNN from GT, g_A from quark model
- 05_chiral_lagrangian.py -- LO chi-PT predictions (m_pi, m_K, m_eta, scattering)

## Key Results Table
| Observable | GU (NJL) | PDG | Error |
|---|---|---|---|
| condensate^(1/3) | 243 MeV | ~250 MeV | -2.9% |
| f_pi | 109 MeV | 92.2 MeV | +18.6% |
| m_pi (GMOR, PDG quarks) | 90 MeV | 139.6 MeV | -35% |
| g_piNN | 10.94 | 12.97 | -15.6% |

## What Is Derived
- Lambda_QCD (zero free parameters)
- Chiral condensate from NJL (partially derived via Lambda_QCD)
- f_pi from Pagels-Stokar (partially derived)

## What Needs More Work
- Quark C_q factors (Phase A) to get correct m_u, m_d
- Full FRG chiral flow for exact f_pi
- Higher-order ChPT (NLO) corrections

## Date
February 2026
