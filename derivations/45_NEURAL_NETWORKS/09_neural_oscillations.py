#!/usr/bin/env python3
"""
Phase III-2: Neural oscillations as collective theta-field resonances.

Builds a synthetic signal from canonical rhythm bands and estimates the power
distribution over delta/theta/alpha/beta/gamma ranges.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Dict, Tuple

import numpy as np

from nn_redo_common import augment_report, write_report as write_contract_report

@dataclass
class OscillationConfig:
    fs_hz: float = 500.0
    duration_s: float = 8.0
    seed: int = 90


def _band_power(freq: np.ndarray, pxx: np.ndarray, lo: float, hi: float) -> float:
    mask = (freq >= lo) & (freq < hi)
    return float(np.trapezoid(pxx[mask], freq[mask])) if np.any(mask) else 0.0


def run_oscillation_model(cfg: OscillationConfig) -> Dict[str, object]:
    rng = np.random.default_rng(cfg.seed)
    n = int(cfg.fs_hz * cfg.duration_s)
    t = np.arange(n) / cfg.fs_hz

    # Composite rhythm signal.
    sig = (
        0.8 * np.sin(2 * np.pi * 2.0 * t)   # delta
        + 1.1 * np.sin(2 * np.pi * 6.0 * t) # theta
        + 0.9 * np.sin(2 * np.pi * 10.0 * t) # alpha
        + 0.55 * np.sin(2 * np.pi * 20.0 * t) # beta
        + 0.35 * np.sin(2 * np.pi * 42.0 * t) # gamma
        + 0.12 * rng.normal(size=n)
    )

    freq = np.fft.rfftfreq(n, d=1.0 / cfg.fs_hz)
    fft = np.fft.rfft(sig)
    pxx = (np.abs(fft) ** 2) / n

    bands: Dict[str, Tuple[float, float]] = {
        "delta": (1.0, 4.0),
        "theta": (4.0, 8.0),
        "alpha": (8.0, 13.0),
        "beta": (13.0, 30.0),
        "gamma": (30.0, 80.0),
    }
    powers = {k: _band_power(freq, pxx, lo, hi) for k, (lo, hi) in bands.items()}
    total = sum(powers.values()) + 1e-12
    frac = {k: v / total for k, v in powers.items()}
    dominant_band = max(frac, key=frac.get)

    # Sensitivity envelope: vary theta amplitude and re-evaluate dominant fraction.
    envelope = []
    for theta_scale in [0.9, 1.0, 1.1]:
        sig_p = (
            0.8 * np.sin(2 * np.pi * 2.0 * t)
            + (1.1 * theta_scale) * np.sin(2 * np.pi * 6.0 * t)
            + 0.9 * np.sin(2 * np.pi * 10.0 * t)
            + 0.55 * np.sin(2 * np.pi * 20.0 * t)
            + 0.35 * np.sin(2 * np.pi * 42.0 * t)
        )
        pxx_p = (np.abs(np.fft.rfft(sig_p)) ** 2) / n
        powers_p = {k: _band_power(freq, pxx_p, lo, hi) for k, (lo, hi) in bands.items()}
        total_p = sum(powers_p.values()) + 1e-12
        frac_p = {k: v / total_p for k, v in powers_p.items()}
        dom_p = max(frac_p, key=frac_p.get)
        envelope.append(
            {
                "theta_scale": theta_scale,
                "dominant_band": dom_p,
                "dominant_fraction": round(float(frac_p[dom_p]), 6),
            }
        )

    return {
        "model": "neural_oscillations",
        "config": cfg.__dict__,
        "summary": {
            "dominant_band": dominant_band,
            "dominant_fraction": round(float(frac[dominant_band]), 6),
            "theta_alpha_ratio": round(float(powers["theta"] / (powers["alpha"] + 1e-12)), 6),
            "gamma_fraction": round(float(frac["gamma"]), 6),
        },
        "band_power_fraction": {k: round(float(v), 6) for k, v in frac.items()},
        "diagnostics": {"sensitivity_envelope": envelope},
    }


def write_report(report: Dict[str, object]) -> Path:
    payload = augment_report(__file__, report)
    return write_contract_report(__file__, payload)


def main() -> None:
    cfg = OscillationConfig()
    report = run_oscillation_model(cfg)
    out_path = write_report(report)
    s = report["summary"]
    print("Neural oscillations (GU)")
    print(f"- dominant band: {s['dominant_band']}")
    print(f"- dominant fraction: {s['dominant_fraction']}")
    print(f"- theta/alpha ratio: {s['theta_alpha_ratio']}")
    print(f"- report: {out_path}")


if __name__ == "__main__":
    main()
