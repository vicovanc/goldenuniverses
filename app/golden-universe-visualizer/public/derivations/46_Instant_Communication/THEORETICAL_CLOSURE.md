# Theoretical Closure for Device Equations

## Purpose

Translate GU entanglement and topology equations into explicit transmitter,
receiver, channel, and measurement variables for a point-to-point device.

## Canonical Equation Set

1. Geometric initialization:
   - `Omega_0 -> Z1 + Z2 = 0`
   - winding geometry: `L_Omega(p,q) = 2pi sqrt(p^2 + q^2/phi^2)`
   - corrected resonance gate: `k_res = round(N/phi^2)`, pass when even and `|delta| < 0.5`
2. Memory channel:
   - `R_mem(t) = int rho^4(tau) exp[-beta(t-tau)] dtau`
   - local form: `dR_mem/dt + beta R_mem = rho^4`
3. Phase transport:
   - `d_mu F^{mu nu} = J^nu + (kappa/2pi^2) (d_mu theta) Ftilde^{mu nu}`
   - `J_theta = (kappa/2pi^2) (theta_dot B + grad(theta) x E)`

## Device-State Model

Define a reduced state:

- `x = [theta_tx, theta_rx, R_tx, R_rx, g_hat, lock_err]`

with dynamics:

- `dR_tx/dt = rho_tx^4 - beta_tx R_tx`
- `dR_rx/dt = rho_rx^4 - beta_rx R_rx`
- `dtheta_tx/dt = u_mod(t) - d_lock * lock_err`
- `dtheta_rx/dt = H_chan(x, p) + n(t)`
- `dg_hat/dt = eta_g * (y_rx - g_hat * s_ref)`

where `H_chan` is the effective phase-memory transfer law.

## Hardware-Observable Mapping

- `u_mod`: transmitter modulation drive
- `y_rx`: receiver demodulated observable
- `g_hat`: online channel-gain estimate
- `lock_err`: synchronization phase error
- `n(t)`: aggregate noise (thermal + electronic + environmental + leakage residual)

## Communication Variables

- `SNR_db = 10 log10(P_signal / P_noise)`
- `BER = bit_errors / bits_total`
- `latency_proxy = t_decode - t_symbol_emit - t_baseline_path`
- `session_lock_time = first t such that |lock_err| < eps_lock for T_hold`

## Modulation Families

1. Phase-shift keying:
   - binary symbol `b in {0,1}` mapped to `u_mod = +/-A`
2. Spread-phase coding:
   - `u_mod = A c_k`, `c_k in {-1,+1}` pseudo-noise code
3. Adaptive hybrid:
   - policy chooses PSK/spread based on `g_hat`, `lock_err`, and measured SNR

## Control Invariants

- `I1`: lock stability margin > threshold
- `I2`: memory depth floor `R_mem >= R_min`
- `I3`: gradient persistence `P(|grad(theta)| > g_min) >= p_min`
- `I4`: finite energy budget in active operation

## Measurable Claims (Machine-Gated)

- detectability: `SNR_db > 0` under blinded conditions
- communication viability: `BER <= target_ber`
- robust lock: `session_lock_time <= target_lock_s`
- aggressive claim gate: only if reproducible across independent labs

## Non-Negotiable Guardrails

- keep explicit null runs with channel-off setting (`grad(theta) = 0`)
- record leakage controls and dummy channels for each run
- any positive result requires holdout and blinded replication
