#!/usr/bin/env python3
"""
Phase III-3: Long-range connectivity as theta superhighways.

Constructs a modular graph with short and long-range links and computes:
  - characteristic path length,
  - global efficiency proxy,
  - communication bandwidth proxy.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Dict, List

import networkx as nx

from nn_redo_common import augment_report, write_report as write_contract_report

@dataclass
class ConnectivityConfig:
    n_nodes: int = 72
    local_degree: int = 4
    n_long_edges: int = 40
    long_edge_weight: float = 0.45
    local_edge_weight: float = 1.0


def _build_graph(cfg: ConnectivityConfig) -> nx.Graph:
    g = nx.watts_strogatz_graph(cfg.n_nodes, cfg.local_degree, 0.05, seed=45)
    added = 0
    i = 0
    while added < cfg.n_long_edges and i < cfg.n_nodes * 20:
        u = (7 * i + 3) % cfg.n_nodes
        v = (11 * i + 17) % cfg.n_nodes
        if u != v and not g.has_edge(u, v):
            g.add_edge(u, v, weight=cfg.long_edge_weight)
            added += 1
        i += 1
    for u, v in g.edges():
        if "weight" not in g[u][v]:
            g[u][v]["weight"] = cfg.local_edge_weight
    return g


def run_connectivity(cfg: ConnectivityConfig) -> Dict[str, object]:
    g = _build_graph(cfg)

    spl = nx.average_shortest_path_length(g, weight="weight")
    glob_eff = nx.global_efficiency(g)
    clustering = nx.average_clustering(g)

    # Simple bandwidth proxy from inverse weighted path length.
    bandwidth_proxy = 1.0 / max(spl, 1e-9)

    hubs: List[int] = sorted(g.degree, key=lambda x: x[1], reverse=True)[:8]

    # Sensitivity envelope: long-edge count perturbation around nominal.
    envelope = []
    for frac in [0.9, 1.0, 1.1]:
        cfg_p = ConnectivityConfig(
            n_nodes=cfg.n_nodes,
            local_degree=cfg.local_degree,
            n_long_edges=max(1, int(round(cfg.n_long_edges * frac))),
            long_edge_weight=cfg.long_edge_weight,
            local_edge_weight=cfg.local_edge_weight,
        )
        g_p = _build_graph(cfg_p)
        spl_p = nx.average_shortest_path_length(g_p, weight="weight")
        envelope.append(
            {
                "long_edge_scale": frac,
                "n_long_edges": cfg_p.n_long_edges,
                "global_efficiency": round(float(nx.global_efficiency(g_p)), 6),
                "bandwidth_proxy": round(float(1.0 / max(spl_p, 1e-9)), 6),
            }
        )

    return {
        "model": "long_range_connectivity",
        "config": cfg.__dict__,
        "summary": {
            "average_shortest_path_weighted": round(float(spl), 6),
            "global_efficiency": round(float(glob_eff), 6),
            "average_clustering": round(float(clustering), 6),
            "bandwidth_proxy": round(float(bandwidth_proxy), 6),
            "n_edges_total": g.number_of_edges(),
        },
        "top_hubs": [{"node": int(n), "degree": int(d)} for n, d in hubs],
        "diagnostics": {"sensitivity_envelope": envelope},
    }


def write_report(report: Dict[str, object]) -> Path:
    payload = augment_report(__file__, report)
    return write_contract_report(__file__, payload)


def main() -> None:
    cfg = ConnectivityConfig()
    report = run_connectivity(cfg)
    out_path = write_report(report)
    s = report["summary"]
    print("Long-range connectivity (GU)")
    print(f"- weighted shortest path: {s['average_shortest_path_weighted']}")
    print(f"- global efficiency: {s['global_efficiency']}")
    print(f"- bandwidth proxy: {s['bandwidth_proxy']}")
    print(f"- report: {out_path}")


if __name__ == "__main__":
    main()
