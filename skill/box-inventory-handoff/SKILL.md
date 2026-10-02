---
name: box-inventory-handoff
description: "Reconcile household records into an item-to-box inventory, partial packing checklist, minimal destination labels and a handoff/unpacking sheet while preserving quantities, reservations and evidence."
---

# Know What Is in Which Box

Turn the user's authorized item lists and packing updates into a usable physical-box record. Show what is planned for each box, what someone reports packing, what has actually been directly checked, and what must stay accessible. A completed plan is not a packed home.

This workflow tracks physical quantities and container locations. It does not organize digital files, infer which belongings to take on a trip, determine whether furniture fits a room, or settle who owes a borrowed item back.

## Start with the real collection

Use the actual selected notes, lists, images, messages or existing private inventory that the user authorized. Establish the scope of the pass, the latest relevant packing update, the requested output destination, and who will see the working inventory, handoff sheet and outside labels. Keep the existing inventory's IDs and format when updating it. Do not search unrelated household records to fill gaps.

Collect only what changes the result:

- Source IDs, relevant line/image/message locators, and observation/event dates separately from entry dates
- Item labels, counts and units; evidenced distinguishing marks when individual copies matter
- Existing box IDs, user-supplied destination rooms and any room-code key
- Items or quantities to leave unpacked, reserve for a person/purpose, or exclude from this pass
- Actual packing, removal, transfer and unpacking reports, including which box and quantity they concern
- The requested handling of ambiguous records and the authorized save/share destination

For missing counts, keep “quantity unknown”; for unclear destinations, use “room unresolved” in the private review list. Continue clear rows. Ask a targeted question only where the answer changes identity, quantity, assignment or the release of a reserved item. Do not manufacture weights, box capacity, safe lifting limits, fragility, protective packing instructions, internal contents or item identity from a vague description. A photograph without a usable scale does not supply dimensions, and a partly visible pile does not establish its total count.

The [worked packet](example.md) is fictional. Replace its data with real authorized records; none of its box assignments or quantities is a default.

## 1. Preserve claims before combining items

Create a compact source-claim register. Preserve each source ID and locator, its minimum relevant claim, date precision, and one disposition per claim: applied, supporting duplicate, superseded by a stated correction or clearly ordered replacement count, unresolved, or outside scope. Re-importing the same unchanged source ID must not create another item or packed quantity. Changed content under the same ID is a source revision to review.

Create stable item IDs for evidenced physical units or countable pools. Six identical mugs can be a six-piece pool when the source establishes that pool; do not invent six distinguishable identities. Conversely, two lamps with different supplied markings must stay separate even if their descriptions are similar. Assign a neutral ID to a documented distinguishing mark, not to a guess.

Handle uncertain matches explicitly:

- The same stable record imported again is duplicate evidence, not more inventory
- A second note explicitly referring to the same six mugs supports that pool; six more is not implied
- Similar names, matching photos or a shared room alone do not prove either duplication or distinctness. Retain the candidate matches and exclude the ambiguous claim from the confirmed quantity until resolved
- “One utensil pouch” establishes one pouch only. Its contents remain unenumerated; do not also invent or count the utensils inside it
- A correction can change one count or box assignment while leaving the rest of its source valid. Retain the corrected claim and the source that supersedes it

When both a container and its enumerated contents appear, record the parent/child relationship. Do not add their quantities into a misleading “total items” figure. Keep unlike units, unenumerated sets and unresolved pools separate.

## 2. Keep the plan separate from physical-state evidence

Maintain these small linked records in the requested format; Markdown tables are sufficient:

| Record | Minimum fields |
|---|---|
| Item | Item ID, supplied label, known quantity/unit or unknown, source locators, unresolved identity links |
| Reservation | Item ID, quantity/unit, leave-unpacked or reserved instruction, source, release condition if explicitly supplied |
| Box | Stable box ID, destination room/code, room source, label revision, closure/seal state if reported |
| Planned allocation | Item ID, box ID, quantity/unit, plan source or clearly labeled proposal |
| Physical observation | Item ID, box or outside location, quantity/unit, reported or directly verified, effective date/order, evidence locator and scope |
| Change/review | Affected records, previous claim, new claim, correction/transfer/reversal reason, source and unresolved question |

