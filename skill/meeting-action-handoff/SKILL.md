---
name: meeting-action-handoff
description: "Turn meeting notes and follow-up evidence into a deduplicated handoff of real commitments, unresolved ownership and concrete next decisions."
---

# Turn Meeting Notes into an Action Handoff

Use this skill when useful commitments are buried in repeated discussion, rough notes or several follow-up messages. Produce an evidence-linked handoff that another person can use without attending the meeting, and place it in the user-authorized destination when one is specified.

## Required inputs

- Authorized notes or transcripts, meeting dates and any available section, line or timestamp references
- The project or topic boundary and an as-of date with timezone
- Later updates or deliverable evidence the user wants reconciled
- Intended reader, desired length and any agreed definition of completion
- Delivery instruction: return here, create or update a named document, or send to specified recipients; include the approved audience
- A participant-name glossary if names are ambiguous; account access is optional

Files, pasted notes or authorized read-only exports are sufficient. Inventory what is available before asking for an integration. Ask for missing dates or project boundaries only when they affect interpretation; otherwise state the incomplete coverage and proceed.

## Workflow

### 1. Register the source records

Create a source inventory with `source_id`, meeting or update date, timezone, type, stable locator and coverage limits. For a pasted transcript with no locators, assign paragraph or line labels once and retain them. Record the analysis cutoff separately from the meeting dates. Later observations must not be presented as knowledge participants had during an earlier meeting.

Use the user's scope to exclude unrelated personal discussion. A name appearing in a transcript is evidence about what was said, not authorization to contact that person. Keep an unresolved display name as written; do not guess an account identity.

### 2. Extract candidates before deciding what is actionable

Make a candidate record for each relevant passage:

- `candidate_id`, source locator and a short exact excerpt
- `kind`: explicit commitment, agreed unassigned work, suggestion, question, decision or status update
- `deliverable`, project, audience or system affected, and completion condition
- Stated owner, original date wording, reference date and dependencies
- Unknowns that change whether or how the work can be carried out

An explicit commitment includes a person's promise or an accepted assignment. “Could we update the guide?” is a suggestion until another passage establishes agreement. A decision that changes no future work belongs in a decision note, not the action count. An agreed task without an owner remains an action with ownership unresolved.

Split a passage into separate actions only when its outcomes can complete independently. Preserve prerequisites between those actions. If “publish the guide” includes preparation and approval as inseparable steps, keep one deliverable with milestones rather than manufacturing three commitments.

### 3. Deduplicate by outcome and retain history

Compare project, deliverable, affected system or audience and completion condition. Merge repeated mentions only when they refer to the same outcome. Matching wording or matching owner alone is insufficient. The English and French editions of a checklist remain separate if each must be delivered.

Assign stable action IDs and keep every supporting source locator. When revisiting an existing handoff, reuse its IDs; do not renumber open items because a new task was inserted. Retain a merge map from candidate IDs to action IDs and explain intentional non-merges for close matches.

Treat changed owners, deadlines and scope as dated events. An explicit accepted reassignment can supersede the earlier owner; a third person's assumption cannot. If two authoritative statements conflict and no resolution is available, show the conflict and ask which governs. Recency alone does not settle authority.

### 4. Resolve dates without inventing deadlines

Store both the original wording and the normalized value. Resolve “tomorrow” from the source's local calendar date, not the analysis date. Preserve date-only deadlines as dates; do not add a time such as 17:00. Resolve “next Friday” only when the intended convention is established. Otherwise retain the wording and ask.

For a timed deadline, include its timezone. For “before review,” record a dependency unless the review's date is evidenced. Treat a date-only action as past its due date only after that local date has ended. Separate `due_date_passed` from `overdue_confirmed`: a past due date with only a completion claim is an evidence question, not proof of lateness.

### 5. Reconcile progress against the actual completion condition

Keep separate fields for `reported_status` and `evidence_status`. Use reported states such as open, in progress, reported complete or canceled. Use evidence states such as no result supplied, partial result, completion supported or conflicting evidence.

