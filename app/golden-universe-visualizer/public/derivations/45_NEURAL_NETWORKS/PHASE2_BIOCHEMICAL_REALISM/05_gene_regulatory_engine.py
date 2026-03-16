#!/usr/bin/env python3
"""
Track A5: Gene regulation and epigenetic state transitions coupled to metabolism and membrane signals.
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


def run_gene_engine() -> Dict[str, object]:
    c = _load("00_common.py", "_p2_common")
    dt = 0.05
    steps = 4000
    # [mRNA_A, protein_A, epi_open, regulator_R, vm_signal, atp_signal]
    y0 = np.array([0.05, 0.10, 0.4, 0.2, -65.0, 2.0], dtype=float)

    def rhs(y: np.ndarray, t: float) -> np.ndarray:
        mrna, prot, epi, reg, vm, atp = y
        stim = 0.5 + 0.3 * np.sin(0.01 * t)

        vm_norm = np.clip((vm + 90.0) / 50.0, 0.0, 1.0)
        atp_norm = np.clip(atp / 3.0, 0.0, 1.5)

        d_epi = 0.02 * (vm_norm + 0.5 * atp_norm) * (1.0 - epi) - 0.01 * epi
        transcription = 0.18 * epi * (0.4 + stim) * (1.0 + 0.4 * reg) * atp_norm
        translation = 0.22 * mrna * atp_norm
        d_mrna = transcription - 0.06 * mrna
        d_prot = translation - 0.03 * prot
        d_reg = 0.015 * prot - 0.02 * reg
        d_vm = 0.2 * (stim - vm_norm) - 0.01 * (vm + 65.0)
        d_atp = 0.05 * (1.0 - atp_norm) - 0.03 * (transcription + translation)
        return np.array([d_mrna, d_prot, d_epi, d_reg, d_vm, d_atp], dtype=float)

    hist = c.explicit_euler(rhs, y0, dt=dt, steps=steps)
    mrna, prot, epi, reg, vm, atp = hist[-1]

    payload = {
        "model": "gene_regulatory_engine",
        "config": {"dt": dt, "steps": steps},
        "assumptions": [
            "Epigenetic openness modulates transcription rate.",
            "Transcription/translation consume ATP-like signal budget.",
            "Membrane state modulates epigenetic accessibility."
        ],
        "units": {"expression": "arb", "vm": "mV", "atp_signal": "mM", "time": "s"},
        "parameter_provenance": {"source": "Phase2 gene-module initialization constants"},
        "summary": {
            "final_mrna_A": float(mrna),
            "final_protein_A": float(prot),
            "final_epi_open_fraction": float(epi),
            "final_regulator_R": float(reg),
            "final_vm_mV": float(vm),
            "final_atp_signal": float(atp),
        },
        "diagnostics": {
            "state_nonnegative_except_vm": bool(np.min(hist[:, [0, 1, 2, 3, 5]]) >= -1e-9),
            "expression_stability_tail_std": float(np.std(hist[-500:, 1])),
        },
    }
    out = c.write_report(__file__, payload)
    return {"output": str(out), "payload": payload}


def main() -> None:
    result = run_gene_engine()
    print(f"wrote {result['output']}")


if __name__ == "__main__":
    main()
