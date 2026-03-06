# GU_formation_pipeline.py — Exhaustive Inventory

**File:** `GU_formation_pipeline.py` (889 lines)  
**Purpose:** Formation → NLDE → mass pipeline for Golden Universe Theory.

---

## 1. Every Function Defined and What It Does

### Section 0: No functions (constants only)

### Section 1: Formation Chain (Law 15)

| Function | Signature | What it does |
|----------|-----------|--------------|
| `golden_impulse` | `golden_impulse()` | Computes Golden Impulse Z₁ and clock start X₀. Z₁ = (M_P/(4√π)) exp(i·2π/φ²), X₀ = \|Re(Z₁)\|. Returns `(Z1, X0, Z1_mag, theta)`. |
| `epoch_scale` | `epoch_scale(X0, n)` | Returns critical threshold at deepness node n: X_{critical,n} = X₀ · φ^{−n}. |
| `phase_closure_quality` | `phase_closure_quality(n)` | Computes how close n/φ² is to an integer. Returns `(k_nearest, residual)` with k_nearest = round(n/φ²), residual = \|n/φ² − k\|. |
| `scan_resonances` | `scan_resonances(n_max=200, threshold=mpf('0.01'))` | Scans n = 1..n_max for nodes where \|n/φ² − k\| < threshold. Returns list of `(n, k, residual)`. |

### Section 2: φ-Ladder and Particle Identification

| Function | Signature | What it does |
|----------|-----------|--------------|
| `particle_epoch_table` | `particle_epoch_table(X0)` | For each entry in `PARTICLES`, computes X_n = epoch_scale(X0, n), phase k and residual. Returns dict: particle → {n, channel, X_n_MeV, X_n_over_MP, phase_k, phase_residual}. |

### Section 3: Mass Computation

| Function | Signature | What it does |
|----------|-----------|--------------|
| `pi_n` | `pi_n(n)` | Regularized pi: π_n = n·sin(π/n), approaching π as n→∞. |
| `electron_mass_route_A` | `electron_mass_route_A()` | Route A: m_e = M_P·(2π_N/φ^{N_e})·C_e(ν)·η_QED. Finds ν such that C_e(ν) = C_target (C_target from CODATA). Uses elliptic K,E, formation coupling y_e, gauge E_gauge, topology (k_res, p, q). Returns (m_e, C_e_val, nu_sol, eta_QED, prefactor). |
| `hierarchy_mass` | `hierarchy_mass(N, C_ratio=mpf('1'))` | m = m_e·(C_particle/C_e)·φ^{N_e−N}. Calls electron_mass_route_A() for m_e and N_e=111, then applies hierarchy. |
| `compute_all_masses` | `compute_all_masses()` | Computes masses for electron, muon, tau, proton, neutron. Electron from Route A; others use C_ratio derived from CODATA and φ^{ΔN}. Returns dict of {particle: {mass_MeV, CODATA, error_pct, N, C_ratio}}. |

### Section 4: FRG Flow Framework

| Function | Signature | What it does |
|----------|-----------|--------------|
| `wetterich_rhs_structure` | `wetterich_rhs_structure()` | Returns a dict describing the Wetterich equation structure (equation string, field content, traces, regulator, note). Informational only. |
| `frg_beta_functions` | `frg_beta_functions(y)` | Takes tuple y = (m_bar, lam_S, lam_V, alpha1, alpha2, alpha3, K_bar, omega_bar_star). Returns tuple of 8 derivatives (dy/dt) from explicit GU truncation + Litim regulator. |
| `h1_litim` | `h1_litim(m_bar)` | Litim tadpole: 1/(1+m̄²). |
| `h2_litim` | `h2_litim(m_bar)` | Litim bubble: 1/(1+m̄²)². |
| `solve_frg_flow` | `solve_frg_flow(X0, X_target, y0=None, n_steps=10000)` | Integrates FRG ODE from X₀ to X_target with RK4. t = ln(X/X₀). Uses safe_betas (clamping). Returns dict of final couplings plus alpha_EM, sin2_theta_W, w_02, w_20, w_11, Lambda_lock. |
| `coupling_at_epoch` | `coupling_at_epoch(coupling_name, X_n, X0)` | Runs solve_frg_flow(X0, X_n) and returns result.get(coupling_name). |

### Section 5: Gauge Sector

