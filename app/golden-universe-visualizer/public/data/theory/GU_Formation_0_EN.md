# Golden Universe Formation 0 — Slow-Roll Cosmology Derivation

> **Translated from Romanian original**: `source_documents/GU Formation 0.docx`
>
> This document works through the cosmological closure of the Golden Universe theory: connecting the Cosmic Clock field $X$ to slow-roll inflation, Friedmann equations, reheating, and the quark-gluon plasma epoch. It identifies what exists in the GU Formation document and derives the missing cosmological equations.

---

## 1. What Type of Inflation Model Is GU?

The GU document does not specify an explicit slow-roll inflaton $\phi$ with a potential $V(\phi)$ and Friedmann/slow-roll equations. Instead, it describes an "algorithm" in modules (RGE → QCD lattice → nuclear → atomic) with **epoch-dependent laws/constants** ($\pi_n, \varphi_n$), a "cosmic clock" $X_n$ that decreases across epochs, and a **memory term** $L_{\text{mem}}$.

### Mapping to Slow-Roll

The most natural approach is to treat the "cosmic clock" $X$ as an **effective scalar field** (a modulus/clock field) that **rolls slowly**. The scaling

$$X_n = X_0 \, \varphi^{-n}$$

resembles an **exponential evolution** in the "time" $n$.

This best fits **plateau-type models** (Starobinsky / $\alpha$-attractors) or a **nearly exponential potential** for a canonicalized field $\chi$:

- **Plateau (very good for small $r$):**

$$V(\chi) = V_0 \left(1 - e^{-k\chi/M_{pl}}\right)^2$$

- **Exponential (rolling clock / scaling):**

$$V(\chi) = V_0 \, e^{-\lambda\chi/M_{pl}}$$

With a simple mapping between "clock" and field:

$$X(\chi) = X_0 \, e^{-\lambda\chi/M_{pl}} \Rightarrow \ln\frac{X}{X_0} = -\lambda\chi/M_{pl}$$

which closely mimics an $X$ that decreases multiplicatively across epochs.

### Why Not "False-Vacuum Bubbles"?

The GU document contains no **tunneling** mechanism between vacua (Coleman–De Luccia), rates $\Gamma$, bubble walls, etc. Instead, the idea of **flow/refinement** of laws with epoch appears — this is more compatible with a **rolling field** (slow-roll) than with "bubbles" from a false vacuum.

---

## 2. What Is Missing for Complete Slow-Roll Inflation

### What Already Exists in the GU Document

- A **clock field** discretized into epochs: $X_{111} = X_0 \cdot \varphi^{-111}$
- The idea that "cooling of the universe" is "evolution of $X$" and drives the phases/epochs
- A **memory term** $L_{\text{mem}}$ / kernel that must be included in the total Lagrangian and is essential for self-consistency (nonlocality)
- The connection that **temperature** relates to "cosmic clock $X$" (but without an explicit formula)

### Missing Equations (Minimum Set to Close the Theory)

**1) Gravity sector + FRW background**

Must explicitly state working on a background:

$$ds^2 = -dt^2 + a(t)^2 d\vec{x}^2, \quad H = \dot{a}/a$$

and the Einstein/Friedmann equations (linking $H$ to field energy).

**2) Continuous dynamics for "clock field" (not just discrete $X_n$)**

Currently there is only $X_n$ on "ticks". For slow-roll, a continuous field is needed (e.g., $X(t)$ or a canonicalized variable $\chi(t)$) with equation of motion:

$$(standard, \; local): \quad \ddot{\chi} + 3H\dot{\chi} + U'(\chi) = 0$$

The **kinetic term** and **potential** (plateau energy) producing $p \simeq -\rho$ must be specified.

**3) Inflaton potential $U(\chi)$ (plateau / hilltop / etc.)**

No $U(\chi)$ or cosmological $V(\phi)$ exists explicitly in the document — only mass formulas and epochs. For slow-roll, a potential must be chosen/derived and shown to be sufficiently flat:

