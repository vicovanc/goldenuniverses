#!/usr/bin/env python3
"""
Stage 02: memory-channel equation system and effective channel gain.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import importlib.util
from pathlib import Path
from typing import Dict, List

_COMMON_PATH = Path(__file__).with_name("00_common.py")
_SPEC = importlib.util.spec_from_file_location("instant_common", _COMMON_PATH)
_COMMON = importlib.util.module_from_spec(_SPEC)
assert _SPEC and _SPEC.loader
_SPEC.loader.exec_module(_COMMON)

LAMBDA_REC_OVER_BETA = _COMMON.LAMBDA_REC_OVER_BETA
write_report = _COMMON.write_report


@dataclass
class Config:
    dt: float = 0.05
    total_t: float = 40.0
    beta: float = 1.0
    drive_amp: float = 0.8
    kappa: float = 1.0
    seed: str = "deterministic_by_construction"


def run(cfg: Config) -> Dict[str, object]:
    n = int(cfg.total_t / cfg.dt)
    r_mem = 0.0
    theta_grad = 0.0
    channel_gain_samples: List[float] = []

    for i in range(n):
        t = i * cfg.dt
        rho = 0.4 + 0.3 * (1.0 + __import__("math").sin(0.25 * t)) / 2.0
        source = rho**4
        dr = source - cfg.beta * r_mem
        r_mem += cfg.dt * dr

        # phase memory proxy responds to accumulated memory
        theta_grad = 0.85 * theta_grad + 0.15 * (cfg.drive_amp * r_mem)
        j_theta = (cfg.kappa / (2.0 * 3.141592653589793**2)) * theta_grad
        channel_gain_samples.append(j_theta)

    channel_gain_nominal = sum(channel_gain_samples) / len(channel_gain_samples)
    return {
        "model": "memory_channel_equations",
        "config": asdict(cfg),
        "summary": {
            "r_mem_final": round(r_mem, 6),
            "theta_grad_final": round(theta_grad, 6),
            "channel_gain_nominal": round(channel_gain_nominal, 6),
            "lambda_rec_over_beta": round(LAMBDA_REC_OVER_BETA, 6),
        },
        "equations": {
            "memory_local_form": "dR/dt + beta*R = rho^4",
            "current_form": "J_theta ~ (kappa/2pi^2)*(d_mu theta)Ftilde",
        },
    }


def main() -> None:
    out = write_report(__file__, run(Config()))
    print(f"[02] wrote {out}")


if __name__ == "__main__":
    main()