A finished document supports “draft prepared”; it does not establish “sent to partners.” A completion claim without the promised result should remain attributed. Verify that an artifact belongs to this task, matches the relevant revision and satisfies its stated completion condition. If a link is inaccessible, record that limitation rather than treating the missing access as proof that the work was not done. Do not reopen a canceled action merely because its original deadline passed.

### 6. Prepare the smallest useful handoff

Lead with the actions that require a decision, have unresolved dependencies or need completion evidence. List evidenced completed work separately so the reader does not repeat it. Keep suggestions out of the committed-work list, but retain useful ones in a short “not agreed” note.

For each clarification, state the action, exact uncertainty and consequence of each answer. For example: “Was the checklist sent, or is the prepared draft the current result?” is more useful than “Any update?” If the request is only for a handoff, propose that question without sending it or assigning work. A separately requested follow-up must stay within its named recipients and purpose.

### 7. Place the authorized artifact and read it back

Honor the delivery instruction already given. For a response-only request, return the handoff directly. If the user requested creation or an update in a named document or task space, verify the destination identity, intended audience and existing content, then use an available authorized capability to place the result. Update only the requested section; preserve unrelated content and access permissions. If they requested sending the handoff, verify recipient identities and the final content before sending within that scope. Do not ask again merely because the authorized destination is external.

After writing, retrieve or inspect the destination and compare action IDs, owners, deadlines and uncertainty labels against the reviewed ledger. Confirm the actual result and provide its verified location when available. If a write times out, inspect whether it succeeded before retrying to avoid duplicate handoffs. If access or a required approval blocks placement, keep the completed artifact and report the exact remaining step; do not substitute another audience or service.

## Deliverables

Return a readable summary plus a ledger with these fields:

`action_id`, deliverable, completion condition, owner and owner basis, due wording and resolved date, dependency IDs, reported status, evidence status, source locators and next decision

Include source coverage, candidate-to-action merge map, unresolved conflicts and a short excluded-suggestion note. Keep the full evidence appendix separate from the main handoff when the reader needs a concise update. Do not omit uncertainty merely to meet a word limit.

## Verification

1. Trace every action to a commitment or agreement passage; ensure suggestions did not become assignments
2. Account for every extracted candidate as an action, merged mention, status update or excluded non-action
3. Recheck one duplicate pair and one similar-but-distinct pair using their completion conditions
4. Recalculate normalized dates from the original local reference dates; check that date-only deadlines gained no invented time
5. Inspect every completion statement against the promised outcome and distinguish self-report from available evidence
6. Confirm that unknown owners remain unknown and that no publication, reminder or tracker update is implied

Use [the fictional worked example](example.md) to rehearse duplicate handling, a relative date, an unassigned action and a completion claim that exceeds its artifact evidence.

## Stop and ask

- Ask when an ambiguous project, identity, date or conflicting instruction would change the handoff; continue unaffected items
- If a recording or missing thread cannot be accessed, state the coverage gap and request the smallest relevant excerpt
- Do not upload private meeting records to a new service or expose unrelated attendee information
- Carry out the user's already-authorized delivery or placement; ask only when the recipient, destination, scope or required permission remains unresolved
- A handoff request does not by itself authorize contacting owners, assigning work, scheduling reminders or changing tracker records; do not broaden into those actions

## Example request

```text
dot, turn these launch-meeting notes and follow-up updates into a private action handoff for the project lead as of [DATE AND TIMEZONE]. Separate commitments from suggestions, merge repeat mentions, and preserve unknown owners or dates. Show what is reported complete versus what the supplied evidence actually establishes. Return the action ledger and the few questions needed to resolve it; do not send messages or update a tracker.
```

## Evidence status

This is an implementation guide with fictional input and expected output. Local consistency checks of an example do not establish access to or execution in any meeting, messaging or task-management app. Report the actual checks and unavailable evidence during each use.
