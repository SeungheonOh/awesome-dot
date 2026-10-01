---
name: borrowed-item-return-ledger
description: "Reconcile lending and return notes into a current physical-item ledger, preserving individual copies, separate loan cycles, partial returns and unresolved evidence; save requested updates with readback."
---

# Know What Is Still Lent Out

Answer which particular item is reported with whom, what remains to come back and what the sources actually establish. This is a lending record, not proof of possession, a retail-return calculation or a reminder service.

## Inputs and scope

Use a bounded set of notes, messages or an existing ledger that the user authorized you to read. Establish the assessment date, the supplied item/person labels, and whether the request is a chat reconciliation or an update to a specific existing private ledger. Preserve its native format and stable identity. Ask only for a missing detail that changes the result; reconcile independent items while others remain unresolved.

Use labels already supplied by the user or ledger. If a physical copy needs a stable ID, attach a neutral ID to its evidenced distinguishing feature, such as the red sticker. A title, model or matching photo description alone does not distinguish copies. A person's name, nickname or initials alone do not justify matching them to a contact or another borrower record. Keep unknown labels unknown; contact details, addresses, serial numbers and reasons for borrowing are usually unnecessary.

Read the [fictional example and executed checks](example.md) for a late-entered return, two identical titles, a partly returned set and a repeated ledger update.

## 1. Separate sources, events and lending cycles

Keep these identities distinct, using the ledger's existing columns or a small accompanying history:

- **Source:** stable reference plus line/message locator, source date, date recorded and the minimum relevant claim
- **Item:** one physical copy or a specifically described set, with the components or quantity actually lent
- **Loan cycle:** one actual lending episode for that item, with lender/borrower direction when needed, borrower label, handover date and promised return date; both dates may be unknown
- **Event:** checkout, return, promise change, correction, ongoing-loan report, proposal or cancellation, linked to its source and the affected cycle/components

Give a returned-and-reloaned item a new cycle even when the borrower is the same. Do not erase its earlier cycle. A report of an ongoing loan can support a cycle with an unknown start date; it does not establish a dated checkout. Do not silently convert a proposal into a loan or a plan to collect into a return.

Record event time separately from message, upload and entry times. Preserve original date precision and wording. Resolve “Friday” only when a reliable source date, context and relevant locale support it; the date someone filed an undated note is not an anchor. Do not manufacture a return date for an item that has no promise.

## 2. Reconcile events to the right cycle

1. Read the selected sources completely enough to identify their item, event and cycle. Account for every source as new evidence, additional support for an existing event, unresolved or outside the requested scope. Re-reading the same source must not add another checkout or subtract another return.
2. Match a return to a physical copy and cycle using explicit evidence. If two copies or cycles fit, hold the return with its candidate set and ask the smallest useful question. Do not close the newest open loan simply because its title matches. A late-entered return from an old cycle must stay in that cycle, even when recorded after a newer checkout.
3. Preserve disagreements. A later file is not automatically a later event or a better source. An explicit correction may supersede a particular field or event; retain what it corrected and why. Two conflicting claims without a clear correction remain unresolved. Mark the affected current custody claim as uncertain rather than presenting an unqualified “with borrower” result.
4. Apply dated events only when their sequence is possible. A return before the matching checkout, two overlapping loans of the same physical component, a promise change that could refer to either cycle, or indistinguishable same-day events needs review. Do not invent a handoff between borrowers to repair the history. Missing dates can leave ordering unresolved even when individual claims are understandable.
5. Reconcile components or quantities within each cycle. For each known component: outstanding = checked out − specifically returned. Require 0 ≤ returned ≤ checked out. A case returning does not establish that its contents returned. Close the cycle only when all lent parts are accounted for, or an explicit whole-set return establishes that fact. Keep an unverified set composition unresolved rather than treating an unspecified “set” as complete.
6. Apply an evidenced promise change only to its cycle and stated components. Preserve the earlier promise and source. A proposed extension is not an agreed change unless the source establishes the relevant commitment. A change to the battery's date must not change another loan's date or make already-returned parts outstanding again.

## 3. Produce the current ledger

Show one row per active cycle, plus relevant returned/proposed items so none silently disappear. Use separate rows for components with different dates. Include:

| Field | What belongs here |
|---|---|
| Item and cycle | Stable IDs plus readable physical-copy label |
| Reported custody | Supplied borrower/lender label, or unknown; distinguish last report from verified current possession |
| Outstanding | Named parts or quantity, including unknown composition |
| Dates | Checkout date/precision and current reported promised date, each with source |
| State | Reported on loan, partly returned, reported returned, proposed only or unresolved |
| Evidence | Applicable events and sources, including conflicting or ambiguous claims |
| Next clarification | Smallest question that would resolve the missing fact |

Compare a known promise with the assessment date only for still-outstanding parts. Prefer “recorded return date passed” to an accusation. A date-only promise supports “due today” on that date, not a fabricated midnight cutoff. If return or date evidence is uncertain, qualify the comparison rather than confidently calling the person late. A completed cycle keeps its history but is not an outstanding obligation.

Lead with the useful result: the reported outstanding items/parts, uncertainty that changes that result, and the few clarifications needed. Separate historical ambiguity from current uncertainty when a later specific return settles current custody without explaining an earlier vague note.

## 4. Save a requested update and verify it

An instruction to update the already-authorized ledger covers ordinary bounded edits; do not repeatedly ask for the same approval. Keep its file/record identity, existing item/cycle/event IDs, access and unrelated rows. Preserve source material and the earlier history; append corrections and evidence rather than rewriting the past into a cleaner story.

Before writing, read the existing ledger by stable identity and note its revision or modification state. Merge new source IDs idempotently. The same ID with changed content is a revision to review, not a duplicate to silently discard. If the ledger changed since the read, reconcile the intervening edits before saving; do not overwrite another person's work.

After saving, reopen the same destination and verify:

- New evidence appears once, existing identities/history remain, and unrelated rows are unchanged
- Each outstanding count reconciles to the cycle's actual checkout and return events
- The late old-cycle return did not close a newer cycle, and same-model copies remain distinct
- Unknown borrower/dates, partial sets and unresolved claims survived the save
- The visible current rows match the event history and the intended bounded change

For a timeout or ambiguous write result, inspect the destination before retrying. If readback is unavailable, report the save as unverified and provide the reconciled result without claiming the live ledger is current. Do not create a replacement ledger, move it to another service or change sharing merely because the requested destination is unavailable.

## Boundaries and completion

Finish when the authorized sources reconcile to the current ledger and history, unresolved claims are visible, and any requested write has a verified result or a clearly reported blocker. This workflow does not authorize contacting borrowers, accusations, purchases, calendar entries or persistent monitoring. Carry out an independently requested routine action only within its actual authority; ask for any missing recipient, content, timing or permission before that action.

## Example request

```text
Use these lending notes to update my existing private item ledger. Keep the two
copies of the field guide separate, preserve previous loans, and show exactly
which parts of the kit are still outstanding. Leave unclear names and dates
unresolved. Save to the same ledger and read it back. Do not message anyone or
create reminders.
```
