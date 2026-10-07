# Methods and limits

## Design and task exposure

This cohort was authorized separately as an exploratory non-sealed, procedural-boundary run after independent AI-assisted case/scorer review. The source review approved preparation and left execution/isolation gates open; it was not a human evaluation. The actual run must not be described as satisfying the source protocol's strict sealed-isolation gate.

The fixed schedule comprised six two-submission waves:

1. T1 repeat 1: C then S
2. T2 repeat 1: S then C
3. T1 repeat 2: S then C
4. T2 repeat 2: C then S
5. T1 repeat 3: C then S
6. T2 repeat 3: S then C

This was fixed counterbalancing, not randomization. Across six pairs, three were C-first and three S-first. Within T1 the order was 2:1 C-first; within T2 it was 2:1 S-first. Maximum observed acknowledgement-to-terminal overlap was two transfer candidates, and native terminal status was checked before advancing waves. These intervals do not certify backend scheduling or global concurrency.

Each submission requested a fresh native session with `fork_turns=none`, reasoning effort `xhigh`, and no model override. Those are requested configuration values, not measurements of actual model/build or compute. Actual model/build, complete realized tool/instruction inventory, token use, cost and precise backend runtime are unknown. Ambient skills and higher-priority runtime instructions could remain exposed to both conditions.

Both conditions received byte-identical effective TASK.md and source inputs within each case. S additionally received its exact designated guide files and the instruction to read/apply them. The procedural boundary allowed local file/shell work with standard-library Python and SQLite, restricted task-data reads to the supplied packet and own outputs/scratch, and prohibited network, external services, installations, other attempts and evaluation material. A procedural prohibition is not evidence of enforcement or an audit proving no access. Shared filesystem and ambient tools remained.

Public prompt projections are newly authored descriptions of common task/condition information. They omit environment-specific paths, operational coordination and authorization text. They were not dispatched and must not be called exact historical prompts. Private intended/observed-reconstruction prompt hashes are retained as labeled hash projections; matching hashes in eleven records reflect controller observation rather than independently retrieved transport.

## Budget and collection

The reviewed source tasks said “You have 900 seconds.” Before candidate outcomes, one exact common sentence replacement produced the effective “You have 1800 seconds.” task versions. All other TASK.md bytes were unchanged, and the source-author freezes were not edited. Each candidate's 1800-second window began at the observer's successful spawn acknowledgement; there was no shared pair cutoff. The schedule also had an absolute hard stop, which truncated none of the 12 windows.

The first terminal response determined the submission. The collector recorded observer UTC, confirmed native terminal status, claimed the first event, then copied only the fixed output names without SQL, JSON or whitespace repair. The bounds were 65,536 bytes for report.sql, 262,144 for reconciliation.json, 524,288 for action_register.json and 131,072 for handoff.txt. Collection required singly linked regular files, no symlink components and no changes during each bounded read.

All 24 files were captured. Input hashes matched at capture and at final verification. Output hashes matched the captured snapshots. Capture started 10.859 to 18.512 seconds after the recorded first-terminal observations. These are collection diagnostics, not speed measurements. The snapshot is bounded at observer collection, not atomic at candidate finalization; undetected intervening changes cannot be excluded. Raw final-message text is private provenance and self-report, and is not included in this public package or credited as test execution.

All 12 first submissions were on time. There were no missing, late, timeout, spawn-error or grader-infrastructure outcomes; no factual hints, candidate corrections, rescues, replacements, retries or primary rescoring occurred. All source and operational hashes passed pre/post checks in the saved records.

## Known dispatch deviation

T2 repeat 1 C's intended dispatch SHA-256 was `53aea7f0f6db7ca409d4188de2d71dc606ac686d498a704b4e4b48bdc2a14dce`. The controller-observed reconstruction SHA-256 was `6436523294517e399fffb8433e09e5359c19bc2d51b2cbf7a4c839e6e710b43c`.

The safe exact delta is “return a brief final message” to “return a brief message.” The independent first-terminal collection rule remained. The controller paused new waves; the root coordinator explicitly approved continuing the remaining unchanged schedule, preserving and disclosing the deviation. No correction, replacement or rerun of that candidate occurred. Exact prompt parity was imperfect, and performance impact is unknown. The private continuation message and operational dispatch texts are excluded.

## Trusted primary grading

One primary grading pass ran only after all 12 slots were terminal and captured. Candidate output files were copied to separate scorer-owned directories. The unchanged trusted graders ran with isolated Python flags `-I -B`, a minimal explicit environment, clean working directory, 12-second wall timeout, 8-second CPU limit, 512 MiB address-space limit, 2 MiB file-size limit and 64 open descriptors. Candidate modules were not imported.

T1 executed submitted SQL as one read-only query on a protected fictional fixture with its existing authorizer, function allowlist, five-second SQL limit, ten-million VM-step bound and 100-row bound. T2 parsed bounded JSON and text; it did not execute candidate code. Successful scorer process exit alone was not a candidate pass. Saved process records, stdout and raw requirement statuses are included. Launch records are labeled projections because command paths/environment locations are private.

The case scoring specifications and expectations are included for inspection. Executable trusted graders and their full dependency trees are intentionally not packaged. The public verifier checks saved evidence/accounting only and does not reproduce or rerun grading.

## Accounting

Every scheduled submission remains in the denominator: three per case-condition, twelve total. T1 has fourteen named checks and T2 twelve, giving 156 scheduled checks, 78 per condition. Pass, fail and unknown statuses remain distinct. Unknown would remain in the scheduled denominator and could not count as passing or all-met. Operational missingness would remain separate from graded task failure. In this run every saved status is pass and no unknown/missing handling changed an outcome.

The preregistered descriptive summaries are passed checks divided by scheduled checks; all-met submissions divided by planned submissions; the unweighted average of the two case fractions within each condition; and S-minus-C fraction for each of six case/repeat pairs. Equal-case averaging avoids giving T1 more weight solely because it has two more checks. There are no significance tests, confidence intervals, new composite metrics, efficacy estimates or pooled historical totals.

## Interpretation

The tie describes these first captured artifacts on two purposefully authored, highly specified tasks. It is not an equivalence or absence-of-effect test. Ceiling performance can conceal differences. Artifact checks do not establish process integrity, honest self-reporting, external actions, generalizable query behavior, real-world handoff quality or production correctness. T1 uses a single public parameter scenario and cannot exclude hardcoding. T2 checks structured facts, schemas and nonempty prose fields, not the meaning of free text.

Authored case controls and this package's verifier controls test checker behavior. They are explicitly non-agent evidence and are not counted among the twelve candidate submissions or 156 primary checks. Historical studies remain separate and unchanged.
