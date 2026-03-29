#!/usr/bin/env python3
"""
Stage 06: benchmark off/assisted/active scenarios.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import importlib.util
from pathlib import Path
from typing import Dict
import math

_COMMON_PATH = Path(__file__).with_name("00_common.py")
_SPEC = importlib.util.spec_from_file_location("instant_common", _COMMON_PATH)
_COMMON = importlib.util.module_from_spec(_SPEC)
assert _SPEC and _SPEC.loader
_SPEC.loader.exec_module(_COMMON)

write_report = _COMMON.write_report


@dataclass
class Config:
    noise_floor: float = 0.02
    off_amp: float = 0.0
    assisted_amp: float = 0.05
    active_amp: float = 0.16
    seed: str = "deterministic_by_construction"


def _snr_db(signal_amp: float, noise_floor: float) -> float:
    p_sig = signal_amp * signal_amp + 1e-12
    p_noise = noise_floor * noise_floor + 1e-12
    return 10.0 * math.log10(p_sig / p_noise)


def run(cfg: Config) -> Dict[str, object]:
    off_snr = _snr_db(cfg.off_amp, cfg.noise_floor)
    assisted_snr = _snr_db(cfg.assisted_amp, cfg.noise_floor)
    active_snr = _snr_db(cfg.active_amp, cfg.noise_floor)
    return {
        "model": "benchmark_scenarios",
        "config": asdict(cfg),
        "summary": {
            "off_snr_db": round(off_snr, 6),
            "assisted_snr_db": round(assisted_snr, 6),
            "active_snr_db": round(active_snr, 6),
            "active_detectable": bool(active_snr > 0.0),
        },
        "regimes": ["off", "assisted", "active"],
    }


def main() -> None:
    out = write_report(__file__, run(Config()))
    print(f"[06] wrote {out}")


if __name__ == "__main__":
    main()
