# Assembly

The file `assembly/stepper.step` contains all 35 parts in their positions. Each part has a name and a colour.

![Assembly with labels](img/assembly_labelled.png)

| View | File |
|---|---|
| Front | [img/assembly_front.png](img/assembly_front.png) |
| Right | [img/assembly_right.png](img/assembly_right.png) |
| Rear | [img/assembly_rear.png](img/assembly_rear.png) |
| No labels | [img/assembly_iso.png](img/assembly_iso.png) |

## Open the model

- `assembly/stepper.step`: open it in FreeCAD, Fusion or Onshape. You can measure each distance there.
- `assembly/stepper.glb`: open it in MeshLab or a web 3D viewer. Use it only to look.

## Build the model

```bash
uv run --with pyvista python -m cad.assembly
```

The command prints the position of each part. It also tests each pair of parts for a collision. The result now is `no collisions`.

## Axes

- x points to the right. y points to the rear. z points up.
- The optical axis is x = 0, y = 0. The table is z = 0.

## Main dimensions (mm)

| Item | Value | Status |
|---|---|---|
| Chip surface above the table | 134.7 | [V] from part dimensions |
| Objective tip above the chip | 1.5 | [V] |
| Objective shoulder | z = 180.2 | [V] |
| Centre of the beamsplitter cube | z = 222.2 | [V] |
| Front face of the camera | y = 111.7 | [E] uses the 150 image distance |
| Projector lens face | z = 299.0 | [V] 41.4 from mirror chip to lens face, projector CAD |
| Top of the projector | z = 361 | [V] projector CAD |
| Top of the uprights | z = 520 | [V] |
| SM1V10 travel in use | 8.4 of 20.6 | [E] |
| Footprint of the frame | 500 × 520 | [V] |

## Lens tubes in the model

| Arm | Parts, from the cube outward |
|---|---|
| Down | SM1L03, SM1L05, SM1A3 (inside the SM1L05), objective |
| Up | SM1V10 (collar in the holder), SM1L10, SM1A53, adapter plate, projector |
| Rear | printed sleeve, camera |

## Simplified parts

- Projector: the pictures and the collision check use the real CAD model (`vendor/projector.brep`). This file is not in the repository. The STEP and GLB files contain a simple block model with the same outside dimensions.
- Micro-manipulator: boxes for the base block, end effector, three motors, three motor mounts and the stand. The positions are from the STL files. Rods, horns and wires are not shown.
- Main board: a plate with the correct outline and holes.
- Screws, nuts, T-nuts, corner brackets, felt and cables are not shown.

## Purchased parts that are not in the model

| Part | Reason |
|---|---|
| SM1V05, SM1CPL05 | Spare. The model does not need them. |
| SM1A9 | Not used. It has a C-mount thread and the camera has an M42 thread. |
| Arduino, CNC shield, A4988 and TMC2209 drivers, proximity sensor | Electronics with no fixed position |
| Pico 2, MT6835 encoders, buck converter, connectors, wires | Electronics of the micro-manipulator |
| Balls, brass rod, cord, magnets, crimp beads | Small parts inside the micro-manipulator |
| UV LEDs, Pico-SPOX connectors | Inside the projector |
| Power supplies | On the table |
