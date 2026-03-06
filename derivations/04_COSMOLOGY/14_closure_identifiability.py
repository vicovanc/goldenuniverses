#!/usr/bin/env python3
"""
14 — Full ODE-backed closure identifiability diagnostics for GU cosmology.

Observable map F(Theta):
  [A_s, n_s, r, N_end, T_reh, z_rec_proxy, eta_B_proxy]

Theta:
  [beta_scale, lambda_ratio, g0, mu_or_f, v_form]
where v_form = 0 (plateau-like), 1 (axion-like).
"""

import argparse
import json
from datetime import datetime, timezone
from importlib.machinery import SourceFileLoader
from pathlib import Path

import numpy as np

PHI = (1.0 + np.sqrt(5.0)) / 2.0
LAMBDA_RATIO_CANON = np.exp(PHI) / (np.pi ** 2)
KAPPA0 = 1.746

closure = SourceFileLoader(
    "gu_closure_core_ident",
    str(Path(__file__).with_name("10_coupled_ode_system.py")),
).load_module()

_CACHE = {}


def _round_key(theta):
    return tuple(float(f"{x:.8g}") for x in theta)


def _build_potential(v_form, mu_or_f):
    if v_form < 0.5:
        class ParamPlateau:
            name = "PlateauParam"
            N_target = 70.5
            A_s = 2.1e-9

            def __init__(self, mu):
                self.mu = max(mu, 0.4)
                x_star = self.mu * np.log(4.0 * self.N_target / 3.0)
                exp_arg = np.exp(x_star / self.mu)
                eps_star = (4.0 / 3.0) / max((exp_arg - 1.0) ** 2, 1e-20)
                self.V_0 = 24.0 * np.pi ** 2 * closure.M_P ** 4 * self.A_s * eps_star

            def V(self, x):
                a = x / self.mu
                if a > 500:
                    return self.V_0
                return self.V_0 * (1.0 - np.exp(-a)) ** 2

            def dV(self, x):
                a = x / self.mu
                if a > 500:
                    return 0.0
                ex = np.exp(-a)
                return self.V_0 * 2.0 * (1.0 - ex) * ex / self.mu

            def ddV(self, x):
                a = x / self.mu
                if a > 500:
                    return 0.0
                ex = np.exp(-a)
                return self.V_0 * 2.0 * ex * (2.0 * ex - 1.0) / self.mu ** 2

        return ParamPlateau(mu_or_f)

    class ParamAxion:
        name = "AxionParam"
        N_target = 70.5
        A_s = 2.1e-9

        def __init__(self, f_x):
            self.f_X = max(f_x, 2.5)
            cot_end = np.sqrt(2.0) * self.f_X / closure.M_P
            self.X_end = 2.0 * self.f_X * np.arctan(1.0 / max(cot_end, 1e-12))
            cos_half_end = np.cos(self.X_end / (2.0 * self.f_X))
            cos_half_star = cos_half_end * np.exp(-self.N_target * closure.M_P ** 2 / (2.0 * self.f_X ** 2))
            cos_half_star = np.clip(cos_half_star, -0.999999, 0.999999)
            self.X_star = 2.0 * self.f_X * np.arccos(cos_half_star)
            eps_star = (closure.M_P / self.f_X) ** 2 / 2.0 * \
                (np.sin(self.X_star / self.f_X)) ** 2 / \
                max((1.0 - np.cos(self.X_star / self.f_X)) ** 2, 1e-20)
            self.Lambda4 = 24.0 * np.pi ** 2 * closure.M_P ** 4 * self.A_s * eps_star

        def V(self, x):
            return self.Lambda4 * (1.0 - np.cos(x / self.f_X))

        def dV(self, x):
            return self.Lambda4 * np.sin(x / self.f_X) / self.f_X

        def ddV(self, x):
            return self.Lambda4 * np.cos(x / self.f_X) / self.f_X ** 2

    return ParamAxion(mu_or_f)


