# 05 Control Law Derivation

## Objective
Maintain lock while maximizing decodable separation between symbols.

## Closed-Loop Law

- `u_tx = K_p e + K_i int e dt + K_d de/dt`
- `e = theta_ref - theta_rx`

## Stability Constraints

Given `L(s) = C(s)H_eff(s)`:
- gain margin `GM >= GM_min`
- phase margin `PM >= PM_min`
- lock settling time `t_settle <= t_settle_max`

Controller tuning rule:
- increase `K_p` to reduce tracking error
- increase `K_i` until steady-state bias removed
- cap `K_d` to avoid noise amplification
