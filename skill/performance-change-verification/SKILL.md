---
name: performance-change-verification
description: "Implement or verify a bounded software performance change against an independent correctness contract; measure the exact baseline and candidate on matched workloads, preserve raw samples and rejected controls, and report only the runtime improvement the measured scope supports."
---

# Verify a Software Performance Change

Establish whether an identified software change makes an agreed operation faster while preserving its required behavior. Deliver actual local implementation and checks when the request authorizes them, plus a reproducible comparison tied to exact source or artifact bytes. A sound result can be “correct on the exercised contract, useful on this batch, inconclusive for small inputs.”

This skill concerns software execution cost. It does not measure human productivity, time saved by an assistant, release packaging completeness, deployment readiness, or a whole service from a small function benchmark. Preserve the user's chosen language, repository, implementation and target environment; the Python example below is an illustration, not a required replacement.

## Establish the decision and execution boundary

Identify these inputs from the request and available files before timing:

- **Operation and decision:** what the user wants to improve, the caller-visible result, and whether the decision is exploratory, a regression check, or acceptance against an existing budget
- **Candidates:** exact baseline and proposed implementation/artifact, relevant commit and dirty changes if applicable, entry point, compiler/runtime versions, dependency versions and build flags
- **Correctness:** required outputs, permitted numerical tolerance, identity and order rules, duplicate semantics, errors and side effects that must remain equivalent
- **Workloads:** allowed input sources, shapes and sizes, data distributions, concurrency, cache state, and which observed or expected usage they represent
- **Measurement:** intended start/end boundary, latency or throughput unit, setup/build cost, resource constraints, repetitions and acceptable total runtime
- **Authority and destination:** whether the user requested inspection, local implementation, local execution, or all three; where a candidate and evidence may be written

Use supplied acceptance thresholds, but never invent a universal speedup threshold across machines. Resolve missing information only when it changes the decision or blocks safe execution. Meanwhile inspect the code, freeze available inputs, and identify observable invariants. Missing baseline measurements remain missing; a remembered “usual duration” is not a baseline.

If verification-only is requested, preserve the implementation and report defects. If a local improvement is requested and edits are authorized, implement the smallest relevant candidate in an isolated copy or the designated workspace, then complete the checks. Do not stop at suggesting a benchmark that you can already run within scope. An unrecognized dependency, live service, production load test, new account, or costly experiment is a separate execution boundary; continue the offline work and name the specific missing authority or prerequisite.

## 1. Fix the contract before looking at speed

Write the comparison's independent acceptance oracle from the caller's requirements. Do not define correctness as “whatever the candidate returns” or accept agreement with a flawed baseline alone. Use separately authored expected outputs for a small diagnostic fixture, then a simple reference model, known mathematical relation, or independently justified invariants for broader inputs.

Make subtle semantics explicit where they matter:

- Stable identifiers retain their original representation; normalization, coercion, case folding and renaming need a contract
- A list may represent occurrences, not a set: distinguish duplicate input rows, repeated query IDs and duplicate output objects
- Missing, null, empty and known zero may mean different things; a truthiness check can silently erase that distinction
- Required output order, tie-breaking, exact fields, errors, input mutation and external effects belong in equivalence
- Numerical tolerance must follow the application's requirements and be fixed before comparing candidates; do not widen it to accommodate the optimization

Execute both baseline and candidate against the same gates. Include empty/minimal inputs and focused counterexamples for the changed algorithm. Check the actual timed workloads as well as unit fixtures. A few hand-picked examples do not prove all inputs; state the tested domain and uncovered cases.

When a plausible shortcut could look fast by doing less required work, create a deliberately wrong control in the isolated harness. Use one concrete contract violation, demonstrate its actual mismatch, and label it ineligible regardless of runtime. If timing the control is permitted and bounded, measure it with the same boundary and retain the samples. Never promote it after a favorable result, silently repair its outputs outside the measured boundary, or ship it as the optimized candidate. A real failing candidate receives the same rejection even if the baseline is slow.

