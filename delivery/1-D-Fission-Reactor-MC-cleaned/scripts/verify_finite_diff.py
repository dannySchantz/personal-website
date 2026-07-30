from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import os
import time
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from fission1d.finite_diff import (
    LoadInputData,
    BuildCrossSections,
    CreateMesh,
    PowerIteration,
)
from fission1d.paths import RESULTS_DIR

OUTPUT_DIR = RESULTS_DIR / "fd_verification"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ENERGY_GROUPS = 2
TEST_CASE = 0
CONFIGS = [0, 1]
CONFIG_LABELS = {0: "Config: UO2-UO2", 1: "Config: MOX-MOX"}
MESH_REFINEMENTS = [1, 2, 4, 8, 16]

def RunCase(config, mesh_refinement=1):
    input_data = LoadInputData(ENERGY_GROUPS, TEST_CASE, config)
    xs = BuildCrossSections(input_data)
    mesh = CreateMesh(input_data, xs, mesh_refinement=mesh_refinement)
    phi, k, k_history = PowerIteration(mesh)
    return mesh, phi, k, k_history

def NormalizeFlux(flux):
    peak = np.max(np.abs(flux))
    return flux / peak if peak > 0 else flux

def RelativeL2FluxError(x_coarse, flux_coarse, x_ref, flux_ref):
    flux_ref_interp = np.interp(x_coarse, x_ref, flux_ref)
    dx = x_coarse[1] - x_coarse[0] if len(x_coarse) > 1 else 1.0
    diff = flux_coarse - flux_ref_interp
    num = np.sqrt(np.sum(diff ** 2) * dx)
    den = np.sqrt(np.sum(flux_ref_interp ** 2) * dx)
    return num / den if den > 0 else 0.0

def PlotFluxComparison():
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    group_names = ["Fast (Group 1)", "Thermal (Group 2)"]
    colors = ["tab:blue", "tab:orange"]

    results = {}
    for cfg in CONFIGS:
        mesh, phi, k, _ = RunCase(cfg)
        results[cfg] = (mesh, phi, k)

    for ax, cfg in zip(axes, CONFIGS):
        mesh, phi, k = results[cfg]
        x = mesh["x_center"]

        for g_idx, group_name in enumerate(group_names):
            flux = phi[g_idx]
            norm_flux = flux / np.max(flux) if np.max(flux) > 0 else flux
            ax.plot(
                x, norm_flux,
                color=colors[g_idx],
                linewidth=1.0,
                label=group_name,
            )

        ax.set_xlabel("Position (cm)")
        ax.set_ylabel("Normalized Flux")
        ax.set_title(f"{CONFIG_LABELS[cfg]}  (k = {k:.5f})")
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()

    path = OUTPUT_DIR / "fd_flux_config_comparison.png"
    plt.savefig(path, dpi=150)
    plt.close(fig)
    print(f"Saved: {path}")

def PlotMeshConvergence():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    group_names = ["Fast (Group 1)", "Thermal (Group 2)"]
    group_markers = ["o", "s"]
    group_styles = ["-", "--"]

    for cfg in CONFIGS:
        case_results = []
        k_values = []
        dx_values = []
        n_cells = []

        print(f"\n--- Mesh convergence: {CONFIG_LABELS[cfg]} ---")
        print(f"  {'Refinement':>10s}  {'Cells':>6s}  {'dx (cm)':>10s}  {'k-eff':>10s}  {'Time (s)':>10s}")

        for ref in MESH_REFINEMENTS:
            start_time = time.perf_counter()
            mesh, phi, k, _ = RunCase(cfg, mesh_refinement=ref)
            elapsed_time = time.perf_counter() - start_time
            case_results.append((ref, mesh, phi, k, elapsed_time))
            k_values.append(k)
            dx_values.append(mesh["dx"])
            n_cells.append(mesh["N"])
            print(
                f"  {ref:>10d}  {mesh['N']:>6d}  {mesh['dx']:>10.6f}  "
                f"{k:>10.6f}  {elapsed_time:>10.4f}"
            )

        axes[0].plot(
            n_cells, k_values,
            marker="o", linewidth=1.2,
            label=CONFIG_LABELS[cfg],
        )

        _, ref_mesh, ref_phi, _, _ = case_results[-1]
        ref_x = ref_mesh["x_center"]
        error_cells = n_cells[:-1]
        errors_by_group = {}

        for g_idx, group_name in enumerate(group_names):
            flux_errors = []

            ref_flux = NormalizeFlux(ref_phi[g_idx])
            for _, mesh, phi, _, _ in case_results[:-1]:
                flux = NormalizeFlux(phi[g_idx])
                err = RelativeL2FluxError(mesh["x_center"], flux, ref_x, ref_flux)
                flux_errors.append(err)

            errors_by_group[g_idx] = flux_errors + [0.0]
            plot_errors = np.asarray(flux_errors)
            positive_errors = plot_errors[plot_errors > 0.0]
            zero_error_floor = (
                0.1 * np.min(positive_errors)
                if len(positive_errors) > 0
                else 1.0e-16
            )
            plot_errors = np.where(plot_errors > 0.0, plot_errors, zero_error_floor)
            zero_note = " (zero error)" if np.any(np.asarray(flux_errors) == 0.0) else ""

            axes[1].plot(
                error_cells, plot_errors,
                marker=group_markers[g_idx],
                linestyle=group_styles[g_idx],
                linewidth=1.2,
                label=f"{CONFIG_LABELS[cfg]} - {group_name}{zero_note}",
            )

        print(f"\n  Relative flux error summary: {CONFIG_LABELS[cfg]}")
        print(
            f"  {'Refinement':>10s}  {'Meshes':>6s}  {'Time (s)':>10s}  "
            f"{'k-eff':>10s}  {'Fast error':>12s}  {'Thermal error':>14s}"
        )
        print("  " + "-" * 76)
        for idx, (ref, mesh, _, k, elapsed_time) in enumerate(case_results):
            print(
                f"  {ref:>10d}  {mesh['N']:>6d}  {elapsed_time:>10.4f}  "
                f"{k:>10.6f}  {errors_by_group[0][idx]:>12.4e}  "
                f"{errors_by_group[1][idx]:>14.4e}"
            )

    axes[0].set_xlabel("Number of Spatial Cells")
    axes[0].set_ylabel("k-eff")
    axes[0].set_title("k-eff vs Mesh Size")
    axes[0].legend(fontsize=9)
    axes[0].grid(True, alpha=0.3)

    axes[1].set_xlabel("Number of Spatial Cells")
    axes[1].set_ylabel("Relative Flux Error")
    axes[1].set_yscale("log")
    axes[1].legend(fontsize=9)
    axes[1].grid(True, alpha=0.3, which="both")

    plt.tight_layout()

    path = OUTPUT_DIR / "fd_mesh_convergence.png"
    plt.savefig(path, dpi=150)
    plt.close(fig)
    print(f"\nSaved: {path}")

if __name__ == "__main__":
    print("=" * 60)
    print("Finite Difference Verification Plots")
    print("=" * 60)

    print("\n[1/2] Flux comparison across configs...")
    PlotFluxComparison()

    print("\n[2/2] Mesh convergence study...")
    PlotMeshConvergence()

    print(f"\nAll plots saved to: {OUTPUT_DIR}")
