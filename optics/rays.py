"""The two light paths in 3D, in machine coordinates.

Run from the repository root:  uv run --with optiland --with pyvista python -m optics.rays

Output: viewer/rays.json (the 3D viewer shows it) and docs/img/optics_3d.png.

Path 1, projector to chip: mirror chip -> cube (straight through) -> objective -> chip.
Path 2, chip to camera:    chip -> objective -> cube (reflected to the rear) -> camera sensor.
"""
import json
from pathlib import Path

import numpy as np

from cad import assembly as A

from .layout import CUBE_S, DMD, DMD_Z, GREEN, SENSOR, UV, system

ROOT = Path(__file__).resolve().parent.parent
RIM = 8                     # rays on the rim of each light cone


def trace(wavelength, field):
    """Trace cones of light from the centre and the four corners of `field` (long side, short side).

    Return an array [ray, surface, 3]: x, y, and the distance s below the object.
    The long side is along machine y [E]. The camera can turn in its clamp.
    """
    o = system(wavelength, field, picture=True)
    half_diagonal = np.hypot(*field) / 2
    hx, hy = field[1] / 2 / half_diagonal, field[0] / 2 / half_diagonal
    angles = np.linspace(0, 2 * np.pi, RIM, endpoint=False)
    rays = []
    for fx, fy in [(0, 0), (hx, hy), (-hx, hy), (hx, -hy), (-hx, -hy)]:
        n = np.ones(RIM)
        o.trace_generic(fx * n, fy * n, np.cos(angles), np.sin(angles), wavelength)
        s = o.surfaces.z - o.surfaces.z[0]
        rays.append(np.stack([o.surfaces.x, o.surfaces.y, s], axis=-1).transpose(1, 0, 2))
    return np.concatenate(rays)


def projector_path():
    """Polylines in machine coordinates: the object is the mirror chip, above the cube."""
    r = trace(UV, DMD)
    r[..., 2] = DMD_Z - r[..., 2]
    return r.tolist()


def camera_path():
    """The same model with the camera sensor as the object, then folded at the diagonal of the cube.

    The diagonal reflects light that goes up (+z) to the rear (+y). It is the plane z - CUBE_Z = y.
    A point above this plane goes to (x, z - CUBE_Z, y + CUBE_Z).
    """
    lines = []
    for ray in trace(GREEN, SENSOR):
        pts = [np.array([x, y, CUBE_S + 15 - s]) for x, y, s in ray]     # z is now from the cube centre
        out = []
        for a, b in zip(pts, pts[1:] + [None]):
            out.append(a)
            if b is not None and (a[2] - a[1]) * (b[2] - b[1]) < 0:      # the segment crosses the diagonal
                t = (a[2] - a[1]) / ((a[2] - a[1]) - (b[2] - b[1]))
                out.append(a + t * (b - a))
        folded = [(p[0], p[2], p[1]) if p[2] - p[1] > 1e-9 else tuple(p) for p in out]
        lines.append([[x, y, z + A.CUBE_Z] for x, y, z in folded])
    return lines


def paths():
    return [
        {"name": "Projector to chip (UV)", "colour": "#6a1bff", "lines": projector_path()},
        {"name": "Chip to camera", "colour": "#00963c", "lines": camera_path()},
    ]


# The parts on the light paths, with their colours in the picture. The viewer shows only these in "Optics only".
PARTS = {"chip": "#6b4fa0", "chip holder": "#b0b0b0", "objective 10X": "#909090", "SM1L05": "#909090",
         "SM1L03": "#909090", "SM1A3": "#909090", "beamsplitter cube": "#5bc0de", "camera sleeve": "#c8a060",
         "camera ASI174MM": "#c04040", "SM1V10": "#909090", "SM1L10": "#909090", "SM1A53 flange": "#909090",
         "adapter plate": "#c8a060", "projector light engine": "#606060"}


def picture(all_paths, out):
    """A picture of the optical parts (transparent) with the two light paths."""
    import pyvista as pv
    show = PARTS
    p = pv.Plotter(off_screen=True, window_size=(1500, 1900))
    p.set_background("white")
    for name, _, solid in A.parts():
        if name in show:
            v, t = solid.tessellate(0.05, 0.3)
            mesh = pv.PolyData(np.array([(q.X, q.Y, q.Z) for q in v]),
                               np.hstack([np.full((len(t), 1), 3), np.array(t)]).ravel())
            p.add_mesh(mesh, color=show[name], opacity=0.3 if name in ("chip", "beamsplitter cube") else 0.06)
            edges = mesh.extract_feature_edges(feature_angle=35, boundary_edges=False,
                                               non_manifold_edges=False, manifold_edges=False)
            if edges.n_points:
                p.add_mesh(edges, color="#30343a", line_width=1, opacity=0.25)
    for path in all_paths:
        for line in path["lines"]:
            p.add_mesh(pv.lines_from_points(np.array(line)), color=path["colour"], line_width=4)
    arm = A.ARM
    labels = {"mirror chip (in the projector)": (0, 0, DMD_Z), "beamsplitter cube": (0, -15, A.CUBE_Z),
              "camera sensor": (0, arm, A.CUBE_Z), "objective": (0, -12, A.SHOULDER - 20), "chip": (0, -16, A.CHIP_TOP),
              "projector to chip (UV)": (0, -13, A.CUBE_Z + 55), "chip to camera": (0, 60, A.CUBE_Z - 14)}
    p.add_point_labels(np.array(list(labels.values()), dtype=float), list(labels), always_visible=True, font_size=24,
                       shape_color="white", shape_opacity=0.85, text_color="black", show_points=False, margin=5)
    p.enable_depth_peeling(12)
    p.enable_anti_aliasing("ssaa")
    p.enable_parallel_projection()
    p.view_xz()
    p.camera.azimuth, p.camera.elevation = 62, 14
    p.reset_camera(bounds=(-35, 35, -35, 150, A.CHIP_TOP - 10, DMD_Z + 25))
    p.camera.zoom(1.25)
    p.screenshot(out)
    p.close()


if __name__ == "__main__":
    all_paths = paths()
    for path in all_paths:
        path["lines"] = [[[round(float(c), 3) for c in pt] for pt in line] for line in path["lines"]]
    (ROOT / "viewer" / "rays.json").write_text(json.dumps({"units": "mm, machine axes: x right, y rear, z up",
                                                           "parts": list(PARTS), "paths": all_paths}))
    print("viewer/rays.json")
    picture(all_paths, ROOT / "docs" / "img" / "optics_3d.png")
    print("docs/img/optics_3d.png")
