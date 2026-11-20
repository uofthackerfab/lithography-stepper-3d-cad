"""Short simulations of the image on the chip. Each one shows one effect.

Run from the repository root:  uv run --with optiland python -m optics.simulate

Output: docs/img/optics_sim_*.png

Method (Fourier optics): the objective passes only the fine detail that its opening (NA) permits.
The light on the chip is the pattern, blurred by the image of one point (the Airy pattern).
The objective is a perfect lens here. A real objective is not better than this.
The projector lights the mirror chip from many directions, thus the model adds intensities (incoherent light).
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.special import j1

from .layout import MAG, MIRROR, NA, UV

OUT = Path(__file__).resolve().parent.parent / "docs" / "img"
PIXEL = MIRROR / MAG * 1000         # one mirror on the chip, micrometres (0.54)
SUB = 8                             # samples for each mirror
DX = PIXEL / SUB
N = 1024                            # the grid is 128 x 128 mirrors
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]      # series colours, fixed order
INK, MUTED, SURFACE = "#0b0b0b", "#52514e", "#fcfcfb"
plt.rcParams.update({"figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "axes.edgecolor": MUTED,
                     "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "text.color": INK,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
                     "grid.color": "#e4e3df", "grid.linewidth": 0.6, "font.size": 10, "lines.linewidth": 2})


def psf(defocus=0.0, wavelength=UV, na=NA):
    """Image of one point of light on the chip. `defocus` in micrometres. The sum is 1."""
    f = np.fft.fftfreq(N, DX)
    sin2 = (wavelength ** 2) * (f[:, None] ** 2 + f[None, :] ** 2)      # sin^2 of the ray angle
    inside = sin2 <= na ** 2
    phase = 2 * np.pi / wavelength * defocus * (np.sqrt(1 - np.where(inside, sin2, 0)) - 1)
    p = np.abs(np.fft.ifft2(inside * np.exp(1j * phase))) ** 2
    return p / p.sum()


def image(pattern, defocus=0.0):
    """Light on the chip for a pattern of 0 (dark) and 1 (bright). A large bright area gives 1."""
    return np.real(np.fft.ifft2(np.fft.fft2(pattern) * np.fft.fft2(psf(defocus))))


def mirrors(cells):
    """Put a small array (one value for each mirror) in the centre of the grid."""
    cells = np.kron(np.asarray(cells, float), np.ones((SUB, SUB)))
    grid = np.zeros((N, N))
    r0, c0 = (N - cells.shape[0]) // 2, (N - cells.shape[1]) // 2
    grid[r0:r0 + cells.shape[0], c0:c0 + cells.shape[1]] = cells
    return grid


def lines(width, count=5, length=40):
    """`count` bright lines, each `width` mirrors wide, with equal dark spaces."""
    row = ([1] * width + [0] * width) * count
    return mirrors(np.tile(row[:-width], (length, 1)))


def axis(n=N):
    return (np.arange(n) - n / 2) * DX


def contrast(width, defocus=0.0):
    """(max - min) / (max + min) across the centre of a line pattern."""
    row = image(lines(width), defocus)[N // 2]
    half = width * SUB * 3 // 2                    # centre line and its two spaces
    centre = row[N // 2 - half:N // 2 + half]
    return (centre.max() - centre.min()) / (centre.max() + centre.min())


def width(row, level):
    """Width of the part of `row` above `level`, in micrometres. NaN if no part is above."""
    above = np.flatnonzero(row >= level)
    if not above.size:
        return np.nan
    i, j = above[0], above[-1]
    left = i - (row[i] - level) / (row[i] - row[i - 1])
    right = j + (row[j] - level) / (row[j] - row[j + 1])
    return (right - left) * DX


def save(fig, name):
    fig.savefig(OUT / f"optics_sim_{name}.png", dpi=150)
    plt.close(fig)
    print(f"docs/img/optics_sim_{name}.png")


def sim_airy():
    """1. One point of light does not make a point on the chip. It makes the Airy pattern."""
    p = np.fft.fftshift(psf())
    p /= p.max()
    x = axis()
    first_dark = 0.61 * UV / NA
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 4.2), gridspec_kw={"width_ratios": [1, 1.25]})
    w = 3.0
    a.imshow(p ** 0.5, cmap="gray", extent=[x[0], x[-1], x[0], x[-1]])
    a.set(xlim=(-w, w), ylim=(-w, w), xlabel="µm on the chip", ylabel="µm on the chip",
          title="Image of one point of light")
    a.grid(False)
    a.add_patch(plt.Rectangle((-PIXEL / 2, -PIXEL / 2), PIXEL, PIXEL, fill=False, edgecolor=C[1], lw=2))
    a.text(PIXEL / 2 + 0.1, PIXEL / 2 + 0.1, "one mirror", color="white", fontsize=9)
    a.text(-w + 0.15, -w + 0.15, "brightness increased to show the rings", color="white", fontsize=8)
    r = np.linspace(1e-6, w, 400)
    v = 2 * np.pi * NA / UV * r
    b.plot(x[N // 2:], p[N // 2, N // 2:], color=C[0], label="simulation")
    b.plot(r, (2 * j1(v) / v) ** 2, color=INK, lw=1, ls="--", label="Airy formula")
    b.axvline(first_dark, color=MUTED, lw=1, ls=":")
    b.text(first_dark + 0.05, 0.6, f"first dark ring\n0.61 × wavelength / NA\n= {first_dark:.2f} µm", fontsize=9)
    b.axvspan(0, PIXEL / 2, color=C[1], alpha=0.15, lw=0)
    b.text(PIXEL / 4, 1.02, "one mirror\n(half width)", ha="center", va="bottom", fontsize=8, color=MUTED)
    b.set(xlim=(0, w), ylim=(0, 1.2), xlabel="Distance from the centre, µm", ylabel="Light (1 = centre)")
    b.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    save(fig, "1_airy")


def sim_lines():
    """2. Narrow lines lose contrast. The space between them is not dark."""
    widths = [1, 2, 3, 4]
    fig, axes = plt.subplots(2, 2, figsize=(10, 6), sharey=True)
    x = axis()
    for ax, w, colour in zip(axes.ravel(), widths, C):
        ideal = lines(w)[N // 2]
        ax.fill_between(x, ideal, color="#e4e3df", step="mid", lw=0, label="pattern on the mirror chip")
        ax.plot(x, image(lines(w))[N // 2], color=colour, label="light on the chip")
        span = w * PIXEL * 5.5
        ax.set(xlim=(-span, span), ylim=(0, 1.15),
               title=f"Lines of {w} mirror{'s' if w > 1 else ''} = {w * PIXEL:.2f} µm.  Contrast {contrast(w):.0%}")
        ax.title.set_fontsize(10)
    for ax in axes[1]:
        ax.set_xlabel("µm on the chip")
    for ax in axes[:, 0]:
        ax.set_ylabel("Light")
    axes[0, 0].legend(frameon=False, fontsize=8, loc="upper right")
    fig.tight_layout()
    save(fig, "2_lines")


def sim_focus():
    """3. Out of focus, the contrast goes down. Narrow lines go first."""
    z = np.linspace(-12, 12, 49)
    fig, (a, b) = plt.subplots(1, 2, figsize=(10, 4.2))
    places = {1: (0, 0.03), 2: (0, -0.09), 3: (0, -0.08), 4: (7.6, -0.25)}     # label position from the peak
    for w, colour in zip([1, 2, 3, 4], C):
        a.plot(z, [contrast(w, d) for d in z], color=colour)
        dx, dy = places[w]
        a.text(dx, contrast(w) + dy, f"{w} mirror{'s' if w > 1 else ''}", ha="left" if dx else "center", fontsize=9)
    dof = UV / (2 * NA ** 2)
    a.axvspan(-dof, dof, color=MUTED, alpha=0.12, lw=0)
    a.text(0, 1.0, f"depth of focus ± {dof:.1f} µm", fontsize=9, color=MUTED, ha="center")
    a.set(xlabel="Chip height error (defocus), µm", ylabel="Contrast of the lines", ylim=(0, 1.1),
          title="Contrast against focus, by line width")
    x = axis()
    steps = [0, 3, 6, 10]
    for d, colour in zip(steps, C):
        b.plot(x, image(lines(2), d)[N // 2], color=colour, label=f"{d} µm")
    b.set(xlim=(-6, 6), ylim=(0, 1.15), xlabel="µm on the chip", ylabel="Light",
          title="Lines of 2 mirrors at four focus errors")
    b.legend(frameon=False, title="Defocus", loc="upper right", fontsize=9)
    fig.tight_layout()
    save(fig, "3_focus")


def test_pattern():
    """A small pattern, one value for each mirror: an L, squares of 1 to 4 mirrors, and lines."""
    m = np.zeros((30, 44), int)
    m[3:21, 3:7] = 1                 # the L: vertical bar, 4 mirrors wide
    m[17:21, 3:17] = 1               # the L: horizontal bar
    for i, s in enumerate([1, 2, 3, 4]):
        m[3:3 + s, 12 + 6 * i:12 + 6 * i + s] = 1          # squares
    for i in range(4):
        m[9:15, 22 + 2 * i] = 1      # lines of 1 mirror
    for i in range(3):
        m[9:15, 32 + 4 * i:34 + 4 * i] = 1                 # lines of 2 mirrors
    for i in range(3):
        m[23:27, 20 + 6 * i:23 + 6 * i] = 1                # lines of 3 mirrors
    m[23:27, 3:11] = 1               # a bar with a gap of 1 mirror
    m[23:27, 6] = 0
    return m


def sim_pattern():
    """4. What a pattern looks like on the chip, and after the resist."""
    m = test_pattern()
    grid = mirrors(m)
    half_h, half_w = m.shape[0] * SUB // 2 + 2 * SUB, m.shape[1] * SUB // 2 + 2 * SUB
    crop = lambda a: a[N // 2 - half_h:N // 2 + half_h, N // 2 - half_w:N // 2 + half_w]
    ext = [-half_w * DX, half_w * DX, -half_h * DX, half_h * DX]
    focus, blurred = image(grid), image(grid, 6.0)
    panels = [("Pattern on the mirror chip", crop(grid)), ("Light on the chip, in focus", crop(focus)),
              ("Resist after exposure, in focus", crop(focus) >= 0.5),
              ("Light on the chip, 6 µm out of focus", crop(blurred)),
              ("Resist after exposure, 6 µm out of focus", crop(blurred) >= 0.5)]
    fig = plt.figure(figsize=(11, 7.2))
    spec = fig.add_gridspec(2, 6)
    places = [spec[0, 0:2], spec[0, 2:4], spec[0, 4:6], spec[1, 1:3], spec[1, 3:5]]
    for (title, data), place in zip(panels, places):
        ax = fig.add_subplot(place)
        ax.imshow(data, cmap="gray", vmin=0, vmax=1, extent=ext, interpolation="nearest")
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("µm")
        ax.grid(False)
    fig.tight_layout()
    save(fig, "4_pattern")


def sim_dose():
    """5. More exposure makes bright lines wider. Narrow lines need more exposure to print at all."""
    dose = np.linspace(1.0, 4.0, 61)             # 1 = the smallest dose that clears a large area
    fig, ax = plt.subplots(figsize=(7.5, 4.4))
    for w, colour in zip([1, 2, 3, 4], C):
        row = image(mirrors(np.ones((40, w))))[N // 2]
        printed = np.array([width(row, 1 / d) for d in dose])
        ax.plot(dose, printed, color=colour)
        ax.axhline(w * PIXEL, color=colour, lw=1, ls=":")
        ax.text(4.05, printed[-1], f"{w} mirror{'s' if w > 1 else ''}", va="center", fontsize=9)
    ax.text(4.55, 2.95, "dotted: the width that the pattern asks for", fontsize=8, color=MUTED, ha="right")
    ax.set(xlabel="Exposure dose (1 = smallest dose that exposes a large area)", ylabel="Printed line width, µm",
           xlim=(1, 4.6), ylim=(0, 3.2), title="Width of one bright line against exposure dose")
    fig.tight_layout()
    save(fig, "5_dose")


if __name__ == "__main__":
    for sim in (sim_airy, sim_lines, sim_focus, sim_pattern, sim_dose):
        sim()
    print("contrast in focus:", {w: round(float(contrast(w)), 2) for w in (1, 2, 3, 4)})
