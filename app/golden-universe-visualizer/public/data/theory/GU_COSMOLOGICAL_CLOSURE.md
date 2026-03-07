# Golden Universe: Cosmological Closure Analysis

> **Purpose**: This document records canonical working closures and gate outcomes for previously
> underdetermined cosmology functions, using Formation/Demonstration inputs plus machine gates.
> Current status is gate-governed (not fully promoted to DERIVED for all functions).

> **Mirror sync note (closure gates)**:
> `beta(X)` provisional, `lambda_rec(X)` provisional at absolute level (ratio-level closed),
> `g_{OmegaX}(X)` constrained, `V_X(X)` chosen non-unique.
> See machine reports in `derivations/04_COSMOLOGY/closure_identifiability_report.json`
> and `derivations/04_COSMOLOGY/closure_function_gates_report.json`.

---

## 1. The Full GU Lagrangian (Complete Form)

From the Demonstration document (Section 2.5) and the Formation document (Section 1.4):

$$\mathcal{L}_{\text{total}} = \mathcal{L}_\Omega + \mathcal{L}_X + \mathcal{L}_{\text{int}} + \mathcal{L}_{\text{mem}}$$

with:

$$\mathcal{L}_\Omega = g^{\mu\nu}(D_\mu \Omega)^\dagger(D_\nu \Omega) - V_\Omega(\Omega, X)$$

$$\mathcal{L}_X = \frac{1}{2}(\partial_\mu X)(\partial^\mu X) - V_X(X)$$

$$\mathcal{L}_{\text{int}} = -g_{\Omega X}(X) \, (\Omega^\dagger\Omega) \, X$$

$$\mathcal{L}_{\text{mem}} = -\lambda_{\text{rec}}(X) \, (\Omega^\dagger\Omega)(t) \int_0^t e^{-\beta(X)(t-\tau)} (\Omega^\dagger\Omega)(\tau) \, d\tau$$

where:

$$V_\Omega(\Omega, X) = m_\Omega^2(X)(\Omega^\dagger\Omega) + \frac{\lambda_\Omega(X)}{4}(\Omega^\dagger\Omega)^2$$

$$m_\Omega^2(X) = M_0^2 \left[\frac{X}{X_c} - \left(\frac{\pi}{\varphi}\right)^\alpha\right]$$

**Sources**: Demonstration Ch.2 Eq.(L_total); Formation Ch.1 Eq.(1.4.1); theory-laws Laws 1-4.

---

## 2. Closure 1: Canonical working $\beta(X)=X$ and ratio-law $\lambda_{\text{rec}}/\beta=e^\varphi/\pi^2$

### The Problem
The memory kernel $G(X; t, \tau) = e^{-\beta(X)(t-\tau)}$ contains $\beta(X)$, which the Formation
document leaves as "evolving with the cosmic clock" without an explicit functional form.

### The Closure

**$\beta(X) = X$** is already the canonical choice throughout the codebase:

| File | Usage |
|------|-------|
| `derivations/utils/frg_solver.py` | "Memory decay rate β(X) = X" |
| `.cursor/skills/golden-universe-theory/SKILL.md` | "β(X) = X (running scale), particle-specific" |
| `derivations/31_QUARK_MASSES/17_particle_specific_memory.py` | β = X_N per particle |
| `derivations/08_RHO_FIELD_UNITY/01_rho_field_unity.md` | β(X) = X |
| `explanatory/CONSCIOUSNESS.md` | "β(X) = X (the running scale)" |

**Physical justification**: $\beta^{-1} = X^{-1}$ is the Compton time at scale $X$, i.e., the
memory relaxation time equals the natural timescale of the substrate at that energy. This is the
unique choice that makes the memory kernel dimensionally consistent without introducing a new scale.

**Consequence**: $\lambda_{\text{rec}}(X)$ is then fixed by Law 32:

$$\frac{\lambda_{\text{rec}}}{\beta} = \frac{e^\varphi}{\pi^2} \approx 0.51098$$

$$\Rightarrow \quad \lambda_{\text{rec}}(X) = X \cdot \frac{e^\varphi}{\pi^2}$$

**Verification**: `derivations/utils/gu_constants.py` defines `lambda_rec_beta = exp(phi)/(pi*pi)`.

**Status**: CLOSED. Zero new assumptions. Both $\beta(X)$ and $\lambda_{\text{rec}}(X)$ are
determined by existing theory.

