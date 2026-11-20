"""The two light paths in 3D, in machine coordinates.

Run from the repository root:  uv run --with optiland --with pyvista python -m optics.rays

Output: viewer/rays.json (the 3D viewer shows it), docs/img/optics_3d.png, optics_3d_chip.png, optics_3d_field.png.

Path 1, projector to chip: mirror chip -> cube (straight through) -> objective -> chip.
Path 2, chip to camera:    chip -> objective -> cube (reflected to the rear) -> camera sensor.

There are two sets of rays:
- "two mirrors": two adjacent mirrors, with a cone of light from each corner. A real mirror is 5.4 micrometres wide
  and is not visible at the scale of the machine. Thus the two mirrors are drawn 960 times larger: each one covers
  half of the mirror chip.
- "whole image": cones of light from the centre and the four corners of the mirror chip and of the camera sensor.

Each cone has its own bright colour on a dark background, as in the layout pictures of lens design programs.
"""
import json
from pathlib import Path

import numpy as np

from cad import assembly as A

from .layout import CUBE_S, DMD, DMD_Z, GREEN, MAG, SENSOR, UV, system

ROOT = Path(__file__).resolve().parent.parent
ENLARGE = 960               # the two drawn mirrors are this many real mirrors wide (1920 / 2)
GAP = 0.15                  # drawn gap between the two mirrors, mm. It keeps the corner cones apart.
angles = np.linspace(0, 2 * np.pi, 12, endpoint=False)
CONE = [(0.0, 0.0)] + list(zip(np.cos(angles), np.sin(angles)))      # the centre ray and 12 rays on the rim
COOL = ["#3d7bff", "#00e5ff", "#00ff3c", "#b98cff"]                  # the four corners of mirror 1
WARM = ["#ff2a2a", "#ff9100", "#ffee00", "#ff3df2"]                  # the four corners of mirror 2
FIVE = ["#ffffff", "#3d7bff", "#00ff3c", "#ff2a2a", "#ffee00"]       # centre and four corners of the whole image


def trace(wavelength, points, pupil=((0.0, 0.0),)):
    """Trace rays from each object point (x, y in mm) through each pupil point (-1 to 1; 0, 0 = the centre ray).

    Return an array [ray, surface, 3]: x, y, and the distance s below the object.
    """
    reach = max(np.hypot(x, y) for x, y in points) or 1.0
    o = system(wavelength, (2 * reach, 0.0), picture=True)
    hx, hy, px, py = np.array([(x / reach, y / reach, u, v) for x, y in points for u, v in pupil]).T
    o.trace_generic(hx, hy, px, py, wavelength)
    s = o.surfaces.z - o.surfaces.z[0]
    return np.stack([o.surfaces.x, o.surfaces.y, s], axis=-1).transpose(1, 0, 2)


def to_projector(rays):
    """Machine coordinates for the projector path: the object is the mirror chip, above the cube."""
    rays = rays.copy()
    rays[..., 2] = DMD_Z - rays[..., 2]
    return rays.tolist()


def to_camera(rays):
    """Machine coordinates for the camera path: the object is the camera sensor. Fold at the diagonal of the cube.

    The diagonal reflects light that goes up (+z) to the rear (+y). It is the plane z - CUBE_Z = y.
    A point above this plane goes to (x, z - CUBE_Z, y + CUBE_Z).
    """
    lines = []
    for ray in rays:
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


def loop(corners, point):
    """A closed outline through `corners` (x, y). `point` puts each corner in the machine."""
    return [list(point(x, y)) for x, y in corners + corners[:1]]


on_mirror_chip = lambda x, y: (x, y, DMD_Z)                         # faces down
on_chip = lambda x, y: (-x / MAG, -y / MAG, A.CHIP_TOP)            # the objective turns the image and makes it smaller
on_sensor = lambda x, y: (x, A.ARM, A.CUBE_Z + y)                   # faces forward; the long side is vertical


def cones(points, colours, group, wavelength, place):
    """One path entry for each object point: the cone of light from that point, in its own colour."""
    rays = place(trace(wavelength, points, CONE))
    n = len(CONE)
    return [{"name": group, "group": group, "colour": c, "lines": rays[i * n:(i + 1) * n]} for i, c in enumerate(colours)]


def two_mirrors():
    """Two adjacent mirrors with a cone of light from each corner. The long side of the mirror chip is along machine y [E]."""
    side, short = DMD[0] / 2, DMD[1] / 2 - GAP
    projector, camera = [], []
    for name, colours, y0, y1 in (("Mirror 1", COOL, -side + GAP, -GAP), ("Mirror 2", WARM, GAP, side - GAP)):
        corners = [(-short, y0), (short, y0), (short, y1), (-short, y1)]
        group = f"{name}: projector to chip"
        projector += cones(corners, colours, group, UV, to_projector)
        projector.append({"name": group, "group": group, "colour": "#ffffff",
                          "lines": [loop(corners, on_mirror_chip), loop(corners, on_chip)]})
        group = f"{name}: chip to camera"
        camera += cones(corners, colours, group, GREEN, to_camera)
        camera.append({"name": group, "group": group, "colour": "#ffffff", "lines": [loop(corners, on_sensor)]})
    return projector + camera


