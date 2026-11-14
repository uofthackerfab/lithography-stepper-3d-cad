# Procedures

## 1. Print the parts

1. Open the STL files in the slicer. Do not turn the parts.
2. Set the quantity of each part. Refer to [parts.md](parts.md).
3. Set the material of each part.
4. Slice the parts.
5. Examine the preview:
   - Each part touches the bed with a flat face.
   - The slicer added no supports.
6. Print the parts.

## 2. Examine the fits

1. Close the two halves of the beamsplitter holder on a lens tube. A seam gap of less than 0.5 mm is satisfactory.
2. Put the cube into the base half. Hold the cube by its rough faces. Push lightly. The ribs hold the cube.
3. If a fit is incorrect, change the value in `cad/params.py` and build the part again.

| Fault | Value to change |
|---|---|
| Seam gap is larger than 0.5 mm | Increase `TUBE_BORE` by 0.2 |
| Tube is loose in a closed holder | Decrease `TUBE_BORE` by 0.1 |
| Cube does not enter | Decrease `CUBE_RIB` by 0.1 |
| Cube is loose | Increase `CUBE_RIB` by 0.1 |
| Sleeve does not enter the camera block | Increase `SLEEVE_BORE` by 0.2 |

The test piece (`00_test_piece.stl`) is optional. It has holes of 30.6, 30.7 and 30.8 mm with 1, 2 and 3 notches. Use it to measure a printer before a long print.

## 3. Assemble the frame

The frame uses the four 500 mm bars:

```
   view from above                    view from the front

   A ====[U]==[U]=========            U   U     two uprights, on bar A
              |                       |   |
              B                    ===A=========
              |  (to the front)
```

- Bar A lies on the table, from left to right.
- The two uprights (U) stand on bar A, at its centre.
- Bar B lies on the table. It points to the front. It joins bar A to the right of the uprights.

1. Put the two halves of the beamsplitter holder together. Their total thickness is 44 mm.
2. Put the two uprights on bar A, with the holder between them as a gauge.
3. Attach each upright to bar A with two corner brackets. Make sure that the front faces of the uprights and of bar A align.
4. Attach bar B to the front face of bar A, 60 mm or more to the right of the right upright.
5. Put T-nuts into the slots: 5 in each front slot of the uprights, 4 in each back slot, 2 in the inner slot of the left upright, and 2 in the front slot of bar A.

CAUTION: The frame falls to the rear if it tilts more than approximately 13°. Do not push the top of the frame to the rear.

## 4. Install the parts

Install the parts from the top to the bottom. Tighten the frame screws only after all tubes align.

1. Attach the adapter plate to the projector with four M2 screws. The countersinks point down.
2. Look into the light hole. If the mirror chip is not in the centre, turn the plate 90° and do this step again.
3. Attach the SM1A53 flange below the plate with four M3 × 6 screws.
4. Put the plate on the projector bracket. Turn the projector so that its larger part points to the front. Attach the plate from below.
5. Bolt the base half of the beamsplitter holder to the inner face of the left upright.
6. Put the cube, the tubes and the sleeve into the base half. Install the cover.
7. Bolt the camera clamp block to the back faces of the uprights.
8. Install the tube clamps and the board rails. Put the rails at a height where the projector cables reach the main board.
9. Bolt the stage base to the front face of bar A, on the left. Put the micro-manipulator stand in the rim.
10. Attach the chip holder to the end effector.

Recommended lens tubes:

| Arm | Parts, from the holder outward | Length |
|---|---|---|
| Objective (down) | SM1L10, SM1A3, objective | 26.2 mm to the objective shoulder |
| Projector (up) | SM1L10, SM1V10, SM1A53 | adjustable: 45 to 66 mm |
| Camera (back) | printed sleeve | 78 mm |

CAUTION: The distance between the objective and the chip is 1.5 mm. Lift the stage slowly.

## 5. Set the focus

1. Move the stage in Z until the camera shows a sharp image of the chip.
2. If the stage has no travel left, slide the camera in its saddle.
3. Project a pattern. Turn the SM1V10 until the pattern is sharp on the camera.