Stop an acceptance comparison on a failed or unverified required gate. A rejected candidate's measured cost may remain as diagnostic evidence, but it is not a speedup for equivalent work. If repairs are authorized, make a new identified candidate and rerun the affected gates; retain the earlier attempt and its disposition.

## 2. Freeze what will run

Record a portable identity manifest for the actual implementation, harness, correctness contract, workload bytes, configuration and built artifact if one exists. Use relative locators and content hashes such as SHA-256; add revision information for navigation, not as a substitute for the bytes actually executed. A source commit with unrecorded local edits is not an exact candidate identity.

If a build is involved, retain its inputs and flags, identify the output, and time that output. Rebuilding creates another artifact. Keep build time separate unless the user's cost boundary includes it. Recheck hashes after measurement; changed bytes invalidate attribution to the frozen candidate. A hash binds content, not provenance, authenticity or evidence that a program was executed.

Use comparable workloads for every variant. Preserve raw inputs when allowed, or provide a deterministic generator, seed, parameters and hashes of the exact generated bytes. Keep favorable and unfavorable sizes visible. Do not choose only the input range where an index or cache amortizes well. If supplied records are sensitive, use the authorized destination and retention rules; do not publish them as sample data.

The bundled example uses authored fictional data only. Its scale and distribution do not represent a production workload.

## 3. State precisely what each timer includes

Define the unit of one completed operation and draw the timer boundary in words before executing it. Match baseline and candidate boundaries.

| Scope | Questions that affect the interpretation |
| --- | --- |
| Algorithm only | Are inputs already parsed? Is candidate indexing/precomputation inside each call or reused? Are allocation, output construction and wrapper overhead included? |
| Named pipeline | Does the interval include decoding, validation, transformation, encoding, transport, file writes and their completion? State every omitted phase; an in-memory JSON pipeline is not a full application measurement |
| Setup/build | What costs occur once or per job? Show observed preparation separately. Do not move only the candidate's work outside the timer or amortize across hypothetical future operations |
| Warm/cold state | Were code, inputs, indexes, file pages or connections already used by correctness tests or warmups? What was actually reset? A new process alone does not demonstrate cold OS caches |

Measure the scope the decision needs. Function-only evidence may help diagnose a change, but cannot establish a service latency improvement. If an additional broader scope is cheap and authorized, measure it separately and explain why the result differs. Otherwise state the missing measurement without extrapolating.

Use an appropriate monotonic elapsed clock for latency, record its implementation and reported resolution, and avoid claiming nanosecond accuracy merely because values use nanosecond units. If CPU time, throughput, memory or tail latency matter, collect them explicitly with appropriate tools; elapsed time alone does not establish them. Preserve garbage-collection policy and any profiler overhead. The example uses Python's integer `perf_counter_ns()` with automatic GC enabled; `timeit` would disable GC by default unless configured otherwise. See the [Python clock documentation](https://docs.python.org/3.12/library/time.html#time.perf_counter_ns) and [timeit documentation](https://docs.python.org/3.12/library/timeit.html).

## 4. Run a bounded, fair comparison

Choose a short execution budget and sample design before observing an advantage. Use a fixed bounded design or document any calibration separately, including its results. A sample that batches many calls estimates average time per call within that batch; those calls are not independent latency samples.

- Interleave or balance variant order where practical; retain the actual sequence and whether assignment was randomized or deterministic
- Apply equivalent warmup and correctness preparation, with no hidden persistent candidate cache
- Rebuild per-call structures inside the timer unless an explicitly defined reuse contract justifies separate setup plus reuse measurements
- Keep the same workload, interpreter/build settings, loop count and boundary for a matched comparison, or explain a necessary difference
- Verify outputs around the timed work and check for input mutation or unstable results. Include checks in the timed boundary only when they are part of the requested operation
- Record runtime, OS/architecture, relevant hardware, clock/GC settings and known contention. Do not call a shared or virtualized host isolated; unknown host activity stays unknown
- Preserve slow samples, exceptions, invalid outputs, incomplete attempts and retries. Do not rerun until a favorable result appears or discard outliers because they weaken the headline

