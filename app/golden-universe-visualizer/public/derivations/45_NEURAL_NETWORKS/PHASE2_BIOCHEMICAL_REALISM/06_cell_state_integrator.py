#!/usr/bin/env python3
"""
Track A6: Coupled cell-state integrator with conservation diagnostics.
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


def run_integrator() -> Dict[str, object]:
    c = _load("00_common.py", "_p2_common")

    # [S_ext,S_cyt,ATP,ADP,Pi,NADH,NADplus,H_in,H_out,mRNA,Prot,m,h,n,Na_in,Na_out,K_in,K_out,Cl_in,Cl_out]
    y = np.array(
        [
            4.0, 0.3, 2.0, 1.0, 1.0, 0.4, 1.6, 1.0, 1.0, 0.05, 0.1,
            0.05, 0.6, 0.32, 15.0, 145.0, 140.0, 5.0, 10.0, 110.0,
        ],
        dtype=float,
    )
    y0 = y.copy()
    dt = 0.001
    steps = 12000

    def nernst(v_in: float, v_out: float, z: float) -> float:
        return 26.7 / z * np.log(max(v_out, 1e-9) / max(v_in, 1e-9))

    for _ in range(steps):
        (
            s_ext, s_cyt, atp, adp, pi, nadh, nadp, h_in, h_out, mrna, prot,
            m, h, n, na_in, na_out, k_in, k_out, cl_in, cl_out
        ) = y

        v_uptake = 0.15 * s_ext / (1.0 + s_ext)
        v_cat = 0.08 * s_cyt * adp * pi * nadp / (1.0 + s_cyt)
        v_atpase = 0.04 * atp
        v_etc = 0.06 * nadh * h_in / (1.0 + nadh)

        p_k, p_na, p_cl = 1.0, 0.05, 0.45
        vm = 26.7 * np.log(
            max(p_k * k_out + p_na * na_out + p_cl * cl_in, 1e-9)
            / max(p_k * k_in + p_na * na_in + p_cl * cl_out, 1e-9)
        )
        m_inf = 1.0 / (1.0 + np.exp(-(vm + 35.0) / 7.5))
        h_inf = 1.0 / (1.0 + np.exp((vm + 58.0) / 8.0))
        n_inf = 1.0 / (1.0 + np.exp(-(vm + 30.0) / 10.0))
        dm = (m_inf - m) / 1.0
        dh = (h_inf - h) / 5.0
        dn = (n_inf - n) / 3.5

        e_na = nernst(na_in, na_out, 1.0)
        e_k = nernst(k_in, k_out, 1.0)
        e_cl = nernst(cl_in, cl_out, -1.0)
        g_na = (m**3) * h
        g_k = n**4
        g_cl = 0.15
        j_na = 0.002 * g_na * (vm - e_na)
        j_k = 0.002 * g_k * (vm - e_k)
        j_cl = 0.002 * g_cl * (vm - e_cl)
        j_pump = 0.01 * atp * (na_in / (na_in + 10.0)) * (k_out / (k_out + 1.0))

        vm_norm = np.clip((vm + 90.0) / 50.0, 0.0, 1.0)
        epi_drive = 0.4 + 0.6 * vm_norm
        tx = 0.03 * epi_drive * atp / (0.5 + atp)
        tl = 0.04 * mrna * atp / (0.5 + atp)
        mrna_decay = 0.02 * mrna
        prot_decay = 0.005 * prot
        h_leak = 0.02 * (h_out - h_in)

        dy = np.array(
            [
                -v_uptake,
                +v_uptake - v_cat + mrna_decay + prot_decay,
                +v_cat - v_atpase - tx - tl - j_pump,
                -v_cat + v_atpase + tx + tl + j_pump,
                -v_cat + v_atpase + j_pump,
                +v_cat - v_etc,
                -v_cat + v_etc,
                -v_etc + h_leak,
                +v_etc - h_leak,
                +tx - mrna_decay - tl,
                +tl - prot_decay,
                dm,
                dh,
                dn,
                -j_na - 3.0 * j_pump,
                +j_na + 3.0 * j_pump,
                -j_k + 2.0 * j_pump,
                +j_k - 2.0 * j_pump,
                -j_cl,
                +j_cl,
            ],
            dtype=float,
        )
        y = y + dt * dy
        for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14, 15, 16, 17, 18, 19]:
            y[i] = max(y[i], 1e-9)
        y[11:14] = np.clip(y[11:14], 0.0, 1.0)

    (
        s_ext, s_cyt, atp, adp, pi, nadh, nadp, h_in, h_out, mrna, prot,
        m, h, n, na_in, na_out, k_in, k_out, cl_in, cl_out
    ) = y

    def frac_drift(v1: float, v0: float) -> float:
        return float((v1 - v0) / max(abs(v0), 1e-12))

    carbon0 = y0[0] + y0[1] + y0[9] + y0[10]
    carbon1 = s_ext + s_cyt + mrna + prot
    na0, na1 = y0[14] + y0[15], na_in + na_out
    k0, k1 = y0[16] + y0[17], k_in + k_out
    cl0, cl1 = y0[18] + y0[19], cl_in + cl_out
    proton0, proton1 = y0[7] + y0[8], h_in + h_out
    aden0, aden1 = y0[2] + y0[3], atp + adp
    pyr0, pyr1 = y0[5] + y0[6], nadh + nadp
    charge0 = na0 + k0 - cl0 + proton0
    charge1 = na1 + k1 - cl1 + proton1
    energy0 = aden0 + pyr0 + y0[4]
    energy1 = aden1 + pyr1 + pi

    carbon_drift = frac_drift(carbon1, carbon0)
    charge_drift = frac_drift(charge1, charge0)
    energy_drift = frac_drift(energy1, energy0)

    payload = {
        "model": "cell_state_integrator",
        "config": {"dt": dt, "steps": steps, "state_dim": 20, "integration_mode": "fully_coupled"},
        "assumptions": [
            "Reaction, membrane, metabolism, and gene states are integrated in one loop.",
            "Conservation checks target explicit near-invariant pools."
        ],
        "units": {"drift": "fraction", "vm": "mV", "concentration": "mM"},
        "parameter_provenance": {"source": "coupled phase2.1 reconstruction"},
        "summary": {
            "carbon_proxy_drift": float(carbon_drift),
            "charge_proxy_drift": float(charge_drift),
            "energy_proxy_drift": float(energy_drift),
            "integrated_vm_rest_mV": float(vm),
            "integrated_energy_charge": float(atp / max(atp + adp, 1e-12)),
            "integrated_protein_A": float(prot),
        },
        "diagnostics": {
            "invariant_pools": {
                "adenylate_total_initial": float(aden0),
                "adenylate_total_final": float(aden1),
                "pyridine_total_initial": float(pyr0),
                "pyridine_total_final": float(pyr1),
                "proton_total_initial": float(proton0),
                "proton_total_final": float(proton1),
                "na_total_initial": float(na0),
                "na_total_final": float(na1),
                "k_total_initial": float(k0),
                "k_total_final": float(k1),
                "cl_total_initial": float(cl0),
                "cl_total_final": float(cl1),
                "carbon_pool_initial": float(carbon0),
                "carbon_pool_final": float(carbon1),
            },
            "conservation_checks": {
                "carbon_pass_abs_lt_0p35": bool(abs(carbon_drift) < 0.35),
                "charge_pass_abs_lt_0p20": bool(abs(charge_drift) < 0.20),
                "energy_pass_abs_lt_0p40": bool(abs(energy_drift) < 0.40),
                "carbon_pass_abs_lt_0p02": bool(abs(carbon_drift) < 0.02),
                "charge_pass_abs_lt_0p02": bool(abs(charge_drift) < 0.02),
                "energy_pass_abs_lt_0p03": bool(abs(energy_drift) < 0.03),
            }
        },
    }
    out = c.write_report(__file__, payload)
    return {"output": str(out), "payload": payload}


def main() -> None:
    result = run_integrator()
    print(f"wrote {result['output']}")


if __name__ == "__main__":
    main()
