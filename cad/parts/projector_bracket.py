"""Part 3b. Projector bracket: ring that carries the adapter plate.

Two legs lie on the front faces of the uprights. The space between the legs
stays open for the beamsplitter holder. Printed upside down (ring on the bed).
"""
from .. import params as P
from ..shapes import box, cyl, frame_slots, prism_x

PRINT_ROT = (180, 0, 0)
OPENING = 56.0              # the SM1A53 flange (44.3 mm corner to corner) passes through
HALF_W = 48.0               # wider than the bars: the gussets clear the screw heads
Y_FRONT = -40.0
DROP = 47.0                 # leg length below the top face


def build():
    t, y0, y1 = P.FLANGE, P.AXIS_TO_FRAME - P.FLANGE, P.AXIS_TO_FRAME
    g = P.UPRIGHT_GAP / 2
    part = box(-HALF_W, HALF_W, Y_FRONT, y1, -t, 0)
    g += 1                                             # 1 mm clear of the beamsplitter holder
    part += box(g, HALF_W, y0, y1, -DROP, 0) + box(-HALF_W, -g, y0, y1, -DROP, 0)
    tri = [(y0, -t), (y0, -DROP), (Y_FRONT + 10, -t)]
    part += prism_x(tri, HALF_W - t, HALF_W) + prism_x(tri, -HALF_W, -HALF_W + t)
    part -= frame_slots(y0, y1, [-15, -37])
    part -= cyl("z", OPENING, -t, 0)
    b = P.PLATE_BOLT
    for x in (-b, b):
        for y in (-b, b):
            part -= cyl("z", P.M3_HOLE, -t, 0, x, y)
    return part
