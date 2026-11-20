"""Part 3b. Projector bracket: carries the adapter plate from the rear and the left.

Two legs lie on the front faces of the uprights. The space between the legs
stays open for the beamsplitter holder. The right side is open: the LED block
of the projector hangs there. Printed upside down (top face on the bed).
"""
from .. import params as P
from ..shapes import box, cyl, frame_slots, prism_x

PRINT_ROT = (180, 0, 0)
OPENING = 52.0              # the SM1A53 flange (49.6 mm corner to corner) passes through
HALF_W = 48.0               # wider than the bars: the gusset clears the screw heads
Y_FRONT = -40.0
DROP = 47.0                 # leg length below the top face
X_OPEN = 22.0               # no bracket to the right of this line in front of the legs (LED block)


def build():
    t, y0, y1 = P.FLANGE, P.AXIS_TO_FRAME - P.FLANGE, P.AXIS_TO_FRAME
    g = P.UPRIGHT_GAP / 2 + 1                          # 1 mm clear of the beamsplitter holder
    part = box(-HALF_W, X_OPEN, Y_FRONT, y1, -t, 0)    # top plate: left, front and rear of the tube
    part += box(X_OPEN, HALF_W, y0, y1, -t, 0)         # rear strip to the right leg
    part += box(g, HALF_W, y0, y1, -DROP, 0) + box(-HALF_W, -g, y0, y1, -DROP, 0)
    tri = [(y0, -t), (y0, -DROP), (Y_FRONT + 10, -t)]
    part += prism_x(tri, -HALF_W, -HALF_W + t)         # one gusset, on the left
    part -= frame_slots(y0, y1, [-15, -37])
    part -= cyl("z", OPENING, -t, 0)
    for px, py in P.PLATE_BOLTS:                       # the plate is turned 90 degrees on the bracket
        part -= cyl("z", P.M3_HOLE, -t, 0, -py, px)
    return part
