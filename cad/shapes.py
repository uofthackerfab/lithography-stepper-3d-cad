"""Small helpers. Every shape is given by its limits in x, y, z (mm)."""
from build123d import (Align, Box, Cone, Cylinder, Plane, Polygon, Pos,
                       RegularPolygon, Rot, extrude)

from . import params as P

_TURN = {"x": Rot(0, 90, 0), "y": Rot(-90, 0, 0), "z": Rot(0, 0, 0)}


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _place(axis, a0, a1, u, v, solid):
    """Put a z-axis solid along `axis` from a0 to a1; (u, v) are the other two coordinates."""
    mid = (a0 + a1) / 2
    pos = {"x": (mid, u, v), "y": (u, mid, v), "z": (u, v, mid)}[axis]
    return Pos(*pos) * _TURN[axis] * solid


def cyl(axis, d, a0, a1, u=0, v=0):
    return _place(axis, a0, a1, u, v, Cylinder(d / 2, a1 - a0))


def hexagon(axis, a0, a1, u=0, v=0, af=P.M3_NUT):
    h = a1 - a0
    prism = Pos(0, 0, -h / 2) * extrude(RegularPolygon(af / 2, 6, major_radius=False), h)
    return _place(axis, a0, a1, u, v, prism)


def slot(axis, along, d, travel, a0, a1, u=0, v=0):
    """A hole along `axis`, made longer by +/- travel in the direction `along`."""
    shift = {"x": (travel, 0, 0), "y": (0, travel, 0), "z": (0, 0, travel)}[along]
    hole = cyl(axis, d, a0, a1, u, v)
    bb = hole.bounding_box()
    lo, hi = [bb.min.X, bb.min.Y, bb.min.Z], [bb.max.X, bb.max.Y, bb.max.Z]
    i = "xyz".index(along)
    lo[i] += d / 2 - travel
    hi[i] -= d / 2 - travel
    mid = box(lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])
    return Pos(*shift) * hole + Pos(*[-s for s in shift]) * hole + mid


def cone(axis, d0, d1, a0, a1, u=0, v=0):
    """Diameter d0 at a0, d1 at a1."""
    return _place(axis, a0, a1, u, v, Cone(d0 / 2, d1 / 2, a1 - a0))


def prism_x(points_yz, x0, x1):
    """Polygon given in (y, z), extruded from x0 to x1."""
    solid = extrude(Plane.YZ * Polygon(*points_yz, align=None), x1 - x0)
    return Pos(x0 - solid.bounding_box().min.X, 0, 0) * solid


def prism_z(points_xy, z0, z1):
    solid = extrude(Polygon(*points_xy, align=None), z1 - z0)
    return Pos(0, 0, z0 - solid.bounding_box().min.Z) * solid


def frame_slots(y0, y1, zs, xs=(-P.UPRIGHT_X, P.UPRIGHT_X)):
    """M5 slots through a plate that lies on the upright faces (plate normal = y)."""
    out = None
    for x in xs:
        for z in zs:
            s = slot("y", "x", P.M5_HOLE, P.M5_TRAVEL, y0, y1, x, z)
            out = s if out is None else out + s
    return out
