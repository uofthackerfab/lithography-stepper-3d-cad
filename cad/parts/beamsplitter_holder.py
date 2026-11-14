"""Part 1. Beamsplitter holder: two halves that close around the cube and three tubes.

The split plane contains both tube axes. Base half: x < 0, bolts to the inner
face of the left upright. Cover half: x > 0.
Top and bottom holes: projector tube and objective tube. Back hole (+y): camera sleeve.
Front (-y): closed light trap with an angled back wall.
"""
from .. import params as P
from ..shapes import box, cyl, hexagon, prism_x, slot

HX = P.UPRIGHT_GAP / 2      # 22: thickness of each half
HZ = 30.0                   # half height
LIP = 2.0                   # wall between the cube and each tube end
Y_FRONT = -44.0
Y_COVER = 50.0
SCREWS = [(y, z) for y in (-39.5, -21.5, 21.5, 42.0) for z in (-23.0, 23.0)]   # M3 x 20
M5_Z = (-22.5, 22.5)
M5_Y = P.AXIS_TO_FRAME + P.BAR / 2
GRIP = 8.0                  # plastic under each M3 head and nut


def _cavity():
    c = P.CUBE_POCKET / 2
    seat = c + LIP
    cut = box(-c - 0.35, c + 0.35, -c, c, -c, c + 0.3)        # cube, plus felt on the x faces
    cut += cyl("z", P.CLEAR_APERTURE, -seat, seat)
    cut += cyl("z", P.TUBE_BORE, seat, HZ) + cyl("z", P.TUBE_BORE, -HZ, -seat)
    cut += cyl("y", P.CLEAR_APERTURE, -seat, seat)
    cut += cyl("y", P.TUBE_BORE, seat, P.FRAME_BACK)
    cut += prism_x([(-seat, -13), (-seat, 13), (-40, 13), (-32, -13)], -13, 13)   # light trap
    return cut


def base():
    part = box(-HX, 0, Y_FRONT, P.FRAME_BACK, -HZ, HZ) - _cavity()
    for y, z in SCREWS:
        part -= cyl("x", P.M3_HOLE, -HX, 0, y, z)
        part -= hexagon("x", -HX, -GRIP, y, z)
    for z in M5_Z:                                            # M5 x 12 into the upright
        part -= slot("x", "y", P.M5_HOLE, P.M5_TRAVEL, -HX, 0, M5_Y, z)
        part -= slot("x", "y", P.M5_HEAD, P.M5_TRAVEL, -HX + P.FLANGE, 0, M5_Y, z)
    return part


def cover():
    part = box(0, HX, Y_FRONT, Y_COVER, -HZ, HZ) - _cavity()
    for y, z in SCREWS:
        part -= cyl("x", P.M3_HOLE, 0, HX, y, z)
        part -= cyl("x", P.M3_HEAD, GRIP, HX, y, z)
    return part
