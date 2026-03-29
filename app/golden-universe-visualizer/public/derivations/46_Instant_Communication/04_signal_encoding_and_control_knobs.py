#!/usr/bin/env python3
"""
Stage 04: model encoding and control knobs for conditional signaling.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import importlib.util
from pathlib import Path
from typing import Dict, List
import math

_COMMON_PATH = Path(__file__).with_name("00_common.py")
_SPEC = importlib.util.spec_from_file_location("instant_common", _COMMON_PATH)
_COMMON = importlib.util.module_from_spec(_SPEC)
assert _SPEC and _SPEC.loader
_SPEC.loader.exec_module(_COMMON)

write_report = _COMMON.write_report


@dataclass
class Config:
    steps: int = 120
    gain: float = 1.2
    damping: float = 0.15
    phase_lock: float = 0.75
    seed: str = "deterministic_by_construction"


def run(cfg: Config) -> Dict[str, object]:
    theta = 0.0
    decoded: List[float] = []
    symbols = [1, 0, 1, 1, 0, 0, 1, 0]
    for i in range(cfg.steps):
        bit = symbols[i % len(symbols)]
        drive = (2 * bit - 1) * cfg.gain
        theta = (1.0 - cfg.damping) * theta + drive * cfg.phase_lock
        noisy = theta + 0.02 * math.sin(i * 0.31)
        decoded_bit = 1.0 if noisy > 0 else 0.0
        decoded.append(decoded_bit == bit)
    control_stability = sum(1.0 for ok in decoded if ok) / len(decoded)

    return {
        "model": "signal_encoding_and_control_knobs",
        "config": asdict(cfg),
        "summary": {
            "control_stability_index": round(control_stability, 6),
            "symbol_error_rate": round(1.0 - control_stability, 6),
            "final_theta_state": round(theta, 6),
        },
        "knobs": ["gain", "damping", "phase_lock"],
    }


def main() -> None:
    out = write_report(__file__, run(Config()))
    print(f"[04] wrote {out}")


if __name__ == "__main__":
    main()
