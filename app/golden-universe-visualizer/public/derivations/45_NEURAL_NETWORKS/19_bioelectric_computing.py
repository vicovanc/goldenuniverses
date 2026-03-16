#!/usr/bin/env python3
"""
Phase V-2: Bioelectric computing hardware proxy model.

Evaluates throughput, latency, and energy on a hybrid architecture combining:
  - digital control plane,
  - analog/bioelectric compute plane.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Dict

from nn_redo_common import augment_report, write_report as write_contract_report

@dataclass
class HardwareConfig:
    digital_ops_per_s: float = 3.5e9
    bioelectric_ops_per_s: float = 4.0e8
    digital_energy_per_op_j: float = 4.8e-12
    bioelectric_energy_per_op_j: float = 7.0e-13
    bridge_overhead_fraction: float = 0.14
    workload_ops: float = 1.2e9


def run_hardware_proxy(cfg: HardwareConfig) -> Dict[str, object]:
    digital_share = 0.45
    bio_share = 0.55
    digital_ops = cfg.workload_ops * digital_share
    bio_ops = cfg.workload_ops * bio_share

    t_digital = digital_ops / cfg.digital_ops_per_s
    t_bio = bio_ops / cfg.bioelectric_ops_per_s
    latency = max(t_digital, t_bio) * (1.0 + cfg.bridge_overhead_fraction)

    e_digital = digital_ops * cfg.digital_energy_per_op_j
    e_bio = bio_ops * cfg.bioelectric_energy_per_op_j
    energy_total = (e_digital + e_bio) * (1.0 + cfg.bridge_overhead_fraction)

    throughput = cfg.workload_ops / max(latency, 1e-12)
    perf_per_watt_proxy = throughput / max(energy_total / max(latency, 1e-12), 1e-12)

    return {
        "model": "bioelectric_computing",
        "config": cfg.__dict__,
        "summary": {
            "latency_s": round(latency, 9),
            "total_energy_j": round(energy_total, 9),
            "throughput_ops_per_s": round(throughput, 3),
            "performance_per_watt_proxy": round(perf_per_watt_proxy, 3),
        },
        "canonical_observables": {
            "latency_s": round(latency, 9),
            "total_energy_j": round(energy_total, 9),
            "throughput_ops_per_s": round(throughput, 3),
        },
        "exploratory_metrics": {
            "performance_per_watt_proxy": round(perf_per_watt_proxy, 3),
        },
        "breakdown": {
            "digital_ops": digital_ops,
            "bioelectric_ops": bio_ops,
            "digital_energy_j": e_digital,
            "bioelectric_energy_j": e_bio,
        },
    }


def write_report(report: Dict[str, object]) -> Path:
    payload = augment_report(__file__, report)
    return write_contract_report(__file__, payload)


def main() -> None:
    cfg = HardwareConfig()
    report = run_hardware_proxy(cfg)
    out_path = write_report(report)
    s = report["summary"]
    print("Bioelectric computing (GU)")
    print(f"- latency [s]: {s['latency_s']}")
    print(f"- total energy [J]: {s['total_energy_j']}")
    print(f"- perf/W proxy: {s['performance_per_watt_proxy']}")
    print(f"- report: {out_path}")


if __name__ == "__main__":
    main()
