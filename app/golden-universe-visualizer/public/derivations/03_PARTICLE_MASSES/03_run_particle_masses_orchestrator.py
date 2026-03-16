#!/usr/bin/env python3
"""
STATUS: canonical_integration
ROLE: Orchestrator/reporting entrypoint for 03_PARTICLE_MASSES.

This script does not claim first-principles closure for all sectors. It runs:
1) local legacy mass report for leptons (01_all_particle_masses.py), and
2) canonical quark derivation script in 31_QUARK_MASSES.

Each section prints provenance so outputs are not misattributed.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _run_python_script(script_path: Path, timeout_s: int = 240) -> Tuple[int, str]:
    cmd = ["python3", str(script_path)]
    proc = subprocess.run(
        cmd,
        cwd=str(_project_root()),
        capture_output=True,
        text=True,
        timeout=timeout_s,
        check=False,
    )
    output = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    return proc.returncode, output


def _extract_lepton_errors(raw_output: str) -> Dict[str, str]:
    """
    Parse lepton error lines from 01_all_particle_masses.py output.
    """
    result: Dict[str, str] = {}
    lines = raw_output.splitlines()
    particles = ["ELECTRON", "MUON", "TAU"]
    for idx, line in enumerate(lines):
        clean = line.strip()
        if clean in {f"{p}:" for p in particles}:
            name = clean[:-1].lower()
            window = lines[idx : idx + 12]
            for w in window:
                if "Error:" in w:
                    result[name] = w.strip().replace("Error:", "").strip()
                    break
    return result


def _extract_quark_summary_tail(raw_output: str, max_lines: int = 16) -> List[str]:
    """
    Keep a concise tail for canonical quark script output display.
    """
    lines = [ln.rstrip() for ln in raw_output.splitlines() if ln.strip()]
    if not lines:
        return ["(no output captured)"]
    return lines[-max_lines:]


def main() -> None:
    root = _project_root()
    local_01 = root / "derivations" / "03_PARTICLE_MASSES" / "01_all_particle_masses.py"
    canonical_31 = (
        root / "derivations" / "31_QUARK_MASSES" / "25_corrected_quark_derivations.py"
    )

    print("=" * 88)
    print("03_PARTICLE_MASSES ORCHESTRATOR")
    print("Status model: 0 free params + 1 boundary condition (m_e) for mass closure wording")
    print("=" * 88)

    print("\n[SECTION A] LOCAL LEPTON REPORT (legacy-local provenance)")
    print(f"Source: {local_01}")
    rc_01, out_01 = _run_python_script(local_01)
    print(f"Exit code: {rc_01}")
    if rc_01 != 0:
        print("Result: FAILED")
    else:
        lepton_errors = _extract_lepton_errors(out_01)
        if lepton_errors:
            print("Parsed lepton error summary:")
            for key in ("electron", "muon", "tau"):
                val = lepton_errors.get(key, "not found")
                print(f"  - {key}: {val}")
        else:
            print("Parsed lepton error summary: unavailable (format changed).")

    print("\n[SECTION B] CANONICAL QUARK REPORT (31_QUARK_MASSES provenance)")
    print(f"Source: {canonical_31}")
    if not canonical_31.exists():
        print("Result: SKIPPED (canonical script not found).")
    else:
        rc_31, out_31 = _run_python_script(canonical_31)
        print(f"Exit code: {rc_31}")
        if rc_31 != 0:
            print("Result: FAILED")
        else:
            print("Canonical output tail:")
            for ln in _extract_quark_summary_tail(out_31):
                print(f"  {ln}")

    print("\n[SECTION C] STATUS AND HONESTY FLAGS")
    print("- local lepton report: reference_legacy / leptons_derived_local")
    print("- local quark scripts in this folder: quarks_not_derived_local unless stated otherwise")
    print("- canonical quark closure: derivations/31_QUARK_MASSES")
    print("- unsupported final closure sectors here: neutrino/higgs mass closure")
    print("- this orchestrator reports provenance; it does not relabel exploratory scripts as canonical")


if __name__ == "__main__":
    main()
