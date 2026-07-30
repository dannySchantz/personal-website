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


def load_mc_module():
    from fission1d import monte_carlo as mod
    return mod


def LoadInputJson(energy_groups: int) -> dict:
    from fission1d.paths import DATA_DIR
    p = DATA_DIR / f"parsed_output_{energy_groups}_group.json"
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def BuildRuntimeInput(
    base: dict,
    *,
    config: int,
    test_case: int | None,
    generations: int,
    histories: int,
    skip: int,
) -> dict:
    ri = dict(base)
    ri["Config"] = config
    if test_case is not None:
        ri["TestCase"] = test_case
    ri["Generations"] = int(generations)
    ri["Histories"] = int(histories)
    ri["Skip"] = int(min(skip, max(0, generations - 1)))
    return ri


def ApplyOverridesWhenFull(mesh_data: dict, full: bool, generations: int, histories: int):
    m = dict(mesh_data)
    if full:
        m["totalGenerations"] = generations
        m["totalHistories"] = histories
    m["skipGenerations"] = min(m["skipGenerations"], m["totalGenerations"] - 1)
    return m


def RunCase(
    mc,
    base_input: dict,
    *,
    config: int,
    test_case: int | None,
    generations: int,
    histories: int,
    skip: int,
    seed: int,
    engine: str,
    full: bool = True,
):
    ri = BuildRuntimeInput(
        base_input,
        config=config,
        test_case=test_case,
        generations=generations,
        histories=histories,
        skip=skip,
    )
    xs = mc.BuildCrossSectionTables(ri)
    mesh_data = mc.CreateMeshAndAssignData(ri, xs)
    mesh_data = ApplyOverridesWhenFull(mesh_data, full, generations, histories)
    results = mc.SimulateParticlesAndCalculateParametersOfInterest(
        mesh_data, seed=seed, engine=engine
    )
    return ri, mesh_data, results


def normalize_flux(phi: np.ndarray) -> np.ndarray:
    m = np.max(phi)
    if m <= 0:
        return phi
    return phi / m


def PlotFLuxComparison(plt, mesh_data: dict, results_by_cfg: dict, out_dir: Path):
    x = mesh_data["xCenter"]
    dx = np.asarray(mesh_data["deltaXArray"], dtype=float)
    midpoint = mesh_data["domainWidth"] / 2.0
    first_assembly = x < midpoint
    second_assembly = x > midpoint

    fig, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    for g in range(2):
        ax = axes[g]
        for config, res in sorted(results_by_cfg.items()):
            phi = res["averageFlux"][g]
            if config == 0:
                name = "UO2-UO2"
                color = "C0"
            elif config == 1:
                name = "MOX-MOX"
                color = "C1"
            else:
                name = f"Config {config}"
                color = "C2"

            ax.plot(x, phi, lw=1.2, color=color, label=name)

            first_assembly_average = float(np.average(phi[first_assembly], weights=dx[first_assembly]))
            second_assembly_average = float(np.average(phi[second_assembly], weights=dx[second_assembly]))
            ax.hlines(first_assembly_average, x[first_assembly][0], x[first_assembly][-1],
                      colors=color, ls="--", lw=1.2, alpha=0.7,
                      label=f"{name} Ass 1 avg = {first_assembly_average:.4f}")
            ax.hlines(second_assembly_average, x[second_assembly][0], x[second_assembly][-1],
                      colors=color, ls=":", lw=1.2, alpha=0.7,
                      label=f"{name} Ass 2 avg = {second_assembly_average:.4f}")

        ax.set_ylabel(f"Group {g} flux")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=7)
    axes[-1].set_xlabel("x (cm)")
    fig.tight_layout()
    p = out_dir / "part2_flux_by_config.png"
    fig.savefig(p, dpi=150)
    plt.close(fig)
    return p


