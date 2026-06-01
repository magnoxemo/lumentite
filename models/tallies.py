from __future__ import annotations
from pathlib import Path
import openmc


def build_tallies(total_length: float, transverse_half_width: float,  mesh_cells: int,  xml_dir: Path) -> openmc.Tallies:
    hw = transverse_half_width

    mesh = openmc.RegularMesh()
    mesh.dimension = (mesh_cells, 1, 1)
    mesh.lower_left = (0.0, -hw, -hw)
    mesh.upper_right = (total_length, hw, hw)

    flux_tally = openmc.Tally(name="spatial_flux")
    flux_tally.filters = [openmc.MeshFilter(mesh)]
    flux_tally.scores = ["flux", "fission", "nu-fission"]

    global_tally = openmc.Tally(name="global_rates")
    global_tally.scores = ["nu-fission", "fission"]

    tallies = openmc.Tallies([flux_tally, global_tally])
    return tallies


def build_settings(total_length: float, transverse_half_width: float, batches: int, inactive: int,
                   particles: int) -> openmc.Settings:

    hw = transverse_half_width

    source_box = openmc.stats.Box( lower_left=(0.0, -hw, -hw), upper_right=(total_length, hw, hw))

    settings = openmc.Settings()
    settings.energy_mode = "multi-group"
    settings.batches = batches
    settings.inactive = inactive
    settings.particles = particles
    settings.source = openmc.IndependentSource(space=source_box, constraints={"fissionable": True})
    settings.output = {"tallies": True, "summary": False}

    return settings
