from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from fission1d.paths import RESULTS_DIR

import argparse
import os
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


CONFIGS = {
    "UO2-MOX": (0, 1),
    "MOX-UO2": (1, 0),
}
MATERIAL_NAMES = {0: "UO2", 1: "MOX", 2: "H2O", 3: "CTR"}

P_REACTOR = 3565e6
E_FISSION = 200 * 1.602e-13
H_ACTIVE = 365.76
N_ASSEMBLIES = 193


def LoadMCModule():
    from fission1d import monte_carlo as mod
    return mod


def AssemblyRow(fuel_material: int, num_rods: int) -> list[int]:
    row = []
    for _ in range(num_rods):
        row.extend([2, fuel_material])
    row.append(2)
    return row


def WaterAssemblyRow(num_rods: int) -> list[int]:
    return [2] * (2 * num_rods + 1)


def AddControlRods(row: list[int], positions: tuple[int, ...] = (3, 15)) -> list[int]:
    controlled = list(row)
    for rod_position in positions:
        controlled[2 * rod_position - 1] = 3
    return controlled


def BuildCaseInput(
    assembly_fuels: tuple[int, int],
    *,
    right_boundary: float,
    add_reflector: bool = False,
    control_rods_left: bool = False,
    generations: int = 100,
    histories: int = 1000,
    skip: int = 10,
) -> dict:
    data = LoadInputData(2, test_case=0, config=0)
    data = dict(data)
    num_rods = int(data["NumRods"])

    rows = [AssemblyRow(assembly_fuels[0], num_rods), AssemblyRow(assembly_fuels[1], num_rods)]
    if control_rods_left:
        rows[0] = AddControlRods(rows[0])
    if add_reflector:
        rows.append(WaterAssemblyRow(num_rods))

    data["NumAss"] = len(rows)
    data["Config"] = 0
    data["Configs"] = 1
    data["Generations"] = generations
    data["Histories"] = histories
    data["Skip"] = min(skip, max(0, generations - 1))
    data["BoundL"] = [1.0, 1.0]
    data["BoundR"] = [right_boundary, right_boundary]
    data["ConfigSets"] = {"0": {"MatID": rows}}
    return data


def RunFD(input_data: dict, mesh_refinement: int):
    xs = BuildCrossSections(input_data)
    mesh = CreateMesh(input_data, xs, mesh_refinement=mesh_refinement)
    phi, k, k_history = PowerIteration(mesh)
    return xs, mesh, phi, k, k_history


def RunMC(mc, input_data: dict, seed: int, engine: str):
    xs = mc.BuildCrossSectionTables(input_data)
    mesh_data = mc.CreateMeshAndAssignData(input_data, xs)
    mesh_data["totalGenerations"] = input_data["Generations"]
    mesh_data["totalHistories"] = input_data["Histories"]
    mesh_data["skipGenerations"] = input_data["Skip"]
    results = mc.SimulateParticlesAndCalculateParametersOfInterest(
        mesh_data,
        seed=seed,
        engine=engine,
    )
    return mesh_data, results


def ComputeFDPowerNormalization(input_data: dict, xs: dict, mesh: dict, phi: np.ndarray) -> float:
    sig_f = xs["SigF"][:, mesh["mat_id"]]
    fission_rate_1d = float(np.sum(sig_f * phi * mesh["dx"]))
    assembly_width = float(input_data["AssemblyWidth"])
    domain_width = mesh["N"] * mesh["dx"]
    d_eff = N_ASSEMBLIES * assembly_width**2 / domain_width
    return P_REACTOR / (E_FISSION * fission_rate_1d * d_eff * H_ACTIVE)


def ComputeMCPowerNormalization(input_data: dict, mesh_data: dict, results: dict) -> float:
    sig_f = mesh_data["NXS_SigF"]
    phi = results["averageFlux"]
    dx = mesh_data["deltaXArray"]
    fission_rate_1d = float(np.sum(sig_f * phi * dx[None, :]))
    assembly_width = float(input_data["AssemblyWidth"])
    d_eff = N_ASSEMBLIES * assembly_width**2 / mesh_data["domainWidth"]
    return P_REACTOR / (E_FISSION * fission_rate_1d * d_eff * H_ACTIVE)


