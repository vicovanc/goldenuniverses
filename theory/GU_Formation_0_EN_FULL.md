# GU Formation 0 — Full English Translation

> Source: `source_documents/GU Formation 0.docx`
> Method: step-by-step chunk translation from `GU_Formation_0_SOURCE_FULL.md`.
> Note: equations/LaTeX are preserved where already present in source markdown.

If you're referring to the PDF you uploaded, **it's not an explicitly specified "slow-roll inflation" model** (no inflaton $\phi$ with a potential $V(\phi)$ appears, nor the Friedmann/slow-roll equations). The document is mainly about the "algorithm" in modules (RGE → QCD lattice → nuclear → atomic) and about the idea of ​​**epoch-dependent laws/constants** ($\pi_{n},\varphi_{n}$) + a "cosmic clock" $X_{n}$ which decreases on epochs and a **memory** term $L_{mem}$.

Golden Universe Theory for the ...

**Then "what type" would it be, if we want to map it to slow-roll?**

In your scheme, it is most natural to treat the "cosmic clock" $X$ as an **effective scalar field** (a module/clock field) that **rolls slowly**. How a type scaling appears in the text

$$X_{n} = X_{0}\text{ }\varphi^{- n}$$

(the idea of "ticks"/epochs), this is more like **exponential evolution** in $n$ "time".

Golden Universe Theory for the ...

This fits best with **plateau-type models** (Starobinsky / $\alpha$-attractors) or a **near-exponential potential** for a canonicalized $\chi$ field of the form:

- **Plateau (very good for** $r$**small):**

> $$V(\chi) = V_{0}\left( 1-e^{- k\chi/M_{pl}} \right)^{2}$$
- **Exponential (rolling clock / scaling):**

> $$V(\chi) = V_{0}\text{ }e^{- \lambda\chi/M_{pl}}$$

And a simple mapping between "clock" and field:

$$X(\chi) = X_{0}\text{ }e^{- \lambda\chi/M_{pl}} \Rightarrow \ln\text{ ⁣}\frac{X}{X_{0}} = - \lambda\chi/M_{pl}$$

which mimics very well an $X$ that decreases multiplicatively over epochs.

**Why no "false-vacuum bubbles" here?**

The **tunneling** type mechanism between the vacuum (Coleman--De Luccia), $\Gamma$ rates, bubble wall, etc. does not appear in the PDF. Instead, the idea of ​​**flow/refinement** of the laws with time appears → this is more compatible with a **rolling field** (slow-roll) than with "bubbles" from a false vacuum.

Golden Universe Theory for the ...

If you tell me exactly what you mean by "What type is he?" (potential: plateau vs hilltop vs exponential) I choose a concrete $V(\chi)$ and write $\epsilon_{V},\eta_{V}$, $N(\chi)$, and what scaling results for $X(\chi)$, so that it is compatible with $X_{n} = X_{0}\varphi^{- n}$.

Golden Universe Theory for the ...
Sources

That's what I mean by slow roll, what equations are we missing

Thought for 39s

In PDF you already have the "ingredients" of *clock field* and *memory*, but you **don't yet have the full cosmological system** to make it *slow-roll inflation* (ie $a(t)$, $H(t)$, a rolling field, and a potential $V$).

**What you already have (from the document)**

- A **clock-field** discretized by epochs: $X_{111} = X_{0} \cdot \varphi^{- 111}$.

> Golden Universe Theory for the ...

- The idea that the "cooling of the universe" is the "evolution of $X$" and drives the phases/epochs.

> Golden Universe Theory for the ...

- A **memory** $L_{mem}$/ kernel term that must be included in the total Lagrangian and is essential for self-consistency (nonlocality).
> Golden Universe Theory for the ...
>
> Golden Universe Theory for the ...

- The link that **temperature** is related to "cosmic clock $X$" (but without the explicit formula).

> Golden Universe Theory for the ...

**What equations are you missing to be "slow-roll" (the minimal set that closes the theory)**

**1) Gravity sector + FRW background**

You must explicitly write that you are working on a background:

$$ds^{2} = - dt^{2} + a(t)^{2}d{\overrightarrow{x}}^{2},H = \dot{a}/a$$

and the Einstein/Friedmann equations (which relate $H$ to the field energy).

**2) Continuous dynamics for "clock field" (not just** $\mathbf{X}_{\mathbf{n}}$**discrete)**
Now you have $X_{n}$ on "ticks". As slow-roll you need a continuous field (e.g. $X(t)$ or a canonical variable $\chi(t)$) with equation of motion:

**(standard, local variant)**

$$\ddot{\chi} + 3H\dot{\chi} + U'(\chi) = 0$$

or directly in $X$ if you canonicalize it. Important: The **kinetic term** and the **potential** ("plateau" energy) that produces $p \simeq - \rho$ must be specified.

**3) Inflaton potential** $\mathbf{U(\chi)}$**(plateau / hilltop / etc.)**

There is no explicit cosmological $U(\chi)$ or $V(\phi)$ in the document --- only mass and epoch formulas. For it to be slow-roll, you have to choose/derive a potential and show that it is flat enough that:

$$\epsilon_{V} = \frac{M_{pl}^{2}}{2}\left( \frac{U'}{U} \right)^{2} \ll 1,\eta_{V} = M_{pl}^{2}\frac{U^{''}}{U} \ll 1$$

**4) Link X ↔ time ↔ scale (how** $\mathbf{X}$**evolves with expansion)**

You mentioned that temperature relates to $X$ , but you are missing the functional relationship $T(X)$ or $X(a)$ .

Golden Universe Theory for the ...
For example you have to choose something like:

$$\frac{d\ln X}{dN} = f(X)\text{where}N = \ln a$$

to connect the "ticks" with e-folds / physical time.

**5) Exit from inflation + reheating (for plasma to appear)**

To reach the "plasma" (hot big bang), you lack a **reheating** mechanism:

$${\dot{\rho}}_{\chi} + 3H(\rho_{\chi} + p_{\chi}) = - \Gamma\text{ }\rho_{\chi},{\dot{\rho}}_{r} + 4H\rho_{r} = + \Gamma\text{ }\rho_{\chi}$$

That's the mathematical step that turns potential energy (slow-roll) into radiation/particles.

**6) How does** $\mathbf{L}_{\mathbf{mem}}$** enter cosmology (not just hadron/nucleus)**

In PDF, $L_{mem}$ is critical for bound states and self-consistency

Golden Universe Theory for the ...
Golden Universe Theory for the ...

, but it is not derived as it modifies:

- momentum-energy $T_{\mu\nu}$,

- the clock-field equation of motion (it would become **integral-differential**, non-Markov),\
  of type:

$$\ddot{\chi} + 3H\dot{\chi} + U'(\chi) + \int_{}^{t}{K(t -}t')\text{ }\chi(t')\text{ }dt' = 0$$

(This would directly tie "nonlocal memory" to slow-roll cosmology.)

**7) (If you want comparison with observations) the perturbation equations**

To bind $n_{s}$, $r$, $A_{s}$, you lack the standard set of perturbations (Mukhanov--Sasaki / slow-roll formulas).

**In short**

**You are missing 3 structural things:**
1. $a(t),H(t)$(Friedmann) + source $T_{\mu\nu}$,

2. **a continuous dynamics for** $X$(field + plateau potential),

3. **an explicit bridge** between "epochs $n$/ clock $X$" and **time/temperature/reheating** (for plasma to appear).

If you want, I propose a minimal "closure" compatible with $X_{n} = X_{0}\varphi^{- n}$

Golden Universe Theory for the ...

: we choose a canonicalization $\chi$ and a plateau-like $U(\chi)$ such that the solution reproduces the multiplicative decrease of $X$ on "ticks", then we add reheating and (optionally) the kernel $L_{mem}$ to the equation of $\chi$.

Sources

We continue with the formulas

Thought for 44s

Perfect --- let's go ahead and "close" the **slow-roll cosmology** part to be compatible with what you already have in the PDF:
- you already have **Cosmic Clock** $X_{n}$ (eg $X_{111} = X_{0}\varphi^{- 111}$)

> Golden Universe Theory for the ...
>
> ,

- you already have the idea that **universe cooling = evolution of** $X$

> Golden Universe Theory for the ...
>
> ,

- and that the **temperature** $T$ is related to $X$ (eg recombination $T \approx 1\text{ eV} \Rightarrow N_{rec} \approx 128$)

> Golden Universe Theory for the ...
>
> ,

- plus you have a **memory kernel** $L_{mem}$ which is the "engine" of self-consistency
> Golden Universe Theory for the ...
>
> and appears as a memory integral $I(x)$ that induces an effective potential $V_{mem}$
>
> Golden Universe Theory for the ...
>
> .

What is missing is the cosmological module that ties all of this to $a(t)$, $H(t)$, slow-roll, and reheating.

**1) Clock-Field Definition (continued)**

In PDF you discreetly:

$$X_{n} = X_{0}\text{ }\varphi^{- n}(\text{ex. }n = 111):contentReference\lbrack oaicite:5\rbrack index = 5$$

We make it continuous by introducing a real $n(t)$:

$$X(t) = X_{0}\text{ }\varphi^{- n(t)}$$
from where:

$$n(t) = - \frac{\ln(X/X_{0})}{\ln\varphi},\dot{n} = - \frac{1}{\ln\varphi}\frac{\dot{X}}{X}$$

(this is the bridge between "ticks" and dynamics).

**2) Cosmological module (gravity + field-clock)**

We take FRW:

$$ds^{2} = - dt^{2} + a(t)^{2}\text{ }d{\overrightarrow{x}}^{2},H = \frac{\dot{a}}{a}$$

Minimum clock field action (in canonical form):

$$S = \int d^{4}x\sqrt{- g}\left\lbrack \frac{M_{pl}^{2}}{2}R - \frac{1}{2}(\partial\chi)^{2} - U(\chi) \right\rbrack + S_{rad} + S_{mem}$$

where $\chi$ is the canonical field associated with $X$ (we relate $\chi$ to $X$ below).

**Basic equations:**
$${H^{2} = \frac{1}{3M_{pl}^{2}}\left( \rho_{\chi}+\rho_{r}+\rho_{m} \right)
}{\dot{H} = - \frac{1}{2M_{pl}^{2}}\left( {\dot{\chi}}^{2}+\frac{4}{3}\rho_{r}+\rho_{m} \right)
}{\rho_{\chi} = \frac{1}{2}{\dot{\chi}}^{2} + U(\chi),p_{\chi} = \frac{1}{2}{\dot{\chi}}^{2} - U(\chi)
}$$

**3) Equation of motion + memory term (nonlocal)**

In the PDF "memory" appears as the integral $I(x)$ which generates an effective potential $V_{mem}$

Golden Universe Theory for the ...

and is presented as essential for stable states

Golden Universe Theory for the ...

.

The minimal (effective) cosmological form is a nonlocal term:
$$S_{mem} = - \frac{1}{2}\int d^{4}x\sqrt{- g}\int d^{4}x'\sqrt{- g'}\text{\:\,}\chi(x)\text{ }K(x,x')\text{ }\chi(x')$$

The variation gives an integro-differential equation:

$$\ddot{\chi} + 3H\dot{\chi} + U'(\chi) + \int_{0}^{t}{\text{ ⁣}d}t'\text{\:\,}K(t,t')\text{ }\chi(t') = 0$$

(in homogeneous regime we reduced the kernel in time; analogous to $I(x)$ from PDF

Golden Universe Theory for the ...

).

**4) Slow-roll (with and without memory)**

The classic conditions:

$${\dot{\chi}}^{2} \ll U(\chi), \mid \ddot{\chi} \mid \ll 3H \mid \dot{\chi} \mid $$

Then:
$$H^{2} \simeq \frac{U}{3M_{pl}^{2}},3H\dot{\chi} \simeq - U'(\chi)$$

With memory, an additional "force" appears:

$$3H\dot{\chi} \simeq - (U'(\chi) + F_{mem}(t)),F_{mem}(t) \equiv \int_{0}^{t}dt'\text{ }K(t,t')\text{ }\chi(t')$$

**5) Slow-roll parameters (for predictions)**

