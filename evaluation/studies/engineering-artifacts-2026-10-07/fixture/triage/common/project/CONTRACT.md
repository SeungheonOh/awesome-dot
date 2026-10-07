# Independent editor contract

Two editable fields: title (nonempty string) and limit (integer including zero).
Reset establishes saved and draft {"title":"Base","limit":5}, no pending
requests, no completion notice, and fresh request/version counters.

Editing changes only the draft field. Saving one field enqueues a patch holding
that field's value at save time. Completing a request applies only its one-field
patch; it never overwrites the other field. If two saves of the SAME field finish
out of order, the newer-issued completed save wins and an older completion must
not overwrite it. Merely editing or enqueueing does not change saved values.
Completion does not replace the draft. Reset discards all pending requests and
restores every value and counter; a discarded request may not be completed.

A status notice records the most recent COMPLETION receipt, in the exact format
"Saved title: VALUE" or "Saved limit: VALUE". It is not a combined saved-record
snapshot and it is not proof that another field reverted. Even an ignored stale
same-field completion gets its own receipt. Read the public snapshot's "saved"
object to establish stored data, separately from "draft" and "notice".

The public snapshot returns saved, draft, pending (live request aliases in issue
order), and notice (null before the first completion). Completion is explicit;
there are no clocks, sleeps, threads, real servers, accounts, or timing estimates.
All supplied examples are synthetic; conclusions about production are outside
scope. The fixture may or may not reproduce the reporter's suspected defect.