$$\epsilon_V = \frac{M_{pl}^2}{2}\left(\frac{U'}{U}\right)^2 \ll 1, \quad \eta_V = M_{pl}^2 \frac{U''}{U} \ll 1$$

**4) Link $X \leftrightarrow$ time $\leftrightarrow$ scale (how $X$ evolves with expansion)**

The document mentions that temperature is linked to $X$, but the functional relationship $T(X)$ or $X(a)$ is missing.

For example, something like:

$$\frac{d\ln X}{dN} = f(X) \quad \text{where } N = \ln a$$

to connect "ticks" with e-folds / physical time.

**5) Exit from inflation + reheating (for the plasma to appear)**

To reach "plasma" (hot big bang), a **reheating** mechanism is missing:

$$\dot{\rho}_\chi + 3H(\rho_\chi + p_\chi) = -\Gamma \, \rho_\chi, \quad \dot{\rho}_r + 4H\rho_r = +\Gamma \, \rho_\chi$$

This is the mathematical step that transforms potential energy (slow-roll) into radiation/particles.

**6) How $L_{\text{mem}}$ enters cosmology (not just hadron/nucleus)**

In the document, $L_{\text{mem}}$ is critical for bound states and self-consistency, but it is not derived how it modifies:

- the energy-momentum $T_{\mu\nu}$,
- the clock-field equation of motion (which would become **integro-differential**, non-Markov):

$$\ddot{\chi} + 3H\dot{\chi} + U'(\chi) + \int^t K(t-t') \, \chi(t') \, dt' = 0$$

(This would directly link "nonlocal memory" to slow-roll cosmology.)

**7) (For observational comparison) perturbation equations**

To connect to $n_s$, $r$, $A_s$, the standard perturbation set (Mukhanov–Sasaki / slow-roll formulas) is needed.

### Summary of Missing Structural Elements

1. $a(t), H(t)$ (Friedmann) + source $T_{\mu\nu}$
2. **Continuous dynamics for $X$** (field + plateau potential)
3. **An explicit bridge** between "epochs $n$ / clock $X$" and **time/temperature/reheating** (for the plasma to appear)

---

## 3. What Already Exists in "The Golden Universe Formation"

The skeleton for slow-roll already exists, but only the **field part** $X$ (driver), not the complete "cosmological package" (with $a(t)$, $H$, Friedmann, reheating).

### Total Lagrangian

$$L_{\text{total}} = L_\Omega + L_X + L_{\text{int}} + L_{\text{mem}}$$

### Driver Sector (Clock Field)

$$L_X = \frac{1}{2}(\partial_\mu X)(\partial^\mu X) - V_X(X)$$

The document explicitly states that $V_X(X)$ "provides the gentle slope" that **drives the slow roll** of $X$.

### Local Coupling with the Substrate

$$L_{\text{int}} = -g_{\Omega X}(X) \, S_{\text{coupling}}(\Omega) \, X$$

### Memory Term (Non-Local in Time)

$$L_{\text{mem}} = -\lambda_{\text{rec}}(X) \, S_{\text{mem}}(\Omega(t)) \int_0^t G(X;t,\tau) \, H[\Omega(\tau)] \, d\tau$$

with kernel:

$$G(X;t,\tau) = e^{-\beta(X)(t-\tau)}$$

### Initial Condition for $X$ from $Z_1$ + the "Roll" Concept

$$X(0) = \mathfrak{R}(Z_1) = |Z_1| \cos\theta, \quad \theta = \frac{2\pi}{\varphi^2}$$

and the equation of motion written in the text:

$$\square X - \frac{\partial V(X)}{\partial X} = 0$$

### Epoch Thresholds ("Ticks")

$$X_{\text{critical},n} = X_0 \, \varphi^{-n}$$

---

## 4. Closing the Cosmological System

### 4A. Gravity + FRW

Add the Einstein–Hilbert term:

$$S = \int d^4x \sqrt{-g} \left[\frac{M_{pl}^2}{2} R + L_{\text{total}}\right]$$

and assume an FRW background:

$$ds^2 = -dt^2 + a(t)^2 \, d\vec{x}^2, \quad H = \frac{\dot{a}}{a}$$

### 4B. Energy + Pressure for Field $X$

