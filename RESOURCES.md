# Resources

All links and source files for the printed parts of the lithography stepper.
Collected on 2026-11-14.

## Reference designs

| Resource | Link |
|---|---|
| Hacker Fab Stepper V2 build page | https://docs.hackerfab.org/hacker-fab-space/fab-toolkit/patterning/lithography-stepper-v2-build-work-in-progress |
| Hacker Fab full assembly (Onshape) | https://cad.onshape.com/documents/64016e74334e9df7f3829a37/w/da5b11336b83f611c84f6d9f/e/345550da08271685cbf13c97 |
| Hacker Fab adapter plate (Onshape) | https://cad.onshape.com/documents/64016e74334e9df7f3829a37/v/b7cf6897006e1bbfe46b354b/e/0e8c1f104c4c4708545e72bb |
| Hacker Fab base plate (Onshape) | https://cad.onshape.com/documents/052936cc5219e79ce8b1d191/w/decf2990870bd6e2bca78fa2/e/bd3bd601a477f0977cdc93cc |
| Hacker Fab vacuum chuck (Onshape) | https://cad.onshape.com/documents/f6235112d9655ce90371982d/w/a0efdc80157be57df12af66d/e/fe48a0682c07d2cebc332aac |
| Hacker Fab Stepper V2.1 build page (photos of each projector step) | https://docs.hackerfab.org/home/fab-toolkit/lithography-stepper/lithography-stepper-v2.1+-build |
| Hacker Fab UV LED board files | https://github.com/hacker-fab/stepper-v2-led |
| Hacker Fab stepper CAD files (Thorlabs STEP files, objective) | https://github.com/hacker-fab/stepper_cad |

The projector model (`SPEC_800-0255-A_F16D`) is in the Onshape assembly. To get it, export the full assembly as STEP. This repository reads it from `vendor/projector.brep`, which is not committed.

Onshape element ids for the adapter plate: `0e8c1f104c4c4708545e72bb` (aluminium), `6aae798fd8c31fe1bc320fe1` (3D print).

## Datasheets and drawings

| Item | Link |
|---|---|
| TI DLPDLCR471TPEVM product page | https://www.ti.com/tool/DLPDLCR471TPEVM |
| TI user's guide DLPU105 | https://www.ti.com/lit/pdf/DLPU105 |
| TI Front-End (side) Board design package | `dlpc147.zip`, https://www.ti.com/lit/zip/DLPC147 (TI sign-in necessary) |
| TI Formatter Board design package | `dlpc145.zip` (the user has this file; drill file `DLP046B-1-10-np.drl`) |
| ZWO ASI174MM product page | https://www.zwoastro.com/product/asi174mm-mono |
| ZWO ASI174MM manual (drawing on page 17) | https://cdn.shopify.com/s/files/1/0652/6245/2965/files/ZWO-ASI174MM-Manual.pdf |
| ZWO ASI174MM mechanical diagram | https://i.zwoastro.com/wp-content/uploads/2022/07/85140bf03e5491a08424460f8f8ba675.jpg |
| ZWO ASI174MM manual (APM copy) | https://www.apm-telescopes.net/downloads/manuals/ASI174MM.pdf |
| ZWO STEP files (none for the ASI174MM body) | https://www.zwoastro.com/software/step-files-for-zwo-products/ |
| Stepper motor 17HM15-0904S, manufacturer's page (STEP file: download by hand) | https://www.omc-stepperonline.com/index.php?route=product/search&search=17HM15-0904S |
| Edmund 10X DIN Plan objective, #43-907 | https://www.edmundoptics.com/p/10x-din-plan-commercial-grade-objective/5386/ |
| Thorlabs SM1 tube catalogue page | https://thorlabs.com/catalogpages/V21/152.PDF |
| Thorlabs CP90F (shows the 1.2 inch tube bore) | https://www.thorlabs.de/catalogpages/Obsolete/2019/CP90F-F.pdf |
| 2020 extrusion datasheet (copy) | https://fab.academany.org/2021/labs/agrilab/students/antonio-anaya/files/week10/profile_alum_2020_datasheet.pdf |

Thorlabs drawings. Prefix each with `https://media.thorlabs.com/globalassets/items/s/sm/sm1/`. For the STEP file, replace `.pdf` with `.step`.

| Part | Drawing |
|---|---|
| SM1A53 | `sm1a53/itn000795-e0w.pdf` (STEP file: same name, `.step`) |
| SM1L03 | `sm1l03/0823-e0w.pdf` |
| SM1L05 | `sm1l05/0370-e0w.pdf` |
| SM1L10 | `sm1l10/0371-e0w.pdf` |
| SM1V05 | `sm1v05/0591-e0w.pdf` |
| SM1V10 | `sm1v10/0592-e0w.pdf` |
| SM1CPL05 | `sm1cpl05/ttn112022-e0w.pdf` |
| SM1A9 | `sm1a9/8742-e0w.pdf` |
| SM1A3 | `sm1a3/0165-e0w.pdf` |

## Optics and electronics that the user has

