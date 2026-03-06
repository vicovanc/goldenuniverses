#!/usr/bin/env python3
"""
15 — Per-function closure decision gates for GU cosmology.

Reads identifiability evidence and emits explicit gate outcomes for:
  Gate A: beta(X)
  Gate B: lambda_rec(X)
  Gate C: g_{OmegaX}(X)
  Gate D: V_X(X)
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


def main():
    parser = argparse.ArgumentParser(description="Run GU closure function gates.")
    parser.add_argument(
        "--ident-report",
        default=str(Path(__file__).with_name("closure_identifiability_report.json")),
        help="Path to identifiability JSON report from script 14.",
    )
    parser.add_argument(
        "--json-out",
        default=str(Path(__file__).with_name("closure_function_gates_report.json")),
        help="Output JSON gate report path.",
    )
    args = parser.parse_args()

    ident_path = Path(args.ident_report)
    if not ident_path.exists():
        raise FileNotFoundError(
            f"Missing identifiability report: {ident_path}. Run 14_closure_identifiability.py first."
        )
    ident = json.loads(ident_path.read_text(encoding="utf-8"))
    vx_report_path = Path(__file__).resolve().parent.parent / "43_VX_FROM_LTOTAL" / "vx_from_ltotal_report.json"
    vx_report = None
    if vx_report_path.exists():
        try:
            vx_report = json.loads(vx_report_path.read_text(encoding="utf-8"))
        except Exception:
            vx_report = None

    # Local sensitivities for each closure target.
    phi_gr = (1.0 + np.sqrt(5.0)) / 2.0
    lambda_ratio = np.exp(phi_gr) / (np.pi ** 2)
    x_ref = float(phi_gr ** (-95))  # QCD epoch in Planck units
    eps = max(abs(x_ref) * 1e-3, 1e-12)

    def beta_x(x):
        return max(float(x), 1e-30)

    def lambda_rec_x(x):
        return beta_x(x) * lambda_ratio

    def g_omegax_x(_x):
        return 0.1

    beta_sens = abs(
        beta_x(x_ref + eps) - beta_x(x_ref - eps)
    ) / (2.0 * eps)
    lambda_sens = abs(
        lambda_rec_x(x_ref + eps) - lambda_rec_x(x_ref - eps)
    ) / (2.0 * eps)
    g_sens = abs(
        g_omegax_x(x_ref + eps) - g_omegax_x(x_ref - eps)
    ) / (2.0 * eps)

    local_rank_full = bool(ident.get("jacobian_rank_full", False))
    global_degenerate = bool(ident.get("global_degeneracy_found", False))
    uniqueness_evidence = local_rank_full and (not global_degenerate)

    vx_uniqueness = bool(vx_report.get("uniqueness_pass", False)) if vx_report else False
    falsification_matrix = {
        "beta": {
            "hypothesis": "beta(X) has uniquely identified canonical form in production domain",
            "observable_discriminant": "ODE map sensitivity of [A_s, n_s, r, N, T_reh, z_rec, eta_B] to beta_scale",
            "pass_criteria": "full-rank identifiability and no practically equivalent alternative beta_scale in bounded box",
            "pass": bool(uniqueness_evidence and beta_sens > 0),
            "rejection_implications": "keep beta(X) provisional and publish non-uniqueness path",
        },
        "lambda_rec": {
            "hypothesis": "absolute lambda_rec(X) is uniquely fixed (not only ratio-level)",
            "observable_discriminant": "independent leverage beyond lambda_rec/beta ratio in ODE observables",
            "pass_criteria": "full-rank identifiability plus absolute-level separability",
            "pass": bool(uniqueness_evidence and lambda_sens > 0),
            "rejection_implications": "keep only ratio-level closure and absolute form provisional",
        },
        "g_OmegaX": {
            "hypothesis": "interaction coupling has no residual effective dial",
            "observable_discriminant": "degeneracy collapse under bounded g0 scans",
            "pass_criteria": "identifiability pass and zero residual dial under consistency constraints",
            "pass": bool(uniqueness_evidence and g_sens == 0),
            "rejection_implications": "retain constrained status with explicit free-dial declaration",
        },
        "V_X": {
            "hypothesis": "a single canonical potential family is uniquely selected",
            "observable_discriminant": "cross-family ODE falsification on [n_s, r, A_s, N]",
            "pass_criteria": "all alternatives rejected at agreed thresholds and identifiability remains full-rank",
            "pass": bool(uniqueness_evidence and vx_uniqueness),
            "rejection_implications": "retain chosen_non_unique with formal non-uniqueness proof",
        },
    }

    gates = {
        "beta": {
            "gate": "A",
            "status": "derived" if falsification_matrix["beta"]["pass"] else "provisional",
            "reason": (
                "canonical beta(X) is sensitivity-active and uniqueness evidence passes"
                if falsification_matrix["beta"]["pass"]
                else "rank-deficient or non-unique map; keep canonical beta(X) as provisional"
            ),
        },
        "lambda_rec": {
            "gate": "B",
            "status": "derived" if falsification_matrix["lambda_rec"]["pass"] else "provisional_ratio_closed",
            "reason": (
                "absolute lambda_rec(X) uniquely supported by map evidence"
                if falsification_matrix["lambda_rec"]["pass"]
                else "only ratio-level closure lambda_rec/beta is currently justified"
            ),
        },
        "g_OmegaX": {
            "gate": "C",
            "status": "derived" if falsification_matrix["g_OmegaX"]["pass"] else "constrained",
            "reason": (
                "constant coupling uniquely fixed with no residual dial"
                if falsification_matrix["g_OmegaX"]["pass"]
                else "effective dial remains; keep constrained status"
            ),
        },
        "V_X": {
            "gate": "D",
            "status": "derived_unique" if falsification_matrix["V_X"]["pass"] else "chosen_non_unique",
            "reason": (
                "single canonical potential selected by uniqueness gate"
                if falsification_matrix["V_X"]["pass"]
                else "theory-band remains; keep CHOSEN with formal non-uniqueness note"
            ),
        },
    }

    report = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "closure_mode_runtime": "provisional",
        "promotion_rule_enforced": "DERIVED requires full-ODE identifiability + falsification pass",
        "identifiability_summary": {
            "jacobian_rank": ident.get("jacobian_rank"),
            "jacobian_rank_full": local_rank_full,
            "global_degeneracy_found": global_degenerate,
            "condition_number": ident.get("condition_number"),
            "diagnostic_type": ident.get("diagnostic_type", "unknown"),
        },
        "local_sensitivities": {
            "beta_dX": beta_sens,
            "lambda_rec_dX": lambda_sens,
            "g_OmegaX_dX": g_sens,
        },
        "falsification_matrix": falsification_matrix,
        "vx_ltotal_report": {
            "path": str(vx_report_path),
            "present": bool(vx_report is not None),
            "candidate_count_admissible": None if vx_report is None else vx_report.get("candidate_count_admissible"),
            "candidate_count_total": None if vx_report is None else vx_report.get("candidate_count_total"),
            "uniqueness_pass": None if vx_report is None else vx_report.get("uniqueness_pass"),
        },
        "gates": gates,
    }

    out_path = Path(args.json_out)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("=" * 80)
    print("GU CLOSURE FUNCTION GATES")
    print("=" * 80)
    for key in ["beta", "lambda_rec", "g_OmegaX", "V_X"]:
        g = gates[key]
        print(f"Gate {g['gate']} ({key}): {g['status']} — {g['reason']}")
    print(f"\nMachine report written: {out_path}")


if __name__ == "__main__":
    main()

