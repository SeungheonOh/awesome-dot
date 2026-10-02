---
name: calendar-file-reconciliation
description: "Repair or reconcile supplied ICS calendar files with wrong dates, duplicate components or stale revisions, preserving event and recurrence identity. Produce a parser-checked copy plus exact changes and unresolved holds. Use for offline event-file repair and transfer preparation, not finding meeting times, sending invitations or cleaning a live calendar."
---

# Reconcile a calendar file without changing its meaning

Produce a usable `.ics` copy whose event dates and identities are supported by the supplied evidence. Explain every omitted or changed component. A calendar file can parse successfully while representing the wrong day, reviving a cancelled event, or detaching an exception from its series; validate those meanings as well as its syntax.

Keep the original bytes. Work on copies and finish the bounded file task even when some events must remain held. A request to repair an export does not authorize importing it, deleting existing events, sending invitations or subscribing to a feed.

## Establish the file's intended use

Resolve from the request and files:

- The symptom and one concrete example: what the user expected, what the file encodes, and what the app displayed. A displayed offset can come from the viewer's zone rather than damaged source data
- The source files, their provenance, export dates and scope; whether they are successive exports of one calendar or independent calendars with uncertain identity relationships
- Whether this is a one-time transfer, recovery of a known revision, a proposed new schedule change, or repair of an invitation. Do not treat these as interchangeable
- The intended destination if known, whether it is empty or already contains these events, and whether the user expects future source changes to appear automatically
- Authoritative evidence for disputed fields: a known-good export, event-owner correction, original schedule or explicit user interpretation. Filenames, download order and the assistant's local zone are not evidence of intended timing

Inspect the supplied packet before asking for missing information. If the destination is unspecified, prepare a standards-oriented file and state that app import behavior remains untested. If a zone or conflicting time is unresolved, hold that event while completing independent groups.

## 1. Inventory with a real parser

Check what parser or safe local consumer is actually installed, record its version, and use its documented parsing and serialization interfaces. Do not build a whole iCalendar parser around line splitting or global replacements. Content folding, parameters, escaped punctuation and nested components make those approaches unreliable.

Record source hashes, encoding, calendar/component counts, calendar-level metadata and parser errors. Assign each source component a stable reference using the file hash and ordinal. Preserve line-ending and normalization changes separately from semantic changes. A tolerant parse is useful evidence, not a complete conformance verdict.

Identify `METHOD`, organizer/attendee data, alarms, attachments, remote references and components other than `VEVENT`. Preserve their evidence without activating anything. Do not fetch a `TZURL`, follow an attachment URL, execute alarm actions or upload a private export as an incidental validation step. Treat invitation or cancellation messages as scheduling material requiring their own intended-action review; the included helper accepts snapshot files without `METHOD`.

Read the relevant [format references](references.md) when applying unfamiliar semantics. Use current official documentation for an actual destination. Product import behavior is not defined merely by the `.ics` extension.

## 2. Resolve event identity before choosing versions

Build a component map within each proven source lineage. For every record, retain source reference, `UID`, recurrence identity, revision metadata, start/end forms, status and dependencies.

The essential format rules are:

- `UID` identifies the event; a detached occurrence also needs `RECURRENCE-ID`. A moved occurrence keeps the original occurrence's identifier, even when its `DTSTART` changes
- `SEQUENCE` is revision metadata. Preserve it when selecting a source revision; do not renumber records to make a preferred copy win
- `DATE` is a calendar date. `DTEND` is exclusive; an all-day event including October 24–26 ends on October 27
- UTC, local time with `TZID`, and floating time have different meanings. Retain the appropriate `VTIMEZONE` definition for referenced local times

