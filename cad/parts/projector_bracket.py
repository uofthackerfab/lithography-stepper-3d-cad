"""Part 3b. Projector bracket: carries the adapter plate from the rear and the right.

Two legs lie on the front faces of the uprights. A rear wall joins them above the
beamsplitter holder. The left side is open: the LED block of the projector hangs there.
The left leg is short: one heat sink of the LED block is above it.
Printed upside down (top face on the bed). The left leg needs support.
"""
from .. import params as P
from ..shapes import box, cyl, frame_slots, prism_x

PRINT_ROT = (180, 0, 0)
OPENING = 52.0              # the SM1A53 flange (49.6 mm corner to corner) passes through
HALF_W = 48.0               # wider than the bars: the gusset clears the screw heads
Y_FRONT = -40.0
DROP = 47.0                 # leg length below the top face
X_OPEN = -22.0              # no bracket to the left of this line in front of the legs (LED block)
LEG_TOP = -21.0             # top of the left leg: 9 below the heat sink (measured, +/- 1)
WALL_DROP = 39.0            # the rear wall ends 1.8 above the beamsplitter holder
SLOTS = (-15, -37)          # M5 screws, below the top face


def build():
    t, y0, y1 = P.FLANGE, P.AXIS_TO_FRAME - P.FLANGE, P.AXIS_TO_FRAME
    g = P.UPRIGHT_GAP / 2 + 1                          # 1 mm clear of the beamsplitter holder
    part = box(X_OPEN, HALF_W, Y_FRONT, y1, -t, 0)     # top plate: right, front and rear of the tube
    part += box(g, HALF_W, y0, y1, -DROP, 0)           # right leg
    part += box(-HALF_W, -g, y0, y1, -DROP, LEG_TOP)   # left leg, below the heat sink
    part += box(-g, g, y0, y1, -WALL_DROP, 0)          # rear wall: joins the left leg to the plate
    tri = [(y0, -t), (y0, -DROP), (Y_FRONT + 10, -t)]
    part += prism_x(tri, HALF_W - t, HALF_W)           # one gusset, on the right
    part -= frame_slots(y0, y1, SLOTS, xs=(P.UPRIGHT_X,))
    part -= frame_slots(y0, y1, SLOTS[1:], xs=(-P.UPRIGHT_X,))
    part -= cyl("z", OPENING, -t, 0)
    for px, py in P.PLATE_BOLTS:                       # the plate is turned 90 degrees on the bracket
        part -= cyl("z", P.M3_HOLE, -t, 0, py, -px)
    return part
