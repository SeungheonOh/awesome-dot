# Fictional packing packet: revision 2

This is an original fictional household example. The notes, people-free labels and events below were invented for this workflow. No real belongings, photographs or boxes were inspected. Every current contents claim is **reported**, and direct physical verification is **not established**. Running the accompanying check verifies the records' internal consistency only.

## Supplied records

The source IDs and locators below remain in the output. Event order is explicitly supplied as A, B, C; no timestamp is inferred from when the records are imported. The intake includes S01 a second time with unchanged content and the same ID.

| Source / locator | Supplied claim |
|---|---|
| S01:1 | Inventory: six plain white mugs, counted as one interchangeable pool |
| S01:2 | Inventory: five bath towels, counted as one pool |
| S01:3 | Inventory: one desk lamp with blue tape on its base |
| S01:4 | Inventory: one extension lead with a red tie |
| S01:5 | Inventory: one closed utensil pouch; contents not listed |
| S02:1 | Kitchen note: “Mugs, 6. Same six as S01:1, copied here for the kitchen list” |
| S03:1 | Leave two mugs, one towel and the red-tie extension lead unpacked; no release condition given |
| S04:1 | Plan: B01 Kitchen = two mugs; B02 Kitchen = two mugs and the utensil pouch |
| S04:2 | Plan: B03 Bathroom = four towels; B04 Study = the blue-tape lamp |
| S05:1 | Packing report at A: “Four mugs packed in B01” |
| S05:2 | At A: “Three towels are in B03; blue-tape lamp in B04; the pouch is in B02” |
| S05:3 | At A: “Two mugs, two towels and the red-tie lead are still outside the boxes. One of those towels is reserved; the other is still to add to B03” |
| S06:1 | Separate undated note: “Lamp, 1, hallway” |
| S07:1 | Separate undated note: “box of cables?” |
| S08:1 | Review answer at B: “S05:1 was wrong. It was two mugs in B01 and two in B02. I didn't add any more mugs or move them just now” |
| S08:2 | At B: “The hallway lamp note means the same blue-tape lamp. It is now in B04 as reported. I don't know what the cable note refers to” |
| S09:1 | At C: “B01 and B02 are closed; B03 and B04 are open. No contents changed after B” |

The user's fictional authorization is to prepare and save a private packet for their own review. All four boxes are described by the user as existing. Room names are approved for the outside labels. No sharing or physical work is authorized.

## Review correction

The first pass preserves the explicit pool of six mugs and excludes two from the plan. S05:1 nevertheless places all four planned mugs in B01, leaving B02's two-mug allocation unmet. This is a distribution conflict, not an overall shortage: the two remaining mugs are explicitly outside and reserved.

The review asks: “Should the report put all four mugs in B01, or is the two-in-each-box plan still correct? Also, does S06's hallway lamp mean the blue-tape lamp or a second lamp?”

S08 corrects the current mug report and resolves the lamp match. The before/after record is:

| Field | Before review | Revision 2 | Effect |
|---|---|---|---|
| I01 mug report in B01 | Four, S05:1 | Two, S08:1 | S05:1 superseded for this claim |
| I01 mug report in B02 | No report | Two, S08:1 | Corrected distribution, not another packing event |
| I03 / S06 lamp identity | Same lamp or another; unresolved | Same blue-tape lamp, S08:2 | Supporting record, no extra lamp added |
| S07 cables note | Identity, quantity, container and contents unknown | Still unresolved | No invented item or box |

The plan stays unchanged. The corrected report has four packed mugs across two boxes, plus two explicitly outside. Replaying the same review answer has no further effect.

## Current private item-to-box inventory

All quantities below derive from the fictional sources. “Not established” is not a verified count of zero.

| Item / source | In-scope quantity | Leave unpacked | Planned allocation | Current reported packed | Explicitly outside | Current direct verification |
|---|---:|---:|---|---|---:|---|
| I01 Plain white mug pool / S01:1, S02:1 | 6 pieces | 2 / S03:1 | B01: 2; B02: 2 / S04:1 | B01: 2; B02: 2 / S08:1 | 2 / S05:3, S09:1 | Not established |
| I02 Bath towel pool / S01:2 | 5 pieces | 1 / S03:1 | B03: 4 / S04:2 | B03: 3 / S05:2, S09:1 | 2 / S05:3, S09:1 | Not established |
| I03 Blue-tape desk lamp / S01:3 | 1 piece | 0 | B04: 1 / S04:2 | B04: 1 / S05:2, S08:2, S09:1 | 0 by scoped remainder | Not established |
| I04 Red-tie extension lead / S01:4 | 1 piece | 1 / S03:1 | None | None reported packed | 1 / S05:3, S09:1 | Not established |
| I05 Closed utensil pouch / S01:5 | 1 pouch | 0 | B02: 1 / S04:1 | B02: 1 / S05:2, S09:1 | 0 by scoped remainder | Not established |

