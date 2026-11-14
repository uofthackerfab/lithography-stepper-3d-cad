"""Part 2. Camera clamp: block on the back faces of the uprights, and a cap.

Along y: sleeve hole, then a full ring around the camera nose (blocks light),
then an open saddle. The camera slides in the saddle to set focus. The cap locks it.
"""
from build123d import Circle, Pos, extrude

from .. import params as P
from ..shapes import box, cyl, frame_slots

BORE = P.CAMERA_OD + 0.5
Y0 = P.FRAME_BACK
Y_RING = Y0 + 31            # camera nose can start here
Y_SADDLE = Y_RING + 12
Y_END = Y_SADDLE + 40
HALF_W = 42.0
Z_BOT, Z_TOP = -37.0, 36.0
CAP_W = 14.0
CAP_Y = Y_SADDLE + 4        # front edge of the cap
SCREW_X = 37.0              # M3 x 16


def block():
    part = box(-HALF_W, HALF_W, Y0, Y_END, Z_BOT, Z_TOP)
    part += box(-HALF_W, HALF_W, Y0, Y0 + P.FLANGE, Z_BOT - 20, Z_TOP + 20)   # flange
    part -= box(-HALF_W, HALF_W, Y_SADDLE, Y_END, 0, Z_TOP)                   # open the saddle
    part -= cyl("y", P.TUBE_BORE, Y0, Y_RING)
    part -= cyl("y", BORE, Y_RING, Y_END)
    part -= frame_slots(Y0, Y0 + P.FLANGE, [Z_BOT - 10, Z_TOP + 10])
    yc = CAP_Y + CAP_W / 2
    for s in (-1, 1):
        part -= cyl("z", P.M3_HOLE, -12, 0, s * SCREW_X, yc)
        x0, x1 = sorted((s * (SCREW_X - P.M3_NUT / 2), s * HALF_W))
        part -= box(x0, x1, yc - P.M3_NUT / 2, yc + P.M3_NUT / 2, -5 - P.M3_NUT_T, -5)   # nut slot
    return part


def cap():
    r = BORE / 2
    part = Pos(0, 0, 0) * extrude(Circle(r + 4), CAP_W)
    part += box(-HALF_W, HALF_W, 1, 7, 0, CAP_W)            # ears; local y is machine z
    part -= box(-HALF_W - 1, HALF_W + 1, -r - 5, 1, 0, CAP_W)
    part -= extrude(Circle(r), CAP_W)
    for s in (-1, 1):
        part -= cyl("y", P.M3_HOLE, 1, 7, s * SCREW_X, CAP_W / 2)
    return part
