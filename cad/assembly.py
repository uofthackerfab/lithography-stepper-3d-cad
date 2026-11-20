"""Put every part of the stepper in its position. Check for collisions. Write the files.

Run from the repository root:  uv run --with pyvista python -m cad.assembly

Output: assembly/public/ (simple projector), assembly/private/ (real projector, not in git),
        docs/img/assembly_*.png (front, back, left, right, top, angle, labelled)
Axes: x = right, y = rear, z = up. The optical axis is x = y = 0. The table is z = 0.
"""
from itertools import combinations
from pathlib import Path

from build123d import Color, Compound, Pos, Rot, export_gltf, export_step

from . import params as P
from . import purchased as B
from .parts import (adapter_plate, beamsplitter_holder as holder, board_rail, camera_clamp,
                    camera_sleeve, chip_holder, projector_bracket, side_board_holder, stage_base, tube_clamp)
from .shapes import box

ROOT = Path(__file__).resolve().parent.parent

# --- Heights above the table, from the bottom up ---
STAND_Z = stage_base.T                       # bottom of the manipulator stand
BLOCK_Z = STAND_Z + 65.6                     # origin of the base block
EE_TOP = BLOCK_Z + 62.0                      # top face of the end effector
CHIP_TOP = EE_TOP + chip_holder.T - chip_holder.DEPTH + P.CHIP_T
OBJ_TIP = CHIP_TOP + 1.5                     # working distance
SHOULDER = OBJ_TIP + 44.0                    # objective shoulder = lower end of the tube
L03, L05, L10 = 8.4, 13.5, 26.2              # body lengths of the SM1 lens tubes
LOWER = L05 + L03                            # objective tube: SM1L05 below, SM1L03 above
SEAT = holder.CUBE_Z + holder.LIP            # cube centre to the end of each tube
CUBE_Z = SHOULDER + LOWER + 3 + SEAT         # centre of the beamsplitter cube
IMAGE = 150.0 + 10.2                         # objective shoulder to image; 10.2 for the cube glass [E]
ARM = IMAGE - (CUBE_Z - SHOULDER)            # cube centre to camera sensor, and to the mirror chip
DMD_TO_FACE = 41.4                           # mirror chip to lens face [V], projector CAD
FACE_Z = CUBE_Z + ARM - DMD_TO_FACE          # projector lens face = top of the adapter plate
PLATE_Z = FACE_Z - adapter_plate.T
V10_Z = CUBE_Z + SEAT                        # bottom of the SM1V10 collar; the collar sits in the holder
V10_TRAVEL = PLATE_Z - 5.56 - L10 - (V10_Z + 13.5)    # exposed barrel; the limit is 20.6
CAMERA_Y = ARM - 6.5                         # front face of the camera collar
BAR_TOP = P.BAR                              # the uprights stand on bar A
RAIL_Z = (CUBE_Z + 85, CUBE_Z + 85 + 115)    # main board rails
SIDE_Z = 510.0                               # screws of the side board; the uprights end at 520
CLAMP_Z = SHOULDER + 1.0                     # the clamp holds the SM1L05

FRAME, PRINTED, OPTICS, CAMERA, PROJECTOR, BOARD, STAGE, GLASS = (
    "#b8bcc2", "#3d4756", "#1c1c1e", "#b3261e", "#6f7d8c", "#1f7a3d", "#c98a2b", "#9fd6e8")


TURN = Rot(0, 0, 90)                          # the lip and LED block of the projector point to the right