$$\epsilon_{V} = \frac{M_{pl}^{2}}{2}\left( \frac{U'}{U} \right)^{2},\eta_{V} = M_{pl}^{2}\frac{U^{''}}{U}$$

Inflation: $\epsilon_{V} \ll 1$, $\mid \eta_{V} \mid \ll 1$. It ends when $\epsilon_{V} \simeq 1$.

Number of e-folds:

$$N = \int H\text{ }dt \simeq \frac{1}{M_{pl}^{2}}\int_{\chi_{end}}^{\chi}\frac{U}{U'}\text{ }d\chi$$

**6) The explicit link** $\mathbf{\chi \leftrightarrow X \leftrightarrow n}$

We choose a simple and very useful mapping:
$$X(\chi) = X_{0}\text{ }e^{- \beta\chi/M_{pl}}$$

involving:

$$n(\chi) = \frac{\beta}{\ln\varphi}\frac{\chi}{M_{pl}} \Rightarrow \Delta n = 1\text{\:\,} \Longleftrightarrow \text{\:\,}\Delta\chi = \frac{\ln\varphi}{\beta}M_{pl}$$

This makes $n$ **ticks** compatible with a **continuous roll**.

**7) How plasma occurs (reheating)**

After the slow-roll ends, the energy in $U(\chi)$ is transferred into radiation:

$${{\dot{\rho}}_{\chi} + 3H(\rho_{\chi} + p_{\chi}) = - \Gamma\text{ }\rho_{\chi}
}{{\dot{\rho}}_{r} + 4H\rho_{r} = + \Gamma\text{ }\rho_{\chi}
}$$

This is where "plasma" appears (the universe enters the hot phase). Only much later, at QCD temperatures, do you reach QGP.

**8) Deck with "T is linked to X" (Epoch calibration)**
The PDF explicitly says:

- "temperature is related to cosmic clock $X$"

> Golden Universe Theory for the ...
>
> ,

- and for recombination $T \approx 1\text{ eV} \Rightarrow N_{rec} \approx 128$

> Golden Universe Theory for the ...
>
> .

Mathematically, this means that you need to introduce a monotonic function:

$$T = T(X)\text{or}T = T(n)$$

and you calibrate it with anchor points (eg $n \approx 128$ to $T \approx 1\text{ eV}$)
Golden Universe Theory for the ...

.

**If you want, the next step is the choice of** $\mathbf{U(\chi)}$

To be complete, we need to fix a potential shape (plateau / hilltop, etc.) and impose that the solution reproduces $X(t) = X_{0}\varphi^{- n(t)}$ and the calibration $T \leftrightarrow X$.

Tell me what you want to be "natural" in GU:

1. **plateau potential** (small r, very observationally compatible), or

2. **hilltop** (slow-roll near $\chi = 0$, nicely related to "boot-up"),

and I write to you immediately:

- $U(\chi)$,

- $\epsilon(\chi),\eta(\chi)$,
- $N(\chi)$,

- and the explicit relation $n(N)$ (ie how ticks relate to e-folds).

Sources

The Golden Universe Formation.pdf

PDF

But wait isn't there?

Thought for 35s

Yes --- **in "The Golden Universe Formation" there is already the skeleton for slow-roll**, but it's only **the field part** $X$(driver), not the whole "cosmological package" (with $a(t)$, $H$, Friedmann, reheating).

**What's already in the document**

- **The total Lagrangian** is defined as
> $$L_{\text{total}} = L_{\Omega} + L_{X} + L_{\text{int}} + L_{\text{mem}}$$
>
> The Golden Universe Formation

- **Driver Sector**:

> $$L_{X} = \frac{1}{2}(\partial_{\mu}X)(\partial^{\mu}X) - V_{X}(X)$$
>
> and explicitly says that $V_{X}(X)$ "provides the gentle slope" that **drives the slow roll of** $X$.
>
> The Golden Universe Formation

- **The equation of motion for** $X$ is written:

> $$\square X - \frac{\partial V(X)}{\partial X} = 0$$
>
> The Golden Universe Formation

- **Initial condition** for $X$ appears as:
> $$X(t\text{ ⁣} = \text{ ⁣}0) = \mathfrak{R}(Z_{1}) = \mid Z_{1} \mid cos\text{ ⁣}(\frac{2\pi}{\varphi^{2}})$$
>
> and an initial scale $X_{0} \sim 0.104\text{ }E_{P}$ "consistent with the scale of inflation" is estimated.
>
> The Golden Universe Formation

- **Memory** is put directly into the Lagrangian as a non-local term in time, with a kernel of type $e^{- \beta(X)(t - \tau)}$.

> The Golden Universe Formation

**What is still missing to be full "slow-roll inflation" (standard cosmology)**

1. **Explicit coupling to gravity** (the Einstein--Hilbert $\frac{M_{pl}^{2}}{2}R$ term) and assuming an FRW background:

$$ds^{2} = - dt^{2} + a(t)^{2}d{\overrightarrow{x}}^{2},H = \dot{a}/a$$

2. The **Friedmann equations** that relate the expansion to the energy of $X$:

$$H^{2} = \frac{1}{3M_{pl}^{2}}\rho_{X},\rho_{X} = \frac{1}{2}{\dot{X}}^{2} + V_{X}(X)$$
3. **Slow-roll approximations** (which are the ones used practically):

$$H^{2} \simeq \frac{V_{X}}{3M_{pl}^{2}},3H\dot{X} \simeq - V_{X}'(X)$$

4. **Slow-roll parameters** $\epsilon,\eta$+ end condition:

$$\epsilon_{V} = \frac{M_{pl}^{2}}{2}\left( \frac{V'}{V} \right)^{2},\eta_{V} = M_{pl}^{2}\frac{V^{''}}{V},\epsilon_{V} \simeq 1\text{ at end}$$

5. **Reheating** (how the energy in $V_{X}$ becomes plasma/radiation):

$${\dot{\rho}}_{X} + 3H(\rho_{X} + p_{X}) = - \Gamma\rho_{X},{\dot{\rho}}_{r} + 4H\rho_{r} = + \Gamma\rho_{X}$$

6. (In GU) **how concretely** $L_{mem}$ enters the equation of $X$ or the effective energy (ie the exact form of the memory term in EOM/ $T_{\mu\nu}$), not just its description.

If you want, we do the next step directly on your GU text: we choose an explicit form for $V_{X}(X)$(plateau/hilltop) so that it has slow-roll, then we write the **closed system** $\left\{ a(t),H(t),X(t) \right\}$+ how the thresholds $X_{\text{critical},n} = X_{0}\varphi^{- n}$ are mapped to $N = \ln a$.

Sources

please
Thought for 44s

Yes --- in **"The Golden Universe Formation"** you already have the "core" of slow-roll: the clock-field $X$, its potential and the memory term. What we do now is **close the cosmology**: we add gravity (FRW + Friedmann) and write the equations for $a(t)$, $H(t)$, $X(t)$, plus how $L_{\text{int}}$ and $L_{\text{mem}}$ come in.

Below is the complete set.

**1) What you already have in GU (directly from the document)**

**Total Lagrangian**

$$L_{\text{total}} = L_{\Omega} + L_{X} + L_{\text{int}} + L_{\text{mem}}$$

The Golden Universe Formation

**Driver sector (clock-field)**

$$L_{X} = \frac{1}{2}(\partial_{\mu}X)(\partial^{\mu}X) - V_{X}(X)$$

and explicit: $V_{X}(X)$ is the "gentle slope" driving the slow-roll of $X$.
The Golden Universe Formation

**Local coupling to the substrate**

$$L_{\text{int}} = - g_{\Omega X}(X)\text{ }S_{\text{coupling}}(\Omega)\text{ }X$$

The Golden Universe Formation

**Memory term (non-local in time)**

$$L_{\text{mem}} = - \lambda_{\text{rec}}(X)\text{ }S_{\text{mem}}(\Omega(t))\int_{0}^{t}{G(X;t,\tau)\text{ }H\lbrack\Omega(\tau)\rbrack\text{ }d\tau}$$

with kernel:

$$G(X;t,\tau) = e^{- \beta(X)(t - \tau)}$$

The Golden Universe Formation

The Golden Universe Formation
**Initial condition for** $\mathbf{X}$**from** $\mathbf{Z}_{\mathbf{1}}$**+ idea of "roll"**

$$X(0) = \mathfrak{R}(Z_{1}) = \mid Z_{1} \mid cos\theta,\theta = \frac{2\pi}{\varphi^{2}}$$

and the equation of motion written in the text:

$$\square X - \frac{\partial V(X)}{\partial X} = 0$$

The Golden Universe Formation

**The thresholds of the epochs ("ticks")**

$$X_{\text{critical},n} = X_{0}\text{ }\varphi^{- n}$$

The Golden Universe Formation

**2) What do we add to make it *slow-roll inflation* complete (FRW cosmology)**

**(A) Gravity + FRW**
Add the Einstein--Hilbert term (this is not written explicitly in the GU snippet above, but is the standard step to get $H(t)$):

$$S = \int d^{4}x\sqrt{- g}\left\lbrack \frac{M_{pl}^{2}}{2}R+L_{\text{total}} \right\rbrack$$

and assume an FRW background:

$$ds^{2} = - dt^{2} + a(t)^{2}\text{ }d{\overrightarrow{x}}^{2},H = \frac{\dot{a}}{a}$$

**(B) Energy + pressure for the field** $\mathbf{X}$

For a homogeneous $X(t)$:

$$\rho_{X} = \frac{1}{2}{\dot{X}}^{2} + V_{X}(X),p_{X} = \frac{1}{2}{\dot{X}}^{2} - V_{X}(X)$$

**(C) Friedmann equations (expansion background)**

If in the era of inflation $X$ dominates:

$${H^{2} = \frac{1}{3M_{pl}^{2}}\text{ }\rho_{\text{tot}} \approx \frac{1}{3M_{pl}^{2}}\left( \frac{1}{2}{\dot{X}}^{2}+V_{\text{eff}} \right)
}{\dot{H} = - \frac{1}{2M_{pl}^{2}}\left( {\dot{X}}^{2}+\frac{4}{3}\rho_{r}+\rho_{m} \right)
}$$

where $V_{\text{eff}}$ also includes effects from $\Omega$, interaction, and memory (below).

**3) Complete equation for** $\mathbf{X}$**in FRW, with interaction + memory**

**(A) Standard part (from** $\mathbf{L}_{\mathbf{X}}$**)**

In FRW, $\square X \rightarrow - (\ddot{X} + 3H\dot{X})$, so the local part becomes:

$$\ddot{X} + 3H\dot{X} + V_{X}'(X) = \text{(additional forces)}$$

(compatible with the form $\square X - \partial V/\partial X = 0$ from the text)

The Golden Universe Formation

**(B) Contribution from interaction** $\mathbf{L}_{\text{int}}$

From
$$L_{\text{int}} = - g_{\Omega X}(X)S_{\text{coupling}}(\Omega)X$$

results in a term in the equation of $X$:

$$F_{\text{int}}(X,\Omega) = \frac{\partial}{\partial X}\lbrack g_{\Omega X}(X)S_{\text{coupling}}(\Omega)\text{ }X\rbrack$$

The Golden Universe Formation

**(C) Contribution from memory** $\mathbf{L}_{\text{mem}}$

From

$$L_{\text{mem}} = - \lambda_{\text{rec}}(X)S_{\text{mem}}(\Omega(t))\int_{0}^{t}e^{- \beta(X)(t - \tau)}H\lbrack\Omega(\tau)\rbrack\text{ }d\tau$$

you get an effective (schematic) term of the type:

$$F_{\text{mem}}(t) = \frac{\partial}{\partial X}\left\lbrack \lambda_{\text{rec}}(X)S_{\text{mem}}(\Omega(t))\int_{0}^{t}e^{- \beta(X)(t - \tau)}H\lbrack\Omega(\tau)\rbrack\text{ }d\tau \right\rbrack$$

