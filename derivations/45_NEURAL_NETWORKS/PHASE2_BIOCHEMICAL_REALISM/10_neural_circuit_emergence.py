#!/usr/bin/env python3
"""
Track B4: Emergence of sensory-motor motifs from tissue-level couplings.
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


def run_circuit_emergence(
    *,
    seed: int = 1010,
    n: int = 24,
    steps: int = 1200,
    dt: float = 0.01,
    input_amplitude: float = 0.8,
    recurrent_gain: float = 0.92,
    hebbian_lr: float = 0.002,
    sensory_motor_bias: float = 0.0,
    write_report: bool = True,
) -> Dict[str, object]:
    c = _load("00_common.py", "_p2_common")
    rng = np.random.default_rng(seed)
    w = rng.normal(0.0, 0.25, size=(n, n))
    np.fill_diagonal(w, 0.0)

    sensory_idx = np.arange(0, 6)
    motor_idx = np.arange(18, 24)
    state = np.zeros(n, dtype=float)

    # Optional structured prior to test motif emergence under explicit bias.
    if sensory_motor_bias != 0.0:
        for si in sensory_idx:
            for mi in motor_idx:
                w[mi, si] += sensory_motor_bias

    responses = []
    for k in range(steps):
        inp = np.zeros(n, dtype=float)
        if 100 <= k <= 300 or 600 <= k <= 850:
            inp[sensory_idx] = input_amplitude
        state = np.tanh(recurrent_gain * state + dt * (w @ state + inp))
        responses.append(float(np.mean(state[motor_idx])))

        # Hebbian adaptation on active pairs.
        if k % 10 == 0:
            corr = np.outer(state, state)
            w += hebbian_lr * corr
            np.fill_diagonal(w, 0.0)
            w = np.clip(w, -1.0, 1.0)

    response_arr = np.array(responses)
    pre_stim = float(np.mean(response_arr[:100]))
    in_stim = float(np.mean(response_arr[120:280]))
    post_stim = float(np.mean(response_arr[-100:]))
    motif_gain = in_stim - pre_stim

    payload = {
        "model": "neural_circuit_emergence",
        "config": {
            "n_nodes": n,
            "steps": steps,
            "dt": dt,
            "seed": seed,
            "input_amplitude": input_amplitude,
            "recurrent_gain": recurrent_gain,
            "hebbian_lr": hebbian_lr,
            "sensory_motor_bias": sensory_motor_bias,
        },
        "assumptions": [
            "Sensory-to-motor motifs emerge via recurrent dynamics and Hebbian reinforcement.",
            "Motor response mean is used as circuit-level output observable."
        ],
        "units": {"state": "normalized", "time": "s"},
        "parameter_provenance": {"source": "phase2 circuit initialization"},
        "summary": {
            "pre_stim_motor_mean": pre_stim,
            "in_stim_motor_mean": in_stim,
            "post_stim_motor_mean": post_stim,
            "motif_gain": motif_gain,
        },
        "diagnostics": {
            "stimulus_responsive": bool(motif_gain > 0.05),
            "weight_mean_abs": float(np.mean(np.abs(w))),
        },
    }
    if write_report:
        out = c.write_report(__file__, payload)
        return {"output": str(out), "payload": payload}
    return {"output": None, "payload": payload}


def main() -> None:
    result = run_circuit_emergence()
    print(f"wrote {result['output']}")


if __name__ == "__main__":
    main()