def RelativeKChange(k_new: float, k_old: float) -> float:
    return float((k_new - k_old) / k_old) if k_old != 0.0 else float("nan")


def ReactivityWorthPcm(k_with: float, k_without: float) -> float:
    rho_with = (k_with - 1.0) / k_with
    rho_without = (k_without - 1.0) / k_without
    return float((rho_with - rho_without) * 1.0e5)


def PlotFDComparison(title: str, cases: dict, out_path: Path):
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=False)
    for label, (input_data, xs, mesh, phi, k, _) in cases.items():
        c_norm = ComputeFDPowerNormalization(input_data, xs, mesh, phi)
        for g, ax in enumerate(axes):
            ax.plot(mesh["x_center"], c_norm * phi[g], lw=1.1, label=f"{label} (k={k:.5f})")
            ax.set_ylabel(f"Group {g + 1} flux")
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=8)
    axes[-1].set_xlabel("x (cm)")
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def PlotMCComparison(title: str, cases: dict, out_path: Path):
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=False)
    for label, (input_data, mesh_data, results) in cases.items():
        c_norm = ComputeMCPowerNormalization(input_data, mesh_data, results)
        for g, ax in enumerate(axes):
            ax.plot(
                mesh_data["xCenter"],
                c_norm * results["averageFlux"][g],
                lw=1.0,
                label=f"{label} (k={results['kEffective']:.5f})",
            )
            ax.set_ylabel(f"Group {g + 1} flux")
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=8)
    axes[-1].set_xlabel("x (cm)")
    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def PrintReflectorTable(fd_results: dict, mc_results: dict):
    print("\nReflector comparison")
    print(
        f"{'Method':<6s}  {'Config':<8s}  {'k vacuum':>10s}  {'k reflector':>12s}  "
        f"{'Delta k/k':>11s}  {'Worth (pcm)':>12s}"
    )
    print("-" * 70)
    for config_name in CONFIGS:
        fd_vac = fd_results[(config_name, "vacuum")][4]
        fd_ref = fd_results[(config_name, "reflector")][4]
        print(
            f"{'FD':<6s}  {config_name:<8s}  {fd_vac:10.5f}  {fd_ref:12.5f}  "
            f"{RelativeKChange(fd_ref, fd_vac):11.3e}  {ReactivityWorthPcm(fd_ref, fd_vac):12.2f}"
        )
        mc_vac = mc_results[(config_name, "vacuum")][2]["kEffective"]
        mc_ref = mc_results[(config_name, "reflector")][2]["kEffective"]
        print(
            f"{'MC':<6s}  {config_name:<8s}  {mc_vac:10.5f}  {mc_ref:12.5f}  "
            f"{RelativeKChange(mc_ref, mc_vac):11.3e}  {ReactivityWorthPcm(mc_ref, mc_vac):12.2f}"
        )