The Golden Universe Formation
**(D) Complete (closed) driver equation**

$$\boxed{\ddot{X} + 3H\dot{X} + V_{X}'(X) + F_{\text{int}}(X,\Omega) + F_{\text{mem}}(t) = 0}$$

This is the "full GU" form of slow-roll: local roll + backreaction (interaction) + history (memory).

**4) Slow-roll approximation (inflationary regime)**

When:

$${\dot{X}}^{2} \ll V_{\text{eff}}, \mid \ddot{X} \mid \ll 3H \mid \dot{X} \mid $$

then:

$${H^{2} \simeq \frac{V_{\text{eff}}}{3M_{pl}^{2}}
}{3H\dot{X} \simeq - (V_{X}'(X) + F_{\text{int}} + F_{\text{mem}})
}$$

**5) Link with "ticks":** $\mathbf{n(X)}$**and thresholds** $\mathbf{\varphi}^{\mathbf{- n}}$
You have the thresholds:

$$X_{\text{critical},n} = X_{0}\varphi^{- n}$$

The Golden Universe Formation

So the continuous definition of epoch:

$$\boxed{n(X) = {\log}_{\varphi}\text{ ⁣}\left( \frac{X_{0}}{X} \right) = \frac{\ln(X_{0}/X)}{\ln\varphi}}$$

When $X(t)$ passes through $X_{\text{critical},n}$, it triggers the phase transition of the substrate $\Omega$ (in the logic of the document).

The Golden Universe Formation

The Golden Universe Formation

**6) (Mandatory next step) Reheat → plasma**

To make the plasma appear "after inflation", you add a phenomenological transfer term:
$${\dot{\rho}}_{X} + 3H(\rho_{X} + p_{X}) = - \Gamma\rho_{X},{\dot{\rho}}_{r} + 4H\rho_{r} = + \Gamma\rho_{X}$$

(this is not yet written as equations in GU; it is the standard piece that closes the cosmology and produces the hot big bang).

**Next step (so as not to be left with** $\mathbf{V}_{\mathbf{X}}$**undefined)**

In GU it is said that $V_{X}(X)$ exists and that it gives "gentle slope"

The Golden Universe Formation

, but **his form is not yet fixed**. In order to be able to calculate $H(t)$, $N$e-folds, and concretely relate $X(t)$ to $\varphi^{- n}$ thresholds, we need to choose/derive a shape for $V_{X}(X)$ (plateau/hilltop/exponential, etc.).

Tell me what you want us to impose as a property:

1. $X$ to decrease almost **exponentially** in $N = \ln a$, or

2. $X$ should decrease so that $\Delta n \approx 1$ corresponds to an almost constant interval of e-folds, or

3. Let $V_{X}$ be a **plateau** (compatible with $r$small).
And I immediately write you $V_{X}(X)$+ $\epsilon,\eta$+ $N(X)$ in closed form.

Sources

Well, it must create the conditions of our universe Physicists have recreated the conditions of the first millisecond of the Universe and discovered new details about the primordial matter. Experiments at the Large Hadron Collider (LHC) at CERN show that the plasma of the early Universe behaved more like a liquid than a gas, writes Phys. The results provide rare information about the quark-gluon plasma, the state of matter that filled the cosmos a few microseconds after the Big Bang.

Thought for 1m 20s

Exactly --- if we take **slow-roll** as the phase that "starts" the Universe, then the model must produce (after inflation) a **hot Big Bang** hot enough that, when it cools naturally, it goes through the **quark-gluon plasma (QGP)** epoch that the LHC recreates in the lab.

Below is the complete "chain" + the formulas that link it directly to QGP.

**1) Slow-roll (inflation) → set of equations (background)**

In our FRW patch:

$${ds^{2} = - dt^{2} + a(t)^{2}d{\overrightarrow{x}}^{2},H = \dot{a}/a
}{H^{2} = \frac{1}{3M_{pl}^{2}}\left( \frac{1}{2}{\dot{X}}^{2} + V_{X}(X) \right)
}{\ddot{X} + 3H\dot{X} + V_{X}'(X) = 0
}$$
Slow-roll:

$$H^{2} \simeq \frac{V_{X}}{3M_{pl}^{2}},3H\dot{X} \simeq - V_{X}'(X)$$

and ends when:

$$\epsilon_{V} = \frac{M_{pl}^{2}}{2}\left( \frac{V_{X}'}{V_{X}} \right)^{2} \simeq 1$$

**2) The missing piece to get to "plasma" (reheat)**

In order for **hot plasma** to appear after slow-roll, a **reheating** mechanism is needed: the energy from $X$ is transferred to radiation/particles.

Standard phenomenological model:

$${{\dot{\rho}}_{X} + 3H(\rho_{X} + p_{X}) = - \Gamma\text{ }\rho_{X}
}{{\dot{\rho}}_{r} + 4H\rho_{r} = + \Gamma\text{ }\rho_{X}
}$$

where $\Gamma$ is the effective decay/transfer rate.
Reheat temperature (approx.):

$$T_{reh}\text{\:\,} \approx \text{\:\,}\left( \frac{90}{\pi^{2}g_{*}} \right)^{1/4}\sqrt{\Gamma\text{ }M_{pl}}$$

**The minimum requirement for QGP** is simple:

$$T_{reh}\text{ } \gtrsim \text{ }\mathcal{O}(200\text{ MeV})$$

(if it's much higher, the more likely you're going through the QGP era on the way to cooling).

**3) After reheating: dominated radiation → time--temperature connection**

In the era dominated by radiation:

$${\rho_{r} = \frac{\pi^{2}}{30}g_{*}T^{4}
}{H \simeq 1.66\text{ }\sqrt{g_{*}}\text{ }\frac{T^{2}}{M_{pl}}
}$$

and approximately:
$$t \sim \frac{1}{2H}\text{ } \propto \text{ }\frac{M_{pl}}{\sqrt{g_{*}}\text{ }T^{2}}$$

(this scaling $H \sim T^{2}/M_{pl}$ is standard in early Universe thermodynamics).

**4) When does QGP appear in the Universe (and why isn't it the "first millisecond")**

Lattice QCD indicates that the transition is a **crossover** at $T_{pc} \approx 156.5$MeV (at $\mu_{B} \approx 0$, relevant for the Universe and for the LHC).

If you put $T \sim 150\text{ ⁣} - \text{ ⁣}200$MeV into the $t \propto T^{- 2}$ relation, you get a cosmic time of order **microseconds--tens of microseconds**, not 1ms. (Popular articles sometimes say "millisecond", but the QGP epoch is, physically, "a few microseconds after the Big Bang".)

**5) What the LHC tells us about QGP and what must "come out" of the model**

LHC (heavy-ion) shows that QGP behaves as a **almost perfect fluid** (low viscosity), not a rare gas --- this is already explicitly stated in the CERN materials.

Recent results (CMS) use correlations with the **Z boson** as a "clean marker" and look for the environmental response (wake) produced by an energetic quark --- a direct signature of "liquid/soup" behavior.

**Cosmological translation:**

- if your model produces a **hot and thermalized** Universe after reheating,
- then **QCD** (not inflation) decides that at $T \gtrsim 155$MeV matter is deconfined and behaves hydrodynamically (fluid).\
  That is: slow-roll only needs to deliver *temperature* and *balance*; "liquid" is a property of QCD.

**6) What concrete conditions do you need to impose in your model**

To "create the conditions of our universe" up to QGP:

1. **Reheating hot enough**

$$T_{reh} > 200\text{ MeV}(\text{practically, it is usually much higher})$$

2. **Fast thermalization** (interactions should be faster than expansion)\
    Intuition: microscopic rates $\Gamma_{int}$ must be $\gg H$ to have fluid/hydrodynamics.

3. **Standard RD evolution** up to $T \sim 155$MeV\
    Then you naturally enter the QGP era and then hadronization (crossover).

If you want, the next step is to fix the **shape of** $V_{X}(X)$ in GU (plateau/hilltop) and choose $\Gamma(X)$ so that we explicitly calculate:
- $N$e-folds,

- $T_{reh}$,

- and the time $t$when you pass through $T_{pc} \approx 156.5$MeV (the QGP epoch).

Okay

Thought for 59s

Great. Then we "freeze" a **slow-roll** model for the GU $X$ field and explicitly link it to **reheating → plasma → QGP**.

**1) We choose a *plateau* type potential for** $\mathbf{X}$

A very good example (gives $r$small and is stable) is:

$$V_{X}(X) = V_{0}(1 - e^{- X/\mu})^{2}$$

Inflation occurs at $X \gg \mu$, and the field runs toward the minimum at $X \rightarrow 0$.
**2) Background equations (FRW + inflaton)**

$${ds^{2} = - dt^{2} + a(t)^{2}d{\overrightarrow{x}}^{2},H = \frac{\dot{a}}{a}
}{H^{2} = \frac{1}{3M_{pl}^{2}}\left( \frac{1}{2}{\dot{X}}^{2} + V_{X}(X) \right)
}{\ddot{X} + 3H\dot{X} + V_{X}'(X) = 0
}$$

**Slow-roll**

$$H^{2} \simeq \frac{V_{X}}{3M_{pl}^{2}},3H\dot{X} \simeq - V_{X}'(X)$$

**3) Slow-roll parameters, end of inflation, e-folds**

Derivatives:

$$V_{X}'(X) = \frac{2V_{0}}{\mu}\text{ }e^{- X/\mu}(1 - e^{- X/\mu})$$

Parameter:

$$\epsilon_{V} = \frac{M_{pl}^{2}}{2}\left( \frac{V'}{V} \right)^{2} = \frac{2M_{pl}^{2}}{\mu^{2}}\left( \frac{e^{- X/\mu}}{1 - e^{- X/\mu}} \right)^{2}$$
Inflation ends when $\epsilon_{V} \simeq 1$, i.e.:

$$e^{- X_{end}/\mu} = \frac{1}{1 + \sqrt{2}\text{ }M_{pl}/\mu} \Rightarrow X_{end} = \mu\ln\text{ ⁣}(1 + \sqrt{2}\text{ }M_{pl}/\mu)$$

Number of e-folds:

$$N \equiv \int H\text{ }dt \simeq \frac{1}{M_{pl}^{2}}\int_{X_{end}}^{X_{*}}\frac{V}{V'}\text{ }dX$$

For the above potential:

$${\frac{V}{V'} = \frac{\mu}{2}(e^{X/\mu} - 1)
}{\Rightarrow N = \frac{\mu^{2}}{2M_{pl}^{2}}(e^{X_{*}/\mu} - e^{X_{end}/\mu}) - \frac{\mu}{2M_{pl}^{2}}(X_{*} - X_{end})
}$$

**4) How do we fix the scale** $\mathbf{V}_{\mathbf{0}}$**(to match our universe)**

From the amplitude of the observed scalar fluctuations:

$$A_{s} \simeq \frac{1}{24\pi^{2}M_{pl}^{4}}\frac{V_{*}}{\epsilon_{*}}$$
That fixes your $V_{0}$ (for a typical $N$ \~ 50--60).

**5) Reheating: how "plasma" appears after slow-roll**

Without that you don't get to the "soup" and therefore not to the QGP either.

Phenomenological equations:

$${{\dot{\rho}}_{X} + 3H(\rho_{X} + p_{X}) = - \Gamma\text{ }\rho_{X}
}{{\dot{\rho}}_{r} + 4H\rho_{r} = + \Gamma\text{ }\rho_{X}
}$$

Reheating temperature:

$$T_{reh} \approx \left( \frac{90}{\pi^{2}g_{*}} \right)^{1/4}\sqrt{\Gamma\text{ }M_{pl}}$$

**Condition for the universe to safely pass through QGP:**

$$T_{reh} \gtrsim 200\text{ MeV}$$
(in practice, many models give much higher $T_{reh}$, so QGP is guaranteed on the cooling path.)

**6) The radiation age and the "QGP moment"**

After reheating, you have dominated radiation:

$$\rho_{r} = \frac{\pi^{2}}{30}g_{*}T^{4},H \simeq 1.66\sqrt{g_{*}}\frac{T^{2}}{M_{pl}}$$

QGP appears when $T$ decreases through the QCD zone ($\sim 150\text{ ⁣} - \text{ ⁣}200$ MeV). Then matter (QCD) behaves hydrodynamically --- the "liquid" that the LHC sees is a property of QCD in that regime; cosmology just needs to get there via a hot Big Bang.

**7) Connection with GU "ticks"** $\mathbf{X}_{\mathbf{n}}\mathbf{=}\mathbf{X}_{\mathbf{0}}\mathbf{\varphi}^{\mathbf{- n}}$

