"""Part 4. Tube clamp: split ring with one M3 pinch screw. Bolts across both uprights."""
from build123d import Circle, Pos, extrude

from .. import params as P
from ..shapes import box, cyl, frame_slots, hexagon, prism_z

PRINT_ROT = (0, 0, 0)
H = 10.0                    # the objective tube has 12 mm free below the holder


def build():
    ro = P.TUBE_BORE / 2 + 5
    y0, y1 = P.AXIS_TO_FRAME - P.FLANGE, P.AXIS_TO_FRAME
    part = extrude(Circle(ro), H)
    part += box(-8, 8, -ro - 9, -ro + 3, 0, H)                       # ears
    part += prism_z([(-14, 10), (14, 10), (30, y0), (-30, y0)], 0, H)  # arm
    part += box(-P.UPRIGHT_X - 10, P.UPRIGHT_X + 10, y0, y1, 0, H)   # flange
    part -= cyl("z", P.TUBE_BORE, 0, H)
    part -= box(-1, 1, -ro - 9, 0, 0, H)                             # slit
    yp = -ro - 4.5
    part -= cyl("x", P.M3_HOLE, -8, 8, yp, H / 2)
    part -= hexagon("x", -8, -8 + P.M3_NUT_T, yp, H / 2)
    part -= frame_slots(y0, y1, [H / 2])
    return part
