#!/usr/bin/env python3
"""
Track A3: Membrane transport and ion-channel gating ODEs.
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


def _goldman_vm(k_in: float, k_out: float, na_in: float, na_out: float, cl_in: float, cl_out: float) -> float:
    p_k, p_na, p_cl = 1.0, 0.05, 0.45
    top = p_k * k_out + p_na * na_out + p_cl * cl_in
    bot = p_k * k_in + p_na * na_in + p_cl * cl_out
    vm = 26.7 * np.log(max(top, 1e-12) / max(bot, 1e-12))
    return float(vm)


def run_membrane() -> Dict[str, object]:
    c = _load("00_common.py", "_p2_common")
    dt = 0.001
    steps = 12000

    # state: [m_gate, h_gate, n_gate, K_in, Na_in, Cl_in]
    y0 = np.array([0.05, 0.6, 0.32, 140.0, 15.0, 10.0], dtype=float)
    na_out, k_out, cl_out = 145.0, 5.0, 110.0

    def rhs(y: np.ndarray, _t: float) -> np.ndarray:
        m, h, n, k_in, na_in, cl_in = y
        vm = _goldman_vm(k_in, k_out, na_in, na_out, cl_in, cl_out)

        m_inf = 1.0 / (1.0 + np.exp(-(vm + 35.0) / 7.5))
        h_inf = 1.0 / (1.0 + np.exp((vm + 58.0) / 8.0))
        n_inf = 1.0 / (1.0 + np.exp(-(vm + 30.0) / 10.0))

        dm = (m_inf - m) / 1.0
        dh = (h_inf - h) / 5.0
        dn = (n_inf - n) / 3.5

        g_na = (m**3) * h
        g_k = n**4
        i_na = g_na * (vm - 55.0)
        i_k = g_k * (vm + 77.0)
        i_cl = 0.15 * (vm + 60.0)

        # Pump counterbalances leak with ATP-like normalization.
        pump = 0.02 * (na_in / (na_in + 10.0)) * (k_out / (k_out + 1.0))

        dk = -0.002 * i_k + 0.005 * pump
        dna = -0.002 * i_na - 0.007 * pump
        dcl = +0.002 * i_cl
        return np.array([dm, dh, dn, dk, dna, dcl], dtype=float)

    hist = c.explicit_euler(rhs, y0, dt=dt, steps=steps)
    vm_series = [
        _goldman_vm(row[3], k_out, row[4], na_out, row[5], cl_out)
        for row in hist
    ]
    vm_arr = np.array(vm_series, dtype=float)

    payload = {
        "model": "membrane_transport_engine",
        "config": {"dt": dt, "steps": steps},
        "assumptions": [
            "HH-like gating on top of Goldman membrane potential.",
            "Minimal Na/K ATPase pump abstraction."
        ],
        "units": {"vm": "mV", "concentration": "mM", "time": "s"},
        "parameter_provenance": {"source": "Phase2 membrane initialization constants"},
        "summary": {
            "vm_rest_mV": float(vm_arr[-1]),
            "vm_min_mV": float(vm_arr.min()),
            "vm_max_mV": float(vm_arr.max()),
            "final_gates": {
                "m": float(hist[-1, 0]),
                "h": float(hist[-1, 1]),
                "n": float(hist[-1, 2]),
            },
        },
        "diagnostics": {
            "vm_stable_tail_std": float(np.std(vm_arr[-2000:])),
            "state_nonnegative": bool(np.min(hist[:, 3:]) > 0.0),
        },
    }
    out = c.write_report(__file__, payload)
    return {"output": str(out), "payload": payload}


def main() -> None:
    result = run_membrane()
    print(f"wrote {result['output']}")


if __name__ == "__main__":
    main()
