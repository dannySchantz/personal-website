import argparse
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from fission1d.paths import DATA_DIR, RESULTS_DIR

def LoadInputData(energy_groups, test_case=0, config=0):
    path = DATA_DIR / f"parsed_output_{energy_groups}_group.json"
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["TestCase"] = test_case
    data["Config"] = config
    return data


def BuildCrossSections(input_data):
    G = input_data["EnergyGroups"]
    M = input_data["MatTypes"]
    xs_raw = input_data["XSData"][str(input_data["TestCase"])]

    field_names = ["SigA", "SigF", "SigIS", "SigDS", "nuT", "ChiT"]
    xs = {name: np.zeros((G, M)) for name in field_names}
    xs["D"] = np.zeros((G, M))

    for m in range(M):
        for g in range(G):
            for name in field_names:
                xs[name][g, m] = xs_raw[name][str(m)][str(g)]

            sig_tr = xs_raw.get("SigTR", {}).get(str(m), {}).get(str(g), 0.0)
            sig_t = xs_raw.get("SigT", {}).get(str(m), {}).get(str(g), 0.0)

            if sig_tr > 0:
                xs["D"][g, m] = 1.0 / (3.0 * sig_tr)
            elif sig_t > 0:
                xs["D"][g, m] = 1.0 / (3.0 * sig_t)

    return xs

