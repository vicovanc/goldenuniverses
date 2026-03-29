#!/usr/bin/env python3
"""
Stage 08: operating-region phase diagram from channel and guardrail constraints.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import importlib.util
from pathlib import Path
from typing import Dict

_COMMON_PATH = Path(__file__).with_name("00_common.py")
_SPEC = importlib.util.spec_from_file_location("instant_common", _COMMON_PATH)
_COMMON = importlib.util.module_from_spec(_SPEC)
assert _SPEC and _SPEC.loader
_SPEC.loader.exec_module(_COMMON)

write_report = _COMMON.write_report


@dataclass
class Config:
    grad_theta_min: float = 0.08
    grad_theta_max: float = 0.22
    memory_depth_min: float = 0.45
    memory_depth_max: float = 0.9
    scan_points: int = 25
    seed: str = "deterministic_by_construction"


def run(cfg: Config) -> Dict[str, object]:
    viable = 0
    total = cfg.scan_points * cfg.scan_points
    for i in range(cfg.scan_points):
        g = i / (cfg.scan_points - 1)
        for j in range(cfg.scan_points):
            m = j / (cfg.scan_points - 1)
            in_grad = cfg.grad_theta_min <= g <= cfg.grad_theta_max
            in_mem = cfg.memory_depth_min <= m <= cfg.memory_depth_max
            if in_grad and in_mem:
                viable += 1
    frac = viable / total
    if frac <= 0.05:
        class_label = "not viable"
    elif frac <= 0.35:
        class_label = "viable only in constrained window"
    else:
        class_label = "broadly viable"
    return {
        "model": "phase_diagram_and_operating_regions",
        "config": asdict(cfg),
        "summary": {
            "viable_window_fraction": round(frac, 6),
            "viability_classification": class_label,
            "viable_points": viable,
            "total_points": total,
        },
        "operating_window": {
            "grad_theta": [cfg.grad_theta_min, cfg.grad_theta_max],
            "memory_depth": [cfg.memory_depth_min, cfg.memory_depth_max],
        },
    }


def main() -> None:
    out = write_report(__file__, run(Config()))
    print(f"[08] wrote {out}")


if __name__ == "__main__":
    main()
