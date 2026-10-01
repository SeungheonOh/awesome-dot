---
name: event-run-sheet-handoff
description: "Turn an authorized event brief into a coordinator run sheet with fixed anchors, supplied task durations, predecessor gates, role/resource availability, handoffs, contingencies and unresolved decisions. Create or update the requested artifact and verify it without treating a plan as a booking, notification or live-event guarantee."
---

# Build a coordinator's event run sheet

Translate the actual brief into an executable-looking but honestly qualified schedule: what must happen, when, with whom, what releases the next task, and who decides when something fails. Cover setup, opening, program and close. Keep a task's planned time, readiness and execution evidence separate.

This workflow coordinates an event already described by the user. It does not find meeting availability, make a packing list or summarize general project progress. The [fictional example](example.md) and [standard-library checker](check_example.py) illustrate the handoff, not a live event.

## 1. Establish the brief and authority

Read the authorized event brief, revisions, venue instructions, roster and relevant status reports. Preserve the user's requested artifact format and destination. If updating an existing run sheet, read it completely enough to preserve unaffected content and distinguish an approved change from a suggestion or an older version.

Extract a small source ledger:

- Source reference/link, author or issuing role, version/effective date, issue time if known, and time retrieved or supplied
- Event date, source time zone and explicit UTC offsets where needed; keep multiple source zones visible
- Each fixed anchor and its meaning: access begins, doors open, program starts/ends, load-out ends, venue handback or departure
- Task durations actually supplied, their units and any supported range; identify estimates separately
- Required predecessor tasks, finish-to-start lags, approval gates, allowable parallelism and any explicitly permitted interruption
- Assigned roles, named people only if supplied, resource capacities, availability intervals and known breaks or transfers
- Decision owners, acceptance criteria, unresolved requirements and source-backed contingency permissions

Tag facts as supplied, independently checked, conflicting, stale or unknown. A brief's assertion of a booking is evidence of that assertion; do not describe it as a booking you made or independently confirmed. Resolve conflicting revisions through the authorized decision owner; do not prefer whichever version makes the timeline fit.

Ask only for gaps that materially change the next decision. A missing duration, role assignment, recipient or approval is unknown, not zero, nobody or implied consent. Proposed task additions may expose an omission, but keep their durations and assignments unassigned until supplied or approved. Do not invent safety staffing, legal requirements, venue capacity, permits, crowd controls or emergency procedures. Carry supplied requirements accurately and refer unanswered safety/legal questions to the event's designated qualified owner.

Creating or updating the requested run-sheet artifact does not authorize calling people, inviting attendees, messaging a venue, changing bookings, buying supplies, publishing a schedule, or editing calendars. Obtain the actual action-specific authority before any such step. Record external actions as proposed, authorized, attempted or verified, with a readback when performed; never infer success from the existence of a plan.

## 2. Express the timing model

Use a task ID and one row per meaningful handoff or block of work. Include phase, task, planned start/finish, duration source, predecessors/lags, assigned roles/resources, deliverable or acceptance gate, and source references. Represent a zero-duration milestone only when it really is a milestone; a required unknown-length task remains unscheduled or conditional.

Normalize dated timestamps to instants for comparisons, while retaining the source-local displays and zone. Ask about ambiguous or nonexistent daylight-saving times instead of guessing. A task crossing midnight needs both dates. Preserve exact source precision and do not round a missed anchor into compliance.

State the boundary conventions used by the brief, then apply them consistently. For a model that explicitly permits equality:

```text
finish = start + supplied duration
successor.start >= predecessor.finish + separately supplied lag
availability.start <= task.start AND task.finish <= availability.end
fixed start: task.start == anchor
finish-by: task.finish <= cutoff
half-open occupancy: [start, finish)
overlap: max(a.start, b.start) < min(a.finish, b.finish)
```

Under those conventions, one role may finish at 15:00 and start another task at 15:00. This does not establish that travel, reset or handoff effort takes no time. Include any supplied transition duration as its own task or lag, once. If equality is prohibited, use the actual stated reserve or strict condition; do not choose an arbitrary epsilon. Distinguish an exact end time from a latest finish and a doors-open milestone from the ongoing admissions task.

## 3. Check dependencies and scarce capacity