def whole_image():
    """Cones of light from the centre and the four corners of the mirror chip and of the camera sensor."""
    def points(field):
        u, v = field[1] / 2, field[0] / 2
        return [(0, 0), (u, v), (-u, v), (u, -v), (-u, -v)]
    group = "Outlines: mirror chip, camera sensor, their areas on the chip"
    return (cones(points(DMD), FIVE, "Projector to chip (UV)", UV, to_projector)
            + cones(points(SENSOR), FIVE, "Chip to camera", GREEN, to_camera)
            + [{"name": group, "group": group, "colour": "#ffffff",
                "lines": [loop(points(DMD)[1:2] + points(DMD)[3:4] + points(DMD)[4:5] + points(DMD)[2:3], place)
                          for place in (on_mirror_chip, on_chip)]
                         + [loop(points(SENSOR)[1:2] + points(SENSOR)[3:4] + points(SENSOR)[4:5] + points(SENSOR)[2:3], place)
                            for place in (on_sensor, on_chip)]}])


# The parts on the light paths, with their colours in the picture. The viewer shows only these in "Optics only".
PARTS = {"chip": "#9a86c8", "chip holder": "#c0c4d0", "objective 10X": "#c0c4d0", "SM1L05": "#c0c4d0",
         "SM1L03": "#c0c4d0", "SM1A3": "#c0c4d0", "beamsplitter cube": "#7fd8f0", "camera sleeve": "#d8c090",
         "camera ASI174MM": "#e09090", "SM1V10": "#c0c4d0", "SM1L10": "#c0c4d0", "SM1A53 flange": "#c0c4d0",
         "adapter plate": "#d8c090", "projector light engine": "#c0c4d0"}


def picture(paths, out, bounds=None, view=(62, 14), zoom=1.25, size=(1500, 1900)):
    """A picture of the optical parts (transparent) with the light paths. It has no text: docs/optics.md names the parts."""
    import pyvista as pv
    p = pv.Plotter(off_screen=True, window_size=size)
    p.set_background("#16226e", top="#02040f")          # dark, as in lens design programs
    for name, _, solid in A.parts():
        if name in PARTS:
            v, t = solid.tessellate(0.05, 0.3)
            mesh = pv.PolyData(np.array([(q.X, q.Y, q.Z) for q in v]),
                               np.hstack([np.full((len(t), 1), 3), np.array(t)]).ravel())
            p.add_mesh(mesh, color=PARTS[name], opacity=0.25 if name in ("chip", "beamsplitter cube") else 0.10)
            edges = mesh.extract_feature_edges(feature_angle=35, boundary_edges=False,
                                               non_manifold_edges=False, manifold_edges=False)
            if edges.n_points:
                p.add_mesh(edges, color="#c8d2f0", line_width=1, opacity=0.3)
    for path in paths:
        for line in path["lines"]:
            p.add_mesh(pv.lines_from_points(np.array(line)), color=path["colour"], line_width=2.5)
    p.enable_depth_peeling(12)
    p.enable_anti_aliasing("ssaa")
    p.enable_parallel_projection()
    p.view_xz()
    p.camera.azimuth, p.camera.elevation = view
    p.reset_camera(bounds=bounds or (-35, 35, -35, 150, A.CHIP_TOP - 10, DMD_Z + 25))
    p.camera.zoom(zoom)
    p.screenshot(out)
    p.close()


if __name__ == "__main__":
    views = [{"name": f"Two mirrors, drawn {ENLARGE} X larger", "paths": two_mirrors()},
             {"name": "Whole image: 5 points", "paths": whole_image()}]
    for view in views:
        for path in view["paths"]:
            path["lines"] = [[[round(float(c), 3) for c in pt] for pt in line] for line in path["lines"]]
    (ROOT / "viewer" / "rays.json").write_text(json.dumps({
        "units": "mm, machine axes: x right, y rear, z up", "parts": list(PARTS),
        "chip": [0, 0, round(A.CHIP_TOP, 3)], "views": views}))
    print("viewer/rays.json")

    img = ROOT / "docs" / "img"
    picture(views[0]["paths"], img / "optics_3d.png")
    picture(views[0]["paths"], img / "optics_3d_chip.png", bounds=(-0.5, 0.5, -0.8, 0.8, A.CHIP_TOP, A.CHIP_TOP + 1.2),
            view=(62, 30), zoom=1.0, size=(1500, 1100))
    picture(views[1]["paths"], img / "optics_3d_field.png")
    print("docs/img/optics_3d.png, optics_3d_chip.png, optics_3d_field.png")