| Function | Signature | What it does |
|----------|-----------|--------------|
| `gauge_running_structure` | `gauge_running_structure()` | Returns dict with unified_group, breaking_chain, matching_conditions_at_X_GUT, one_loop_beta_coefficients, G_e_from_SU5, note. Informational only. |
| `force_strengths_at_epoch` | `force_strengths_at_epoch(n, X0)` | Returns dict of force names → {coupling, scale, derivation, status}. Uses alpha_em, 1/29, 0.1179, (m_e/M_P)²; status flags indicate what is derived vs placeholder. |

### Section 6: Lock Normalization

| Function | Signature | What it does |
|----------|-----------|--------------|
| `phase_stiffness` | `phase_stiffness(Z_chi, R0_vac)` | K(X) = Z_χ·R₀². Returns None if either input is None. |
| `lock_strength` | `lock_strength(K_X, activation=mpf('1'))` | Λ_lock(X) = K(X)·activation. Returns None if K_X is None. |
| `target_frequency` | `target_frequency(X_n, omega_bar_star)` | ω★(X) = X_n·ω̄★. Returns None if omega_bar_star is None. |
| `cosine_series_curvature` | `cosine_series_curvature(a_m_coeffs)` | κ = Σ_{m≥1} a_m·m². Returns None if a_m_coeffs is None. |

### Main

| Function | Signature | What it does |
|----------|-----------|--------------|
| `main` | `main()` | Runs full pipeline: Formation anchor, φ-ladder table, resonances, masses, force strengths, FRG flow X₀→X_e, then prints pipeline status. |

---

## 2. Implemented vs Placeholder / Circular

### Fully implemented (no CODATA/placeholders in the logic)

- **Formation:** `golden_impulse`, `epoch_scale`, `phase_closure_quality`, `scan_resonances`, `particle_epoch_table` — all from first principles (φ, M_P, π).
- **FRG:** `frg_beta_functions`, `h1_litim`, `h2_litim`, `solve_frg_flow`, `coupling_at_epoch` — explicit ODE and RK4; UV ICs use one analytic parameter (α_GUT) set so α_EM(X_e) matches CODATA.
- **Lock helpers:** `phase_stiffness`, `lock_strength`, `target_frequency`, `cosine_series_curvature` — formulas implemented; they need Z_χ, R₀, ω̄★ from FRG/elsewhere.
- **Structural/info:** `wetterich_rhs_structure`, `gauge_running_structure` — documentation only.
- **pi_n:** Implemented.

### Uses CODATA or fixed numbers (boundary / calibration)

- **electron_mass_route_A:** C_target is computed from CODATA['electron']; the closure C_e(ν)=C_target is solved so the *output* m_e matches CODATA by construction. So electron mass is **back-computed / calibrated** to CODATA, not predicted.
- **compute_all_masses (muon, tau, proton, neutron):** C_ratio is set from CODATA and φ^{ΔN} so that GU mass = CODATA. So these masses are **back-computed** to match CODATA, not derived from first principles.
- **hierarchy_mass:** If C_ratio=1 it uses Route A (electron); if C_ratio is passed from elsewhere it applies hierarchy; when used from compute_all_masses, C_ratio comes from CODATA → circular for non-electron.
- **solve_frg_flow UV ICs:** α_GUT = 1/63.0776276 is chosen so α_EM(X_e)=1/137.036 (one datum). Other ICs (m_bar_0, lam_S_0, lam_V_0, K_bar_0, omega_bar_star_0) are fixed numbers, not yet derived from heat kernel.

### Placeholder / not yet implemented

- **force_strengths_at_epoch:** Returns fixed numbers (α_em, 1/29, 0.1179, (m_e/M_P)²) with status text saying explicit threshold matching at X_EW, X_QCD and induced gravity are still needed.
- **phase_stiffness / lock_strength / target_frequency:** Implemented as formulas but are never called with real Z_χ, R₀, ω̄★ from FRG; FRG currently sets beta_K = 0, beta_omega_star = 0 so K̄ and ω̄★ are constant (placeholders).
- **NLDE BVP:** Not in this file; mentioned in main() as “Solve full NLDE BVP at X_e with frozen FRG coefficients”.
- **Multi-epoch FRG:** Single flow X₀ → X_target only; no epoch loop or threshold switching.
- **QCD chiral flow:** No separate chiral/constituent mass flow.

---

## 3. Exact FRG Beta Functions as Coded (All 8 Equations)

**State vector:**  
`y = (m_bar, lam_S, lam_V, alpha1, alpha2, alpha3, K_bar, omega_bar_star)`

**Auxiliary:**
- `w = m_bar**2`
- `h1 = 1/(1+w)`  (tadpole)
- `h2 = 1/(1+w)**2`  (bubble)
- `eta_psi = (1/(6*pi**2)) * 4 * alpha3`  (anomalous dimension, leading QCD)
- `pi` is global set to `mp_pi` (line 316)

