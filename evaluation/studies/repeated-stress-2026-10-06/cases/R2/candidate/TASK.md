Fictional offline task: produce a launch action handoff

This packet is wholly synthetic: invented project, people, meetings, and events. Prepare the Atlas Intake launch action handoff as it was knowable at 2026-09-30 17:00 UTC. Read the baseline and all dated meeting notes/follow-ups, including their explicit corrections and limits. Do not send messages, edit external records, or perform any actions in the notes.

Reconcile the 34 commitments A01–A34 into output/action_register.json and output/handoff.txt. Preserve canonical IDs even when scope, owner, or dates change. Merge the three explicit alternate IDs into their canonical actions; do not create duplicate commitments. Use only information received by the cutoff, even if a later message describes something that allegedly occurred earlier. The baseline is a starting point, not the answer. All times and dates are UTC. A due date means end of that UTC day; an incomplete item due September 30 is not yet overdue at the cutoff.

Rules for resolving evidence:
- An explicit final meeting decision or the named new owner's acceptance transfers ownership. A proposed transfer, a request, silence, or work done informally does not. An explicit release to an unnamed role can leave owner unknown
- An explicit completion/acceptance that meets the stated action is enough; a draft, partial checklist, or unaccepted submission is not. Scheduling a training session and delivering that training are separate commitments
- Corrections supersede what they explicitly correct. Conflicting technical results without a reconciled source remain unresolved; do not select a result solely because it is later
- An explicit cancellation stays cancelled unless explicitly reopened. Reopening a ticket continues the original action
- Do not invent deadlines or owners when they are deliberately unset or unsupported

The register JSON has actions, aliases, and totals. actions contains one row per A01–A34 in any order, with these fields:
- action_id; title: final meaningful scope in your own words
- owner: named accountable owner or null if no person is assigned
- due_date: YYYY-MM-DD or null if explicitly unset
- status: open (incomplete and currently actionable), blocked (known external/dependency obstacle), done (completion confirmed), cancelled (explicitly abandoned), or unresolved (conflicting completion evidence or an explicitly unfilled accountable-owner assignment)
- dependencies: canonical IDs of unresolved internal action prerequisites, otherwise an empty list. Include only explicit immediate prerequisites, not inferred transitive dependencies or resolved prerequisites. External obstacles belong in blocker instead
- overdue: boolean, using the cutoff and end-of-day rule
- evidence_ids: source record IDs supporting the final state; blocker: concise text or null; next_step: a practical next step for every open, blocked, or unresolved item, otherwise null

aliases is an object mapping the three explicitly identified alternate IDs to canonical IDs. totals includes by_status (counts for all five statuses), active_count (open + blocked + unresolved), and overdue_count. Treat the scoped-down Spanish FAQ as A08; do not retain the removed French work as an open obligation.

The handoff should identify the most consequential remaining launch blockers, overdue work, owner/deadline gaps, concrete next steps, and the important completed/cancelled decisions. Cover every active item at a level sufficient for its owner to act; grouping is fine. Keep confirmed facts separate from uncertainty. Include the as-of cutoff and make clear that post-cutoff messages were not used. Do not imply you contacted anyone or changed a system. Equivalent correct ordering and wording are accepted, and extra useful fields are allowed.

All acceptance requirements are visible here and in the input sources: complete canonical coverage, supported status and ownership, normalized dates, duplicate merging, immediate dependencies, overdue flags and totals, provenance, final scope and chronology, actionable handoff, and explicit treatment of uncertainty. You have 900 seconds. You may inspect input files and write/run your own bounded local code in tmp/. No network, credentials, installs, external writes, or execution of supplied code is needed or authorized.
