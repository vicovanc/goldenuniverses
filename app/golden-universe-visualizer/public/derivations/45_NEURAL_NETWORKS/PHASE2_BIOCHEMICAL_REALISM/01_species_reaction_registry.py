#!/usr/bin/env python3
"""
Track A1: Species/reaction registry with stoichiometric consistency checks.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import importlib.util
from pathlib import Path
from typing import Dict, List

import numpy as np


def _common():
    p = Path(__file__).with_name("00_common.py")
    spec = importlib.util.spec_from_file_location("_p2_common", p)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


@dataclass
class Species:
    name: str
    charge: int
    compartment: str
    units: str = "mM"


def build_registry() -> Dict[str, object]:
    species: List[Species] = [
        Species("S_ext", 0, "outside"),
        Species("S_cyt", 0, "cytoplasm"),
        Species("ATP", -4, "cytoplasm"),
        Species("ADP", -3, "cytoplasm"),
        Species("Pi", -2, "cytoplasm"),
        Species("NADH", -1, "cytoplasm"),
        Species("NADplus", -1, "cytoplasm"),
        Species("H_in", 1, "cytoplasm"),
        Species("H_out", 1, "outside"),
        Species("mRNA_A", -1, "cytoplasm"),
        Species("Prot_A", 0, "cytoplasm"),
    ]

    names = [s.name for s in species]
    idx = {n: i for i, n in enumerate(names)}
    # Reactions: uptake, catabolism, ATPase, ETC proton pump, transcription, translation, decay.
    # Matrix shape: n_species x n_reactions
    n_species = len(species)
    n_reac = 7
    s = np.zeros((n_species, n_reac), dtype=float)

    # R0: S_ext -> S_cyt
    s[idx["S_ext"], 0] = -1
    s[idx["S_cyt"], 0] = +1
    # R1: S_cyt + ADP + Pi + NADplus -> ATP + NADH
    s[idx["S_cyt"], 1] = -1
    s[idx["ADP"], 1] = -1
    s[idx["Pi"], 1] = -1
    s[idx["NADplus"], 1] = -1
    s[idx["ATP"], 1] = +1
    s[idx["NADH"], 1] = +1
    # R2: ATP -> ADP + Pi
    s[idx["ATP"], 2] = -1
    s[idx["ADP"], 2] = +1
    s[idx["Pi"], 2] = +1
    # R3: NADH + H_in -> NADplus + H_out
    s[idx["NADH"], 3] = -1
    s[idx["H_in"], 3] = -1
    s[idx["NADplus"], 3] = +1
    s[idx["H_out"], 3] = +1
    # R4: ATP -> ADP + mRNA_A
    s[idx["ATP"], 4] = -1
    s[idx["ADP"], 4] = +1
    s[idx["mRNA_A"], 4] = +1
    # R5: mRNA_A + ATP -> Prot_A + ADP
    s[idx["mRNA_A"], 5] = -1
    s[idx["ATP"], 5] = -1
    s[idx["Prot_A"], 5] = +1
    s[idx["ADP"], 5] = +1
    # R6: mRNA_A -> sink
    s[idx["mRNA_A"], 6] = -1

    charge_vec = np.array([sp.charge for sp in species], dtype=float)
    charge_balance = (charge_vec[:, None] * s).sum(axis=0)
    conserved_charge_reactions = [int(abs(x) < 1e-12) for x in charge_balance]

    return {
        "species": [asdict(sp) for sp in species],
        "species_index": idx,
        "stoichiometric_matrix": s.tolist(),
        "charge_balance_per_reaction": charge_balance.tolist(),
        "charge_conserved_flags": conserved_charge_reactions,
    }


def main() -> None:
    cm = _common()
    reg = build_registry()
    payload = {
        "model": "species_reaction_registry",
        "config": {"n_reactions": 7},
        "assumptions": [
            "Minimal proto-cell chemistry with ATP/NADH coupling.",
            "Single-compartment cytoplasm plus external reservoir.",
            "Charge conservation checked reaction-wise."
        ],
        "units": {"concentration": "mM", "time": "s"},
        "parameter_provenance": {"source": "Phase2 mechanistic initialization"},
        "summary": {
            "n_species": len(reg["species"]),
            "n_reactions": 7,
            "charge_conserved_reaction_fraction": float(np.mean(reg["charge_conserved_flags"]))
        },
        "diagnostics": {
            "charge_balance_per_reaction": reg["charge_balance_per_reaction"],
            "charge_conserved_flags": reg["charge_conserved_flags"]
        },
        "registry": reg,
    }
    out = cm.write_report(__file__, payload)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
