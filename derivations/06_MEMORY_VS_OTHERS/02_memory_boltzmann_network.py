#!/usr/bin/env python3
"""
Item 2 report: full memory-coupled Boltzmann network.
"""

from pathlib import Path

from memory_open_items_models import (
    BoltzmannConfig,
    solve_memory_coupled_boltzmann,
    write_json_report,
)


def main():
    cfg = BoltzmannConfig()
    result = solve_memory_coupled_boltzmann(cfg)
    out = Path(__file__).with_name("boltzmann_memory_report.json")
    write_json_report(result, str(out))

    print("=" * 80)
    print("GU MEMORY-COUPLED BOLTZMANN NETWORK REPORT")
    print("=" * 80)
    print(f"eta_B(with memory)     = {result['eta_B']:.6e}")
    print(f"eta_B(no memory)       = {result['eta_B_no_memory']:.6e}")
    print(f"memory fractional shift= {result['memory_fractional_shift']:.4%}")
    print(f"final M                = {result['final_state']['M']:.6e}")
    print(f"\nReport written: {out}")


if __name__ == "__main__":
    main()

