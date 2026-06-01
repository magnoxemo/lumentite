import sys
sys.path.append("../../")


import argparse
from pathlib import Path
import openmc
from models.geometry_base import SlabLayer, build_1D_geometry
from models.tallies import build_settings, build_tallies
from models.utilities import build_mgxs_library, build_openmc_materials, load_yaml
from properties import *


def build_model(xs_yaml: Path, output_dir: Path, batches: int, inactive: int, particles: int, mesh_cells: int,
                transverse_half_width: float = 0.5) -> openmc.Model:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    hdf5_path = output_dir / "slab_mgxs.h5"
    xs_config = load_yaml(xs_yaml)["cross_sections"]

    build_mgxs_library(xs_config, hdf5_path)
    materials = build_openmc_materials(xs_config, hdf5_path)
    mat_map = {mat.name: mat for mat in materials}

    slab_stack = [SlabLayer(m, t) for m, t in zip(MATERIALS, THICKNESSES)]
    geometry, total_length = build_1D_geometry(slab_stack, mat_map, transverse_half_width)

    tallies = build_tallies(total_length, transverse_half_width, mesh_cells, output_dir)
    settings = build_settings(total_length, transverse_half_width, batches, inactive, particles)

    model = openmc.Model(geometry=geometry, materials=materials, settings=settings, tallies=tallies)
    model.export_to_model_xml(output_dir / "model.xml")
    return model


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--xs", type=Path, default=Path("../../cross_sections/cross_section.yaml"))
    parser.add_argument("--outdir", type=Path, default=Path("."))
    parser.add_argument("--batches", type=int, default=200)
    parser.add_argument("--inactive", type=int, default=50)
    parser.add_argument("--particles", type=int, default=50_000)
    parser.add_argument("--mesh-cells", type=int, default=200)
    args = parser.parse_args()

    build_model(xs_yaml=args.xs, output_dir=args.outdir, batches=args.batches, inactive=args.inactive, particles=args.particles, mesh_cells=args.mesh_cells, )


if __name__ == "__main__":
    main()
