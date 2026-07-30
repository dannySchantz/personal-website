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


CONFIG_NAMES = {0: "UO2-UO2", 1: "MOX-MOX", 2: "UO2-MOX"}
ENERGY_BINS_EV = np.array([
    1.0e-5,
    5.179474679231213e-4,
    2.6826957952797246e-2,
    1.389495494373136,
    71.96856730011514,
    3727.593720314938,
    193069.77288832457,
    1.0e7,
])

P_REACTOR = 3565e6
E_FISSION = 200 * 1.602e-13
H_ACTIVE = 365.76
N_ASSEMBLIES = 193


def LoadMCModule():
    from fission1d import monte_carlo as mod
    return mod


def RunSevenGroupReference(config: int, case: int, mesh_refinement: int):
    input_data = LoadInputData(7, case, config)
    xs = BuildCrossSections(input_data)
    mesh = CreateMesh(input_data, xs, mesh_refinement=mesh_refinement)
    phi, k, k_history = PowerIteration(mesh)
    return input_data, xs, mesh, phi, k, k_history


def WeightedAverage(values: np.ndarray, weights: np.ndarray) -> float:
    total_weight = float(np.sum(weights))
    if total_weight <= 0.0:
        return 0.0
    return float(np.sum(values * weights) / total_weight)


def BuildCollapseFractions(split_group: int, cutoff_energy: float | None):
    fractions = np.zeros((2, 7))

    if cutoff_energy is None:
        fractions[0, :split_group] = 1.0
        fractions[1, split_group:] = 1.0
        return fractions

    for g in range(7):
        e_low = ENERGY_BINS_EV[g]
        e_high = ENERGY_BINS_EV[g + 1]

        if e_high <= cutoff_energy:
            fractions[0, g] = 1.0
        elif e_low >= cutoff_energy:
            fractions[1, g] = 1.0
        else:
            thermal_fraction = np.log(cutoff_energy / e_low) / np.log(e_high / e_low)
            fractions[0, g] = thermal_fraction
            fractions[1, g] = 1.0 - thermal_fraction

    return fractions


