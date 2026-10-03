# Historical synthesis contract

Inputs: the original question, code anchor and revision, source findings, and coverage gaps. Read [epistemics](epistemics.md). This is read-only synthesis; do not fix code, ask third parties, or publish a report unless separately authorized.

Read every supplied finding. Merge duplicates while retaining independent support. Confirm consequential citations when the actual source is available. If not, attribute the finding to the supplied excerpt or report and disclose the narrower verification. Do not launder an unverified worker claim into a direct source claim.

Build the answer around the question, not a source-by-source dump. Separate the historical trigger, choice of mechanism, numerical tuning, and present necessity when they have different evidence. A source can answer one and leave another unknown.

## Reconciliation

For each claim identify its tier: Direct, Supported, Inferred, Speculative, or Unknown. State direct documented claims precisely, hedge interpretations, and omit empty conjecture. Check dates, candidate revisions, superseded plans, release timing, and copied sources. Show conflicts that change the conclusion. Explain when apparent conflicts concern different scopes.

Telemetry and error trends usually establish temporal association, not causal authorship. A closed ticket records status, not verified product behavior. A design note records intent, not proof that the final implementation matches it. Preserve these distinctions.

## Suggested answer shape

Adapt length and headings to the task. A small answer need not carry eight empty sections.

1. The answer with calibrated confidence
2. Target code or decision, including revision and locations when useful
3. What the record states, with citations adjacent to each claim
4. Reasonable interpretations and their evidence chain
5. Competing explanations if evidence cannot distinguish them
6. Important unknowns and the specific missing evidence
7. Source coverage: actual searches/time windows, relevant nulls, unavailable and unsearched sources with reasons
8. A concise confidence summary if several claims differ in strength

If the work prepares a change, add Preserve / Change / Avoid / Risk constraints tied to evidence. Do not imply the investigation authorizes implementation or external action.

## Before returning

Check that every factual claim is supported, every inference is labeled, and uncertainty survived editing. Verify that a cited source says what the answer attributes to it. Acknowledge the user's hypothesis without endorsing it automatically. Give the useful negative answer when no rationale was found. Do not manufacture a satisfying origin story.
