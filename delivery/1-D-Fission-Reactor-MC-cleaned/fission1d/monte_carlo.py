import argparse
import json
import os
import time

import numpy as np

try:
    from numba import njit, types
    from numba.typed import List
    _NUMBA_AVAILABLE = True
except ImportError:  # pragma: no cover - optional acceleration
    _NUMBA_AVAILABLE = False

from fission1d.paths import DATA_DIR, RESULTS_DIR


# Numba
if _NUMBA_AVAILABLE:

    @njit(cache=False)
    def _find_mesh_jit(x, domain_width, n_meshes, x_right):
        if x <= 0.0:
            return 0
        if x >= domain_width:
            return n_meshes - 1
        return np.searchsorted(x_right, x, side="right")

    @njit(cache=False)
    def _reflective_jit(bound, energy_group):
        return bound[energy_group] >= 0.5

    @njit(cache=False)
    def _sample_chi_jit(chi_t, mesh_idx, n_groups):
        s = 0.0
        for g in range(n_groups):
            s += chi_t[g, mesh_idx]
        if s <= 0.0:
            return 0
        xi = np.random.random() * s
        c = 0.0
        for g in range(n_groups):
            c += chi_t[g, mesh_idx]
            if xi < c:
                return g
        return n_groups - 1

    @njit(cache=False)
    def _sample_interaction_jit(sig_f, sig_a, sig_is, sig_ds, n_groups, eg):
        sig_capture = sig_a - sig_f if sig_a > sig_f else 0.0
        w0 = sig_capture
        w1 = sig_f
        w2 = sig_is
        w3 = sig_ds
        tw = w0 + w1 + w2 + w3
        if tw <= 0.0:
            return 0, eg
        xi = np.random.random() * tw
        if xi < w0:
            return 0, eg
        xi -= w0
        if xi < w1:
            return 1, eg
        xi -= w1
        if xi < w2:
            return 2, eg
        new_eg = eg + 1
        if new_eg >= n_groups:
            new_eg = n_groups - 1
        return 2, new_eg

    @njit(cache=False)
    def _bank_fission_jit(nu_t, chi_t, eg, mesh_idx, x, fission_sites, fx, fg):
        nu = nu_t[eg, mesh_idx]
        n = int(np.floor(nu + np.random.random()))
        fission_sites[mesh_idx] += n
        ngroups = chi_t.shape[0]
        for _ in range(n):
            g = _sample_chi_jit(chi_t, mesh_idx, ngroups)
            fx.append(x)
            fg.append(np.int64(g))

    @njit(cache=False)
    def _track_particle_numba(
        x_position,
        energy_group,
        domain_width,
        n_meshes,
        n_groups,
        x_right,
        x_left,
        material_id,
        nxs_sigt,
        nxs_sigis,
        nxs_sigds,
        nxs_sigtr,
        nxs_siga,
        nxs_sigf,
        nxs_nut,
        nxs_chit,
        bound_l,
        bound_r,
        track_length,
        surface_current,
        collisions,
        fission_sites,
        fx,
        fg,
    ):
        mu = 2.0 * np.random.random() - 1.0
        if abs(mu) < 1.0e-12:
            mu = 1.0

        particle_exists = True
        small_number = 1.0e-12

        while particle_exists:
            mesh_idx = _find_mesh_jit(x_position, domain_width, n_meshes, x_right)

            xs_total = nxs_sigt[energy_group, mesh_idx]
            xs_inscatter = nxs_sigis[energy_group, mesh_idx]
            xs_downscatter = nxs_sigds[energy_group, mesh_idx]
            xs_transport = nxs_sigtr[energy_group, mesh_idx]
            xs_scattering = xs_inscatter + xs_downscatter
            xs_absorption = nxs_siga[energy_group, mesh_idx]

            if xs_total == 0:
                xs_total = xs_absorption + xs_scattering

            if xs_transport == 0:
                xs_transport = xs_total - mu * xs_scattering

            remaining_travel_length = -np.log(np.random.random()) / xs_total

            while particle_exists and remaining_travel_length > 0.0:
                mesh_idx = _find_mesh_jit(x_position, domain_width, n_meshes, x_right)

                if mu > 0.0:
                    boundary_x = x_right[mesh_idx]
                    distance_to_boundary_x = boundary_x - x_position
                    interface_idx = mesh_idx + 1
                else:
                    boundary_x = x_left[mesh_idx]
                    distance_to_boundary_x = x_position - boundary_x
                    interface_idx = mesh_idx

                if distance_to_boundary_x < 0.0:
                    distance_to_boundary_x = 0.0
                travel_length_to_boundary = distance_to_boundary_x / abs(mu)

                if remaining_travel_length < travel_length_to_boundary - 1.0e-12:
                    track_length[energy_group, mesh_idx] += remaining_travel_length
                    x_position += mu * remaining_travel_length
                    if x_position < 0.0:
                        x_position = 0.0
                    elif x_position > domain_width:
                        x_position = domain_width
                    collisions[energy_group, mesh_idx] += 1.0

                    sig_f = nxs_sigf[energy_group, mesh_idx]
                    sig_a = nxs_siga[energy_group, mesh_idx]
                    sig_is = nxs_sigis[energy_group, mesh_idx]
                    sig_ds = nxs_sigds[energy_group, mesh_idx]
                    kind, new_eg = _sample_interaction_jit(
                        sig_f, sig_a, sig_is, sig_ds, n_groups, energy_group
                    )

                    if kind == 0:
                        particle_exists = False
                    elif kind == 1:
                        _bank_fission_jit(
                            nxs_nut,
                            nxs_chit,
                            energy_group,
                            mesh_idx,
                            x_position,
                            fission_sites,
                            fx,
                            fg,
                        )
                        particle_exists = False
                    else:
                        energy_group = new_eg
                        mu = 2.0 * np.random.random() - 1.0
                        if abs(mu) < 1.0e-12:
                            mu = 1.0

                    remaining_travel_length = 0.0
                    continue

                track_length[energy_group, mesh_idx] += travel_length_to_boundary
                sgn = 1.0 if mu > 0.0 else -1.0
                surface_current[energy_group, interface_idx] += sgn
                remaining_travel_length -= travel_length_to_boundary
                x_position = boundary_x

                if abs(boundary_x) < 1.0e-12:
                    if _reflective_jit(bound_l, energy_group):
                        mu *= -1.0
                        x_position += small_number
                    else:
                        particle_exists = False
                    continue

                if abs(boundary_x - domain_width) < 1.0e-12:
                    if _reflective_jit(bound_r, energy_group):
                        mu *= -1.0
                        x_position -= small_number
                    else:
                        particle_exists = False
                    continue

                next_position = boundary_x + small_number * sgn
                next_mesh_idx = _find_mesh_jit(
                    next_position, domain_width, n_meshes, x_right
                )
                crossed_material = material_id[next_mesh_idx] != material_id[mesh_idx]
                x_position = next_position

                if crossed_material:
                    break


