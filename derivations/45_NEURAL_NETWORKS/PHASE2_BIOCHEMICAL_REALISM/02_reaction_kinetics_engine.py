#!/usr/bin/env python3
"""
Track A2: Reaction kinetics engine (mass-action + MM/Hill style terms).
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


def _rates(x: np.ndarray, idx: Dict[str, int]) -> np.ndarray:
    # State vector order from registry.
    s_ext = x[idx["S_ext"]]
    s_cyt = x[idx["S_cyt"]]
    atp = x[idx["ATP"]]
    adp = x[idx["ADP"]]
    pi = x[idx["Pi"]]
    nadh = x[idx["NADH"]]
    nadp = x[idx["NADplus"]]
    h_in = x[idx["H_in"]]
    mrna = x[idx["mRNA_A"]]

    v = np.zeros(7, dtype=float)
    v[0] = 0.25 * s_ext / (1.0 + s_ext)                         # uptake
    v[1] = 0.12 * s_cyt * adp * pi * nadp / (1.0 + s_cyt)       # catabolic ATP synthesis
    v[2] = 0.09 * atp                                            # ATPase consumption
    v[3] = 0.07 * nadh * h_in / (1.0 + nadh)                    # proton pumping
    v[4] = 0.03 * atp / (0.4 + atp)                             # transcription MM
    v[5] = 0.06 * mrna * (atp / (0.5 + atp))                    # translation MM
    v[6] = 0.02 * mrna                                           # mRNA decay
    return v


def run_engine() -> Dict[str, object]:
    c = _load("00_common.py", "_p2_common")
    # Local mirror of registry to avoid cross-module dataclass import fragility.
    species = ["S_ext", "S_cyt", "ATP", "ADP", "Pi", "NADH", "NADplus", "H_in", "H_out", "mRNA_A", "Prot_A"]
    idx = {n: i for i, n in enumerate(species)}
    s = np.zeros((len(species), 7), dtype=float)
    s[idx["S_ext"], 0] = -1
    s[idx["S_cyt"], 0] = +1
    s[idx["S_cyt"], 1] = -1
    s[idx["ADP"], 1] = -1
    s[idx["Pi"], 1] = -1
    s[idx["NADplus"], 1] = -1
    s[idx["ATP"], 1] = +1
    s[idx["NADH"], 1] = +1
    s[idx["ATP"], 2] = -1
    s[idx["ADP"], 2] = +1
    s[idx["Pi"], 2] = +1
    s[idx["NADH"], 3] = -1
    s[idx["H_in"], 3] = -1
    s[idx["NADplus"], 3] = +1
    s[idx["H_out"], 3] = +1
    s[idx["ATP"], 4] = -1
    s[idx["ADP"], 4] = +1
    s[idx["mRNA_A"], 4] = +1
    s[idx["mRNA_A"], 5] = -1
    s[idx["ATP"], 5] = -1
    s[idx["Prot_A"], 5] = +1
    s[idx["ADP"], 5] = +1
    s[idx["mRNA_A"], 6] = -1

    x0 = np.array([4.0, 0.2, 2.0, 1.2, 1.0, 0.3, 1.5, 0.8, 0.6, 0.05, 0.1], dtype=float)

    def rhs(x: np.ndarray, _t: float) -> np.ndarray:
        v = _rates(np.clip(x, 1e-9, None), idx)
        return s @ v

    hist = c.explicit_euler(rhs, x0, dt=0.05, steps=800)
    x_end = hist[-1]
    v_end = _rates(np.clip(x_end, 1e-9, None), idx)

    # Non-negativity / boundedness diagnostics.
    min_conc = float(hist.min())
    max_conc = float(hist.max())

    payload = {
        "model": "reaction_kinetics_engine",
        "config": {"dt": 0.05, "steps": 800, "n_reactions": 7},
        "assumptions": [
            "Mass-action core with MM saturations for transcription/translation.",
            "Fixed external reservoir species are dynamic but not replenished.",
        ],
        "units": {"concentration": "mM", "time": "s", "rate": "mM/s"},
        "parameter_provenance": {"source": "Phase2 kinetics initialization constants"},
        "summary": {
            "final_atp": float(x_end[idx["ATP"]]),
            "final_nadh": float(x_end[idx["NADH"]]),
            "final_mrna": float(x_end[idx["mRNA_A"]]),
            "min_concentration_observed": min_conc,
            "max_concentration_observed": max_conc,
        },
        "diagnostics": {
            "final_reaction_rates": v_end.tolist(),
            "state_nonnegative": bool(min_conc >= -1e-8),
        },
    }
    out = c.write_report(__file__, payload)
    return {"output": str(out), "payload": payload}


def main() -> None:
    result = run_engine()
    print(f"wrote {result['output']}")


if __name__ == "__main__":
    main()