You continuously define:

$$n(X) = {\log}_{\varphi}\text{ ⁣}\left( \frac{X_{0}}{X} \right) = \frac{\ln(X_{0}/X)}{\ln\varphi}$$

and e-fold laws by:

$$\frac{dX}{dN} = \frac{\dot{X}}{H} \simeq - M_{pl}^{2}\frac{V'}{V} \Rightarrow \frac{dn}{dN} = \frac{1}{\ln\varphi}\left( -\frac{1}{X}\frac{dX}{dN} \right)$$
This tells you how many "ticks" $n$ are consumed on a given number of e-folds.

If you want to go further *no questions asked*, the next logical step is:

1. we choose $\mu$ (for example $\mu \sim M_{pl}$ as a realistic plateau),

2. we fix $N = 55$ (standard),

3. we calculate $X_{*}$, $\epsilon_{*}$, then $V_{0}$ from $A_{s}$,

4. we choose $\Gamma$ such that $T_{reh} > 200$MeV (QGP ensured).

Okay

Thought for 1m 54s

Perfect --- then we do **a complete example** (slow-roll → reheating → plasma → QGP), so you can see that the model can really reproduce the "conditions of our Universe".

Below I choose a **plateau potential** for the GU field $X$ and calibrate it to standard values ​​($N = 55$, $A_{s} \simeq 2.1 \times 10^{- 9}$). That automatically gives you a hot Big Bang that goes through QGP.
**1) Slow-roll model for** $\mathbf{X}$

**Potential (plateau)**

$$V_{X}(X) = V_{0}(1 - e^{- X/\mu})^{2}$$

**The background equations (FRW)**

$$H^{2} = \frac{1}{3M_{pl}^{2}}\left( \frac{1}{2}{\dot{X}}^{2} + V_{X}(X) \right),\ddot{X} + 3H\dot{X} + V_{X}'(X) = 0$$

**Slow-roll**

$$H^{2} \simeq \frac{V_{X}}{3M_{pl}^{2}},3H\dot{X} \simeq - V_{X}'(X)$$

**2) Numerical closure (choose** $\mathbf{\mu =}\mathbf{M}_{\mathbf{pl}}$**,** $\mathbf{N = 55}$**)**

**End of inflation** $\mathbf{\epsilon \simeq 1}$

$$\epsilon_{V} = \frac{M_{pl}^{2}}{2}\left( \frac{V'}{V} \right)^{2}$$
Result:

$$X_{end} \approx 0.881\text{ }M_{pl}$$

**The value at "horizon exit" for** $\mathbf{N = 55}$

From the formula of e-folds

$$N \simeq \frac{1}{M_{pl}^{2}}\int_{X_{end}}^{X_{*}}\frac{V}{V'}\text{ }dX$$

output:

$$X_{*} \approx 4.756\text{ }M_{pl}$$

**Slow-roll parameters at** $\mathbf{X}_{\mathbf{*}}$

$$\epsilon_{*} \approx 1.50 \times 10^{- 4},\eta_{*} \approx - 1.72 \times 10^{- 2}$$

Predictions (just as a sanity check):
$${n_{s} \simeq 1 - 6\epsilon_{*} + 2\eta_{*} \approx 0.9647
}{r \simeq 16\epsilon_{*} \approx 0.0024
}$$

(very "ok" compared to what we know observationally).

**3) We fix the energy scale from** $\mathbf{A}_{\mathbf{s}}$**(actual calibration)**

$$A_{s} \simeq \frac{1}{24\pi^{2}M_{pl}^{4}}\frac{V_{*}}{\epsilon_{*}} \Rightarrow V_{0} \approx 7.6 \times 10^{- 11}\text{ }M_{pl}^{4}$$

Inflation Energy Scale:

$$V_{0}^{1/4} \approx 2.95 \times 10^{- 3}M_{pl} \approx 7.2 \times 10^{15}\text{ GeV}$$

**4) Critical part for "plasma": reheating**

Enter the energy transfer from $X$ to radiation:

$${{\dot{\rho}}_{X} + 3H(\rho_{X} + p_{X}) = - \Gamma\rho_{X}
}{{\dot{\rho}}_{r} + 4H\rho_{r} = + \Gamma\rho_{X}
}$$

Reheating temperature:

$$T_{reh} \approx \left( \frac{90}{\pi^{2}g_{*}} \right)^{1/4}\sqrt{\Gamma M_{pl}}$$

**Minimum condition for Universe to go through QGP**

QGP appears when $T \gtrsim 150\text{ ⁣} - \text{ ⁣}200$MeV. So that's enough:

$$T_{reh} \gtrsim 0.2\text{ GeV}$$

With $g_{*} \sim 100$ this means an extremely small rate:

$$\Gamma_{\min} \approx 5.4 \times 10^{- 20}\text{ GeV}$$

That is **almost any reasonable reheating** gives you $T_{reh}$much higher than 0.2 GeV → **QGP is guaranteed** in the thermal history.

**5) When QGP occurs in cosmic time (microseconds)**
After reheating, the Universe is radiation-dominated; the temperature decreases, and at $T \sim 156$MeV (QCD crossover zone) the time is of order:

$$t(T\text{ ⁣} \sim \text{ ⁣}0.156\text{ GeV}) \sim 10^{- 5}\text{ s} \approx 10\text{ }\mu\text{s}$$

That's exactly "a few microseconds" after the Big Bang (not 1 ms).

At that epoch, QCD matter is **quark-gluon plasma** and behaves like a **fluid** (this is what the LHC confirms in the laboratory).

**Next step (to be full GU, not just standard cosmology)**

We need to bind $\Gamma$(reheating) to $L_{\text{int}}$ from GU (eg an explicit coupling $g(X)$ to fields $\chi$, $\psi$), so that it is not a "put" parameter.

If you want, I'll write you exactly:

- a minimal choice of $L_{\text{int}}$ that produces $\Gamma(X)$,

- and we calculate the $T_{reh}$result (and thus the QGP condition) directly from the GU parameters.

K
Thought for 51s

Yes --- in **GU** you already have exactly the "slow-roll" ingredients: the field $X$, the potential $V_{X}(X)$, the coupling $L_{\text{int}}$ and the non-local term $L_{\text{mem}}$.

The Golden Universe Formation

\+ the initial condition and the idea of "slow roll" of $X$ from $X_{0}$ to 0

The Golden Universe Formation

\+ thresholds $X_{\text{critical},n} = X_{0}\varphi^{- n}$.

The Golden Universe Formation

To "create the conditions of our universe" up to plasma/QGP, we just have to **close the cosmological system** and derive the **reheating** from $L_{\text{int}}$.

**1) Closed cosmological system:** $\left\{ \mathbf{a(t),H(t),X(t)} \right\}$

**(a) Add gravity (Einstein--Hilbert)**
$$S = \int d^{4}x\sqrt{- g}(\frac{M_{pl}^{2}}{2}R + L_{\Omega} + L_{X} + L_{int} + L_{mem}),$$

where $L_{X} = \frac{1}{2}(\partial X)^{2} - V_{X}(X)$.

The Golden Universe Formation

**(b) FRW Background**

$$ds^{2} = - dt^{2} + a(t)^{2}d{\overrightarrow{x}}^{2},H = \frac{\dot{a}}{a}.$$

**(c) Friedmann (dominant** $\mathbf{X}$**in inflation)**

$${H^{2} = \frac{1}{3M_{pl}^{2}}\text{ }\rho_{tot} \approx \frac{1}{3M_{pl}^{2}}(\frac{1}{2}{\dot{X}}^{2} + V_{eff}(X,t)),
}{\dot{H} = - \frac{1}{2M_{pl}^{2}}({\dot{X}}^{2} + \frac{4}{3}\rho_{r} + \rho_{m}).
}$$

**(d) Full equation for** $\mathbf{X}$**(local + interaction + memory)**

From GU:
$${L_{int} = - g_{\Omega X}(X)\text{ }S_{coupling}(\Omega)\text{ }X,L_{mem} = - \lambda_{rec}(X)\text{ }S_{mem}(\Omega(t))\int_{0}^{t}{G(X;t,\tau)\text{ }H\lbrack\text{ }d\tau,}
}{G(X;t,\tau) = e^{- \beta(X)(t - \tau)}.
}$$

The Golden Universe Formation

In FRW (homogeneous), $\square X \rightarrow \ddot{X} + 3H\dot{X}$, so:

$$\boxed{\ddot{X} + 3H\dot{X} + V_{X}'(X) + F_{int}(X,\Omega) + F_{mem}(t) = 0}$$

with

$${F_{int} = \frac{\partial}{\partial X}\lbrack g_{\Omega X}(X)\text{ }S_{coupling}(\Omega)\text{ }X\rbrack,
}{F_{mem}(t) = \frac{\partial}{\partial X}\left\lbrack \lambda_{rec}(X)\text{ }S_{mem}(\Omega(t))\int_{0}^{t}e^{- \beta(X)(t - \tau)}H\lbrack\Omega(\tau)\rbrack\text{ }d\tau \right\rbrack.
}$$

**(e) Slow-roll regime (what you want)**

$${{\dot{X}}^{2} \ll V_{eff}, \mid \ddot{X} \mid \ll 3H \mid \dot{X} \mid
}{H^{2} \simeq \frac{V_{eff}}{3M_{pl}^{2}},3H\dot{X} \simeq - (V_{X}'(X) + F_{int} + F_{mem}).
}$$

**2) How do you get plasma (reheating) from** $\mathbf{L}_{\text{int}}$

GU gives you the general form of the $X \leftrightarrow \Omega$ coupling.

The Golden Universe Formation

To make $\Gamma$ computable, you choose a "light" component of $\Omega$ that plays the role of "matter" produced at the end of inflation (schematically: a scalar $\chi$ or a fermion $\psi$).

**Minimum variant 1:** $\mathbf{X \rightarrow \chi\chi}$

You choose

$$S_{coupling}(\Omega) \supset \frac{1}{2}\chi^{2} \Rightarrow L_{int} \supset - \frac{1}{2}g\text{ }X\text{ }\chi^{2}$$

(this is exactly in the spirit of $L_{int} = - g_{\Omega X}S_{coupling}X$).

The Golden Universe Formation
Decay width (for $m_{\chi} \ll m_{X}$):

$$\Gamma_{X \rightarrow \chi\chi} \simeq \frac{g^{2}}{32\pi\text{ }m_{X}}$$

where the effective mass of $X$ after inflation is e

$$m_{X}^{2} = V_{X}^{''}(X_{\min}).$$

**Minimum variant 2:** $\mathbf{X \rightarrow}\overset{ˉ}{\mathbf{\psi}}\mathbf{\psi}$

You choose

$${S_{coupling}(\Omega) \supset \overset{ˉ}{\psi}\psi \Rightarrow L_{int} \supset - y\text{ }X\text{ }\overset{ˉ}{\psi}\psi
}{\Gamma_{X \rightarrow \overset{ˉ}{\psi}\psi} \simeq \frac{y^{2}}{8\pi}\text{ }m_{X}(m_{\psi} \ll m_{X}).
}$$

**3) Reheating → temperature → QGP (the "universe like ours" condition)**

After $X$ begins to decay/transfer energy, you write the energy equations:
$${\dot{\rho}}_{X} + 3H(\rho_{X} + p_{X}) = - \Gamma\text{ }\rho_{X},{\dot{\rho}}_{r} + 4H\rho_{r} = + \Gamma\text{ }\rho_{X}.$$