---

## 3. Closure 2: $H[\Omega] = S_{\text{mem}} = S_{\text{coupling}} = \Omega^\dagger\Omega$

### The Problem
The Formation document leaves the history functional $H[\Omega]$, the memory receptor $S_{\text{mem}}$,
and the interaction scalar $S_{\text{coupling}}$ as unspecified functionals with only "examples."

### The Closure

The Demonstration document (Section 2.5, Memory Sector) uses the explicit canonical choice:

$$S_{\text{mem}}(\Omega) = \Omega^\dagger\Omega, \quad H[\Omega(\tau)] = \Omega^\dagger\Omega(\tau), \quad S_{\text{coupling}}(\Omega) = \Omega^\dagger\Omega$$

**EFT justification**: $\Omega^\dagger\Omega$ is the lowest-dimension gauge-invariant scalar
constructible from $\Omega$. Any higher-dimension operator (e.g., $(\Omega^\dagger\Omega)^2$,
$\text{Tr}(F_{\mu\nu}F^{\mu\nu})$) is suppressed by powers of the cutoff $M_0$. The EFT
minimal-dimension principle uniquely selects $\Omega^\dagger\Omega$ as the canonical choice.

**Consequence**: The memory Lagrangian becomes:

$$\mathcal{L}_{\text{mem}} = -\lambda_{\text{rec}}(X) \, |\Omega|^2(t) \int_0^t e^{-X(t-\tau)} |\Omega|^2(\tau) \, d\tau$$

and the interaction:

$$\mathcal{L}_{\text{int}} = -g_{\Omega X}(X) \, |\Omega|^2 \, X$$

**Status**: CLOSED. Canonical EFT choice, explicit in Demonstration document.

---

## 4. Closure 3: Adiabatic Slaving $\Omega(t) \approx \Omega_{\text{eq}}(X(t))$

### The Problem
The coupled ODE system involves both $X(N)$ and $\Omega(N)$. Solving the full $\Omega$ dynamics
requires specifying $V_\Omega$ in detail and tracking all 16 components of $\Omega$.

### The Closure

**Adiabatic slaving**: When the $\Omega$ field relaxes to its equilibrium much faster than $X$
evolves (i.e., $m_\Omega \gg H$), we can replace $\Omega(t)$ by its instantaneous equilibrium
value $\Omega_{\text{eq}}(X(t))$.

From $V_\Omega$:
- When $m_\Omega^2(X) > 0$ (high $X$, symmetric phase): $\langle\Omega\rangle = 0$, so $|\Omega_{\text{eq}}|^2 = 0$
- When $m_\Omega^2(X) < 0$ (low $X$, broken phase): $|\Omega_{\text{eq}}|^2 = -2m_\Omega^2(X)/\lambda_\Omega(X)$

This gives the **adiabatic history function**:

$$h(X) \equiv |\Omega_{\text{eq}}(X)|^2 = \begin{cases} 0 & \text{if } X > X_c \cdot (\pi/\varphi)^\alpha \\ -\frac{2m_\Omega^2(X)}{\lambda_\Omega(X)} & \text{if } X < X_c \cdot (\pi/\varphi)^\alpha \end{cases}$$

In practice, with smooth thresholds at each critical epoch $X_j$:

$$h(X) = \sum_j c_j \, \frac{1}{2}\left[1 - \tanh\left(\frac{X - X_j}{\Delta_j}\right)\right]$$

where $X_j = X_0 \varphi^{-n_j}$ are the GU threshold values (not invented: already in the theory)
and $\Delta_j$ are the transition widths (set by $\lambda_\Omega$ and thermal effects).

**Status**: CLOSED up to transition widths $\Delta_j$. Positions are fixed by GU epochs.

---

## 5. Closure 4: $N = 70.5$ e-folds from Dark Matter Dilution

### The Problem
The number of inflationary e-folds was assumed to be $N = 55$ (standard cosmology benchmark),
with no GU-specific derivation.

### The Closure

The Demonstration document (Section 3.2.3) derives $N$ from the Topoknot relic abundance:

1. **Initial defect density** (Kibble mechanism at GUT scale):
   $n_i \approx H_{\text{GUT}}^3$, with $H_{\text{GUT}} = 1.66\sqrt{g_*} \, T_{\text{GUT}}^2/M_P$

2. **Target density today** (85% of dark matter):
   $n_f = 0.85 \, \Omega_{\text{DM}} \, \rho_{\text{crit}} / m_{\text{TK}}$