Bound loops and input size. Stop on the agreed resource/time limit, runaway behavior, unexpected external effects, changing inputs, failed correctness, or environment instability that defeats comparison. A budget checked between batches cannot preempt a hung operation; use an appropriate process timeout for unknown code when already authorized. Return partial evidence and a named gap instead of silently enlarging the experiment.

## 5. Compute only supported comparisons

For each workload and boundary, preserve raw elapsed values, units, batch loop counts, order, output identities and correctness dispositions. Show sample count and descriptive distributions such as minimum, median and observed range. Derive per-call values from elapsed batch time divided by completed calls. Label the statistic: the median of batch averages is not a median of individually timed calls.

For matched blocks, a useful descriptive comparison is `baseline_ns_per_call / candidate_ns_per_call`; above one means the baseline took longer in that block. Also report absolute differences when they help the decision. Keep paired ratios separate from a ratio of medians. A zero or invalid denominator makes the ratio unavailable.

An observed range is not a confidence interval. Repeated samples in one warm process do not establish independent-machine replication, statistical significance, stable tail behavior or causality under production load. With a small noisy result, say “inconclusive at this scope” rather than manufacture confidence or apply a portable fixed threshold. Do not pool small and large workloads into a single speedup without a justified, stated workload weighting.

Reject incorrect controls before ranking speed. Do not convert a runtime ratio into employee time saved, assistant effectiveness, cost savings, product-wide performance or a production capacity estimate. More memory, extra setup, slower small inputs or changed error behavior may make an otherwise faster algorithm unsuitable; show what was and was not measured.

## 6. Deliver the implementation and evidence, then read it back

Return a concise decision with supporting files:

1. **Exact candidate and correctness:** implementation/artifact identity, contract, executed gates, accepted/rejected/unverified status, and the measured negative control's failure witness
2. **Bounded runtime result:** workload, endpoint, state, sample counts and raw-derived distributions; any setup cost and tradeoff affecting the decision
3. **Reproduction:** source/input/configuration identities, commands, actual environment and dependency information, raw samples and failed-attempt dispositions
4. **Limits and next decision:** what the evidence cannot establish, whether the user's threshold was met if supplied, and the smallest additional evidence needed if inconclusive
5. **Execution record:** separate checks actually executed from code or documentation only reviewed; name blocked or omitted checks

Read the saved artifact back. Recompute headline statistics and counts from raw samples, verify source/input/output hashes and relative links, and confirm that rejected controls and failed attempts remain visible. Check behavior and data integrity, not just whether report prose contains expected words. A relocated copy should still identify its inputs without private filesystem paths.

Stop when the requested local change or verification, correctness gates, bounded measurement, evidence readback and supported decision are complete. Do not keep benchmarking merely to narrow an unrequested uncertainty. Deploying, publishing, changing production settings, installing tools, expanding data access or starting ongoing monitoring is outside this result unless separately authorized.

## Runnable worked example

[EXAMPLE.md](EXAMPLE.md) explains the fictional observation summary, actual measurements and scope limits. [VERIFICATION.md](VERIFICATION.md) records execution and readback, including an initial harness serialization failure. Read these when adapting or checking the example.

- [example/contract.json](example/contract.json): independently authored semantics and explicit expected outputs
- [example/summary.py](example/summary.py): baseline, aggregate candidate and wrong last-record control
- [example/workloads.json](example/workloads.json): preserved tiny and batch inputs
- [example/verify.py](example/verify.py): standard-library correctness checks, bounded timing and evidence readback
- [evidence/run.json](evidence/run.json): measured samples, environment, identities and derived results

From this skill directory, use an existing Python 3.12 interpreter:

```sh
python3 -B example/verify.py --readback evidence/run.json
python3 -B example/verify.py --out evidence/new-run.json
```

The first command checks the saved measurement without rebenchmarking. The second runs a new brief offline attempt and refuses to overwrite an existing evidence file. Timings will vary; there is no required speed benefit or fixed performance pass threshold. Do not copy the recorded numbers into a new run.
