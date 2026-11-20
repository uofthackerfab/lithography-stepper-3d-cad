"""Ray diagram and first-order check of the light path. The distances come from the CAD.

Run from the repository root:  uv run --with optiland python -m optics.layout

Output: docs/img/optics_rays.png and a list of numbers on the terminal.
Tool: Optiland (open source, https://github.com/optiland/optiland).

Light path: mirror chip in the projector -> air -> beamsplitter cube -> air -> objective -> chip.
The objective is a purchased part. Its lens data is not published. The model uses a perfect lens
with the published focal length, magnification and conjugate distances.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from optiland.analysis import SpotDiagram
from optiland.materials import IdealMaterial
from optiland.optic import Optic

from cad import assembly as A
from cad import params as P
from cad import purchased as B

OUT = Path(__file__).resolve().parent.parent / "docs" / "img" / "optics_rays.png"

# --- Objective: Edmund 10X DIN Plan, #43-907 [V], Edmund data ---
F = 15.37                   # focal length
MAG = 10.0
NA = 0.25
IMAGE_DIST = 150.0          # shoulder to image, in air (DIN standard)
PARFOCAL = 45.5             # shoulder to object

# --- Light and sensors ---
UV = 0.400                  # micrometres. Lumileds L1F3-U400 [V], part number
GREEN = 0.550               # light for the camera [E]
MIRROR = 5.4e-3             # mirror pitch, DLP471TP [V]
DMD = (1920 * MIRROR, 1080 * MIRROR)
SENSOR = (11.34, 7.13)      # ZWO ASI174MM, 5.86 micrometre pixels [V]
CAMERA_PIXEL = 5.86e-3
PROJECTOR_FNO = 1.7         # light cone of the projector at the mirror chip [E]

# --- Heights from the CAD. s = distance below the mirror chip ---
DMD_Z = A.CUBE_Z + A.ARM
CHIP_S = DMD_Z - A.CHIP_TOP
SHOULDER_S = DMD_Z - A.SHOULDER
CUBE_S = DMD_Z - A.CUBE_Z - P.CUBE / 2          # top face of the cube
# A real objective is a thick lens. It has two reference planes (principal planes).
LENS_S = SHOULDER_S - IMAGE_DIST + F * (1 + MAG)          # plane for the projector side
GAP = IMAGE_DIST + PARFOCAL - F * (1 + MAG) - F * (1 + 1 / MAG)   # distance to the plane for the chip side
TO_CHIP = CHIP_S - LENS_S - GAP                             # chip-side plane to the chip

# Openings on the way down: name, top, bottom (as s), diameter
_s = lambda z: DMD_Z - z
OPENINGS = [
    ("adapter plate", _s(A.FACE_Z), _s(A.PLATE_Z), P.LIGHT_BORE),
    ("SM1A53 + SM1L10", _s(A.PLATE_Z), _s(A.PLATE_Z - 5.56 - A.L10), 23.0),
    ("SM1V10", _s(A.V10_Z + 13.5 + 25.4), _s(A.V10_Z), 22.9),
    ("holder wall", _s(A.CUBE_Z + A.SEAT), _s(A.CUBE_Z + P.CUBE / 2), P.CLEAR_APERTURE),
    ("holder wall", _s(A.CUBE_Z - P.CUBE / 2), _s(A.CUBE_Z - A.SEAT), P.CLEAR_APERTURE),
    ("SM1L03 + SM1L05", _s(A.CUBE_Z - A.SEAT), SHOULDER_S, 23.0),
    ("SM1A3 (RMS thread)", SHOULDER_S - 5.08, SHOULDER_S, 20.1),
]


def system(wavelength=UV, field=DMD, arm_error=0.0, picture=False):
    """The light path as an Optiland model. `arm_error` moves the mirror chip away from the cube.

    With `picture`, the model has the 9.5 mm between the two principal planes of the objective,
    so that each part is at its CAD position. The numbers do not use this.
    """
    half_diagonal = (field[0] ** 2 + field[1] ** 2) ** 0.5 / 2
    o = Optic()
    add = o.surfaces.add
    add(index=0, thickness=CUBE_S + arm_error, comment="mirror chip")
    add(index=1, thickness=P.CUBE, material="N-BK7", comment="cube, top face")
    add(index=2, thickness=LENS_S - CUBE_S - P.CUBE, comment="cube, bottom face")
    add(index=3, surface_type="paraxial", f=F, thickness=0.0 if picture else TO_CHIP, is_stop=True,
        comment="objective, perfect lens")
    if picture:
        # Rays go parallel to the axis between the principal planes. A very high index gives this.
        add(index=4, thickness=GAP, material=IdealMaterial(n=1e4), comment="objective, not modelled")
        add(index=5, thickness=TO_CHIP, comment="objective, chip side")
    add(index=6 if picture else 4, comment="chip")
    o.set_aperture("objectNA", NA / MAG)
    o.fields.set_type("object_height")
    for y in (-half_diagonal, 0.0, half_diagonal):
        o.fields.add(y=y)
    o.wavelengths.add(wavelength, is_primary=True)
    return o


def focus_error(o):
    """Paraxial focus minus chip surface, in micrometres. Positive: the focus is below the chip surface."""
    y, u = o.paraxial.marginal_ray()
    return float(-y[3, 0] / u[3, 0] - TO_CHIP) * 1000


def cube_blur():
    """RMS radius of the ray spot at best focus, worst field, in micrometres. The lens is perfect: the cube is the cause."""
    o = system()
    o.updater.image_solve()
    return max(float(r[0]) for r in SpotDiagram(o).rms_spot_radius()) * 1000


def beam_half_width(o, s):
    """Largest distance of a ray from the axis at s. Uses the corner of the field."""
    o.trace_generic(0.0, 1.0, 0.0, 1.0, o.primary_wavelength)
    ys, zs = o.surfaces.y[:, 0], o.surfaces.z[:, 0]
    zs = zs - zs[0]
    for i in range(len(zs) - 1):
        if zs[i] <= s <= zs[i + 1] and zs[i + 1] > zs[i]:
            return abs(float(ys[i] + (ys[i + 1] - ys[i]) * (s - zs[i]) / (zs[i + 1] - zs[i])))
    raise ValueError(s)


def report():
    o = system()
    mag = abs(float(o.paraxial.magnification()))
    lines = []
    say = lambda name, value: lines.append(f"{name:<52}{value}")

    say("Reduction, mirror chip to chip", f"{1 / mag:.2f} X")
    say("One mirror on the chip", f"{MIRROR * mag * 1000:.2f} um")
    say("Projector image on the chip", f"{DMD[0] * mag:.2f} x {DMD[1] * mag:.2f} mm")
    say("Camera view of the chip", f"{SENSOR[0] * mag:.2f} x {SENSOR[1] * mag:.2f} mm")
    say("One mirror on the camera, in camera pixels", f"{MIRROR / CAMERA_PIXEL:.2f}")
    say("Smallest line, 0.61 x wavelength / NA", f"{0.61 * UV / NA:.2f} um = {0.61 * UV / NA / (MIRROR * mag * 1000):.1f} mirrors")
    dof = UV / (2 * NA ** 2)
    say("Depth of focus at the chip", f"+/- {dof:.1f} um")

    e_uv, e_green = focus_error(o), focus_error(system(GREEN))
    say("Focus error of the CAD distances, UV", f"{e_uv:+.1f} um")
    say("Focus difference, green to UV, cube only", f"{e_green - e_uv:+.1f} um")
    per_mm = focus_error(system(arm_error=1.0)) - e_uv
    say("Focus movement for 1 mm of arm length", f"{per_mm:+.1f} um")
    say("Arm length error that uses all the depth of focus", f"+/- {abs(dof / per_mm):.2f} mm")

    say("Blur from the cube glass, at best focus", f"{cube_blur():.3f} um (diffraction: {0.61 * UV / NA:.2f} um)")

    say("Light that the objective accepts [E]", f"{(NA / MAG * 2 * PROJECTOR_FNO) ** 2 * 100:.1f} %")

    lines.append("")
    lines.append(f"{'Opening':<22}{'radius':>8}{'beam':>8}{'margin':>8}   (projector image, corner of the field)")
    for name, s0, s1, d in OPENINGS:
        beam = max(beam_half_width(o, s0), beam_half_width(o, s1))
        lines.append(f"{name:<22}{d / 2:>8.1f}{beam:>8.1f}{d / 2 - beam:>8.1f}")
    beam = max(beam_half_width(o, s) for _, s0, s1, _ in OPENINGS for s in (s0, s1))
    lines.append(f"{'baffle ring (optional)':<22}{9.0:>8.1f}{beam:>8.1f}{9.0 - beam:>8.1f}")
    cam = system(GREEN, SENSOR)
    beam = max(beam_half_width(cam, s) for s in (0.0, CUBE_S))
    lines.append(f"{'camera arm':<22}{P.CLEAR_APERTURE / 2:>8.1f}{beam:>8.1f}{P.CLEAR_APERTURE / 2 - beam:>8.1f}")
    return "\n".join(lines)


def draw():
    o = system(picture=True)
    fig, ax = plt.subplots(figsize=(13, 4.4))
    o.draw(num_rays=5, ax=ax, show=False)
    x = lambda s: s - CUBE_S            # Optiland puts zero at the first surface after the object
    wall = dict(facecolor="0.55", edgecolor="none", zorder=3)
    for name, s0, s1, d in OPENINGS:
        for sign in (1, -1):
            ax.add_patch(Rectangle((x(s0), sign * d / 2), s1 - s0, sign * (16 - d / 2), **wall))
    tip = SHOULDER_S + 44.0             # objective body: 24 diameter, then a cone to the tip
    for sign in (1, -1):
        ax.add_patch(Rectangle((x(SHOULDER_S), sign * 8), 30, sign * 4, **wall))
        ax.add_patch(plt.Polygon([(x(SHOULDER_S + 30), sign * 8), (x(SHOULDER_S + 30), sign * 12),
                                  (x(tip), sign * 4.5), (x(tip), sign * 3)], **wall))
    ax.add_patch(Rectangle((x(CHIP_S), -16), 0.7, 32, facecolor="tab:purple", edgecolor="none", zorder=3))
    diagonal = (DMD[0] ** 2 + DMD[1] ** 2) ** 0.5
    ax.add_patch(Rectangle((x(0) - 1.2, -diagonal / 2), 1.2, diagonal, facecolor="k", edgecolor="none", zorder=3))
    ax.add_patch(Rectangle((x(CUBE_S), -P.CUBE / 2), P.CUBE, P.CUBE, facecolor="tab:cyan", alpha=0.15, edgecolor="0.4", zorder=1))
    ax.axvline(x(_s(A.FACE_Z)), color="0.4", ls=":", lw=1)

    labels = [
        (0, "mirror chip\n(in the projector)"), (_s(A.FACE_Z), "lens face of\nthe projector"),
        (_s(A.PLATE_Z) + 17, "SM1L10"), (_s(A.V10_Z) - 17, "SM1V10\n(sets this length)"),
        (CUBE_S + 15, "beamsplitter\ncube"), (SHOULDER_S - 12, "SM1L03\nSM1L05"),
        (SHOULDER_S + 22, "objective"), (CHIP_S, "chip"),
    ]
    for s, text in labels:
        ax.text(x(s), 18, text, ha="center", va="bottom", fontsize=9)
    ax.text(x(CUBE_S + 15), -18, "the camera arm goes\nto the rear from here", ha="center", va="top", fontsize=9)
    ticks = range(0, int(CHIP_S) + 1, 20)
    ax.set_xticks([x(t) for t in ticks], [str(t) for t in ticks])
    ax.set_xlim(x(-10), x(CHIP_S + 10))
    ax.set_ylim(-27, 29)
    ax.set_aspect("equal")
    ax.set_xlabel("Distance below the mirror chip [mm]. The real path is vertical: left is up.")
    ax.set_ylabel("Distance from the axis [mm]")
    ax.set_title("")
    fig.tight_layout()
    fig.savefig(OUT, dpi=150)
    return OUT


if __name__ == "__main__":
    print(report())
    print(f"\npicture: {draw().relative_to(OUT.parent.parent.parent)}")