def _patched_observables(theta):
    key = _round_key(theta)
    if key in _CACHE:
        return _CACHE[key]

    beta_scale, lambda_ratio, g0, mu_or_f, v_form = theta
    beta_scale = float(np.clip(beta_scale, 0.6, 1.6))
    lambda_ratio = float(np.clip(lambda_ratio, 0.35, 0.75))
    g0 = float(np.clip(g0, 0.01, 0.35))
    mu_or_f = float(np.clip(mu_or_f, 0.6, 7.0))
    v_form = 1.0 if v_form >= 0.5 else 0.0

    old_g0 = closure.g_0
    old_ratio = closure.lambda_rec_over_beta
    old_beta_fn = closure.beta_X

    def beta_scaled(x, closure_mode=None):
        _ = closure._sanitize_closure_mode(closure_mode)
        return max(beta_scale * float(x), 1e-30)

    try:
        closure.g_0 = g0
        closure.lambda_rec_over_beta = lambda_ratio
        closure.beta_X = beta_scaled

        pot = _build_potential(v_form, mu_or_f)
        res = closure.run_inflation(pot, mode="slow_roll", N_max=180)

        sr = res["sr_star"]
        i_star = res["i_star"]
        x_star = res["X"][i_star]
        m_star = res["M"][i_star]
        v_star = closure.V_eff(x_star, m_star, pot=pot, closure_mode=closure.CLOSURE_MODE)
        eps = max(sr["epsilon"], 1e-20)
        a_s = v_star / (24.0 * np.pi ** 2 * closure.M_P ** 4 * eps)

        # Reheating proxy from interaction + local curvature scale.
        m_x = np.sqrt(max(abs(pot.ddV(max(abs(x_star) * 0.2, 1e-4))), 1e-12))
        gamma = (g0 ** 2) * m_x / (8.0 * np.pi)
        t_reh = np.sqrt(max(gamma, 1e-20))

        # z_rec proxy from dynamical kappa shift.
        n_arr = res["N"]
        x_arr = res["X"]
        kappa_vals = []
        for i in range(1, len(n_arr)):
            d_n = n_arr[i] - n_arr[i - 1]
            if d_n <= 0 or x_arr[i] <= 0:
                continue
            d_x_d_n = (x_arr[i] - x_arr[i - 1]) / d_n
            kappa_vals.append(-1.0 / (np.log(PHI) * x_arr[i]) * d_x_d_n)
        kappa_mean = float(np.median(kappa_vals)) if kappa_vals else KAPPA0
        z_rec = 1089.8 * (1.0 + 0.12 * (kappa_mean - KAPPA0) / max(KAPPA0, 1e-12))

        # Baryogenesis proxy tied to closure-sector dials.
        eta_b = 6.12e-10 * (g0 / 0.1) * (lambda_ratio / LAMBDA_RATIO_CANON) * (2.0 - beta_scale)

        obs = np.array([a_s, sr["n_s"], sr["r"], res["N_end"], t_reh, z_rec, eta_b], dtype=float)
    except Exception:
        obs = np.array([np.nan] * 7, dtype=float)
    finally:
        closure.g_0 = old_g0
        closure.lambda_rec_over_beta = old_ratio
        closure.beta_X = old_beta_fn

    _CACHE[key] = obs
    return obs


def local_jacobian(theta0, eps=5e-3):
    f0 = _patched_observables(theta0)
    if np.any(~np.isfinite(f0)):
        raise RuntimeError("Baseline ODE observables are non-finite.")
    jac = np.zeros((len(f0), len(theta0)))
    for j in range(len(theta0)):
        step = eps * max(abs(theta0[j]), 1.0)
        t_plus = theta0.copy()
        t_minus = theta0.copy()
        t_plus[j] += step
        t_minus[j] -= step
        fp = _patched_observables(t_plus)
        fm = _patched_observables(t_minus)
        jac[:, j] = (fp - fm) / (2.0 * step)
    return jac


def find_degeneracy_evidence(theta_center, n_samples=24, tol=0.02, obs_equiv_thresholds=None):
    rng = np.random.default_rng(42)
    scales = np.array([0.08, 0.03, 0.06, 0.25, 1.0], dtype=float)
    thetas = theta_center + rng.normal(size=(n_samples, 5)) * scales
    thetas[:, 0] = np.clip(thetas[:, 0], 0.7, 1.4)
    thetas[:, 1] = np.clip(thetas[:, 1], 0.35, 0.75)
    thetas[:, 2] = np.clip(thetas[:, 2], 0.01, 0.30)
    thetas[:, 3] = np.clip(thetas[:, 3], 0.7, 7.0)
    thetas[:, 4] = np.where(thetas[:, 4] >= 0.5, 1.0, 0.0)

    obs = np.array([_patched_observables(t) for t in thetas])
    valid = np.all(np.isfinite(obs), axis=1)
    thetas = thetas[valid]
    obs = obs[valid]
    if len(obs) < 4:
        return False, None, None, None, None, None, None, None

    norm = np.maximum(np.std(obs, axis=0), 1e-12)
    if obs_equiv_thresholds is not None:
        norm = np.maximum(norm, np.asarray(obs_equiv_thresholds, dtype=float))
    normed = obs / norm

    for i in range(len(obs)):
        for j in range(i + 1, len(obs)):
            dist = np.linalg.norm(normed[i] - normed[j]) / np.sqrt(normed.shape[1])
            if dist < tol and np.linalg.norm(thetas[i] - thetas[j]) > 0.08:
                return True, i, j, dist, thetas[i], thetas[j], obs[i], obs[j]
    return False, None, None, None, None, None, None, None


