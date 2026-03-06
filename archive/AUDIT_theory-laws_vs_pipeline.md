# COMPLETE AUDIT: theory-laws.md vs GU_formation_pipeline.py

**Scope**: Every physics module and formula in theory-laws.md (~7844 lines) checked against GU_formation_pipeline.py.  
**Date**: February 9, 2026.

---

## 1. MODULE INDEX (theory-laws.md line ranges)

| # | Module / Law block | Lines (approx) | Content |
|---|--------------------|----------------|---------|
| 1 | Laws 0–5 | 13–156 | Action, Lagrangian sectors, gauge |
| 2 | Laws 6a–c, 7 | 158–213 | X-dependence m̃², λ̃, γ̃; angular mod (schematic) |
| 3 | Laws 8a–c | 215–241 | Euler-Lagrange (Ω, X, gauge) |
| 4 | Laws 9–13 | 243–318 | SSB cascade, fermionic NLDE, electron soliton, mass = T₀₀, lepton hierarchy |
| 5 | Laws 14–20 | 369–519 | Conventions, Golden Impulse, phase driver, angular series, Route-B theorem, memory proof, radial ODE |
| 6 | Laws 21–26 | 1039–1188 | Resonance N_e=111, Ω-cell, kink/GY, SU(5), epoch map, forbidden constructions |
| 7 | Laws 27–32 | 1190–1320 | Four primitives, memory ODE, V_e at 111, static kink, Jackiw-Rebbi, memory energy Gamma |
| 8 | Laws 33–38 | 1322–1538 | Route-A closure, Route-B GY, three μ scales, lepton hierarchy explicit, classification, 50-digit values |
| 9 | 10-step NLDE derivation | 2099–2340 | L_Ψ, radial ODEs, S(r;X_e), energy E_sol, C_e definition |
| 10 | 10-step Ω-sector | 2352–2560 | Vortex, phase-driver, angular lock, harmonic m*, energy decomposition |
| 11 | FRG 10-step | 2564–3200 | Wetterich, heat kernel, ω_target dimensions, NLDE with FRG coeffs |
| 12 | Recursion-closure route | 3232–3550 | ω_e, X_e from recursion, strong-lock C_e |
| 13 | No-hidden-choices (NHC) | 3562–5200 | L_e, Ω_eff, radial ODEs, Poisson, lock W(ρ̂,σ̂), **6-term H(x)**, ℓ_ab, w_ab |
| 14 | Formation anchor + pipeline | 5398–6010 | Z₁, X₀, X_e, FRG modules §0–§7, lock closure |
| 15 | §FRG-1, §GAUGE, §LOCK | 6153–6465 | FRG flow, gauge X-dependence, K(X), Λ_lock, ω★(X) |
| 16 | §EVAL-1 through §EVAL-8 | 6475–7010 | Litim, Dirac traces, β_m, β_λ_S,V, gauge b_i, **K̄/ω̄★ beta**, UV ICs, 10-ODE system |
| 17 | §QCD (§QCD-1–§QCD-10) | 6995–7340 | QCD epoch, chiral 4-quark, hadronization, U^χ_k flow, meson/baryon masses |
| 18 | Steps 6A–6D, parameter list | 7188–7380 | Canonical norm, dimensionless BVP, quartic-to-1, μ, β, α |
| 19 | Summary audit chain | 7370–7844 | NHC steps, 6-term H, lock decomposition, GU-must-fix list |

---

## 2. LOCK SECTOR: EXACT FORMULAS vs PIPELINE

### 2.1 ℓ_ab (lock-weight polynomial)

**theory-laws.md**  
- **Lines 5332–5342, 5196–5202, 6222–6246**:  
  - `W_lock(ρ,σ) = ℓ₀₀ + ℓ₁₀ρ + ℓ₀₁σ + ℓ₂₀ρ² + ℓ₁₁ρσ + ℓ₀₂σ²`  
  - `U_X^lock(ρ,σ,θ) = Σ_{a+b≥1} ℓ_ab(X) ρ^a σ^b · V_X(θ)`  
  - Beta: `∂_t ℓ_ab(X) = (1/(a!b!)) ∂_ρ^a ∂_σ^b (∂_t U_X^lock)|_{ρ=σ=0}`  

