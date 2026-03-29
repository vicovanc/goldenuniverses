# 03 Physics Engine Spec

## Equation contract

From Stage2 equation stack:

- memory: `dR/dt + beta R = rho^4`
- phase-coupled EM: `d_mu F^{mu nu} = J^nu + (kappa/2pi^2)(d_mu theta)Ftilde^{mu nu}`
- effective channel: `y_rx = H(theta, R, g, n) * u_tx + n_rx`
- control: `u_tx = K_p e + K_i int(e dt) + K_d de/dt`

## State vector

`x = [theta_tx, theta_rx, R_tx, R_rx, g_hat, lock_err]`

## Computed outputs

- run-level metrics: `SNR_db`, `BER`, `balanced_accuracy`, `session_lock_time`, `viable_window_fraction`
- trial-level outputs: decoded symbol, confidence, lock status
- diagnostics: drift rates, residual errors, observability warnings

## Constraints

- all hardware thresholds must map to this equation layer
- unsupported heuristic parameters are marked and blocked from promotion
