from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from fission1d.finite_diff import (
    BuildCrossSections,
    CreateMesh,
    LoadInputData,
    PowerIteration,
)
from fission1d.paths import RESULTS_DIR
CONFIG_NAMES = {0: "UO2-UO2", 1: "MOX-MOX", 2: "UO2-MOX"}

# Power normalization constants match plot_project_run.py.
P_REACTOR = 3565e6
E_FISSION = 200 * 1.602e-13
H_ACTIVE = 365.76
N_ASSEMBLIES = 193


def RunConfig(energy_groups: int, case: int, config: int, mesh_refinement: int):
    input_data = LoadInputData(energy_groups, case, config)
    xs = BuildCrossSections(input_data)
    mesh = CreateMesh(input_data, xs, mesh_refinement=mesh_refinement)
    phi, k, k_history = PowerIteration(mesh)
    return input_data, xs, mesh, phi, k, k_history


def ComputePowerNormalization(input_data: dict, xs: dict, mesh: dict, phi: np.ndarray) -> float:
    sig_f = xs["SigF"][:, mesh["mat_id"]]
    dx = mesh["dx"]
    fission_rate_1d = float(np.sum(sig_f * phi * dx))

    domain_width = mesh["N"] * dx
    assembly_width = float(input_data.get("AssemblyWidth", domain_width / 2.0))
    d_eff = N_ASSEMBLIES * assembly_width**2 / domain_width

    return P_REACTOR / (E_FISSION * fission_rate_1d * d_eff * H_ACTIVE)


def PlotFluxByConfig(all_results: dict, energy_groups: int, out_dir: Path):
    paths = []
    for cfg, (input_data, xs, mesh, phi, k, _) in sorted(all_results.items()):
        c_norm = ComputePowerNormalization(input_data, xs, mesh, phi)
        x = mesh["x_center"]

        fig, ax = plt.subplots(figsize=(10, 4))
        for g in range(energy_groups):
            ax.plot(x, c_norm * phi[g], lw=1.0, label=f"Group {g + 1}")

        ax.set_xlabel("x (cm)")
        ax.set_ylabel(r"Flux (n/cm$^2$/s)")
        ax.set_title(f"Finite difference flux - {CONFIG_NAMES.get(cfg, f'Config {cfg}')} (k = {k:.5f})")
        ax.legend(fontsize=9, ncols=2 if energy_groups > 4 else 1)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()

        path = out_dir / f"fd_flux_config{cfg}_all_groups.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        paths.append(path)
    return paths


def ComputeKConvergence(k_history: np.ndarray) -> float:
    if len(k_history) < 2:
        return float("nan")
    k_old = k_history[-2]
    return float(abs((k_history[-1] - k_old) / k_old)) if k_old != 0.0 else float(abs(k_history[-1] - k_old))


def PrintSummaryTable(all_results: dict):
    print()
    print(f"{'Configuration':<13s}  {'k_eff':>10s}  {'d_k':>12s}  {'d_flux':>12s}  {'C (n/s)':>12s}  {'Peak flux (n/cm2/s)':>21s}")
    print("-" * 92)

    for cfg, (input_data, xs, mesh, phi, k, k_history) in sorted(all_results.items()):
        c_norm = ComputePowerNormalization(input_data, xs, mesh, phi)
        dk = ComputeKConvergence(k_history)
        d_flux = mesh.get("last_d_flux", float("nan"))
        peak_flux = float(np.max(c_norm * phi))
        name = CONFIG_NAMES.get(cfg, f"Config {cfg}")
        print(f"{name:<13s}  {k:10.5f}  {dk:12.2E}  {d_flux:12.2E}  {c_norm:12.2E}  {peak_flux:21.2E}")

    print()
    print(f"Assumptions: P = {P_REACTOR / 1e6:.0f} MW_th, E_f = 200 MeV/fission,")
    print(f"             H_active = {H_ACTIVE:.2f} cm, N_assemblies = {N_ASSEMBLIES}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Run all finite-difference configs and plot all energy groups."
    )
    parser.add_argument("--energy-groups", type=int, default=7, choices=[2, 7])
    parser.add_argument("--case", type=int, default=0)
    parser.add_argument("--mesh-refinement", type=int, default=1)
    parser.add_argument("--output-dir", type=str, default=str(RESULTS_DIR / "finite_diff"))
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    if not out_dir.is_absolute():
        out_dir = RESULTS_DIR / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    base = LoadInputData(args.energy_groups, args.case, 0)
    configs = list(range(int(base.get("Configs", 3))))

    all_results = {}
    for cfg in configs:
        print(f"Running config {cfg} ({CONFIG_NAMES.get(cfg, '?')}) ...")
        all_results[cfg] = RunConfig(
            args.energy_groups,
            args.case,
            cfg,
            args.mesh_refinement,
        )

    PrintSummaryTable(all_results)

    for path in PlotFluxByConfig(all_results, args.energy_groups, out_dir):
        print(path)


if __name__ == "__main__":
    main()
