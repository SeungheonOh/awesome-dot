---
name: project-update-brief
description: "Draft a concise project update from dated evidence, separating real outcomes, unresolved blockers and decisions from activity or unsupported progress claims."
---

# Write an Evidence-Backed Project Update

Use this skill when several workstreams must become one useful update for a project lead, collaborator or stakeholder. The output should tell the reader what changed, what matters next and what needs a decision without making them read every source.

## Required inputs

- Project boundary, reporting window, as-of time and timezone
- Authorized workstream updates, deliverable records or read-only exports, with dates and source locators
- Intended audience, word limit and delivery instruction: return here, create or update a named document, or post to an exact destination
- Previous brief if the user wants changes since the last report
- Milestones, completion criteria and any agreed freshness or status rules

A bundle of files or pasted updates is enough. Use a connected source only if it is available and authorized. Missing access should lead to an explicit coverage limit, not an invented live status check. Do not wait for every optional input before drafting the supported portions.

## Workflow

### 1. Define what the brief can know

Keep each retained claim traceable to the relevant source and its workstream, date, evidence type and audience restrictions. Preserve event time separately from when an update was written: a message posted this week may describe work completed last week. Use a compact source register when many records, versions or restricted audiences make one useful; a short update from a few clear sources does not need a separate register.

Apply the reporting window to the event date and the as-of cutoff to the information available for the brief. If late-arriving evidence changes an earlier event, label it as a correction or carry-forward rather than claiming it happened in the current period. An update after the cutoff may belong in a later revision, but must not silently change this one.

List expected workstreams and their latest available updates. Use the supplied freshness rule. If none exists, show last-known dates without imposing an arbitrary stale threshold. A missing workstream is unknown, not unchanged or healthy.

### 2. Extract atomic claims and define their proof

Identify the observable claim, outcome stage, event date, supporting source and any contradiction. Break a compound claim into parts when their proof differs. Use stable claim IDs and a structured record when repeated reporting or complex evidence needs them, rather than requiring a claim ledger for every short update.

Match completion language to the outcome actually supported:

- “Draft prepared” requires the relevant draft or an attributed report of it; it does not establish approval
- “Approved” needs the approval decision for that version and scope
- “Implemented” or “merged” needs the relevant change evidence; it does not establish successful validation or release
- “Tested” must identify the test scope, revision and actual result; a partial or interrupted run is not a full pass
- “Released” needs release evidence for the stated audience or environment
- “Improved the outcome” needs a defined measure, comparison period and observation; release alone does not demonstrate benefit

Use the milestones that fit the project, rather than forcing nontechnical work into a software sequence. A statement from a workstream owner can support “the owner reports completion,” while a directly inspectable result may support a stronger statement. Keep that distinction in the supporting evidence and in the brief wherever it changes what the reader can conclude.

### 3. Reconcile history, blockers and contradictions

Compare claims with the prior brief by deliverable or milestone, not by sentence similarity. Label each as newly completed, materially advanced, unchanged with fresh evidence, last-known only, regressed, canceled or unresolved. If the earlier brief is absent, write a current-state brief without invented before/after comparisons.

For every previously open blocker, search the supplied later evidence for resolution, replacement or continued impact. Removal of the original obstacle does not prove the dependent deliverable complete. Preserve a last-known blocker with its date when no newer information exists; do not announce it as definitely active. If a new report conflicts with a stronger artifact or an owner decision, show both and ask for reconciliation. Do not let the newest timestamp automatically win.

Group repeated updates about the same result and avoid counting preparation, approval and delivery as three completed deliverables unless the user's plan treats them as separate milestones. Retain significant reversals and canceled work even when they make the narrative less tidy.

### 4. Calculate only meaningful measures

For every number, record numerator, denominator, unit, scope, time period and source. Recalculate percentages and differences. Distinguish a percentage-point change from a relative percentage change. Do not combine counts with different definitions or infer an overall completion percentage from a subset of tasks or tests.

If a denominator changed, report the change before comparing rates. If counts conflict, omit the derived percentage until resolved or show the competing figures clearly. Small samples should remain visible. A test pass rate describes that test set; it is not a probability of release success or a percent-complete measure for the project.

### 5. Form decision requests without making commitments

