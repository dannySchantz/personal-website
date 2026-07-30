from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from fission1d.paths import RESULTS_DIR

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


CONFIG_NAMES = {0: "UO2-UO2", 1: "MOX-MOX", 2: "UO2-MOX"}

# Power normalization constants
P_REACTOR = 3565e6              # W  (3565 MW_th)
E_FISSION = 200 * 1.602e-13    # J  (200 MeV per fission)
H_ACTIVE = 365.76              # cm (active fuel height, 12 ft)
N_ASSEMBLIES = 193              # full-core assembly count


def LoadMCModule():
    from fission1d import monte_carlo as mod
    return mod


def LoadJson(energy_groups: int) -> dict:
    from fission1d.paths import DATA_DIR
    p = DATA_DIR / f"parsed_output_{energy_groups}_group.json"
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def RunConfig(mc, base: dict, config: int, generations: int, histories: int,
               skip: int, seed: int, engine: str):
    ri = dict(base)
    ri["Config"] = config
    ri["Generations"] = generations
    ri["Histories"] = histories
    ri["Skip"] = min(skip, max(0, generations - 1))

    xs = mc.BuildCrossSectionTables(ri)
    mesh_data = mc.CreateMeshAndAssignData(ri, xs)
    mesh_data["totalGenerations"] = generations
    mesh_data["totalHistories"] = histories
    mesh_data["skipGenerations"] = min(mesh_data["skipGenerations"],
                                       mesh_data["totalGenerations"] - 1)

    results = mc.SimulateParticlesAndCalculateParametersOfInterest(
        mesh_data, seed=seed, engine=engine
    )
    return mesh_data, results


def ComputePowerNormalization(md: dict, res: dict) -> float:
    """Return C such that phi_physical = C * phi_MC  [n/cm^2/s]."""
    sig_f = md["NXS_SigF"]            # (n_groups, n_meshes)
    phi_raw = res["averageFlux"]       # (n_groups, n_meshes)
    dx = md["deltaXArray"]

    # Raw 1D fission rate (per source neutron, per unit area)
    F_1D = float(np.sum(sig_f * phi_raw * dx[None, :]))

    L_ass = md["domainWidth"] / 2.0    # single assembly width
    D_eff = N_ASSEMBLIES * L_ass**2 / md["domainWidth"]

    C = P_REACTOR / (E_FISSION * F_1D * D_eff * H_ACTIVE)
    return C


def PlotFlux(plt, all_results: dict, energy_groups: int, out_dir: Path):
    paths = []
    for cfg, (md, res) in sorted(all_results.items()):
        fig, ax = plt.subplots(figsize=(10, 4))
        C = ComputePowerNormalization(md, res)
        x = md["xCenter"]
        for g in range(energy_groups):
            phi = C * res["averageFlux"][g]
            ax.plot(x, phi, lw=1.0, label=f"Group {g + 1}")
        ax.set_xlabel("x (cm)")
        ax.set_ylabel(r"Flux (n/cm$^2$/s)")
        ax.set_title(f"Cell-center flux — {CONFIG_NAMES.get(cfg, f'Config {cfg}')}")
        ax.legend(fontsize=9, ncols=2 if energy_groups > 4 else 1)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        p = out_dir / f"flux_config{cfg}_all_groups.png"
        fig.savefig(p, dpi=150)
        plt.close(fig)
        paths.append(p)
    return paths


def PlotRawFlux(plt, all_results: dict, energy_groups: int, out_dir: Path):
    paths = []
    for cfg, (md, res) in sorted(all_results.items()):
        fig, ax = plt.subplots(figsize=(10, 4))
        x = md["xCenter"]
        for g in range(energy_groups):
            ax.plot(x, res["averageFlux"][g], lw=1.0, label=f"Group {g + 1}")
        ax.set_xlabel("x (cm)")
        ax.set_ylabel("Raw MC flux")
        ax.set_title(f"Raw cell-center flux — {CONFIG_NAMES.get(cfg, f'Config {cfg}')}")
        ax.legend(fontsize=9, ncols=2 if energy_groups > 4 else 1)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        p = out_dir / f"raw_flux_config{cfg}_all_groups.png"
        fig.savefig(p, dpi=150)
        plt.close(fig)
        paths.append(p)
    return paths


def PlotNormalizedFlux(plt, all_results: dict, energy_groups: int, out_dir: Path):
    paths = []
    for cfg, (md, res) in sorted(all_results.items()):
        fig, ax = plt.subplots(figsize=(10, 4))
        x = md["xCenter"]
        for g in range(energy_groups):
            phi = res["averageFlux"][g]
            peak = np.max(phi)
            phi_norm = phi / peak if peak > 0.0 else phi
            ax.plot(x, phi_norm, lw=1.0, label=f"Group {g + 1}")
        ax.set_xlabel("x (cm)")
        ax.set_ylabel("Normalized flux")
        ax.set_title(f"Normalized raw MC flux — {CONFIG_NAMES.get(cfg, f'Config {cfg}')}")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=9, ncols=2 if energy_groups > 4 else 1)
        fig.tight_layout()
        p = out_dir / f"normalized_raw_flux_config{cfg}_all_groups.png"
        fig.savefig(p, dpi=150)
        plt.close(fig)
        paths.append(p)
    return paths


