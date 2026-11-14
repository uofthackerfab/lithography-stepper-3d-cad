"""Part 6. Main board rail: print two. Each rail holds two corner holes of the TI board (140 mm apart)."""
from .. import params as P
from ..shapes import box, cyl, frame_slots, hexagon

PRINT_ROT = (90, 0, 0)      # rail flat on the bed, standoffs up
T = 3.0                     # thin: an M5 x 8 screw is correct here


def build():
    y0 = P.FRAME_BACK
    top = y0 + T + P.BOARD_STANDOFF
    part = box(-P.BOARD_X / 2, P.BOARD_X / 2, y0, y0 + T, -7, 7)
    for x in (-P.BOARD_HOLE_X / 2, P.BOARD_HOLE_X / 2):
        part += cyl("y", 9, y0, top, x, 0)
        part -= cyl("y", P.M3_HOLE, y0, top, x, 0)
        part -= hexagon("y", y0, y0 + P.M3_NUT_T, x, 0)
    return part - frame_slots(y0, y0 + T, [0])