**Pipeline**  
- **Implemented**: Lock weight in NLDE BVP is a quadratic polynomial in (ρ,σ) with configurable coefficients (`lock_coeffs`: l00, l10, l01, l20, l11, l02) — see `solve_nlde_bvp` (lines 671–719, 718–723, 724–729).  
- **Missing**: No FRG projection for ℓ_ab; no flow ∂_t ℓ_ab. Coefficients are not read from FRG; default is W_lock = ½σ² (l02=0.5, others 0). Pipeline comment (lines 1549–1552): “Determine lock ℓ_ab coefficients from FRG lock-sector projection.”

### 2.2 K̄ (phase stiffness) beta function

**theory-laws.md**  
- **Lines 6328–6335, 6768–6777, 6916–6918**:  
  - `K(X) = Z_χ(X) · R₀²(X)`  
  - `∂_t K̄ = (η_χ + 2 ∂_t ln R̄₀) K̄`  
  - Λ̄_lock(X) = K̄(X) × activation  

**Pipeline**  
- **Implemented**: K̄ is in the state vector and flowed (`K_bar` in `frg_beta_functions` and `solve_frg_flow`).  
- **Missing**: Beta for K̄ is set to **zero** (lines 341–342: `beta_K = mpf('0')`). So K̄ is constant from UV IC (1.0), not the full formula (η_χ + 2 ∂_t ln R̄₀) K̄.

### 2.3 ω̄★ (target frequency) beta function

**theory-laws.md**  
- **Lines 6340–6343, 6784–6793, 6919–6921**:  
  - `ω★(X) = X · ω̄★(X)`  
  - `∂_t ω̄★ = β_ω(X, all couplings)`; at leading order ω̄★ ≈ const.  

**Pipeline**  
- **Implemented**: ω̄★ is in the state vector (`omega_bar_star`), and `target_frequency(X_n, omega_bar_star)` implements ω★(X) = X · ω̄★.  
- **Missing**: Beta for ω̄★ is **zero** (line 342: `beta_omega_star = mpf('0')`). So ω̄★ is constant (0.8 from IC), not from β_ω projection.

---

## 3. NLDE BVP: ALL 6 TERMS OF H(x)

**theory-laws.md**  
- **Lines 5579–5598, 4783–4797, 7776–7782**:  
  Vacuum-subtracted Hamiltonian density (6 terms):

  ```
  H = H_kin + H_mass + H_self + H_EM,int + H_EM,field + H_lock

  H_kin      = Ψ†(−iα·∇)Ψ           [Dirac kinetic]
  H_mass     = m★(X_e) σ              [linear mass]
  H_self     = W_self(ρ,σ;X_e)        [self-interaction potential]
  H_EM,int   = q Φ ρ                   [Coulomb interaction]
  H_EM,field = (1/(2g_EM)) |∇Φ|²     [EM field energy]
  H_lock     = (κ_lock(X_e)/2) W_lock(ρ,σ;X_e) Δ²
  ```

  With ρ = u²+v², σ = u²−v², Δ = (ω−qΦ) − ω★(X_e).  
  Radial form: H_kin = (1/x²)(G D₂F − F D₀G), H_lin = m̂ σ̂ + Φ ρ̂, H_nl = (κ₄/2)σ̂² + (β/3)σ̂³, H_EM = (1/(2α))Φ'², H_lock = (κ_lock/2) W(ρ̂,σ̂) Δ_ε².

**Pipeline**  
- **Implemented**:  
  - Radial NLDE (u,v) with M_eff, E_eff, lock Σ_lock and Π_lock (scalar/vector channels).  
  - Poisson for Φ; lock term in ODEs and in energy (E_lock computed as 4π ∫ (κ_lock/2) W_lock Δ² dr).  
