"""Part 9. Side board holder: holds the TI front-end (HDMI) board above the main board.

A strip on the back faces of the uprights. The board hangs down from two M3 screws.
These are two of its four corner holes (68.58 mm apart). The slots give +/- 3 mm.
"""
from .. import params as P
from ..shapes import box, frame_slots, slot

PRINT_ROT = (90, 0, 0)      # strip flat on the bed, standoffs up
T = 3.0                     # thin: an M5 x 8 screw is correct here
HOLE_X = 68.58              # distance of the board holes [V], TI drill file DLP048B (2.700 inch)
TRAVEL = 3.0                # each slot: +/- 3
Z_M5 = -16.0                # frame screws, below the board screws


def build():
    y0 = P.FRAME_BACK
    top = y0 + T + P.BOARD_STANDOFF
    part = box(-45, 45, y0, y0 + T, -23, 7)
    for side in (-1, 1):
        x = side * HOLE_X / 2
        part += box(x - TRAVEL - 4.5, x + TRAVEL + 4.5, y0, top, -4.5, 4.5)
        part -= slot("y", "x", P.M3_HOLE, TRAVEL, y0, top, x, 0)
        # The nut lies between the strip and the upright. The slot walls stop it from turning.
        part -= box(x - TRAVEL - 3.5, x + TRAVEL + 3.5, y0, y0 + P.M3_NUT_T, -P.M3_NUT / 2, P.M3_NUT / 2)
    return part - frame_slots(y0, y0 + T, [Z_M5])
