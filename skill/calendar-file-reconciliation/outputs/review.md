# Reviewed calendar file

partial; parser-verified; no live import performed

12 source components → 4 output components; 1 duplicate, 5 held, 4 kept, 2 superseded

The held groups are absent from this partial file. This is not a cancellation or deletion request.

## Included occurrences

- office-hour@example.invalid: 2026-10-19T09:00:00+01:00 to 2026-10-19T10:00:00+01:00 (exclusive end)
- office-hour@example.invalid: 2026-10-26T10:00:00+00:00 to 2026-10-26T11:00:00+00:00 (exclusive end); original recurrence identity 2026-10-26T09:00:00+00:00
- office-hour@example.invalid: 2026-11-03T09:00:00+00:00 to 2026-11-03T10:00:00+00:00 (exclusive end)
- separate-office-hour@example.invalid: 2026-10-20T17:00:00+00:00 to 2026-10-20T18:00:00+00:00 (exclusive end)
- swap-weekend@example.invalid: 2026-10-24 to 2026-10-27 (exclusive end); 3 calendar days

## Held groups

- repair-appointment@example.invalid: The floating 09:00 has no authoritative zone. A fixed-instant transfer requires the intended local zone or confirmation that it should remain floating.
- design-review@example.invalid: Two different times have the same UID, SEQUENCE and DTSTAMP. The notes do not choose between them.
- repair-clinic@example.invalid: A later cancelled component exists. Do not restore the older active copy; decide how the intended destination handles this cancellation before any live change.

The JSON report accounts for every source component and shows selected revision changes.
UIDs, revision metadata, recurrence identities and selected event content are preserved.
No target application, duplicate policy, invitation behavior or live import was tested.
