---
name: home-maintenance-record
description: "Build or reconcile a household maintenance record from service evidence and model-matched guidance, keeping completed work, unknown history and proposed reviews distinct."
---

# Keep a Home Maintenance Record You Can Trust

Make it easy to answer what was done, when it was done, what supports that record and what needs review next. Avoid turning an old guess or a suggested interval into a false history of completed work.

## When to use

Use for a private record of ordinary household equipment and low-risk routine care, especially when receipts, manuals and informal notes disagree. The workflow produces and, when requested, updates the actual private record from authorized sources. It does not diagnose failures or prescribe hazardous repairs. A recordkeeping request alone does not authorize service bookings, purchases or reminder setup.

## Intake records

Create an asset list with a stable neutral label, asset type, manufacturer and model when necessary, responsible person label and exclusions. Room labels are generally sufficient; street addresses, serial numbers and entry details are not needed.

For each history entry record asset, task, event date, date precision, status, evidence reference and source date. Keep status explicit: documented completed, user-reported completed, proposed, canceled or unknown. Record the requested review horizon and output format.

For each care rule record task, applicable model, source and retrieval or supplied date, interval value and unit, starting event, operating-condition qualifiers and any stated calendar convention. A model mismatch or unknown starting event is a gap to resolve, not a reason to borrow the nearest-looking rule.

## Workflow

### Reconcile the history without inventing it

1. Read authorized service notes and receipts. Extract the performed-on date separately from invoice, payment, booking and document-upload dates. An estimate or paid deposit does not establish completion. Preserve source references down to the relevant page or line so a later correction can be traced.
2. Match entries to the right asset and task. Similar appliance names or identical receipt amounts are insufficient to merge events. Use model, task, date and explicit source links together. Keep suspected duplicates in a review queue; do not count the same event twice when its identity is confirmed.
3. Resolve disagreements by exposing both claims and their evidence. A service report explicitly naming work and date can support a documented completion, while a contradictory informal note remains visible. If two credible sources disagree materially, mark the last confirmed date unresolved. Do not use “newest file wins,” and do not erase the rejected version of a claim from the audit notes.

### Connect the next review to an actual rule

4. Read the supplied manufacturer instructions or retrieve official guidance when the task calls for current research. Record the exact model match and source date. Separate required care, condition-dependent advice and the user's optional planning interval. If the manual is unavailable, prepare an evidence request or an explicitly labeled planning proposal; do not attribute the proposal to the manufacturer.
5. Match each interval to its stated anchor. A rule based on operating hours needs a trustworthy usage reading; calendar dates cannot substitute for it. A condition-based check may need a user observation rather than an exact due date. A seasonal recommendation may produce a review period, not a day-specific deadline. Preserve those distinctions in the output.
6. Calculate the next review only when the anchor and rule are adequate. Show the last qualifying event, interval, calendar convention and result. Month arithmetic must preserve calendar meaning: do not replace three months with 90 days. Resolve end-of-month and leap-day behavior from the source or a clearly identified user planning choice. If completion is known only to a month, retain a candidate date range or ask for precision rather than inventing a day.
7. Stop the calculation chain at the next unperformed task. A proposed April review cannot become a completed April service that generates a July due date. After the user supplies actual completion evidence, recalculate affected tasks from that event using the rule's correct anchor. Do not reset unrelated tasks on the same asset.

### Produce the useful review list

8. Filter known upcoming reviews against the requested horizon. Separate overdue-by-evidenced-rule, upcoming, unknown-history, model-mismatch and professional-review items. Explain the basis of ordering; uncertain history alone is not proof that an asset is dangerous. Where safety-critical symptoms are reported, flag the need for appropriate qualified assistance and avoid troubleshooting or repair instructions that could cause harm.
9. Save a new private record or update the specifically authorized existing one. Preserve stable asset and event identifiers and a concise change record. Keep source documents unchanged. If the requested editable format is unavailable, return a readable table with the same data rather than claiming a live workbook or connected system exists.

## Output contract

Return an editable asset-and-task log, a history ledger with evidence links, a rule register, calculated next-review dates or ranges, and a prioritized unresolved-evidence list. Every next-review row must identify its anchor and basis. Each unknown needs a practical next step: find the model manual, confirm an event date, obtain a usage reading or ask the responsible person.

## Verification

- Recalculate each date from its evidenced anchor and compare it with the saved output
- Check a month-end, conflicting date and unknown-history case; keep unresolved values visible
- Confirm no invoice date was substituted for service date and no proposed row became completed
- Check that a new receipt changes only the matching task and preserves older evidence
- Reopen the artifact and verify source links, status labels and formulas where applicable

The [fictional worked example](example.md) shows model-specific calendar arithmetic and why a quote cannot fill a gap in service history.

## Stop and ask

Ask for a material missing model, interval anchor, calendar convention or conflicting completion date. Continue assembling the independent history while those calculations are blocked. Keep electrical, gas, structural and other safety-critical diagnosis or repair outside this administrative workflow. Honor ordinary record edits and delivery to a private destination already specified by the user without repeated approval. If the same request includes bounded reminder setup or an authorized routine inquiry, verify the relevant service capability and carry out that explicitly requested action; do not treat the recordkeeping scope as a reason to abandon it. Ask for material missing schedule details or any still-required approval before a purchase, service commitment or sensitive sharing.

## Example request

```text
dot, turn these sanitized maintenance notes and manuals into a private household record. Separate documented work from things I only remember doing, and leave unknown dates unknown. Use the correct model's instructions to calculate the next useful review, show the date arithmetic and tell me what evidence is still missing. Do not book anything, order parts or create reminders.
```

## Evidence status

The example uses invented assets and care guidance to test recordkeeping behavior. Real care instructions require applicable source evidence; the record itself is not evidence that physical work occurred.
