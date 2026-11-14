"""Light sleeve between the beamsplitter holder and the camera clamp. Same diameter as an SM1 tube."""
from .. import params as P
from ..shapes import cyl

PRINT_ROT = (0, 0, 0)
LENGTH = 78.0


def build():
    return cyl("z", P.TUBE_OD, 0, LENGTH) - cyl("z", 26, 0, LENGTH)
