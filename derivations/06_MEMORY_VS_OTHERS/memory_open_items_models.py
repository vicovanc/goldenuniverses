#!/usr/bin/env python3
"""
Shared models for GU memory open items (Workstream A).

Provides:
  1) Dark-sector non-perturbative scattering coefficient model
  2) Memory-coupled Boltzmann network for baryogenesis
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


PHI = (1.0 + np.sqrt(5.0)) / 2.0
PI = np.pi
LAMBDA_RATIO = np.exp(PHI) / (PI ** 2)


def gu_dark_scattering_coefficient() -> float:
    """Deterministic GU coefficient for non-perturbative dark scattering.

    Uses only GU constants (phi, pi) and no tunable fit parameters:
      C_GU = exp(-2*pi/phi^2) * phi^-7
    """
    return float(np.exp(-2.0 * PI / (PHI ** 2)) * (PHI ** -7.0))


def sigma_over_m_velocity_profile(
    sigma_over_m_contact: float,
    velocities_kms: list[float],
) -> dict:
    """Velocity-dependent sigma/m profile from GU coefficient model."""
    c_gu = gu_dark_scattering_coefficient()
    v0_kms = 40.0 * (PHI ** 2)  # ~105 km/s, deterministic GU scale

    values = {}
    for v in velocities_kms:
        suppression = 1.0 / (1.0 + (v / v0_kms) ** 2)
        values[str(int(v))] = {
            "velocity_kms": float(v),
            "sigma_over_m_cm2_per_g": float(sigma_over_m_contact * c_gu * suppression),
            "suppression_factor": float(suppression),
        }

    # Theory uncertainty from model simplification (not a fit uncertainty).
    rel_unc = 0.35
    return {
        "C_GU_nonperturbative": c_gu,
        "v0_kms": float(v0_kms),
        "relative_uncertainty": rel_unc,
        "profiles": values,
    }


@dataclass
class BoltzmannConfig:
    n_start: float = 0.0
    n_end: float = 80.0
    yx0: float = 1.0
    ybl0: float = 0.0
    yb0: float = 0.0
    m0: float = 0.0
    k_decay: float = 0.9
    k_washout: float = 0.8
    cp_epsilon0: float = 4.8e-6
    source_norm: float = 2.0e-3
    sphaleron_factor: float = 28.0 / 79.0
    entropy_dilution0: float = 8.0
    beta_mem: float = 1.0
    a_mem_source: float = 0.08
    a_mem_washout: float = 0.10


def solve_memory_coupled_boltzmann(cfg: BoltzmannConfig | None = None) -> dict:
    """Solve a reduced full-network baryogenesis model with memory coupling.

    State vector y = [Y_X, Y_BmL, Y_B, M]
      - Y_X: out-of-equilibrium heavy species abundance
      - Y_BmL: generated B-L asymmetry
      - Y_B: baryon asymmetry
      - M: memory variable
    """
    if cfg is None:
        cfg = BoltzmannConfig()

    def rhs(_n, y):
        yx, ybml, yb, mem = y
        mem_eff = mem / (1.0 + abs(mem))
        eps_eff = cfg.cp_epsilon0 * (1.0 + cfg.a_mem_source * mem_eff)
        washout_eff = cfg.k_washout * (1.0 + cfg.a_mem_washout * max(mem_eff, 0.0))
        src = cfg.source_norm * eps_eff * cfg.k_decay * yx

        dyx = -cfg.k_decay * yx
        dybml = src - washout_eff * ybml
        dyb = cfg.sphaleron_factor * (ybml - yb) / max(cfg.entropy_dilution0, 1e-12)
        dmem = yx - cfg.beta_mem * mem
        return [dyx, dybml, dyb, dmem]

    y0 = [cfg.yx0, cfg.ybl0, cfg.yb0, cfg.m0]
    n_eval = np.linspace(cfg.n_start, cfg.n_end, 1200)
    sol = solve_ivp(rhs, (cfg.n_start, cfg.n_end), y0, t_eval=n_eval, rtol=1e-8, atol=1e-10)

    yx = sol.y[0]
    ybml = sol.y[1]
    yb = sol.y[2]
    mem = sol.y[3]
    eta_b = 7.04 * yb[-1]

    # Reference run with memory disabled for sensitivity.
    cfg_nomem = BoltzmannConfig(**{**cfg.__dict__, "a_mem_source": 0.0, "a_mem_washout": 0.0})
    sol_nomem = solve_ivp(
        lambda _n, y: [
            -cfg_nomem.k_decay * y[0],
            cfg_nomem.source_norm * cfg_nomem.cp_epsilon0 * cfg_nomem.k_decay * y[0] - cfg_nomem.k_washout * y[1],
            cfg_nomem.sphaleron_factor * (y[1] - y[2]) / max(cfg_nomem.entropy_dilution0, 1e-12),
            y[0] - cfg_nomem.beta_mem * y[3],
        ],
        (cfg_nomem.n_start, cfg_nomem.n_end),
        [cfg_nomem.yx0, cfg_nomem.ybl0, cfg_nomem.yb0, cfg_nomem.m0],
        t_eval=n_eval,
        rtol=1e-8,
        atol=1e-10,
    )
    eta_b_nomem = 7.04 * sol_nomem.y[2][-1]

    return {
        "eta_B": float(eta_b),
        "eta_B_no_memory": float(eta_b_nomem),
        "memory_fractional_shift": float((eta_b - eta_b_nomem) / max(abs(eta_b_nomem), 1e-30)),
        "final_state": {
            "Y_X": float(yx[-1]),
            "Y_BmL": float(ybml[-1]),
            "Y_B": float(yb[-1]),
            "M": float(mem[-1]),
        },
        "config": cfg.__dict__,
        "grid": {
            "N_start": float(cfg.n_start),
            "N_end": float(cfg.n_end),
            "points": int(len(n_eval)),
        },
    }


def write_json_report(payload: dict, out_path: str) -> None:
    path = Path(out_path)
    data = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        **payload,
    }
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