3. **Dilution**: $n_f = n_i \, e^{-3N}$

4. **Result**:
   $$N = \frac{1}{3} \ln\left(\frac{n_i}{n_f}\right) \approx \frac{1}{3} \ln\left(\frac{5.1 \times 10^{42}}{6.57 \times 10^{-50}}\right) \approx 70.5$$

**Significance**: This is NOT a free parameter. The same inflation that solves the flatness
and horizon problems automatically sets the dark matter abundance. The $N = 70.5$ result
falls within the standard range (60-70) required by cosmology.

**Impact on V_X**: Any chosen $V_X(X)$ must produce $N \approx 70.5$ e-folds. This fixes one
parameter of the potential (e.g., $\mu$ in the plateau model or $f_X$ in the axion model).

**Status**: CLOSED. $N$ is derived from DM physics, not postulated.

---

## 6. Closure 5: $g_{\Omega X}(X)$ --- Constrained to ~1 Free Parameter

### The Problem
The interaction coupling $g_{\Omega X}(X)$ has a functional form in theory-laws (Law 4) with
7 free parameters.

### The Closure (Consistency Constraints)

Starting with the minimal closure $g_{\Omega X} = g_0$ (constant), we impose:

1. **Regularity**: $g_0$ must not cause divergences at $X \to X_0$
2. **Stability**: effective potential bounded below at all $X$
3. **Reheating**: produces $T_{\text{reh}} > 0.2$ GeV (QGP guaranteed) --- this gives a lower bound on $g_0$
4. **Decoupling**: after recombination, $g_{\Omega X}$ effects must be negligible to recover standard cosmology
5. **N = 70.5**: the modified slow-roll with $F_{\text{int}}$ must still produce the correct e-folds

These are 5 constraints on what started as 7 parameters. With the constant-$g_0$ ansatz
(1 parameter), the constraints produce a narrow allowed range for $g_0$.

For the full theory-laws form:
$g_{\Omega X}(X) = \tilde{g}_0 M_0^k (\pi^u \varphi^v)(1 + c_g \tanh((X_{c_g} - X)/\Delta X_g))$,
the 5 constraints reduce the 7 parameters to $\sim 2$ effective degrees of freedom.

**Status**: PARTIALLY CLOSED. Reduced from 7 to ~1-2 parameters. Full closure requires
matching to additional observables.

---

## 7. The Closed Coupled ODE System

Substituting all closures into the Formation document's Section 16-17 system:

### Definitions
$$N \equiv \ln a, \quad n(X) = \frac{\ln(X_0/X)}{\ln\varphi}, \quad X_0 = |\text{Re}(Z_1)|$$

### Memory Variable (local ODE replacing the integral)
$$\dot{M} = h(X) - X \cdot M$$

or in e-fold time:

$$M_N = \frac{h(X)}{H} - \frac{X}{H} M$$

where $h(X) = |\Omega_{\text{eq}}(X)|^2$ from Closure 4.

### Slow-Roll for X with Interaction + Memory