For each evidenced decision, record the choice, available options, decision owner if stated, consequence of waiting, deadline and its source. Separate a supplied deadline from a suggested response date. If no deadline is evidenced, omit it or ask; do not create urgency.

Distinguish a blocker, which currently prevents a next step, from a risk that may affect a later outcome. If a recommended decision would commit scope, money, delivery dates or another person's effort, present it as a proposal for the user to review. Never write “we will” merely because an option seems sensible.

### 6. Draft in order of reader value

Lead with a plain-language synthesis of the strongest supported outcome and the main constraint. Then cover meaningful completed results, in-progress work with remaining conditions, material blockers or risks, and the decisions needed. Keep activity such as meetings or investigation only when it explains a result or uncertainty.

Use status colors only when the supplied criteria establish them. Do not compress conflicting or missing evidence into “on track.” Use direct source links or compact references when they help the reader. Keep longer evidence records separate when requested or materially useful; do not automatically add an appendix. Honor the requested length and format, including labels when they count toward the limit, while retaining consequential caveats in the brief.

### 7. Deliver within the requested scope

If the user requested only a draft, return it here. If the request authorizes creating or updating a document, or posting the update to a named destination, perform that action with an available authorized capability after checking the final text and destination. Verify the audience can receive the source material; linking a private appendix does not make it accessible. Do not add recipients, tags, permission changes or a status-field update merely because you are posting a brief.

For an existing document, preserve unrelated sections and replace only the requested update. Read back the result and confirm the main text, as-of date, source references and material caveats survived formatting. For a posted message, verify the returned destination and content when possible. If the result is uncertain, inspect before retrying to avoid duplicates. When access or a required approval blocks delivery, return the completed artifact and the specific blocker. Do not ask for a second approval solely because an already-authorized action uses an external app.

## Deliverables

Return the audience-ready update in the requested format and length. Include the reporting period or as-of context where needed to interpret it; a word-count label, separate title block or review package is not automatically part of the deliverable.

Keep sources recoverable through useful links, locators or working records. Include an evidence appendix when the user requests one or the complexity makes it useful for review. In that case, show the claims, workstreams, outcome stages, source/event dates, support strength, contradictions and justified wording needed to assess the brief. Stable claim IDs are helpful for ongoing or complicated reports, not mandatory decoration.

Surface missing facts or owner decisions that materially affect the update, in the brief or a short separate note as appropriate. Do not add a question list when none is needed. An appendix cannot repair unsupported headline wording; any audience-specific rewrite must remain tied to the same evidence.

## Verification

- Audit every use of complete, approved, tested, shipped, resolved and improved against its exact evidence and scope
- Check every retained or resolved blocker against the latest eligible source and the prior brief
- Recompute metrics from their numerator and denominator; never promote a workstream measure into an overall project score
- Verify the reporting window, cutoff, last-known dates and source locators
- Confirm decisions contain no invented deadline, owner, promise or consequence
- Check the requested length, then reread the update without supporting records to ensure it remains accurate on its own

Use [the fictional worked example](example.md) to test a resolved old blocker, a partial test result, stale coverage and an update that arrives after the cutoff.

## Stop and ask

- If the intended audience is unclear or sources contain information outside that audience's permissions, prepare a private draft and ask before sharing
- Ask when contradictory milestone evidence changes the headline, rather than selecting the more optimistic account
- If the latest state is unavailable, use dated last-known wording and finish the rest of the brief
- Perform already-authorized artifact placement or posting within its stated audience; ask only for an unresolved destination, material scope change or required approval
- Do not add tags, change a project status, contact owners or commit to an option unless the user also authorized that action

## Example request

```text
dot, prepare a private project update for [AUDIENCE] covering [PERIOD], as of [TIME AND TIMEZONE], using these workstream updates and the previous brief. Keep the main text below [WORD LIMIT]. Show outcomes, remaining conditions and decisions, with a source appendix. Flag stale or conflicting evidence and avoid turning code, tests or drafts into claims of delivery. Do not post the update or contact anyone.
```

## Evidence status

This is an implementation guide. Its example uses fictional records and expected wording. Recalculating those records does not prove real project completion, live-system access or publication. Report which evidence was actually inspected in each use.