def CollapseAndHomogenize(input_data: dict, xs: dict, mesh: dict, phi7: np.ndarray, split_group: int, cutoff_energy: float | None):
    num_assemblies = int(input_data["NumAss"])
    assembly_width = float(input_data["AssemblyWidth"])
    dx = mesh["dx"]
    fractions = BuildCollapseFractions(split_group, cutoff_energy)

    collapsed = {
        "D": np.zeros((2, num_assemblies)),
        "SigA": np.zeros((2, num_assemblies)),
        "SigF": np.zeros((2, num_assemblies)),
        "SigIS": np.zeros((2, num_assemblies)),
        "nuSigF": np.zeros((2, num_assemblies)),
        "SigDS": np.zeros((2, num_assemblies)),
        "Chi": np.zeros((2, num_assemblies)),
    }

    sig_is = xs["SigIS"][:, mesh["mat_id"]]
    sig_ds = mesh["SigDS"]
    sig_f = xs["SigF"][:, mesh["mat_id"]]
    nu_sig_f = xs["nuT"][:, mesh["mat_id"]] * sig_f
    fission_source = np.sum(nu_sig_f * phi7, axis=0)

    for assembly in range(num_assemblies):
        in_assembly = (
            (mesh["x_center"] >= assembly * assembly_width)
            & (mesh["x_center"] < (assembly + 1) * assembly_width)
        )

        for coarse_g in range(2):
            group_fraction = fractions[coarse_g, :, None]
            flux_weights = phi7[:, in_assembly] * dx * group_fraction
            collapsed["D"][coarse_g, assembly] = WeightedAverage(
                mesh["D"][:, in_assembly],
                flux_weights,
            )
            collapsed["SigA"][coarse_g, assembly] = WeightedAverage(
                xs["SigA"][:, mesh["mat_id"]][:, in_assembly],
                flux_weights,
            )
            collapsed["SigF"][coarse_g, assembly] = WeightedAverage(
                sig_f[:, in_assembly],
                flux_weights,
            )
            collapsed["nuSigF"][coarse_g, assembly] = WeightedAverage(
                nu_sig_f[:, in_assembly],
                flux_weights,
            )

            production_weights = fission_source[in_assembly] * dx
            total_production = float(np.sum(production_weights))
            if total_production > 0.0:
                collapsed["Chi"][coarse_g, assembly] = float(
                    np.sum(
                        xs["ChiT"][:, mesh["mat_id"]][:, in_assembly]
                        * group_fraction
                        * production_weights[None, :]
                    )
                    / total_production
                )

        coarse_flux_weights = [
            phi7[:, in_assembly] * dx * fractions[coarse_g, :, None]
            for coarse_g in range(2)
        ]

        for coarse_g in range(2):
            scatter_numerator = float(np.sum(sig_is[:, in_assembly] * coarse_flux_weights[coarse_g]))
            for fine_g in range(6):
                scatter_numerator += float(np.sum(sig_ds[fine_g, in_assembly] * phi7[fine_g, in_assembly] * dx * fractions[coarse_g, fine_g]* fractions[coarse_g, fine_g + 1]))
            scatter_denominator = float(np.sum(coarse_flux_weights[coarse_g]))
            if scatter_denominator > 0.0:
                collapsed["SigIS"][coarse_g, assembly] = scatter_numerator / scatter_denominator

        downscatter_numerator = 0.0
        for fine_g in range(6):
            downscatter_numerator += float(np.sum(sig_ds[fine_g, in_assembly] * phi7[fine_g, in_assembly] * dx * fractions[0, fine_g] * fractions[1, fine_g + 1]))
        downscatter_denominator = float(np.sum(coarse_flux_weights[0]))

        if downscatter_denominator > 0.0:
            collapsed["SigDS"][0, assembly] = downscatter_numerator / downscatter_denominator
        collapsed["SigDS"][1, assembly] = 0.0

        chi_sum = np.sum(collapsed["Chi"][:, assembly])
        if chi_sum > 0.0:
            collapsed["Chi"][:, assembly] /= chi_sum

    return collapsed


def CreateCollapsedAssemblyMesh(input_data: dict, collapsed: dict, cells_per_assembly: int):
    num_ass = int(input_data["NumAss"])
    assembly_width = float(input_data["AssemblyWidth"])
    dx = assembly_width / cells_per_assembly
    n_cells = num_ass * cells_per_assembly
    x_center = (np.arange(n_cells, dtype=float) + 0.5) * dx
    assembly_id = np.repeat(np.arange(num_ass), cells_per_assembly)

    sig_ds = collapsed["SigDS"][:, assembly_id]
    sig_a = collapsed["SigA"][:, assembly_id]

    return {
        "G": 2,
        "N": n_cells,
        "dx": dx,
        "x_center": x_center,
        "mat_id": assembly_id,
        "D": collapsed["D"][:, assembly_id],
        "SigR": sig_a + sig_ds,
        "nuSigF": collapsed["nuSigF"][:, assembly_id],
        "Chi": collapsed["Chi"][:, assembly_id],
        "SigDS": sig_ds,
        "SigF": collapsed["SigF"][:, assembly_id],
        "BoundL": np.ones(2),
        "BoundR": np.ones(2),
    }


