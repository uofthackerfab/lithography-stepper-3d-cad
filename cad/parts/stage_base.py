"""Part 8. Stage base: flat plate on the table that locates the micro-manipulator stand.

The stand is demoStandV1.stl from the koalazak fork (101 x 100 mm foot, no holes).
It sits in the rim. The flange bolts to the front face of the base bar below the uprights.
With the stand in the rim, the centre of the end effector is on the optical axis.
"""
from .. import params as P
from ..shapes import box, slot

PRINT_ROT = (0, 0, 0)
T = 3.0
RIM = 3.0
FIT = 0.4                   # clearance around the stand foot
# Stand foot, measured from the end effector centre [V], from the STL files.
X0, X1 = -97.85, 3.15
Y0, Y1 = -97.5, 2.5


def build():
    x0, x1, y0, y1 = X0 - FIT, X1 + FIT, Y0 - FIT, Y1 + FIT
    yf = P.AXIS_TO_FRAME
    part = box(x0 - RIM, x1 + RIM, y0 - RIM, yf, 0, T)
    part += box(x0 - RIM, x1 + RIM, y0 - RIM, y1 + RIM, T, T + RIM) - box(x0, x1, y0, y1, T, T + RIM)
    part += box(x0 - RIM, x1 + RIM, yf - P.FLANGE, yf, 0, P.BAR)
    for x in (-80, -15):
        part -= slot("y", "x", P.M5_HOLE, P.M5_TRAVEL, yf - P.FLANGE, yf, x, P.BAR / 2)
    return part
