# Fictional Routing Examples

These examples use real entry points in this repository and invented requests. Paths should be resolved against the collection actually available when the skill runs. No example is a permanent inventory or proof of live task execution.

## Same input noun, different result

| Fictional request | Primary route | Why, and what happens next |
| --- | --- | --- |
| “Use these receipts and our supplied policy to prepare my reimbursement draft. Leave unknown business purposes unresolved. Save it privately.” | [Expense report reconciliation](../expense-report-reconciliation/SKILL.md) | The output is a policy-governed claim draft. Read the full guide, classify receipt/credit evidence and policy treatment, produce the report and verify its saved contents. Do not send or submit it |
| “Use this spending export and budget to explain why the total changed. The reporting period and categories are supplied.” | [Budget variance waterfall](../budget-variance-waterfall/SKILL.md) | The output is an explained plan-versus-actual difference. It is not a reimbursement claim. Reconcile the comparison and produce the requested explanation/visual when supported |
| “These receipts are for several people. Tell me how to split them, but I haven't said which people share which items.” | Inspect current descriptions for a group-allocation workflow | Do not choose reimbursement merely because it handles receipts. Resolve a real current entry point if one exists; otherwise state that the inspected collection has no confirmed match and use a bounded ordinary allocation approach. Ask for the material participant/share rule while preserving known payments. No imaginary path or transfer is allowed |

The third row intentionally has no hardcoded link to a workflow that might not be present in a copied or partial collection. The router must inspect what it can actually read.

## A clear request should lead to work

Request: “Make five editable slides from these approved notes for the stated audience. Include sources and speaker notes, then save the deck for review.”

Route: [Source-backed presentation](../source-backed-presentation/SKILL.md).

Read the complete guide and inspect available authoring capability. If native creation and inspection are supported, create the deck, check the exact exported file and save it as requested. A reply that merely says “I recommend the presentation skill” leaves the task unfinished. If the necessary authoring capability is absent, return a complete useful script only as an explicitly limited fallback; do not label it a finished editable deck or claim it was rendered.

No additional permission is needed merely to use already-approved notes and save the requested private draft. Uploading to a new service or publishing it would be a different action.

## A minimal sequence needs a real dependency

Request: “This CSV has ambiguous dates and duplicated receipt rows. Clean it without discarding unresolved records, then compare actual spending with the supplied category budget.”

The [spreadsheet cleanup workflow](../spreadsheet-cleanup-reconciliation/SKILL.md) can establish a reconciled table with lineage and held rows. The [budget comparison workflow](../budget-variance-waterfall/SKILL.md) then consumes that result, keeping incomplete totals and category mapping visible. The handoff is the cleaned data plus its unresolved-record report, not an undocumented replacement of the original.

If inspection instead shows the table is already suitable and the apparent duplicates are separate legitimate transactions, do not run a cleanup pass just to use two skills. Use the single adequate comparison route and preserve the evidence.

## An ambiguous task needs one useful question

Request: “Can you clean this up?” Attached material includes a draft presentation and a spending CSV, with no stated desired output.

Ask which result the user needs first: a revised presentation or a reconciled spending table. Do not select based on the word “clean,” edit both files, or ask about every detail before the target is known. Once the user chooses, read the full applicable workflow and continue under that answer.

## An incomplete listing is not a full search

Observed state: a repository connector returns the first page of directories and a continuation token. A plausible form-filling guide is visible, but remaining directory pages have not been read.

Follow the continuation when available. If it cannot be retrieved, report the inspected scope and evaluate the visible guide on its own merits. You may use a clearly adequate accessible match without claiming it is the best of every unseen candidate. Do not report “no relevant skill exists” merely because a desired name was absent from the first page.

The same principle applies when a linked entry point is inaccessible: knowing its name or finding it in an old conversation does not establish its current instructions.

## Selection does not create authority

Request: “Prepare a factual secondhand listing draft from my supplied details. Do not post it.”

If the current inspected collection has no matching seller-draft workflow, say that limitation accurately and prepare the ordinary draft from supported facts if available. Do not route to a purchase comparison just because both involve products. Do not publish the listing, infer equipment condition, choose a buyer or reveal a pickup address. A future added listing skill would still not override “Do not post it.”

## Review criteria

For each case, check the resolved path and complete instructions, desired output, necessary inputs, authority boundary and whether execution actually follows selection. A no-fit response should be bounded by the inspected collection. A route must never select this router again. These are manual decision examples, not automatic keyword tests or evidence that the fictional requests were executed.
