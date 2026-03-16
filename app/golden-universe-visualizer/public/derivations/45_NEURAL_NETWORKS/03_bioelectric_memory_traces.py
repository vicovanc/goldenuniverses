#!/usr/bin/env python3
"""
Phase I-3: Bioelectric memory traces (Vm patterns) from GU principles.

Implements a two-timescale memory model:
  - fast bioelectric state
  - slow gene-expression adaptation stabilizing patterns
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
from pathlib import Path
from typing import Dict, List

from nn_redo_common import augment_report, write_report as write_contract_report

@dataclass
class MemoryConfig:
    dt: float = 0.05
    total_time: float = 180.0
    tau_fast: float = 1.5
    tau_slow: float = 32.0
    coupling_fast_to_slow: float = 0.18
    coupling_slow_to_fast: float = 0.42
    retention_gain: float = 0.22


def _training_signal(t: float) -> float:
    if 20.0 <= t <= 80.0:
        return 0.7 + 0.2 * math.sin(2.0 * math.pi * t / 8.0)
    if 105.0 <= t <= 120.0:
        return 0.4
    return 0.0


def run_memory(cfg: MemoryConfig) -> Dict[str, object]:
    n_steps = int(cfg.total_time / cfg.dt)
    v_fast = 0.0
    g_slow = 0.0
    learned_level = 0.0

    rows: List[Dict[str, float]] = []
    post_training_window: List[float] = []

    for i in range(n_steps):
        t = i * cfg.dt
        inp = _training_signal(t)

        dv = (inp + cfg.coupling_slow_to_fast * g_slow - v_fast) / cfg.tau_fast
        dg = (cfg.coupling_fast_to_slow * v_fast - g_slow) / cfg.tau_slow
        dl = cfg.retention_gain * max(v_fast, 0.0) - 0.02 * learned_level

        v_fast += cfg.dt * dv
        g_slow += cfg.dt * dg
        learned_level += cfg.dt * dl

        if t > 130.0:
            post_training_window.append(v_fast)

        if i % max(1, n_steps // 24) == 0:
            rows.append(
                {
                    "t_s": round(t, 3),
                    "input": round(inp, 6),
                    "fast_vm_state": round(v_fast, 6),
                    "slow_gene_state": round(g_slow, 6),
                    "learned_retention": round(learned_level, 6),
                }
            )

    retention_vm = sum(post_training_window) / max(len(post_training_window), 1)
    retrieval_score = retention_vm / (0.7 + 1e-9)
    memory_half_life_proxy = cfg.tau_slow * math.log(2.0)

    return {
        "model": "bioelectric_memory_traces",
        "config": cfg.__dict__,
        "summary": {
            "retained_vm_post_training": round(retention_vm, 6),
            "retrieval_score": round(retrieval_score, 6),
            "final_fast_vm_state": round(v_fast, 6),
            "final_slow_gene_state": round(g_slow, 6),
            "memory_half_life_proxy_s": round(memory_half_life_proxy, 6),
        },
        "sampled_memory_trajectory": rows,
    }


def write_report(report: Dict[str, object]) -> Path:
    payload = augment_report(__file__, report)
    return write_contract_report(__file__, payload)


def main() -> None:
    cfg = MemoryConfig()
    report = run_memory(cfg)
    out_path = write_report(report)
    s = report["summary"]
    print("Bioelectric memory traces (GU)")
    print(f"- retained Vm post-training: {s['retained_vm_post_training']}")
    print(f"- retrieval score: {s['retrieval_score']}")
    print(f"- memory half-life proxy [s]: {s['memory_half_life_proxy_s']}")
    print(f"- report: {out_path}")


if __name__ == "__main__":
    main()