def BuildRunBasename(mesh_data, runtime_input):
    ng = int(runtime_input["EnergyGroups"])
    tc = int(runtime_input["TestCase"])
    cf = int(runtime_input["Config"])
    gen = int(mesh_data["totalGenerations"])
    hist = int(mesh_data["totalHistories"])
    return f"eg{ng}_case{tc}_cfg{cf}_g{gen}_h{hist}"


def SaveRunResults(output_dir, basename, mesh_data, results, runtime_input, seed):
    os.makedirs(output_dir, exist_ok=True)
    stem = os.path.join(output_dir, basename)
    meta = {
        "energy_groups": int(runtime_input["EnergyGroups"]),
        "test_case": int(runtime_input["TestCase"]),
        "config": int(runtime_input["Config"]),
        "generations": int(mesh_data["totalGenerations"]),
        "histories": int(mesh_data["totalHistories"]),
        "seed": int(seed),
        "k_effective": float(results["kEffective"]),
        "k_effective_std_err": (
            None
            if np.isnan(float(results["kEffectiveStdErr"]))
            else float(results["kEffectiveStdErr"])
        ),
        "wall_time_seconds": float(results["wallTimeSeconds"]),
        "skip_generations_used": int(results["skipGenerationsUsed"]),
        "domain_width_cm": float(mesh_data["domainWidth"]),
        "basename": basename,
    }

    with open(stem + ".meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    np.savez_compressed(
        stem + ".npz",
        k_generation=results["kGeneration"],
        average_flux=results["averageFlux"],
        average_current=results["averageCurrent"],
        x_center=mesh_data["xCenter"],
        fission_source_density=results["fissionSourceDensity"],
        generation_flux=results["generationFlux"],
        generation_current=results["generationCurrent"],
    )
    return stem


