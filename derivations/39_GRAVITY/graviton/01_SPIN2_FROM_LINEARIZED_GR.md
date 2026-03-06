# Spin-2 from Linearized General Relativity

**Standard Physics Derivation — No GU-specific claims**

---

## 1. Linearized Gravity

General Relativity describes gravity as spacetime curvature. In the weak-field limit, we expand the metric around Minkowski spacetime:

$$g_{\mu\nu} = \eta_{\mu\nu} + h_{\mu\nu}$$

where:
- $\eta_{\mu\nu} = \text{diag}(-1,+1,+1,+1)$ is the Minkowski metric
- $|h_{\mu\nu}| \ll 1$ is the perturbation

The inverse metric to first order is:
$$g^{\mu\nu} = \eta^{\mu\nu} - h^{\mu\nu}$$

where indices on $h$ are raised with $\eta$.

---

## 2. Einstein-Hilbert Action Expansion

The Einstein-Hilbert action is:

$$S_{\text{EH}} = \frac{c^4}{16\pi G_N} \int d^4x \, \sqrt{-g} \, R$$

Expanding to second order in $h_{\mu\nu}$ (see e.g. Carroll 2004, Wald 1984):

1. **Christoffel symbols** (first order):
$$\Gamma^\lambda_{\mu\nu} = \frac{1}{2}\eta^{\lambda\rho}(\partial_\mu h_{\nu\rho} + \partial_\nu h_{\mu\rho} - \partial_\rho h_{\mu\nu})$$

2. **Riemann tensor** (first order in $h$):
$$R_{\mu\nu\rho\sigma} \sim \partial\partial h$$

3. **Ricci scalar** (first order):
$$R \sim \partial^\mu\partial^\nu h_{\mu\nu} - \Box h$$

4. **Second-order effective action** for $h_{\mu\nu}$:
$$S^{(2)} = \frac{c^4}{64\pi G_N} \int d^4x \left[ \partial_\lambda h_{\mu\nu} \partial^\lambda h^{\mu\nu} - 2 \partial_\mu h^{\mu\nu} \partial^\lambda h_{\lambda\nu} + 2 \partial^\mu h \partial^\nu h_{\mu\nu} - \partial^\mu h \partial_\mu h \right]$$

where $h = \eta^{\mu\nu} h_{\mu\nu}$ is the trace.

---

## 3. Fierz-Pauli Action

The unique Lorentz-invariant action for a **massless spin-2 field** was derived by Fierz and Pauli (1939). After gauge fixing (see next document), the free graviton action takes the form:

$$S_{\text{FP}} = -\frac{1}{2} \int d^4x \left[ \partial_\lambda h_{\mu\nu} \partial^\lambda h^{\mu\nu} - \frac{1}{2} \partial_\lambda h \partial^\lambda h \right]$$

**Key result**: The linearized Einstein-Hilbert action, expanded to second order in $h_{\mu\nu}$, *is* the Fierz-Pauli action (up to overall normalization and gauge-fixing terms). There are **no free parameters**—the structure is fixed entirely by:
- General covariance (diffeomorphism invariance)
- The Einstein field equations

---

## 4. Spin-2 Identification

A symmetric rank-2 tensor $h_{\mu\nu}$ in 4D has $10$ components. Under the Lorentz group $\text{SO}(1,3)$, a symmetric traceless tensor transforms in the **spin-2 representation**.

**Fierz-Pauli theorem** (modern formulation): The only consistent Lorentz-invariant action for a massless particle of spin 2 that couples to a conserved source $T_{\mu\nu}$ is the linearized Einstein-Hilbert action. Any deviation (e.g., a mass term) breaks gauge invariance and introduces pathologies (e.g., Boulware-Deser ghost for massive spin-2).

---

## 5. Summary

| Property | Derivation |
|----------|------------|
| **Spin-2** | Symmetric $h_{\mu\nu}$; Lorentz representation theory |
| **Action** | Unique (Fierz-Pauli) from linearized GR |
| **Free parameters** | None—fixed by GR and gauge symmetry |

---

## References

- Fierz, M. & Pauli, W. (1939). On relativistic wave equations for particles of arbitrary spin in an electromagnetic field. *Proc. R. Soc. Lond. A* **173**, 211–232.
- Carroll, S. (2004). *Spacetime and Geometry*. Addison Wesley.
- Wald, R. (1984). *General Relativity*. University of Chicago Press.
