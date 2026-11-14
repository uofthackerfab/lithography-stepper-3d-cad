"""Part 3b. Projector bracket: ring that carries the adapter plate, bolted across both uprights."""
from .. import params as P
from ..shapes import cyl
from .shelf import PRINT_ROT, shelf  # noqa: F401

OPENING = 56.0              # the SM1A53 flange (44.3 mm corner to corner) passes through


def build():
    part = shelf(48, -40, 47, [-15, -37])
    part -= cyl("z", OPENING, -P.FLANGE, 0)
    b = P.PLATE_BOLT
    for x in (-b, b):
        for y in (-b, b):
            part -= cyl("z", P.M3_HOLE, -P.FLANGE, 0, x, y)
    return part
