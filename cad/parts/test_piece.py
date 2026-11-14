"""Part 0 (optional). Test piece: shows how accurate the printer is.

Three tube holes, one 30.3 mm square for the cube, one M5 hole, one M3 nut pocket.
"""
from .. import params as P
from ..shapes import box, cyl, hexagon

PRINT_ROT = (0, 0, 0)
BORES = (30.6, 30.7, 30.8)   # marked with 1, 2, 3 notches
POCKET = 30.3
T = 8.0


def build():
    part = box(0, 165, 0, 44, 0, T)
    for i, d in enumerate(BORES):
        x = 22 + 36 * i
        part -= cyl("z", d, 0, T, x, 22)
        for n in range(i + 1):
            part -= cyl("z", 2, 0, T, x - 3 * i / 2 + 3 * n, 0)
    part -= box(130 - POCKET / 2, 130 + POCKET / 2, 22 - POCKET / 2, 22 + POCKET / 2, 0, T)
    part -= cyl("z", P.M5_HOLE, 0, T, 157, 11)
    part -= cyl("z", P.M3_HOLE, 0, T, 157, 31)
    part -= hexagon("z", T - P.M3_NUT_T, T, 157, 31)
    return part
