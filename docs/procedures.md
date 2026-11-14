# Procedures

## 1. Print the test piece

1. Open `stl/00_test_piece.stl` in the slicer.
2. Use the material that you will use for the beamsplitter holder.
3. Apply the settings in [parts.md](parts.md).
4. Slice the part. Make sure that the slicer adds no supports.
5. Print the part.

## 2. Read the test piece

The test piece has three round holes. Notches on the edge identify them.

| Notches | Hole diameter |
|---|---|
| 1 | 30.6 mm |
| 2 | 30.7 mm |
| 3 | 30.8 mm |

1. Push an SM1 lens tube into each round hole.
2. Record the smallest hole that the tube enters without force.
3. Put the beamsplitter cube into the square pocket (30.3 mm). Hold the cube by its rough faces.
4. Record the result: loose, correct, or does not enter.
5. Put an M5 screw through the small round hole. Put an M3 nut into the hexagonal pocket.
6. Record the fit of the screw and the nut.

## 3. Apply the result

1. Open `cad/params.py`.
2. Set `TUBE_BORE` to the hole diameter from step 2.2.
3. If the cube did not enter, increase `CUBE_POCKET` by 0.2. If the cube was loose, decrease it by 0.1.
4. Run `uv run python -m cad.build`.
5. Make sure that each line shows `OK`.

## 4. Print the parts

1. Open the STL files in the slicer. Do not turn the parts.
2. Set the quantity of each part. Refer to [parts.md](parts.md).
3. Set the material of each part.
4. Slice the parts.
5. Examine the preview:
   - Each part touches the bed with a flat face.
   - The slicer added no supports.
6. Print the parts.

## 5. Assemble the frame

CAUTION: The projector is at the top of the frame. A narrow base can fall over. Make sure that the frame is stable before you install the optics.

1. Put the two halves of the beamsplitter holder together. Their total thickness is 44 mm.
2. Set the two uprights parallel, with the holder between them as a gauge.
3. Attach the uprights to the base bars with corner brackets.
4. Put T-nuts into the upright slots before you close the ends.

The base layout is not final. One option: one base bar below the two uprights, and one base bar that points to the front.

## 6. Install the parts

Install the parts from the top to the bottom. Tighten the frame screws only after all tubes align.

1. Attach the adapter plate to the projector with four M2 screws. The countersinks point down.
2. Look into the light hole. If the mirror chip is not in the centre, turn the plate 90° and do this step again.
3. Attach the SM1A53 flange below the plate.
4. Put the plate on the projector bracket. Attach it from below.
5. Bolt the base half of the beamsplitter holder to the inner face of the left upright.
6. Put the cube, the tubes and the sleeve into the base half. Install the cover.
7. Bolt the camera clamp block to the back faces of the uprights.
8. Install the tube clamps, the board rails and the stage platform.
9. Attach the chip holder to the end effector.

CAUTION: The distance between the objective and the chip is 1.5 mm. Lift the stage slowly.
