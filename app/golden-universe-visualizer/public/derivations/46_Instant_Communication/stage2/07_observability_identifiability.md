# 07 Observability and Identifiability

## Observability

For linearized model `x_dot = Ax + Bu`, `y = Cx`:
- rank condition: `rank([C; CA; ...; CA^(n-1)]) = n`

## Identifiability

Parameter vector:
- `p = [a_theta, b_theta, d_theta, beta, c_r]`

Local identifiability condition:
- Fisher information matrix `F = J^T W J` is full rank
- confidence intervals for key parameters below tolerance bounds

## Stage2 Rule

No threshold promotion if:
- observability rank fails, or
- `cond(F)` exceeds limit, or
- confidence bands overlap null-model zone.
