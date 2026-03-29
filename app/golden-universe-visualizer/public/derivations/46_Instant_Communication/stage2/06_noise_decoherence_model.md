# 06 Noise and Decoherence Model

## Noise Sources

- instrumental: ADC/DAC quantization and amplifier noise
- environmental: thermal/vibration/EM pickup
- channel: memory depth fluctuations and phase drift

## Model

- `y_rx = H_eff u_tx + n_inst + n_env + n_dec`
- `sigma_tot^2 = sigma_inst^2 + sigma_env^2 + sigma_dec^2`
- `SNR = P_sig / sigma_tot^2`

Decoherence proxy:

- `sigma_dec = a_d * exp(b_d * T_run) * f_grad`

Requirement:
- choose protocol duration and operating point keeping `SNR_db >= threshold`.