def BuildCrossSectionTables(input_data):
    energy_groups = input_data["EnergyGroups"]
    number_of_materials = input_data["MatTypes"]
    cross_sections = input_data["XSData"][str(input_data["TestCase"])]

    xs_tables = {
        "SigT": np.zeros((energy_groups, number_of_materials)),
        "SigTR": np.zeros((energy_groups, number_of_materials)),
        "SigIS": np.zeros((energy_groups, number_of_materials)),
        "SigDS": np.zeros((energy_groups, number_of_materials)),
        "SigA": np.zeros((energy_groups, number_of_materials)),
        "SigF": np.zeros((energy_groups, number_of_materials)),
        "nuT": np.zeros((energy_groups, number_of_materials)),
        "ChiT": np.zeros((energy_groups, number_of_materials)),
    }

    for material_idx in range(number_of_materials):
        for energy_group in range(energy_groups):
            if energy_groups == 2:
                xs_tables["SigT"][energy_group, material_idx] = 0
                xs_tables["SigTR"][energy_group, material_idx] = cross_sections["SigTR"][str(material_idx)][str(energy_group)]
            if energy_groups == 7:
                xs_tables["SigT"][energy_group, material_idx] = cross_sections["SigT"][str(material_idx)][str(energy_group)]
                xs_tables["SigTR"][energy_group, material_idx] = 0
            
            xs_tables["SigIS"][energy_group, material_idx] = cross_sections["SigIS"][str(material_idx)][str(energy_group)]
            xs_tables["SigDS"][energy_group, material_idx] = cross_sections["SigDS"][str(material_idx)][str(energy_group)]
            xs_tables["SigA"][energy_group, material_idx] = cross_sections["SigA"][str(material_idx)][str(energy_group)]
            xs_tables["SigF"][energy_group, material_idx] = cross_sections["SigF"][str(material_idx)][str(energy_group)]
            xs_tables["nuT"][energy_group, material_idx] = cross_sections["nuT"][str(material_idx)][str(energy_group)]
            xs_tables["ChiT"][energy_group, material_idx] = cross_sections["ChiT"][str(material_idx)][str(energy_group)]

    return xs_tables



