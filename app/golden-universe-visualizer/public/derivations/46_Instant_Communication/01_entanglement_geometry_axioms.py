#!/usr/bin/env python3
"""
Stage 01: geometric entanglement axioms and topological initialization.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import importlib.util
from pathlib import Path
from typing import Dict

_COMMON_PATH = Path(__file__).with_name("00_common.py")
_SPEC = importlib.util.spec_from_file_location("instant_common", _COMMON_PATH)
_COMMON = importlib.util.module_from_spec(_SPEC)
assert _SPEC and _SPEC.loader
_SPEC.loader.exec_module(_COMMON)

PHI = _COMMON.PHI
PI = _COMMON.PI
M_P_MEV = _COMMON.M_P_MEV
resonance_values = _COMMON.resonance_values
write_report = _COMMON.write_report


@dataclass
class Config:
    epoch_n: int = 111
    p_winding: int = -41
    q_winding: int = 70
    kappa: int = 1
    seed: str = "deterministic_by_construction"


def run(cfg: Config) -> Dict[str, object]:
    r2 = cfg.p_winding**2 + (cfg.q_winding**2) / (PHI * PHI)
    l_omega = 2.0 * PI * (r2 ** 0.5)
    nu_topo = abs(cfg.q_winding / PHI) / (r2 ** 0.5)
    k_res, delta = resonance_values(cfg.epoch_n)
    resonance_pass = (k_res % 2 == 0) and (abs(delta) < 0.5)
    gate_margin = max(0.0, 0.5 - abs(delta))

    return {
        "model": "entanglement_geometry_axioms",
        "config": asdict(cfg),
        "summary": {
            "epoch_n": cfg.epoch_n,
            "k_res": k_res,
            "delta": round(delta, 6),
            "resonance_pass": resonance_pass,
            "resonance_gate_margin": round(gate_margin, 6),
            "l_omega": round(l_omega, 6),
            "nu_topo": round(nu_topo, 6),
            "z1_magnitude_mev": round(M_P_MEV / (4.0 * (PI ** 0.5)), 6),
        },
        "axioms": [
            "A1: genesis is mirrored (Omega_0 -> Z1 + Z2).",
            "A2: geometric entanglement is encoded by winding topology.",
            "A3: corrected resonance gate uses round(N/phi^2), not floor.",
            "A4: signaling hypotheses are conditional on topological activation.",
        ],
    }


def main() -> None:
    payload = run(Config())
    out = write_report(__file__, payload)
    print(f"[01] wrote {out}")


if __name__ == "__main__":
    main()
