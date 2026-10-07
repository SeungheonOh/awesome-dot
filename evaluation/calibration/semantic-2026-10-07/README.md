# Semantic grader calibration results

Two fresh review contexts per output matched every accepted gold label in this exploratory calibration: **84/84 individual votes and 42/42 paired outcomes**. All eight deliberately failing checks were detected and all 34 passing checks were preserved. There were no disagreements, reviewer unknowns, missing, invalid or late reviews, or replacement attempts.

These are exact ceiling results on a small set of related synthetic fixtures. They do not establish broad reviewer reliability, measure skill uplift, or change any historical experiment score.

## Results

| Measure | Individual votes | Paired outcomes |
|---|---:|---:|
| Exact gold matches | 84/84 | 42/42 |
| Failure detection sensitivity | 16/16 | 8/8 |
| Passed-check preservation and specificity | 68/68 | 34/34 |
| False failures | 0/68 | 0/34 |
| Reviewer unknown or unresolved outcome | 0/84 | 0/42 |

Each of the two reviewer replicas independently matched 42/42 labels. Both detected an actually defective criterion in all six defective outputs. None of the eight acceptable outputs received a false failure. The four outputs emphasizing genuine uncertainty in source facts preserved all 12 passing checks, yielding 24/24 passing individual votes. Correctly explaining uncertain task facts is different from a reviewer lacking enough evidence to decide.

| Criterion | Paired failed checks detected | Paired passing checks preserved | Individual failed checks detected | Individual passing checks preserved |
|---|---:|---:|---:|---:|
| R1-12 | 1/1 | 6/6 | 2/2 | 12/12 |
| R1-13 | 1/1 | 6/6 | 2/2 | 12/12 |
| R1-14 | 1/1 | 6/6 | 2/2 | 12/12 |
| R2-12 | 1/1 | 6/6 | 2/2 | 12/12 |
| R2-13 | 2/2 | 5/5 | 4/4 | 10/10 |
| R2-14 | 2/2 | 5/5 | 4/4 | 10/10 |

The failed checks were SC03:R1-12, SC04:R1-14, SC09:R2-13, SC10:R2-13/14, SC13:R1-13 and SC14:R2-12/14. Their defects include invented payment or approval, incorrect policy timing, omitted required handoff work, fabricated ownership, an omitted unresolved evidence request and invented acceptance of excluded scope. The [raw reviews](reviews/) preserve each evidence-grounded rationale. Full confusion matrices, all 84 votes and all 42 paired outcomes are in [the analysis](results/analysis.json).

## Study design

The cohort contains 14 outputs over two frozen tasks: expense reconciliation and action-register handoff. Seven outputs use each task, and each output has a structured JSON artifact and prose artifact. The mix is four baseline-correct outputs, six deliberately incorrect outputs and four outputs handling genuine source uncertainty correctly. Structured results remain correct throughout; the unchanged objective grader passes 154/154 checks.

Gold contains 34 pass, eight fail and zero unknown labels. A reviewer separate from the fixture author accepted all labels without changes. This gold review was label-aware; that reviewer had also proposed the two additional negative mutations before auditing their implementation. It was not blinded or independent of mutation design, and gold agreement is not counted as performance evidence.

Before predictions, the operational cohort froze its gold, packet hashes, 28 exact prompts, deterministic randomized schedule, 480-second per-review deadlines, first-submission policy and aggregation. Each reviewer received a fresh context, one opaque packet path, its task sources, rubric and one candidate's two output artifacts. No model override was requested; requested reasoning effort was xhigh. Exact serving model/build, temperature and token limits were not exposed. All 28 serving-model disclosures remain unknown.

Two matching valid pass/fail votes determine a paired result. Other pairs remain unknown, with raw votes and delivery reasons retained. All planned positions remain in metric denominators. There were no later adjudications, feedback-driven revisions, selective reruns or replacements. Review final messages arrived 47–75 seconds after observed spawn acknowledgement, within the fixed 480-second windows.

## Limits and deviations

- **Procedural masking only.** Reviewers shared a filesystem. One-packet access was instructed, not enforced by OS isolation. All reviewers reported no outside-task exposure, but a full independent file-read telemetry audit was not available. The source protocol's strict isolation gate was unmet. A separately named exploratory amendment accepting this limitation was approved and frozen before predictions
- **Sparse, related examples.** These are variants of two tasks, with identical structured JSON within each task family. Each criterion has only one or two negative examples. Eight failed checks overlap across six defective outputs; repeated votes and overlapping checks are not independent defects
- **Unknown sensitivity is untested.** There are no gold unknown cases. Zero observed unknown votes does not establish reliable behavior when evidence is genuinely insufficient
- **Temporary concurrency deviation.** Between approximately 03:20:12 and 03:20:37 UTC, two semantic reviewers overlapped one engineering-v1 candidate. The semantic cohort stayed within its two-reviewer cap but exceeded the other cohort's stricter global two-trial bound. Both first reviews were retained, the overlap was recorded, and subsequent dispatch honored the clarified limit until engineering v1 ended
- **Interruption between waves.** A dispatcher interruption was recovered after checking durable submissions and live status. Twenty-two reviews were already terminal; six were unstarted and no semantic review was in flight. The remaining six ran in the original fixed order, without lost or replaced reviews
- **No historical rescore.** Original source artifacts, rubric, gold-authoring stage and historical results remain unchanged. This study contains no skill/no-skill intervention and supports no skill uplift or model ranking claim

A constant all-pass reviewer would match 34/42 gold labels while detecting 0/8 failures. The actual reviewers detected these specified defects; the small, exposed fixture set remains unsuitable as a broad reliability certificate or as held-out validation for later tuning.

## Evidence and reproduction

- [Protocol and provenance hashes](protocol.json): settings, limits, deviations and the original freeze hashes
- [Gold labels and evidence](gold.json): accepted labels, source-grounded rationales and exact artifact hashes
- [Schedule and timing](schedule.json): fixed order, opaque reviewer IDs, prompt hashes, raw-review hashes and observed times
- [Raw reviews](reviews/): all 28 first submissions, byte-for-byte preserved
- [Synthetic sources](sources/) and [candidate outputs](outputs/): unchanged evidence and evaluated artifacts
- [Frozen-grader results](results/frozen_grader/): all 42 semantic statuses match the separate analysis
- [Prompt projection](reviewer_prompt_public_projection.txt): a clearly labeled public projection; the exact execution template and messages remain hash-bound, and no execution prompt was changed

Original source citations use candidate/inputs paths and private/rubric.json relative to each task family. In this package those map to sources/R1 or sources/R2, with the evaluator-only directory named evaluator. This directory rename does not change file bytes. Objective expected values were not supplied to masked reviewers; they are included here for post-run verification.

Run `python verify.py` from this directory to verify the package hashes, reconstruct every vote and paired result, and compare them with the unchanged frozen graders. An independent deterministic audit reproduced the recorded results and verified the preserved evidence; the limits and deviations above still apply.
