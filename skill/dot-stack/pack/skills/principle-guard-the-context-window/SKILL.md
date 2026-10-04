---
name: principle-guard-the-context-window
description: "Keep long investigations usable by bounding retrieval, preserving decision-relevant evidence, and producing source-linked handoffs instead of accumulating raw output."
---

# Guard the context window

Use this when a task involves large files, verbose logs, many artifacts, or repeated investigation. Context is a limited working area; a host may compact or restore it, but those operations can lose detail. Preserve recoverable evidence rather than assuming either unlimited recall or unavoidable failure.

## Keep the next decision in view

1. State the current question and retrieve only the relevant slice: targeted search, bounded command output, a specific page, or a representative sample. Check whether a result was truncated before treating it as complete.
2. Keep raw artifacts in an authorized working location when needed. Summarize the decision-relevant facts with source paths, line ranges or identifiers, artifact revision, and unresolved questions. A summary without a way back to evidence becomes another unsupported claim.
3. Preserve constraints that must survive compression: user goal, scope, authority boundaries, accepted decisions, current candidate, failed attempts, and the next discriminating check. Do not copy credentials or irrelevant private content into handoffs.
4. Read common short guidance inline; keep substantial optional details in discoverable references. Avoid reloading an entire reference to answer one question, but return to the original when a detail matters.
5. Size phases so their inputs and evidence can be reconciled before the next phase. A phase boundary should correspond to a result, not an arbitrary token count.

Available independent workers can inspect isolated large artifacts and return source-linked findings. Give them the required context and verify important conclusions against actual evidence. When delegation is unavailable, use sequential bounded passes and a compact working summary. Do not invent workers, persistent memory, or resumed execution.

## Example and counterexample

Applies: a failing build emits thousands of lines. Save the log, extract the first causally relevant error plus context, inspect that file, and retain the command and exit status.

Does not apply: the task is to verify every clause of a short agreement or every row of a finite mapping. Sampling or dropping “boring” sections would sacrifice coverage. Read the complete material in chunks and track coverage.

## Completion

A handoff should let another authorized reader identify what is known, what remains uncertain, and exactly where to resume. Stop compressing when it would erase a material exception or acceptance criterion. Saved notes are not proof that future execution is scheduled.
