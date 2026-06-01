from __future__ import annotations
from typing import NamedTuple
import openmc


class SlabLayer(NamedTuple):
    material: str
    thickness: float  # cm


def build_1D_geometry(slab_stack: list[SlabLayer], mat_map: dict[str, openmc.Material], transverse_half_width: float) \
        -> tuple[openmc.Geometry, float]:
    total_length = sum(layer.thickness for layer in slab_stack)
    x_planes = _build_x_planes(slab_stack)
    transverse = _build_transverse_region(transverse_half_width)

    cells = [_make_cell(i, layer, mat_map, x_planes, transverse) for i, layer in enumerate(slab_stack)]

    geometry = openmc.Geometry(openmc.Universe(cells=cells))
    return geometry, total_length


def _build_x_planes(slab_stack: list[SlabLayer]) -> list[openmc.XPlane]:
    planes = [openmc.XPlane(x0=0.0, boundary_type="reflective")]
    x = 0.0
    for layer in slab_stack:
        x += layer.thickness
        planes.append(openmc.XPlane(x0=x))
    planes[-1].boundary_type = "reflective"
    return planes


def _build_transverse_region(hw: float):
    return (+openmc.YPlane(y0=-hw, boundary_type="reflective") & -openmc.YPlane(y0=hw, boundary_type="reflective")
            & +openmc.ZPlane(z0=-hw, boundary_type="reflective") & -openmc.ZPlane(z0=hw, boundary_type="reflective"))


def _make_cell(index: int, layer: SlabLayer, mat_map: dict[str, openmc.Material], x_planes: list[openmc.XPlane], transverse_region) -> openmc.Cell:
    """Create and return a single slab cell."""
    cell = openmc.Cell(name=f"slab_{index + 1}_{layer.material}")
    cell.fill = mat_map[layer.material]
    cell.region = +x_planes[index] & -x_planes[index + 1] & transverse_region
    return cell
