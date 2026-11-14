"""Part 5. Baffle ring (optional): drops into an SM1 tube. Sizes are the user's estimates."""
from ..shapes import cyl

PRINT_ROT = (0, 0, 0)


def build():
    return cyl("z", 25.2, 0, 1.5) - cyl("z", 18, 0, 1.5)
