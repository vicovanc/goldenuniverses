# 04 Transfer Function Derivation

Assume reduced linearized dynamics around operating point:

- `theta_rx_dot = a_theta theta_rx + b_theta u_tx + d_theta R_rx + w`
- `R_rx_dot = -beta R_rx + c_r rho^4`

Laplace transform gives:

- `Theta_rx(s) = G_theta(s) U_tx(s) + G_r(s) R_rx(s) + W(s)`
- `G_theta(s) = b_theta / (s - a_theta)`
- `G_r(s) = d_theta / (s - a_theta)`
- `R_rx(s) = (c_r/(s+beta)) Rho4(s)`

Effective transfer:

- `H_eff(s) = G_theta(s) + G_r(s)*c_r/(s+beta)`

Design implication:
- choose operating region where `|H_eff(jw)|` is high and stable over target band.
