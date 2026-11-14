"""Part 8. Stage platform: flat table for the micro-manipulator, with M3 slots. Slide it on the uprights for height."""
from .. import params as P
from ..shapes import slot
from .shelf import PRINT_ROT, shelf  # noqa: F401


def build():
    part = shelf(60, -70, 57, [-15, -45])
    for x in (-30, -15, 0, 15, 30):
        for y in (-55, -25, 5):
            part -= slot("z", "y", P.M3_HOLE, 8, -P.FLANGE, 0, x, y)
    return part
