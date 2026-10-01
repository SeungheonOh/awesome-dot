# Fictional room-layout comparison

All values and source labels below are invented for this demonstration. No actual room was measured, product checked, furniture moved or purchase made.

## Request and source ledger

```text
Compare A and B using my supplied rectangular footprints. Keep a 90 cm
entry route and the desk's 80 cm deep working zone empty. Furniture must
not touch other furniture or room walls. Boundary contact with a protected
zone is allowed, but nothing may project into it. Do not move or buy anything.

F1: simulated owner tape-measure worksheet, 2026-09-30, all values in cm
    Usable room: 420 wide x 320 deep, rectangular, no reported intrusions
    Desk: 140 wide x 60 deep, rectangular, front faces south
    Sofa: 180 wide x 80 deep, rectangular, front faces north
    Bookcase: 80 wide x 30 deep, rectangular, front faces south at 0 degrees
    Side table: 40 wide x 40 deep, rectangular, no directional operation
    South-wall opening: x = 0 to 90, y = 320; inward opening
    Reading precision and measurement/placement uncertainty: not supplied

F2: simulated user clearance instructions attached to F1
    Entry route: x = 0, y = 0, width = 90, depth = 320
    Door operating reserve: x = 0, y = 230, width = 90, depth = 90
    Desk working reserve: whole desk width, 80 deep immediately south of desk
    These are user-specified rectangular reserves, not regulatory thresholds

F3: simulated user candidate placements (northwest anchor after rotation)
    A: desk (100,5), 0 degrees; sofa (160,235), 0 degrees;
       bookcase (385,10), 90 degrees clockwise; table (345,275), 0 degrees
    B: same except sofa (170,115), 0 degrees
```

## Result

Candidate A is feasible at the supplied nominal dimensions. Candidate B is rejected because its sofa enters the desk's required working zone. Neither is a verified physical fit: uncertainty, protrusions and delivery-route dimensions remain unresolved.

The origin is the inside northwest corner; x increases right/east and y increases down/south. These are plan directions. Coordinates and dimensions below are in cm. A 90° clockwise rotation changes the bookcase from 80 × 30 to 30 × 80, with its front facing west.

```text
Candidate A    x    y   base w,d   rotation   resulting w,d   east,south
Desk         100    5    140,60       0          140,60          240,65
Sofa         160  235    180,80       0          180,80          340,315
Bookcase     385   10     80,30      90           30,80          415,90
Table        345  275     40,40       0           40,40          385,315

Reserves                    x    y      w     d        east,south
Entry route                 0    0     90   320          90,320
Door operation              0  230     90    90          90,320
Desk work                 100   65    140    80         240,145

Candidate B changed row:
Sofa         170  115    180,80       0          180,80          350,195
```

### Checks and the reason to reject B

- A: every item and required reserve is inside the rectangular room. No two furniture footprints overlap or touch. No furniture has positive-area overlap with a protected reserve
- A: the desk meets its working reserve at y = 65. This permitted boundary contact is not an obstruction. The entry strip connects the complete supplied south-wall opening to y = 0, and contains the door reserve
- A: the smallest nominal furniture-to-wall gap is 5 cm. This is a calculated gap, not a supplied tolerance or promised allowance. The bookcase's east edge is 415, leaving 420 − 415 = 5 cm
- B: all furniture still fits within the room and no furniture pair intersects. The sofa's x interval [170,350] intersects the desk-work interval [100,240] by 70 cm. Its y interval [115,195] intersects [65,145] by 30 cm. Obstruction = 70 × 30 = 2,100 cm². Reject B even though its furniture-only collision check passes

### Unresolved before moving or buying

```text
Need                           Why it matters
Measurement uncertainty and    Cannot establish a worst-case fit or say the
desired extra margin           5 cm smallest wall gap absorbs all errors
Wall squareness/baseboards,     F1 reports a rectangle but has no independent
item protrusions               check of the maximum usable/occupied envelopes
Bookcase operating needs       Only a static rotated footprint was supplied;
and relevant height limits     no door/drawer/vertical clearance is established
Delivery route and item        The south opening's nominal width does not
handling/assembled dimensions  establish that any item can be brought inside
```

Keep A as the nominal candidate to verify. B needs the sofa repositioned away from the desk-work zone before reconsideration. No claim is made about comfort, emergency egress, legal/accessibility compliance, structural capacity or actual installation.

## Schematic and local verification

[candidate-a.svg](candidate-a.svg) depicts A from the exact checked coordinates. Shaded reserves intentionally overlap. It omits unmeasured geometry and cannot resolve the unknowns above.

Run the fixture check from this folder with an existing Python 3 interpreter; no third-party packages are required:

```sh
python3 check_example.py
# Regenerate the schematic from the checked fixture, if needed:
python3 check_example.py --write-svg
```

The checker asserts the expected A/B outcomes, exact obstruction width/depth/area, width/depth rotation, negative/out-of-room coordinates, connected entry route, permitted and prohibited edge/corner contact, positive-area collision, invalid dimensions and non-finite/float input rejection. It also parses the SVG and compares its furniture/zone rectangles and opening endpoints to the fixture.

Observed on 2026-10-01 with Python 3.12.14: both commands above passed, as did the skill-frontmatter validator. The SVG passed XML, labeling-reference and coordinate-parity checks. It was also rendered at 920 × 870 pixels using the existing librsvg/Cairo libraries and visually checked: labels were readable and unclipped, with distinct furniture and reserve zones. These checks exercise only this fictional, rectangular, nominal model. They do not validate real measurements, arbitrary polygons, tolerance envelopes, vertical clearances, moving/operating envelopes or delivery fit.
