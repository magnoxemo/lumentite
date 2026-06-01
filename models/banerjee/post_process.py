from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import openmc
from properties import *


def shade_materials(ax) -> None:
    x = 0.0
    for mat, dx in zip(MATERIALS, THICKNESSES):
        ax.axvspan(x, x + dx, facecolor=MATERIAL_COLORS[mat], alpha=0.55, zorder=0)
        x += dx


def load_mesh_tally(statepoint_path: Path):
    with openmc.StatePoint(statepoint_path) as sp:
        tally = sp.get_tally(name="spatial_flux")
        mesh = tally.find_filter(openmc.MeshFilter).mesh

        nx = mesh.dimension[0]
        edges = np.linspace(mesh.lower_left[0], mesh.upper_right[0], nx + 1)
        x_centers = 0.5 * (edges[:-1] + edges[1:])

        flux = tally.get_values(scores=["flux"]).flatten()
        fission = tally.get_values(scores=["fission"]).flatten()
        keff = sp.keff

    return x_centers, flux, fission, keff


def plot(statepoint_path: Path, output_path: Path) -> None:
    x, flux, fission, keff = load_mesh_tally(statepoint_path)

    dx = x[1] - x[0]
    flux = flux / dx
    fission = fission / dx
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6), sharex=True)

    shade_materials(ax1)
    ax1.plot(x, flux, color="#1f3a93", lw=1.8)
    ax1.set_ylabel("flux")
    ax1.set_title(f"Banerjee 1-D slab   k_eff = {keff.n: .5f} ± {keff.s: .5f}")
    ax1.grid(alpha=0.3)

    shade_materials(ax2)
    ax2.plot(x, fission, color="#b8312f", lw=1.8)
    ax2.set_ylabel("fission rate")
    ax2.set_xlabel("x (cm)")
    ax2.grid(alpha=0.3)

    handles = [plt.Rectangle((0, 0), 1, 1, fc=c, alpha=0.55) for c in MATERIAL_COLORS.values()]
    ax1.legend(handles, list(MATERIAL_COLORS.keys()), loc="upper right", framealpha=0.9)

    ax1.set_xlim(x[0] - (x[1] - x[0]) / 2, x[-1] + (x[1] - x[0]) / 2)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    print(f"wrote {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("statepoint", type=Path)
    parser.add_argument("-o", "--output", type=Path, default=Path("flux_profile.png"))
    args = parser.parse_args()
    plot(args.statepoint, args.output)


if __name__ == "__main__":
    main()