**Coded equations:**

1. **Mass (∂_t m̄)**  
   `beta_m = -(1 - eta_psi)*m_bar + (1/pi**2)*lam_S*m_bar*h1`

2. **Scalar four-fermion (∂_t λ̄_S)**  
   `beta_lam_S = (2+2*eta_psi)*lam_S - (2/pi**2)*h2*(lam_S**2 + 1.5*lam_S*lam_V + 1.5*lam_V**2) - (3/pi**2)*alpha3*lam_S`

3. **Vector four-fermion (∂_t λ̄_V)**  
   `beta_lam_V = (2+2*eta_psi)*lam_V - (2/pi**2)*h2*(0.5*lam_S**2 + 1.25*lam_S*lam_V + 0.75*lam_V**2) - (3/pi**2)*alpha3*lam_V`

4. **U(1) gauge (∂_t α₁)**  
   `b1 = 41/6`  
   `beta_alpha1 = -(b1/(2*pi))*alpha1**2`

5. **SU(2) gauge (∂_t α₂)**  
   `b2 = -19/6`  
   `beta_alpha2 = -(b2/(2*pi))*alpha2**2`

6. **SU(3) gauge (∂_t α₃)**  
   `b3 = -7`  
   `beta_alpha3 = -(b3/(2*pi))*alpha3**2`

7. **Lock stiffness (∂_t K̄)**  
   `beta_K = 0`

8. **Lock target frequency (∂_t ω̄★)**  
   `beta_omega_star = 0`

**Summary:** Six equations are nontrivial (mass, λ̄_S, λ̄_V, α₁, α₂, α₃); two are placeholder (K̄, ω̄★ constant).

---

## 4. RK4 Solver Details

### Step count

- **Default:** `n_steps=10000` in `solve_frg_flow`.
- **In main():** `solve_frg_flow(X0, X_e, n_steps=5000)`.

So main uses **5000** steps from X₀ to X_e.

### Time variable and step size

- RG time: `t = ln(X/X₀)`. From X₀ to X_target: `t_final = log(X_target/X0)` (negative for X_target < X₀).
- Step: `dt = t_final / n_steps`.
- Integration: one step per loop; no adaptive stepping.

### Clamping (safe_betas)

Before each call to `frg_beta_functions`, state is clamped:

- `y[0]` (m̄): clamp to `[-100, 100]`
- `y[1]` (λ̄_S): clamp to `[0, 200]`
- `y[2]` (λ̄_V): clamp to `[0, 200]`
- `y[3], y[4], y[5]` (α₁, α₂, α₃): clamp to `[1e-10, 10]`
- `y[6], y[7]` (K̄, ω̄★): not clamped in the shown code

Clamping is applied to the copy passed to `frg_beta_functions`; the actual state `y` is updated by RK4 without clamping, so large values can still occur between steps.

### Initial conditions (y0)

When `y0 is None`:

| Variable | Value | Comment |
|----------|--------|--------|
| alpha_GUT | 1/63.0776276 | Set so α_EM(X_e)=1/137.036 |
| m_bar_0 | 0.01 | Small at Planck |
| lam_S_0 | 0.5 | Sub-critical |
| lam_V_0 | 0.1 | Sub-critical |
| alpha1_0 | (3/5)*alpha_GUT | GUT normalization |
| alpha2_0 | alpha_GUT | |
| alpha3_0 | alpha_GUT | |
| K_bar_0 | 1.0 | Phase stiffness O(1) |
| omega_bar_star_0 | 0.8 | Dimensionless target freq |

### RK4 update (per step)

```
k1 = safe_betas(y)
y_temp = y + 0.5*dt*k1
k2 = safe_betas(y_temp)
y_temp = y + 0.5*dt*k2
k3 = safe_betas(y_temp)
y_temp = y + dt*k3
k4 = safe_betas(y_temp)
y = y + (dt/6)*(k1 + 2*k2 + 2*k3 + k4)
```

Precision: mpmath with `mp.dps = 50`.

---

## 5. Mass Computation: Derived vs Back-Computed from CODATA

### Electron

- **electron_mass_route_A:**  
  - Target: `C_target = CODATA['electron'] / (M_P_MeV * prefactor * eta_QED)`.  
  - Solves `C_e_full(nu) = C_target` for ν (e.g. starting at 0.82).  
  - Then `m_e = M_P_MeV * prefactor * C_e_val * eta_QED` ⇒ m_e equals CODATA by construction.  
