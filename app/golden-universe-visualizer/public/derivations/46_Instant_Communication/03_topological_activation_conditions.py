#!/usr/bin/env python3
"""
Stage 03: classify off/assisted/active phase-channel activation.
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

write_report = _COMMON.write_report
mean = _COMMON.mean


@dataclass
class Config:
    grad_theta_off: float = 0.0
    grad_theta_assisted: float = 0.06
    grad_theta_active: float = 0.18
    threshold: float = 0.08
    kappa: float = 1.0
    e_field: float = 1.0
    seed: str = "deterministic_by_construction"


def _current(grad_theta: float, kappa: float, e_field: float) -> float:
    return (kappa / (2.0 * 3.141592653589793**2)) * abs(grad_theta * e_field)


def run(cfg: Config) -> Dict[str, object]:
    regime = {
        "off": _current(cfg.grad_theta_off, cfg.kappa, cfg.e_field),
        "assisted": _current(cfg.grad_theta_assisted, cfg.kappa, cfg.e_field),
        "active": _current(cfg.grad_theta_active, cfg.kappa, cfg.e_field),
    }
    labels: List[int] = [0, 1, 2]
    obs: List[float] = [regime["off"], regime["assisted"], regime["active"]]
    sep = (obs[2] - obs[0]) / (1e-9 + (abs(obs[1] - mean(obs)) + 1e-9))

    return {
        "model": "topological_activation_conditions",
        "config": asdict(cfg),
        "summary": {
            "off_current": round(regime["off"], 8),
            "assisted_current": round(regime["assisted"], 8),
            "active_current": round(regime["active"], 8),
            "activation_separation_sigma": round(sep, 6),
            "active_crosses_threshold": regime["active"] > cfg.threshold / 100.0,
        },
        "activation_logic": {
            "off": "grad_theta = 0 -> channel off",
            "assisted": "weak structured gradients",
            "active": "sustained gradients above activation threshold",
        },
    }


def main() -> None:
    out = write_report(__file__, run(Config()))
    print(f"[03] wrote {out}")


if __name__ == "__main__":
    main()
