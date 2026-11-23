"""Parts 10 and 11. Printed substitutes for two boards of the Open Micro-Manipulator.

Part 10, ball joint plate: 20 x 8 x 1.6. Six in the stage (two for each arm).
Part 11, ball alignment disc: diameter 8 x 1.6. Two in the rod press tool.

Dimensions [V] from the order files of the project (balljoint_plate_pcb_jlcpcb.zip,
ball_alignment_disc_pcb.zip): outline and drill files. Origin: centre of the outline.
The seat and pin holes have their nominal size. A printed hole is smaller: open each
hole with a drill bit of the nominal size.
"""
from build123d import Polygon, Pos, extrude, fillet

from ..shapes import cyl

T = 1.6                     # board thickness
SEAT = 0.8                  # seat for a 1 mm ball
SEAT_X = 8.5                # the two seats are 17 mm apart
CORD = 1.2                  # elastic cord holes (1.0 in the board; the size is not important)
PIN = 2.0                   # M2 dowel pins and screws
BATCH_PITCH = (24.0, 12.0)  # distance between parts in a batch file


def plate():
    pts = [(-10, 4), (10, 4), (10, -1.5), (7.5, -4), (-7.5, -4), (-10, -1.5)]
    outline = Polygon(*pts, align=None)
    part = extrude(fillet(outline.vertices(), 1.0), T)
    part = Pos(0, 0, -part.bounding_box().min.Z) * part      # bottom face at z = 0
    for sx in (-1, 1):
        part -= cyl("z", SEAT, 0, T, sx * SEAT_X, 1.0)
        for y in (2.75, -0.75):
            part -= cyl("z", CORD, 0, T, sx * SEAT_X, y)
        for y in (1.0, -2.0):
            part -= cyl("z", PIN, 0, T, sx * 4.75, y)
    return part


def disc():
    return cyl("z", 8.0, 0, T) - cyl("z", 1.0, 0, T)


def _batch(builder, nx, ny, pitch):
    """nx x ny copies with the same orientation. Print them in one job."""
    out = None
    for i in range(nx):
        for j in range(ny):
            p = Pos(i * pitch[0], j * pitch[1], 0) * builder()
            out = p if out is None else out + p
    return out


def plates_x8():
    return _batch(plate, 2, 4, BATCH_PITCH)


def discs_x4():
    return _batch(disc, 2, 2, (12.0, 12.0))
