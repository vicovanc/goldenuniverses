#!/usr/bin/env python3
"""
Track C3: Promotion rules for derived vs provisional biology claims.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Dict


def _load(path_name: str, mod_name: str):
    p = Path(__file__).with_name(path_name)
    spec = importlib.util.spec_from_file_location(mod_name, p)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def run_promotion() -> Dict[str, object]:
    c = _load("00_common.py", "_p2_common")
    id_report = _load("11_bio_identifiability.py", "_p2_i").run_identifiability()["payload"]
    fa_report = _load("12_bio_falsification_gates.py", "_p2_f").run_falsification()["payload"]

    rank_ok = id_report["summary"]["identifiable_full_rank"]
    fals_ok = all(v == "pass" for v in fa_report["gate_status"].values())

    if rank_ok and fals_ok:
        status = "derived"
    elif fals_ok:
        status = "constrained"
    else:
        status = "provisional"

    payload = {
        "model": "bio_promotion_rules",
        "config": {"promotion_rule": "identifiability && falsification"},
        "assumptions": ["Promotion requires both full-rank identifiability and falsification pass."],
        "units": {},
        "parameter_provenance": {"source": "phase2 promotion policy"},
        "summary": {
            "rank_ok": bool(rank_ok),
            "falsification_ok": bool(fals_ok),
            "promotion_status": status,
        },
        "gate_status": {
            "identifiability_gate": "pass" if rank_ok else "fail",
            "falsification_gate": "pass" if fals_ok else "fail",
            "promotion_gate": status,
        },
    }
    out = c.write_report(__file__, payload)
    return {"output": str(out), "payload": payload}


def main() -> None:
    result = run_promotion()
    print(f"wrote {result['output']}")


if __name__ == "__main__":
    main()