def CreateMesh(input_data, xs, mesh_refinement=1):
    rods_per_assembly = int(input_data["NumRods"])
    rod_pitch = float(input_data["RodPitch"])
    mpfr = input_data["MPFR"] * mesh_refinement
    mpwr = input_data["MPWR"] * mesh_refinement
    num_groups = input_data["EnergyGroups"]
    num_ass = int(input_data.get("NumAss", 1))
    mat_rows = input_data["ConfigSets"][str(input_data["Config"])]["MatID"]
    assembly_width = float(input_data.get("AssemblyWidth", rods_per_assembly * rod_pitch))

    meshes_per_cell = mpfr + mpwr
    dx = rod_pitch / meshes_per_cell
    total_rods = rods_per_assembly * num_ass
    N = total_rods * meshes_per_cell

    x_center = np.zeros(N)
    mat_id = np.zeros(N, dtype=int)

    idx = 0
    for ass in range(num_ass):
        ids = mat_rows[ass]
        mods = [ids[i] for i in range(0, len(ids), 2)]
        fuels = [ids[i] for i in range(1, len(ids), 2)]
        x0 = ass * assembly_width

        for rod in range(rods_per_assembly):
            cell_start = x0 + rod * rod_pitch
            local = 0

            for _ in range(mpwr // 2):
                x_center[idx] = cell_start + (local + 0.5) * dx
                mat_id[idx] = mods[rod]
                local += 1
                idx += 1

            for _ in range(mpfr):
                x_center[idx] = cell_start + (local + 0.5) * dx
                mat_id[idx] = fuels[rod]
                local += 1
                idx += 1

            for _ in range(mpwr // 2):
                x_center[idx] = cell_start + (local + 0.5) * dx
                mat_id[idx] = mods[rod + 1]
                local += 1
                idx += 1

    D = xs["D"][:, mat_id]
    SigR = xs["SigA"][:, mat_id] + xs["SigDS"][:, mat_id]
    nuSigF = xs["nuT"][:, mat_id] * xs["SigF"][:, mat_id]
    Chi = xs["ChiT"][:, mat_id]
    SigDS = xs["SigDS"][:, mat_id]

    return {
        "G": num_groups,
        "N": N,
        "dx": dx,
        "x_center": x_center,
        "mat_id": mat_id,
        "D": D,
        "SigR": SigR,
        "nuSigF": nuSigF,
        "Chi": Chi,
        "SigDS": SigDS,
        "BoundL": np.asarray(input_data["BoundL"], dtype=float),
        "BoundR": np.asarray(input_data["BoundR"], dtype=float),
    }

def BuildDiffusionMatrix(mesh, g):
    N = mesh["N"]
    dx = mesh["dx"]
    D = mesh["D"][g]
    SigR = mesh["SigR"][g]
    BL = mesh["BoundL"][g]
    BR = mesh["BoundR"][g]

    diag = np.zeros(N)
    upper = np.zeros(N - 1)
    lower = np.zeros(N - 1)

    d_cell = D / dx
    D_interface = np.zeros(N - 1)
    for i in range(N - 1):
        s = D[i] + D[i + 1]
        D_interface[i] = 2.0 * D[i] * D[i + 1] / s if s > 0 else 0.0
    d = D_interface / dx

    for i in range(1, N - 1):
        lower[i - 1] = -d[i - 1]
        diag[i] = d[i - 1] + d[i] + SigR[i] * dx
        upper[i] = -d[i]

    beta_l = 1.0 / (1.0 + d_cell[0] * (1.0 - BL) / (1.0 + BL))
    beta_r = 1.0 / (1.0 + d_cell[-1] * (1.0 - BR) / (1.0 + BR))

    # Left boundary row: a11 = 2*d1*(1-beta) + dx*SigR + d1,2
    diag[0] = 2.0 * d_cell[0] * (1.0 - beta_l) + SigR[0] * dx + d[0]
    upper[0] = -d[0]

    # Right boundary row: aNN = 2*dN*(1-beta) + dx*SigR + dN-1,N
    diag[N - 1] = 2.0 * d_cell[-1] * (1.0 - beta_r) + SigR[N - 1] * dx + d[N - 2]
    lower[N - 2] = -d[N - 2]

    return diag, lower, upper


def SolveMatrix(diag, lower, upper, rhs):
    A = np.diag(diag) + np.diag(upper, 1) + np.diag(lower, -1)
    return np.linalg.solve(A, rhs)

def PowerIteration(mesh, tol_k=1e-6, tol_flux=1e-5, max_iter=10000):
    G = mesh["G"]
    N = mesh["N"]
    dx = mesh["dx"]
    nuSigF = mesh["nuSigF"]
    Chi = mesh["Chi"]
    SigDS = mesh["SigDS"]

    matrices = [BuildDiffusionMatrix(mesh, g) for g in range(G)]

    phi = np.ones((G, N))
    k = 1.0

    fission_source = np.sum(nuSigF * phi, axis=0)
    F_total = np.sum(fission_source) * dx

    k_history = [k]
    dk = float("nan")
    d_flux = float("nan")

    for iteration in range(max_iter):
        k_old = k
        F_old = F_total
        phi_old = phi.copy()

        for g in range(G):
            rhs = (Chi[g] / k) * fission_source * dx

            if g > 0:
                rhs += SigDS[g - 1] * phi[g - 1] * dx

            diag, lower, upper = matrices[g]
            phi[g] = SolveMatrix(diag, lower, upper, rhs)

        fission_source_new = np.sum(nuSigF * phi, axis=0)
        F_new = np.sum(fission_source_new) * dx

        k = k_old * F_new / F_old

        peak = np.max(np.abs(phi))
        if peak > 0:
            phi /= peak

        flux_den = np.maximum(np.abs(phi_old), 1.0e-30)
        d_flux = np.max(np.abs((phi - phi_old) / flux_den))

        fission_source = np.sum(nuSigF * phi, axis=0)
        F_total = np.sum(fission_source) * dx

        dk = abs((k - k_old) / k_old) if k_old != 0.0 else abs(k - k_old)

        k_history.append(k)

        if iteration > 10 and dk < tol_k and d_flux < tol_flux:
            print(f"Power iteration converged in {iteration + 1} iterations")
            print(f"  k-eff = {k:.6f}")
            print(f"  |dk/k| = {dk:.2e},  |d_flux| = {d_flux:.2e}")
            mesh["last_dk"] = dk
            mesh["last_d_flux"] = d_flux
            return phi, k, np.array(k_history)

    print(f"Power iteration did NOT converge after {max_iter} iterations")
    print(f"  k-eff = {k:.6f},  |dk/k| = {dk:.2e},  |d_flux| = {d_flux:.2e}")
    mesh["last_dk"] = dk
    mesh["last_d_flux"] = d_flux
    return phi, k, np.array(k_history)

def ComputeEdgeCurrents(mesh, phi):
    G = mesh["G"]
    N = mesh["N"]
    dx = mesh["dx"]
    D = mesh["D"]
    x_edges = np.arange(N + 1, dtype=float) * dx
    currents = np.zeros((G, N + 1))

    for g in range(G):
        Dg = D[g]
        for i in range(N - 1):
            s = Dg[i] + Dg[i + 1]
            D_interface = 2.0 * Dg[i] * Dg[i + 1] / s if s > 0 else 0.0
            currents[g, i + 1] = -D_interface * (phi[g, i + 1] - phi[g, i]) / dx

        if mesh["BoundL"][g] < 0.5:
            currents[g, 0] = -0.5 * phi[g, 0]
        if mesh["BoundR"][g] < 0.5:
            currents[g, -1] = 0.5 * phi[g, -1]

    return x_edges, currents

def PlotGroupFluxes(mesh, phi, k, energy_groups, case, config, save=True):
    G = mesh["G"]
    x = mesh["x_center"]

    if G <= 3:
        fig, axes = plt.subplots(1, G, figsize=(6 * G, 5))
    else:
        ncols = 4
        nrows = int(np.ceil(G / ncols))
        fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4 * nrows))

    if G == 1:
        axes = [axes]
    else:
        axes = np.asarray(axes).ravel()

    for g in range(G):
        axes[g].plot(x, phi[g], linewidth=1.2)
        axes[g].set_xlabel("Position (cm)")
        axes[g].set_ylabel(r"$\phi_{{{}}}(x)$".format(g + 1))
        axes[g].set_title(f"Group {g + 1}")
        axes[g].grid(True, alpha=0.3)

    for g in range(G, len(axes)):
        axes[g].set_visible(False)

    plt.tight_layout()

    if save:
        out_dir = RESULTS_DIR / "finite_diff"
        out_dir.mkdir(parents=True, exist_ok=True)
        fname = out_dir / f"fd_{energy_groups}g_case{case}_cfg{config}.png"
        plt.savefig(fname, dpi=150)
        print(f"Saved plot: {fname}")

