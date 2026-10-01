# Worked example: Read a fictional row-preview study

Everything attributed to the paper below is invented for this example. It is not a real publication, citation, product evaluation, or current research claim. The sample agent output is illustrative; actual artifact checks are listed separately.

## Supplied request and source

```text
Reader: Comfortable with spreadsheets; unfamiliar with research statistics.
Question: Does this paper justify adopting a row preview for our large,
collaboratively edited catalog files?
Requested output: Reading route, claim map, glossary, three comprehension
questions, a small conceptual example, and a separate answer guide.
Source: Fictional paper "Row Preview and Catalog Checks", excerpt version A.
Coverage: Only A1, M1, M2, R1, L1, and D1 below. No other pages supplied.

[A1 — Abstract]
A row preview improved correct-check rates by 25% in a controlled task.
This finding suggests row previews could help routine catalog data entry.

[M1 — Method: participants and assignment]
Forty adult volunteers familiar with spreadsheets were randomly assigned
in equal groups: 20 used a basic editor and 20 used an editor with a row
preview. Each participant judged the same 10 synthetic six-row files in
the same fixed order, producing 200 judgments in each group.

[M2 — Method: outcome and task rule]
Both groups received the same written validation rules. A judgment counted
as correct if the participant correctly accepted a valid file or rejected
an invalid file. This was one binary outcome per file, not one per row.
One rule was that every item identifier must be unique; column order did
not matter. Figure 1 illustrated the row-preview interface, but the figure
is not included in these supplied excerpts.

[R1 — Results]
The basic-editor group made 120 correct judgments out of 200 (60%).
The row-preview group made 150 correct judgments out of 200 (75%).
No participant-level score distribution or confidence interval is supplied.

[L1 — Limitations]
The files were small and synthetic. Outcomes were collected in one session.
The study did not assess large files, collaboration, actual data-entry
errors in routine work, or whether any benefit persisted. Multiple judgments
came from each participant; the 200 judgments were not 200 independent users.

[D1 — Discussion]
The authors propose testing the preview in a real catalog workflow before
recommending routine adoption.
```

## Illustrative agent output: Reading companion

The supplied excerpt supports a higher correct-judgment rate in this particular task. It does not establish that the preview improves large, collaborative catalog work. The evidence needed for that application is explicitly absent in L1, and D1 proposes further testing.

### Reading route

1. Read A1 and predict what “25%” compares before checking the numbers
2. Read M1–M2 to identify who participated, what differed, and the exact outcome
3. Recompute R1, distinguishing a relative increase from a percentage-point difference
4. Read L1–D1 and name one assumption needed to apply the result to the requested setting

### Claim-to-evidence map

| Claim | Inspectable evidence | Reading conclusion |
|---|---|---|
| Correct-check rate improved by 25% | R1: 120/200 versus 150/200 | The relative increase is 25%; the absolute rate difference is 15 percentage points |
| The preview helps routine data entry | A1 suggests it; M2 measured file judgments | The measured outcome is different from routine data-entry errors; application remains uncertain |
| The result applies to large shared files | L1 says these were not assessed | Unsupported by the supplied study |
| The exact interface can be reproduced | M2 mentions unavailable Figure 1 | Interface details cannot be reconstructed from these excerpts |

M1 establishes randomized assignment as described by the fictional authors. The reported counts alone do not provide the missing uncertainty analysis or establish the size of a reproducible effect. Treat the observed difference as a result in this sample; do not label it statistically significant.

### Small glossary

- **Baseline:** The comparison condition, here the basic editor's 60% correct rate
- **Denominator:** The population of counted outcomes, here 200 file judgments per group
- **Percentage points:** Subtraction of percentages: 75% minus 60% equals 15 points
- **Relative increase:** The increase divided by the baseline: 15/60 equals 25%
- **Repeated observations:** Each participant contributed 10 judgments, so judgment count is not participant count

### Attempt-first questions

- **Q1:** What exactly was compared and counted? Include the participant count, judgment count, and outcome definition
- **Q2:** A colleague says, “The preview was 25 percentage points better.” Repair the statement using both an absolute and a relative comparison
- **Q3:** Which two mismatches most directly limit applying this result to the supplied catalog context? Name the source locator and one kind of additional evidence that would help

### Conceptual example

This is a teaching example, not a replication of the study. Apply the uniqueness rule in M2:

```text
item_id,label
11,Blue folder
12,Green folder
11,Red folder
```

Should this file be accepted? Would rearranging the columns fix the issue? Predict first, then consult the answer guide. The exercise teaches the task rule; it does not measure whether a preview helps anyone use it.

## Solution boundary: Illustrative answer guide

- **Q1:** Basic editor versus editor with row preview; 40 volunteers, 20 per group; 10 judgments per participant and 200 per group. A judgment counted as correct when the participant correctly accepted a valid file or rejected an invalid file; the unit was a file judgment, rather than a row. R1 reports 270 correct and 130 incorrect judgments across both groups. Sources: M1–M2 and R1
- **Q2:** Correct rate rose from 60% to 75%, an increase of 15 percentage points or 25% relative to the 60% baseline. The calculation is (75−60)/60 = 0.25. Source: R1
- **Q3:** Large files and collaborative editing were not assessed. Suitable next evidence would include an authorized evaluation using representative large-file tasks and collaboration conditions, with an outcome relevant to real data-entry mistakes. This is an evidence-needed proposal, not permission to run it. Source: L1. Other justified answers about task or persistence may also be valid
- **Conceptual example:** Reject because identifier 11 appears twice. Reordering columns leaves the duplicate unchanged. Source: M2

### Wrong-answer branch

Fictional Q2 response:

```text
75 minus 60 is 15, so the improvement is 15% relative to the basic editor.
```

Illustrative feedback:

“You correctly found the difference of 15 percentage points. The relative comparison still needs the baseline denominator. In R1, which rate is the baseline? Divide the 15-point difference by that rate, then revise your wording.”

Record Q2 as partially correct with this evidence. Do not mark the whole paper understood. If the learner requests the solution, reveal the calculation and label a subsequent retry as assisted.

### Missing-answer or missing-source branch

- If the learner does not answer Q1, leave it unevaluated and ask the smaller question: “Does 200 refer to people, rows, or file judgments? Check M1–M2.” Do not fabricate an attempt
- If only A1 is supplied, return its question and claims, but request methods and results before verifying the 25% statement. Do not reuse the counts above as though they came from the user's incomplete file
- If a new result excerpt conflicts with R1, retain both values and their versions, flag the discrepancy, and ask which version governs. Do not silently choose the more impressive number

## Checks a reader can repeat

1. Compute 20 × 10 = 200 judgments per group, then 200 + 200 = 400 total judgments from 40 people
2. Compute 120/200 = 0.60 and 150/200 = 0.75
3. Compute 0.75 − 0.60 = 0.15, or 15 percentage points
4. Compute (0.75 − 0.60)/0.60 = 0.25, or a 25% relative increase
5. Trace every substantive claim to an excerpt identifier; confirm no unseen interface details or uncertainty interval were invented
6. Check whether feedback distinguishes arithmetic success from denominator error and leaves missing responses unevaluated
7. Compare the final application conclusion with L1 and D1: no routine-adoption endorsement follows from these excerpts

## Actual verification and limits

During authoring, the group totals, rates, percentage-point difference, and relative increase were recalculated using exact fractions. All six source locators used in the guide were checked against the supplied fictional excerpts, and the answer guide covers all three comprehension questions plus the conceptual example.

No real paper was retrieved, no interface or study was reproduced, and no learner responses were collected. Statistical significance, real-world effectiveness, and learner understanding remain unestablished.
