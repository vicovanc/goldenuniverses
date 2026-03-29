# 03 Dimensionless Groups

## Primary Groups

- Memory number:
  - `Pi_M = beta * T_obs`
- Activation number:
  - `Pi_A = |grad(theta)| / g_ref`
- Gain-noise number:
  - `Pi_GN = g_hat / sigma_n`
- Lock margin number:
  - `Pi_L = eps_lock / |lock_err|`

## Usage

- `Pi_A > 1` required for active regime qualification.
- `Pi_GN` maps directly to detectability and BER behavior.
- `Pi_L > 1` indicates stable lock envelope.
