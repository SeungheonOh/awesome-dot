---
name: code-review-handoff
description: "Explain one immutable code change through its intent, affected behavior, verification evidence and focused reviewer questions."
---

# Prepare a Reviewer-Ready Change Handoff

Explain one immutable code change through its intent, affected behavior, verification evidence and focused reviewer questions.

## When to use

An engineer has finished a fictional booking-calendar change and wants a colleague to review it efficiently. The diff mixes the behavior change with generated files, and the local test results came from an earlier revision. A useful handoff shows what to inspect, why it changed and which claims have evidence, while leaving approval to the reviewer.

## Required inputs

- An authorized immutable diff with base and head identifiers, or a clearly versioned patch
- The requirement, linked acceptance criteria or sanitized issue description
- Relevant surrounding source files and architectural constraints
- Test results with the exact revision, command, environment and date when known
- Intended reviewer role and a short list of known concerns or deliberate tradeoffs

## Workflow

### Freeze the review subject

Create a manifest with base identifier, head identifier or patch checksum, supplied context paths, requirement references and evidence timestamps. List any files missing from the patch or surrounding context. If the change cannot be identified consistently, request a stable export before making review-wide claims. Preserve the author's stated rationale as attributed input; do not replace missing intent with an inferred story.

### Build the handoff

1. Inventory changed paths and classify each as behavior, interface, persistence, test, documentation, generated output or mechanical movement. Record renames separately from semantic edits. Inspect generated artifacts for contract or runtime effects before putting them in a lower-attention group.
2. Extract the requirement into numbered acceptance criteria. For each, identify the changed entry point, affected call path or data transformation and the relevant test assertions. Describe before/after behavior using source references on both sides. If surrounding code is unavailable, state precisely which part of the path cannot be evaluated.
3. Establish a reading order following the behavior: public contract or entry point, decision logic, state or dependency boundary, then tests. Group supporting edits beneath that path instead of listing every filename with equal weight. Call out unrelated edits as review-scope questions without automatically declaring them incorrect.
4. Trace normal, invalid or empty, and repeated-operation cases through the changed logic. Turn unresolved concerns into questions with a location, a concrete failure condition and the evidence needed to answer. Reserve defect language for a demonstrated contradiction with the supplied requirement or implementation behavior.
5. Reconcile every test result to the immutable head. Record command, environment, revision, timestamp, result and completeness. A result at another revision is stale or conditional evidence, even when the changed files appear unrelated; explain relevance without relabeling it current. A canceled or partial run is not a pass.

### Deliver and quality-check

Return a compact review description with intent, behavioral changes, suggested reading order, three highest-value reviewer questions and known limits. Put the complete criterion map, path classification and verification ledger in an appendix. Every important claim should have a source location or be visibly marked as an assumption. Check that all changed paths appear in a group and that every acceptance criterion has implementation evidence, a gap or an out-of-scope explanation. When authorized tests can run safely, use only documented relevant commands and record their actual result; otherwise keep the ledger unrun. End with what the reviewer still must decide, never an approval recommendation presented as completed review. Do not request reviewers, post the draft, edit code or merge without separate authorization.

## Deliverables

- A review description with intent, behavior changes and a recommended reading order
- An acceptance-criterion map to implementation and test evidence
- A revision-specific verification ledger
- A focused question list with source references and unresolved tradeoffs

## Verification

- The handoff names both immutable endpoints or the exact supplied patch identity
- Each important behavior change cites a relevant location rather than merely listing filenames
- Test evidence from an earlier revision is visibly stale or conditionally relevant
- An empty or invalid input case has a documented outcome or a specific reviewer question
- Generated files are identified without automatically dismissing their runtime impact
- Concerns are not described as confirmed defects unless the supplied evidence establishes the failure
- The draft does not imply that a human review, approval or merge has occurred

## Stop and ask

- Keep the review within authorized files and exclude credentials or customer examples
- Actual test execution requires a permitted environment, an available toolchain and understood side effects
- Ask for a stable diff if the supplied files cannot establish which change is being reviewed
- Posting, requesting reviewers, changing code, pushing or merging requires separate authorization

## Example request

```text
dot, prepare a code-review handoff for [IMMUTABLE BASE AND HEAD OR PATCH] that implements [REQUIREMENT]. Use [AUTHORIZED DIFF, CONTEXT FILES AND TEST EVIDENCE]. The reader is [REVIEWER ROLE], and the handoff should help them evaluate correctness and maintainability without relying on this chat. Do not approve, merge or edit the change.

Summarize the intended behavior before and after the change, then group files by their contribution to that behavior. Suggest a reading order that starts with the contract or entry point and ends with supporting tests. Explain generated or mechanical changes separately, while retaining any that affect runtime behavior. Map each acceptance criterion to implementation locations and test evidence.

Create a short verification ledger with checked revision, command, observed result and unresolved limits. If a test result predates the supplied head, do not present it as verification of the final change. Identify precise reviewer questions about assumptions, edge cases and compatibility, and distinguish a demonstrated defect from a concern needing investigation. Avoid inventing author intent or implementation facts absent from the inputs.

Check a normal path, an empty or invalid input path and any repeated operation affected by the change. If execution is not authorized or the local toolchain is unavailable, review statically and label tests unrun. Keep source private and ask before external actions, additional access, installations, code edits or posting to a review system. Return a concise handoff draft plus a source-linked evidence appendix.
```

## Focused follow-ups

### 1. Prioritize review attention

```text
Reduce the reviewer questions to the three that could most change the accept-or-revise decision. For each, cite the exact changed location and the evidence needed to resolve it.
```

### 2. Reconcile updated test evidence

```text
Apply [NEW TEST RESULTS] to the verification ledger. Check their revision and environment before changing any status, and retain failures or incomplete runs that remain relevant.
```

### 3. Respond to review feedback

```text
Use [SANITIZED REVIEW COMMENTS] to draft a response plan grouped into clarification, code change and deferred decision. Identify which requests are already satisfied by evidence and which still need work; do not post replies.
```

## Evidence status

This is an implementation guide. End-to-end execution has not been established; report actual checks and unrun steps for each use.
