# A stale export, a moved occurrence and an off-by-one day

## Request and supplied evidence

> My local calendar exports disagree. The office-hour series seems duplicated, one moved session appears at the old time, and the equipment swap weekend is missing its final day. Prepare a corrected file for review before I transfer it to a separate empty calendar. Keep uncertain events out and tell me what needs deciding. Do not import anything.

The complete packet is fictional:

- [Earlier export](fixtures/earlier.ics): six event components
- [Revised export](fixtures/revised.ics): six event components, including an accidentally repeated master
- [Owner notes](fixtures/owner-notes.md): the intended dates, one common export lineage and unresolved facts
- [Selection plan](fixtures/selection.json): source hashes, evidence hash and explicit retained or held groups

The notes establish which revisions to recover. The program checks the plan; it does not infer truth from whichever file was downloaded last. In a real task, the agent must prepare the plan from authorized evidence rather than treating this example's choices as universal rules.

## Reconciled result

The [candidate ICS](outputs/reconciled.ics) contains four `VEVENT` components representing three UIDs. One UID is a recurring master plus one moved-occurrence override. The other two are an all-day event and an independent one-off event. A component count is therefore not an occurrence count.

| Source disposition | Components | Reason |
| --- | ---: | --- |
| Retained | 4 | The reviewed master, moved occurrence, corrected all-day revision and independent event |
| Duplicate representation | 1 | The revised file repeats its selected master exactly |
| Superseded revision | 2 | The older master has a stale room; the older all-day revision omits the final day |
| Held | 5 | Three groups have unresolved timing or cancellation handling |
| Total | 12 | Every source component has one disposition |

The selected series keeps local London clock times across the October offset change:

| Original recurrence slot | Actual local occurrence | UTC occurrence | What happened |
| --- | --- | --- | --- |
| October 19, 09:00 | October 19, 09:00–10:00, UTC+01:00 | 08:00–09:00 | Ordinary weekly occurrence |
| October 26, 09:00 | October 26, 10:00–11:00, UTC+00:00 | 10:00–11:00 | Moved occurrence; its recurrence identifier remains 09:00 |
| November 2, 09:00 | None | None | Excluded by `EXDATE` |
| November 3, 09:00 | November 3, 09:00–10:00, UTC+00:00 | 09:00–10:00 | Extra occurrence from `RDATE` |

The equipment swap weekend retains `VALUE=DATE` from October 24 through the exclusive end October 27. It covers October 24, 25 and 26. The example does not turn those dates into midnight UTC or assume that the clock-change weekend is exactly 72 elapsed hours.

The independent October 20 event has the same title as the series but a different UID. It remains a separate event at 17:00–18:00 UTC.

## Holds that make the copy partial

- `repair-appointment@example.invalid`: one floating 09:00 record. The requested fixed-instant transfer needs an intended zone or a different explicit transfer decision
- `design-review@example.invalid`: two records with identical UID, sequence and timestamp but different times. Choosing one requires stronger evidence
- `repair-clinic@example.invalid`: an older active record and a later cancelled record. Neither is included. The file is not an instruction to delete anything from another calendar, and the older event must not be restored accidentally

The [review](outputs/review.md) explains these omissions. The [JSON ledger](outputs/reconciliation.json) records all source references, selected revisions, before/after fields, hashes and the finite occurrence projection. This partial copy is not a full calendar-service snapshot and must not be used as a deletion manifest.

## Reproduce the offline check

Use a Python interpreter that already has `icalendar` and `python-dateutil` available. The recorded run used Python 3.12.14, icalendar 6.3.2 and python-dateutil 2.9.0.post0. Those packages are dependencies, not bundled code. If they are unavailable, report the missing dependency or use an approved existing parser; do not claim that an unrun command passed.

From this skill's folder, choose a new output directory:

```sh
python3 scripts/reconcile.py --fixtures fixtures --output example-run
python3 scripts/verify.py
```

The helper never overwrites an existing output directory. If every group is held, it stops before creating any candidate or output directory and directs the reader to the original files and hold reasons. It makes no network calls and does not open a calendar application. The checks create temporary copies of fictional inputs, prohibit socket creation during reconciliation, and verify the saved bytes. They do not send invitations, connect an account or import to a provider.

## The helper's explicit contract

`offline-event-snapshot-v1` is a small worked adapter, not an RFC validator or a general repair library:

- One snapshot calendar per source, with `VERSION`, `PRODID` and optional `CALSCALE`; no `METHOD` or other calendar-level properties
- `VEVENT` records with explicit UID, nonnegative sequence, UTC timestamp, start and end; no nested alarms, attendee/organizer fields, attachments or remote properties
- Standalone UTC events and all-day dates, plus local timed events whose embedded zone is present and whose selected instants agree with the parser's interpretation
- Embedded local-zone coverage limited to calendar year 2026 in this fixture; conflicting serialized definitions are blocked, even if a difference might later prove cosmetic
- For recurrence, a one-hour weekly timed master with a count from 1 to 100, explicit added/excluded dates and ordinary detached overrides. No `UNTIL`, other rule parts, recurring all-day dates or `RANGE` changes
- Recurrence values must use the master's date/time form. Skipped/repeated local times, projected occurrences outside the supplied zone's worked coverage, and occurrences spanning an offset transition are blocked
- Only the passive descriptive fields and `X-EXAMPLE-COLOR` used here are accepted. Other properties need a reviewed adapter extension or a hold; they are not silently discarded
- Explicit selection of whole source components. Every source recurrence identity must have a selected counterpart or the entire UID must be held. Conflicting equal/newer revisions cannot be silently superseded

The script's conservative limits are engineering choices for a reproducible example. They are not assertions that other valid iCalendar data is invalid. See [verification.md](verification.md) for the tested boundaries and what remains unverified.
