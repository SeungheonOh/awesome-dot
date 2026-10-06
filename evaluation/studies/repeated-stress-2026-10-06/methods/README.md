# Methods and limits

[Study overview](../README.md) · [24 attempts](../results/attempts.json) · [Requirements](../results/requirements.json) · [Saved evidence](../evidence/)

## What was compared

Four openly synthetic, authored offline workflows were repeated three times per condition: expense reconciliation (R1), dated meeting-action handoff (R2), SQL report reconciliation (R3), and merge/persistence maintenance (R4). Identical task/input bytes were used for repeats. These are four cases and 12 case/repeat pairs, not 12 independent tasks.

- C: common instructions and task packet, without the designated package
- S: the same packet plus its designated package and a fixed instruction to read it

C may still have ambient runtime instructions or skills. This is an incremental designated-package comparison. Both conditions requested fresh native cloud agents, no inherited conversation, `xhigh` reasoning effort, and no model override. Exact serving model/build, backend equivalence, identical ambient tool inventory, tokens and provider cost were not independently exposed and remain unknown.

The eight guide/example files were pinned at repository commit `67bb5a82d3d97c1ee1bbbfaa3e695a604c3a0d56`, retrieved with Git blob and SHA-256 bindings. The treatment included each package's internal referenced files and the repository license; neighboring packages and external webpages were outside the allowlist. [Inspect guide provenance](../provenance/packages.json) and [the supplied files](../guides/).

## Frozen before outcomes

The synthetic cases and scoring fixtures were AI-authored and separately reviewed before trials. Task authors were separate from package preparation and instructed not to read the designated guides or candidate submissions. Requirements were reviewed for task grounding, solvability and distinguishing controls before dispatch. This separation was procedural, not independently enforced blindness. Separate conversations do not establish independent model families or population validity.

Task/input, grader/rubric, reference/control, package, common-instruction, schedule and prompt hashes were frozen before dispatch. The final preparation freeze was at 2026-10-06 06:01:34 UTC; the first dispatch intent was at 06:03:44 UTC. A visual-selection rule was added before any dispatch without changing tasks, scoring or prompts. [Freeze metadata](../provenance/freeze.json) and [source bindings](../provenance/source-bindings.json) distinguish exact bytes from public projections.

The published `cases/<case>/candidate/` directories contain the actual task/input packets, including supplied starter output where applicable. Their sibling `private/` directories contain frozen scoring sources, rubrics, references and author controls. “Private” here means withheld from candidate attempts, not user data. Author references and control checks are preparation evidence, never candidate outcomes.

## Schedule and first submissions

A predeclared seeded schedule fixed 24 rows: six CS and six SC pairs, with balanced within-case order. Dispatch followed row order; up to four attempts could overlap. Pair order means dispatch order, not completion order. All 24 first submissions remain in every results view; none was replaced or selected as the best of several.

Caps were 900 seconds for R1–R3 and 1,500 seconds for R4, measured from controller dispatch intent. The retained elapsed times run from dispatch intent to first terminal observation and include queue, tools, overlap and observation delay. They are approximate controller timings, not verified model-compute budgets or productivity measurements. [Public schedule](schedule.json), [observed event ledger](../results/ledger-public.json) and [collection receipts](../receipts/) preserve that distinction.

## Artifact collection and boundaries

The 45 original artifact files were copied without executing them and are published byte-for-byte. Collection rejected unsafe file types and recorded hashes/errors. Input/package content matched at collection and at the final binding check. The original 96-record ledger's chain was checked before public projection. This demonstrates retained content consistency, not comprehensive process integrity.

Every attempt shared a filesystem. Directory allowlists, separate contexts and review masking were instructions, not OS/process/network isolation. Transient prohibited reads or edits, training exposure and descendant quiescence cannot be ruled out. Snapshot collection was non-atomic. Overall process integrity remains unknown for every attempt, even when every artifact requirement passes.

## What a pass means

There are 53 distinct requirements and 318 scheduled instances. Each requirement is binary with a separate not-assessed state. A pass requires saved evidence; missing evidence is neither a verified pass nor proof of a defect. “All criteria met” refers only to the predeclared artifact requirements, not live deployment, broad correctness or process acceptance.

