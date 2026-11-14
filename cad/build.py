"""Build every part, check each mesh, write STL files to stl/.

Run from the repository root:  uv run python -m cad.build [part ...]
"""
import sys
from pathlib import Path

import trimesh
from build123d import Pos, Rot, export_step, export_stl

from .parts import (adapter_plate, baffle_ring, beamsplitter_holder, board_rail,
                    camera_clamp, camera_sleeve, chip_holder, projector_bracket,
                    stage_platform, test_piece, tube_clamp)

ROOT = Path(__file__).resolve().parent.parent

# file name: (builder, rotation that puts the part in its print orientation)
PARTS = {
    "00_test_piece": (test_piece.build, test_piece.PRINT_ROT),
    "01_beamsplitter_holder_base": (beamsplitter_holder.base, (0, -90, 0)),
    "01_beamsplitter_holder_cover": (beamsplitter_holder.cover, (0, 90, 0)),
    "02_camera_clamp_block": (camera_clamp.block, (90, 0, 0)),
    "02_camera_clamp_cap": (camera_clamp.cap, (0, 0, 0)),
    "02_camera_sleeve": (camera_sleeve.build, camera_sleeve.PRINT_ROT),
    "03_adapter_plate": (adapter_plate.build, adapter_plate.PRINT_ROT),
    "03_projector_bracket": (projector_bracket.build, projector_bracket.PRINT_ROT),
    "04_tube_clamp": (tube_clamp.build, tube_clamp.PRINT_ROT),
    "05_baffle_ring": (baffle_ring.build, baffle_ring.PRINT_ROT),
    "06_board_rail": (board_rail.build, board_rail.PRINT_ROT),
    "07_chip_holder": (chip_holder.build, chip_holder.PRINT_ROT),
    "08_stage_platform": (stage_platform.build, stage_platform.PRINT_ROT),
}


def on_bed(part, rot):
    part = Rot(*rot) * part
    bb = part.bounding_box()
    return Pos(-(bb.min.X + bb.max.X) / 2, -(bb.min.Y + bb.max.Y) / 2, -bb.min.Z) * part


def main(names):
    (ROOT / "stl").mkdir(exist_ok=True)
    (ROOT / "step").mkdir(exist_ok=True)
    ok = True
    for name in names or PARTS:
        builder, rot = PARTS[name]
        part = on_bed(builder(), rot)
        path = ROOT / "stl" / f"{name}.stl"
        export_stl(part, str(path), tolerance=0.01, angular_tolerance=0.1)
        export_step(part, str(ROOT / "step" / f"{name}.step"))
        mesh = trimesh.load(path)
        good = mesh.is_watertight and mesh.is_winding_consistent and mesh.body_count == 1 and max(mesh.extents) <= 200
        ok &= good
        x, y, z = mesh.extents
        print(f"{'OK  ' if good else 'FAIL'} {name:30s} {x:6.1f} x {y:6.1f} x {z:5.1f} mm  {mesh.volume / 1000:6.1f} cm3")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main(sys.argv[1:])
