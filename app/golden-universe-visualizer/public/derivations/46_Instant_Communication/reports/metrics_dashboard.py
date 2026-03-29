#!/usr/bin/env python3
"""
Aggregate key report metrics into one scorecard JSON.
"""

from __future__ import annotations

from pathlib import Path
import json


BASE = Path(__file__).resolve().parents[1]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    p_bench = read_json(BASE / "06_benchmark_scenarios_report.json")
    p_fals = read_json(BASE / "07_identifiability_and_falsification_report.json")
    p_phase = read_json(BASE / "08_phase_diagram_and_operating_regions_report.json")
    p_sim1 = read_json(BASE / "sim/01_channel_transfer_model_report.json")
    p_sim2 = read_json(BASE / "sim/02_noise_decoherence_sweep_report.json")
    p_sim3 = read_json(BASE / "sim/03_control_locking_sim_report.json")

    summary = {
        "active_snr_db": p_bench["summary"]["active_snr_db"],
        "balanced_accuracy": p_fals["summary"]["balanced_accuracy"],
        "promotion_ready_stage07": p_fals["summary"]["promotion_ready"],
        "viability_classification": p_phase["summary"]["viability_classification"],
        "viable_window_fraction": p_phase["summary"]["viable_window_fraction"],
        "sim_effective_gain": p_sim1["summary"]["effective_gain"],
        "sim_noise_decoh_viable_fraction": p_sim2["summary"]["viable_fraction"],
        "sim_session_lock_time_s": p_sim3["summary"]["session_lock_time_s"],
    }

    gates = {
        "detectability_gate": summary["active_snr_db"] > 0.0,
        "falsification_gate": bool(summary["promotion_ready_stage07"]),
        "operating_window_gate": summary["viable_window_fraction"] > 0.05,
        "lock_gate": summary["sim_session_lock_time_s"] < 20.0,
    }

    payload = {
        "model": "instant_comm_metrics_dashboard",
        "summary": summary,
        "gates": gates,
        "overall_pass": all(gates.values()),
    }

    out = BASE / "reports/metrics_dashboard_report.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[dashboard] wrote {out}")


if __name__ == "__main__":
    main()
