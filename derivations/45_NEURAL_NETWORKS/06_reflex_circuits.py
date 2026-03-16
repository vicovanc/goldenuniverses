#!/usr/bin/env python3
"""
Phase II-3: Reflex circuits from GU-inspired attractor dynamics.

Implements a small sensory-interneuron-motor loop and evaluates response
latency, stability, and adaptive settling.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Dict, List

from nn_redo_common import augment_report, write_report as write_contract_report
import numpy as np


@dataclass
class ReflexConfig:
    dt: float = 0.002
    total_time: float = 1.2
    sensory_pulse_start: float = 0.15
    sensory_pulse_end: float = 0.4
    gain_si: float = 1.6
    gain_im: float = 1.3
    gain_feedback: float = 0.55
    leak: float = 0.9
    threshold_motor: float = 0.08


def _pulse(t: float, t0: float, t1: float) -> float:
    return 1.0 if t0 <= t <= t1 else 0.0


def run_reflex(cfg: ReflexConfig) -> Dict[str, object]:
    n_steps = int(cfg.total_time / cfg.dt)
    state = np.zeros(3, dtype=float)  # [sensory, interneuron, motor]
    rows: List[Dict[str, float]] = []
    motor_cross_time = None
    peak_motor = -1e9

    for i in range(n_steps):
        t = i * cfg.dt
        sensory_input = _pulse(t, cfg.sensory_pulse_start, cfg.sensory_pulse_end)

        s, n, m = state
        ds = sensory_input - cfg.leak * s
        dn = cfg.gain_si * s - cfg.leak * n
        dm = cfg.gain_im * n - cfg.gain_feedback * m * m - cfg.leak * m

        state = state + cfg.dt * np.array([ds, dn, dm], dtype=float)
        s, n, m = state

        peak_motor = max(peak_motor, m)
        if motor_cross_time is None and m >= cfg.threshold_motor:
            motor_cross_time = t

        if i % max(1, n_steps // 24) == 0:
            rows.append(
                {
                    "t_s": round(t, 6),
                    "sensory_state": round(float(s), 6),
                    "interneuron_state": round(float(n), 6),
                    "motor_state": round(float(m), 6),
                    "sensory_input": sensory_input,
                }
            )

    if motor_cross_time is None:
        response_latency = None
    else:
        response_latency = motor_cross_time - cfg.sensory_pulse_start

    tail_start = int(0.8 * n_steps)
    tail = [r["motor_state"] for r in rows if r["t_s"] >= cfg.total_time * 0.8]
    settle_std = float(np.std(tail)) if tail else 0.0
    stable_attractor = settle_std < 0.02

    return {
        "model": "reflex_circuits",
        "config": cfg.__dict__,
        "summary": {
            "peak_motor_response": round(peak_motor, 6),
            "response_latency_s": round(response_latency, 6) if response_latency is not None else None,
            "settling_std_tail": round(settle_std, 6),
            "stable_attractor": stable_attractor,
            "tail_window_start_step": tail_start,
        },
        "sampled_reflex_state": rows,
    }


def write_report(report: Dict[str, object]) -> Path:
    payload = augment_report(__file__, report)
    return write_contract_report(__file__, payload)


def main() -> None:
    cfg = ReflexConfig()
    report = run_reflex(cfg)
    out_path = write_report(report)
    s = report["summary"]
    print("Reflex circuits (GU)")
    print(f"- peak motor response: {s['peak_motor_response']}")
    print(f"- response latency [s]: {s['response_latency_s']}")
    print(f"- stable attractor: {s['stable_attractor']}")
    print(f"- report: {out_path}")


if __name__ == "__main__":
    main()