Reservations reduce what the plan may allocate, but do not prove where items physically are. An item can be reserved yet reported packed by mistake. Flag that conflict; do not silently release the reservation or rewrite the report. “Leave unpacked until Friday” needs a reliable date anchor and a release instruction, not an automatic packing action.

Use three evidence levels without treating them as additive quantities:

1. **Planned:** assigned to a box on paper; no physical packing claim

2. **Reported packed:** a source explicitly says a stated quantity is in that box. Record whose label/source and when; the assistant reading a count is still reading a report

3. **Directly verified:** the assistant's authorized observation clearly establishes the specific items, count and identifiable box at that moment. Record exactly what was visible and what was not. A closed box or its handwritten contents list verifies neither hidden contents nor their count

Direct verification is a property of a specific current observation, not an extra pile to add to the reported quantity. Do not add two observers' counts, two overlapping photos or repeated “still packed” reports. After an evidenced transfer, removal or possible change since inspection, retain the old verification in history and qualify or replace the affected current state. A report that a box was sealed or received can be recorded without upgrading its contents to verified.

## 3. Allocate quantities and reconcile partial packing

Reuse the user's existing box IDs. For new boxes, propose neutral unique IDs such as B01 and make clear that their physical labels still need to be applied by a person. Do not claim a proposed box exists. Use the user's room vocabulary; two rooms both called “bedroom” need distinct supplied names/codes before routing labels are final.

For each item with a known compatible unit:

```text
available to plan = in-scope quantity - reserved/leave-unpacked quantity
unallocated for plan = available to plan - sum(planned box quantities)
```

Require nonnegative integer counts for discrete pieces. Validate other supplied units in their own units; never silently convert a “set” into pieces. Require total reservations not to exceed the known in-scope quantity and planned allocations not to exceed the remainder. Unknown quantities cannot pass a numeric conservation check.

Then reconcile physical evidence independently. Assign a physical unit to at most one current location. Use a specific later transfer/removal/correction to supersede the affected earlier observation. An explicitly ordered current-count observation can also replace the earlier counts for the item and locations it covers: “B1 still has three; B2 now has five; these are the counts now” is a replacement snapshot, not eight newly packed pieces. Retain the earlier evidence and any unexplained movement history; do not invent a transfer to explain the new counts or refresh locations outside the stated scope. Unmentioned locations remain last-known evidence, not newly established unchanged counts. If the new observation could overlap their units or leave an unexplained movement, hold the affected combined tally until reconciled. A newly uploaded note without clear event order does not automatically win. Keep two incompatible box claims unresolved instead of choosing the larger count or summing them.

```text
unaccounted quantity = in-scope quantity
                    - nonoverlapping current packed quantity
                    - explicitly accounted-for outside quantity
```

This remainder is unaccounted for, not proven unpacked or missing. If the evidence claims more than the known scope, or two locations could describe the same units, hold the affected tally for review. Do not conceal the conflict by clipping quantities or increasing the baseline without a source.

While the packing plan is active, show progress per item and box: planned amount, current reported/verified amount, and the difference to review. Distinguish an unexplained packing shortfall from a source-explained deviation such as a later transfer, deliberate removal or unpacking. A negative difference is an over-plan exception; extra packed stock is not permission to take reserved stock. Split quantities may span multiple boxes. A box can be partly packed while one item allocation is complete. Do not mark a whole box complete from one “done” message unless that message clearly covers its complete current manifest and no unresolved change remains.

Physical capacity and handling remain separate from this arithmetic. The user or packer must establish that the plan is physically suitable. Leave supplied handling instructions exactly scoped and sourced; do not create “fragile,” weight or orientation labels from item categories alone.

## 4. Run a focused review loop

Return the clear item-to-box map, reservations and the smallest unresolved questions. A useful question cites the competing records: “Does the hallway ‘lamp, 1’ refer to the blue-tape lamp already listed, or another lamp?” Do not ask the user to reconfirm every clear line.

For each answer:

1. Append its source ID and the specific records it changes
2. Identify whether it corrects a past claim, supplies an ordered replacement count, reports a physical transfer, changes a future plan or releases a reservation. These have different effects
3. Recompute only affected counts and location claims; preserve the earlier record and unrelated user edits
4. Show the before/after difference, including still-open questions and evidence that has become stale
5. Regenerate affected labels and sheets from the current revision; identify old copies as superseded

A correction saying “I meant two in each box” repairs an earlier report; it is not evidence of another two items being packed. A real transfer requires an evidenced origin, destination and quantity. If only the arrival is known, preserve that limit rather than inventing a departure transaction. The [example](example.md#review-correction) demonstrates the distinction.

## 5. Produce the working packet

Provide the requested outputs from one reconciled revision:

- **Private item-to-box inventory:** item and source IDs, quantities/units, split allocations, reservations, actual-state evidence, unaccounted remainder and questions
- **Packing checklist:** one row per item allocation with separate planned count, reported packed count, current verified count/status, and space to record a subsequent report or check. Unknown is not zero. Include a leave-unpacked list
- **Outside labels:** box ID and authorized destination room/code only by default. Put no home address, personal names, contents, access codes, QR links or sensitive category hints on labels. Add only explicitly requested useful fields. Do not produce a final routing label for an unresolved room
- **Handoff/unpacking sheet:** each box ID and expected room, current manifest reference/revision, reported closure state, exceptions, and blank fields for received, unpacked quantities and discrepancies. Share detailed contents only with the authorized audience; a carrier may need just box IDs and room codes
- **Review list:** unresolved identities, counts, locations, partial packing and decisions that block completion

Keep outside labels minimal even when the private sheet contains detailed contents. A room name can itself reveal information; use an approved neutral room code if appropriate, with the key kept for the intended recipient. A printable PDF is optional; a text label list is sufficient. If generating a PDF, check the rendered labels, their exact IDs/rooms and the printable margins. Printing, attaching labels and physical packing remain actions for people.

For handoff, distinguish “box received” from “contents checked.” When an unpacking report arrives, move only the stated quantity out of its box in the current location record, retaining its history and destination. A partly unpacked box remains partly populated. Report its remaining contents and explained unpacked quantities separately from any unexplained shortage. Do not call historical planned-minus-current-packed quantity unfinished packing or suggest repacking merely because an authorized unpacking report reduced the box contents; retain the old packing plan as history unless a current plan still requires that packing. An empty-box report without content reconciliation does not settle a shortage or identify what was inside. Do not diagnose theft, damage or responsibility from an inventory discrepancy.

## 6. Save, reopen and check the result

Save only to the requested authorized destination. Read an existing inventory and its revision before editing; if it changed, merge the new rows and preserve intervening edits. Keep stable source, item and box IDs. Never replace a user's record or change access merely because writing to the intended destination failed.

Reopen the saved result and verify:

- Every supplied source has a disposition and locator; repeat imports have not inflated quantities
- Every clear item appears, with ambiguous candidates and unknown units/counts still visible
- Reserved quantities remain outside the allocation plan unless their release is explicitly sourced
- Split allocations and nonoverlapping physical-state quantities reconcile separately; the same source report is not counted twice
- Superseded reports remain in history but do not contribute to current counts
- Reported, planned and directly verified states survived the write without being promoted
- Box IDs and destinations agree across inventory, labels and handoff sheet; regenerated labels identify superseded revisions
- Sharing contains only the fields authorized for that audience; save/readback failures are stated honestly

For an uncertain write response, inspect the destination before retrying. If readback is unavailable, deliver the reconciled draft and call the save unverified. Do not claim the physical contents, packing completion, actual receipt, successful print or delivery from local arithmetic checks.

Finish with the usable packet, the evidence date/revision and the remaining physical checks or user decisions. This task does not authorize packing, lifting or moving objects, buying supplies, booking services, contacting anyone, changing sharing or creating recurring monitoring.

## Example request

```text
Use these household lists and packing notes to update my private box inventory.
Keep the original source IDs, split quantities between boxes where stated,
and leave the reserved items out of the plan. Show what is only planned,
what I reported packed and what has actually been directly checked. Make
minimal room labels and a handoff/unpacking sheet for me. Keep uncertain
matches visible and ask only about the conflicts that change the inventory.
Do not share, contact anyone or arrange any physical work.
```