def PrintControlRodTable(fd_results: dict, mc_results: dict):
    print("\nControl rod comparison")
    print(
        f"{'Method':<6s}  {'Config':<8s}  {'k base':>10s}  {'k rods':>10s}  "
        f"{'Delta k/k':>11s}  {'Worth (pcm)':>12s}"
    )
    print("-" * 66)
    for config_name in CONFIGS:
        fd_base = fd_results[(config_name, "base")][4]
        fd_rods = fd_results[(config_name, "control_rods")][4]
        print(
            f"{'FD':<6s}  {config_name:<8s}  {fd_base:10.5f}  {fd_rods:10.5f}  "
            f"{RelativeKChange(fd_rods, fd_base):11.3e}  {ReactivityWorthPcm(fd_rods, fd_base):12.2f}"
        )
        mc_base = mc_results[(config_name, "base")][2]["kEffective"]
        mc_rods = mc_results[(config_name, "control_rods")][2]["kEffective"]
        print(
            f"{'MC':<6s}  {config_name:<8s}  {mc_base:10.5f}  {mc_rods:10.5f}  "
            f"{RelativeKChange(mc_rods, mc_base):11.3e}  {ReactivityWorthPcm(mc_rods, mc_base):12.2f}"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--generations", type=int, default=100)
    parser.add_argument("--histories", type=int, default=1000)
    parser.add_argument("--skip", type=int, default=10)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--engine", choices=("python", "numba"), default="numba")
    parser.add_argument("--mesh-refinement", type=int, default=1)
    parser.add_argument("--output-dir", type=str, default=str(RESULTS_DIR / "extracredit"))
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    if not out_dir.is_absolute():
        out_dir = RESULTS_DIR / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    mc = LoadMCModule()
    fd_reflector_results = {}
    mc_reflector_results = {}
    fd_control_results = {}
    mc_control_results = {}

    run_index = 0
    for config_name, fuels in CONFIGS.items():
        reflector_inputs = {
            "vacuum": BuildCaseInput(
                fuels,
                right_boundary=0.0,
                add_reflector=False,
                generations=args.generations,
                histories=args.histories,
                skip=args.skip,
            ),
            "reflector": BuildCaseInput(
                fuels,
                right_boundary=0.0,
                add_reflector=True,
                generations=args.generations,
                histories=args.histories,
                skip=args.skip,
            ),
        }
        fd_plot_cases = {}
        mc_plot_cases = {}
        for case_name, input_data in reflector_inputs.items():
            print(f"Running reflector {case_name}: {config_name} FD ...")
            fd_result = (input_data, *RunFD(input_data, args.mesh_refinement))
            fd_reflector_results[(config_name, case_name)] = fd_result
            fd_plot_cases[case_name] = fd_result

            print(f"Running reflector {case_name}: {config_name} MC ...")
            mc_result = (input_data, *RunMC(mc, input_data, args.seed + run_index, args.engine))
            mc_reflector_results[(config_name, case_name)] = mc_result
            mc_plot_cases[case_name] = mc_result
            run_index += 1

        PlotFDComparison(
            f"FD reflector comparison - {config_name}",
            fd_plot_cases,
            out_dir / f"fd_reflector_{config_name}.png",
        )
        PlotMCComparison(
            f"MC reflector comparison - {config_name}",
            mc_plot_cases,
            out_dir / f"mc_reflector_{config_name}.png",
        )

        control_inputs = {
            "base": BuildCaseInput(
                fuels,
                right_boundary=1.0,
                add_reflector=False,
                control_rods_left=False,
                generations=args.generations,
                histories=args.histories,
                skip=args.skip,
            ),
            "control_rods": BuildCaseInput(
                fuels,
                right_boundary=1.0,
                add_reflector=False,
                control_rods_left=True,
                generations=args.generations,
                histories=args.histories,
                skip=args.skip,
            ),
        }
        fd_plot_cases = {}
        mc_plot_cases = {}
        for case_name, input_data in control_inputs.items():
            print(f"Running control rod {case_name}: {config_name} FD ...")
            fd_result = (input_data, *RunFD(input_data, args.mesh_refinement))
            fd_control_results[(config_name, case_name)] = fd_result
            fd_plot_cases[case_name] = fd_result

            print(f"Running control rod {case_name}: {config_name} MC ...")
            mc_result = (input_data, *RunMC(mc, input_data, args.seed + run_index, args.engine))
            mc_control_results[(config_name, case_name)] = mc_result
            mc_plot_cases[case_name] = mc_result
            run_index += 1

        PlotFDComparison(
            f"FD control rod comparison - {config_name}",
            fd_plot_cases,
            out_dir / f"fd_control_rods_{config_name}.png",
        )
        PlotMCComparison(
            f"MC control rod comparison - {config_name}",
            mc_plot_cases,
            out_dir / f"mc_control_rods_{config_name}.png",
        )

    PrintReflectorTable(fd_reflector_results, mc_reflector_results)
    PrintControlRodTable(fd_control_results, mc_control_results)

    print(f"\nPlots saved to: {out_dir}")


if __name__ == "__main__":
    main()
