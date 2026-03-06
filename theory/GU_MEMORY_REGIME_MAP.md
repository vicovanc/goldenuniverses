# GU Memory Regime Map

This note summarizes how memory operates across cosmological epochs in the Golden Universe (GU) framework, based on the Feb 2026 cosmology rebuild and tension-resolution pass.

## 1) Core Memory Structure (Canonical)

The memory sector is modeled by:

- History functional: `H[Omega] = Omega^dagger Omega` (effective minimal closure form)
- Legacy Hamiltonian exact-kernel notation often writes `rho^4`; this is treated as a regime-specific composite response, while cosmology closure uses the minimal `Omega^dagger Omega` authority form.
- Decay scale: `beta(X) = X`
- Recovery coupling: `lambda_rec(X)/beta(X) = e^phi / pi^2`
- Local memory variable: `M` obeying a first-order relaxation/source equation in the coupled system
- Validity rule: exact nonlocal kernel and local `M_N` reduction are both admissible, but any claim must declare which regime/approximation is used.

Current closure-gate status (from machine diagnostics):

- `beta(X)`: provisional
- `lambda_rec(X)`: provisional at absolute level (ratio-level closed)
- `g_{OmegaX}(X)`: constrained
- `V_X(X)`: chosen non-unique

Full-ODE identifiability note: current machine report remains rank-deficient (`rank 2/5`), so promotion to DERIVED is blocked by policy.

Effective potential level:

- `V_eff = V_X + V_int + V_mem`
- `V_mem` and its force term `F_mem` are always present structurally

Key point: memory is part of the full equations at all times, but its numerical impact is regime-dependent.

---

## 2) Regime-by-Regime Behavior

## A. Inflation (UV, high X)

What we learned:

- In solved trajectories, memory is numerically subleading at horizon exit (`M ~ 0` in practice).
- Inflation observables (`n_s`, `r`, `A_s`) are dominated by `V_X` shape, not by memory backreaction.
- Memory must still be included in the formal derivatives for consistency, but it does not control fit quality in this regime.

Operational status:

- Memory = structurally active, phenomenologically weak.

---

## B. End of Inflation and Reheating

What we learned:

- Memory enters as a correction channel to the background evolution and reheating bookkeeping.
- Interaction strength and reheating details still depend on unresolved coupling structure (`g_0` sector), not memory alone.

Operational status:

- Memory = moderate correction channel, not a standalone reheating driver.

---

## C. Baryogenesis Epoch

What we learned:

- Main quantitative control is from CP source + Boltzmann washout (`K = Gamma_D/H`) and sphaleron conversion.
- Required entropy dilution is `S ~ 7.9` in the current closure.
- Memory may influence effective rates indirectly through background evolution, but current successful fit chain is washout-driven, not memory-dominated.

Operational status:

- Memory = indirect contributor; washout network is primary.

---

## D. Recombination / CMB Epoch

What we learned:

- Recombination tension was resolved by replacing ad hoc correction factors with explicit Peebles ODE treatment.
- The decisive physics is atomic non-equilibrium (Lyman-alpha trapping + two-photon channel), not a large memory correction.
- Current result: `z_rec ~ 1064` vs Planck `1089.8` (about 2.4% offset in simplified 3-level treatment).

Operational status:

- Memory = background-level influence at most; atomic kinetics dominate observables.

---

## E. Late-Time Structure / Dark Sector

What we learned:

- Dark glueball self-interaction tension is controlled by non-perturbative scattering normalization.
- Contact estimate gives large `sigma/m`; viable values require suppression factor (`C`-type non-perturbative reduction).
- This is not evidence of large cosmological memory forcing; it is a dark microphysics/lattice problem.

Operational status:

- Memory = plausible framework ingredient, but current constraint is dark scattering microphysics.

---

## F. Induced Gravity / Heat-Kernel Sector

Critical interpretation update:

- GU memory modes are treated as classical backgrounds in induced-gravity counting.
- They should not be included as propagating quantum DOF in `Str(a_0)` counting.
- This preserves consistency between `c_R` and cosmological-constant bookkeeping.

Operational status:

- Memory = geometric/background structure in UV gravity accounting, not quantum particle content.

---

## 3) What Changed in Theory Understanding

Before this pass:

- Memory was often treated as potentially dominant across all cosmological stages.

After this pass:

- Memory has a cleaner role: structurally universal, numerically selective.
- Inflation/CMB fits are primarily potential/atomic-kinetic controlled.
- Memory is more likely to matter strongly in history dependence, backreaction organization, and cross-scale consistency, not as a universal leading term in each observable.

In short:

- Memory is real and necessary.
- Memory is not uniformly dominant.
- Regime dependence is now an explicit canonical feature.

---

## 4) Memory-Specific Task Status (Latest Machine Pass)

1. **Dark-sector scattering coefficient** — **implemented**
   - Deterministic GU coefficient now used: `C_GU = exp(-2π/φ²)·φ^-7 ≈ 0.0031`.
   - Contact upper bound remains large, but GU-calibrated `σ/m` moves into the SIDM-favored window.
   - Artifact path: `derivations/06_MEMORY_VS_OTHERS/01_dark_scattering_first_principles.py`.

2. **Full thermal Boltzmann network with memory-coupled rates** — **implemented**
   - Full coupled network now reports `η_B(with memory)` and `η_B(no memory)` explicitly.
   - Current output: memory correction is sub-percent; absolute `η_B` remains low vs observation.
   - Artifact path: `derivations/06_MEMORY_VS_OTHERS/02_memory_boltzmann_network.py`.

3. **Recombination extension (H + He + matter-temperature decoupling)** — **implemented**
   - Extension integrated and tested against `z_rec`; memory contribution currently non-measurable at sub-percent level.
   - Artifact path: `derivations/42_RECOMBINATION_HELIUM_DECOUPLING/01_recombination_extension.py`.

4. **Derive `V_X` from `L_total`** — **partially closed (non-unique)**
   - Candidate generator and gate wiring are in place.
   - Latest report keeps `V_X` as `chosen_non_unique` (`5/9` candidates admissible).
   - Artifact path: `derivations/43_VX_FROM_LTOTAL/01_vx_from_ltotal.py`.

---

## 5) Canonical One-Line Summary

Memory in GU is a universal structural channel (`beta = X`, `H[Omega]` closure) whose numerical impact is strongly epoch-dependent: subleading in inflation and recombination fits, potentially important in backreaction, history dependence, and cross-sector consistency, while full uniqueness remains gated.

