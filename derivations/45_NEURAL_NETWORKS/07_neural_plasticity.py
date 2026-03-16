#!/usr/bin/env python3
"""
Phase II-4: Neural plasticity from temporal theta-correlation logic.

Implements a compact STDP-like rule:
  - pre before post -> potentiation
  - post before pre -> depression
and tracks long-term synaptic efficacy trajectory.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Dict, List

from nn_redo_common import augment_report, write_report as write_contract_report

@dataclass
class PlasticityConfig:
    tau_plus: float = 0.02
    tau_minus: float = 0.03
    a_plus: float = 0.012
    a_minus: float = 0.010
    w_init: float = 0.45
    w_min: float = 0.05
    w_max: float = 1.20


def _make_spike_trains() -> Dict[str, List[float]]:
    pre = [0.11, 0.23, 0.37, 0.52, 0.77, 0.95, 1.11]
    post = [0.14, 0.20, 0.40, 0.57, 0.74, 1.00, 1.16]
    return {"pre": pre, "post": post}


def run_plasticity(cfg: PlasticityConfig) -> Dict[str, object]:
    spikes = _make_spike_trains()
    pre = spikes["pre"]
    post = spikes["post"]

    w = cfg.w_init
    rows: List[Dict[str, float]] = []
    ltp_count = 0
    ltd_count = 0

    for t_pre in pre:
        for t_post in post:
            dt = t_post - t_pre
            if dt > 0:
                dw = cfg.a_plus * math.exp(-dt / cfg.tau_plus)
                ltp_count += 1
            else:
                dw = -cfg.a_minus * math.exp(dt / cfg.tau_minus)
                ltd_count += 1
            w = min(cfg.w_max, max(cfg.w_min, w + dw))
            rows.append(
                {
                    "t_pre": round(t_pre, 6),
                    "t_post": round(t_post, 6),
                    "delta_t": round(dt, 6),
                    "delta_w": round(dw, 8),
                    "weight": round(w, 8),
                }
            )

    final_weight = w
    net_change = final_weight - cfg.w_init
    consolidation_index = final_weight / cfg.w_init

    return {
        "model": "neural_plasticity",
        "config": cfg.__dict__,
        "spike_trains": spikes,
        "summary": {
            "initial_weight": round(cfg.w_init, 8),
            "final_weight": round(final_weight, 8),
            "net_weight_change": round(net_change, 8),
            "consolidation_index": round(consolidation_index, 8),
            "ltp_pairs": ltp_count,
            "ltd_pairs": ltd_count,
        },
        "pairwise_updates": rows[:250],
    }


def write_report(report: Dict[str, object]) -> Path:
    payload = augment_report(__file__, report)
    return write_contract_report(__file__, payload)


def main() -> None:
    cfg = PlasticityConfig()
    report = run_plasticity(cfg)
    out_path = write_report(report)
    s = report["summary"]
    print("Neural plasticity (GU)")
    print(f"- initial weight: {s['initial_weight']}")
    print(f"- final weight: {s['final_weight']}")
    print(f"- consolidation index: {s['consolidation_index']}")
    print(f"- report: {out_path}")


if __name__ == "__main__":
    main()