- **Gaps**:  
  - No explicit split of E_rest into H_kin, H_mass, H_self, H_EM,int, H_EM,field, H_lock; only ε + E_lock is used for total energy.  
  - H_EM,field (Φ'²) is not explicitly added to the energy functional in the code (Poisson is solved but field energy term not in the documented 6-term sum in one place).

---

## 4. MASS FORMULA: EXACT PREFACTOR PER PARTICLE

**theory-laws.md**  
- **Electron (Route A)**: Lines 1322–1340 — `m_e = M_P · (2π/φ^111) · C_e(ν) · η_QED`; C_e(ν) = |δ_e|K(ν) + η_μ(ν)(ν/2) − (λ_rec/β)κ(ν)/3 + α/(2π).  
- **Electron (Route B)**: Lines 1342–1360 — `m_e c² = E_P · (2π φ^{−111}) · G_e · (2μ) · C_GY(μ)`; G_e = √(5/3), C_GY(μ) = √{[μ+sinh μ]/[sinh μ(cosh μ+1)]}.  
- **Lepton hierarchy**: Lines 1362–1386, 258–278 — `m_i = M_P · (2π C_i / φ^{N_i}) · η_QED`; m_μ/m_e = (C_μ/C_e)·φ^{11}, m_τ/m_e = (C_τ/C_e)·φ^{17}.  
- **Hadrons**: Lines 279–300 — m_p/m_e ≈ φ^16 · C_p/C_e; neutron = proton + isospin splitting.

**Pipeline**  
- **Implemented**:  
  - Route A: `electron_mass_route_A()` with prefactor 2π_N/φ^N_e, C_e(ν) with K(ν), E(ν), η_μ, κ(ν), closure on ν.  
  - Route B: G_e = √(5/3) and C_GY appear in comments/law references; no separate Route-B mass function that returns m_e from μ.  
  - `compute_all_masses()`: electron from Route A; muon/tau/proton from hierarchy with φ^{ΔN} and C_ratio from CODATA; neutron = proton + (m_n−m_p)_CODATA.  
- **Gaps**:  
  - Route B: no function that takes μ (or μ_self-consistent) and returns m_e = E_P·(2π φ^{−111})·G_e·(2μ)·C_GY(μ)·η_QED.  
  - C_μ/C_e and C_τ/C_e are taken from CODATA (inverse: C_ratio = CODATA/m_e/φ^{ΔN}), not from NLDE at each epoch.

---

## 5. ROUTE A (ELLIPTIC) vs ROUTE B (GEL'FAND–YAGLOM)

### 5.1 Route A — elliptic integral closure

**theory-laws.md**  
- **Lines 1322–1340, 1233–1240**:  
  - C_e(ν) = |δ_e|·K(ν) + η_μ(ν)·(ν/2) − (λ_rec/β)·κ(ν)/3 + α/(2π).  
  - K(ν), E(ν) complete elliptic; κ(ν) elliptic kappa; η_μ(ν) modular correction.  
  - Closure: C_e(ν) = C_e^{target}; ν ≈ 0.82054.  
  - 4K(ν) = μ · l_Ω (μ_closure = 4K(ν)/l_Ω).

**Pipeline**  
- **Implemented**: `electron_mass_route_A()` uses ellipk, ellipe, and a C_e_full(nu) with term1 (|δ_e| K), term2 (η_μ (ν/2)), term3 (−y_e κ/3), term4 (E_gauge).  
- **Gap**: η_μ(ν) in pipeline is built from (2π/l_Ω)²(K/π)² + E/K + (ν−1) (lines 207–210); theory also gives “modular correction from Pöschl–Teller” — consistency with theory wording to be confirmed. λ_rec/β = y_e = e^φ/π² is used.

### 5.2 Route B — Gel'fand–Yaglom closure

**theory-laws.md**  
- **Lines 1105–1123, 1342–1360**:  
  - det L₋/det L₀ = y₋(+½)/y₀(+½) = [μ+sinh μ]/[sinh μ(cosh μ+1)].  
  - C_GY(μ) = √{[μ+sinh μ]/[sinh μ(cosh μ+1)]}.  
  - m_e c² = E_P · (2π φ^{−111}) · G_e · (2μ) · C_GY(μ) (C_mem=1).  
  - μ_self-consistent ≈ 0.4192 from C_e(μ) = C_e^{target}.

**Pipeline**  
- **Implemented**: G_e = √(5/3) in comments and structure; no dedicated Route-B routine that computes C_GY(μ) and m_e from μ.  
- **Missing**:  
  - Function C_GY(μ) = √((μ+sinh μ)/(sinh μ(cosh μ+1))).  
  - Function that solves G_e·(2μ)·C_GY(μ) = C_e^{target} for μ and returns m_e.  
  - No explicit “Route B mass” entry point.

---

## 6. sin²θ_W CORRECTION AND THRESHOLD MATCHING

**theory-laws.md**  
- **Lines 6971–6975, 6310–6314, 6720–6745, 6943–6950**:  
  - sin²θ_W(X_e) = 0.657 from minimal one-loop SU(5) is wrong; GU corrects via X-dependent thresholds at X_EW, X_QCD.  
  - b_i(X) piecewise at X_GUT, X_EW, X_QCD; threshold matching when decoupling W, Z, top, Higgs.

**Pipeline**  
- **Implemented**:  
  - `sin2_theta_W = a1/(a1+a2)` at X_e (lines 584–588).  
  - `gauge_b_coefficients(X_current)` implements piecewise b₁,b₂,b₃ for X_GUT, X_EW, X_QCD (lines 352–388).  
  - Main prints sin²θ_W and notes minimal SU(5) gives wrong value (lines 1391–1394).  
- **Gaps**:  
  - No explicit “threshold matching” step (e.g. matching conditions at X_EW for α_EM, sin²θ_W).  
  - sin²θ_W is not corrected by a dedicated X_EW threshold formula; it is just the running ratio a1/(a1+a2).

---

## 7. QCD MODULE: CHIRAL FLOW, HADRONIZATION

**theory-laws.md**  
- **§QCD-1–§QCD-10 (lines 6995–7340)**:  
  - **§QCD-1**: Epoch trigger at X_QCD (m²_Q, gluon dynamics).  
  - **§QCD-2**: Truncation: gluon + quark + chiral 4-quark λ_S [(Q̄Q)²−(Q̄iγ₅τ⃗Q)²] + diquark λ_Δ.  
  - **§QCD-3**: Projections Z_{A,k}, Z_{Q,k}, m_{Q,k}, g_{s,k}, λ_{S,k}, λ_{Δ,k}.  
  - **§QCD-4**: ∂_t g_s = −(b₀/(16π²)) g_s³, N_f^{eff}(k); ∂_t λ̂_S = (2+2η_Q)λ̂_S − A λ̂_S² − B λ̂_S g_s² − C g_s⁴.  
  - **§QCD-5**: Hadronization scale k★ = X_QCD (λ̂_S critical or m²_{φ,k}→0).  
  - **§QCD-6**: Dynamical hadronization: 4-quark → mesons (σ, π⃗), λ_S ↔ h_k²/m²_φ,k.  
  - **§QCD-7**: Chiral potential flow: ∂_t U^χ_k = k⁵/(12π²)[1/E_σ + 3/E_π − 4N_c N_f/E_ψ].  
  - **§QCD-8**: m²_π = (1/Z_{π,0}) U'(ρ₀), m²_σ = (1/Z_{σ,0})[U'(ρ₀)+2ρ₀ U''(ρ₀)], m_q = h₀ σ₀, f²_π = Z_{φ,0} σ₀².  
  - **§QCD-9**: Baryon masses via diquark bosonization and Faddeev/pole.  
  - **§QCD-10**: m_had = k★ × m̂_had.

