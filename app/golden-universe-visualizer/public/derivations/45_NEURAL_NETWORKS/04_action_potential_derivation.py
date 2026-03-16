#!/usr/bin/env python3
"""
Phase II-1: Action potential derivation in a GU-style effective model.

Implements a compact Hodgkin-Huxley/FitzHugh-Nagumo hybrid surrogate to
represent theta-channel driven spike propagation along an axonal cable.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Dict, List

from nn_redo_common import augment_report, write_report as write_contract_report

@dataclass
class SpikeConfig:
    dt: float = 0.01
    total_time: float = 150.0
    a: float = 0.7
    b: float = 0.8
    tau: float = 12.5
    stimulus_start: float = 20.0
    stimulus_end: float = 90.0
    stimulus_amp: float = 0.55
    myelin_speed_gain: float = 1.35


def _input_current(t: float, cfg: SpikeConfig) -> float:
    if cfg.stimulus_start <= t <= cfg.stimulus_end:
        return cfg.stimulus_amp
    return 0.0


def run_spike_model(cfg: SpikeConfig) -> Dict[str, object]:
    n_steps = int(cfg.total_time / cfg.dt)
    v = -1.1
    w = 0.0
    spikes: List[float] = []
    rows: List[Dict[str, float]] = []
    last_v = v

    for i in range(n_steps):
        t = i * cfg.dt
        i_inj = _input_current(t, cfg)

        # FitzHugh-Nagumo style dynamics.
        dv = v - (v**3) / 3.0 - w + i_inj
        dw = (v + cfg.a - cfg.b * w) / cfg.tau
        v += cfg.dt * dv
        w += cfg.dt * dw

        # Spike when crossing upward threshold.
        if last_v < 0.8 and v >= 0.8:
            spikes.append(t)
        last_v = v

        if i % max(1, n_steps // 24) == 0:
            rows.append(
                {
                    "t_ms_proxy": round(t, 4),
                    "v_membrane": round(v, 6),
                    "w_recovery": round(w, 6),
                    "input_current": round(i_inj, 6),
                }
            )

    isi = [spikes[i + 1] - spikes[i] for i in range(len(spikes) - 1)]
    mean_isi = sum(isi) / len(isi) if isi else 0.0
    firing_rate_hz = (1.0 / mean_isi) if mean_isi > 0 else 0.0
    refractory_proxy = min(isi) if isi else 0.0
    conduction_speed_proxy = cfg.myelin_speed_gain * (10.0 + 90.0 * min(firing_rate_hz / 100.0, 1.0))

    return {
        "model": "action_potential_derivation",
        "config": cfg.__dict__,
        "summary": {
            "spike_count": len(spikes),
            "mean_isi_s": round(mean_isi, 6),
            "firing_rate_hz": round(firing_rate_hz, 6),
            "refractory_proxy_s": round(refractory_proxy, 6),
            "conduction_speed_proxy_m_per_s": round(conduction_speed_proxy, 6),
        },
        "spike_times_s": [round(x, 6) for x in spikes[:200]],
        "sampled_state": rows,
    }


def write_report(report: Dict[str, object]) -> Path:
    payload = augment_report(__file__, report)
    return write_contract_report(__file__, payload)


def main() -> None:
    cfg = SpikeConfig()
    report = run_spike_model(cfg)
    out_path = write_report(report)
    s = report["summary"]
    print("Action potential derivation (GU)")
    print(f"- spikes: {s['spike_count']}")
    print(f"- firing rate [Hz]: {s['firing_rate_hz']}")
    print(f"- refractory proxy [s]: {s['refractory_proxy_s']}")
    print(f"- conduction speed proxy [m/s]: {s['conduction_speed_proxy_m_per_s']}")
    print(f"- report: {out_path}")


if __name__ == "__main__":
    main()
