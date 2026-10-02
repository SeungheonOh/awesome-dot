# Fictional owner evidence

These notes and both ICS files are invented for the example. They represent exports from one local calendar, not invitations or a live provider feed. The owner wants a reviewed, partial transfer file for a separate empty calendar, with anything unresolved left out and explained. No live import is requested.

## A. Office-hour series

Keep the revised snapshot of `office-hour@example.invalid`, sequence 3. The room is now Café room. It remains a one-hour series starting at 09:00 Europe/London on October 19, 2026, with three weekly generated starts. November 2 is excluded; November 3 at 09:00 is an additional occurrence. Only the October 26 occurrence moves to 10:00–11:00; its original occurrence was October 26 at 09:00. The repeated master in the revised file is an accidental duplicate export of the same component.

## B. Equipment swap weekend

The event occupies October 24, 25 and 26, 2026. The revised snapshot, sequence 2, corrects the earlier export's missing final day. This is an all-day date range, not three fixed 24-hour periods.

## C. Separate event with a reused title

`separate-office-hour@example.invalid` is an independent event on October 20 at 17:00–18:00 UTC. Its title happens to match the series. Keep its UID and its one-off timing.

## D. Unresolved information

- The device repair appointment says 09:00–09:30, but neither the notes nor the file identifies a time zone. The owner wants a fixed instant when transferred; no zone has been chosen
- Two interface design review records claim sequence 4 with the same DTSTAMP but disagree about the time. Neither has been confirmed
- The repair clinic has a later cancelled revision. Do not recover the older active version. The owner has not chosen a destination cancellation or deletion action

These notes authorize only the fictional file preparation described above. They do not establish how a particular calendar app handles an import or a re-import.
