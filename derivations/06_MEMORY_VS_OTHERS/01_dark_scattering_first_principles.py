#!/usr/bin/env python3
"""
Item 1 report: non-perturbative dark-sector scattering coefficient.
"""

from pathlib import Path

from memory_open_items_models import (
    sigma_over_m_velocity_profile,
    write_json_report,
)


def main():
    sigma_contact = 210.0  # cm^2/g geometric upper bound from DG contact estimate
    velocities = [30.0, 100.0, 300.0, 1000.0]
    report = sigma_over_m_velocity_profile(sigma_contact, velocities)
    out = Path(__file__).with_name("dark_scattering_report.json")
    write_json_report(report, str(out))

    print("=" * 80)
    print("GU DARK SCATTERING FIRST-PRINCIPLES REPORT")
    print("=" * 80)
    print(f"C_GU(non-perturbative) = {report['C_GU_nonperturbative']:.6f}")
    print(f"v0 = {report['v0_kms']:.2f} km/s")
    for k in ["30", "100", "300", "1000"]:
        p = report["profiles"][k]
        print(
            f"v={p['velocity_kms']:.0f} km/s -> sigma/m={p['sigma_over_m_cm2_per_g']:.3f} cm^2/g"
            f" (supp={p['suppression_factor']:.3f})"
        )
    print(f"\nReport written: {out}")


if __name__ == "__main__":
    main()

