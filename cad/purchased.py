"""Models of the purchased parts, for the assembly view. Dimensions in mm.

Each function makes a simple model with the correct outside dimensions.
Sources are in docs/dimensions.md.

If REAL is True and the folder vendor/ contains the CAD file of the manufacturer,
the function returns that model. real() puts it in the position of the simple model.
The folder vendor/ is not in the repository: do not share these files.
"""
from pathlib import Path

from build123d import Pos

from . import params as P
from .shapes import box, cone, cyl

VENDOR_DIR = Path(__file__).resolve().parent.parent / "vendor"
VENDOR = VENDOR_DIR / "projector.brep"
REAL = False                # assembly.py sets this
DATA = Path(__file__).resolve().parent / "data"
SM1_ID = 26.3               # bore of an SM1 tube (internal thread, major diameter)
SM1_MALE = 26.2             # male SM1 thread, drawn 0.1 small so that mated threads do not overlap


def real(key, simple, tol=1.0):
    """Return the manufacturer's model vendor/<key>.step in the position of `simple`.

    The function tries the 24 axis-aligned orientations. It keeps the orientations in which the
    bounding box is equal to that of `simple` (difference less than `tol`). Of these, it returns
    the one with the largest common volume. If the file is absent, it returns `simple`.
    """
    path = VENDOR_DIR / f"{key}.step"
    if not (REAL and path.exists()):
        return simple
    from build123d import Rot, import_step
    part, box0, best = import_step(str(path)), simple.bounding_box(), (-1, None)
    for up in (Rot(0, 0, 0), Rot(90, 0, 0), Rot(180, 0, 0), Rot(270, 0, 0), Rot(0, 90, 0), Rot(0, 270, 0)):
        for spin in (0, 90, 180, 270):
            s = up * Rot(0, 0, spin) * part
            b = s.bounding_box()
            if max(abs(b.size.X - box0.size.X), abs(b.size.Y - box0.size.Y), abs(b.size.Z - box0.size.Z)) > tol:
                continue
            s = Pos(*(box0.center() - b.center())) * s
            common = s & simple
            score = sum(c.volume for c in common) if isinstance(common, list) else (common.volume if common else 0)
            if score > best[0]:
                best = (score, s)
    if best[1] is None:
        b = part.bounding_box()
        raise ValueError(f"{key}: size {b.size.X:.1f} x {b.size.Y:.1f} x {b.size.Z:.1f} is not the size of the simple model "
                         f"{box0.size.X:.1f} x {box0.size.Y:.1f} x {box0.size.Z:.1f}")
    return best[1]


def bar(axis, a0, a1, u, v):
    """2020 extrusion along `axis` from a0 to a1; (u, v) is the centre of the section."""
    h, slot_w, slot_d = P.BAR / 2, 6.2, 6.1
    solid = box(-h, h, -h, h, a0, a1)
    for sx, sy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if sx:
            solid -= box(*sorted((sx * (h - slot_d), sx * h)), -slot_w / 2, slot_w / 2, a0, a1)
        else:
            solid -= box(-slot_w / 2, slot_w / 2, *sorted((sy * (h - slot_d), sy * h)), a0, a1)
    from build123d import Rot
    turn = {"z": Rot(0, 0, 0), "x": Rot(0, 90, 0), "y": Rot(-90, 0, 0)}[axis]
    pos = {"z": (u, v, 0), "x": (0, u, v), "y": (u, 0, v)}[axis]
    return Pos(*pos) * turn * solid


def lens_tube(length, male_up=True):
    """SM1L tube, axis z, body from 0 to `length`. The 3 mm male thread is above or below the body."""
    t0, t1 = (length, length + 3) if male_up else (-3, 0)
    simple = cyl("z", P.TUBE_OD, 0, length) + cyl("z", SM1_MALE, t0, t1) - cyl("z", SM1_ID, 0, length) - cyl("z", 23, -3, length + 3)
    return real({8.4: "SM1L03", 13.5: "SM1L05", 26.2: "SM1L10"}.get(length, ""), simple)


def sm1v10(travel):
    """Adjustable tube: collar from 0 to 13.5, male barrel above it. `travel` is the exposed barrel."""
    part = cyl("z", P.TUBE_OD, 0, 13.5) + cyl("z", SM1_MALE, 13.5, 13.5 + 25.4)
    part += cyl("z", 31.8, 13.5 + travel - 2.8, 13.5 + travel)            # lock nut
    return real("SM1V10", part - cyl("z", 22.9, 0, 13.5 + 25.4))


def sm1a53():
    """Flange plate, 35.05 square, 5.56 thick, four M3 holes on a 26 mm square."""
    h = 35.05 / 2
    part = box(-h, h, -h, h, 0, 5.56) - cyl("z", SM1_ID, 0, 5.56)
    for x in (-13, 13):
        for y in (-13, 13):
            part -= cyl("z", 3.6, 0, 5.56, x, y)
    return real("SM1A53", part)


