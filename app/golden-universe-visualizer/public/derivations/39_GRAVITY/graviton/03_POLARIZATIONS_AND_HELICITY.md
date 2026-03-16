# Polarizations and Helicity

**Massless spin-2 has exactly two polarization states: helicity ±2**

---

## 1. Degrees of Freedom Counting

A symmetric rank-2 tensor $h_{\mu\nu}$ in 4D has **10** independent components.

**Gauge freedom** (4 functions $\xi_\mu$): removes 4 degrees of freedom → **6** remaining.

**Residual gauge** (e.g., harmonic/De Donder gauge $\partial^\mu \bar{h}_{\mu\nu} = 0$): removes 4 more → **2** physical degrees of freedom.

**Conclusion**: The massless spin-2 graviton has **2** physical polarizations.

---

## 2. Traceless-Transverse (TT) Gauge

In the **traceless-transverse** gauge:
- **Transverse**: $\partial^\mu h_{\mu\nu} = 0$
- **Traceless**: $h = \eta^{\mu\nu} h_{\mu\nu} = 0$

For a plane wave $h_{\mu\nu}(x) = \epsilon_{\mu\nu}(k) e^{ik\cdot x}$ propagating in the $z$-direction ($k^\mu = (\omega/c, 0, 0, k)$):
- $k^\mu \epsilon_{\mu\nu} = 0$ (transverse)
- $\eta^{\mu\nu} \epsilon_{\mu\nu} = 0$ (traceless)

The only non-vanishing components are $\epsilon_{xx}$, $\epsilon_{yy}$, $\epsilon_{xy}$, with $\epsilon_{xx} = -\epsilon_{yy}$ (traceless). This leaves **2** independent amplitudes.

---

## 3. Helicity States

Under a rotation by angle $\theta$ around the propagation axis (e.g., $z$), a massless particle of helicity $s$ picks up a phase $e^{i s \theta}$.

For spin-2:
- **Helicity +2**: $\epsilon^{(+)}_{\mu\nu}$ (plus polarization)
- **Helicity −2**: $\epsilon^{(\times)}_{\mu\nu}$ (cross polarization)

These correspond to the **+, ×** polarizations observed in gravitational wave detectors (LIGO, Virgo, KAGRA).

---

## 4. Lorentz Group Representation

For massless particles in 4D, the little group is $\text{ISO}(2)$ (E(2)). The representation is labeled by **helicity** $s$. For spin-2, $s = \pm 2$. There are no $s = 0$ or $s = \pm 1$ modes for a pure spin-2 field—they are removed by gauge symmetry.

---

## 5. Summary

| Property | Value | Origin |
|----------|-------|--------|
| **Polarizations** | 2 | 10 − 4 (gauge) − 4 (residual) = 2 |
| **Helicity** | ±2 | Spin-2, massless |
| **Names** | +, × | Plus and cross tensor modes |
| **GW observation** | Consistent | LIGO/Virgo tensor polarizations |

---

## References

- Weinberg, S. (1972). *Gravitation and Cosmology*. Wiley.
- Maggiore, M. (2007). *Gravitational Waves*. Oxford University Press.
