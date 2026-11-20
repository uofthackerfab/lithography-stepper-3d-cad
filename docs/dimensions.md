# Dimensions and open items

Each value has a status:

- **[V]** verified from a primary source or from a file
- **[E]** estimate
- **[U]** unknown

All dimensions are in millimetres. Links are in [RESOURCES.md](../RESOURCES.md).

## Lens tubes (Thorlabs SM1) [V]

| Part | Length that it adds | Largest diameter |
|---|---|---|
| SM1L03 | 8.4 | 30.5 |
| SM1L05 | 13.5 | 30.5 |
| SM1L10 | 26.2 | 30.5 |
| SM1V05 | 13.5 collar, 7.9 travel | 31.8 (lock nut) |
| SM1V10 | 13.5 collar, 20.6 travel | 31.8 (lock nut) |
| SM1CPL05 | 0 (sleeve, 12.7 long) | 37.1 |
| SM1A9 | 4.4 | 30.7 |
| SM1A3 | 0 (inside the tube) | - |
| SM1A53 | 5.6 | 35.1 square |

- SM1A53: flat plate, internal SM1 thread, four counterbored M3 holes on a 26.0 × 26.0 square.
- SM1A53 counterbore: 6.5 diameter, 4.27 deep. 1.29 of material is below the screw head [V], from the Thorlabs STEP file.
- A printed 30.7 hole does not accept the SM1CPL05 or a lock nut.

## Camera: ZWO ASI174MM [V]

- Body diameter 62.
- Sensor 6.5 behind the front face of the M42 collar.
- USB and ST4 ports on the round side wall.
- One 1/4 inch tapped hole on the back face.
- Body length 30.1, plus a 4 collar [V].
- Ports in the rear 10 of the body [E].
- Mass 140 g [V].

## Objective: Edmund 10X DIN Plan, #43-907 [V]

- Length 44.0 without threads. Largest diameter 24.
- Working distance 1.5.
- RMS thread. The SM1A3 adapts it to SM1.

## Beamsplitter cube

- 30 nominal [V]. Real dimension and tolerance [U].
- The holder accepts a cube from 29.8 to 30.3. Crush ribs take up the difference.

## Projector: TI DLPDLCR471TPEVM

The values come from the CAD model of the light engine in the Hacker Fab assembly (`SPEC_800-0255-A_F16D`) [V].
They are not measured on the real unit.

- Engine with the lens removed: 85.0 × 58.1 in plan, 62.3 high above the lens face.
- From the optical axis: 42.5 to each side, 28.1 to one long side, 29.9 to the other. The uprights are 55 away.
- Lens face: four holes on a 28 × 28 square. The lens mount (a square flange with a disc) comes off with these four screws [E].
- Mirror chip: 3.0 from the centre of the square. The adapter plate uses 2.9, as the Hacker Fab plate does.
- A thin lip is on the side that the mirror chip is nearest to. It is 45 wide and goes 8.5 below the lens face. Small ribs are next to it.
- The adapter plate has a slot for the lip. Thus the plate fits in one position.
- Mirror chip to lens face: 41.4. Glass in the engine can change the optical distance by some millimetres [E].
- Holes in the housing: 2.8 diameter in the model, 4 or more deep. Mass [U]. Length of the cables to the main board [U].
- TI user's guide: envelope 88.49 × 83.96 × 136.39 with the projection lens.
- Temperature at the lens face [U]. PETG or ASA is specified there.

## Main board: TI DLP046 rev B [V]

- Outline 150 × 125. Thickness 1.57.
- Four corner holes, 3.43 diameter, on a 140 × 115 rectangle.
- Small parts only on the bottom side.
- Height of the fan on the top side [U]. It does not matter: the top side points away from the rails.

## Frame

- 2020 extrusion. Slot opening 6.2, slot depth 6.1 [V, copy of a datasheet].
- Mass of one 500 bar: approximately 245 g [V, listing]. The bar ends are not tapped [E].
- A 7 thick printed plate and an M5 × 12 screw put 5 of thread into the slot.

## Stage: Open Micro-Manipulator v4

- End effector: 29 cube. Each outer face has two 3.0 holes, 10 apart [V], from the STL.
- End effector centre: 47.5 from the base block origin on each axis [V].
- Travel: 23 for each axis is given for version 3 [V]. Approximately 20 for version 4 [E].
- Motors: 42 × 42 × 39 [V], from the user.
- The end effector holes are plain, 8 deep [V], from the FreeCAD file.
- The base block has no holes for a mount [V]. The documented mount is the printed stand `demoStandV1.stl`, with five M3 screws at the motor mounts.
- Stand foot: 101 × 100, flat, no holes. The end effector top face is 127.6 above the bottom of the foot.
- The stand does not touch motors of 38, 40 or 48 length [V], point test against the stand mesh.

## Optical distances [E]

- Image distance of the objective: 150 from its shoulder, plus 10 for the glass of the cube.
- With the SM1L05 and SM1L03 below the holder, the camera sensor is 118 from the cube centre.
- The camera clamp accepts a camera front face from 106 to 115 behind the optical axis.
- Heights above the table: chip 135, cube centre 222, projector lens face 299, top of the projector 361. The uprights are 500.

## Decisions in this design

| Decision | Reason |
|---|---|
| Base: bar A below the uprights, bar B to the front | Wide in both directions. Tilt limit to the rear approximately 13° [E]. |
| Stage stands on the table in its printed stand | The stand is a known interface. The stage Z travel sets the focus. |
| Fits with ribs and split holes | A printer error of ±0.2 does not stop the assembly. |
| Chip held with polyimide tape | Nothing can be higher than the chip surface. |
| All parts in matte black PETG | One material is sufficient for light, heat and strength. |
| Two uprights behind the optical axis, 44 apart | The beamsplitter holder fills the gap. The camera arm goes between the bars. |
| Holder split in two halves, no lid | Each half prints without supports. |
| Printed sleeve on the camera arm | This arm has no lens. The SM1 tubes stay available for the other arms. |
| Adapter plate separate from the bracket | Each part prints flat. The lip of the projector points to the front. |
| No objective shroud | The 1.5 working distance gives no space. |
| M3 nuts in printed pockets | No heat-set inserts and no special tool. |

## Open items

| Item | Who | Status |
|---|---|---|
| Printer | User | Not selected. Minimum bed 170 × 120. |
| Reach of the projector cables to the main board | User | Not published. Slide the rails to the correct height at assembly. |
| Screws at the projector lens face | User | Use the four screws that held the lens mount, if they are long enough for the 6 mm plate. If not, try M2 × 8, then M2 × 10. |
| Lens mount of the projector | User | Make sure that it comes off with its four screws. The model shows this, the real unit is not examined. |
| All fits | User | Confirmed only after a print |
| Slicer preview | User | Do it in the slicer of the selected printer. The geometry check found no supports necessary. |