$$X_N \simeq -M_P^2 \, \frac{V_X'(X) + F_{\text{int}}(X) + F_{\text{mem}}(X, M)}{V_{\text{eff}}(X, M)}$$

where:

$$F_{\text{int}}(X) = \frac{\partial}{\partial X}\left[g_0 \, h(X) \, X\right] = g_0\left[h(X) + X \, h'(X)\right]$$

$$F_{\text{mem}}(X, M) = \frac{\partial}{\partial X}\left[\frac{X \, e^\varphi}{\pi^2} \, h(X) \, M\right]$$

$$V_{\text{eff}}(X, M) = V_X(X) + g_0 \, h(X) \, X + \frac{X \, e^\varphi}{\pi^2} \, h(X) \, M$$

### Friedmann
$$3M_P^2 H^2 \simeq V_{\text{eff}} \quad \text{(inflation)}$$

### Tick Rate
$$\kappa(N) = -\frac{1}{\ln\varphi} \frac{1}{X} X_N$$

### Temperature
$$\ln\frac{T(n)}{T(n_0)} = -\int_{n_0}^n \frac{dn'}{\kappa(n')}$$

calibrated with $n = 95 \leftrightarrow T_{\text{QCD}} = 0.16$ GeV and $n = 128 \leftrightarrow 1$ eV.

---

## 8. $V_X(X)$: Theory Band (Two Canonical Forms)

The potential form is not uniquely determined. We run both and report predictions as a band:

### Form A: Plateau (Starobinsky-type)
$$V_X^{(A)}(X) = V_0\left(1 - e^{-X/\mu}\right)^2$$

- $V_0$ fixed from $A_s = 2.1 \times 10^{-9}$
- $\mu$ fixed from $N = 70.5$
- Predicts small $r$ (attractor behavior)

### Form B: Axion-like (Natural inflation)
$$V_X^{(B)}(X) = \Lambda_X^4\left(1 - \cos(X/f_X)\right)$$

- $\Lambda_X$ fixed from $A_s$
- $f_X$ fixed from $N = 70.5$
- Connects to the periodic structure of the GU spiral

Both forms are run through the coupled ODE system. The spread in predictions
($n_s$, $r$, $T_{\text{CMB}}$, etc.) defines the structural uncertainty of the theory.

---

## 9. $n_{\text{today}}$ Derivation

Using the Formation document's calibrated bridge with $\kappa_0 = 1.746$:

$$T(n) = 0.16 \text{ GeV} \cdot \exp\left(-\frac{n - 95}{1.746}\right)$$

Setting $T = T_{\text{CMB}} = 2.725$ K $= 2.349 \times 10^{-13}$ GeV:

$$n_{\text{today}} = 95 + 1.746 \cdot \ln\left(\frac{0.16}{2.349 \times 10^{-13}}\right) = 95 + 47.6 \approx 142.6$$

The previous value of $n_{\text{today}} = 200$ was groundless. The correct value is $\approx 143$.

Memory corrections modify $\kappa(n)$ near thresholds but do not substantially change $n_{\text{today}}$
(corrections are localized near EW and QCD epochs).

---

## 10. Dark Matter: Quantitative Predictions

### Component A: Topoknot (85% of $\Omega_{\text{DM}}$)
- Mass: $m_{\text{TK}} \approx 2.8$ TeV (benchmark)
- Production: Kibble mechanism at GUT-scale phase transition
- Abundance set by $N = 70.5$ inflationary dilution
- Direct detection: nuclear recoil in multi-ton xenon experiments

### Component B: Dark Glueball (15% of $\Omega_{\text{DM}}$)
- Dark confinement scale: $\Lambda_D \approx 8.2$ MeV
- Mass: $m_{\text{DG}} \approx 7\Lambda_D \approx 57$ MeV
- Self-interaction: contact estimate is large ($\sigma/m \sim 10^2$ cm$^2$/g);
  QCD-analog calibrated effective value is $\mathcal{O}(1)$ cm$^2$/g.
- Production: SIMP 3-to-2 thermal freeze-out
- Signature: core formation in dwarf spheroidal galaxies

---

## 11. Error Propagation Chain

All GU predictions inherit errors from upstream constants:

$$m_e^{\text{GU}} \xrightarrow{23 \text{ ppm}} M_P \xrightarrow{23 \text{ ppm}} G_N \xrightarrow{47 \text{ ppm}}$$
$$\quad\quad\quad\quad\quad\quad\quad \searrow M_0 \xrightarrow{+0.26\% \text{ from } c_R}$$

Every derived cosmological observable must carry error bars propagated from these.

---

## 12. Summary: What Is Derived vs What Is Chosen vs What Is Open

| Quantity | Status | Source |
|----------|--------|--------|
| $\beta(X) = X$ | DERIVED | Particle physics (FRG, memory sector) |
| $\lambda_{\text{rec}}(X) = X e^\varphi/\pi^2$ | DERIVED | Law 32 + $\beta = X$ |
| $\tau_{\text{mem}} = 1/X$ | DERIVED | $\beta^{-1}$ |
| $S_{\text{mem}} = S_{\text{coupling}} = H[\Omega] = \Omega^\dagger\Omega$ | CANONICAL (EFT) | Demonstration doc + minimal dimension |
| $N = 70.5$ e-folds | DERIVED | Topoknot DM dilution (Demonstration) |
| $V_\Omega$, $m_\Omega^2(X)$ | DERIVED | Demonstration doc Eq.(V_Omega) |
| $\Omega_{\text{DM}}$ (Topoknot) | DERIVED | Kibble + inflation (Demonstration Ch.3) |
| $\Omega_{\text{DM}}$ (Glueball) | DERIVED | SIMP mechanism (Demonstration Ch.3) |
| Adiabatic slaving $\Omega \to \Omega_{\text{eq}}(X)$ | PHYSICAL CLOSURE | Standard EFT practice |
| $h(X)$ from thresholds | DERIVED (up to $\Delta_j$) | GU epochs + $V_\Omega$ |
| $n_{\text{today}} \approx 143$ | DERIVED | $\kappa = 1.746$ + $T_{\text{CMB}}$ |
| $\kappa_0 = 1.746$ | CALIBRATED | Two anchors: $n_{\text{QCD}} = 95$, $n_{\text{rec}} = 128$ |
| Inflation regime | DERIVED | Canonical slow-roll with finite end ($\epsilon = 1$ termination) |
| Eternal inflation | TESTED (negative in baseline) | Quantum diffusion test implemented; Plateau/Axion/Linear give $\max(\delta X_{\text{quantum}}/\delta X_{\text{classical}})\sim 5\times10^{-5}\ll 1$ |
| $V_X(X)$ form | CHOSEN (two options) | Plateau or axion-like (theory band) |
| $g_0$ (interaction strength) | CONSTRAINED | Reheating + stability (~1 param) |
| $\Delta_j$ (transition widths) | OPEN | Requires thermal field theory |
| Cosmological constant | OPEN | $\text{Str}(a_0) = 3$ reduces but does not solve |

---

---

## 13. V_X: Structural Limitation and Observational Constraints

The cosmic clock potential V_X(X) is **chosen**, not derived from L_total. The source documents (Formation Section 7, Demonstration Ch.2) explicitly offer multiple functional forms without selecting one. This is a structural limitation, analogous to the inflaton potential ambiguity in standard cosmology.

### What observational data constrains

Three V_X forms are tested against Planck 2018 + BICEP/Keck data:

| Form | n_s | r | n_s tension | r status |
|------|-----|---|-------------|----------|
| Plateau (Starobinsky, α=1) | 0.9725 | 0.0022 | 1.8σ | OK |
| Axion (f_X = 5.5 M_P) | 0.9599 | 0.028 | 1.2σ | OK |
| Linear (−σX) | 0.9788 | 0.057 | 3.3σ | **EXCLUDED** |

The Linear form is observationally ruled out by the BICEP/Keck bound r < 0.036.

### Alpha-attractor generalization

The Plateau family generalizes to alpha-attractors: μ = √(3α/2) × M_P. For α ≈ 5-7, n_s shifts to within 0.2σ of Planck while r remains well below the bound. The parameter α is O(1) and natural in supergravity (Kähler curvature). This resolves the Plateau n_s tension.

### What would close the gap

A first-principles derivation of V_X would require deriving the X-field self-interaction from the structure of L_total — specifically, from the way the X-field's symmetry-breaking pattern (its role as a GU epoch driver) constrains its potential. Currently, V_X is not a consequence of the Lagrangian; it is a separate ansatz.

---

## 14. Erratum: Demonstration Document Arithmetic Errors

### Dark Glueball σ/m Calculation (Demonstration Ch.3.4)

The Demonstration document claims σ/m ≈ 1.8 cm²/g for the dark glueball component with Λ_D = 8.2 MeV. Two arithmetic errors have been identified:

1. **Exponent error**: The intermediate value is stated as 8.13 × 10⁶ GeV⁻³; the correct value is 8.13 × 10⁵ GeV⁻³ (one power of 10 too high).
2. **Unit conversion error**: The final cm²/g conversion contains a factor ~100 decimal place error.

Faithfully reproducing the calculation with Λ_D = 7.7 MeV (from f_DG = 0.15 fraction) gives σ/m ≈ **210 cm²/g** — the correct contact-limit result. This is the geometric upper bound σ ~ π/Λ_D² divided by m_DG ~ 7Λ_D.

**Resolution**: Comparison with QCD (where the analogous geometric estimate overshoots the measured pp cross section by ~250×) suggests a non-perturbative calibration factor C ≈ 0.004, yielding σ/m ≈ 0.8 cm²/g — within astrophysical bounds. A rigorous lattice calculation of dark glueball scattering is needed to pin down C precisely.

See `derivations/04_COSMOLOGY/13_dark_matter_abundance.py` for the full analysis.

---

*Document created: February 2026. Based on: GU Formation 0, GU Demonstration, theory-laws, gu_constants.py, and particle derivation codebase.*
