#!/usr/bin/env python3
"""
Phase V-1: GU-inspired neural architectures.

Compares a baseline dense architecture with a theta-memory augmented variant
on a synthetic task, reporting accuracy and efficiency proxies.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Dict

import numpy as np

from nn_redo_common import augment_report, write_report as write_contract_report

@dataclass
class ArchConfig:
    n_samples: int = 800
    input_dim: int = 12
    hidden_dim: int = 20
    epochs: int = 120
    lr: float = 0.08
    seed: int = 18


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def _build_data(cfg: ArchConfig) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(cfg.seed)
    x = rng.normal(size=(cfg.n_samples, cfg.input_dim))
    y = ((x[:, 0] + 0.6 * x[:, 1] - 0.5 * x[:, 2] + 0.25 * np.sin(x[:, 3])) > 0.0).astype(float)
    return x, y.reshape(-1, 1)


def _train(cfg: ArchConfig, use_theta_memory: bool) -> Dict[str, float]:
    rng = np.random.default_rng(cfg.seed + (101 if use_theta_memory else 0))
    x, y = _build_data(cfg)

    w1 = 0.3 * rng.normal(size=(cfg.input_dim, cfg.hidden_dim))
    b1 = np.zeros((1, cfg.hidden_dim))
    w2 = 0.3 * rng.normal(size=(cfg.hidden_dim, 1))
    b2 = np.zeros((1, 1))
    mem = np.zeros((1, cfg.hidden_dim))

    for _ in range(cfg.epochs):
        h_pre = x @ w1 + b1
        h = np.tanh(h_pre)
        if use_theta_memory:
            # Memory-augmented hidden channel (GU-inspired).
            h = np.tanh(h + 0.25 * mem)
            mem = 0.92 * mem + 0.08 * np.mean(h, axis=0, keepdims=True)

        y_hat = _sigmoid(h @ w2 + b2)
        err = y_hat - y

        d2 = err * y_hat * (1.0 - y_hat)
        grad_w2 = h.T @ d2 / x.shape[0]
        grad_b2 = np.mean(d2, axis=0, keepdims=True)
        d1 = (d2 @ w2.T) * (1.0 - h**2)
        grad_w1 = x.T @ d1 / x.shape[0]
        grad_b1 = np.mean(d1, axis=0, keepdims=True)

        w2 -= cfg.lr * grad_w2
        b2 -= cfg.lr * grad_b2
        w1 -= cfg.lr * grad_w1
        b1 -= cfg.lr * grad_b1

    pred = (_sigmoid(np.tanh(x @ w1 + b1) @ w2 + b2) > 0.5).astype(float)
    acc = float(np.mean(pred == y))
    param_count = w1.size + b1.size + w2.size + b2.size
    energy_proxy = float(param_count * (1.15 if use_theta_memory else 1.0))

    return {
        "accuracy": round(acc, 6),
        "param_count": int(param_count),
        "energy_proxy": round(energy_proxy, 6),
    }


def run_architecture_comparison(cfg: ArchConfig) -> Dict[str, object]:
    base = _train(cfg, use_theta_memory=False)
    gu = _train(cfg, use_theta_memory=True)
    gain = gu["accuracy"] - base["accuracy"]
    eff = gain / max((gu["energy_proxy"] - base["energy_proxy"]), 1e-9)

    return {
        "model": "gu_inspired_architectures",
        "config": cfg.__dict__,
        "summary": {
            "baseline_accuracy": base["accuracy"],
            "gu_theta_memory_accuracy": gu["accuracy"],
            "accuracy_gain": round(gain, 6),
            "energy_normalized_gain": round(eff, 6),
        },
        "canonical_observables": {
            "accuracy_gain": round(gain, 6),
            "energy_delta_proxy": round(float(gu["energy_proxy"] - base["energy_proxy"]), 6),
        },
        "exploratory_metrics": {
            "energy_normalized_gain": round(eff, 6),
        },
        "baseline": base,
        "gu_theta_memory": gu,
    }


def write_report(report: Dict[str, object]) -> Path:
    payload = augment_report(__file__, report)
    return write_contract_report(__file__, payload)


def main() -> None:
    cfg = ArchConfig()
    report = run_architecture_comparison(cfg)
    out_path = write_report(report)
    s = report["summary"]
    print("GU-inspired architectures")
    print(f"- baseline accuracy: {s['baseline_accuracy']}")
    print(f"- GU theta-memory accuracy: {s['gu_theta_memory_accuracy']}")
    print(f"- accuracy gain: {s['accuracy_gain']}")
    print(f"- report: {out_path}")


if __name__ == "__main__":
    main()