def sm1a3():
    """RMS adapter: ring with an outer SM1 thread and an inner RMS thread, 5.08 thick, from z = 0."""
    return real("SM1A3", cyl("z", SM1_MALE, 0, 5.08) - cyl("z", 20.4, 0, 5.08))


def objective():
    """Edmund 10X DIN, #43-907. Shoulder at z = 0, tip at z = -44. RMS thread above the shoulder."""
    return real("objective", cyl("z", 20.3, 0, 3.6) + cyl("z", 24, -30, 0) + cone("z", 9, 24, -44, -30)
                - cyl("z", 6, -44, -40))


def cube():
    h = P.CUBE / 2
    return box(-h, h, -h, h, -h, h)


def camera():
    """ZWO ASI174MM. Front face of the M42 collar at y = 0, body behind it (+y)."""
    return (cyl("y", 46, 0, 4) + cyl("y", P.CAMERA_OD, 4, 4 + P.CAMERA_LEN)
            - cyl("y", 20, 0, 4))


def projector(real=False):
    """TI DLPDLCR471TPEVM light engine, lens removed. Lens face at z = 0, light hole at x = y = 0.

    Dimensions [V] from the Hacker Fab CAD model of the engine (SPEC_800-0255-A_F16D).
    real=True loads that model from vendor/projector.brep. The file is not in the repository.
    """
    if real and VENDOR.exists():
        from build123d import import_brep
        o = P.DMD_OFFSET
        engine = Pos(-23.82, 37.75 + o, -179.137) * import_brep(str(VENDOR))
        return engine - box(-22.6, 22.6, -22.72 + o, 22.7 + o, -7, 0)   # lens mount: removed with the lens
    o = P.DMD_OFFSET                                    # model origin is the centre of the M2 square
    part = box(-23.2, 23.2, -31 + o, 22.6 + o, 0, 12) - cyl("z", P.LIGHT_BORE, 0, 12)
    part += box(-42.5, 42.5, -31 + o, 27 + o, 12, 47)
    for i in range(12):                                 # heat sink
        part += box(-41, 41, -28 + o + 4.6 * i, -26.5 + o + 4.6 * i, 47, 62.3)
    return part + box(-22.5, 22.5, -29.14 + o, -27.3 + o, -P.LIP_DROP, 0)   # the lip


def led_block():
    """LED block of the projector, with heat sinks [E]. Same axes as projector().

    The CAD model of the engine does not contain it. Size from the TI figure and from photos:
    it starts at the lip, goes 37 away from the engine and 45 below the lens face.
    """
    o = P.DMD_OFFSET
    return box(-45, 45, -66 + o, -31.1 + o, -45, 47)


def main_board():
    """TI DLP046 formatter board, 150 x 125 x 1.57. Centre at the origin, bottom side at y = 0."""
    part = box(-75, 75, 0, 1.57, -62.5, 62.5)
    for x in (-70, 70):
        for z in (-57.5, 57.5):
            part -= cyl("y", 3.43, 0, 1.57, x, z)
    return part + box(-30, 0, 1.57, 12, -20, 10)                          # DLPC6540 fan and heat sink [E]


def side_board():
    """TI DLP048 front-end (HDMI) board, approximately 77 x 73 [E]. Origin between its two screw holes.

    It hangs down from the holes, bottom side at y = 0. The cable connector is at the lower edge.
    """
    return box(-38.5, 38.5, 0, 1.6, -69, 4) + box(-30, 30, 1.6, 8, -66, -8)   # board, and its parts [E]


def manipulator():
    """Open Micro-Manipulator v4 with its printed stand. Base block origin at (0, 0, 0).

    Returns {name: shape}. The shapes are the CAD of the project (MIT licence).
    cad/import_manipulator.py made the file cad/data/manipulator.brep from that CAD.
    """
    from build123d import import_brep
    names = (DATA / "manipulator.txt").read_text().split("\n")
    parts = dict(zip(names, list(import_brep(str(DATA / "manipulator.brep")))))
    path = VENDOR_DIR / "motor.step"
    if REAL and path.exists():
        # Manufacturer's model of the motor 17HM15-0904S. In its file: shaft on the z axis, front face
        # at z = 10, cable to -y. In the stage CAD: shaft of motor 1 at x = -21.5, y = 21, front face at
        # z = 36.5. Motors 2 and 3 are motor 1, turned 120 and 240 degrees about the block diagonal.
        from build123d import Axis, import_step
        motor = Pos(-21.5, 21, 26.5) * import_step(str(path))
        for k in range(3):
            parts[f"actuator {k + 1} motor"] = motor.rotate(Axis((0, 0, 0), (1, 1, 1)), 120 * k)
    return parts