Reheating temperature:

$$T_{reh} \approx \left( \frac{90}{\pi^{2}g_{*}} \right)^{1/4}\sqrt{\Gamma M_{pl}}.$$

**The minimum condition for the Universe to go through the quark--gluon plasma era** is simply:

$$T_{reh} \gtrsim 0.2\text{ GeV},$$

because then, on cooling, you inevitably go through $T \sim 150\text{ ⁣} - \text{ ⁣}200$MeV (deconfinement/crossover QCD regime).

**4) Link with GU "ticks"**

Thresholds are already in GU:

$$X_{\text{critical},n} = X_{0}\varphi^{- n}.:contentReference\lbrack oaicite:7\rbrack index = 7$$

Useful continuous definition:
$$n(X) = {\log}_{\varphi}\text{ ⁣}(\frac{X_{0}}{X}) = \frac{\ln(X_{0}/X)}{\ln\varphi},$$

and $X_{0}$ is fixed by the initial condition in $Z_{1}$: $X(0) = \mathfrak{R}(Z_{1}) = \mid Z_{1} \mid cos\theta$and $X_{0} = \mid X(0) \mid$.

The Golden Universe Formation

If you say "continue", I do the next step **without further questions**:

1. choose an explicit form $V_{X}(X)$(plateau) compatible with the "gentle slope" in GU

> The Golden Universe Formation
>
> ,

2. calculate $m_{X} = \sqrt{V_{X}^{''}(X_{\min})}$,

3. obtain from $L_{int}$ a $\Gamma$ (depending on $g$ or $y$),

