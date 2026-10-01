---
id: evidence-first-async-status
title: "Evidence-First Async Status Brief"
summary: "Produce a concise asynchronous project update that makes progress, uncertainty, decisions needed, and next evidence easy to inspect."
category: team-operations
level: beginner
timebox_minutes: 30
capabilities: ["files"]
tags: ["status", "async", "communication"]
status: recipe-not-run
---

# Evidence-First Async Status Brief

Produce a concise asynchronous project update that makes progress, uncertainty, decisions needed, and next evidence easy to inspect.

## Scenario

A fictional engineering lead has updates from several workstreams but needs a readable weekly brief. Some entries describe effort rather than outcomes, and one old blocker may already be resolved. A bounded synthesis can make the next decision clear without exaggerating progress.

## Inputs to prepare

- Authorized workstream updates and their timestamps
- The reporting window, as-of date, audience, and word limit
- The previous brief if comparison is needed
- The documented milestones and any decisions requiring review

## Copy this prompt into dot

```text
dot, draft an asynchronous status brief for [PROJECT] for [AUDIENCE], covering [REPORTING WINDOW] as of [DATE]. Use [AUTHORIZED UPDATES] and, if supplied, [PREVIOUS BRIEF]. Keep the main brief under [WORD LIMIT] words. First flag missing or stale workstream updates that could materially change the summary.

Lead with the overall outcome supported by the evidence. Then show completed deliverables, work still in progress, blockers, and decisions needed. Distinguish a merged change, a successful test, a release, and observed user impact; never treat one as proof of the others. For each decision request, state the choice, consequence of waiting, and deadline only if evidenced. Put supporting source locators in a short appendix.

Use plain language and remove activity lists that do not explain a result. Check that an old unresolved blocker is not silently treated as current, that partially completed work is not called done, and that conflicting updates remain visible. Do not manufacture a green, yellow, or red status without agreed criteria.

Return the draft, its evidence appendix, and unresolved questions. Keep it private. Do not post the update, tag colleagues, change project status, or make commitments on anyone’s behalf.
```

## Iterate with a purpose

### 1. Tune for an executive reader

```text
Rewrite the same evidence for a reader with two minutes and limited technical context. Preserve uncertainty, consequences, and decision requests; do not add claims of business impact.
```

### 2. Test each done claim

```text
Audit every use of complete, shipped, fixed, or resolved. Show the supporting evidence and replace the wording where it overstates what was actually observed.
```

### 3. Prepare the next evidence request

```text
List the smallest missing facts that would materially improve next week’s brief. Group them by workstream and explain why each matters without contacting anyone.
```

## Expected deliverables

- A word-limited private status brief
- An evidence appendix with source timestamps and locators
- A clear set of decision requests supported by the supplied record
- A list of stale, contradictory, or missing updates

## Acceptance checks

- The main brief meets the requested word limit
- Every completion claim uses the right milestone: code, test, release, or observed impact
- A stale blocker is labeled with its last known date
- Partially finished work remains visibly in progress
- A decision deadline is sourced or omitted rather than invented
- The draft contains no unsupported promise or status color

## Access, privacy and stop conditions

- Use only updates permitted for the intended audience; sanitize customer and personnel details
- Drafting does not authorize posting, tagging, or distributing the brief
- If the latest state is unavailable, preserve the as-of limit instead of implying a live status check

## Two possible extensions

- Create audience-specific versions that share one evidence appendix
- Build a reusable update intake form based on the gaps found in this review