The lamp/pouch rows' outside zero is a consequence of their explicit one-unit scope and current one-unit box report, not an observation of the entire home. The pouch's internal contents remain unknown. S07 is unresolved outside the confirmed inventory; there is no claim that all household belongings have been accounted for.

## Packing checklist for this revision

| Allocation | Planned | Reported packed | Current verified quantity | Still to confirm against plan | Follow-through |
|---|---:|---:|---|---:|---|
| I01 → B01 | 2 pieces | 2 | Not established | 0 | Counts agree on paper; contents not directly checked |
| I01 → B02 | 2 pieces | 2 | Not established | 0 | Corrected report S08:1 retained |
| I02 → B03 | 4 pieces | 3 | Not established | 1 | One explicitly outside, nonreserved towel remains to pack or replan |
| I03 → B04 | 1 piece | 1 | Not established | 0 | Match to hallway note resolved |
| I05 → B02 | 1 pouch | 1 | Not established | 0 | No assertion about pouch contents |

Leave unpacked: I01 two mugs; I02 one towel; I04 the red-tie lead. Packing the spare nonreserved towel is still a physical task, not something completed by making this list. Do not release these reservations merely because the box plan is ready.

## Minimal outside labels

The [printable candidate](labels.pdf) reproduces exactly these labels. Its page header/footer identify it as a fictional draft; each label contains only a box ID and destination room. It has no contents, address or personal name.

```text
B01  Kitchen
B02  Kitchen
B03  Bathroom
B04  Study
```

The text and PDF represent proposed labels to print and apply. No printing or physical application occurred. Revisions of the private contents report do not change the four box IDs or room labels in this example. If a room later changes, mark the previous routing label superseded and have the user replace it before relying on it.

## Private handoff and unpacking sheet

For the household user's own review, revision 2, evidence through event C. A future recipient's version requires an authorized audience and only the fields they need. “Closed” is a report, not confirmation of a seal or its contents.

| Box / room | Expected contents from current report | Closure report | Exception / unpack check | Received box | Contents checked and unpacked | Discrepancy / source |
|---|---|---|---|---|---|---|
| B01 / Kitchen | I01: 2 mugs | Closed / S09:1 | Check against corrected report S08:1 | ___ | ___ | ___ |
| B02 / Kitchen | I01: 2 mugs; I05: 1 closed pouch | Closed / S09:1 | Pouch contents unenumerated | ___ | ___ | ___ |
| B03 / Bathroom | I02: 3 towels | Open / S09:1 | Plan calls for 4; one nonreserved towel still outside | ___ | ___ | ___ |
| B04 / Study | I03: 1 blue-tape lamp | Open / S09:1 | No second lamp is established by S06 | ___ | ___ | ___ |

At handoff, fill “received box” independently from “contents checked and unpacked.” If someone later reports unpacking two of B03's three towels, record two at the stated unpack destination and one still reported in B03; do not close the whole row. This is a future example of how to update the sheet, not an event in revision 2.

## Source coverage and remaining decisions

| Source | Disposition |
|---|---|
| S01 | Applied baseline, five line-level identities; identical re-import ignored |
| S02 | Supporting duplicate for I01; no extra quantity |
| S03 | Applied reservations; no release supplied |
| S04 | Applied plan and room assignments |
| S05:1 | Superseded by S08:1; retained in history |
| S05:2–3 | Applied current reports, reaffirmed by S09:1 |
| S06 | Supporting duplicate for I03 after S08:2; former ambiguity preserved |
| S07 | Unresolved; no item ID, box ID, count or contents inferred |
| S08 | Applied correction and identity resolution, once |
| S09 | Applied closure report and no-content-change affirmation; does not verify contents |

The next useful decision is whether to add the spare towel to B03 or change the plan. The cable note needs identification only if the user wants it included in this scope. Physical checks remain outstanding for every contents claim. No one has been contacted, no service ordered and no box packed by this workflow.

See [verification.md](verification.md) for executed local checks and their limits. [example-data.json](example-data.json) supplies the compact count/source fixture used by [check_example.py](check_example.py); it is example data, not a required storage format for real requests.
