# Hadron Pipeline — Golden Universe

## Overview

This folder implements the QCD hadron mass calculation within the Golden Universe (GU) framework. It takes gauge couplings from the GU epoch ladder and computes hadron masses as QCD bound states.

**Honesty policy**: every number is labeled as `[GU-DERIVED]`, `[PDG-INPUT]`, `[ESTIMATED]`, or `[PLACEHOLDER]`.

---

## Architecture

The hadron calculation has three stages, reflecting the physical transition from perturbative QCD to confinement:

```
Stage 1: Perturbative Running        Stage 2: Phase Transition       Stage 3: Bound States
───────────────────────────          ──────────────────────────      ────────────────────────
  α_GUT (calibrated from α_EM)       Confinement at α_s ~ 1          Cornell potential
       ↓                              Chiral breaking:                  V(r) = -C/r + σr
  One-loop β functions                   ⟨ψ̄ψ⟩ ~ −Λ³_QCD                   ↓
  with EFT thresholds:                Constituent masses:              Schrödinger → E_bind
    SU(5) → SM → SU(2)frozen          M_dyn = Λ³/(3f²_π)               ↓
    → SU(3)frozen                      m_q = M_dyn + m_current        Hadron masses:
       ↓                                  ↓                            M = Σm_q + E_bind
  α₁,α₂,α₃ at Λ_QCD                  σ ~ Λ²_QCD                       + ΔE_hyp + E_mem
```

---

## Files

| File | What it does | Status |
|------|-------------|--------|
| `01_qcd_hadron_calculation.py` | 3-stage pipeline: gauge running → phase transition → hadron masses (Cornell potential) | Working |
| `02_bound_state_equations.py` | Schrödinger + Cornell solver for mesons and quark-diquark for baryons | Working |
| `03_current_quark_masses_from_epochs.py` | Derive m_u, m_d from φ-ladder: M_P·φ^{-N_u}, M_P·φ^{-N_d} (N_u=110, N_d=105) | Working |
| `04_string_tension_and_confinement.py` | **Four-term proton decomposition** + Λ_QCD + string tension + E_self/modulus/phase/memory | Working, but **C_mem fitted** to match m_p (not first-principles) |
| `05_chiral_perturbation.py` | Pion mass from GMOR using GU-derived m_u, m_d, Λ_QCD (no PDG input) | Working, **3.8% error on m_π** |
| `README.md` | This document | Current |

---

## Key Results

### Proton Mass (Four-Term Ansatz) — Matches CODATA, But Read the Fine Print

The proton decomposition from "Some GU Particles Stuff.md" is a **postulated ansatz**, not a derivation from L_total:

| Component | Formula | Value (MeV) | Status |
|-----------|---------|-------------|--------|
| \(\Lambda_\text{QCD}\) | \((\pi/3) \cdot M_P \cdot \varphi^{-95}\) | 179.0 | Motivated (SU(3)), not derived |
| \(E_\text{self}\) | \((4\pi/\varphi) \cdot \Lambda_\text{QCD}\) | +1390.3 | Motivated (bag), not derived |
| \(E_\text{modulus}\) | \((1/\pi) \cdot M_P \cdot \varphi^{-91}\) | +373.0 | Motivated (standing wave), not derived |
| \(E_\text{phase}\) | \(2m_u + m_d\) (valence quarks) | +1.9 | Motivated (quarks), not derived |
| \(E_\text{memory}\) | \(-C_\text{mem} \cdot (\pi^2/\varphi) \cdot M_P \cdot \varphi^{-96}\) | -826.9 | **C_mem = 1.2831 FITTED** (not derived; needs hadronic NLDE at N=95) |
| **Total** | | **938.272** | 9 free choices, 1 constraint |

The numerical agreement is not yet a prediction — there are 9 free parameters (5 node integers, 4 prefactors, plus C_mem fitted) for 1 target number. The structural insight that the proton decomposes into bag + breathing + valence + memory IS a genuine framework; the numerical verification requires the FRG + hadronic soliton computation.

### Light Quark Masses — Ansatz, Not Derived

\[m_u = M_P \cdot \varphi^{-110} \text{ (bare scale)}, \quad m_d = M_P \cdot \varphi^{-105} \text{ (bare scale)}\]

**NOTE**: The canonical quark epochs are N_u=110, N_d=105 (from `gu_constants.py`). Previous versions incorrectly used epochs 107, 106. The bare scale masses M_P·φ^{-N_q} lack C_q shape factors (analogous to C_e for the electron) which have not yet been derived for quarks. The φ-ladder scale IS first-principles; the specific prefactors and epochs need the Yukawa sector.

### Pion Mass from GMOR — 3.8% Error (Semi-First-Principles)

Using GU-derived \(\Lambda_\text{QCD}\) and φ-ladder quark masses with dimensional estimates for \(f_\pi\) and \(\langle\bar\psi\psi\rangle\):

\[m_\pi \approx 144.9 \text{ MeV} \quad (\text{PDG: } 139.6 \text{ MeV})\]

