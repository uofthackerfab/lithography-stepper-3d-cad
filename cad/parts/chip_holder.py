"""Part 7. Chip holder: plate on the top face of the end effector. The chip stands 0.1 mm above the plate."""
from .. import params as P
from ..shapes import box, cone, cyl

PRINT_ROT = (0, 0, 0)
T = 4.0
SIZE = 40.0
DEPTH = 0.4                 # pocket depth; chip is 0.525


def build():
    h, c = SIZE / 2, (P.CHIP + 0.4) / 2
    floor = T - DEPTH
    part = box(-h, h, -h, h, 0, T) - box(-c, c, -c, c, floor, T)
    part -= cyl("z", 12, 0, T, 0, -h)                  # finger notch
    part -= box(-12.5, 8.8, -16, -7.5, 0, 1.0)         # a band collet of the stage is 0.5 above the end effector
    for x, y in P.EE_HOLES:                            # M3 countersunk, heads under the chip
        part -= cyl("z", P.M3_HOLE, 0, T, x, y)
        part -= cone("z", P.M3_HOLE, 6.6, floor - 1.6, floor, x, y)
    return part