**Pipeline**  
- **Not implemented**: No QCD-specific code.  
- **Mentioned**: `gauge_b_coefficients` uses X_QCD for b₃ (confinement region); main (line 1552) says “Implement QCD chiral flow for hadron masses (§QCD module)”.  
- **Missing**: All of §QCD-2–§QCD-10: no chiral 4-quark flow, no hadronization, no U^χ_k flow, no m_π/m_σ/m_q/f_π extraction, no baryon mass.

---

## 8. FORMATION, FRG, AND EVAL SECTIONS

### 8.1 Formation anchor (Z₁, X₀, φ-ladder)

**theory-laws.md**  
- **Laws 15, 25; lines 5398–5435, 5817–5865**:  
  - Z₁ = [M_P/(4√π)] exp(i·2π/φ²), X₀ = |Re(Z₁)|, X_{critical,n} = X₀·φ^{−n}, X_e = X₀·φ^{−111}.

**Pipeline**  
- **Implemented**: `golden_impulse()`, `epoch_scale(X0, n)`, `particle_epoch_table`, resonance scan.

### 8.2 FRG beta functions (§EVAL-3, §EVAL-4, §EVAL-5)

**theory-laws.md**  
- **Lines 6352–6365 (β_m)**, **6388–6445 (β_λ_S, β_λ_V)**, **6652–6692 (gauge b_i)**.  
  - β_m: ∂_t m̄ = −m̄ + (1/π²) λ̄_S m̄/(1+m̄²).  
  - β_λ_S, β_λ_V: explicit Fierz-mixed formulas with h₂(m̄²).  
  - ∂_t α_i = −(b_i/(2π)) α_i², piecewise b_i.