These distinctions come from [RFC 5545](https://www.rfc-editor.org/rfc/rfc5545#section-3.6.1). Keep the exact supplied identity values and parameters; title matching is only a clue for review. Two similar-looking events with different UIDs are not automatically duplicates.

Assign each source component one disposition: retained, duplicate representation, superseded revision, held, or known-invalid. Keep the reasons and links to retained representatives.

- Collapse an identical repeated component only when provenance establishes repeated representations of the same object. Compare the complete parsed component, including extension properties and subcomponents, not just its title and start
- Choose a superseding revision only within a comparable lineage and with evidence supporting that choice. A larger sequence number from an unrelated or corrupted source is not enough. Equal revision metadata with different content stays unresolved unless stronger evidence decides it
- Keep a recurring master, its overrides, exclusions, added dates and time-zone dependencies coherent. Do not discard an override because its start no longer matches the master; that may be the intended move
- If an unresolved component could change an included series, hold the affected series. Emitting its master alone can resurrect an excluded or moved occurrence
- A later cancellation must not cause an older active copy to be emitted as a fallback. Absence from an export also does not by itself prove deletion. Explain the unresolved destination action instead of performing one

Never merge independent snapshots solely because their UIDs happen to collide. Do not invent replacement UIDs to evade a conflict or an importer's duplicate handling.

## 3. Make only evidence-backed repairs

For every proposed semantic change, record the before value, intended value, precise source and affected component identity. Prefer selecting a complete known-good revision over reconstructing it from fragments. Do not combine the date from one disputed version with the room from another simply because each looks plausible.

Distinguish recovery of an existing revision from a new schedule decision. Recovering damaged serialization or selecting a known-good snapshot should preserve that revision's identity and metadata. A newly requested reschedule, attendee change or cancellation belongs in the owning calendar's authorized update workflow; do not manufacture scheduling messages or claim an offline edit updates attendees.

For dates and recurrence:

- Keep all-day data as dates. Do not turn it into midnight UTC or calculate its length as a fixed number of hours
- Preserve the distinction between `DTEND` and `DURATION`, including legitimate omitted-end semantics. If the chosen adapter cannot represent a form, hold it rather than inventing a duration
- Resolve a disputed local clock time against the date-specific zone and supplied evidence. A repeated or skipped clock hour needs an explicit interpretation when human intent is unclear; parser normalization does not establish that intent
- Do not convert a local recurring series to one fixed UTC hour. Check occurrences on both sides of a relevant offset change and retain wall-clock behavior when that is what the source represents
- Keep recurrence exclusions and additional dates attached to the right series. Validate the original slot of each moved occurrence as well as its new start
- Handle `RANGE=THISANDFUTURE`, complex recurrence, missing masters or conflicting definitions only with an adapter that actually supports them. Otherwise hold that dependency group and identify the unsupported feature

When the available evidence cannot establish a correction, deliver the unaffected subset and a precise question such as “Which zone does this floating 09:00 belong to?” Do not present a guessed value as an import-ready repair.

## 4. Write and reopen the actual copy

Write a new file, never over the original. Include only coherent retained groups and their required definitions. Preserve relevant properties and extension fields; if a chosen tool drops or rewrites an unsupported field, either use a preserving route or hold the affected group. Do not silently strip alarms or attendees and call the result equivalent.

Save a readable review with:

- Source and output hashes; source-component counts and disposition totals
- Included event identities and human-readable local dates, zones and exclusive ends
- Changes with before/after values and evidence; duplicate and stale source references
- Every held group, the consequence of leaving it out and the smallest missing fact or capability
- Exact verification performed and remaining destination limitations

Mark partial copies prominently. An omitted cancelled record is not a cancellation request to the destination. If nothing is safely included, deliver the review and originals instead of a misleading empty “fixed” calendar.

Reopen the saved bytes using the installed parser. Compare all retained component properties with the intended components and verify that source hashes have not changed. Check:

1. Counts reconcile without hiding holds inside the imported count
2. UIDs, recurrence identifiers, sequence values, timestamps and time-zone parameters survived
3. All-day dates cover the intended calendar days; timed intervals have the intended instants and duration
4. A bounded recurrence projection includes the relevant ordinary, moved, excluded and extra occurrences, especially around the reported date error or clock change
5. Text escapes, folded lines, Unicode and retained extension fields survive serialization

State the projection's scope. Checking a sample from an infinite series does not prove every future occurrence. A recurrence engine's successful expansion also does not prove a calendar app's handling of updates.

## 5. Separate file readiness from destination readiness

If an installed consumer can be exercised in an isolated, unsynchronized local profile with synthetic data, use it when it meaningfully tests the destination format. Inspect persisted readback after import, including series exceptions and all-day spans. Do not open the fixture in a configured calendar account as a casual test; importing can change data or trigger alarms.

If only parsing was tested, say so. For a named destination, check its official import route and establish whether it creates copies, updates existing identities, ignores repeats or accepts only part of the file. Do not promise idempotent re-import without evidence. For example, Google documents that imported events do not remain synchronized with the source and that guests and conference data are not imported; see [Google's import guidance](https://support.google.com/calendar/answer/37118?hl=en).

A requested, authorized live import is a separate next action with a known destination and side effects. Before retrying any uncertain import, inspect what arrived; do not upload the entire file again as a diagnostic. Finish this skill's file result with the actual corrected copy, review and honest verification status.

## Worked file repair

[The example](example.md) reconciles fictional local exports for a software office-hour series and everyday repair/community events. It produces an actual [partial ICS copy](outputs/reconciled.ics), [readable review](outputs/review.md) and [component ledger](outputs/reconciliation.json).

The [offline helper](scripts/reconcile.py) applies an explicit, hash-bound selection plan and uses installed `icalendar` and `python-dateutil` libraries. It accepts a deliberately small profile described in the example; it is not an implementation of all RFC 5545. The [behavioral check](scripts/verify.py) exercises ambiguity and unsupported-input boundaries without any calendar account, invitation or network request. [Verification](verification.md) records what was run.