def BuildCollapsedMCInput(input_data: dict, collapsed: dict, generations: int,
                          histories: int, skip: int):
    num_ass = int(input_data["NumAss"])
    config_rows = []
    for ass in range(num_ass):
        config_rows.append([ass] * (2 * int(input_data["NumRods"]) + 1))

    xs_data = {}
    for name in ["SigTR", "SigIS", "SigDS", "SigA", "SigF", "nuT", "ChiT"]:
        xs_data[name] = {}
        for mat in range(num_ass):
            xs_data[name][str(mat)] = {}
            for g in range(2):
                if name == "SigTR":
                    value = 1.0 / (3.0 * collapsed["D"][g, mat])
                elif name == "nuT":
                    sig_f = collapsed["SigF"][g, mat]
                    value = collapsed["nuSigF"][g, mat] / sig_f if sig_f > 0.0 else 0.0
                elif name == "ChiT":
                    value = collapsed["Chi"][g, mat]
                else:
                    value = collapsed[name][g, mat]
                xs_data[name][str(mat)][str(g)] = float(value)

    return {
        "Solution": 1,
        "TestCase": 0,
        "Config": 0,
        "Analk": 1,
        "Cases": 1,
        "Configs": 1,
        "MatTypes": num_ass,
        "EnergyGroups": 2,
        "solver": 0,
        "Generations": generations,
        "Histories": histories,
        "Skip": min(skip, max(0, generations - 1)),
        "NumAss": num_ass,
        "NumRods": int(input_data["NumRods"]),
        "RodDia": float(input_data["RodDia"]),
        "RodPitch": float(input_data["RodPitch"]),
        "AssemblyWidth": float(input_data["AssemblyWidth"]),
        "MPFR": int(input_data["MPFR"]),
        "MPWR": int(input_data["MPWR"]),
        "BoundL": [1.0, 1.0],
        "BoundR": [1.0, 1.0],
        "XSData": {"0": xs_data},
        "ConfigSets": {"0": {"MatID": config_rows}},
    }


def RefineCollapsedFDMesh(input_data: dict, mesh: dict, mesh_refinement: int):
    if mesh_refinement <= 1:
        return mesh

    refined = dict(mesh)
    base_dx = mesh["dx"]
    refined["dx"] = base_dx / mesh_refinement
    refined["N"] = mesh["N"] * mesh_refinement
    refined["x_center"] = (np.arange(refined["N"], dtype=float) + 0.5) * refined["dx"]
    refined["mat_id"] = np.repeat(mesh["mat_id"], mesh_refinement)

    for name in ["D", "SigR", "nuSigF", "Chi", "SigDS", "SigF"]:
        refined[name] = np.repeat(mesh[name], mesh_refinement, axis=1)

    return refined


def RunCollapsedMC(mc, input_data: dict, collapsed: dict, generations: int,
                   histories: int, skip: int, seed: int, engine: str):
    mc_input = BuildCollapsedMCInput(input_data, collapsed, generations, histories, skip)
    xs_tables = mc.BuildCrossSectionTables(mc_input)
    mesh_data = mc.CreateMeshAndAssignData(mc_input, xs_tables)
    mesh_data["totalGenerations"] = generations
    mesh_data["totalHistories"] = histories
    mesh_data["skipGenerations"] = min(skip, max(0, generations - 1))
    results = mc.SimulateParticlesAndCalculateParametersOfInterest(
        mesh_data,
        seed=seed,
        engine=engine,
    )
    return mc_input, mesh_data, results


def ComputeFDPowerNormalization(input_data: dict, mesh: dict, phi: np.ndarray) -> float:
    fission_rate_1d = float(np.sum(mesh["SigF"] * phi * mesh["dx"]))
    domain_width = mesh["N"] * mesh["dx"]
    assembly_width = float(input_data["AssemblyWidth"])
    d_eff = N_ASSEMBLIES * assembly_width**2 / domain_width
    return P_REACTOR / (E_FISSION * fission_rate_1d * d_eff * H_ACTIVE)


def ComputeMCPowerNormalization(mesh_data: dict, results: dict) -> float:
    sig_f = mesh_data["NXS_SigF"]
    phi = results["averageFlux"]
    dx = mesh_data["deltaXArray"]
    fission_rate_1d = float(np.sum(sig_f * phi * dx[None, :]))
    assembly_width = mesh_data["domainWidth"] / int(mesh_data.get("numAss", 2))
    d_eff = N_ASSEMBLIES * assembly_width**2 / mesh_data["domainWidth"]
    return P_REACTOR / (E_FISSION * fission_rate_1d * d_eff * H_ACTIVE)


