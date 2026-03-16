#!/usr/bin/env python3
"""
Track A4: ATP/redox metabolism with proton motive coupling.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Dict

import numpy as np


def _load(path_name: str, mod_name: str):
    p = Path(__file__).with_name(path_name)
    spec = importlib.util.spec_from_file_location(mod_name, p)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def run_metabolic() -> Dict[str, object]:
    c = _load("00_common.py", "_p2_common")
    dt = 0.01
    steps = 15000
    # [ATP, ADP, NADH, NADplus, dPsi, proton_gradient]
    y0 = np.array([2.2, 0.8, 0.4, 1.6, 110.0, 0.6], dtype=float)

    def rhs(y: np.ndarray, _t: float) -> np.ndarray:
        atp, adp, nadh, nadp, dpsi, dp = y
        v_cat = 0.10 * adp * nadh
        v_atpase = 0.08 * atp
        v_etc = 0.12 * nadh * (1.0 + 0.004 * dpsi)
        v_resp = 0.05 * dp
        v_leak = 0.015 * dpsi

        datp = +v_cat + 0.5 * v_resp - v_atpase
        dadp = -v_cat - 0.5 * v_resp + v_atpase
        dnadh = +0.06 - v_etc
        dnadp = -dnadh
        ddpsi = +9.0 * v_etc - 5.5 * v_resp - v_leak
        ddp = +0.6 * v_etc - 0.7 * v_resp
        return np.array([datp, dadp, dnadh, dnadp, ddpsi, ddp], dtype=float)

    hist = c.explicit_euler(rhs, y0, dt=dt, steps=steps)
    atp, adp, nadh, nadp, dpsi, dp = hist[-1]
    energy_charge = float(atp / max(atp + adp, 1e-12))
    atp_turnover_proxy = float(np.mean(np.abs(np.diff(hist[:, 0])) / dt))

    payload = {
        "model": "metabolic_redox_engine",
        "config": {"dt": dt, "steps": steps},
        "assumptions": [
            "Minimal ETC-proton-motive ATP coupling model.",
            "NADH production source represented by constant feed term."
        ],
        "units": {"metabolites": "mM", "dPsi": "mV", "time": "s"},
        "parameter_provenance": {"source": "Phase2 metabolic initialization constants"},
        "summary": {
            "final_atp": float(atp),
            "final_nadh": float(nadh),
            "final_dPsi_mV": float(dpsi),
            "energy_charge": energy_charge,
            "atp_turnover_proxy": atp_turnover_proxy,
        },
        "diagnostics": {
            "state_nonnegative_metabolites": bool(np.min(hist[:, :4]) > 0.0),
            "dPsi_range_mV": [float(np.min(hist[:, 4])), float(np.max(hist[:, 4]))],
        },
    }
    out = c.write_report(__file__, payload)
    return {"output": str(out), "payload": payload}


def main() -> None:
    result = run_metabolic()
    print(f"wrote {result['output']}")


if __name__ == "__main__":
    main()
