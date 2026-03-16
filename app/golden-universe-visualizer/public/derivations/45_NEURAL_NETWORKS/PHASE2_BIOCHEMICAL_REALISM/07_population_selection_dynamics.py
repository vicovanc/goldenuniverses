#!/usr/bin/env python3
"""
Track B1: Mutation-selection dynamics on mechanistic trait vectors.
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


def run_population() -> Dict[str, object]:
    c = _load("00_common.py", "_p2_common")
    rng = np.random.default_rng(707)
    n_pop = 300
    steps = 180

    # Traits: [metabolic_eff, membrane_stability, replication_fidelity, signaling_eff]
    traits = np.clip(rng.normal([0.5, 0.5, 0.5, 0.45], [0.12, 0.1, 0.08, 0.1], size=(n_pop, 4)), 0.01, 0.99)

    mean_hist = []
    for _ in range(steps):
        fitness = (
            0.35 * traits[:, 0]
            + 0.25 * traits[:, 1]
            + 0.20 * traits[:, 2]
            + 0.20 * traits[:, 3]
        )
        fitness = np.clip(fitness, 1e-6, None)
        probs = fitness / fitness.sum()
        parent_idx = rng.choice(np.arange(n_pop), size=n_pop, p=probs, replace=True)
        offspring = traits[parent_idx].copy()

        # Mutations
        mut = rng.normal(0.0, 0.02, size=offspring.shape)
        offspring += mut
        traits = np.clip(offspring, 0.0, 1.0)
        mean_hist.append(np.mean(traits, axis=0))

    mean_hist = np.array(mean_hist)
    final_mean = mean_hist[-1]
    initial_mean = mean_hist[0]
    gain = final_mean - initial_mean

    payload = {
        "model": "population_selection_dynamics",
        "config": {"population": n_pop, "steps": steps, "seed": 707},
        "assumptions": [
            "Fitness is weighted composite of mechanistic proto-cell traits.",
            "Mutation process is Gaussian and unbiased."
        ],
        "units": {"traits": "0..1 normalized"},
        "parameter_provenance": {"source": "phase2 evolutionary initialization"},
        "summary": {
            "initial_trait_mean": initial_mean.tolist(),
            "final_trait_mean": final_mean.tolist(),
            "trait_gain": gain.tolist(),
            "net_adaptation_index": float(np.mean(gain)),
        },
        "diagnostics": {
            "final_trait_std": np.std(traits, axis=0).tolist(),
        },
    }
    out = c.write_report(__file__, payload)
    return {"output": str(out), "payload": payload}


def main() -> None:
    result = run_population()
    print(f"wrote {result['output']}")


if __name__ == "__main__":
    main()
