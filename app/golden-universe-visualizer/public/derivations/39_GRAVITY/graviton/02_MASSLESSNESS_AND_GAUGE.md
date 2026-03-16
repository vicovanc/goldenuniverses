# Masslessness and Gauge Invariance

**Diffeomorphism invariance forbids a graviton mass**

---

## 1. Linearized Diffeomorphisms

General Relativity is invariant under diffeomorphisms (coordinate transformations). In the linearized limit, an infinitesimal coordinate transformation $x^\mu \to x^\mu + \xi^\mu$ induces:

$$h_{\mu\nu} \to h_{\mu\nu} + \partial_\mu \xi_\nu + \partial_\nu \xi_\mu$$

This is the **gauge symmetry** of linearized gravity. The perturbation $h_{\mu\nu}$ is only defined up to this transformation.

---

## 2. Why the Graviton Must Be Massless

A naive mass term for $h_{\mu\nu}$ would be:

$$S_{\text{mass}} = -\frac{m^2}{2} \int d^4x \left( h_{\mu\nu} h^{\mu\nu} - \alpha h^2 \right)$$

For generic $\alpha$, this term is **not** invariant under $h_{\mu\nu} \to h_{\mu\nu} + \partial_\mu \xi_\nu + \partial_\nu \xi_\mu$. Under this transformation:

$$\delta S_{\text{mass}} = -m^2 \int d^4x \, h^{\mu\nu} (\partial_\mu \xi_\nu + \partial_\nu \xi_\mu) + \ldots \neq 0$$

Therefore:

**Conclusion**: Gauge invariance (linearized diffeomorphism invariance) **forbids** any mass term for $h_{\mu\nu}$. The graviton must be **massless**.

---

## 3. Fierz-Pauli Tuning (Massive Case)

For a *massive* spin-2 field, Fierz and Pauli showed that the only ghost-free mass term has the specific form $h_{\mu\nu}h^{\mu\nu} - h^2$ (with $\alpha = 1$). However:
- This breaks gauge invariance
- The massless limit $m \to 0$ does not smoothly recover GR (vDVZ discontinuity)
- Observations (gravitational waves, Newton's law) are consistent with **massless** graviton

---

## 4. Physical Consequences of Masslessness

1. **Long-range force**: A massless mediator yields a $1/r$ potential (Newton's law)
2. **Speed of propagation**: Massless particles travel at $c$—consistent with GW170817 (gravitational waves and gamma rays arrived within 1.7 s over 140 Mpc)
3. **No Yukawa suppression**: No exponential decay $\sim e^{-mr}$ of the gravitational potential

---

## 5. Summary

| Property | Origin |
|----------|--------|
| **Masslessness** | Gauge invariance (diffeomorphism) forbids $m^2 h^2$ |
| **Long-range** | Massless mediator → $1/r$ potential |
| **Propagation at c** | Massless → null geodesics |

---

## References

- Fierz, M. & Pauli, W. (1939). On relativistic wave equations for particles of arbitrary spin.
- van Dam, H. & Veltman, M. (1970). Massive and massless Yang-Mills and gravitational fields. *Nuclear Physics B* **22**, 397–411.
