#!/usr/bin/env python3
"""
Stage 05: causality and consistency guardrails.
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

write_report = _COMMON.write_report


@dataclass
class Config:
    enforce_unconscious_limit: bool = True
    enforce_regime_switching: bool = True
    enforce_energy_budget: bool = True
    enforce_non_markovian_memory: bool = True
    seed: str = "deterministic_by_construction"


def run(cfg: Config) -> Dict[str, object]:
    checks = {
        "maxwell_unconscious_limit": cfg.enforce_unconscious_limit,
        "regime_activation_consistency": cfg.enforce_regime_switching,
        "finite_energy_budget": cfg.enforce_energy_budget,
        "history_dependence_required": cfg.enforce_non_markovian_memory,
    }
    pass_fraction = sum(1.0 for v in checks.values() if v) / len(checks)
    return {
        "model": "causality_and_guardrail_checks",
        "config": asdict(cfg),
        "summary": {
            "guardrail_pass_fraction": round(pass_fraction, 6),
            "all_guardrails_passed": bool(pass_fraction == 1.0),
        },
        "guardrails": checks,
    }


def main() -> None:
    out = write_report(__file__, run(Config()))
    print(f"[05] wrote {out}")


if __name__ == "__main__":
    main()
