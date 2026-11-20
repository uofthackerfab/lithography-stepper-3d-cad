# Lithography stepper: printed parts

This repository contains the 3D-printed parts of the maskless lithography stepper.
It does not contain the micro-manipulator parts. See [RESOURCES.md](RESOURCES.md) for those files.

The parts are drawn by code. The STL files in `stl/` are ready for a slicer.
A slicer is the program that converts an STL file into printer instructions.

## The machine

Six views of the complete machine. The labelled view and the main dimensions are in [docs/assembly.md](docs/assembly.md).

| | | |
|---|---|---|
| ![Front view](docs/img/assembly_front.png)<br>Front | ![Back view](docs/img/assembly_back.png)<br>Back | ![View from above at 45 degrees](docs/img/assembly_angle.png)<br>From above, at 45° |
| ![Left view](docs/img/assembly_left.png)<br>Left | ![Right view](docs/img/assembly_right.png)<br>Right | ![Top view](docs/img/assembly_top.png)<br>Top (the rear of the machine is up) |

## Parts

Each picture shows the part in its print orientation.

| | | |
|---|---|---|
| ![Test piece (optional)](docs/img/00_test_piece.png)<br>`00_test_piece`<br>Test piece (optional) | ![Beamsplitter holder, base](docs/img/01_beamsplitter_holder_base.png)<br>`01_beamsplitter_holder_base`<br>Beamsplitter holder, base | ![Beamsplitter holder, cover](docs/img/01_beamsplitter_holder_cover.png)<br>`01_beamsplitter_holder_cover`<br>Beamsplitter holder, cover |
| ![Camera clamp, block](docs/img/02_camera_clamp_block.png)<br>`02_camera_clamp_block`<br>Camera clamp, block | ![Camera clamp, cap](docs/img/02_camera_clamp_cap.png)<br>`02_camera_clamp_cap`<br>Camera clamp, cap | ![Camera sleeve](docs/img/02_camera_sleeve.png)<br>`02_camera_sleeve`<br>Camera sleeve |
| ![Adapter plate](docs/img/03_adapter_plate.png)<br>`03_adapter_plate`<br>Adapter plate | ![Projector bracket](docs/img/03_projector_bracket.png)<br>`03_projector_bracket`<br>Projector bracket | ![Tube clamp](docs/img/04_tube_clamp.png)<br>`04_tube_clamp`<br>Tube clamp |
| ![Baffle ring (optional)](docs/img/05_baffle_ring.png)<br>`05_baffle_ring`<br>Baffle ring (optional) | ![Board rail](docs/img/06_board_rail.png)<br>`06_board_rail`<br>Board rail | ![Chip holder](docs/img/07_chip_holder.png)<br>`07_chip_holder`<br>Chip holder |
| ![Stage base](docs/img/08_stage_base.png)<br>`08_stage_base`<br>Stage base | ![Side board holder](docs/img/09_side_board_holder.png)<br>`09_side_board_holder`<br>Side board holder |   |

## Status

- All 14 STL files are closed meshes and each one is smaller than 200 mm.
- A geometry check found no overhang that needs supports.
- No part is printed yet. A fit is confirmed only after a print.
- The fits tolerate a printer error of ±0.2 mm. The test piece is optional.

## Contents

| Path | Contents |
|---|---|
| `stl/` | STL files, in print orientation |
| `cad/params.py` | All dimensions |
| `cad/parts/` | One file for each part |
| `cad/build.py` | Builds and checks all parts |
| `cad/render.py` | Makes the pictures in `docs/img/` |
| [docs/assembly.md](docs/assembly.md) | The complete machine: model, views, main dimensions |
| `assembly/public/` | STEP and GLB files of the complete machine, with a simple projector shape. These can be shared. |
| `assembly/private/` | The same files with the manufacturer's projector model. Git ignores this folder. Do not share it. |
| `cad/assembly.py`, `cad/purchased.py` | Positions of all parts; models of the purchased parts |
| `cad/data/` | CAD of the micro-manipulator (MIT licence), converted by `cad/import_manipulator.py` |
| `viewer/` | Web page that shows the complete machine in 3D. See [docs/assembly.md](docs/assembly.md). |
| [docs/parts.md](docs/parts.md) | Part list, print settings, screws |
| [docs/procedures.md](docs/procedures.md) | Test piece, print, and assembly procedures |
| [docs/dimensions.md](docs/dimensions.md) | Dimensions with their sources, and open items |
| [RESOURCES.md](RESOURCES.md) | All links |

## Build the STL files

1. Install [uv](https://docs.astral.sh/uv/).
2. Go to the repository folder.
3. Run this command:

```bash
uv run python -m cad.build
```

The command writes `stl/` and `step/`. It prints `OK` for each part that passes the mesh check.

To build one part, add its name:

```bash
uv run python -m cad.build 04_tube_clamp
```

## Change a dimension

1. Open `cad/params.py`.
2. Change the value.
3. Run the build command again.