For a homogeneous $X(t)$:

$$\rho_X = \frac{1}{2}\dot{X}^2 + V_X(X), \quad p_X = \frac{1}{2}\dot{X}^2 - V_X(X)$$

### 4C. Friedmann Equations (Expansion Background)

If in the inflation epoch $X$ dominates:

$$H^2 = \frac{1}{3M_{pl}^2} \, \rho_{\text{tot}} \approx \frac{1}{3M_{pl}^2}\left(\frac{1}{2}\dot{X}^2 + V_{\text{eff}}\right)$$

$$\dot{H} = -\frac{1}{2M_{pl}^2}\left(\dot{X}^2 + \frac{4}{3}\rho_r + \rho_m\right)$$

where $V_{\text{eff}}$ includes effects from $\Omega$, interaction, and memory.

---

## 5. Complete Equation for $X$ in FRW, with Interaction + Memory

### 5A. Standard Part (from $L_X$)

In FRW, $\square X \rightarrow -(\ddot{X} + 3H\dot{X})$, so the local part becomes:

$$\ddot{X} + 3H\dot{X} + V_X'(X) = \text{(additional forces)}$$

### 5B. Contribution from Interaction $L_{\text{int}}$

From $L_{\text{int}} = -g_{\Omega X}(X) S_{\text{coupling}}(\Omega) X$:

$$F_{\text{int}}(X,\Omega) = \frac{\partial}{\partial X}[g_{\Omega X}(X) S_{\text{coupling}}(\Omega) \, X]$$

### 5C. Contribution from Memory $L_{\text{mem}}$

From the memory Lagrangian:

$$F_{\text{mem}}(t) = \frac{\partial}{\partial X}\left[\lambda_{\text{rec}}(X) S_{\text{mem}}(\Omega(t)) \int_0^t e^{-\beta(X)(t-\tau)} H[\Omega(\tau)] \, d\tau\right]$$

### 5D. Complete (Closed) Equation for the Driver