| Item | Qty | Link |
|---|---|---|
| TI DLP EVM (DLPDLCR471TPEVM) | 1 | https://www.ti.com/tool/DLPDLCR471TPEVM |
| ZWO ASI174MM camera | 1 | https://telescopescanada.ca/products/zwo-asi174mm-usb3-0-mono-astronomy-camera |
| Beamsplitter cube, 50/50, 30 mm | 1 | https://www.amazon.ca/dp/B0B34H1HFS |
| 10X DIN Plan objective | 1 | https://www.edmundoptics.ca/p/10x-din-plan-commercial-grade-objective/5386/ |
| Lens tube SM1L03 | 1 | https://www.thorlabs.com/item/SM1L03 |
| Lens tube SM1L05 | 1 | https://www.thorlabs.com/item/SM1L05 |
| Lens tube SM1L10 | 1 | https://www.thorlabs.com/item/SM1L10 |
| Tube coupler SM1CPL05 | 1 | https://www.thorlabs.com/item/SM1CPL05 |
| Adjustable tube SM1V05 | 1 | https://www.thorlabs.com/item/SM1V05 |
| Adjustable tube SM1V10 | 1 | https://www.thorlabs.com/item/SM1V10 |
| C-mount adapter SM1A9 | 1 | https://www.thorlabs.com/item/SM1A9 |
| RMS adapter SM1A3 | 1 | https://www.thorlabs.com/item/SM1A3 |
| Flange SM1A53 | 1 | https://www.thorlabs.com/item/SM1A53 |
| UV LED, Lumileds L1F3-U400200012000 | 4 | https://www.digikey.com/en/products/detail/lumileds/L1F3-U400200012000/7389568 |
| Molex Pico-SPOX 10-position connector | 3 | https://www.digikey.ca/en/products/detail/molex/0874371043/717647 |
| Power supply, 19 V 4.74 A | 1 | https://www.amazon.com/dp/B074J81XRB |
| Power supply, 12 V | 1 | https://www.amazon.com/dp/B01GEA8PQA |
| Wafer, UniversityWafer item 1830 (100 mm, 525 µm) | - | no link recorded |

## Frame, screws and print material to buy

| Item | Link |
|---|---|
| 2020 T-slot extrusion, 4 × 500 mm | https://www.amazon.ca/dp/B08CMZ2D8N |
| Corner brackets, 20 pieces, with M5 T-nuts and screws | https://www.amazon.ca/dp/B09T6XML24 |
| M5 T-nuts and screws, 210 pieces (Taiss) | https://www.amazon.ca/dp/B0DPF94TD2 |
| M3 screws and nuts, 550 pieces (Mywish) | https://www.amazon.ca/dp/B0DJP6C8MF |
| M2 countersunk screws, 210 pieces (Hilitchi) | https://www.amazon.ca/dp/B06Y3M62Z8 |
| Self-adhesive black felt, 10 sheets | https://www.amazon.ca/dp/B0CJJ9L17G |
| Polyimide (Kapton) tape, for the chip | no link recorded |
| Digital caliper, 150 mm | https://www.amazon.ca/dp/B07X8JQ8L5 |
| Matte black PETG, 1 kg (SUNLU) | https://www.amazon.ca/dp/B0FD2ZKHND |

## Micro-manipulator stage (not part of this repository)

| Resource | Link |
|---|---|
| Open Micro-Manipulator repository | https://github.com/0x23/MicroManipulatorStepper |
| Printable STL files | https://github.com/0x23/MicroManipulatorStepper/tree/main/construction/v4_3dprinting_stl |
| Author's video (travel 23 mm, version 3) | https://youtu.be/MgQbPdiuUTw |
| Stepwise project page | https://www.stepwisedocs.com/docs/projects/open-micro-manipulator-13 |
| Stepwise bill of materials | https://www.stepwisedocs.com/docs/projects/open-micro-manipulator-13/guides/bill-of-materials-72 |
| Stepwise rod manufacturing guide | https://www.stepwisedocs.com/docs/projects/open-micro-manipulator-13/guides/precision-ball-joints-rods-manufacturing-process-73 |
| Stepwise assembly guide | https://www.stepwisedocs.com/docs/projects/open-micro-manipulator-13/guides/micro-manipulator-assembly-instructions-74 |
| Stepper motor, 42 × 42 × 39 mm (3 in use) | https://www.amazon.ca/dp/B00W98OYE4 |
| Printed stand (`demoStandV1.stl`). The stage base in this repository holds it. | https://github.com/koalazak/MicroManipulatorStepper/tree/stl-extras/construction/v4_3dprinting_stl/extras |
| Hacker Fab build notes for the micro-manipulator | https://docs.hackerfab.org/home/fab-toolkit/submodules/nanopositioner/micromanipulator |
| Motor driver TB6612FNG, 2 in a pack (3 drivers necessary) | https://www.amazon.ca/dp/B09MN94LVF |
| Author's answer on other drivers (issue 42) | https://github.com/0x23/MicroManipulatorStepper/issues/42 |

The repaired jig files `RodGrindingJigA_repaired.stl` and `RodGrindingJigB_repaired.stl` are in the source chat. Use them, not the GitHub jig files.

## Printing

| Resource | Link |
|---|---|
| Hatchery 3D printing at Myhal | https://hatchery.engineering.utoronto.ca/3d-printing/ |
| U of T Libraries: 3D printing labs on campus | https://guides.library.utoronto.ca/3Dprinting/campus |

## Source of the requirements

| Resource | Link |
|---|---|
| Chat "Optics fundamentals for projector build" | https://claude.ai/chat/a7b60fbc-24f1-469c-8fbb-e08b27deac88 |
| Handoff file from that chat | `STEPPER_PRINTED_PARTS_SPEC.md` (chat output; its facts are in [docs/dimensions.md](docs/dimensions.md)) |