- R1/R2: 11 mechanical requirements and three source-grounded semantic requirements per submission
- R3: 12 deterministic requirements using three fixture scenarios, source-inspected SQL, read-only SQLite controls, an allowlisted authorizer and bounded resources; no candidate Python execution
- R4: 13 deterministic behavioral requirements, after exact submitted Python/dependencies and frozen probes were inspected and the exact hash-bound plan approved; bounded writes used evaluator-owned fixture copies

R4 source-reviewed execution is not a general Python sandbox or OS-isolation guarantee. Public plan summaries retain source/probe/runner/plan/approval hashes and limits while omitting private authorization messages and machine paths. Their original hashes identify retained records; omitted private preimages cannot be reconstructed from this bundle.

### Semantic review

Each R1/R2 artifact pair received two distinct AI-assisted reviews from fresh contexts. Reviewers saw a single opaque packet containing task, sources, frozen rubric/instructions and exact artifacts; they were instructed not to inspect conditions, schedule, other submissions or peer reviews. Artifact content might reveal condition. Masking and independence are procedural and self-attested, not enforced access boundaries or human evaluation.

The unchanged frozen grader requires two-review agreement and preserves both rationales. Missing reviews or disagreement stay not assessed pending separately recorded masked adjudication; original judgments are never overwritten. Public review records expose opaque reviewer labels, timestamps, packet/source/artifact bindings and judgments, without private agent identities. Internal reviewer handoff text is omitted; its original packet-manifest hash is retained, while the frozen case review instructions and complete judgments are public.

Candidate notes and final self-reports did not supply independent test counts or grading evidence. Inspect saved grader outcomes and semantic rationales instead.

## Reporting choices

All three repeats appear for every case/condition, with raw pass/fail/not-assessed denominators and paired verified-pass differences. The descriptive aggregate is the equal-case mean of each case's verified fraction; unknowns remain in scheduled denominators. Different requirements are not interchangeable measures of general quality.

No confidence intervals, significance tests, population efficacy, causal model-level effects, human-time savings, cost savings or full-dot efficacy claims are made. A ceiling tie is a valid result and may indicate limited discrimination. This study is separate from the historical eight-case native-cloud study and the original sealed protocol, which remains unrun.

Examples follow a predeclared rule: first substantive observed failure in case/requirement/dispatch order plus first verified success from a different case. If there is no observed failure, representative verified outputs are shown and the absence of a failure example is stated. No not-assessed evidence is recast as failure and no visual variation is invented.

## Operational deviations and caveats

1. **Post-start bootstrap deviation.** T01–T04 used the frozen bootstrap with trailing line feeds removed. T05–T24 additionally received a common administrative reporting/permission-handling paragraph. Both members of each pair used the same variant. No task facts, scoring, caps, task/input/package bytes or model attempts changed. The extra wording could affect behavior; prompt identity across the entire study is not claimed. Effective-message hashes are reconstructed from the controller's construction report, not independently captured API requests. See [variant hashes](bootstrap-variants.json) and [operational addendum](operational-addendum.md).
2. **T24 logging disconnect.** A transport disconnect prevented the first launch-record logging process from starting. After verifying no launch event existed, only logging was retried against the intact ledger. The launch timestamp is delayed; no replacement model run occurred. Dispatch intent and the final receipt remained bound to T24.
3. **R4 flattened-input lookup.** Static inspection of flattened saved artifacts could not locate the original TASK.md and smoke-test input. That lookup remains unreadable, not a fabricated pass or candidate failure. Separate collection receipts and final bindings record unchanged protected files. Behavioral results come from the exact approved probe execution, not the missing lookup.
4. **Approximate observations.** Collection/timing hashes are content and controller-observation evidence. They do not prove trusted clocks, isolation, complete tool histories or process acceptance.

## Safe reproduction

From this study directory run `python -I -B reproduce_saved_evidence.py`. It reads JSON and hashes only. It verifies the public manifest, original artifact bindings, per-requirement outcomes, semantic agreements, pair arithmetic and aggregate accounting. It does not import graders, run submitted code or SQL, launch models, install anything, use the network, or write results. Saved-evidence reproduction is not an independent rerun or re-review.