def ComputeKConvergence(k_history: np.ndarray) -> float:
    if len(k_history) < 2:
        return float("nan")
    k_old = k_history[-2]
    return float(abs((k_history[-1] - k_old) / k_old)) if k_old != 0.0 else float(abs(k_history[-1] - k_old))


def PlotFluxByConfig(results: dict, out_dir: Path):
    paths = []
    for cfg, result in sorted(results.items()):
        input_data, _, mesh, phi, k, _ = result
        c_norm = ComputeFDPowerNormalization(input_data, mesh, phi)

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(mesh["x_center"], c_norm * phi[0], lw=1.2, label="Collapsed Group 1")
        ax.plot(mesh["x_center"], c_norm * phi[1], lw=1.2, label="Collapsed Group 2")
        ax.set_xlabel("x (cm)")
        ax.set_ylabel(r"Flux (n/cm$^2$/s)")
        ax.set_title(
            f"Collapsed/homogenized FD flux - {CONFIG_NAMES.get(cfg, f'Config {cfg}')} "
            f"(k = {k:.5f})"
        )
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=9)
        fig.tight_layout()

        path = out_dir / f"collapsed_fd_flux_config{cfg}_all_groups.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        paths.append(path)
    return paths


def PlotMCFluxByConfig(results: dict, out_dir: Path):
    paths = []
    for cfg, (_, mesh_data, mc_results) in sorted(results.items()):
        c_norm = ComputeMCPowerNormalization(mesh_data, mc_results)

        fig, ax = plt.subplots(figsize=(10, 4))
        for g in range(2):
            ax.plot(
                mesh_data["xCenter"],
                c_norm * mc_results["averageFlux"][g],
                lw=1.0,
                label=f"Collapsed Group {g + 1}",
            )
        ax.set_xlabel("x (cm)")
        ax.set_ylabel(r"Flux (n/cm$^2$/s)")
        ax.set_title(
            f"Collapsed/homogenized MC flux - {CONFIG_NAMES.get(cfg, f'Config {cfg}')} "
            f"(k = {mc_results['kEffective']:.5f})"
        )
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=9)
        fig.tight_layout()

        path = out_dir / f"collapsed_mc_flux_config{cfg}_all_groups.png"
        fig.savefig(path, dpi=150)
        plt.close(fig)
        paths.append(path)
    return paths


def PrintSummaryTable(results: dict):
    print()
    print("Collapsed finite-difference summary")
    print(f"{'Configuration':<13s}  {'k_eff':>10s}  {'d_k':>12s}  {'d_flux':>12s}  {'C (n/s)':>12s}  {'Peak flux (n/cm2/s)':>21s}")
    print("-" * 92)
    for cfg, result in sorted(results.items()):
        input_data, _, mesh, phi, k, k_history = result
        c_norm = ComputeFDPowerNormalization(input_data, mesh, phi)
        peak_flux = float(np.max(c_norm * phi))
        dk = ComputeKConvergence(k_history)
        d_flux = mesh.get("last_d_flux", float("nan"))
        print(
            f"{CONFIG_NAMES.get(cfg, f'Config {cfg}'):<13s}  {k:10.5f}  "
            f"{dk:12.2E}  {d_flux:12.2E}  {c_norm:12.2E}  {peak_flux:21.2E}"
        )
    print()


def PrintMCSummaryTable(results: dict):
    print()
    print("Collapsed Monte Carlo summary")
    print(f"{'Configuration':<13s}  {'k_eff':>10s}  {'Std err':>10s}  {'C (n/s)':>12s}  {'Peak flux (n/cm2/s)':>21s}")
    print("-" * 78)
    for cfg, (_, mesh_data, mc_results) in sorted(results.items()):
        c_norm = ComputeMCPowerNormalization(mesh_data, mc_results)
        peak_flux = float(np.max(c_norm * mc_results["averageFlux"]))
        print(
            f"{CONFIG_NAMES.get(cfg, f'Config {cfg}'):<13s}  "
            f"{mc_results['kEffective']:10.5f}  {mc_results['kEffectiveStdErr']:10.5f}  "
            f"{c_norm:12.2E}  {peak_flux:21.2E}"
        )
    print()