1. Validate IDs, nonnegative known durations, predecessor references and source links. Reject duplicate IDs, self-dependencies and cycles; report the involved chain. An unknown duration makes affected timing unresolved even if someone supplied a nominal finish time.
2. Check every fixed anchor, deadline, predecessor lag and availability window against the proposed intervals. Keep separate windows separate; do not run work through a role's unavailable break.
3. Check shared named people across all their role labels, not just identical role names. Also check resources with their stated capacity. A location label such as “hall” is not automatically a capacity-one resource. Model exclusive equipment or room reservations only when the evidence supports exclusivity.
4. For capacity one, reject positive overlap; for capacity greater than one, sum simultaneous demand, including every required unit and the full task interval. Distinguish an unassigned role, unavailable person, duplicate use and unconfirmed attendance. One is not evidence of another.
5. Make handoff effort visible. A five-minute briefing needing two people occupies both for the entire five minutes unless the source supplies another arrangement. Do not insert a silent multitasking exception.
6. Check the close-out path through the actual handback/departure anchor, not merely the program end. Include packing, restoration, reconciliation or equipment return only as supported by the brief; list unsupplied requirements for the owner.

A feasible timing model is not an operational readiness decision. A proposed start can be legal while the room, materials, approval or recipient is unavailable.

For small cases, manual interval checks may be sufficient. If generating candidate schedules, name the method, explored choices and limits. Greedy earliest-start propagation, a fixed-departure check or a single ordering is not a universal optimizer. Failure of one candidate only rejects that candidate.

Claim impossibility only with a valid bound or complete search for the stated model. For example, a mandatory non-overlapping dependency chain with 70 minutes of supplied work released at 14:00 cannot meet a 15:00 finish-by anchor, even before resource contention. State which assumptions make that bound valid. Missing durations, uncertain assignments or an exhausted heuristic justify “no complete feasible schedule established,” not “no schedule exists.” Do not optimize away mandatory tasks or move fixed anchors without an authorized decision.

## 4. Define operational handoffs and states

For each consequential handoff, record sender, recipient, expected item/information, planned time, acceptance criterion, evidence channel or reference, and decision owner if rejected. Retain unknown recipients explicitly. A named responsible role is not proof that anyone accepted the assignment.

Use separate fields rather than one ambiguous “done” checkbox:

- **Plan:** proposed / approved for planning / superseded, with version and source
- **Readiness:** ready / blocked / not yet assessed, as of a timestamp, with prerequisite and resource evidence. Require the brief's specified level of predecessor evidence; do not invent a rule that every report counts as verified
- **Execution:** not started / in progress / completion reported / completion verified, with actual times if supplied, reporter, evidence reference and verifier where applicable

A clock reaching a planned finish never completes a task. A checklist tick, verbal report or screenshot establishes only what it actually demonstrates. Mark self-reports as reported; reserve verified completion for evidence sufficient for the task's acceptance criterion. Verification after the finish time is not extra task duration unless it actually consumes a modeled verification step. Reopening a failed acceptance gate must block affected successors even if the nominal end time passed.

When a late status arrives, preserve the original plan and reported actuals, create a forecast if requested, recompute the affected downstream intervals and resource conflicts, and show changes. Do not silently overwrite fixed anchors, mark a missed start as “ready on time,” or claim an entire event is ready because some tasks passed.

## 5. Put contingencies beside the affected gate

For each material source-supported risk, write:

```text
Trigger/evidence -> affected task or anchor -> immediate permitted step
-> decision owner -> latest useful decision time -> unresolved choice
```

Separate a pre-authorized response from an option awaiting approval. A fallback needs its own duration, roles/resources and effects on anchors; unknown fallback effort remains conditional. Show what cannot be salvaged under the stated constraints rather than promising recovery. If a predecessor fails, identify the blocked downstream tasks and next decision. Do not automatically cancel, change venue, extend hire, buy replacements or notify people.

## 6. Create, update and read back the artifact

Deliver the requested document, sheet or other artifact through an authorized destination. Include:

1. Event/date/time zone, revision/as-of time, scope and model verdict, qualified by unresolved requirements
2. Source-backed fixed-anchor list and timing/equality conventions
3. Run-sheet rows covering setup, opening, program and close, with roles/resources and predecessor gates
4. Handoff/acceptance list, readiness/execution evidence, contingencies and decision owners
5. Unresolved requirements with their impact and supplied owner, or “owner unassigned” when missing
6. What actually changed or was performed, plus material model limitations

After a create/update, reopen or reread the saved artifact. Check anchor values, time zones, formulas or totals, every task ID, assignments, duration unknowns, evidence/status fields and links. Recompute affected timings and shared-role conflicts from the saved values, not just the draft. Confirm the destination and permissions before sharing; preserve the existing artifact identity when updating it. If saving or reading back fails, retain the draft and report the unverified step instead of claiming delivery.

Finish with the most important constraint and next decision. State that this is a plan under the recorded inputs, not a live-event guarantee or evidence of bookings, staffing attendance or notifications.

## Bounded example check

From the repository root, run:

```bash
python3 skill/event-run-sheet-handoff/check_example.py
```

The checker validates one supplied schedule and deliberate counterexamples using only the standard library. It does not generate schedules, optimize task order, validate safety/legal compliance, poll a live event or prove feasibility beyond its explicit model.
