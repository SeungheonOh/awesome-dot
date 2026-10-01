---
name: room-layout-fit-check
description: "Compare proposed furniture layouts from supplied room and item measurements, check footprints and user-defined clearances, and return a coordinate plan with unresolved measurements before anything is moved or bought."
---

# Check a Room Layout Before Moving Anything

Compare the user's candidate placements against measured geometry and the space they want to keep clear. Return a readable plan, the exact reason each candidate passes or fails, and the measurements still needed. This is a planning check, not purchasing, construction, structural, medical, or accessibility advice. Do not claim building-code, legal, accessibility, or evacuation compliance.

## Establish the measured model

Use actual authorized inputs for a real request; the [worked example](example.md) is entirely fictional. Record each value's source, date or version where available, units, measurement endpoints, and whether it is measured, supplier-specified, estimated, or unknown. Do not present a supplied value as something you measured or independently verified. A photo may help identify objects or questions, but cannot supply exact dimensions or reliable scale.

Collect only what changes the decision:

- Room's usable interior outline, including recesses, columns, built-ins, baseboards and other relevant intrusions. A rectangular room needs width and depth; an irregular outline needs a measured polygon or explicitly verified free-space regions
- Each item's maximum assembled footprint, shape, protrusions and operating state, such as drawers open or chair pulled out. Record height when a window ledge, sloping ceiling or another vertical constraint matters
- Doors and openings: wall, endpoints, width, opening direction, and supplied operating/swing reserve. Record windows, vents or other areas the user wants unobstructed
- Candidate positions, allowed rotations, which side faces forward, and any items fixed in place. Ask for missing positions or propose clearly labeled positions if layout generation is requested
- User-defined protected routes and clearance zones, their exact widths/extents, and what each connects or serves. Confirm whether boundary contact is permitted; do not invent a universal walkway or accessibility width
- Measurement uncertainty, placement tolerance and extra margin the user wants. Preserve unknowns rather than assuming zero uncertainty

Missing critical dimensions prevent a fit verdict for the affected area. Continue the known checks and list what to measure, from which reference edge, and why. Do not silently omit an unmeasured object, substitute zero, or select a convenient orientation. Conflicting sources remain visible until the user chooses or remeasures.

## Make the coordinates unambiguous

1. Choose one unit and one origin. For a rectangular plan, use the inside northwest corner, x increasing east/right and y increasing south/down. Label these directions on the output; they need not match geographic north. Define x/y as the northwest corner of the final, rotated bounding rectangle.
2. Convert using exact decimal values or rational arithmetic. Construct Decimal values from strings, not binary floats; 1 inch = 2.54 cm exactly. Reject non-finite coordinates and non-positive widths/depths. Preserve source precision instead of presenting extra decimal places as measured precision.
3. Record unrotated width/depth and rotation separately. At 90° or 270°, swap width and depth; at 0° or 180°, retain them. Also rotate front-facing and operating-clearance directions. A width/depth swap alone does not describe which side a drawer opens from. Arbitrary angles require polygon geometry and are outside the simple rectangle calculation below.
4. Represent fixed obstacles and protected space separately from furniture. Store a clearance zone's owner and purpose so a moved or rotated desk also moves its required working zone. Overlapping reserve zones are allowed: they describe space to keep empty, not furniture collisions. Verify that the complete required zone lies in usable room space and that route segments connect their stated endpoints without a gap.

## Check every candidate against the same rules

For a rectangle R = (x, y, w, d), its east/south limits are x+w and y+d. In a rectangular room W by D, require x ≥ 0, y ≥ 0, x+w ≤ W, y+d ≤ D. This containment check does not validate an irregular room by its bounding box.

For two rectangles A and B, calculate:

```text
ix = min(A.x + A.w, B.x + B.w) - max(A.x, B.x)
iy = min(A.y + A.d, B.y + B.d) - max(A.y, B.y)
positive-area overlap: ix > 0 AND iy > 0
boundary contact: ix >= 0 AND iy >= 0 AND (ix == 0 OR iy == 0)
overlap area = max(0, ix) * max(0, iy)
```

- Check each furniture footprint against the room, all other items, fixed obstacles, door reserves and protected zones. A candidate can fail a clearance check even when no furniture touches another item
- Report positive-area intersections separately from edge/corner contact. Apply the user's explicit contact rule to furniture pairs and room walls. When a clearance zone already represents a minimum required gap, a boundary touch meets that nominal minimum only if the agreed boundary rule permits it; it leaves no spare margin
- State the blocking pair/zone, coordinates and intrusion distances. Do not accept a drawing that merely looks clear or count unused floor area as proof of a continuous route
- For known uncertainty bounds, test conservative room limits, item/placement envelopes and required clearances. Explain how each bound was applied; do not add or subtract a blanket tolerance twice. With unknown bounds or marginal gaps, report nominal feasibility and the unresolved margin, not a guaranteed physical fit
- Keep irregular shapes visible. A conservative bounding rectangle can provide a sufficient no-overlap check if it encloses the complete item and lies entirely in verified usable space, but an overlap of such boxes may be a false rejection. Use measured polygons or mark that case unresolved; never certify it from a photo

Keep modeled and unmodeled issues separate. A floor footprint does not establish that an item can be carried through doorways, hall turns, stairs or elevators, assembled there, supported by a wall/floor, or used comfortably. Physical delivery routes and relevant vertical/operating dimensions need their own supplied measurements. Do not advise modifications to buildings or safety-critical equipment.

## Return a decision-ready plan

Lead with the most useful result: which candidate meets the supplied constraints, which is rejected, and what prevents a stronger conclusion. Include:

- Input ledger with measurement provenance, units and remaining estimates/unknowns
- Coordinate plan for each candidate: item, x, y, original width/depth, rotation, resulting width/depth, facing and relevant reserve zones
- Checks with specific pass/fail/unknown results; distinguish nominal feasibility from a tolerance-checked result
- User-relevant tradeoffs among passing candidates, without inventing preference weights
- Short unresolved-measurement list and the next decision before moving or buying anything

An optional top-down SVG should be generated from the checked coordinates, with consistent scale, origin, labels and separate furniture/protected-zone styling. Use it as a schematic, not a photorealistic or product-interface mockup. Check the XML and confirm every drawn rectangle agrees with the calculation; clearly label omitted or unknown geometry. A textual coordinate plan is sufficient.

Reopen the output and verify that all supplied items, openings and constraints appear, rotations agree between plan and checks, and a rejected candidate has not been shown as approved. Retain full calculation precision through the checks; round only the display, without rounding a failure into a pass.

Stop after the requested comparison and clarification list. It does not authorize purchases, supplier contact, software installation, room alterations or moving furniture. Save/share only to an authorized destination; no external service is needed for the rectangle checks.

## Worked example and bounded verification

[example.md](example.md) contains a nominally feasible layout and a rejected alternative with identical furniture but an obstructed desk-clearance zone. [check_example.py](check_example.py) uses the Python standard library and Decimal arithmetic to verify those fictional rectangles, rotation, contact rules, room bounds and input rejection. [candidate-a.svg](candidate-a.svg) is a small schematic derived from the same values. The checker is a fixture, not a general room survey, polygon engine or tolerance solver.

[The L-shaped example](l-shaped-example.md) checks a supplied union of two rectangles. It shows why a solid bounding box can falsely reject a cabinet in an open notch, while actual footprint overlap or prohibited boundary contact still rejects another position.
