from __future__ import annotations

from pathlib import Path

import numpy as np
import openmc
import openmc.mgxs as mgxs
import yaml


def load_yaml(path: Path) -> dict:
    with open(path) as fh:
        return yaml.safe_load(fh)


def build_mgxs_library(xs_config: dict, hdf5_path: Path) -> mgxs.EnergyGroups:
    bounds = xs_config.get("energy_bounds_eV", [0.0, 20.0e6])
    groups = mgxs.EnergyGroups(np.array(bounds, dtype=float))

    library = openmc.MGXSLibrary(groups)
    for name, xs in xs_config["materials"].items():
        library.add_xsdata(_make_xsdata(name, xs, groups))

    library.export_to_hdf5(str(hdf5_path))
    return groups


def _make_xsdata(name: str, xs: dict, groups: mgxs.EnergyGroups) -> openmc.XSdata:
    G = groups.num_groups
    sig_t = np.array(xs["sigma_t"], dtype=float)
    sig_a = np.array(xs["sigma_a"], dtype=float)
    sig_s = np.array(xs["sigma_s"], dtype=float).reshape(G, G)
    sig_f = np.array(xs["sigma_f"], dtype=float)
    nu = np.array(xs["nu"], dtype=float)

    xsdata = openmc.XSdata(name, energy_groups=groups)
    xsdata.order = 0
    xsdata.set_total(sig_t)
    xsdata.set_absorption(sig_a)
    xsdata.set_scatter_matrix(sig_s[np.newaxis, :, :])

    if np.any(sig_f > 0.0):
        chi = np.array(xs.get("chi", [1.0 / G] * G), dtype=float)
        if G == 1:
            chi = np.array([1.0])
        xsdata.set_fission(sig_f)
        xsdata.set_nu_fission(nu * sig_f)
        xsdata.set_chi(chi)

    return xsdata


def build_openmc_materials(xs_config: dict, hdf5_path: Path) -> openmc.Materials:
    mat_map: dict[str, openmc.Material] = {}
    for mat_id, name in enumerate(xs_config["materials"], start=1):
        mat = openmc.Material(mat_id, name)
        mat.set_density("macro", 1.0)
        mat.add_macroscopic(name)
        mat_map[name] = mat

    collection = openmc.Materials(list(mat_map.values()))
    collection.cross_sections = str(hdf5_path)
    return collection
