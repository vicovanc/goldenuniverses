# 01 Equation Stack

## Core Stack

1. Memory kernel:
   - `dR/dt + beta R = rho^4`
2. Phase-coupled transport:
   - `d_mu F^{mu nu} = J^nu + (kappa/2pi^2)(d_mu theta)Ftilde^{mu nu}`
3. Effective channel form:
   - `y_rx = H(theta, R, g, n) * u_tx + n_rx`
4. Control closure:
   - `u_tx = K_p e + K_d de/dt + K_i int e dt`

## Device-State Vector

`x = [theta_tx, theta_rx, R_tx, R_rx, g_hat, lock_err]`

## Gate-Critical Derived Metrics

- `SNR_db`
- `BER`
- `balanced_accuracy`
- `session_lock_time`
- `viable_window_fraction`