def PlotAllGroupFluxes(mesh, phi, k, energy_groups, case, config, save=True):
    x = mesh["x_center"]
    fig, ax = plt.subplots(figsize=(9, 5))

    for g in range(mesh["G"]):
        ax.plot(x, phi[g], linewidth=1.2, label=f"Group {g + 1}")

    ax.set_xlabel("Position (cm)")
    ax.set_ylabel("Flux")
    ax.set_title(f"All Energy Group Fluxes (k = {k:.6f})")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=9, ncols=2 if mesh["G"] > 4 else 1)
    plt.tight_layout()

    if save:
        out_dir = RESULTS_DIR / "finite_diff"
        out_dir.mkdir(parents=True, exist_ok=True)
        fname = out_dir / f"fd_flux_allgroups_{energy_groups}g_case{case}_cfg{config}.png"
        plt.savefig(fname, dpi=150)
        print(f"Saved plot: {fname}")

def PlotAllGroupCurrents(mesh, phi, energy_groups, case, config, save=True):
    x_edges, currents = ComputeEdgeCurrents(mesh, phi)
    fig, ax = plt.subplots(figsize=(9, 5))

    for g in range(mesh["G"]):
        ax.plot(x_edges, currents[g], linewidth=1.2, label=f"Group {g + 1}")

    ax.set_xlabel("Position (cm)")
    ax.set_ylabel("Current")
    ax.set_title("All Energy Group Currents")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=9, ncols=2 if mesh["G"] > 4 else 1)
    plt.tight_layout()

    if save:
        out_dir = RESULTS_DIR / "finite_diff"
        out_dir.mkdir(parents=True, exist_ok=True)
        fname = out_dir / f"fd_current_allgroups_{energy_groups}g_case{case}_cfg{config}.png"
        plt.savefig(fname, dpi=150)
        print(f"Saved plot: {fname}")



def PlotKConvergence(k_history, save_path=None):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(k_history, marker="o", linewidth=0.8)
    ax.set_xlabel("Iteration (0 = initial guess)")
    ax.set_ylabel("k-eff")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)

def main():
    parser = argparse.ArgumentParser(
        description="Multigroup finite-difference diffusion k-eigenvalue solver"
    )
    parser.add_argument("--energy-groups", type=int, default=2, choices=[2, 7])
    parser.add_argument("--case", type=int, default=0)
    parser.add_argument("--config", type=int, default=0)
    parser.add_argument("--mesh-refinement", type=int, default=1,
                        help="Multiply MPFR and MPWR by this factor")
    parser.add_argument("--tol-k", type=float, default=1e-6,
                        help="Relative k convergence tolerance")
    parser.add_argument("--tol-flux", type=float, default=1e-5,
                        help="Relative flux convergence tolerance")
    parser.add_argument("--compare-mc", action="store_true",
                        help="Compare with Monte Carlo results if available")
    args = parser.parse_args()

    input_data = LoadInputData(args.energy_groups, args.case, args.config)
    xs = BuildCrossSections(input_data)
    mesh = CreateMesh(input_data, xs, mesh_refinement=args.mesh_refinement)

    print(f"{'='*60}")
    print(f"Multigroup Finite Difference Diffusion Solver")
    print(f"{'='*60}")
    print(f"  Energy groups:    {mesh['G']}")
    print(f"  Spatial cells:    {mesh['N']}")
    print(f"  Cell width (dx):  {mesh['dx']:.6f} cm")
    print(f"  Mesh refinement:  {args.mesh_refinement}x")
    print(f"  Test case:        {args.case}")
    print(f"  Config:           {args.config}")
    print(f"  Left BC:          {'Reflective' if mesh['BoundL'][0] >= 0.5 else 'Vacuum'}")
    print(f"  Right BC:         {'Reflective' if mesh['BoundR'][0] >= 0.5 else 'Vacuum'}")
    print(f"{'='*60}\n")

    phi, k, k_history = PowerIteration(
        mesh, tol_k=args.tol_k, tol_flux=args.tol_flux
    )

    print(f"\n{'='*60}")
    print(f"  RESULT:  k-eff = {k:.6f}")
    print(f"{'='*60}\n")

    PlotGroupFluxes(mesh, phi, k, args.energy_groups, args.case, args.config)
    PlotAllGroupFluxes(mesh, phi, k, args.energy_groups, args.case, args.config)
    PlotAllGroupCurrents(mesh, phi, args.energy_groups, args.case, args.config)
    out_dir = RESULTS_DIR / "finite_diff"
    out_dir.mkdir(parents=True, exist_ok=True)
    PlotKConvergence(
        k_history,
        save_path=str(
            out_dir
            / f"fd_convergence_{args.energy_groups}g_case{args.case}_cfg{args.config}.png"
        ),
    )

if __name__ == "__main__":
    main()