$$\boxed{\ddot{X} + 3H\dot{X} + V_X'(X) + F_{\text{int}}(X,\Omega) + F_{\text{mem}}(t) = 0}$$

This is the "GU-complete" form of slow-roll: local roll + backreaction (interaction) + history (memory).

---

## 6. Slow-Roll Approximation (Inflationary Regime)

When:

$$\dot{X}^2 \ll V_{\text{eff}}, \quad |\ddot{X}| \ll 3H|\dot{X}|$$

then:

$$H^2 \simeq \frac{V_{\text{eff}}}{3M_{pl}^2}$$

$$3H\dot{X} \simeq -(V_X'(X) + F_{\text{int}} + F_{\text{mem}})$$

### Slow-Roll Parameters

$$\epsilon_V = \frac{M_{pl}^2}{2}\left(\frac{V_X'}{V_X}\right)^2, \quad \eta_V = M_{pl}^2 \frac{V_X''}{V_X}$$

Inflation: $\epsilon_V \ll 1$, $|\eta_V| \ll 1$. Ends when $\epsilon_V \simeq 1$.

### Number of e-Folds

$$N = \int H \, dt \simeq \frac{1}{M_{pl}^2} \int_{X_{end}}^{X_*} \frac{V_X}{V_X'} \, dX$$

### Explicit Link $\chi \leftrightarrow X \leftrightarrow n$

Choose a simple and useful mapping:

$$X(\chi) = X_0 \, e^{-\beta\chi/M_{pl}}$$

which implies:

$$n(\chi) = \frac{\beta}{\ln\varphi}\frac{\chi}{M_{pl}} \Rightarrow \Delta n = 1 \iff \Delta\chi = \frac{\ln\varphi}{\beta} M_{pl}$$

This makes the **ticks** $n$ compatible with a **continuous roll**.

---

## 7. Plateau Potential: Worked Example

### 7.1 Potential Choice

$$V_X(X) = V_0(1 - e^{-X/\mu})^2$$

Inflation occurs at $X \gg \mu$; the field rolls toward a minimum at $X \rightarrow 0$.

### 7.2 Background Equations (FRW + Inflaton)

$$H^2 = \frac{1}{3M_{pl}^2}\left(\frac{1}{2}\dot{X}^2 + V_X(X)\right), \quad \ddot{X} + 3H\dot{X} + V_X'(X) = 0$$

### 7.3 Slow-Roll Parameters, End of Inflation, e-Folds

Derivatives:

$$V_X'(X) = \frac{2V_0}{\mu} \, e^{-X/\mu}(1 - e^{-X/\mu})$$

Parameter:

$$\epsilon_V = \frac{2M_{pl}^2}{\mu^2}\left(\frac{e^{-X/\mu}}{1 - e^{-X/\mu}}\right)^2$$

Inflation ends when $\epsilon_V \simeq 1$:

$$e^{-X_{end}/\mu} = \frac{1}{1 + \sqrt{2} \, M_{pl}/\mu} \Rightarrow X_{end} = \mu \ln(1 + \sqrt{2} \, M_{pl}/\mu)$$

e-Folds:

$$\frac{V_X}{V_X'} = \frac{\mu}{2}(e^{X/\mu} - 1)$$

$$\Rightarrow N = \frac{\mu^2}{2M_{pl}^2}(e^{X_*/\mu} - e^{X_{end}/\mu}) - \frac{\mu}{2M_{pl}^2}(X_* - X_{end})$$

### 7.4 Numerical Closure ($\mu = M_{pl}$, $N = 55$)

**End of inflation** ($\epsilon \simeq 1$):

$$X_{end} \approx 0.881 \, M_{pl}$$

**Horizon exit value for $N = 55$:**

$$X_* \approx 4.756 \, M_{pl}$$

**Slow-roll parameters at $X_*$:**

$$\epsilon_* \approx 1.50 \times 10^{-4}, \quad \eta_* \approx -1.72 \times 10^{-2}$$

Predictions (sanity check):

$$n_s \simeq 1 - 6\epsilon_* + 2\eta_* \approx 0.9647$$
$$r \simeq 16\epsilon_* \approx 0.0024$$

(Very consistent with observational data.)

### 7.5 Fixing the Energy Scale from $A_s$

$$A_s \simeq \frac{1}{24\pi^2 M_{pl}^4}\frac{V_*}{\epsilon_*} \Rightarrow V_0 \approx 7.6 \times 10^{-11} \, M_{pl}^4$$

Inflationary energy scale:

$$V_0^{1/4} \approx 2.95 \times 10^{-3} M_{pl} \approx 7.2 \times 10^{15} \text{ GeV}$$

---

## 8. Reheating: How the Plasma Appears After Slow-Roll

### 8.1 Phenomenological Transfer Equations

$$\dot{\rho}_X + 3H(\rho_X + p_X) = -\Gamma \, \rho_X$$
$$\dot{\rho}_r + 4H\rho_r = +\Gamma \, \rho_X$$

### 8.2 Reheating Temperature

$$T_{reh} \approx \left(\frac{90}{\pi^2 g_*}\right)^{1/4} \sqrt{\Gamma \, M_{pl}}$$

### 8.3 Minimum Condition for QGP

QGP appears when $T \gtrsim 150$–$200$ MeV. Thus it suffices:

$$T_{reh} \gtrsim 0.2 \text{ GeV}$$

With $g_* \sim 100$, this requires an extremely small rate:

$$\Gamma_{\min} \approx 5.4 \times 10^{-20} \text{ GeV}$$

**Almost any reasonable reheating** gives $T_{reh}$ much larger than 0.2 GeV → **QGP is guaranteed** in the thermal history.

---

## 9. Deriving Reheating from $L_{\text{int}}$ (Not "Put by Hand")

GU gives the general coupling form:

$$L_{\text{int}} = -g_{\Omega X}(X) \, S_{\text{coupling}}(\Omega) \, X$$

### 9A. Scalar Channel: $S_{\text{coupling}}(\Omega) \supset \frac{1}{2}\chi^2$

$$L_{\text{int}} \supset -\frac{1}{2} g \, X \, \chi^2 \Rightarrow \Gamma_{X \rightarrow \chi\chi} \simeq \frac{g^2}{32\pi \, m_X}$$

(Here $g$ has dimension of mass.)

### 9B. Fermionic Channel: $S_{\text{coupling}}(\Omega) \supset \bar{\psi}\psi$

$$L_{\text{int}} \supset -y \, X \, \bar{\psi}\psi \Rightarrow \Gamma_{X \rightarrow \bar{\psi}\psi} \simeq \frac{y^2}{8\pi} \, m_X$$

(Here $y$ is dimensionless.)

### 9C. Effective Mass of $X$ After Inflation

At the minimum $X_{\min} = 0$:

$$m_X^2 = V_X''(0) = \frac{2V_0}{\mu^2} \Rightarrow m_X = \sqrt{\frac{2V_0}{\mu^2}}$$

With the worked example: $m_X \approx 3.0 \times 10^{13}$ GeV.

### 9D. Minimum Coupling for QGP

**Fermionic channel:**

$$\Gamma = \frac{y^2}{8\pi} m_X \geq \Gamma_{\min} \Rightarrow y_{\min} \approx 2.1 \times 10^{-16}$$

**Scalar channel:**

$$\Gamma = \frac{g^2}{32\pi m_X} \geq \Gamma_{\min} \Rightarrow g_{\min} \approx 1.28 \times 10^{-2} \text{ GeV}$$

It is "easy" to produce a hot big bang that passes through QGP — incredibly small couplings suffice to reach at least 200 MeV.

---

## 10. Connecting $V_0$ to $Z_1$

### 10A. GU-First Approach

GU gives:

- $|Z_1| = \frac{M_P}{4\sqrt{\pi}}$ (magnitude of initial impulse)
- $\mathfrak{R}(Z_1) \approx -2.264 \times 10^{-9}$ kg
- Interpretation: $\mathfrak{R}(Z_1)$ is the **initial value of the clock field** $X$ and sets the energy scale $\sim 10^{18}$ GeV

The epoch thresholds:

$$X_{\text{critical},n} = X_0 \, \varphi^{-n}, \quad \text{with } X_0 = |\mathfrak{R}(Z_1)|$$

The simplest (without inventing initial volume):

$$V_0 = \alpha \, X_0^4$$

where $\alpha$ is a dimensionless constant (fixed later from $A_s$ or from an internal GU condition). This directly preserves the GU idea: "initial energy (from $Z_1$) is the fuel."

### 10B. Observation-First Approach

Fix $V_0$ from observed scalar fluctuations:

$$A_s \simeq \frac{1}{24\pi^2 M_{pl}^4}\frac{V_*}{\epsilon_*}$$

yielding a typical $V_0$ well below Planck scale ($\sim 10^{16}$ GeV). In GU, reconciliation is natural if:

- $Z_1$ sets the **raw scale**,
- $F_{\text{mem}}$ + $F_{\text{int}}$ can effectively "shape" the slope/plateau so that $V_*$ (at the exit of observable modes) is lower than the initial scale.

---

## 11. QCD Epoch in GU

GU explicitly marks:

- **Pattern k=2 (QCD Epoch, $X \approx X_{QCD}$)**: "gluon-sector dynamics becomes dominant" and confined states (hadrons) form.

In standard thermal terms: after reheating, the universe cools, and in the QCD zone (150–200 MeV) the state is **quark-gluon plasma**, then crossover/hadronization. GU translates this as "when $X$ passes the threshold $X_{QCD}$".

### QGP Timeline

After reheating, in the radiation-dominated era:

$$\rho_r = \frac{\pi^2}{30} g_* T^4, \quad H \simeq 1.66 \sqrt{g_*} \frac{T^2}{M_{pl}}$$

and approximately:

$$t \sim \frac{1}{2H} \propto \frac{M_{pl}}{\sqrt{g_*} \, T^2}$$

At $T \sim 156$ MeV (QCD crossover zone):

$$t(T \sim 0.156 \text{ GeV}) \sim 10^{-5} \text{ s} \approx 10 \, \mu\text{s}$$

This is exactly "a few microseconds" after the Big Bang. In that epoch, QCD matter is **quark-gluon plasma** and behaves as a **fluid** — this is what LHC confirms in the laboratory.

### What LHC Tells Us About QGP

LHC (heavy-ion) shows that QGP behaves as a **nearly perfect fluid** (low viscosity), not a dilute gas. Recent CMS results use correlations with the **Z boson** as a "clean marker" and search for the medium response (wake) produced by an energetic quark — a direct signature of "liquid/soup" behavior.

**Cosmological translation:**
- If the model produces a **hot and thermalized** universe after reheating,
- then **QCD** (not inflation) determines that at $T \gtrsim 155$ MeV matter is deconfined and behaves hydrodynamically (fluid). Slow-roll only needs to deliver *temperature* and *equilibrium*; the "liquid" is a QCD property.

---

## 12. Connecting Ticks to Temperature

### 12.1 Continuous Epoch Definition

From GU thresholds:

$$X_{\text{critical},n} = X_0 \, \varphi^{-n}$$

Define continuously:

$$\boxed{n(X) = \log_\varphi\left(\frac{X_0}{X}\right) = \frac{\ln(X_0/X)}{\ln\varphi}}$$

### 12.2 After Reheating: Radiation-Dominated Universe $\Rightarrow T \propto 1/a$

In the standard regime (after thermalized plasma):

$$T(a) \propto \frac{1}{a}$$

With $N = \ln a$:

$$T(N) = T_{reh} \, e^{-(N - N_{reh})}$$

### 12.3 Key Bridge: How "Clock Ticks" Relate to e-Folds

$$\frac{dn}{dN} = \kappa(N) \quad \text{(in general)}$$

**Minimal closure (simplest, very useful):**

Assume $\kappa \approx$ const over long epochs (RD/MD):

$$\frac{dn}{dN} \approx \kappa = \text{const} \Rightarrow n(N) = n_{reh} + \kappa \, (N - N_{reh})$$

### 12.4 Final Formula: Temperature Directly as Function of Tick $n$

Combining with $T(N)$:

$$\boxed{T(n) = T_{reh} \, \exp\left(-\frac{n - n_{reh}}{\kappa}\right)}$$

In powers of $\varphi$:

$$T(n) = T_{reh} \, \varphi^{-(n-n_{reh})/\kappa_\varphi}, \quad \kappa_\varphi \equiv \kappa / \ln\varphi$$

### 12.5 Calibrating $\kappa$ from Two "Anchors"

Take two points $(n_1, T_1)$, $(n_2, T_2)$ (e.g., recombination and QCD) and solve:

$$\boxed{\kappa = -\frac{n_2 - n_1}{\ln(T_2/T_1)}}$$

**Example (numerical demonstration):**

Using:
- Recombination: $T_{rec} \sim 1$ eV at $n_{rec} \approx 128$
- QCD: $T_{QCD} \sim 0.16$ GeV at $n_{QCD} \approx 95$

$$\kappa_{avg} = \frac{n_{rec} - n_{QCD}}{\ln(T_{QCD}/T_{rec})} = \frac{33}{\ln(0.16/10^{-9})} \approx \frac{33}{18.89} \approx 1.746$$

The **minimal model** reproducing the exact thermal chronology between QCD and recombination:

$$\boxed{T(n) = 0.16 \text{ GeV} \cdot \exp\left(-\frac{n-95}{1.746}\right)}$$

and indeed at $n = 128$ this gives $T \simeq 1$ eV.

---

## 13. Memory Kernel as Local ODE (Key Trick)

### 13.1 Replacing the Memory Integral with an Auxiliary Variable

Define the **memory variable**:

$$M(t) \equiv \int_0^t e^{-\beta(X)(t-\tau)} H[\Omega(\tau)] \, d\tau$$

Then the GU term becomes simply:

$$L_{\text{mem}} = -\lambda_{\text{rec}}(X) \, S_{\text{mem}}(\Omega(t)) \, M(t)$$

Treating $\beta(X)$ as "nearly constant" over a short interval (adiabatic), $M(t)$ satisfies a local ODE:

$$\boxed{\dot{M} = H[\Omega(t)] - \beta(X) \, M}$$

This is enormous: we have eliminated the integral and have a closed differential system.

### 13.2 In e-Fold Time $N = \ln a$

Using $d/dt = H \, d/dN$, denote $X_N \equiv dX/dN$, $M_N \equiv dM/dN$:

**Memory becomes:**

$$\boxed{M_N = \frac{H[\Omega]}{H} - \frac{\beta(X)}{H} \, M}$$

**$X$ equation** (in slow-roll regime, neglecting $X_{NN}$ relative to friction term):

$$\boxed{X_N \simeq -M_{pl}^2 \, \frac{V_X'(X) + F_{\text{int}} + F_{\text{mem}}}{V_{\text{eff}}}}$$

---

## 14. Tick Rate $\kappa(N)$ with Memory Included

GU defines thresholds:

$$X_{\text{critical},n} = X_0 \, \varphi^{-n}, \quad X_0 = |\mathfrak{R}(Z_1)|$$

Define continuously:

$$n(X) = \log_\varphi\left(\frac{X_0}{X}\right)$$

Differentiate:

$$\boxed{\kappa(N) \equiv \frac{dn}{dN} = -\frac{1}{\ln\varphi}\frac{1}{X}\frac{dX}{dN} = \frac{1}{\ln\varphi}\frac{1}{X}(-X_N)}$$

Substituting the slow-roll expression for $X_N$:

$$\boxed{\kappa(N) \simeq \frac{M_{pl}^2}{\ln\varphi} \, \frac{V_X'(X) + F_{\text{int}} + F_{\text{mem}}}{X \, V_{\text{eff}}}}$$

This is the "working formula" showing how **memory** (through $M(N)$) makes $\kappa$ variable → ticks are not uniform "in expansion time" but have *hysteresis / backflow* controlled by memory.

### Temperature Formula When $\kappa$ Is Not Constant

After reheating, in the radiation-dominated regime:

$$\frac{d\ln T}{dN} \simeq -1$$

Combining with $\kappa(N) = dn/dN$:

$$\boxed{\frac{d\ln T}{dn} \simeq -\frac{1}{\kappa(n)}}$$

Integrate:

$$\boxed{\ln\frac{T(n)}{T(n_0)} \simeq -\int_{n_0}^n \frac{dn'}{\kappa(n')}}$$

- If $\kappa$ is constant → recover the simple formula $T(n) = T_0 \, e^{-(n-n_0)/\kappa}$
- If memory is strong in certain epochs → $\kappa(n)$ deforms locally and "shifts" the thresholds (QCD, recombination, etc.) finely

---

## 15. Memory-Corrected $\kappa(n)$ with "Snap" at Thresholds

### 15.1 Decomposition

$$\boxed{\kappa(n) = \kappa_0 + \Delta\kappa(n)} \quad \text{where } \kappa_0 \approx 1.746$$

### 15.2 GU-Friendly Choice for "Snap" at Thresholds

Use the thresholds $X_{\text{critical},n} = X_0 \varphi^{-n}$ and put memory to be strong only near certain epochs (QCD, EW, etc.):

$$\boxed{\Delta\kappa(n) = \sum_{j \in \{\text{EW, QCD, ...}\}} A_j \, \exp\left(-\frac{(n-n_j)^2}{2\sigma_j^2}\right)}$$

- $A_j > 0$: "accelerates" ticks (temperature drops faster with $n$)
- $A_j < 0$: "decelerates" (plateau/delay)
- $\sigma_j$: how "sharp" the transition (snap) is

This is exactly the mechanism by which transitions can be made more **discrete** (as desired in GU) without breaking the global calibration.

### 15.3 Memory Variable Linked to $\kappa$

$$\boxed{\kappa(n) = \kappa_0 (1 + \alpha \, M(n))}$$

with $\alpha$ small (so it's a correction, not a total rewrite).

---

## 16. Final Equation Set (Minimal, Ready to Use)

### Definitions

$$N \equiv \ln a, \quad \frac{d}{dt} = H\frac{d}{dN}$$
$$n(X) = \log_\varphi\left(\frac{X_0}{X}\right) = \frac{\ln(X_0/X)}{\ln\varphi}, \quad X_0 = |\mathfrak{R}(Z_1)|$$
$$\kappa(N) \equiv \frac{dn}{dN} = -\frac{1}{\ln\varphi}\frac{1}{X}\frac{dX}{dN}$$

### Memory (Replaces GU Integral with ODE)

GU kernel: $G = e^{-\beta(X)(t-\tau)}$. Define:

$$M(t) = \int_0^t e^{-\beta(X)(t-\tau)} H[\Omega(\tau)] \, d\tau$$

$\Rightarrow$ local equivalent:

$$\boxed{\dot{M} = H[\Omega(t)] - \beta(X) M}$$

or in $N$:

$$\boxed{M_N = \frac{H[\Omega]}{H} - \frac{\beta(X)}{H} M}$$

### Slow-Roll for $X$ with Interaction + Memory

$$\boxed{X_N \simeq -M_{pl}^2 \, \frac{V_X'(X) + F_{\text{int}}(X,\Omega) + F_{\text{mem}}(X,\Omega,M)}{V_{\text{eff}}(X,\Omega,M)}}$$

where, from GU:

$$F_{\text{int}} = \frac{\partial}{\partial X}[g_{\Omega X}(X) S_{\text{coupling}}(\Omega) X]$$
$$F_{\text{mem}} = \frac{\partial}{\partial X}[\lambda_{\text{rec}}(X) S_{\text{mem}}(\Omega) M]$$

### Friedmann (for $H$)

In inflation:

$$\boxed{3M_{pl}^2 H^2 \simeq V_{\text{eff}}}$$

After reheating (RD):

$$\rho_r = \frac{\pi^2}{30} g_* T^4, \quad H \simeq 1.66 \sqrt{g_*} \frac{T^2}{M_{pl}}$$

### Reheating (for the Plasma to Appear)

$$\boxed{\dot{\rho}_X + 3H(\rho_X + p_X) = -\Gamma\rho_X, \quad \dot{\rho}_r + 4H\rho_r = +\Gamma\rho_X}$$
$$\boxed{T_{reh} \approx \left(\frac{90}{\pi^2 g_*}\right)^{1/4}\sqrt{\Gamma M_{pl}}}$$

QGP condition:

$$\boxed{T_{reh} \gtrsim 0.2 \text{ GeV}}$$

### Temperature Directly as Function of Tick $n$ (with Memory)

After reheating:

$$\frac{d\ln T}{dN} \simeq -1$$

Therefore:

$$\boxed{\frac{d\ln T}{dn} \simeq -\frac{1}{\kappa(n)}} \Rightarrow \boxed{\ln\frac{T(n)}{T(n_0)} \simeq -\int_{n_0}^n \frac{dn'}{\kappa(n')}}$$

---

## 17. Complete Cosmological Chain

The system is local and closed in $(X, M, a)$:

1. **Initialization:** $X(0) = \mathfrak{R}(Z_1)$, so $X_0 = |X(0)|$ (GU calculates $X_0 \approx 0.104 \, E_P$)

2. **Dynamics:** integrate in $N$:

$$X_N \simeq -M_{pl}^2 \frac{V_X' + F_{\text{int}} + F_{\text{mem}}}{V_{\text{eff}}}, \quad M_N = \frac{H[\Omega]}{H} - \frac{\beta(X)}{H} M$$

3. **Tick rate:** $\kappa(N) = dn/dN$ from the formula above

4. **Temperature:** $T(n)$ from the integral $\ln T = -\int dn/\kappa$, calibrated with $n = 95 \leftrightarrow T_{\text{QCD}}$ and $n = 128 \leftrightarrow 1$ eV

### Complete Lane

$$\text{slow-roll} \rightarrow \text{reheating} \rightarrow \text{radiation-dominated cooling} \rightarrow X \text{ crosses } X_{QCD} \rightarrow \text{QGP} \rightarrow \text{hadronization}$$

---

*Translated from the original Romanian working document `GU Formation 0.docx`. All equations preserved exactly.*