- **Verdict:** **Back-computed** from CODATA (one boundary condition to fix ν). Structural form (elliptic, topology, η_QED) is derived; numerical value is not a prediction.

### Muon

- `C_mu_ratio = CODATA['muon'] / (m_e * phi^11)` then `m_mu = m_e * C_mu_ratio * phi^11` ⇒ m_mu = CODATA by construction.
- **Verdict:** **Back-computed** (C_ratio chosen to match CODATA).

### Tau

- Same pattern: `C_tau_ratio = CODATA['tau'] / (m_e * phi^17)`, then m_τ = m_e * C_tau_ratio * phi^17.
- **Verdict:** **Back-computed**.

### Proton

- `C_p_ratio = CODATA['proton'] / (m_e * phi^16)`, then m_p = m_e * C_p_ratio * phi^16.
- **Verdict:** **Back-computed**.

### Neutron

- `delta_mn = CODATA['neutron'] - CODATA['proton']`, then m_n = m_p + delta_mn (isospin splitting from CODATA).
- **Verdict:** **Back-computed** (proton from above + CODATA splitting).

**Overall:** Only the *form* of the hierarchy (m = m_e·(C/C_e)·φ^{ΔN}) and Route A structure are derived; all numerical masses in this script are tuned to CODATA.

---

## 6. Functions That Would Need to Be Added

### (a) Multi-epoch FRG

- **Epoch loop:** A function that, for a list of epoch scales (e.g. X_n for n in particle list), either:
  - runs a single flow from X₀ to each X_n and stores results, or
  - runs one flow with **piecewise beta functions** that change at threshold scales X_GUT, X_EW, X_QCD (e.g. b_i(X) and/or field content).
- **Threshold handling:** Functions that:
  - Take X_EW, X_QCD (or derive them from m_H²(X)=0, confinement condition).
  - Switch or weight beta coefficients (e.g. b₁, b₂, b₃) or regulator content at these X.
- **State across epochs:** Optionally return or store full coupling history y(X) for many X_n, not only one X_target.
- **No new physics formula** in the current file for multi-epoch; the comment in the code states b_i(X) is piecewise and “X-dependent threshold switching” is the intended correction.

### (b) NLDE BVP shooting

- **BVP setup:** Function(s) that define the radial NLDE (e.g. 2-point BVP in r for the soliton profile), with:
  - Coefficients taken from FRG output at X_e: m_bar → m★, w_02, w_20, w_11, Λ_lock, ω★ (from K_bar, omega_bar_star, X_n).
- **Boundary conditions:** Enforce BCs at r=0 and r→∞ (or r_max).
- **Shooting or collocation:** Either:
  - Shoot for a parameter (e.g. central value or ω) so that the other boundary is satisfied, or
  - Use a collocation/solver (e.g. scipy boundary value solver) for the radial ODE system.
- **Q = 1 normalization:** Enforce charge/lock normalization Q = 1 (as in the docstring) and obtain ω from “lock” condition.
- **Energy functional:** Evaluate the 6-term Hamiltonian (vacuum-subtracted) on the solution to get E_rest = m c² and thus m_e (to compare with Route A / CODATA).
- **Current file:** Has no BVP solver, no radial NLDE ODE, no E_rest evaluation; only lock-related helpers (phase_stiffness, lock_strength, target_frequency, cosine_series_curvature) that would feed into such a solver.

### (c) QCD chiral flow

- **Chiral/constituent mass:** A separate running mass or sigma expectation value (e.g. m_σ(X) or ⟨ψ̄ψ⟩(X)) that drives chiral symmetry breaking, possibly with its own beta or gap equation.
- **Threshold at X_QCD:** Function that defines or detects X_QCD (e.g. where α₃ or a chiral order parameter crosses a threshold) and possibly switches to a different effective description (e.g. hadronic).
- **Integration with current FRG:** Either:
  - Add equations to the same 8-dimensional system (e.g. chiral condensate or constituent mass), or
  - A separate “chiral flow” that takes α₃(X) and other couplings from the main FRG and returns m_constituent(X) or similar.
- **Current file:** Only has leading QCD effect in η_psi (4*alpha3/(6*pi²)) and in the −(3/pi²)*alpha3*lam_S/V terms; no dedicated chiral or constituent-mass flow.

---

## 7. Current main() Flow and Output

### Execution order

1. **Banner**  
   Print "GOLDEN UNIVERSE — FORMATION PIPELINE".

2. **Formation anchor**  
   Call `golden_impulse()` → Z₁, X₀, |Z₁|, θ.  
   Print: |Z₁|, θ (rad and °), cos(θ), X₀ (MeV), X₀/M_P.

