#!/usr/bin/env python3
"""
Common utilities for Phase 2 biochemical realism modules.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Callable, Dict

import numpy as np


def write_report(script_path: str, payload: Dict[str, object]) -> Path:
    path = Path(script_path)
    out = path.with_name(f"{path.stem}_report.json")
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def finite_diff_jacobian(
    f: Callable[[np.ndarray], np.ndarray], theta: np.ndarray, eps: float = 1e-6
) -> np.ndarray:
    y0 = f(theta)
    m, n = y0.size, theta.size
    j = np.zeros((m, n), dtype=float)
    for k in range(n):
        d = np.zeros_like(theta)
        d[k] = eps
        y1 = f(theta + d)
        y2 = f(theta - d)
        j[:, k] = (y1 - y2) / (2.0 * eps)
    return j


def explicit_euler(rhs: Callable[[np.ndarray, float], np.ndarray], y0: np.ndarray, dt: float, steps: int) -> np.ndarray:
    y = y0.astype(float).copy()
    hist = np.zeros((steps + 1, y.size), dtype=float)
    hist[0] = y
    t = 0.0
    for i in range(steps):
        y = y + dt * rhs(y, t)
        hist[i + 1] = y
        t += dt
    return hist
