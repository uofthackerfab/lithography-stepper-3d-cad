# Parts

## How the parts fit together

```
            [ projector ]            lens removed, points down
            adapter plate            03_adapter_plate
            projector bracket        03_projector_bracket
            SM1A53 + lens tubes
                  |
   [ light trap | cube ] -- sleeve -- [ camera ]
     01_beamsplitter_holder   02_camera_sleeve   02_camera_clamp
                  |
              lens tube              04_tube_clamp
            [ objective ]
                  |  1.5 mm
            [ chip holder ]          07_chip_holder
            [ micro-manipulator ]
            stage platform           08_stage_platform
```

View from above:

```
        back
   [ camera clamp ]         on the back faces of the uprights
   [bar]  sleeve  [bar]     two uprights, 44 mm apart
          cube              optical axis, 55 mm in front of the uprights
        light trap
        front
```

- The frame has two vertical 2020 bars (uprights). The clear distance between them is 44.0 mm.
- The optical axis is vertical. It is 55 mm in front of the uprights, on the centre line between them.
- The camera arm goes back between the uprights. The light trap points to the front.

## Part list

Print one of each file unless the table gives a different quantity.

| File | Qty | Function | Material |
|---|---|---|---|
| `00_test_piece` | 1 | Finds the correct hole size for the tube and the cube. Print it first. | Same as part 01 |
| `01_beamsplitter_holder_base` | 1 | Half of the cube holder. Bolts to the left upright. | Matte black PETG |
| `01_beamsplitter_holder_cover` | 1 | Other half. Closes the holder. | Matte black PETG |
| `02_camera_clamp_block` | 1 | Holds the camera behind the uprights. | Matte black PETG |
| `02_camera_clamp_cap` | 1 | Locks the camera in the block. | Any |
| `02_camera_sleeve` | 1 | Light tube between the holder and the camera. | Matte black PETG |
| `03_adapter_plate` | 1 | Joins the projector lens face to the SM1A53 flange. | PETG or ASA |
| `03_projector_bracket` | 1 | Carries the adapter plate and the projector. | PETG or ASA |
| `04_tube_clamp` | 3 | Holds a lens tube to the frame. The third clamp is a spare. | Any |
| `05_baffle_ring` | 4 to 6 | Optional. Decreases reflections in a lens tube. | Matte black PETG |
| `06_board_rail` | 2 | Holds the TI main board on the uprights. | Any |
| `07_chip_holder` | 1 | Holds the chip on the micro-manipulator. | Any |
| `08_stage_platform` | 1 | Table for the micro-manipulator. | Any |

"Any" means PLA or PETG of any colour.
Parts in the light path must be black and opaque.
Parts near the projector become warm. PLA can deform there.

## Print settings

| Setting | Value |
|---|---|
| Nozzle | 0.4 mm |
| Layer height | 0.2 mm |
| Walls | 4 |
| Infill | 40 % |
| Supports | Off |
| Orientation | As opened. Do not turn the parts. |

These settings are recommendations. They are not tested.

## Screws

| Joint | Screw | Qty |
|---|---|---|
| Printed part to upright | M5 × 12 and T-nut | 20 |
| Board rail to upright | M5 × 8 and T-nut | 4 |
| Beamsplitter holder, base to cover | M3 × 20 and nut | 8 |
| Tube clamp pinch screw | M3 × 16 and nut | 3 |
| Camera cap | M3 × 16 and nut | 2 |
| Adapter plate to projector bracket | M3 × 12 and nut | 4 |
| Main board to rails | M3 × 12 and nut | 4 |
| SM1A53 flange to adapter plate | M3 × 8 socket head and nut | 4 |
| Adapter plate to projector | M2 countersunk | 4 |
| Chip holder to end effector | M3 countersunk | 2 |

- The Taiss kit contains 20 M5 × 12 screws. This is the exact quantity.
- The M2 screw length is unknown. Start with the shortest screw that grips. Do not use force.
- The end effector holes are 3.0 mm. Their thread type is unknown.

## Notes for each part

**01 Beamsplitter holder**
- The two halves close around the cube, two lens tubes and the sleeve.
- The cube sits on a 2 mm ledge. The tubes stop on the other side of the ledge and do not touch the glass.
- Put felt on the two large inner faces. The felt presses the cube.
- Line the light trap with felt.
- The tube holes are slip fits. The tube clamps and the projector bracket hold the tubes.
- Put black tape on the seam between the halves.

**02 Camera clamp**
- The camera lies in the saddle. Slide it to set focus, then tighten the cap.
- The camera nose must stay in the closed ring. The ring blocks room light.
- Turn the camera until its ports point up.
- The block is large (approximately 290 cm³). Its print time is long.

**03 Adapter plate and projector bracket**
- The light hole is 2.9 mm from the centre of the M2 hole square. The direction on your projector is unknown.
- The plate fits on the projector in four positions. Only one is correct.
- The plate also fits on the bracket in four positions. Thus the projector can point in any of four directions.

**07 Chip holder**
- The pocket is 31.95 mm square and 0.4 mm deep. The chip surface is 0.1 mm above the plate.
- The screw heads are below the chip.
- The method to hold the chip is not decided. Tape is possible.

**08 Stage platform**
- The platform is a flat table with M3 slots. It is not a fitted mount.
- The position of the micro-manipulator on the platform is not designed.