3. **φ-ladder table**  
   Call `particle_epoch_table(X0)`.  
   Print table: Particle, n, X_n/M_P, k (resonance), |n/φ²−k| for electron, muon, tau, proton, neutron.

4. **Phase-closure resonances**  
   Call `scan_resonances(n_max=200, threshold=0.005)`.  
   Print table: n, k, |n/φ²−k|, φ^{111−n}, candidate label (ELECTRON, MUON, TAU, HADRON?).

5. **Particle masses**  
   Call `compute_all_masses()`.  
   Print table: Particle, N, GU mass (MeV), CODATA (MeV), error %.

6. **Force strengths**  
   Call `force_strengths_at_epoch(111, X0)`.  
   Print for each force: name, α ≈ value, [status string].

7. **FRG flow**  
   X_e = epoch_scale(X0, 111).  
   Print: X₀, X_e, t_e = ln(X_e/X₀), “Integrating 8 coupled beta functions”.  
   Call `solve_frg_flow(X0, X_e, n_steps=5000)` → frg_result.

8. **FRG output**  
   Print “FROZEN COEFFICIENTS AT X_e”: m̄, λ̄_S=w₀₂, λ̄_V=w₂₀, α₁, α₂, α₃, α_EM, K̄, ω̄★ with short role labels.  
   Print α_EM vs CODATA and 1/α_EM comparison with % error.  
   Print sin²θ_W(X_e) vs 0.23122 and note on minimal SU(5).  
   Print four-fermion analysis: π² critical coupling, λ̄_S(X_e), λ̄_V(X_e), “SUB-CRITICAL” and short explanation.

9. **Pipeline status**  
   Print “PIPELINE STATUS — ALL ITEMS CLOSED” and checklist (Formation, NLDE structure, energy functional, mass hierarchy, FRG betas, Fierz, gauge running, lock sector, UV ICs, FRG ODE, α_EM tuned, four-fermion).  
   Print “REMAINING”: NLDE BVP at X_e, E_rest→m_e, X-dependent thresholds for sin²θ_W and α₃.

### Output (summary)

- Formation numbers (Z₁, X₀, θ).
- Particle epoch table (5 rows).
- Resonance list (several n with small residual).
- Mass table (5 particles, GU vs CODATA, error %).
- Force strengths (4 forces with status).
- FRG couplings at X_e (8 + alpha_EM, sin²θ_W).
- α_EM and sin²θ_W comparison lines.
- Four-fermion paragraph.
- Status checklist and “REMAINING” items.

---

## Constants (Exact Values in Code)

| Symbol | Value / Formula |
|--------|------------------|
| φ | (1+√5)/2 |
| φ² | phi**2 |
| θ (golden_angle) | 2π/φ² |
| M_P_GeV | 1.22089e19 |
| M_P_MeV | M_P_GeV * 1000 |
| ℏ | 1.054571817e-34 |
| c | 299792458 |
| G_N | 6.67430e-11 |
| l_P | √(ℏ G/c³) |
| t_P | l_P/c |
| α_EM | 1/137.035999177 |
| CODATA['electron'] | 0.51099895069 MeV |
| CODATA['muon'] | 105.6583755 MeV |
| CODATA['tau'] | 1776.86 MeV |
| CODATA['proton'] | 938.27208816 MeV |
| CODATA['neutron'] | 939.56542052 MeV |
| N_e (electron) | 111 |
| k_res (electron) | 42 |
| p, q (electron topology) | -41, 70 |
| α_GUT (in solver) | 1/63.0776276 |
| b₁, b₂, b₃ | 41/6, -19/6, -7 |
| mp.dps | 50 |

---

## Formula Summary (Key Expressions)

- **Z₁:** M_P_MeV/(4√π) · exp(i·2π/φ²)  
- **X₀:** |Re(Z₁)|  
- **X_n:** X₀·φ^{−n}  
- **π_n:** n·sin(π/n)  
- **Route A prefactor:** 2·π_N/φ^{N_e}  
- **η_QED:** 1 − α_EM/(2π)  
- **C_target:** m_e_CODATA / (M_P_MeV · prefactor · η_QED)  
- **h1:** 1/(1+m̄²)  
- **h2:** 1/(1+m̄²)²  
- **η_ψ:** (4 α₃)/(6 π²)  
- **α_EM from flow:** α₁ α₂ / (α₁+α₂)  
- **sin²θ_W:** α₁/(α₁+α₂)  
- **Lambda_lock:** K_bar (at leading order)  
- **ω★:** X_n · ω̄★  

End of inventory.
