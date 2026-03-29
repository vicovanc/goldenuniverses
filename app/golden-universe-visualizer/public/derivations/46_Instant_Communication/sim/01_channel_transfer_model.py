#!/usr/bin/env python3
"""
Sim 01: reduced channel transfer model for TX->RX phase-memory signaling.
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
    gain: float = 0.14
    memory_depth: float = 0.7
    activation: float = 0.18
    noise_floor: float = 0.02
    seed: str = "deterministic_by_construction"


def run(cfg: Config) -> dict:
    effective_gain = cfg.gain * cfg.memory_depth * (1.0 + cfg.activation)
    snr_linear = (effective_gain**2 + 1e-12) / (cfg.noise_floor**2 + 1e-12)
    snr_db = 10.0 * __import__("math").log10(snr_linear)
    return {
        "model": "sim_channel_transfer_model",
        "config": asdict(cfg),
        "summary": {
            "effective_gain": round(effective_gain, 6),
            "snr_db": round(snr_db, 6),
            "detectable": bool(snr_db > 0.0),
        },
    }


def main() -> None:
    payload = _COMMON.with_contract(__file__, run(Config()))
    out = Path(__file__).with_name("01_channel_transfer_model_report.json")
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[sim01] wrote {out}")


if __name__ == "__main__":
    main()