def CreateMeshAndAssignData(input_data, xs_tables):
    rods_per_assembly = int(input_data["NumRods"])
    rod_pitch = float(input_data["RodPitch"])
    mesh_per_fuel_rod = input_data["MPFR"]
    mesh_per_water_rod = input_data["MPWR"]
    energy_groups = input_data["EnergyGroups"]
    num_ass = int(input_data.get("NumAss", 1))

    mat_rows = input_data["ConfigSets"][str(input_data["Config"])]["MatID"]

    assembly_width = float(input_data.get("AssemblyWidth", rods_per_assembly * rod_pitch))

    meshes_per_unit_cell = mesh_per_fuel_rod + mesh_per_water_rod
    delta_x = rod_pitch / meshes_per_unit_cell
    num_rods_total = rods_per_assembly * num_ass
    total_meshes = num_rods_total * meshes_per_unit_cell
    domain_width = num_ass * assembly_width

    delta_x_array = np.full(total_meshes, delta_x)
    x_left = np.zeros(total_meshes)
    x_right = np.zeros(total_meshes)
    x_center = np.zeros(total_meshes)
    material_id = np.zeros(total_meshes, dtype=np.int64)

    mesh_idx = 0
    for assembly_idx in range(num_ass):
        mat_ids = mat_rows[assembly_idx]
        moderator_materials = [mat_ids[idx] for idx in range(0, len(mat_ids), 2)]
        fuel_materials = [mat_ids[idx] for idx in range(1, len(mat_ids), 2)]

        x0 = assembly_idx * assembly_width

        for rod_idx in range(rods_per_assembly):
            unit_cell_start = x0 + rod_idx * rod_pitch
            current_mesh_in_cell = 0
            left_moderator = moderator_materials[rod_idx]
            right_moderator = moderator_materials[rod_idx + 1]
            fuel_material = fuel_materials[rod_idx]

            for _ in range(mesh_per_water_rod // 2):
                x_left[mesh_idx] = unit_cell_start + current_mesh_in_cell * delta_x
                x_right[mesh_idx] = x_left[mesh_idx] + delta_x
                x_center[mesh_idx] = 0.5 * (x_left[mesh_idx] + x_right[mesh_idx])
                material_id[mesh_idx] = left_moderator
                current_mesh_in_cell += 1
                mesh_idx += 1

            for _ in range(mesh_per_fuel_rod):
                x_left[mesh_idx] = unit_cell_start + current_mesh_in_cell * delta_x
                x_right[mesh_idx] = x_left[mesh_idx] + delta_x
                x_center[mesh_idx] = 0.5 * (x_left[mesh_idx] + x_right[mesh_idx])
                material_id[mesh_idx] = fuel_material
                current_mesh_in_cell += 1
                mesh_idx += 1

            for _ in range(mesh_per_water_rod // 2):
                x_left[mesh_idx] = unit_cell_start + current_mesh_in_cell * delta_x
                x_right[mesh_idx] = x_left[mesh_idx] + delta_x
                x_center[mesh_idx] = 0.5 * (x_left[mesh_idx] + x_right[mesh_idx])
                material_id[mesh_idx] = right_moderator
                current_mesh_in_cell += 1
                mesh_idx += 1

    expanded_xs = {}
    for xs_name, xs_table in xs_tables.items():
        expanded_xs[f"NXS_{xs_name}"] = xs_table[:, material_id]

    fuel_meshes = np.flatnonzero(np.any(expanded_xs["NXS_SigF"] > 0.0, axis=0))

    return {
        "energyGroups": energy_groups,
        "totalMeshes": total_meshes,
        "meshesPerUnitCell": meshes_per_unit_cell,
        "domainWidth": domain_width,
        "deltaX": delta_x,
        "deltaXArray": delta_x_array,
        "xLeft": x_left,
        "xRight": x_right,
        "xCenter": x_center,
        "materialID": material_id,
        "fuelMeshes": fuel_meshes,
        "BoundL": np.asarray(input_data["BoundL"], dtype=np.float64),
        "BoundR": np.asarray(input_data["BoundR"], dtype=np.float64),
        "totalGenerations": input_data["Generations"],
        "totalHistories": input_data["Histories"],
        "skipGenerations": input_data["Skip"],
        **expanded_xs,
    }



def SampleEnergyGroup(probabilities, rng, fallback_group=0):
    probabilities = np.asarray(probabilities, dtype=float)
    total_probability = probabilities.sum()
    if total_probability <= 0.0:
        return fallback_group

    normalized = probabilities / total_probability
    return int(rng.choice(len(normalized), p=normalized))


def FindMesh(x_position, mesh_data):
    if x_position <= 0.0:
        return 0
    if x_position >= mesh_data["domainWidth"]:
        return mesh_data["totalMeshes"] - 1
    return int(np.searchsorted(mesh_data["xRight"], x_position, side="right"))


def IsReflectiveBoundary(boundary_values, energy_group):
    return bool(boundary_values[energy_group] >= 0.5)


def CreateTallies(mesh_data):
    return {
        "trackLength": np.zeros((mesh_data["energyGroups"], mesh_data["totalMeshes"])),
        "surfaceCurrent": np.zeros((mesh_data["energyGroups"], mesh_data["totalMeshes"] + 1)),
        "collisions": np.zeros((mesh_data["energyGroups"], mesh_data["totalMeshes"])),
        "fissionSites": np.zeros(mesh_data["totalMeshes"]),
    }


def CreateEmptySourceBank():
    return {
        "x": np.empty(0, dtype=float),
        "group": np.empty(0, dtype=np.int64),
    }


def BuildSourceBank(fission_positions, fission_groups):
    if not fission_positions:
        return CreateEmptySourceBank()

    return {
        "x": np.asarray(fission_positions, dtype=float),
        "group": np.asarray(fission_groups, dtype=np.int64),
    }


def SampleBirthPosition(mesh_data, rng, source_bank=None):
    if source_bank is not None and source_bank["x"].size > 0:
        source_idx = int(rng.integers(source_bank["x"].size))
        return (
            float(source_bank["x"][source_idx]),
            int(source_bank["group"][source_idx]),
        )

    mesh_idx = int(rng.choice(mesh_data["fuelMeshes"]))
    x_position = rng.uniform(mesh_data["xLeft"][mesh_idx], mesh_data["xRight"][mesh_idx])
    energy_group = SampleEnergyGroup(mesh_data["NXS_ChiT"][:, mesh_idx], rng, fallback_group=0)
    return float(x_position), energy_group


def SampleTypeOfInteraction(mesh_data, energy_group, mesh_idx, rng):
    sig_f = mesh_data["NXS_SigF"][energy_group, mesh_idx]
    sig_a = mesh_data["NXS_SigA"][energy_group, mesh_idx]
    sig_is = mesh_data["NXS_SigIS"][energy_group, mesh_idx]
    sig_ds = mesh_data["NXS_SigDS"][energy_group, mesh_idx]
    sig_capture = max(sig_a - sig_f, 0.0)

    event_weights = np.array([sig_capture, sig_f, sig_is, sig_ds], dtype=float)
    total_weight = event_weights.sum()
    if total_weight <= 0.0:
        return "capture", energy_group

    xi = rng.random() * total_weight
    if xi < event_weights[0]:
        return "capture", energy_group
    xi -= event_weights[0]
    if xi < event_weights[1]:
        return "fission", energy_group
    xi -= event_weights[1]
    if xi < event_weights[2]:
        return "scatter", energy_group
    return "scatter", min(energy_group + 1, mesh_data["energyGroups"] - 1)


def BankFissionNeutrons(mesh_data, energy_group, mesh_idx, x_position, tallies, fission_positions, fission_groups, rng):
    expected_nu = mesh_data["NXS_nuT"][energy_group, mesh_idx]
    produced_neutrons = int(np.floor(expected_nu + rng.random()))
    tallies["fissionSites"][mesh_idx] += produced_neutrons

    for _ in range(produced_neutrons):
        new_group = SampleEnergyGroup(mesh_data["NXS_ChiT"][:, mesh_idx], rng, fallback_group=0)
        fission_positions.append(float(x_position))
        fission_groups.append(int(new_group))


def TrackParticle(particle, mesh_data, tallies, fission_positions, fission_groups, rng):
    x_position = float(particle[0])
    energy_group = int(particle[1])
    mu = 2.0 * rng.random() - 1.0
    if abs(mu) < 1.0e-12:
        mu = 1.0

    particle_exists = True
    small_number = 1.0e-12

    while particle_exists:
        mesh_idx = FindMesh(x_position, mesh_data)

        xs_total = mesh_data["NXS_SigT"][energy_group, mesh_idx]
        xs_inscatter = mesh_data["NXS_SigIS"][energy_group, mesh_idx]
        xs_downscattter = mesh_data["NXS_SigDS"][energy_group, mesh_idx]
        xs_transport = mesh_data["NXS_SigTR"][energy_group, mesh_idx]
        xs_scattering = xs_inscatter + xs_downscattter
        xs_absorption = mesh_data["NXS_SigA"][energy_group, mesh_idx]

        if xs_total == 0:
            xs_total = xs_absorption + xs_scattering

        if xs_transport == 0:
            xs_transport = xs_total - mu * xs_scattering

        remaining_travel_length = -np.log(rng.random()) / xs_total

        while particle_exists and remaining_travel_length > 0.0:
            mesh_idx = FindMesh(x_position, mesh_data)

            if mu > 0.0:
                boundary_x = mesh_data["xRight"][mesh_idx]
                distance_to_boundary_x = boundary_x - x_position
                interface_idx = mesh_idx + 1
            else:
                boundary_x = mesh_data["xLeft"][mesh_idx]
                distance_to_boundary_x = x_position - boundary_x
                interface_idx = mesh_idx

            distance_to_boundary_x = max(distance_to_boundary_x, 0.0)
            travel_length_to_boundary = distance_to_boundary_x / abs(mu)

            if remaining_travel_length < travel_length_to_boundary - 1.0e-12:
                tallies["trackLength"][energy_group, mesh_idx] += remaining_travel_length
                x_position += mu * remaining_travel_length
                x_position = np.clip(x_position, 0.0, mesh_data["domainWidth"])
                tallies["collisions"][energy_group, mesh_idx] += 1.0

                interaction_type, new_group = SampleTypeOfInteraction(mesh_data, energy_group, mesh_idx, rng)

                if interaction_type == "capture":
                    particle_exists = False
                elif interaction_type == "fission":
                    BankFissionNeutrons(mesh_data, energy_group, mesh_idx, x_position, tallies, fission_positions, fission_groups, rng)
                    particle_exists = False
                else:
                    energy_group = new_group
                    mu = 2.0 * rng.random() - 1.0
                    if abs(mu) < 1.0e-12:
                        mu = 1.0

                remaining_travel_length = 0.0
                continue

            tallies["trackLength"][energy_group, mesh_idx] += travel_length_to_boundary
            tallies["surfaceCurrent"][energy_group, interface_idx] += np.sign(mu)
            remaining_travel_length -= travel_length_to_boundary
            x_position = boundary_x

            if np.isclose(boundary_x, 0.0):
                if IsReflectiveBoundary(mesh_data["BoundL"], energy_group):
                    mu *= -1.0
                    x_position += small_number
                else:
                    particle_exists = False
                continue

            if np.isclose(boundary_x, mesh_data["domainWidth"]):
                if IsReflectiveBoundary(mesh_data["BoundR"], energy_group):
                    mu *= -1.0
                    x_position -= small_number
                else:
                    particle_exists = False
                continue

            next_position = boundary_x + small_number * np.sign(mu)
            next_mesh_idx = FindMesh(next_position, mesh_data)
            crossed_material = mesh_data["materialID"][next_mesh_idx] != mesh_data["materialID"][mesh_idx]
            x_position = next_position

            if crossed_material:
                break


# --- Numba-facing wrappers (call compiled kernels) -----------------------------------


def FindMeshNumba(x_position, mesh_data):
    if not _NUMBA_AVAILABLE:
        return FindMesh(x_position, mesh_data)
    return int(
        _find_mesh_jit(
            float(x_position),
            float(mesh_data["domainWidth"]),
            int(mesh_data["totalMeshes"]),
            mesh_data["xRight"],
        )
    )


def SampleEnergyGroupNumba(mesh_data, mesh_idx):
    return int(_sample_chi_jit(mesh_data["NXS_ChiT"], int(mesh_idx), int(mesh_data["energyGroups"])))


def TrackParticleNumba(particle, mesh_data, tallies, fission_positions, fission_groups, rng):
    if not _NUMBA_AVAILABLE:
        TrackParticle(particle, mesh_data, tallies, fission_positions, fission_groups, rng)
        return

    fx = List.empty_list(types.float64)
    fg = List.empty_list(types.int64)
    md = mesh_data
    _track_particle_numba(
        float(particle[0]),
        int(particle[1]),
        float(md["domainWidth"]),
        int(md["totalMeshes"]),
        int(md["energyGroups"]),
        np.ascontiguousarray(md["xRight"], dtype=np.float64),
        np.ascontiguousarray(md["xLeft"], dtype=np.float64),
        np.ascontiguousarray(md["materialID"], dtype=np.int64),
        np.ascontiguousarray(md["NXS_SigT"], dtype=np.float64),
        np.ascontiguousarray(md["NXS_SigIS"], dtype=np.float64),
        np.ascontiguousarray(md["NXS_SigDS"], dtype=np.float64),
        np.ascontiguousarray(md["NXS_SigTR"], dtype=np.float64),
        np.ascontiguousarray(md["NXS_SigA"], dtype=np.float64),
        np.ascontiguousarray(md["NXS_SigF"], dtype=np.float64),
        np.ascontiguousarray(md["NXS_nuT"], dtype=np.float64),
        np.ascontiguousarray(md["NXS_ChiT"], dtype=np.float64),
        np.ascontiguousarray(md["BoundL"], dtype=np.float64),
        np.ascontiguousarray(md["BoundR"], dtype=np.float64),
        tallies["trackLength"],
        tallies["surfaceCurrent"],
        tallies["collisions"],
        tallies["fissionSites"],
        fx,
        fg,
    )
    fission_positions.extend(list(fx))
    fission_groups.extend(list(fg))


def UseNumbaOrRegularPython(engine: str):
    engine = engine.lower().strip()
    if engine == "numba":
        if not _NUMBA_AVAILABLE:
            print("Numba is not installed; falling back to the pure-Python engine.")
            return "python"
        return "numba"
    if engine == "python":
        return "python"
    raise ValueError(f"Unknown engine '{engine}'. Choose 'python' or 'numba'.")

def SimulateParticlesAndCalculateParametersOfInterest(mesh_data, seed=12345, engine=None):
    if engine is None:
        engine = "numba" if _NUMBA_AVAILABLE else "python"
    engine = UseNumbaOrRegularPython(engine)
    track_fn = TrackParticleNumba if engine == "numba" else TrackParticle

    rng = np.random.default_rng(seed)
    if engine == "numba":
        np.random.seed(int(seed))
    total_generations = mesh_data["totalGenerations"]
    total_histories = mesh_data["totalHistories"]
    energy_groups = mesh_data["energyGroups"]
    total_meshes = mesh_data["totalMeshes"]

    generation_flux = np.zeros((total_generations, energy_groups, total_meshes))
    generation_current = np.zeros((total_generations, energy_groups, total_meshes + 1))
    generation_k = np.zeros(total_generations)
    source_bank = None
    completed_generations = 0

    t0 = time.perf_counter()
    for generation_idx in range(total_generations):
        tallies = CreateTallies(mesh_data)
        fission_positions = []
        fission_groups = []

        for _ in range(total_histories):
            particle = SampleBirthPosition(mesh_data, rng, source_bank)
            track_fn(particle, mesh_data, tallies, fission_positions, fission_groups, rng)

        fission_bank = BuildSourceBank(fission_positions, fission_groups)
        generation_flux[generation_idx] = tallies["trackLength"] / (
            total_histories * mesh_data["deltaXArray"][None, :]
        )
        generation_current[generation_idx] = tallies["surfaceCurrent"] / total_histories
        generation_k[generation_idx] = fission_bank["x"].size / total_histories
        completed_generations += 1

        source_bank = fission_bank

    generation_flux = generation_flux[:completed_generations]
    generation_current = generation_current[:completed_generations]
    generation_k = generation_k[:completed_generations]

    skip_generations = min(mesh_data["skipGenerations"], completed_generations - 1)
    average_flux = generation_flux[skip_generations:].mean(axis=0)
    average_current = generation_current[skip_generations:].mean(axis=0)
    k_active = generation_k[skip_generations:]
    k_effective = float(k_active.mean())
    n_active = int(k_active.size)
    if n_active > 1:
        k_effective_std_err = float(np.std(k_active, ddof=1) / np.sqrt(n_active))
    else:
        k_effective_std_err = float("nan")
    wall_time_seconds = time.perf_counter() - t0

    fission_source_density = np.sum(
        mesh_data["NXS_nuT"] * mesh_data["NXS_SigF"] * average_flux,
        axis=0,
    )

    return {
        "completedGenerations": completed_generations,
        "kGeneration": generation_k,
        "kEffective": k_effective,
        "kEffectiveStdErr": k_effective_std_err,
        "wallTimeSeconds": wall_time_seconds,
        "generationFlux": generation_flux,
        "generationCurrent": generation_current,
        "averageFlux": average_flux,
        "averageCurrent": average_current,
        "fissionSourceDensity": fission_source_density,
        "skipGenerationsUsed": skip_generations,
    }


def PrintResultsSummary(mesh_data, results):
    print("Simulation summary")
    print(f"  Completed generations: {results['completedGenerations']}")
    print(f"  Histories per generation: {mesh_data['totalHistories']}")
    print(f"  Skipped generations: {results['skipGenerationsUsed']}")
    print(f"  Estimated k-effective: {results['kEffective']:.6f}")
    k_se = results["kEffectiveStdErr"]
    if np.isnan(k_se):
        print("  Std err on k (active generations, mean): n/a (< 2 active generations)")
    else:
        print(f"  Std err on k (active generations, mean): {k_se:.6f}")
    print(f"  Wall time (simulation): {results['wallTimeSeconds']:.3f} s")
    print()

    print("Generation-by-generation k")
    for generation_idx, k_value in enumerate(results["kGeneration"]):
        print(f"  Generation {generation_idx:3d}: k = {k_value:.6f}")
    print()

    print("Average flux by energy group")
    for energy_group in range(mesh_data["energyGroups"]):
        peak_mesh = int(np.argmax(results["averageFlux"][energy_group]))
        print(
            f"  Group {energy_group}: peak flux = {results['averageFlux'][energy_group, peak_mesh]:.6f} "
            f"at x = {mesh_data['xCenter'][peak_mesh]:.4f} cm"
        )
    print()


def ParseArguments():
    parser = argparse.ArgumentParser(
        description="1D multigroup Monte Carlo transport for the ENU6106 project."
    )
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--generations", type=int, default=None)
    parser.add_argument("--histories", type=int, default=None)
    parser.add_argument("--seed", type=int, default=12345)
    parser.add_argument("--case", type=int, default=None)
    parser.add_argument("--config", type=int, default=None)
    parser.add_argument("--energy-groups", type=int, default=2)
    parser.add_argument("--output-dir", type=str, default=str(RESULTS_DIR / "monte_carlo"))
    parser.add_argument("--no-save", action="store_true")   
    parser.add_argument("--engine", type=str, choices=("python", "numba"), default="numba")
    return parser.parse_args()


def ApplyRuntimeOverrides(mesh_data, arguments):
    updated_mesh = dict(mesh_data)

    if arguments.full:
        if arguments.generations is not None:
            updated_mesh["totalGenerations"] = arguments.generations
        if arguments.histories is not None:
            updated_mesh["totalHistories"] = arguments.histories
    else:
        if arguments.generations is None:
            updated_mesh["totalGenerations"] = min(updated_mesh["totalGenerations"], 10)
        else:
            updated_mesh["totalGenerations"] = arguments.generations

        if arguments.histories is None:
            updated_mesh["totalHistories"] = min(updated_mesh["totalHistories"], 200)
        else:
            updated_mesh["totalHistories"] = arguments.histories

    updated_mesh["skipGenerations"] = min(
        updated_mesh["skipGenerations"],
        updated_mesh["totalGenerations"] - 1,
    )
    return updated_mesh


def main():
    arguments = ParseArguments()
    energy_groups = arguments.energy_groups

    input_file = DATA_DIR / f"parsed_output_{energy_groups}_group.json"

    with open(input_file, "r", encoding="utf-8") as file:
        input_data = json.load(file)

    runtime_input = dict(input_data)
    if arguments.case is not None:
        runtime_input["TestCase"] = arguments.case
    if arguments.config is not None:
        runtime_input["Config"] = arguments.config

    xs_tables = BuildCrossSectionTables(runtime_input)
    mesh_data = CreateMeshAndAssignData(runtime_input, xs_tables)
    mesh_data = ApplyRuntimeOverrides(mesh_data, arguments)
    results = SimulateParticlesAndCalculateParametersOfInterest(
        mesh_data, seed=arguments.seed, engine=arguments.engine
    )
    PrintResultsSummary(mesh_data, results)

    if not arguments.no_save:
        out_dir = arguments.output_dir
        if not os.path.isabs(out_dir):
            out_dir = str(RESULTS_DIR / out_dir)
        basename = BuildRunBasename(mesh_data, runtime_input)
        stem = SaveRunResults(out_dir, basename, mesh_data, results, runtime_input, arguments.seed)
        print(f"Saved run data: {stem}.npz")
        print(f"Saved metadata: {stem}.meta.json")


if __name__ == "__main__":
    main()