def parts(real=False):
    """Return [(name, colour, solid)] with every solid in its final position.

    real=True uses the manufacturers' CAD files in vendor/, where they are present.
    """
    B.REAL = real
    y0, y1 = P.AXIS_TO_FRAME, P.FRAME_BACK
    yc = (y0 + y1) / 2
    out = [
        ("bar A (base)", FRAME, B.bar("x", -250, 250, yc, P.BAR / 2)),
        ("bar B (base)", FRAME, B.bar("y", y0 - 500, y0, 72, P.BAR / 2)),
        ("upright left", FRAME, B.bar("z", BAR_TOP, BAR_TOP + 500, -P.UPRIGHT_X, yc)),
        ("upright right", FRAME, B.bar("z", BAR_TOP, BAR_TOP + 500, P.UPRIGHT_X, yc)),
        ("stage base", PRINTED, stage_base.build()),
        ("chip holder", PRINTED, Pos(0, 0, EE_TOP) * chip_holder.build()),
        ("chip", GLASS, box(-P.CHIP / 2, P.CHIP / 2, -P.CHIP / 2, P.CHIP / 2, CHIP_TOP - P.CHIP_T, CHIP_TOP)),
        ("objective 10X", OPTICS, Pos(0, 0, SHOULDER) * B.objective()),
        ("SM1L05", OPTICS, Pos(0, 0, SHOULDER) * B.lens_tube(L05)),
        ("SM1A3", OPTICS, Pos(0, 0, SHOULDER) * B.sm1a3()),
        ("SM1L03", OPTICS, Pos(0, 0, SHOULDER + L05) * B.lens_tube(L03)),
        ("tube clamp", PRINTED, Pos(0, 0, CLAMP_Z) * tube_clamp.build()),
        ("beamsplitter holder base", PRINTED, Pos(0, 0, CUBE_Z) * holder.base()),
        ("beamsplitter holder cover", PRINTED, Pos(0, 0, CUBE_Z) * holder.cover()),
        ("beamsplitter cube", GLASS, Pos(0, 0, CUBE_Z) * B.cube()),
        ("camera sleeve", PRINTED, Pos(0, SEAT, CUBE_Z) * Rot(-90, 0, 0) * camera_sleeve.build()),
        ("camera clamp block", PRINTED, Pos(0, 0, CUBE_Z) * camera_clamp.block()),
        ("camera clamp cap", PRINTED,
         Pos(0, camera_clamp.CAP_Y + camera_clamp.CAP_W, CUBE_Z) * Rot(90, 0, 0) * camera_clamp.cap()),
        ("camera ASI174MM", CAMERA, Pos(0, CAMERA_Y, CUBE_Z) * B.camera()),
        ("SM1V10", OPTICS, Pos(0, 0, V10_Z) * B.sm1v10(V10_TRAVEL)),
        ("SM1L10", OPTICS, Pos(0, 0, V10_Z + 13.5 + V10_TRAVEL) * B.lens_tube(L10)),
        ("SM1A53 flange", OPTICS, Pos(0, 0, PLATE_Z - 5.56) * B.sm1a53()),
        ("adapter plate", PRINTED, Pos(0, 0, PLATE_Z) * TURN * adapter_plate.build()),
        ("projector bracket", PRINTED, Pos(0, 0, PLATE_Z) * projector_bracket.build()),
        ("projector light engine", PROJECTOR, Pos(0, 0, FACE_Z) * TURN * B.projector(real)),
        ("projector LED block [E]", PROJECTOR, Pos(0, 0, FACE_Z) * TURN * B.led_block()),
        ("board rail lower", PRINTED, Pos(0, 0, RAIL_Z[0]) * board_rail.build()),
        ("board rail upper", PRINTED, Pos(0, 0, RAIL_Z[1]) * board_rail.build()),
        ("main board", BOARD,
         Pos(0, y1 + board_rail.T + P.BOARD_STANDOFF, sum(RAIL_Z) / 2) * B.main_board()),
        ("side board holder", PRINTED, Pos(0, 0, SIDE_Z) * side_board_holder.build()),
        ("side board (HDMI)", BOARD,
         Pos(0, y1 + side_board_holder.T + P.BOARD_STANDOFF, SIDE_Z) * B.side_board()),
    ]
    ee = 47.5                                              # end effector centre in base block coordinates
    for name, solid in B.manipulator().items():
        colour = PRINTED if name == "stand" else OPTICS if "motor" == name[-5:] or "screws" in name else STAGE
        out.append((f"stage: {name}", colour, Pos(-ee, -ee, BLOCK_Z) * solid))
    return out


# Screw threads: in the manufacturers' models the two threads of a joint overlap.
THREADS = [{"SM1L05", "SM1A3"}, {"SM1L05", "SM1L03"}, {"SM1V10", "SM1L10"}, {"SM1L10", "SM1A53 flange"},
           {"SM1A3", "objective 10X"}]


def collisions(items, limit=1.0, skip=()):
    """Return [(name, name, volume)] for each pair that overlaps by more than `limit` mm3."""
    boxes = [s.bounding_box() for _, _, s in items]
    bad = []
    for i, j in combinations(range(len(items)), 2):
        a, b = boxes[i], boxes[j]
        if {items[i][0], items[j][0]} in skip:
            continue
        if items[i][0].startswith("stage:") and items[j][0].startswith("stage:"):
            continue                                       # the manipulator is one checked assembly
        if (a.min.X > b.max.X or b.min.X > a.max.X or a.min.Y > b.max.Y or b.min.Y > a.max.Y
                or a.min.Z > b.max.Z or b.min.Z > a.max.Z):
            continue
        common = items[i][2] & items[j][2]
        vol = common.volume if common else 0
        if vol > limit:
            bad.append((items[i][0], items[j][0], vol))
    return bad