**Pipeline**  
- **Implemented**: `frg_beta_functions()` with mass, lam_S, lam_V, alpha1,2,3, and piecewise `gauge_b_coefficients(X_current)`.

### 8.3 Lock sector in FRG (§EVAL-6)

**theory-laws.md**  
- **Lines 6696–6732**: K̄ flow, Λ̄_lock = K̄×activation, ω̄★ flow β_ω, ℓ̄_ab flow.

**Pipeline**  
- **Implemented**: K̄ and ω̄★ in state; Λ_lock = K_bar at leading order.  
- **Missing**: Actual ∂_t K̄ and ∂_t ω̄★ (set to 0); no ℓ_ab flow.

### 8.4 UV initial conditions (§EVAL-7)

**theory-laws.md**  
- **Lines 6736–6889**: Γ_{X₀} from heat kernel; m̄(X₀), λ̄_S(X₀), α_GUT; (8/3)/α_GUT from 1/α_EM(X_e) and (b₁+b₂)/(2π)·t_e.

**Pipeline**  
- **Implemented**: α_GUT chosen so α_EM(X_e) = CODATA (and `tune_alpha_GUT`); m_bar_0, lam_S_0, lam_V_0, K_bar_0, omega_bar_star_0 fixed; no heat-kernel computation of these.

---

## 9. RADIAL NLDE: ODEs AND BCS

