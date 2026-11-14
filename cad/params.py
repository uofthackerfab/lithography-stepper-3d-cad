"""All dimensions, in millimetres. Change a value here, then run the build again.

Status of each value: [V] verified, [E] estimate.
"""

# --- Fits. Each one tolerates a printer error of +/- 0.2 ---
TUBE_BORE = 30.7        # hole for an SM1 tube (tube is 30.5 [V]). Split parts close on the tube.
SLEEVE_BORE = 31.0      # closed hole for the printed sleeve: loose
CUBE_POCKET = 30.6      # pocket for the 30 mm cube; crush ribs take up the clearance
CUBE_RIB = 0.3          # each rib stands this far into the pocket

# --- Optics [V] ---
TUBE_OD = 30.5          # Thorlabs SM1 lens tube, outside diameter
CUBE = 30.0             # beamsplitter cube, nominal
CAMERA_OD = 62.0        # ZWO ASI174MM body
CAMERA_LEN = 30.1
CLEAR_APERTURE = 24.0   # light opening in the printed walls [E]

# --- Frame: 2020 extrusion, two uprights behind the optical axis ---
BAR = 20.0              # [V]
UPRIGHT_GAP = 44.0      # clear distance between the two uprights
UPRIGHT_X = UPRIGHT_GAP / 2 + BAR / 2   # 32: upright centre, each side of the axis
AXIS_TO_FRAME = 55.0    # optical axis to the front face of the uprights
FRAME_BACK = AXIS_TO_FRAME + BAR        # 75: back face of the uprights

# --- Screws ---
M5_HOLE = 5.5
M5_HEAD = 10.5          # pocket for the screw head
M5_TRAVEL = 2.0         # slots give +/- this much adjustment
M3_HOLE = 3.4
M3_HEAD = 6.5
M3_NUT = 5.8            # pocket across flats (nut is 5.5)
M3_NUT_T = 2.8          # pocket depth (nut is 2.4)
M2_HOLE = 2.4
M2_CSK = 4.4            # countersink diameter, 90 degrees

FLANGE = 7.0            # plate that bolts to the frame. An M5 x 12 screw then enters the slot by 5 mm
WALL = 4.0              # minimum wall

# --- Projector lens face [V], Hacker Fab adapter plate CAD ---
M2_SQUARE = 28.0        # four M2 holes on a 28 x 28 square
DMD_OFFSET = 2.9        # light bore is this far from the centre of the square
LIGHT_BORE = 25.4
SM1A53_BOLT_R = 18.385  # four M3 holes on a 26 x 26 square [V], Thorlabs drawing
PLATE = 62.0            # adapter plate, square
PLATE_BOLT = 26.0       # plate-to-bracket M3 holes at (+/-26, +/-26)

# --- Main board: TI DLP046 rev B [V], TI design package ---
BOARD_X = 150.0
BOARD_HOLE_X = 140.0
BOARD_STANDOFF = 8.0    # [E] clears the parts on the underside

# --- Stage and chip ---
CHIP = 31.75            # square chip [V]
CHIP_T = 0.525          # [V]
EE_HOLES = [(6.0, 1.0), (6.0, 11.0)]   # 3 mm holes in the end effector face [V], from the STL
