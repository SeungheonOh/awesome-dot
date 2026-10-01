# Worked example: Write testable acceptance criteria

This is a fictional example. The request, product rules, learner response, and agent outputs below are illustrative. No learner completed this workbook and no product was tested.

## Supplied inputs

```text
Skill: Write acceptance criteria with an exact condition and observable outcome.
Context: A small catalog tool previews a requested label quantity.
Source: Fictional product note, version 1; complete relevant rules below.
P1. Quantity must be a whole number from 1 through 5, inclusive.
P2. On Preview, an accepted quantity appears unchanged in the preview.
P3. For an out-of-range or non-whole quantity, show exactly:
    "Use a whole number from 1 to 5". Do not show a preview.
P4. For a missing quantity, show exactly:
    "Enter a quantity". Do not show a preview.
P5. Preview never submits or saves a request.
Workbook: Five exercises; plain Markdown; show answers separately.
Permitted aids: The product note. No product or repository access.
Current work samples: None; use a fictional baseline without grading me.
```

## Illustrative agent output: Attempt-first workbook

The first bottleneck is making a criterion independently checkable. Write three fields for each exercise: Setup, Action, and Observable result. Name the exact input, the displayed result, and whether anything is submitted or saved. Use the supplied rules; do not invent a confirmation screen.

- **B0, baseline:** The quantity is 3. Describe what should happen on Preview
- **D1, boundary drill:** Change only the quantity from 3 to 1. Write the criterion again
- **D2, adjacent-value drill:** Change only the quantity from 1 to 0. Write the criterion again
- **D3, missing-input drill:** Change only the quantity from 0 to missing. Write the criterion again
- **T1, transfer:** A separate fictional layout tool accepts a whole number of columns from 2 through 8. Its Preview shows accepted columns unchanged, never submits or saves, and shows “Use a whole number from 2 to 8” without a preview for an out-of-range or non-whole value. Write the criterion for 9 columns, then explain why copying the old error text would be wrong

For D1–D3, only the input value or presence changes. The product note, action, output format, and scoring criteria stay fixed. T1 deliberately changes context and limits to test transfer.

### Rubric supplied before scoring

Score each dimension separately; these are observations about one written criterion, not an overall ability score.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Condition and action | Missing or incorrect condition, or a conflicting action | A compatible broad input class with Preview or no stated action; or the exact supplied input with the action omitted | Exact supplied value or explicit missing input, with the specified Preview action |
| Outcome | Wrong or unobservable result | Correct accept/reject decision, but missing value or exact message | Exact preview value or required message, including preview absence on rejection |
| Scope | Claims a submission or save occurs | Submission/save behavior omitted | Explicitly states no submission or save |

No response means **unevaluated**, not three zeros. Equivalent wording is acceptable unless the product note specifies exact displayed text. A named conflicting action, such as Submit, earns 0 for Condition and action even when the exact input is present; do not infer Preview from a correct expected result. A conflicting exact input also earns 0 (for example, quantity 4 in the quantity-0 exercise), even if its trigger is Preview. Apply a 0 anchor before considering partial credit.

T1 also requires a separate explanation: the new source changes the allowed range from 1–5 to 2–8, so reusing the old error message would contradict that source. Mark this explanation **supported**, **missing**, or **contradicted**, citing the response. T1 is complete only when its three dimensions earn 2 and its explanation is supported. B0 and D1–D3 do not require this additional explanation.

### Learner record

```text
Exercise ID:
Actual response:
Assistance used:
Condition and action / Outcome / Scope evidence:
T1 explanation evidence and completion status (if applicable):
Revision:
Next exercise and reason:
```

## Solution boundary: Illustrative answer guide

Read this after attempting the exercises, or if a worked example is requested.

- **B0:** Setup: quantity 3. Action: select Preview. Result: preview shows 3; nothing is submitted or saved
- **D1:** Setup: quantity 1. Action: select Preview. Result: preview shows 1; nothing is submitted or saved. The lower endpoint is included by P1
- **D2:** Setup: quantity 0. Action: select Preview. Result: show “Use a whole number from 1 to 5”; no preview, submission, or save
- **D3:** Setup: quantity missing. Action: select Preview. Result: show “Enter a quantity”; no preview, submission, or save. Missing input follows P4, not P3
- **T1:** Setup: 9 columns. Action: select Preview. Result: show “Use a whole number from 2 to 8”; no preview, submission, or save. The new source defines different limits, so the old message would contradict it

### Wrong-answer branch

Fictional D2 response:

```text
Given quantity 0, when Preview is selected, show a preview of 0.
Nothing is submitted or saved.
```

Illustrative feedback:

“You specified the exact input and kept Preview separate from saving. Condition and action: 2; Outcome: 0; Scope: 2. The phrase ‘show a preview of 0’ conflicts with P1 and P3. Check the smallest permitted quantity, then revise only the displayed outcome. What must appear instead?”

The next step is a revised D2 attempt. Do not mark the skill mastered or advance solely because the other dimensions scored well. If the learner asks for the answer, reveal D2 and label the later retry as assisted.

### Missing-answer branch

Illustrative response:

“D2 is still unattempted. Start with one decision: is 0 inside the permitted interval? You can answer that first, or ask to see the worked example.”

Leave the response and score empty. Do not invent a failure, add an assessment record, or send reminders.

## Checks a reader can repeat

1. Trace each worked result to P1–P5 or the distinct T1 source; no hidden product behavior is needed
2. Check the endpoints: 1 and 5 are accepted; 0 and 6 are rejected
3. Check 1.5: it is within the numeric interval but is rejected because it is not whole
4. Check missing input: it has a different message from an out-of-range number
5. Score the fictional wrong answer independently: exact condition and no-save statement earn 2 each; the contradicted outcome earns 0
6. Replace “nothing is submitted or saved” with “no request is committed”; accept it if its meaning clearly covers both prohibited effects
7. Inspect T1: 9 is outside 2–8, and its message must use the new limits
8. Replace Preview with Submit in an otherwise correct D2 response: Condition and action is 0, while Outcome and Scope can still be 2; this does not demonstrate the requested trigger
9. Remove only the explanation from an otherwise correct T1 response: the three dimensions remain 2, but explanation is missing and T1 is incomplete. Saying “the old message is wrong” without relating it to the changed limits is not a supported explanation

## Actual verification and limits

During authoring, the supplied rule was checked against missing input, 0, 1, 3, 5, 6, and 1.5 using a small independent rule calculation. The listed accept/reject outcomes and message distinctions agreed. Exercise identifiers, solution coverage, and the wrong-answer rubric were also reviewed. A later manual rubric review checked a wrong-trigger response, an omitted-trigger response, and a correct T1 criterion with its explanation removed; the anchors now distinguish these from a complete answer. This was a review of stated criteria, not automated grading of free text.

These are checks of this fictional artifact. Product execution, learner performance, retention, and transfer remain untested.
