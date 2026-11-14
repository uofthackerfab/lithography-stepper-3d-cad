"""Part 3a. Adapter plate: projector lens face on top, SM1A53 flange below.

The plate centre is the optical axis. The M2 square is 2.9 mm off centre, so
the tube sits on the mirror chip. Turn the plate in 90 degree steps on the
projector, and on the bracket, until both are correct.
"""
from .. import params as P
from ..shapes import box, cone, cyl, hexagon

PRINT_ROT = (180, 0, 0)     # countersinks face up on the printer
T = 6.0
BRACKET_NUT = 4.0           # deep pockets: M3 x 12 screws stay below the top face


def build():
    h = P.PLATE / 2
    part = box(-h, h, -h, h, 0, T) - cyl("z", P.LIGHT_BORE, 0, T)
    a = P.M2_SQUARE / 2
    for x in (-a, a):                                   # M2 countersunk, heads on the bottom
        for y in (-a, a):
            part -= cyl("z", P.M2_HOLE, 0, T, x, y + P.DMD_OFFSET)
            part -= cone("z", P.M2_CSK, P.M2_HOLE, 0, (P.M2_CSK - P.M2_HOLE) / 2, x, y + P.DMD_OFFSET)
    r, b = P.SM1A53_BOLT_R, P.PLATE_BOLT
    for x, y, depth in [(r, 0, P.M3_NUT_T), (-r, 0, P.M3_NUT_T), (0, r, P.M3_NUT_T), (0, -r, P.M3_NUT_T),
                        (b, b, BRACKET_NUT), (b, -b, BRACKET_NUT), (-b, b, BRACKET_NUT), (-b, -b, BRACKET_NUT)]:
        part -= cyl("z", P.M3_HOLE, 0, T, x, y)
        part -= hexagon("z", T - depth, T, x, y)        # nuts on the projector side
    return part
