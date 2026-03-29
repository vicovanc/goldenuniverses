#!/usr/bin/env python3
"""
Sim 02: sweep noise and decoherence to map robust operating band.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import importlib.util
from pathlib import Path
import json

_COMMON_PATH = Path(__file__).resolve().parents[1] / "00_common.py"
_SPEC = importlib.util.spec_from_file_location("instant_common", _COMMON_PATH)
_COMMON = importlib.util.module_from_spec(_SPEC)
assert _SPEC and _SPEC.loader
_SPEC.loader.exec_module(_COMMON)


@dataclass
class Config:
    base_gain: float = 0.12
    memory_depth: float = 0.72
    noise_min: float = 0.01
    noise_max: float = 0.08
    decoh_min: float = 0.0
    decoh_max: float = 0.4
    grid: int = 21
    seed: str = "deterministic_by_construction"


def run(cfg: Config) -> dict:
    viable = 0
    total = cfg.grid * cfg.grid
    for i in range(cfg.grid):
        n = cfg.noise_min + (cfg.noise_max - cfg.noise_min) * i / (cfg.grid - 1)
        for j in range(cfg.grid):
            d = cfg.decoh_min + (cfg.decoh_max - cfg.decoh_min) * j / (cfg.grid - 1)
            gain_eff = cfg.base_gain * cfg.memory_depth * (1.0 - d)
            snr_db = 10.0 * __import__("math").log10((gain_eff**2 + 1e-12) / (n**2 + 1e-12))
            if snr_db > 0.0:
                viable += 1
    frac = viable / total
    return {
        "model": "sim_noise_decoherence_sweep",
        "config": asdict(cfg),
        "summary": {
            "viable_fraction": round(frac, 6),
            "viable_points": viable,
            "total_points": total,
        },
    }


def main() -> None:
    payload = _COMMON.with_contract(__file__, run(Config()))
    out = Path(__file__).with_name("02_noise_decoherence_sweep_report.json")
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[sim02] wrote {out}")


if __name__ == "__main__":
    main()