Encouraging, but \(f_\pi\) and the condensate are estimated, not computed from the chiral FRG flow.

---

## What Is Derived vs Input

### Genuinely GU-Derived

These come from the GU framework without PDG input:

| Quantity | Formula | Source |
|----------|---------|--------|
| \(\Lambda_\text{QCD}\) | \(M_P \cdot \varphi^{-95}\) | Epoch ladder (N_QCD = 95) |
| \(\alpha_\text{GUT}\) | Calibrated from α_EM (1/(8πφ) FALSIFIED — gives α_EM≈1/180) | gu_constants |
| EFT thresholds | \(X_\text{EW} = M_P \varphi^{-89}\), etc. | Epoch ladder |
| Memory coupling | \(\lambda_\text{rec}/\beta = e^\varphi/\pi^2\) | Law 32 |
| Pattern-k=2 | \(\pi^2\) enhancement at QCD scale | Law 37 |
| b-coefficients | 41/6, -19/6, -7 (standard SM) | One-loop SM |
| β-function sign | \(d\alpha/dt = +(b/2\pi)\alpha^2\) | Corrected convention |

### Derived from GMOR + PDG

These use a GU-derived scale combined with a measured input:

| Quantity | Formula | GU Part | PDG Part |
|----------|---------|---------|----------|
| Constituent mass (u,d) | \(\Lambda^3_\text{QCD}/(3f_\pi^2) + m_\text{current}\) | \(\Lambda_\text{QCD}\) | \(f_\pi\), \(m_u\), \(m_d\) |
| Constituent mass (s) | Same | \(\Lambda_\text{QCD}\) | \(f_\pi\), \(m_s\) |
| Binding energies | Variational Cornell | \(\sigma \sim \Lambda^2\) | \(\alpha_s\) at QCD scale |

### PDG Input (Not Yet Derivable)

| Quantity | Value | Why needed |
|----------|-------|-----------|
| Current quark masses | \(m_u\)=2.16, \(m_d\)=4.67, \(m_s\)=93.4 MeV | Lagrangian parameters — need Yukawa sector |
| \(f_\pi\) = 92.1 MeV | Pion decay constant | Used in GMOR relation |
| Heavy quarks | \(m_c\)=1270, \(m_b\)=4180 MeV | No chiral mass generation |

### Placeholders (Structural But Not Numerical)

| Quantity | Issue | What's needed |
|----------|-------|---------------|
| Memory integral \(\int\rho^4 d^3x\) | No hadronic soliton profile | Solve hadronic NLDE at N~95 |
| Lock coefficients \(\Lambda_m\) at QCD epoch | Lock sector not projected | FRG lock-sector computation |
| String tension O(1) factor | \(\sigma = \Lambda^2\) vs lattice \((440)^2\) | FRG or lattice calibration |
| Pattern-k=2 mechanism | \(\pi^2\) enters — but how exactly? | Derive from action at QCD epoch |

---

## Fixes Applied (February 2026)

### In `01_qcd_hadron_calculation.py`:

1. **b₁ coefficient**: Changed from `41/10` (wrong) to `41/6` (correct GUT-normalized)
2. **EFT thresholds**: Added. SU(2) freezes below X_EW, SU(3) freezes below X_QCD
3. **β-function sign**: Verified: `dα/dt = +(b/2π)α²` (no leading minus)
4. **α₁ convention**: GUT-normalized throughout. `αY = (3/5)·α₁` for EM observables
5. **Constituent masses**: Now derived from GMOR (`Λ³/(3f²_π) + m_current`), not hardcoded 330 MeV
6. **Binding energies**: Variational Cornell potential, not ad-hoc formulas
7. **Hyperfine**: Proper contact interaction formula, no `× 200` fudge
8. **Memory**: Uses actual `e^φ/π²` coupling, not `× 10` fudge
9. **Logic bug**: Fixed `E_hyp = 100*(1 if q1==q2==q3 else -1)` tautology
10. **Honest labeling**: Every quantity tagged with its provenance

### In `02_bound_state_equations.py`:

1. **Units**: All MeV and MeV⁻¹. Removed false "fm units" comments
2. **Name**: "Schrödinger + Cornell", not "Bethe-Salpeter" (honest about what it solves)
3. **Diquark binding**: Fixed from `V₀ × m_reduced` (dimensionally wrong) to proper eigenvalue problem
4. **Faddeev**: Fixed `σ × r_conf` dimensional error — now uses consistent MeV⁻¹ grid
5. **GU corrections**: Replaced `R_mem = N²` (made up) with dimensional estimate from explanatory/CONSCIOUSNESS.md
6. **Pattern correction**: Replaced `/100` fudge with documented O(1) enhancement
7. **Grid**: Automatic scaling based on Bohr radius and confinement length
8. **Color factors**: Explicit and documented (4/3 for singlet, 2/3 for 3̄ diquark)
9. **Level 2 roadmap**: Clear TODO for actual Bethe-Salpeter/Faddeev/ChPT

---

## How the Physics Works

