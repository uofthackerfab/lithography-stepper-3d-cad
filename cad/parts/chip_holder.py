"""Part 7. Chip holder: plate on the top face of the end effector. The chip stands 0.1 mm above the plate."""
from .. import params as P
from ..shapes import box, cone, cyl

PRINT_ROT = (0, 0, 0)
T = 4.0
SIZE = 40.0
DEPTH = 0.4                 # pocket depth; chip is 0.525


def build():
    h, c = SIZE / 2, (P.CHIP + 0.2) / 2
    floor = T - DEPTH
    part = box(-h, h, -h, h, 0, T) - box(-c, c, -c, c, floor, T)
    part -= cyl("z", 12, 0, T, 0, -h)                  # finger notch
    for x, y in P.EE_HOLES:                            # M3 countersunk, heads under the chip
        part -= cyl("z", P.M3_HOLE, 0, T, x, y)
        part -= cone("z", P.M3_HOLE, 6.6, floor - 1.6, floor, x, y)
    return part
