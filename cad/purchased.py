"""Simple models of the purchased parts, for the assembly view. Dimensions in mm.

Each model has the correct outside dimensions. Small details are omitted.
Sources are in docs/dimensions.md.
"""
from pathlib import Path

from build123d import Pos

from . import params as P
from .shapes import box, cone, cyl

VENDOR = Path(__file__).resolve().parent.parent / "vendor" / "projector.brep"
SM1_ID = 26.3               # bore of an SM1 tube (internal thread, major diameter)
SM1_MALE = 26.2             # male SM1 thread, drawn 0.1 small so that mated threads do not overlap


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
    return cyl("z", P.TUBE_OD, 0, length) + cyl("z", SM1_MALE, t0, t1) - cyl("z", SM1_ID, 0, length) - cyl("z", 23, -3, length + 3)


def sm1v10(travel):
    """Adjustable tube: collar from 0 to 13.5, male barrel above it. `travel` is the exposed barrel."""
    part = cyl("z", P.TUBE_OD, 0, 13.5) + cyl("z", SM1_MALE, 13.5, 13.5 + 25.4)
    part += cyl("z", 31.8, 13.5 + travel - 2.8, 13.5 + travel)            # lock nut
    return part - cyl("z", 22.9, 0, 13.5 + 25.4)


def sm1a53():
    """Flange plate, 35.05 square, 5.56 thick, four M3 holes on a 26 mm square."""
    h = 35.05 / 2
    part = box(-h, h, -h, h, 0, 5.56) - cyl("z", SM1_ID, 0, 5.56)
    for x in (-13, 13):
        for y in (-13, 13):
            part -= cyl("z", 3.6, 0, 5.56, x, y)
    return part


def objective():
    """Edmund 10X DIN, #43-907. Shoulder at z = 0, tip at z = -44. RMS thread above the shoulder."""
    return (cyl("z", 20.3, 0, 4.5) + cyl("z", 24, -30, 0) + cone("z", 9, 24, -44, -30)
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


def main_board():
    """TI DLP046 formatter board, 150 x 125 x 1.57. Centre at the origin, bottom side at y = 0."""
    part = box(-75, 75, 0, 1.57, -62.5, 62.5)
    for x in (-70, 70):
        for z in (-57.5, 57.5):
            part -= cyl("y", 3.43, 0, 1.57, x, z)
    return part + box(-30, 0, 1.57, 12, -20, 10)                          # DLPC6540 fan and heat sink [E]


def _turn(b):
    """Turn a box about the diagonal of the base block: (x, y, z) -> (y, z, x)."""
    return b[2:] + b[:2]


def manipulator():
    """Open Micro-Manipulator v4 with its printed stand, simplified. Base block origin at (0, 0, 0).

    Returns {name: solid}. Positions are from the STL files. Rods, horns and wires are omitted.
    The three motors and their mounts are the same shape, turned about the block diagonal.
    """
    m, L, h = 42.3 / 2, 39.0, 34.5
    mount = [(-42.5, -30.5, -11.5, 50, h, h + 7),       # three boxes follow the outline of MotorMount.stl
             (-30.5, -7.5, -11.5, 10, h, h + 7),
             (-10.5, 25, 0, 25, h, h + 7)]
    motor = [(-21.5 - m, -21.5 + m, 21 - m, 21 + m, h - L, h)]
    out = {"base block": box(0, h, 0, h, 0, h) - box(25, h, 25, h, 25, h),
           "end effector": box(33, 62, 33, 62, 33, 62)}
    for axis in "ZYX":
        for name, boxes in (("motor mount", mount), ("motor", motor)):
            solid = None
            for b in boxes:
                solid = box(*b) if solid is None else solid + box(*b)
            out[f"{name} {axis}"] = solid
        mount, motor = [_turn(b) for b in mount], [_turn(b) for b in motor]
    out["stand"] = (box(-50.35, 50.65, -50, 50, -65.6, -61.6)
                    + box(-50.35, -43.2, -11.5, 50, -61.6, h)
                    + box(-50.35, -25.35, 43, 50, -61.6, h))
    return out