def PlotFluxAll(plt, all_results: dict, energy_groups: int, out_dir: Path):
    fig, axes = plt.subplots(energy_groups, 1, figsize=(10, 2.5 * energy_groups),
                             sharex=True, squeeze=False)
    for g in range(energy_groups):
        ax = axes[g, 0]
        for cfg, (md, res) in sorted(all_results.items()):
            C = ComputePowerNormalization(md, res)
            x = md["xCenter"]
            phi = C * res["averageFlux"][g]
            ax.plot(x, phi, lw=1.0, label=CONFIG_NAMES.get(cfg, f"Config {cfg}"))
        ax.set_ylabel(f"Group {g}")
        ax.legend(fontsize=7)
        ax.grid(True, alpha=0.3)
    axes[-1, 0].set_xlabel("x (cm)")
    fig.supylabel(r"Flux (n/cm$^2$/s)", fontsize=11)
    fig.suptitle("Cell-center flux by configuration", fontsize=11)
    fig.tight_layout()
    p = out_dir / "flux_all_groups.png"
    fig.savefig(p, dpi=150)
    plt.close(fig)
    return p


def PlotCurrent(plt, all_results: dict, energy_groups: int, out_dir: Path):
    paths = []
    for g in range(energy_groups):
        fig, ax = plt.subplots(figsize=(10, 4))
        for cfg, (md, res) in sorted(all_results.items()):
            C = ComputePowerNormalization(md, res)
            x_left = md["xLeft"]
            x_right = md["xRight"]
            x_edges = np.concatenate(([x_left[0]], x_right))
            current = C * res["averageCurrent"][g].copy()
            current[0] = 0.0
            current[-1] = 0.0
            ax.plot(x_edges, current, lw=1.0,
                    label=CONFIG_NAMES.get(cfg, f"Config {cfg}"))
        ax.set_xlabel("x (cm)")
        ax.set_ylabel(r"Current (n/cm$^2$/s)")
        ax.set_title(f"Edge current — Group {g}")
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        p = out_dir / f"current_group{g}.png"
        fig.savefig(p, dpi=150)
        plt.close(fig)
        paths.append(p)
    return paths


def PlotCurrentAll(plt, all_results: dict, energy_groups: int, out_dir: Path):
    fig, axes = plt.subplots(energy_groups, 1, figsize=(10, 2.5 * energy_groups),
                             sharex=True, squeeze=False)
    for g in range(energy_groups):
        ax = axes[g, 0]
        for cfg, (md, res) in sorted(all_results.items()):
            C = ComputePowerNormalization(md, res)
            x_left = md["xLeft"]
            x_right = md["xRight"]
            x_edges = np.concatenate(([x_left[0]], x_right))
            current = C * res["averageCurrent"][g].copy()
            current[0] = 0.0
            current[-1] = 0.0
            ax.plot(x_edges, current, lw=1.0,
                    label=CONFIG_NAMES.get(cfg, f"Config {cfg}"))
        ax.set_ylabel(f"Group {g}")
        ax.legend(fontsize=7)
        ax.grid(True, alpha=0.3)
    axes[-1, 0].set_xlabel("x (cm)")
    fig.supylabel(r"Current (n/cm$^2$/s)", fontsize=11)
    fig.suptitle("Edge current by configuration", fontsize=11)
    fig.tight_layout()
    p = out_dir / "current_all_groups.png"
    fig.savefig(p, dpi=150)
    plt.close(fig)
    return p


def PrintSummaryTable(all_results: dict):
    print()
    print(f"{'Config':>12s}  {'k_eff':>10s}  {'Std err':>10s}  {'C (n/s)':>12s}  {'Peak flux':>12s}")
    print("-" * 62)
    for cfg in sorted(all_results):
        md, res = all_results[cfg]
        C = ComputePowerNormalization(md, res)
        peak = float(np.max(C * res["averageFlux"]))
        name = CONFIG_NAMES.get(cfg, f"Config {cfg}")
        print(f"{name:>12s}  {res['kEffective']:10.5f}  {res['kEffectiveStdErr']:10.5f}  {C:12.4e}  {peak:12.4e}")
    print()
    print(f"  Assumptions: P = {P_REACTOR/1e6:.0f} MW_th,  E_f = 200 MeV/fission,")
    print(f"               H_active = {H_ACTIVE:.2f} cm,  N_assemblies = {N_ASSEMBLIES}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Run all configs and plot flux / current / k_eff.")
    parser.add_argument("--energy-groups", type=int, default=7)
    parser.add_argument("--generations", type=int, default=100)
    parser.add_argument("--histories", type=int, default=1000)
    parser.add_argument("--skip", type=int, default=10)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--engine", choices=("python", "numba"), default="numba")
    parser.add_argument("--output-dir", type=str, default=str(RESULTS_DIR / "monte_carlo"))
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    if not out_dir.is_absolute():
        out_dir = RESULTS_DIR / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    mc = LoadMCModule()

    base = LoadJson(args.energy_groups)
    n_configs = int(base.get("Configs", 3))
    configs = list(range(n_configs))

    all_results: dict[int, tuple] = {}
    for cfg in configs:
        print(f"Running config {cfg} ({CONFIG_NAMES.get(cfg, '?')}) ...",
              file=sys.stderr)
        md, res = RunConfig(mc, base, cfg,
                             generations=args.generations,
                             histories=args.histories,
                             skip=args.skip,
                             seed=args.seed,
                             engine=args.engine)
        all_results[cfg] = (md, res)

    PrintSummaryTable(all_results)

    figures = []
    figures.extend(PlotFlux(plt, all_results, args.energy_groups, out_dir))
    figures.extend(PlotRawFlux(plt, all_results, args.energy_groups, out_dir))
    figures.extend(PlotNormalizedFlux(plt, all_results, args.energy_groups, out_dir))
    figures.extend(PlotCurrent(plt, all_results, args.energy_groups, out_dir))
    figures.append(PlotCurrentAll(plt, all_results, args.energy_groups, out_dir))

    for p in figures:
        print(p)


if __name__ == "__main__":
    main()
