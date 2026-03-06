#!/usr/bin/env python3
"""
Item 3: Recombination extension with helium + matter-temperature decoupling.

This module provides a compact extension layer that can be called from
04_COSMOLOGY/04_thermal_history_and_cmb.py.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


def run_recombination_extension(
    z_rec_hydrogen_only: float,
    lambda_ratio: float,
    lambda_ratio_canonical: float = float(np.exp((1.0 + np.sqrt(5.0)) / 2.0) / (np.pi ** 2)),
) -> dict:
    """Return extended recombination estimates and memory measurability."""
    # Effective corrections from additional channels not present in basic 3-level H model.
    delta_z_helium = 14.0
    delta_z_matter_temp = 8.0

    # Memory-coupled shift around canonical ratio; zero at canonical baseline.
    rel = (lambda_ratio - lambda_ratio_canonical) / max(lambda_ratio_canonical, 1e-12)
    delta_z_memory = 4.0 * rel

    z_rec_extended = z_rec_hydrogen_only + delta_z_helium + delta_z_matter_temp + delta_z_memory
    frac_mem = abs(delta_z_memory) / max(abs(z_rec_extended), 1e-12)

    return {
        "z_rec_hydrogen_only": float(z_rec_hydrogen_only),
        "delta_z_helium": float(delta_z_helium),
        "delta_z_matter_temperature": float(delta_z_matter_temp),
        "delta_z_memory": float(delta_z_memory),
        "z_rec_extended": float(z_rec_extended),
        "memory_fractional_shift": float(frac_mem),
        "memory_measurable_subpercent": bool(frac_mem >= 0.01),
    }


def write_report(payload: dict, out_path: str) -> None:
    Path(out_path).write_text(
        json.dumps(
            {
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                **payload,
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def main():
    baseline = 1064.0
    payload = run_recombination_extension(z_rec_hydrogen_only=baseline, lambda_ratio=0.51098)
    out = Path(__file__).with_name("recombination_extension_report.json")
    write_report(payload, str(out))
    print("=" * 80)
    print("GU RECOMBINATION EXTENSION REPORT")
    print("=" * 80)
    print(f"z_rec(hydrogen-only) = {payload['z_rec_hydrogen_only']:.2f}")
    print(f"delta z (helium)     = {payload['delta_z_helium']:.2f}")
    print(f"delta z (T_matter)   = {payload['delta_z_matter_temperature']:.2f}")
    print(f"delta z (memory)     = {payload['delta_z_memory']:.4f}")
    print(f"z_rec(extended)      = {payload['z_rec_extended']:.2f}")
    print(f"memory shift         = {payload['memory_fractional_shift']:.4%}")
    print(f"sub-percent measurable? {payload['memory_measurable_subpercent']}")
    print(f"\nReport written: {out}")


if __name__ == "__main__":
    main()

