---
name: show-me-your-work
description: "Keep a local append-only decision and evidence log for multi-phase work, audit claims against receipts, and identify unresolved verification gaps."
---


# Show me your work

Keep a reviewable record of meaningful decisions and observed outcomes. Log concise rationale and evidence, not private deliberation, every tool click, or sensitive data. Use one canonical log per run or an explicitly coordinated shared effort.

## Format and storage

The [TSV template](references/decision-log-template.tsv) has exactly six columns: `ts`, `phase`, `decision`, `why`, `evidence`, `result`. Cells are single-line. `ts` is UTC ISO 8601. Evidence is a resolvable artifact pointer, source revision, or receipt ID, not an unsupported paragraph.

Keep the log in the chosen project run directory, for example `.dot-stack/state/<run-id>/decisions.tsv`, or another explicit local artifact directory. Do not write into a read-only plugin cache or auto-commit the log. Sharing and committing require the relevant request.

Use a single writer. Workers return evidence to the coordinator or write separate logs that the coordinator links. Do not assume append operations from different processes are coordinated.

## Append a row

The full pack includes the central [dispatcher](../../tools/dot-stack.mjs). From the verified package root its command is:

```sh
node tools/dot-stack.mjs log FILE PHASE DECISION WHY EVIDENCE RESULT
```

These are six positional arguments; quote values containing spaces. The helper supplies a UTC timestamp, creates a header for a new log, keeps rows append-only, removes cell delimiters, and neutralizes spreadsheet-formula prefixes. Check its exit result; a failed append is not a recorded decision.

A copied standalone skill may not include the helper. Use an observed package root, or a user-supplied `DOT_STACK_ROOT` whose manifest names `dot-stack` and contains `tools/dot-stack.mjs`. Do not assume a relative link survives copying, search private host directories, or download a helper automatically. If unavailable, use an authorized local writer with the same six-column, single-line, formula-safe contract; otherwise return unrecorded entries as a draft. Never claim they were saved.

For example, from a verified full-pack root:

```sh
node tools/dot-stack.mjs log /tmp/demo-decisions.tsv verification \
  'Rejected the first candidate' 'Cancellation recreated the deleted item' \
  'artifacts/cancel-test.txt' 'Failed; candidate not kept'
```

This demonstrates the command shape. Use evidence that actually exists in the current run; do not copy the example as a factual entry.

## Record boundaries and changes honestly

Begin with a `start` row that binds the run ID, repository or input identity, candidate revision when applicable, and scope through its fields and evidence. A resumed run reads the log tail before appending. If another run has written since, append a fresh `start` row naming the new ownership boundary and prior range being resumed; do not silently take ownership of someone else's claims.

Log a chosen approach, completed unit, failed experiment, pivot, revert, blocker, or corrected verification gate. Distinguish attempted from completed and completed from verified. “Tests green” needs the specific command and artifact identity. “Unverified: browser unavailable” is useful evidence status.

The log is append-only. Supersede a wrong or unsupported row with a new row referencing its timestamp or stable row identity. Do not delete the old claim to make the run look cleaner. Keep secrets, tokens, raw personal records, and unnecessary private conversation text out of every field.

## Audit before handing back

Check the current run's rows against actual tool receipts, saved artifacts, and authorized visible session records. Do not locate hidden transcripts by guessed paths. Confirm evidence resolves and supports the claim at the stated revision. Missing receipts leave the claim unverified; they are not an invitation to reconstruct a successful result.

For substantial or high-risk work, obtain independent read-only review if available. Give the reviewer the log and the permitted receipts, and ask for weak evidence, skipped gates, stale revisions, and unresolved risk. Another context gives independent review; another pass by this assistant is self-review. Model diversity is optional and must be observed, not assumed.

Return the log path or draft, consequential outcomes, and an attention list with evidence pointers. State reviewer coverage accurately. “No flags in this review” is valid, but never infer it from an absent reviewer.
