#!/usr/bin/env python3
"""
Phase IV-4: Language and symbols in a GU-inspired latent-semantic model.

Builds a simple symbol embedding space and evaluates compositionality and
semantic consistency.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Dict, List

import numpy as np

from nn_redo_common import augment_report, write_report as write_contract_report

@dataclass
class LanguageConfig:
    dim: int = 12
    seed: int = 16


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    den = (np.linalg.norm(a) * np.linalg.norm(b)) + 1e-12
    return float(np.dot(a, b) / den)


def run_language(cfg: LanguageConfig) -> Dict[str, object]:
    rng = np.random.default_rng(cfg.seed)

    symbols = {
        "self": rng.normal(size=cfg.dim),
        "world": rng.normal(size=cfg.dim),
        "memory": rng.normal(size=cfg.dim),
        "action": rng.normal(size=cfg.dim),
    }
    for k in symbols:
        symbols[k] = symbols[k] / (np.linalg.norm(symbols[k]) + 1e-12)

    # Composed concepts.
    self_memory = 0.6 * symbols["self"] + 0.4 * symbols["memory"]
    world_action = 0.5 * symbols["world"] + 0.5 * symbols["action"]
    narrative_state = 0.5 * self_memory + 0.5 * world_action

    sims = {
        "sim_self_memory": _cosine(symbols["self"], symbols["memory"]),
        "sim_self_selfmemory": _cosine(symbols["self"], self_memory),
        "sim_world_action": _cosine(symbols["world"], symbols["action"]),
        "sim_narrative_self": _cosine(narrative_state, symbols["self"]),
        "sim_narrative_world": _cosine(narrative_state, symbols["world"]),
    }

    compositionality = 0.5 * (sims["sim_self_selfmemory"] + sims["sim_narrative_world"])
    symbolic_consistency = 1.0 - abs(sims["sim_narrative_self"] - sims["sim_narrative_world"])

    rows: List[Dict[str, float]] = [
        {"pair": k, "cosine_similarity": round(float(v), 6)} for k, v in sims.items()
    ]

    return {
        "model": "language_and_symbols",
        "config": cfg.__dict__,
        "summary": {
            "compositionality_score": round(float(compositionality), 6),
            "symbolic_consistency_score": round(float(symbolic_consistency), 6),
            "semantic_balance": round(float(sims["sim_narrative_self"] - sims["sim_narrative_world"]), 6),
        },
        "canonical_observables": {
            "compositionality_score": round(float(compositionality), 6),
            "symbolic_consistency_score": round(float(symbolic_consistency), 6),
        },
        "exploratory_metrics": {
            "semantic_balance": round(float(sims["sim_narrative_self"] - sims["sim_narrative_world"]), 6),
        },
        "symbol_similarity_metrics": rows,
    }


def write_report(report: Dict[str, object]) -> Path:
    payload = augment_report(__file__, report)
    return write_contract_report(__file__, payload)


def main() -> None:
    cfg = LanguageConfig()
    report = run_language(cfg)
    out_path = write_report(report)
    s = report["summary"]
    print("Language and symbols (GU)")
    print(f"- compositionality score: {s['compositionality_score']}")
    print(f"- symbolic consistency score: {s['symbolic_consistency_score']}")
    print(f"- report: {out_path}")


if __name__ == "__main__":
    main()