4. impose $T_{reh} > 0.2$GeV and give you **the inequalities on** $g$**/** $y$ that guarantee QGP + full thermal chain.
Sources

Okay

Thought for 1m 23s

Perfect --- then we "close" the GU model so that it gives **slow-roll → reheating → plasma → QGP** using exactly the structure from **The Golden Universe Formation**.

**0) What we fix from GU (already exists)**

In GU you already have:

- $L_{\text{total}} = L_{\Omega} + L_{X} + L_{\text{int}} + L_{\text{mem}}$

> The Golden Universe Formation

- $L_{X} = \frac{1}{2}(\partial X)^{2} - V_{X}(X)$ and even says that $V_{X}$ gives the "gentle slope" for slow-roll

> The Golden Universe Formation
- the local coupling $L_{\text{int}} = - g_{\Omega X}(X)\text{ }S_{\text{coupling}}(\Omega)\text{ }X$

> The Golden Universe Formation

- nonlocal memory $L_{\text{mem}} \propto \int_{0}^{t}{G(X;t,\tau)\text{ }H\lbrack\Omega(\tau)\rbrack d\tau}$ with kernel $G = e^{- \beta(X)(t - \tau)}$

> The Golden Universe Formation

- thresholds of epochs $X_{\text{critical},n} = X_{0}\varphi^{- n}$

> The Golden Universe Formation

- and the fact that the initial energy is set by $\mathfrak{R}(Z_{1})$ (the fuel of evolution)

> The Golden Universe Formation
>
> .

**1) We choose an** $\mathbf{V}_{\mathbf{X}}\mathbf{(X)}$**explicit (plateau) to be slow-roll**
A minimal and "safe" choice:

$$V_{X}(X) = V_{0}(1 - e^{- X/\mu})^{2}$$

- at $X \gg \mu$: natural $\Rightarrow$slow-roll plateau

- at $X \rightarrow 0$: stable minimum.

The **Equation of motion** from GU, in FRW, becomes (for $X(t)$homogeneous):

$$\ddot{X} + 3H\dot{X} + V_{X}'(X) + F_{\text{int}}(X,\Omega) + F_{\text{mem}}(t) = 0$$

where $F_{\text{int}}$ and $F_{\text{mem}}$ come directly from $L_{\text{int}},L_{\text{mem}}$

The Golden Universe Formation

.

In slow-roll (ignoring for the moment the backreaction for the first pass):
$$H^{2} \simeq \frac{V_{X}}{3M_{pl}^{2}},3H\dot{X} \simeq - V_{X}'(X).$$

**2) Effective mass of** $\mathbf{X}$**after inflation (key for reheating)**

At minimum $X_{\min} = 0$:

$$m_{X}^{2} \equiv V_{X}^{''}(0).$$

For the above potential:

$$V_{X}^{''}(0) = \frac{2V_{0}}{\mu^{2}} \Rightarrow \boxed{m_{X} = \sqrt{\frac{2V_{0}}{\mu^{2}}}.}$$

**3) We derive reheating from** $\mathbf{L}_{\text{int}}$**(not "put by hand")**

GU gives you the general form:

$$L_{\text{int}} = - g_{\Omega X}(X)\text{ }S_{\text{coupling}}(\Omega)\text{ }X:contentReference\lbrack sheep:7\rbrack index = 7$$

To make $\Gamma$ computable, we choose a "light" component of $\Omega$:
**(A) Scalar channel:** $\mathbf{S}_{\text{coupling}}\mathbf{(}\mathbf{\Omega}\mathbf{) \supset}\frac{\mathbf{1}}{\mathbf{2}}\mathbf{\chi}^{\mathbf{2}}$

$$L_{\text{int}} \supset - \frac{1}{2}\text{ }g\text{ }X\text{ }\chi^{2}$$

(this is exactly the "instantiation" of $S_{\text{coupling}}$).

The Golden Universe Formation

Decay width (for $m_{\chi} \ll m_{X}$):

$$\boxed{\Gamma_{X \rightarrow \chi\chi} \simeq \frac{g^{2}}{32\pi\text{ }m_{X}}}$$

(note: here $g$ has mass dimension).

**(B) Fermionic channel:** $\mathbf{S}_{\text{coupling}}\mathbf{(}\mathbf{\Omega}\mathbf{) \supset}\overset{ˉ}{\mathbf{\psi}}\mathbf{\psi}$

$${L_{\text{int}} \supset - y\text{ }X\text{ }\overset{ˉ}{\psi}\psi
}{\boxed{\Gamma_{X \rightarrow \overset{ˉ}{\psi}\psi} \simeq \frac{y^{2}}{8\pi}\text{ }m_{X}}
}$$
(here $y$ is dimensionless).

**4) Reheating temperature and minimum condition for QGP**

Transfer equations (standard):

$${\dot{\rho}}_{X} + 3H(\rho_{X} + p_{X}) = - \Gamma\rho_{X},{\dot{\rho}}_{r} + 4H\rho_{r} = + \Gamma\rho_{X}.$$

Approximate reheating temperature:

$$\boxed{T_{reh} \approx \left( \frac{90}{\pi^{2}g_{*}} \right)^{1/4}\sqrt{\Gamma\text{ }M_{pl}}}$$

**The requirement for the universe to safely pass through the QGP epoch** is simply:

$$\boxed{T_{reh} \gtrsim 0.2\text{ GeV}}$$

(after which, on cooling, you will inevitably go through the QCD regime; GU even marks a "QCD Epoch" when $X$ goes below $X_{QCD}$

The Golden Universe Formation
).

From here you immediately get:

$$\Gamma_{\min} = \frac{1}{M_{pl}}\left( \frac{T_{reh}}{\left( \frac{90}{\pi^{2}g_{*}} \right)^{1/4}} \right)^{2}$$

and then direct constraints on couplings:

**(A) For** $\mathbf{X \rightarrow \chi\chi}$

$$\Gamma = \frac{g^{2}}{32\pi m_{X}} \geq \Gamma_{\min} \Rightarrow \boxed{g \geq \sqrt{32\pi\text{ }m_{X}\text{ }\Gamma_{\min}}}$$

**(B) For** $\mathbf{X \rightarrow}\overset{ˉ}{\mathbf{\psi}}\mathbf{\psi}$

$$\Gamma = \frac{y^{2}}{8\pi}m_{X} \geq \Gamma_{\min} \Rightarrow \boxed{y \geq \sqrt{\frac{8\pi\text{ }\Gamma_{\min}}{m_{X}}}}$$

**5) Link with "clock ticks" and GU eras**

Thresholds are:
$$X_{\text{critical},n} = X_{0}\varphi^{- n}:contentReference\lbrack oaicite:10\rbrack index = 10$$

So you define (continuously) the epoch index:

$$\boxed{n(X) = {\log}_{\varphi}\text{ ⁣}\left( \frac{X_{0}}{X} \right)}$$

and you can identify the QCD epoch as the time when $X$ passes below $X_{QCD}$ (in GU: "Pattern k=2 (QCD Epoch, $X \approx X_{QCD}$" )

The Golden Universe Formation

.

If you say "continue", I do the next step exactly like this:

1. we choose values for $\mu$ and $V_{0}$ (or tie them to the initial scale set by $\mathfrak{R}(Z_{1})$

> The Golden Universe Formation
>
> ),
2. we calculate $m_{X}$,

3. we put in the formulas above and they give you numerically **how small can be** $g$or $y$ to be sure $T_{reh} > 0.2$GeV (so QGP guaranteed).

Sources

Continue

Thought for 1m 7s

According to the uploaded document (**"The Golden Universe Formation"**; I don't see it once in the metadata), you already have exactly the slow-roll "engine" in GU: $L_{\text{total}} = L_{\Omega} + L_{X} + L_{\text{int}} + L_{\text{mem}}$, with $X$ as real scalar, potential $V_{X}(X)$(gentle slope) and memory kernel $G = e^{- \beta(X)(t - \tau)}$.

The Golden Universe Formation

Next, we do the complete closure + reheating **numerically**, so that the **plasma/QGP** comes out safely.

**1) We fix an** $\mathbf{V}_{\mathbf{X}}\mathbf{(X)}$**explicitly (as a complete example)**

In GU it is said that there is $V_{X}(X)$ and that it gives "gentle slope" (slow roll), but the shape is not fixed.
The Golden Universe Formation

A standard *plateau* example (compatible with cosmological data) is:

$$V_{X}(X) = V_{0}(1 - e^{- X/\mu})^{2}$$

In FRW:

$$H^{2} = \frac{1}{3M_{pl}^{2}}(\frac{1}{2}{\dot{X}}^{2} + V_{X}(X)),\ddot{X} + 3H\dot{X} + V_{X}'(X) + F_{int} + F_{mem} = 0$$

where $F_{int}$ and $F_{mem}$ are exactly the contributions from $L_{\text{int}}$ and $L_{\text{mem}}$.

The Golden Universe Formation

**2) We link the initial GU scale to the beginning of the evolution**

GU fixes the initial by $Z_{1}$: $\mathfrak{R}(Z_{1})$ is the "fuel" for the evolution and sets the initial scale of $X$.

The Golden Universe Formation
The GU also says that the age thresholds are:

$$X_{\text{critical},n} = X_{0}\text{ }\varphi^{- n},X_{0} = \mathfrak{\mid R}(Z_{1}) \mid $$

The Golden Universe Formation

**3) The mass of** $\mathbf{X}$**after inflation (we need it for** $\mathbf{\Gamma}$**)**

At minimum $X \simeq 0$:

$$m_{X}^{2} = V_{X}^{''}(0) = \frac{2V_{0}}{\mu^{2}} \Rightarrow m_{X} = \sqrt{\frac{2V_{0}}{\mu^{2}}}$$

To have a **fully numerical** example, I choose (standard in cosmology):

- $\mu = M_{pl}$(reduced Planck),

- $V_{0}$ fixed to give the observed scalar amplitude (not from GU, but from standard cosmology).

It typically results in:
$$V_{0} \approx 7.6 \times 10^{- 11}M_{pl}^{4} \Rightarrow m_{X} \approx 3.0 \times 10^{13}\text{ GeV}.$$

**4) Reheating derived from** $\mathbf{L}_{\text{int}}$**(minimum two channels)**

GU has:

$$L_{\text{int}} = - g_{\Omega X}(X)\text{ }S_{\text{coupling}}(\Omega)\text{ }X$$

The Golden Universe Formation

**(A) If** $\mathbf{S}_{\text{coupling}}\mathbf{\supset}\frac{\mathbf{1}}{\mathbf{2}}\mathbf{\chi}^{\mathbf{2}}$

$$L_{\text{int}} \supset - \frac{1}{2}g\text{ }X\chi^{2} \Rightarrow \Gamma_{X \rightarrow \chi\chi} \simeq \frac{g^{2}}{32\pi m_{X}}$$

**(B) If** $\mathbf{S}_{\text{coupling}}\mathbf{\supset}\overset{ˉ}{\mathbf{\psi}}\mathbf{\psi}$

$$L_{\text{int}} \supset - y\text{ }X\overset{ˉ}{\psi}\psi \Rightarrow \Gamma_{X \rightarrow \overset{ˉ}{\psi}\psi} \simeq \frac{y^{2}}{8\pi}m_{X}$$

**5) The "universe like ours" condition up to QGP:** $\mathbf{T}_{\mathbf{reh}}\mathbf{\gtrsim 0.2}$**GeV**
Reheating:

$$T_{reh} \approx \left( \frac{90}{\pi^{2}g_{*}} \right)^{1/4}\sqrt{\Gamma M_{pl}}$$

With $g_{*} \sim 100$ and the minimum requirement $T_{reh} \geq 0.2$GeV, you get:

$$\Gamma_{\min} \approx 5.44 \times 10^{- 20}\text{ GeV}.$$

**Implication: MINIMUM (very small) couplings guaranteeing QGP**

Using $m_{X} \approx 3.0 \times 10^{13}$GeV:

**(A) Fermionic Channel**

$$\Gamma = \frac{y^{2}}{8\pi}m_{X} \geq \Gamma_{\min} \Rightarrow y_{\min} \approx 2.1 \times 10^{- 16}.$$

**(B) Scalar Channel**

$$\Gamma = \frac{g^{2}}{32\pi m_{X}} \geq \Gamma_{\min} \Rightarrow g_{\min} \approx 1.28 \times 10^{- 2}\text{ GeV}.$$
I mean: it's "easy" to make a hot big bang that goes through QGP---you need incredibly small couplings to reach at least 200 MeV.

**6) Where does "QCD Epoch" come into GU (QGP/hadronization connection)**

GU explicitly marks:

- **Pattern k=2 (QCD Epoch,** $X \approx X_{QCD}$**)** and that then the gluon-sector dynamics becomes dominant and confined states (hadrons) are formed.

> The Golden Universe Formation

In standard thermal terms: after reheating the universe cools, and in the QCD zone (150--200 MeV) you are in **quark-gluon plasma** regime, then crossover/hadronization. GU translates this to "when $X$crosses the $X_{QCD}$ threshold".

**7) Continuous connection between "ticks" and evolution over time**

From GU thresholds:

$$X_{\text{critical},n} = X_{0}\varphi^{- n}$$

The Golden Universe Formation
define:

$$n(X) = {\log}_{\varphi}\text{ ⁣}\left( \frac{X_{0}}{X} \right)$$

and the cosmic "rail" becomes:

$$X(t)\text{ } \Downarrow \text{ pass thresholds }X_{EW},X_{QCD},\cdots \Rightarrow \text{Pattern-k transitions (k=1,2,...) }$$

The Golden Universe Formation

If you want to go "even tighter" (without standard cosmological parameters), the next step is to tie $V_{0}$ and $\mu$ directly to the initial GU scale ( $\mathfrak{\mid R}(Z_{1}) \mid$ , \~$10^{18}$ GeV in the text)

The Golden Universe Formation

and to explicitly introduce into the equation of $X$ the memory term $L_{mem}$(kernel $e^{- \beta(X)(t - \tau)}$) as an effective correction to the slow-roll drift.

The Golden Universe Formation

Sources
Okay

Thought for 1m 24s

According to the document **"The Golden Universe Formation"** (no date in the available fragment), you already have the key pieces:\
$L_{\text{total}} = L_{\Omega} + L_{X} + L_{\text{int}} + L_{\text{mem}}$, with $L_{X} = \frac{1}{2}(\partial X)^{2} - V_{X}(X)$(gentle slope → slow-roll), $L_{\text{int}} = - g_{\Omega X}(X)\text{ }S_{\text{coupling}}(\Omega)\text{ }X$and nonlocal memory $L_{\text{mem}}$ with kernel $G = e^{- \beta(X)(t - \tau)}$.

The Golden Universe Formation

Below I continue with the **formulas directly connecting GU to "our universe"**: initial scale $Z_{1}$→ $X_{0}$→ $V_{X}$→ reheating → plasma/QGP → QCD threshold in GU.

**1) Initial scale from GU:** $\mathbf{Z}_{\mathbf{1}}\mathbf{\Rightarrow}\mathbf{X}_{\mathbf{0}}$

GU explicitly gives you:

- $\mid Z_{1} \mid = \frac{M_{P}}{4\sqrt{\pi}}$ (the size of the initial impulse)

> The Golden Universe Formation
- $Z_{1} = \mid Z_{1} \mid (\cos\theta + i\sin\theta)$ and numerically $\mathfrak{R}(Z_{1}) \approx - 2.264 \times 10^{- 9}\text{ kg}$

> The Golden Universe Formation
>
> The Golden Universe Formation

- the interpretation: $\mathfrak{R}(Z_{1})$ is the **initial value of the clock-field** $X$ and sets the energy scale $\sim 10^{18}$GeV

> The Golden Universe Formation
>
> .

In the Thresholds section:

$$X_{\text{critical},n} = X_{0}\text{ }\varphi^{- n},\text{with }X_{0} = \mathfrak{\mid R}(Z_{1}) \mid :contentReference\lbrack oaicite:5\rbrack index = 5$$

**2) Slow-roll equations for** $\mathbf{X}$**in GU (with memory + backreaction)**

From the GU structure, in FRW (homogeneous), the effective equation for $X(t)$ is:
$$\boxed{\ddot{X} + 3H\dot{X} + V_{X}'(X) + F_{\text{int}}(X,\Omega) + F_{\text{mem}}(t) = 0}$$

where:

$${F_{\text{int}}(X,\Omega) = \frac{\partial}{\partial X}\lbrack g_{\Omega X}(X)\text{ }S_{\text{coupling}}(\Omega)\text{ }X\rbrack(\text{from }L_{\text{int}}):contentReference\lbrack oaicite:6\rbrack index = 6
}{F_{\text{mem}}(t) = \frac{\partial}{\partial X}\left\lbrack \lambda_{\text{rec}}(X)\text{ }S_{\text{mem}}(\Omega(t))\int_{0}^{t}e^{- \beta(X)(t - \tau)}\text{ }H\lbrack \lambda_{\text{rec}}(X)\text{ }S_{\text{mem}}(\Omega(t)) \right\rbrack(\text{from }L_{\text{mem}}):contentReference\lbrack oaicite:7\rbrack index = 7
}$$

Slow-roll (inflationary regime) means:

$${{\dot{X}}^{2} \ll V_{\text{eff}}, \mid \ddot{X} \mid \ll 3H \mid \dot{X} \mid 
}{\boxed{3H\dot{X} \simeq - (V_{X}'(X) + F_{\text{int}} + F_{\text{mem}})}
}$$

**3) We choose a** $\mathbf{V}_{\mathbf{X}}\mathbf{(X)}$**"plateau" (to be slow-roll robust)**

GU just says that $V_{X}(X)$ exists and gives the gentle slope

The Golden Universe Formation
, so we need a form. A minimal example:

$$\boxed{V_{X}(X) = V_{0}(1 - e^{- X/\mu})^{2}}$$

- for $X \gg \mu$: $V_{X} \approx V_{0}$ (plateau → natural slow-roll)

- for $X \rightarrow 0$: minimum stable (oscillation starts → reheating)

The mass of the "inflaton" (we need it for $\Gamma$):

$$\boxed{m_{X}^{2} = V_{X}^{''}(0) = \frac{2V_{0}}{\mu^{2}} \Rightarrow m_{X} = \sqrt{\frac{2V_{0}}{\mu^{2}}}}$$

**4) How to bind** $\mathbf{V}_{\mathbf{0}}$**of** $\mathbf{Z}_{\mathbf{1}}$**(two coherent modes)**

**(A) GU-first: you start from the ladder** $\mathbf{\mid}\mathbf{Z}_{\mathbf{1}}\mathbf{\mid}\mathbf{\sim 0.141}\text{ }\mathbf{M}_{\mathbf{P}}$**and** $\mathfrak{\mid R}\mathbf{(}\mathbf{Z}_{\mathbf{1}}\mathbf{)}\mathbf{\mid}\mathbf{\sim}\mathbf{10}^{\mathbf{18}}$**GeV**

**The Golden Universe Formation**

**The Golden Universe Formation**
The simplest (without inventing initial volume) is:

$$\boxed{V_{0} = \alpha\text{ }X_{0}^{4}}$$

where $\alpha$ is a dimensionless constant (you fix it later from $A_{s}$ or from an internal GU condition). This directly preserves the idea from GU: "the initial energy (of $Z_{1}$) is the fuel"

The Golden Universe Formation

.

**(B) Obs-first: fix** $\mathbf{V}_{\mathbf{0}}$**from cosmological fluctuations (so that our universe comes out exactly)**

Here you use:

$$A_{s} \simeq \frac{1}{24\pi^{2}M_{pl}^{4}}\frac{V_{*}}{\epsilon_{*}}$$

and you get a typical $V_{0}$ well below Planck ($\sim 10^{16}$GeV scale). This is the "standard cosmology" mode.

In GU, reconciliation is natural if you accept that:
- $Z_{1}$sets the **raw scale**,

- and $F_{\text{mem}}$+ $F_{\text{int}}$ can effectively "shape" the slope/plateau so that $V_{*}$ (at the output of the observable modes) is lower than the initial scale.

**5) Reheating derived from** $\mathbf{L}_{\text{int}}$**→ plasma → QGP**

GU gives you the general coupling $L_{\text{int}}$

The Golden Universe Formation

. A minimal instantiation to compute $\Gamma$:

**Scalar channel (product** $\mathbf{\chi}$**)**

If $S_{\text{coupling}}(\Omega) \supset \frac{1}{2}\chi^{2}$:

$$L_{\text{int}} \supset - \frac{1}{2}g\text{ }X\text{ }\chi^{2} \Rightarrow \boxed{\Gamma_{X \rightarrow \chi\chi} \simeq \frac{g^{2}}{32\pi\text{ }m_{X}}}$$

**Fermionic channel (product** $\mathbf{\psi}$**)**
If $S_{\text{coupling}}(\Omega) \supset \overset{ˉ}{\psi}\psi$:

$$L_{\text{int}} \supset - y\text{ }X\text{ }\overset{ˉ}{\psi}\psi \Rightarrow \boxed{\Gamma_{X \rightarrow \overset{ˉ}{\psi}\psi} \simeq \frac{y^{2}}{8\pi}\text{ }m_{X}}$$

Reheating temperature:

$$\boxed{T_{reh} \approx \left( \frac{90}{\pi^{2}g_{*}} \right)^{1/4}\sqrt{\Gamma\text{ }M_{pl}}}$$

**The minimum condition for the universe to go through QGP** (deconfinement/crossover QCD regime) is:

$$\boxed{T_{reh} \gtrsim 0.2\text{ GeV}}$$

In practice, if $m_{X}$ is large (which GU suggests at the beginning), this condition is extremely easy to satisfy even with small couplings.

**6) "QCD Epoch" in GU: Threshold** $\mathbf{X}_{\mathbf{QCD}}$

GU explicitly says that at **Pattern k=2 (QCD Epoch,** $X \simeq X_{QCD}$**)** "gluon-sector dynamics becomes dominant" and confined states (hadrons) appear.

The Golden Universe Formation
So the complete chain becomes:

1. slow-roll (dominant $V_{X}$)

2. reheating (energy from $X$→ radiation/plasma)

3. the universe is cooling

4. when $X(t)$ passes the $X_{QCD}$ threshold, you enter "Pattern k=2" (QCD becomes defining)

> The Golden Universe Formation

5. in standard terms: in the window $T \sim 150\text{ ⁣} - \text{ ⁣}200$MeV of QGP → then hadronization.

**7) Link "temperature ↔** $\mathbf{X}$**" (so that the exact timeline comes out)**

In your particle paper it explicitly states that "temperature is related to the cosmic clock $X$" and gives the example of recombination $T \simeq 1$eV → $N_{rec} \approx 128$.

Golden Universe Theory for the ...
Mathematically, this means that there must be a monotonic function:

$$\boxed{T = T(X)}\text{(or equivalently }T = T(n)\text{ with }n = {\log}_{\varphi}(X_{0}/X))$$

and points like $T\text{ ⁣} = \text{ ⁣}1\text{ eV} \leftrightarrow n\text{ ⁣} \approx \text{ ⁣}128$ fix the calibration.

Golden Universe Theory for the ...

If you want to go "all-in" on the next piece of formulas, the next step is to write explicitly:

$$\frac{dX}{dN} \simeq - M_{pl}^{2}\frac{V_{X}'(X) + F_{\text{int}} + F_{\text{mem}}}{V_{X}} \Rightarrow \frac{dn}{dN} = \frac{1}{\ln\varphi}\left( -\frac{1}{X}\frac{dX}{dN} \right)$$

and then impose the $T(X)$ calibration so that the $X_{QCD}$ threshold corresponds to $T \sim 0.15\text{ ⁣} - \text{ ⁣}0.2$GeV (QGP), and $n \approx 95$ is the "hadronization moment" in your modules.

Sources

Okay

Thought for 25s
Perfect --- the next step (after we put **slow-roll + reheating**) is to **close the GU-clock link** $X$**↔ expansion** $a(t)$**↔ temperature** $T$, so that the epochs (including **QGP/QCD**) come out automatically.

Below I give you the "missing" set of formulas to directly map **ticks** $n$ onto **temperature**.

**1) Basic definition: the tick** $\mathbf{n}$**of** $\mathbf{X}$

From GU:

$$X_{\text{critical},n} = X_{0}\text{ }\varphi^{- n}$$

We continuously define:

$$\boxed{n(X) = {\log}_{\varphi}\text{ ⁣}\left( \frac{X_{0}}{X} \right) = \frac{\ln(X_{0}/X)}{\ln\varphi}}$$

**2) After reheating: RD Universe (radiation-dominated) ⇒** $\mathbf{T \propto 1}\mathbf{/}\mathbf{a}$

In standard mode (after you have thermalized plasma):

$$\boxed{T(a) \propto \frac{1}{a}}$$
With $N = \ln a$:

$$\boxed{T(N) = T_{reh}\text{ }e^{- (N - N_{reh})}}$$

**3) Key deck: how the clock tick relates to e-folds**

You need a relationship of type:

$$\boxed{\frac{dn}{dN} = \kappa(N)\text{ }\text{ }\text{ }\text{ }\text{ }\text{ }\text{ }\text{ }\text{ (}\widehat{\text{ı}}\text{n general)}}$$

**Minimal closure (simplest, very useful):**

assume constant $\kappa$\~ over long epochs (RD/MD):

$$\boxed{\frac{dn}{dN} \approx \kappa = \text{const}} \Rightarrow n(N) = n_{reh} + \kappa\text{ }(N - N_{reh})$$

We invert:

$$N - N_{reh} = \frac{n - n_{reh}}{\kappa}$$
**4) Final formula: temperature directly as a function of tick** $\mathbf{n}$

Combining with $T(N)$:

$$\boxed{T(n) = T_{reh}\text{ }\exp\text{ ⁣}\left( -\frac{n - n_{reh}}{\kappa} \right)}$$

If you want explicitly in powers of $\varphi$:

$$T(n) = T_{reh}\text{ }\varphi^{- \text{ }(n - n_{reh})/\kappa_{\varphi}},\kappa_{\varphi} \equiv \kappa/ln\varphi$$

(but the exponent form is cleaner).

**5) Calibration of** $\mathbf{\kappa}$**from two "anchors" (this makes the model "our universe")**

Take two points $\left( n_{1},T_{1} \right)$, $\left( n_{2},T_{2} \right)$ (eg recombination and QCD) and solve:

$$\boxed{\kappa = - \text{ }\frac{n_{2} - n_{1}}{\ln(T_{2}/T_{1})}}$$

**Example (as numerical demonstration only)**
If you use:

- recombination $T_{rec} \sim 1\text{ eV}$ at $n_{rec} \approx 128$ (as you have in your texts),

- QCD $T_{QCD} \sim 0.16\text{ GeV}$,

- and if in GU you put $n_{QCD} \approx 95$,

then it comes out:

$$\kappa \approx 0.84$$

(ie \~0.84 ticks per e-fold in that calibration).

**6) Link with reheating (to fix** $\mathbf{n}_{\mathbf{reh}}$**and** $\mathbf{T}_{\mathbf{reh}}$**)**

You already have:

$$T_{reh} \approx \left( \frac{90}{\pi^{2}g_{*}} \right)^{1/4}\sqrt{\Gamma M_{pl}}$$
and

$$\boxed{n_{reh} \approx n(X_{end}) = {\log}_{\varphi}\text{ ⁣}\left( \frac{X_{0}}{X_{end}} \right)}$$

(you approximate that reheating is fast compared to the evolution of $X$, so $X$ does not "consume" many ticks there; if you want, we can include a small correction $\Delta n_{reh}$).

**7) What does this mean for QGP (simple condition)**

Once you have $T(n)$ , QGP/QCD appears automatically when:

$$\boxed{T(n) \approx 0.15\text{–}0.2\text{ GeV}}$$

and that directly fixes your $n_{QCD}$ (or vice versa, if $n_{QCD}$ is imposed by GU, it fixes your $\kappa$).

If you say "go ahead", I take the next step: I include the **memory term** as a correction to $\kappa$ (ie $\kappa(N)$ is no longer constant, but gets a controlled "backflow"), and I show you how it can finely move the position of your thresholds (QCD, recombination) without ruining slow-roll.

Ok go ahead

Thought for 1m 10s
According to a document (date not specified in the PDF), GU already gives you exactly the form of memory we need to go "further" without inventing another mechanism: the term

$$L_{\text{mem}} = - \lambda_{\text{rec}}(X)\text{ }S_{\text{mem}}(\Omega(t))\int_{0}^{t}{G(X;t,\tau)\text{ }H\lbrack\Omega(\tau)\rbrack\text{ }d\tau}$$

with exponential kernel

$$G(X;t,\tau) = e^{- \beta(X)(t - \tau)}.$$

The Golden Universe Formation

The Golden Universe Formation

Below is the "next step": how you turn non-local memory into a **local** system (but with real memory effect), then how it directly gives you $\kappa(N) = dn/dN$ and $T(n)$.

**1) Replacing the memory integral with an auxiliary variable (the key trick)**

Define **memory variable**:

$$M(t)\text{\:\,} \equiv \text{\:\,}\int_{0}^{t}e^{- \beta(X)(t - \tau)}\text{ }H\lbrack\Omega(\tau)\rbrack\text{ }d\tau.$$
Then the term GU becomes simple:

$$L_{\text{mem}} = - \lambda_{\text{rec}}(X)\text{ }S_{\text{mem}}(\Omega(t))\text{ }M(t).$$

(same structure as in text)

The Golden Universe Formation

If we treat $\beta(X)$ as "almost constant" on a short interval (adiabatic; exactly what GU suggests by "$\beta(X)$ can evolve" but does not explode instantly)

The Golden Universe Formation

, then $M(t)$ satisfies a local ODE:

$$\boxed{\dot{M} = H\lbrack\Omega(t)\rbrack - \beta(X)\text{ }M.}$$

This is huge: you got rid of the integral and you have a closed differential system.

**2) Complete equation for** $\mathbf{X}$**(with memory + backreaction), in FRW**
GU says: $L_{\text{total}} = L_{\Omega} + L_{X} + L_{\text{int}} + L_{\text{mem}}$

The Golden Universe Formation

, with

$$L_{X} = \frac{1}{2}(\partial X)^{2} - V_{X}(X),V_{X}\text{ d}\breve{\text{a}}\text{ slope bl}\widehat{\text{a}}\text{nd}\breve{\text{a}}\text{ (slow-roll)}$$

The Golden Universe Formation

And local interaction:

$$L_{\text{int}} = - g_{\Omega X}(X)\text{ }S_{\text{coupling}}(\Omega)\text{ }X.$$

The Golden Universe Formation

In an FRW background, the equation of motion becomes (schematically, but exactly in structure):

$$\boxed{\ddot{X} + 3H\dot{X} + V_{X}'(X) + F_{\text{int}}(X,\Omega) + F_{\text{mem}}(X,\Omega,M) = 0}$$
where

+ \text{\:\,}\lambda_{\text{rec}}(X)\text{ }S_{\text{mem}}\frac{\partial M}{\partial X}.$$

(and $M$ is defined above from the GU kernel)

The Golden Universe Formation

**3) Switching to "expansion" time** $\mathbf{N =}\mathbf{\ln}\mathbf{a}$**(to get** $\mathbf{dn}\mathbf{/}\mathbf{dN}$**)**

You use $d/dt = H\text{ }d/dN$. We denote $X_{N} \equiv dX/dN$, $M_{N} \equiv dM/dN$.

**Memory becomes:**

$$\boxed{M_{N} = \frac{H\lbrack\Omega\rbrack}{H} - \frac{\beta(X)}{H}\text{ }M.}$$

**Equation of** $X$ (in slow-roll mode, i.e. you neglect $X_{NN}$ compared to the friction term):

$$3H^{2}\text{ }X_{N}\text{\:\,} \simeq \text{\:\,} - (V_{X}'(X) + F_{\text{int}} + F_{\text{mem}}).$$
And with Friedmann $3H^{2}M_{pl}^{2} \simeq V_{\text{eff}}$ (in inflation), you can write compactly:

$$\boxed{X_{N} \simeq - \text{ }M_{pl}^{2}\text{ }\frac{V_{X}'(X) + F_{\text{int}} + F_{\text{mem}}}{V_{\text{eff}}}}$$

**4) Now comes your piece:** $\mathbf{\kappa(N) = dn}\mathbf{/}\mathbf{dN}$**with memory included**

GU defines the thresholds (ticks):

$$X_{\text{critical},n} = X_{0}\text{ }\varphi^{- n},X_{0} = \mathfrak{\mid R}(Z_{1}) \mid .$$

The Golden Universe Formation

So we define continuously:

$$n(X) = {\log}_{\varphi}\text{ ⁣}(\frac{X_{0}}{X}) = \frac{\ln(X_{0}/X)}{\ln\varphi}.$$

We derive:

$$\boxed{\kappa(N) \equiv \frac{dn}{dN} = - \frac{1}{\ln\varphi}\frac{1}{X}\frac{dX}{dN} = \frac{1}{\ln\varphi}\frac{1}{X}( - X_{N}).}$$
Substituting the slow-roll expression for $X_{N}$:

$$\boxed{\kappa(N) \simeq \frac{M_{pl}^{2}}{\ln\varphi}\text{\:\,}\frac{V_{X}'(X) + F_{\text{int}} + F_{\text{mem}}}{X\text{ }V_{\text{eff}}}.}$$

That's the "working" formula that tells you how **memory** (via $M(N)$) makes your $\kappa$ variable → i.e. the ticks are not uniform "in expansion time", but have *hysteresis / backflow* controlled.

**5) Temperature connection: exact formula when** $\mathbf{\kappa}$**is NOT constant**

After reheating, in a radiation-dominated regime, you have approximately:

$$\frac{d\ln T}{dN} \simeq - 1$$

(plus a small correction from $g_{*s}(T)$ if you want precision).

Combining with $\kappa(N) = dn/dN$:

$$\boxed{\frac{d\ln T}{dn} = \frac{d\ln T/dN}{dn/dN} \simeq - \frac{1}{\kappa(n)}.}$$

Integrate:
$$\boxed{\ln\frac{T(n)}{T(n_{0})} \simeq - \int_{n_{0}}^{n}\frac{dn'}{\kappa(n')}.}$$

- if $\kappa$ is constant → you recover the simple formula $T(n) = T_{0}\text{ }e^{- (n - n_{0})/\kappa}$;

- if the memory is strong in certain epochs → $\kappa(n)$ deforms locally and finely "moves" your thresholds (QCD, recombination, etc.).

**6) Calibration with your GU anchors (recombination and hadronization/QCD)**

From "Particles" you explicitly have:

- recombination: $T \approx 1\text{ eV}$ corresponds to an epoch $N_{\text{rec}} \approx 128$ and "the temperature is related to the cosmic clock $X$".

> Golden Universe Theory for the ...

Also there you use hadronization/QCD around:

- $n = 95$ (hadron calculation at $n = 95$ and BBN immediately after, $n \approx 95\text{–}96$).

> Golden Universe Theory for the ...
If you take $T_{\text{QCD}} \sim 0.16\text{ GeV}$ as the order of magnitude and $T_{\text{rec}} \sim 1\text{ eV}$, then an **average** $\kappa$between $n = 95$and $n = 128$ is:

$$\kappa_{\text{avg}} \approx \frac{n_{\text{rec}} - n_{\text{QCD}}}{\ln(T_{\text{QCD}}/T_{\text{rec}})} = \frac{33}{\ln(1.6 \times 10^{8})} \approx 1.75.$$

Interpretation: in that calibration, \~1.75 ticks per e-fold (on average), and deviations from that come naturally from $F_{\text{mem}}$ (ie from $M(N)$).

**7) What we actually do "next" (next piece of construction)**

Now you have a closed local system in $\left( X,M,a \right)$:

1. **Initialization:** $X(0) = \mathfrak{R}(Z_{1})$, so $X_{0} = \mid X(0) \mid$(GU actually computes $X_{0} \approx 0.104\text{ }E_{P}$)

> The Golden Universe Formation

2. **Dynamics:** integrate in $N$:

$$X_{N} \simeq - M_{pl}^{2}\frac{V_{X}' + F_{\text{int}} + F_{\text{mem}}}{V_{\text{eff}}},M_{N} = \frac{H\lbrack\Omega\rbrack}{H} - \frac{\beta(X)}{H}M$$

3. **Tick rate:** $\kappa(N) = dn/dN$ from the formula above.
4. **Temperature:** $T(n)$from integral $\ln T = - \int dn/\kappa$, calibrated with $n = 95 \leftrightarrow T_{\text{QCD}}$and $n = 128 \leftrightarrow 1\text{ eV}$.

> Golden Universe Theory for the ...
>
> Golden Universe Theory for the ...

If you want, the next concrete step is to choose a minimal form for the GU functions:

- $\lambda_{\text{rec}}(X)$,

- $\beta(X)$,

- and a simple proxy for $H\lbrack\Omega\rbrack$ (eg $H\lbrack\Omega\rbrack \propto \Omega^{\dagger}\Omega$ as the example $S_{\text{mem}} = \Omega^{\dagger}\Omega$ suggests)

> The Golden Universe Formation
>
> ,

and I write you explicitly **how the "snap"** (quick transitions) occurs at the $X_{\text{critical},n}$ thresholds due to the inertia of $M$ (memory), i.e. exactly the mechanism that makes the transitions more "discrete" than a perfectly smooth roll.
Sources

Okay

Perfect --- then we now have the "closed set" GU → our universe, with **memory** implemented correctly (no integral), and with the bridge to **QGP/QCD**.

**Final set of equations (minimal, ready to use)**

**1) Definitions**

$${N \equiv \ln a,\frac{d}{dt} = H\frac{d}{dN}
}{n(X) = {\log}_{\varphi}\text{ ⁣}(\frac{X_{0}}{X}) = \frac{\ln(X_{0}/X)}{\ln\varphi},X_{0} = \mathfrak{\mid R}(Z_{1}) \mid 
}{\kappa(N) \equiv \frac{dn}{dN} = - \frac{1}{\ln\varphi}\frac{1}{X}\frac{dX}{dN}
}$$

**2) Memory (completely replace GU with ODE)**\
The GU kernel: $G = e^{- \beta(X)(t - \tau)}$.\
You define:

$$M(t) = \int_{0}^{t}e^{- \beta(X)(t - \tau)}H\lbrack\Omega(\tau)\rbrack\text{ }d\tau$$
⇒ local equivalent:

$$\boxed{\dot{M} = H\lbrack\Omega(t)\rbrack - \beta(X)M}$$

or in $N$:

$$\boxed{M_{N} = \frac{H\lbrack\Omega\rbrack}{H} - \frac{\beta(X)}{H}M}$$

**3) Slow-roll for** $X$**with interaction + memory**

$$\boxed{X_{N} \simeq - \text{ }M_{pl}^{2}\text{ }\frac{V_{X}'(X) + F_{int}(X,\Omega) + F_{mem}(X,\Omega,M)}{V_{eff}(X,\Omega,M)}}$$

where, from GU:

$${F_{int} = \frac{\partial}{\partial X}\lbrack g_{\Omega X}(X)S_{coupling}(\Omega)X\rbrack
}{F_{mem} = \frac{\partial}{\partial X}\lbrack\lambda_{rec}(X)S_{mem}(\Omega)M\rbrack
}$$

($L_{int}$ and $L_{mem}$ are exactly those in the document).
**4) Friedmann (for** $H$**)**\
In inflation:

$$\boxed{3M_{pl}^{2}H^{2} \simeq V_{eff}}$$

After reheating (RD):

$$\rho_{r} = \frac{\pi^{2}}{30}g_{*}T^{4},H \simeq 1.66\sqrt{g_{*}}\frac{T^{2}}{M_{pl}}$$

**5) Reheating (for plasma to appear)**

$${\boxed{{\dot{\rho}}_{X} + 3H(\rho_{X} + p_{X}) = - \Gamma\rho_{X},{\dot{\rho}}_{r} + 4H\rho_{r} = + \Gamma\rho_{X}}
}{\boxed{T_{reh} \approx \left( \frac{90}{\pi^{2}g_{*}} \right)^{1/4}\sqrt{\Gamma M_{pl}}}
}$$

QGP condition:

$$\boxed{T_{reh} \gtrsim 0.2\text{ GeV}}$$
**6) Temperature directly as a function of tick** $n$**(with memory)**\
After reheating:

$$\frac{d\ln T}{dN} \simeq - 1$$

So:

$$\boxed{\frac{d\ln T}{dn} \simeq - \frac{1}{\kappa(n)}} \Rightarrow \boxed{\ln\frac{T(n)}{T(n_{0})} \simeq - \int_{n_{0}}^{n}\frac{dn'}{\kappa(n')}}$$

This is exactly where **memory** (via $\kappa(n)$) can finely move the thresholds.

**What does "ok" mean here**

It means we have:

- how $X$ runs (slow-roll),

- how we "remember" the past (memory $M$),

- how to connect $X \rightarrow n$,
- how to get $T(n)$,

- and the condition for QGP/QCD.

If you want to start the **numerical calibration** part (no further questions), I can take your typical anchors:

- $n_{QCD} \approx 95$and $T_{QCD} \approx 0.16$GeV,

- $n_{rec} \approx 128$and $T_{rec} \approx 1$eV,

and I give you $\kappa_{avg}$, then a minimal form for $\beta(X)$ and $\lambda_{rec}(X)$ that produces a "snap" at thresholds $X_{\text{critical},n}$ (ie discrete transitions as you want in GU).

Okay

Thought for 11s

Perfect --- then we do the next step: **calibration** (so that our Universe comes out exactly) and then we add **memory** as a controlled warp around the $X_{\text{critical},n}$ thresholds.

**1) Minimum calibration** $\mathbf{T(n)}$**of two anchors (QCD and recombination)**
We take the anchors we already use:

- QCD/QGP: $n_{QCD} = 95$, $T_{QCD} \approx 0.16\text{ GeV}$

- recombination: $n_{rec} = 128$, $T_{rec} \approx 1\text{ eV} = 10^{- 9}\text{ GeV}$

In the RD regime, with $\kappa = \frac{dn}{dN}$ approximately constant over a large interval:

$$T(n) = T_{QCD}\text{ }\exp\text{ ⁣}\left( -\frac{n - n_{QCD}}{\kappa} \right)$$

We calibrate $\kappa$ from the two points:

$$\kappa_{avg} = \frac{n_{rec} - n_{QCD}}{\ln\text{ ⁣}\left( T_{QCD}/T_{rec} \right)} = \frac{33}{\ln(0.16/10^{- 9})} \approx \frac{33}{18.89} \approx 1.746$$

So the **minimum model** that exactly reproduces the thermal history between QCD and recombination is:

$$\boxed{T(n) = 0.16\text{ GeV} \cdot \exp\text{ ⁣}\left( -\frac{n - 95}{1.746} \right)}$$

and indeed at $n = 128$ it gives $T \simeq 1\text{ eV}$.
**2) Now we add the memory:** $\mathbf{\kappa(n)}$**is no longer constant, but "curves" at the thresholds**

We already have the general formula:

$$\frac{d\ln T}{dn} \simeq - \frac{1}{\kappa(n)},\ln\frac{T(n)}{T(n_{0})} \simeq - \int_{n_{0}}^{n}\frac{dn'}{\kappa(n')}$$

So the "memory" basically comes in as:

$$\boxed{\kappa(n) = \kappa_{0} + \Delta\kappa(n)}\text{where}\kappa_{0} \approx 1.746$$

**A GU-friendly choice for "snap" at thresholds (pulses around** $\mathbf{n}$**)**

You use the thresholds:

$$X_{\text{critical},n} = X_{0}\varphi^{- n} \Rightarrow n(X) = {\log}_{\varphi}(X_{0}/X)$$

and you set the memory to be strong only near certain epochs (QCD, EW, etc.):

$$\boxed{\Delta\kappa(n) = \sum_{j \in \{\text{EW,QCD,...}\}}^{}A_{j}\text{ }\exp\text{ ⁣}\left( -\frac{\left( n-n_{j})^{2} \right.\ }{2\sigma_{j}^{2}} \right)}$$
- $A_{j} > 0$: "accelerate" the ticks (decrease $T$ by $n$ faster)

- $A_{j} < 0$: "slow down" (plateau/delay)

- $\sigma_{j}$: how "sharp" is the transition (snap)

This is exactly the mechanism by which you can make the transitions more **discrete** (as you want in GU) without breaking the global calibration.

**3) GU memory in local form (without integral)**

We define the memory variable:

$$M(t) = \int_{0}^{t}e^{- \beta(X)(t - \tau)}\text{ }H\lbrack\Omega(\tau)\rbrack\text{ }d\tau$$

which becomes ODE:

$$\boxed{\dot{M} = H\lbrack\Omega(t)\rbrack - \beta(X)M}$$

Then a law of $\kappa$ (simple, efficient):
$$\boxed{\kappa(n) = \kappa_{0}(1 + \alpha\text{ }M(n))}$$

with $\alpha$small (to be a fix, not a total rewrite).

**4) What do we do immediately after this "Ok"**

Concretely, the next step is to choose **2--3 thresholds** where you want to "snap" (eg QCD at $n = 95$, recombination is only anchor, maybe EW at another $n$ from GU) and set:

- $\kappa_{0} = 1.746$

- $\Delta\kappa(n)$as 1--2 pulses (amplitude + width)

This gives you:

1. $T(n)$complete (with memory),

2. "how suddenly" the transitions happen,

3. how it aligns with "Pattern k=2 QCD epoch" from GU.
If you want, in the next message I can directly write you a simple numerical set (eg a pulse at $n = 95$ with $\sigma = 0.7$, small amplitude) and the result: how $T(n)$changes locally without breaking the global anchors.