def PrintCollapsedCrossSections(results: dict):
    print("Collapsed assembly cross sections")
    print(
        f"{'Config':<10s}  {'Assembly':>8s}  {'Group':>5s}  {'D':>10s}  "
        f"{'SigA':>10s}  {'SigF':>10s}  {'nuSigF':>10s}  {'SigDS':>10s}  {'Chi':>10s}"
    )
    print("-" * 98)
    for cfg, (_, collapsed, _, _, _, _) in sorted(results.items()):
        for ass in range(collapsed["D"].shape[1]):
            for g in range(2):
                print(
                    f"{CONFIG_NAMES.get(cfg, f'Config {cfg}'):<10s}  {ass + 1:8d}  "
                    f"{g + 1:5d}  {collapsed['D'][g, ass]:10.4e}  "
                    f"{collapsed['SigA'][g, ass]:10.4e}  {collapsed['SigF'][g, ass]:10.4e}  "
                    f"{collapsed['nuSigF'][g, ass]:10.4e}  {collapsed['SigDS'][g, ass]:10.4e}  "
                    f"{collapsed['Chi'][g, ass]:10.4e}"
                )
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Collapse 7-group FD results to 2 groups and homogenize by assembly."
    )
    parser.add_argument("--case", type=int, default=0)
    parser.add_argument("--configs", type=int, nargs="+", default=[0, 1, 2])
    parser.add_argument("--mesh-refinement", type=int, default=1)
    parser.add_argument("--cells-per-assembly", type=int, default=80)
    parser.add_argument("--generations", type=int, default=100)
    parser.add_argument("--histories", type=int, default=1000)
    parser.add_argument("--skip", type=int, default=10)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--engine", choices=("python", "numba"), default="numba")
    parser.add_argument("--skip-mc", action="store_true")
    parser.add_argument("--split-group", type=int, default=3)
    parser.add_argument("--cutoff-energy", type=float, default=1)
    parser.add_argument("--output-dir", type=str, default=str(RESULTS_DIR / "collapsed"))
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    if not out_dir.is_absolute():
        out_dir = RESULTS_DIR / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    results = {}
    mc_results = {}
    mc = None if args.skip_mc else LoadMCModule()
    for cfg in args.configs:
        print(f"Running 7-group reference config {cfg} ({CONFIG_NAMES.get(cfg, '?')}) ...")
        input_data, xs, mesh7, phi7, _, _ = RunSevenGroupReference(
            cfg,
            args.case,
            1,
        )
        collapsed = CollapseAndHomogenize(
            input_data,
            xs,
            mesh7,
            phi7,
            args.split_group,
            args.cutoff_energy,
        )
        base_collapsed_mesh = CreateCollapsedAssemblyMesh(
            input_data,
            collapsed,
            args.cells_per_assembly,
        )
        collapsed_mesh = RefineCollapsedFDMesh(
            input_data,
            base_collapsed_mesh,
            args.mesh_refinement,
        )
        print(f"Running collapsed 2-group config {cfg} ({CONFIG_NAMES.get(cfg, '?')}) ...")
        phi2, k2, k2_history = PowerIteration(collapsed_mesh)
        results[cfg] = (input_data, collapsed, collapsed_mesh, phi2, k2, k2_history)
        if mc is not None:
            print(f"Running collapsed 2-group MC config {cfg} ({CONFIG_NAMES.get(cfg, '?')}) ...")
            mc_results[cfg] = RunCollapsedMC(
                mc,
                input_data,
                collapsed,
                args.generations,
                args.histories,
                args.skip,
                args.seed + cfg,
                args.engine,
            )

    PrintSummaryTable(results)
    if mc_results:
        PrintMCSummaryTable(mc_results)
    PrintCollapsedCrossSections(results)

    for path in PlotFluxByConfig(results, out_dir):
        print(path)
    for path in PlotMCFluxByConfig(mc_results, out_dir):
        print(path)


if __name__ == "__main__":
    main()