def render(items, out):
    import numpy as np
    import pyvista as pv
    meshes = []
    for name, colour, solid in items:
        try:
            v, t = solid.tessellate(0.05, 0.3)
            pts = np.array([(p.X, p.Y, p.Z) for p in v])
            faces = np.hstack([np.full((len(t), 1), 3), np.array(t)]).ravel()
            meshes.append((colour, pv.PolyData(pts, faces)))
        except AttributeError:                             # a face without triangles (imported CAD)
            import tempfile
            from build123d import export_stl
            with tempfile.TemporaryDirectory() as d:
                export_stl(solid, f"{d}/a.stl", tolerance=0.05, angular_tolerance=0.3)
                meshes.append((colour, pv.read(f"{d}/a.stl")))
    labels = {"projector light engine": "projector", "main board": "main board", "side board (HDMI)": "side board", "SM1L10": "lens tubes",
              "beamsplitter holder cover": "beamsplitter holder (cube inside)", "camera ASI174MM": "camera",
              "objective 10X": "10X objective", "chip": "chip", "stage: base block": "micro-manipulator",
              "stage base": "stage base", "projector bracket": "projector bracket", "projector LED block [E]": "LED block (estimate)",
              "upright right": "2020 frame", "tube clamp": "tube clamp", "camera clamp block": "camera clamp"}
    centres = {n: s.bounding_box().center() for n, _, s in items if n in labels}
    # name: (azimuth, elevation). Azimuth 0 = camera in front; 90 = at the right. "top" looks straight down.
    views = {"front": (0, 0), "back": (180, 0), "left": (-90, 0), "right": (90, 0), "top": None,
             "angle": (-45, 45), "labelled": (-55, 12)}
    for view, angles in views.items():
        p = pv.Plotter(off_screen=True, window_size=(1400, 1600), lighting="three lights")
        p.set_background("white")
        for colour, mesh in meshes:
            edges = mesh.extract_feature_edges(feature_angle=35, boundary_edges=False,
                                               non_manifold_edges=False, manifold_edges=False)
            p.add_mesh(mesh.compute_normals(split_vertices=True, feature_angle=35), color=colour,
                       smooth_shading=True, specular=0.2, ambient=0.25, diffuse=0.8)
            if edges.n_points:
                p.add_mesh(edges, color="#15191f", line_width=1.2)
        if view == "labelled":
            p.add_point_labels(np.array([(c.X, c.Y, c.Z) for c in centres.values()]),
                               [labels[n] for n in centres], always_visible=True, font_size=26,
                               shape_color="white", shape_opacity=0.9, text_color="black",
                               show_points=False, margin=6)
        p.enable_anti_aliasing("ssaa")
        p.enable_parallel_projection()
        if angles is None:
            p.view_xy()                                    # camera above; the rear of the machine is up
        else:
            p.view_xz()                                    # camera in front, looks to the rear
            p.camera.azimuth, p.camera.elevation = angles
        p.reset_camera(bounds=(-110, 110, -110, 170, 0, 520))   # the tower; the base bars run out of view
        p.camera.zoom(1.15)
        p.screenshot(out / f"assembly_{view}.png")
        p.close()


def write(items, out):
    """Write stepper.step and stepper.glb to the folder `out`."""
    solids = []
    for name, colour, s in items:
        s.label, s.color = name, Color(colour)
        solids.append(s)
    out.mkdir(parents=True, exist_ok=True)
    asm = Compound(label="lithography stepper", children=solids)
    export_step(asm, str(out / "stepper.step"))
    export_gltf(asm, str(out / "stepper.glb"), binary=True, linear_deflection=0.1, angular_deflection=0.5)


def main():
    items = parts()
    print(f"{'part':34s} {'x':>15s} {'y':>15s} {'z':>15s}")
    for name, _, s in items:
        b = s.bounding_box()
        print(f"{name:34s} {b.min.X:7.1f}..{b.max.X:6.1f} {b.min.Y:7.1f}..{b.max.Y:6.1f} {b.min.Z:7.1f}..{b.max.Z:6.1f}")
    print(f"\ncube centre z = {CUBE_Z:.1f}   lens face z = {FACE_Z:.1f}   camera front y = {CAMERA_Y:.1f}"
          f"   SM1V10 travel used = {V10_TRAVEL:.1f} of 20.6")
    bad = collisions(items)                                 # simple models: threads do not overlap
    real = parts(real=True) if B.VENDOR_DIR.exists() else items
    if real is not items:                                   # manufacturers' models, if present
        print("second collision check, with the manufacturers' models in vendor/")
        bad += [c for c in collisions(real, skip=THREADS) if c not in bad]
    for a, b, vol in bad:
        print(f"COLLISION  {a}  /  {b}  {vol:.0f} mm3")
    print("no collisions" if not bad else f"{len(bad)} collisions")

    write(items, ROOT / "assembly" / "public")              # simple projector model: can be shared
    if real is not items:
        write(real, ROOT / "assembly" / "private")           # manufacturer's projector model: do not share
    render(real, ROOT / "docs" / "img")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
