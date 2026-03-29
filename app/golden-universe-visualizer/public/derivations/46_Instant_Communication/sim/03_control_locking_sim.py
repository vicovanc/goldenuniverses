#!/usr/bin/env python3
"""
Sim 03: control-loop locking dynamics and session lock time.
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
    dt: float = 0.02
    t_end: float = 20.0
    kp: float = 0.9
    kd: float = 0.15
    eps_lock: float = 0.01
    hold_s: float = 0.8
    seed: str = "deterministic_by_construction"


def run(cfg: Config) -> dict:
    n = int(cfg.t_end / cfg.dt)
    err = 0.7
    derr_prev = 0.0
    hold_count = 0
    locked_at = None
    for i in range(n):
        derr = -cfg.kp * err - cfg.kd * (err - derr_prev) / cfg.dt
        derr_prev = err
        err += cfg.dt * derr
        if abs(err) < cfg.eps_lock:
            hold_count += 1
            if locked_at is None and hold_count * cfg.dt >= cfg.hold_s:
                locked_at = i * cfg.dt
        else:
            hold_count = 0
    if locked_at is None:
        locked_at = cfg.t_end
    return {
        "model": "sim_control_locking",
        "config": asdict(cfg),
        "summary": {
            "session_lock_time_s": round(locked_at, 6),
            "final_lock_error": round(err, 8),
            "lock_achieved": bool(locked_at < cfg.t_end),
        },
    }


def main() -> None:
    payload = _COMMON.with_contract(__file__, run(Config()))
    out = Path(__file__).with_name("03_control_locking_sim_report.json")
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[sim03] wrote {out}")


if __name__ == "__main__":
    main()
