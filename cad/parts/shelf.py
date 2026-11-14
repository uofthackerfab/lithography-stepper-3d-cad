"""Shared shape: a horizontal plate with two legs and two gussets below it.

The legs lie on the front faces of the uprights. The space between the legs
stays open for the beamsplitter holder.

Printed upside down (plate on the bed). Used by the projector bracket and the stage platform.
"""
from .. import params as P
from ..shapes import box, frame_slots, prism_x

PRINT_ROT = (180, 0, 0)


def shelf(half_w, y_front, drop, slot_zs):
    t, y0, y1 = P.FLANGE, P.AXIS_TO_FRAME - P.FLANGE, P.AXIS_TO_FRAME
    fx = P.UPRIGHT_X + 16                              # legs are wider than the bars: gussets clear the screw heads
    part = box(-half_w, half_w, y_front, y1, -t, 0)
    part += box(P.UPRIGHT_GAP / 2, fx, y0, y1, -drop, 0) + box(-fx, -P.UPRIGHT_GAP / 2, y0, y1, -drop, 0)
    tri = [(y0, -t), (y0, -drop), (y_front + 10, -t)]
    part += prism_x(tri, fx - t, fx) + prism_x(tri, -fx, -fx + t)
    return part - frame_slots(y0, y1, slot_zs)
