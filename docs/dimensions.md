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
- The SM1A53 counterbore depth is unknown [U].
- A printed 30.7 hole does not accept the SM1CPL05 or a lock nut.

## Camera: ZWO ASI174MM [V]

- Body diameter 62.
- Sensor 6.5 behind the front face of the M42 collar.
- USB and ST4 ports on the round side wall.
- One 1/4 inch tapped hole on the back face.
- Body length approximately 31, plus a 4 collar [E].

## Objective: Edmund 10X DIN Plan, #43-907 [V]

- Length 44.0 without threads. Largest diameter 24.
- Working distance 1.5.
- RMS thread. The SM1A3 adapts it to SM1.

## Beamsplitter cube

- 30 nominal [V]. Real dimension and tolerance [U]. The test piece gives the answer.

## Projector: TI DLPDLCR471TPEVM

- Light engine envelope 88.49 × 83.96 × 136.39 [V].
- Lens face: four M2 holes on a 28 × 28 square [V], from the Hacker Fab CAD.
- Light hole 25.4, at 2.9 from the centre of the square [V]. Direction on the real unit [U].
- Position of the lens face on the engine [U]. Clearance to the uprights is not verified.
- Temperature at the lens face [U].

## Main board: TI DLP046 rev B [V]

- Outline 150 × 125. Thickness 1.57.
- Four corner holes, 3.43 diameter, on a 140 × 115 rectangle.
- Small parts only on the bottom side.
- Height of the fan on the top side [U].

## Frame

- 2020 extrusion. Slot opening 6.2, slot depth 6.1 [V, copy of a datasheet].
- A 7 thick printed plate and an M5 × 12 screw put 5 of thread into the slot.

## Stage: Open Micro-Manipulator v4

- End effector: 29 cube. Each outer face has two 3.0 holes, 10 apart [V], from the STL.
- Travel approximately 20 for each axis [E].
- Interface between the base block and a mount [U].

## Optical distances [E]

- Image distance of the objective: 150 from its shoulder, plus 10 for the glass of the cube.
- With one SM1L10 below the holder, the camera sensor is approximately 117 from the cube centre.
- The camera clamp accepts a camera front face from 106 to 115 behind the optical axis.

## Decisions in this design

| Decision | Reason |
|---|---|
| Two uprights behind the optical axis, 44 apart | The beamsplitter holder fills the gap. The camera arm goes between the bars. |
| Holder split in two halves, no lid | Each half prints without supports. |
| Tube holes in the holder are slip fits | The clamps and the bracket hold the tubes. |
| Printed sleeve on the camera arm | This arm has no lens. The SM1 tubes stay available for the other arms. |
| Adapter plate separate from the bracket | The offset direction is unknown. The projector can point in four directions. |
| No objective shroud | The 1.5 working distance gives no space. |
| M3 nuts in printed pockets | No heat-set inserts and no special tool. |

## Open items

| Item | Who | Status |
|---|---|---|
| Printer and material | User | Not selected |
| Tube hole and cube pocket dimensions | User | Print the test piece |
| Offset direction at the projector | User | Find at assembly |
| Projector clearance to the uprights | User | Examine at assembly |
| Base layout and stability | User | Not final |
| Method to hold the chip | User | Not decided |
| Mount of the micro-manipulator on the platform | - | Not designed |
| Slicer check of all parts | - | Not done. No slicer was available. |