def main():
    parser = argparse.ArgumentParser(description="GU full ODE closure identifiability diagnostics.")
    parser.add_argument(
        "--json-out",
        default=str(Path(__file__).with_name("closure_identifiability_report.json")),
        help="Path to write diagnostics JSON report.",
    )
    args = parser.parse_args()

    theta0 = np.array([1.0, LAMBDA_RATIO_CANON, 0.1, 1.22, 0.0], dtype=float)
    jac = local_jacobian(theta0)
    rank = np.linalg.matrix_rank(jac, tol=1e-8)
    svals = np.linalg.svd(jac, compute_uv=False)
    cond = svals[0] / max(svals[-1], 1e-14)
    baseline_obs = _patched_observables(theta0)

    print("=" * 80)
    print("GU FULL-ODE CLOSURE IDENTIFIABILITY DIAGNOSTICS")
    print("=" * 80)
    print(f"Theta0 = [beta_scale, lambda_ratio, g0, mu_or_f, v_form] = {theta0}")
    print(f"Baseline observables = {baseline_obs}")
    print(f"Local Jacobian shape: {jac.shape}")
    print(f"Local Jacobian rank : {rank} / {jac.shape[1]}")
    print(f"Singular values     : {svals}")
    print(f"Condition number    : {cond:.3e}")

    obs_equiv_thresholds = [
        2.5e-10,  # A_s absolute tolerance
        0.0042,   # n_s (Planck 1 sigma)
        0.005,    # r practical equivalence
        1.0,      # N
        0.2,      # T_reh (log-level proxy, normalized by spread anyway)
        25.0,     # z_rec proxy
        1.5e-10,  # eta_B
    ]
    is_degenerate, i, j, dist, th_i, th_j, obs_i, obs_j = find_degeneracy_evidence(
        theta0,
        obs_equiv_thresholds=obs_equiv_thresholds,
    )
    print("\nDegeneracy search:")
    if is_degenerate:
        print("  Evidence found: Theta_i != Theta_j with near-equivalent observables.")
        print(f"  Pair indices: ({i}, {j}), normalized distance={dist:.3e}")
        print(f"  Theta_i: {th_i}")
        print(f"  Theta_j: {th_j}")
        print(f"  Obs_i  : {obs_i}")
        print(f"  Obs_j  : {obs_j}")
    else:
        print("  No near-degenerate pair found in bounded sampled domain.")

    local_unique = rank == jac.shape[1]
    print("\nLocal uniqueness gate:")
    print(f"  Pass = {local_unique}")
    if not local_unique:
        print("  Reason: rank-deficient local Jacobian.")

    report = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "diagnostic_type": "full_ode_backed",
        "theta0": theta0.tolist(),
        "baseline_observables": baseline_obs.tolist(),
        "jacobian_shape": list(jac.shape),
        "jacobian_rank": int(rank),
        "jacobian_rank_full": bool(local_unique),
        "singular_values": svals.tolist(),
        "condition_number": float(cond),
        "global_degeneracy_found": bool(is_degenerate),
        "degeneracy_pair": {
            "i": None if i is None else int(i),
            "j": None if j is None else int(j),
            "normalized_distance": None if dist is None else float(dist),
            "theta_i": None if th_i is None else th_i.tolist(),
            "theta_j": None if th_j is None else th_j.tolist(),
            "obs_i": None if obs_i is None else obs_i.tolist(),
            "obs_j": None if obs_j is None else obs_j.tolist(),
        },
        "reproducibility": {
            "script": str(Path(__file__).name),
            "seed": 42,
            "cache_size": len(_CACHE),
        },
        "observable_equivalence_thresholds": {
            "A_s": obs_equiv_thresholds[0],
            "n_s": obs_equiv_thresholds[1],
            "r": obs_equiv_thresholds[2],
            "N": obs_equiv_thresholds[3],
            "T_reh_proxy": obs_equiv_thresholds[4],
            "z_rec_proxy": obs_equiv_thresholds[5],
            "eta_B_proxy": obs_equiv_thresholds[6],
        },
    }
    out_path = Path(args.json_out)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nMachine report written: {out_path}")


if __name__ == "__main__":
    main()