### Stage 1: Gauge Running

The three SM gauge couplings \(\alpha_1, \alpha_2, \alpha_3\) start unified at the GUT scale \(X_\text{GUT} = M_P \varphi^{-67}\). (Note: \(\alpha_\text{GUT} = 1/(8\pi\varphi)\) is FALSIFIED — gives α_EM≈1/180, 24% wrong; gu_constants now calibrates from α_EM.)

They evolve via one-loop β-functions:

\[
\frac{d\alpha_i}{dt} = \frac{b_i}{2\pi} \alpha_i^2, \quad t = \ln(X/X_\text{GUT})
\]

with piecewise b-coefficients respecting EFT thresholds:
- **Full SM** (above EW): All particles active
- **SU(2) frozen** (below EW): W, Z, Higgs integrated out
- **SU(3) frozen** (below QCD): Quarks and gluons confined

The integration stops at \(\Lambda_\text{QCD}\) where \(\alpha_s \sim 1\).

### Stage 2: Chiral Symmetry Breaking

Below \(\Lambda_\text{QCD}\), quarks acquire a large dynamical mass from the quark condensate:

\[
M_\text{dyn} = \frac{|\langle\bar\psi\psi\rangle|}{3f_\pi^2} \approx \frac{\Lambda^3_\text{QCD}}{3f_\pi^2} \approx 300\text{-}350 \text{ MeV}
\]

The constituent mass is: \(m_\text{const} = M_\text{dyn} + m_\text{current}\).

### Stage 3: Bound States

Hadrons are bound states in the Cornell potential:

\[
V(r) = -\frac{4\alpha_s}{3r} + \sigma r
\]

- **Mesons** (\(q\bar{q}\)): Direct Schrödinger eigenvalue problem
- **Baryons** (\(qqq\)): Two-step quark-diquark approximation
  - Form scalar diquark in color \(\bar{3}\) channel
  - Bind diquark to spectator quark

### GU Corrections

Two GU-specific effects modify hadron masses:

1. **Memory binding**: \(E_\text{mem} = -(e^\varphi/\pi^2) \cdot \int\rho^4\,d^3x\)
   - Currently estimated by dimensional analysis
   - Proper calculation needs hadronic soliton profile

2. **Pattern-k=2 enhancement**: Strong coupling is enhanced by \(\pi^2\) at the QCD epoch
   - Enters through the string tension \(\sigma\)
   - Exact mechanism not yet derived from the action

---

## Known Limitations

1. **Pion mass**: The constituent model gives \(m_\pi \approx\) 600+ MeV instead of 140 MeV. This is expected — the pion is a pseudo-Goldstone boson whose mass requires chiral perturbation theory: \(m_\pi^2 f_\pi^2 = -(m_u + m_d)\langle\bar\psi\psi\rangle\).

2. **Non-relativistic**: Light quarks are inherently relativistic (\(m_q \sim\) 5 MeV \(\ll \Lambda_\text{QCD}\)). The Schrödinger approach is only semi-quantitative.

3. **String tension**: \(\sigma = \Lambda^2_\text{QCD}\) gives \(\sigma \approx (171)^2\) MeV² vs lattice \((440)^2\) MeV². There is an O(6) factor missing.

4. **No sea quarks**: Virtual \(q\bar{q}\) pairs contribute \(\sim\) 100 MeV to nucleon mass.

5. **No instantons**: Topological vacuum fluctuations affect the \(\eta'\) mass and nucleon spin.

---

## What Would Make This First-Principles

For the hadron sector to be genuinely "from first principles" in GU, we need:

1. **Current quark masses from Yukawa coupling**: The Yukawa sector of GU must predict \(m_u, m_d, m_s\) from the theory (via Yukawa couplings at the appropriate epoch). Currently these are PDG inputs.

2. **String tension from FRG**: \(\sigma\) should emerge from the non-perturbative FRG flow at the QCD epoch, not be estimated as \(\Lambda^2\).

3. **Hadronic soliton profile**: The memory integral \(\int\rho^4 d^3x\) needs the actual \(\rho\) profile of the hadronic soliton, which requires solving the NLDE in the QCD regime.

4. **Lock-sector projection at N~95**: The lock coefficients \(\Lambda_m(X)\) must be computed at the hadronic epoch, not inherited from the electron sector.

5. **Pion as Goldstone**: Either solve the full chiral Lagrangian emerging from GU's SSB cascade, or implement ChPT with GU-derived low-energy constants.

---

## Connection to Other Pipeline Components

| Component | How it feeds into hadrons |
|-----------|--------------------------|
| `pipeline/GU_formation_pipeline.py` | Provides corrected FRG flow, gauge running |
| `gu_constants.py` | Epoch scales, coupling constants |
| `explanatory/CONSCIOUSNESS.md` | Memory formula for binding correction |
| `08_RHO_FIELD_UNITY/` | ρ is the same field in hadronic and leptonic sectors |
| `03_PARTICLE_MASSES/` | Quark masses from φ-ladder (to be reconciled) |