def PlotKByGeneration(plt, results_by_cfg: dict, out_dir: Path):
    fig, ax = plt.subplots(figsize=(8, 4))
    for config, res in sorted(results_by_cfg.items()):
        k_eff_generation = res["kGeneration"]
        k_eff_avg = float(res["kEffective"])
        if config == 0:
            label = f"UO2-UO2 ($\\langle k_{{eff}}\\rangle$ = {k_eff_avg:.5f})"
        elif config ==1:
            label = f"MOX-MOX ($\\langle k_{{eff}}\\rangle$ = {k_eff_avg:.5f})"
        ax.plot(np.arange(len(k_eff_generation)), k_eff_generation, lw=1, marker="o", ms=2, label=label)
    # Analytical k_eff (η·f): UO2-UO2 = config 0, MOX-MOX = config 1
    ax.axhline(1.26, color="C0", ls="--", lw=1.2, alpha=0.85, label="Analytic k (UO2) = 1.26")
    ax.axhline(1.125, color="C1", ls="--", lw=1.2, alpha=0.85, label="Analytic k (MOX) = 1.125")
    ax.set_xlabel("Generation")
    ax.set_ylabel(r"$k_{eff}}$ (per generation)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    p = out_dir / "part2_k_by_generation.png"
    fig.savefig(p, dpi=150)
    plt.close(fig)
    return p


def PlotMeshConvergence(plt, delta_x_list, k_eff_list, se_list, out_dir: Path):
    dx = np.asarray(delta_x_list, dtype=float)
    k = np.asarray(k_eff_list, dtype=float)
    se = np.asarray(se_list, dtype=float)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.errorbar(dx, k, yerr=se, fmt="ko-", ms=8, lw=1.2, capsize=4,
                label=r"$k_{eff} \pm$ std err")
    ax.set_xlabel(r"Mesh size $\Delta x$ (cm)")
    ax.set_ylabel(r"$k_{eff}$")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    p = out_dir / "part2_mesh_convergence.png"
    fig.savefig(p, dpi=150)
    plt.close(fig)
    return p


def PlotGenerationConvergence(plt, gen_list, k_eff_list, std_err_list, out_dir: Path):
    g = np.asarray(gen_list, dtype=float)
    k = np.asarray(k_eff_list, dtype=float)
    se = np.asarray(std_err_list, dtype=float)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.errorbar(g, k, yerr=se, fmt="ko-", ms=8, lw=1.2, capsize=4, label=r"$k_{eff} \pm$ std err")
    ax.set_xlabel("Number of generations")
    ax.set_ylabel(r"$k_{eff}$")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    p = out_dir / "part2_generation_convergence.png"
    fig.savefig(p, dpi=150)
    plt.close(fig)
    return p


def PlotSkipConvergence(plt, skip_list, k_eff_list, se_list, out_dir: Path):
    s = np.asarray(skip_list, dtype=float)
    k = np.asarray(k_eff_list, dtype=float)
    se = np.asarray(se_list, dtype=float)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.errorbar(s, k, yerr=se, fmt="ko-", ms=8, lw=1.2, capsize=4,
                label=r"$k_{eff} \pm$ std err")
    ax.set_xlabel("Skip (inactive) generations")
    ax.set_ylabel(r"$k_{eff}$")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    p = out_dir / "part2_skip_convergence.png"
    fig.savefig(p, dpi=150)
    plt.close(fig)
    return p


def NumericalConvergence(plt, histories_list: list, se_k: np.ndarray, out_dir: Path):
    h = np.asarray(histories_list, dtype=float)
    y = np.asarray(se_k, dtype=float)
    inv_sqrt = 1.0 / np.sqrt(h)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(inv_sqrt, y, "ko-", ms=8, lw=1.2, label="MC runs")

    slope = float(np.dot(inv_sqrt, y) / np.dot(inv_sqrt, inv_sqrt))
    xs = np.linspace(0, float(inv_sqrt.max()) * 1.05, 100)
    ax.plot(xs, slope * xs, "r--", lw=1.2, label=rf"fit $\propto 1/\sqrt{{N}}$")

    ax.set_xlabel(r"$1/\sqrt{N}$  (histories per generation)")
    ax.set_ylabel(r"Std error of $k_{eff}$")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    p = out_dir / "part2_se_k_vs_inv_sqrt.png"
    fig.savefig(p, dpi=150)
    plt.close(fig)
    return p


def main():
    parser = argparse.ArgumentParser(description="Part 2 MC verification (both configs).")
    parser.add_argument("--energy-groups", type=int, default=2)
    parser.add_argument("--test-case", type=int, default=None, help="Override TestCase from JSON")
    parser.add_argument("--output-dir", type=str, default=str(RESULTS_DIR / "mc_verification"))
    parser.add_argument("--engine", choices=("python", "numba"), default="numba")
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--seed", type=int, default=42, help="Fixed RNG seed for every MC run")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    if not out_dir.is_absolute():
        out_dir = RESULTS_DIR / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        mc = load_mc_module()
    except Exception as e:
        print("Failed to import fission1d.monte_carlo:", e, file=sys.stderr)
        sys.exit(1)

    if args.engine is None:
        args.engine = "numba" if getattr(mc, "_NUMBA_AVAILABLE", False) else "python"


    base = LoadInputJson(args.energy_groups)

    if args.quick:
        generations, histories, skip = 40, 300, 5
        hist_sweep: list[int] = []
        mesh_multipliers: list[int] = []
        gen_sweep: list[int] = []
        skip_sweep: list[int] = []
    else:
        generations, histories, skip = 200, 100000, 5
        mesh_multipliers: list[int] = []
        hist_sweep: list[int] = [200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000]
        gen_sweep: list[int] = [] # [25, 50, 75, 100, 150, 200, 300, 400, 500, 600]
        skip_sweep: list[int] =[] # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    test_case = args.test_case if args.test_case is not None else base.get("TestCase")

    results_main = {}
    mesh_data_ref = None
    for cfg in (0, 1):
        ri, mesh_data, results = RunCase(
            mc,
            base,
            config=cfg,
            test_case=test_case,
            generations=generations,
            histories=histories,
            skip=skip,
            seed=args.seed,
            engine=args.engine,
        )
        results_main[cfg] = results
        mesh_data_ref = mesh_data


    figure_paths: list[Path | None] = []
    figure_paths.append(PlotFLuxComparison(plt, mesh_data_ref, results_main, out_dir))
    figure_paths.append(PlotKByGeneration(plt, results_main, out_dir))

    if hist_sweep:
        se_k = np.zeros(len(hist_sweep))
        k_eff_vals = np.zeros(len(hist_sweep))
        wall_times = np.zeros(len(hist_sweep))
        for i, h in enumerate(hist_sweep):
            if h == histories and 0 in results_main:
                res = results_main[0]
            else:
                _, _, res = RunCase(
                    mc,
                    base,
                    config=0,
                    test_case=test_case,
                    generations=generations,
                    histories=h,
                    skip=skip,
                    seed=args.seed,
                    engine=args.engine,
                )
            k_eff_vals[i] = float(res["kEffective"])
            se_k[i] = float(res["kEffectiveStdErr"])
            wall_times[i] = float(res["wallTimeSeconds"])

        print()
        print("=== History Convergence (UO2-UO2, config 0) ===")
        print(f"{'Histories':>10s}  {'k_eff':>10s}  {'Std err':>10s}  {'Time (s)':>10s}")
        print("-" * 46)
        for i, h in enumerate(hist_sweep):
            print(f"{h:10d}  {k_eff_vals[i]:10.5f}  {se_k[i]:10.5f}  {wall_times[i]:10.2f}")
        print()

        if len(hist_sweep) >= 2:
            figure_paths.append(NumericalConvergence(plt, hist_sweep, se_k, out_dir))
    elif args.quick:
        print(
            "# --quick: skipped convergence plots (run without --quick to generate).",
            file=sys.stderr,
        )

    # --- Mesh convergence sweep (config 0) ---
    if mesh_multipliers:
        base_mpfr = base["MPFR"]
        base_mpwr = base["MPWR"]
        dx_vals = []
        k_mesh = []
        se_mesh = []
        t_mesh = []
        n_meshes_list = []

        for mult in mesh_multipliers:
            sweep_base = dict(base)
            sweep_base["MPFR"] = base_mpfr * mult
            sweep_base["MPWR"] = base_mpwr * mult
            _, md, res = RunCase(
                mc,
                sweep_base,
                config=0,
                test_case=test_case,
                generations=generations,
                histories=histories,
                skip=skip,
                seed=args.seed,
                engine=args.engine,
            )
            dx_vals.append(float(md["deltaX"]))
            k_mesh.append(float(res["kEffective"]))
            se_mesh.append(float(res["kEffectiveStdErr"]))
            t_mesh.append(float(res["wallTimeSeconds"]))
            n_meshes_list.append(int(md["totalMeshes"]))

        print()
        print("=== Mesh Convergence (UO2-UO2, config 0) ===")
        print(f"{'MPFR':>6s}  {'MPWR':>6s}  {'Meshes':>7s}  {'dx (cm)':>10s}  {'k_eff':>10s}  {'Std err':>10s}  {'Time (s)':>10s}")
        print("-" * 67)
        for i, mult in enumerate(mesh_multipliers):
            print(
                f"{base_mpfr*mult:6d}  {base_mpwr*mult:6d}  {n_meshes_list[i]:7d}  "
                f"{dx_vals[i]:10.5f}  {k_mesh[i]:10.5f}  {se_mesh[i]:10.5f}  {t_mesh[i]:10.2f}"
            )
        print()

        if len(mesh_multipliers) >= 2:
            figure_paths.append(PlotMeshConvergence(plt, dx_vals, k_mesh, se_mesh, out_dir))

    # --- Generation convergence sweep (config 0) ---
    if gen_sweep:
        k_gen_sweep = []
        se_gen_sweep = []
        t_gen_sweep = []

        for g in gen_sweep:
            s = min(skip, g - 1)
            _, _, res = RunCase(
                mc,
                base,
                config=0,
                test_case=test_case,
                generations=g,
                histories=histories,
                skip=s,
                seed=args.seed,
                engine=args.engine,
            )
            k_gen_sweep.append(float(res["kEffective"]))
            se_gen_sweep.append(float(res["kEffectiveStdErr"]))
            t_gen_sweep.append(float(res["wallTimeSeconds"]))

        print()
        print("=== Generation Convergence (UO2-UO2, config 0) ===")
        print(f"{'Generations':>12s}  {'k_eff':>10s}  {'Std err':>10s}  {'Time (s)':>10s}")
        print("-" * 48)
        for i, g in enumerate(gen_sweep):
            print(f"{g:12d}  {k_gen_sweep[i]:10.5f}  {se_gen_sweep[i]:10.5f}  {t_gen_sweep[i]:10.2f}")
        print()

        if len(gen_sweep) >= 2:
            figure_paths.append(PlotGenerationConvergence(plt, gen_sweep, k_gen_sweep, se_gen_sweep, out_dir))

    # --- Skip generation convergence sweep (config 0) ---
    if skip_sweep:
        k_skip = []
        se_skip = []
        t_skip = []

        for s in skip_sweep:
            if s >= generations:
                continue
            _, _, res = RunCase(
                mc,
                base,
                config=0,
                test_case=test_case,
                generations=generations,
                histories=histories,
                skip=s,
                seed=args.seed,
                engine=args.engine,
            )
            k_skip.append(float(res["kEffective"]))
            se_skip.append(float(res["kEffectiveStdErr"]))
            t_skip.append(float(res["wallTimeSeconds"]))

        valid_skips = [s for s in skip_sweep if s < generations]
        print()
        print("=== Skip Generation Convergence (UO2-UO2, config 0) ===")
        print(f"{'Skip':>6s}  {'Active':>7s}  {'k_eff':>10s}  {'Std err':>10s}  {'Time (s)':>10s}")
        print("-" * 48)
        for i, s in enumerate(valid_skips):
            print(f"{s:6d}  {generations - s:7d}  {k_skip[i]:10.5f}  {se_skip[i]:10.5f}  {t_skip[i]:10.2f}")
        print()

        if len(valid_skips) >= 2:
            figure_paths.append(PlotSkipConvergence(plt, valid_skips, k_skip, se_skip, out_dir))

    for p in figure_paths:
        if p:
            print(p)


if __name__ == "__main__":
    main()