**theory-laws.md**  
- **Law 20 (lines 496–518)**; **NHC Steps 5–7, 31 (lines 4089–4112, 5344–5367)**; **Module §5 (lines 6083–6111)**.  
  - dg/dr − (1/r)g = (m_eff + S_NL + E)·f, df/dr + (1/r)f = (m_eff + S_NL − E)·g (Law 20).  
  - Equivalently u' = (M+E)v, v' + (2/r)v = (M−E)u; Poisson (1/r²)d/dr(r² Φ') = −α ρ + lock back-reaction.  
  - BCs: r=0 — g finite, f=0, Φ'(0)=0; r→∞ — g,f,Φ→0. Normalization: 4π ∫(g²+f²)dr = 1 or ∫(u²+v²)dr = 1 (convention-dependent).

**Pipeline**  
- **Implemented**: `nlde_rhs`, `solve_nlde_bvp` with u,v,Φ, lock (Σ_lock, Π_lock), Poisson, normalization to Q=1, shooting on ε.

---

## 10. CONSTANTS AND COEFFICIENTS (SELECTED)

| Constant / Formula | theory-laws.md | Pipeline |
|-------------------|----------------|----------|
| φ, π, e | Law 14a | phi, mp_pi; e via exp(phi)/pi² for y_e |
| N_e = 111 | Laws 14c, 21 | 111 |
| λ_rec/β = e^φ/π² | Laws 14d, 32 | y_e = exp(phi)/(mp_pi**2) in Route A |
| G_e = √(5/3) | Laws 18, 24 | sqrt(5/3) in comments / structure; not in a single Route-B mass function |
| (p,q) = (−41,70) | Law 22 | p, q = -41, 70 in electron_mass_route_A |
| l_Ω = 374.50 | Law 22 | 2π√(p²+(q/φ)²) |
| η_QED = 1 − α/(2π) | Law 33 | eta_QED = 1 - alpha_em/(2*mp_pi) |
| C_GY(μ) | Law 23 | **Not** implemented as a function |
| μ_self-consistent = 0.4192 | Law 34 | Not computed in code |
| ν = 0.82054 | Law 33 | From findroot in Route A |

---

## 11. NEWER / EASY-TO-MISS SECTIONS

- **6-term H(x) and vacuum-subtracted E_rest (Steps 32–34, 5579–5598, 5344–5376)**: Structure is in the doc; pipeline does not break down E_rest into the six terms explicitly.  
- **Lock back-reaction in Poisson (lines 4360–4375, 6110)**: (1/x²)d/dx(x² Φ') = −γ_EM ρ̄ + γ_EM Λ̄_lock W̄_lock Δ̄. Pipeline Poisson is −α ρ (and lock in ODEs); back-reaction in Poisson not clearly present.  
- **W_self vs W_lock and ℓ_ab ≠ w_ab (lines 5332–5342, 5196–5202)**: Doc stresses ℓ_ab as separate polynomial from w_ab. Pipeline uses one lock polynomial (W_lock); no separate w_ab self-interaction polynomial in the energy beyond the simple Soler-type terms in the ODE.  
- **Quartic-to-1 and μ = √(4π/|λ_{4,c}|) (Steps 6D, 7244–7280)**: Doc fixes μ by |g₄|=1. Pipeline uses m_hat=1 and does not implement quartic-to-1 rescaling or μ from λ_{4,c}.  
- **10-coupling state vector (y with Λ̄_lock, Z̄_ψ) (lines 6890–6892, 6910–6935)**: Doc has 10 couplings including Λ̄_lock, Z̄_ψ. Pipeline uses 8 (m_bar, lam_S, lam_V, alpha1,2,3, K_bar, omega_bar_star); no Λ̄_lock or Z̄_ψ as separate state.

---

## 12. SUMMARY: IMPLEMENTED vs MISSING

### Implemented

- Formation: Z₁, X₀, φ-ladder, resonance, particle table.  
- Mass: Route A (elliptic closure), hierarchy formula, compute_all_masses (electron, μ, τ, p, n).  
- FRG: 8 coupled ODEs (m̄, λ̄_S, λ̄_V, α₁,α₂,α₃, K̄, ω̄★), piecewise b_i(X), α_GUT tuning for α_EM(X_e).  
- NLDE: Radial BVP with u,v,Φ, lock polynomial W_lock(ρ,σ), Σ_lock/Π_lock, Poisson, normalization, E_lock, C_e.  
- Gauge: SU(5) matching structure, sin²θ_W from a1/(a1+a2).  
- Lock helpers: phase_stiffness, lock_strength, target_frequency, cosine_series_curvature (formulas only; no FRG-driven Z_χ, R₀, ω̄★).

### Missing or incomplete

- **Lock sector**: ∂_t ℓ_ab (FRG projection for lock-weight polynomial); ∂_t K̄ = (η_χ + 2 ∂_t ln R̄₀) K̄; ∂_t ω̄★ = β_ω.  
- **NLDE energy**: Explicit 6-term H(x) decomposition and H_EM,field in the energy integral; lock back-reaction term in Poisson.  
- **Route B**: C_GY(μ), solution of G_e·(2μ)·C_GY(μ) = C_e^{target}, and a single “Route B electron mass” function.  
- **sin²θ_W**: Explicit X_EW threshold matching to correct sin²θ_W.  
- **QCD**: Full §QCD module (chiral 4-quark flow, hadronization, U^χ_k flow, m_π, m_σ, m_q, f_π, baryon masses).  
- **Quartic-to-1**: μ = √(4π/|λ_{4,c}|) and dimensionless BVP in μ-rescaled variables.  
- **C_μ, C_τ**: From NLDE at N_μ, N_τ instead of inverting CODATA.

---

*End of audit. All line references are to theory-laws.md unless stated otherwise.*
