---
name: regression-boundary-investigation
description: "Locate and assess a behavioral regression boundary in bounded local Git history using a verified good/bad predicate, isolated execution, explicit skipped or unstable outcomes, and candidate-neighbor checks."
---

# Locate a Regression Boundary Without Overclaiming Its Cause

Turn a reproducible change in behavior into an evidence-backed boundary or an honest unresolved candidate interval. Execute the authorized local investigation, retain the search evidence, and explain what the result establishes about the named behavior. A commit selected by a search is a starting point for explanation, not proof that every line it changed caused the failure.

Use when the question is “which revision changed this behavior?” and a bounded history is available. The result is a checked historical boundary, not necessarily a repair. For repairing a failure already located, use [failing-build-repair](../failing-build-repair/SKILL.md); for investigating variability itself, use [flaky-test-investigation](../flaky-test-investigation/SKILL.md); for combining accepted changes, use [parallel-change-integration](../parallel-change-integration/SKILL.md). None of those outcomes is a prerequisite for this investigation.

## Establish the question and permitted experiment

Resolve these inputs from the request and accessible project instructions before running historical code:

- The behavior that regressed, the expected contract and concrete reproducing input, and the observable assertion that distinguishes it
- The authorized local repository and isolation/output location; immutable known-good and known-bad revisions or a bounded set of candidate endpoints
- Which history matters: one ancestry chain, a first-parent integration sequence, or the full reachable graph
- The installed runtime and dependencies, test entrypoint, allowed side effects, relevant fixture/configuration versions, and practical revision/run/time budget
- The requested outcome: locate the boundary, explain the change, or additionally implement a repair; ask only for missing facts or authority that affect the next step

Do not infer that a report of an older passing CI run is a reproducible good endpoint today. Pair its observation with its environment and test version, then verify the endpoint under the chosen current experiment. If both endpoints pass, both fail, or the environment is materially different, resolve that discrepancy before bisection. A changed requirement or changed test can explain the contrast without a product regression.

A request to investigate this local history covers necessary local inspection, separate diagnostic copies and understood offline checks. It does not authorize remote jobs, installs, contacting services, manipulating accounts, production activity, rewriting history, or pushing. Inspect source and invoked scripts before execution. Do not reproduce a security vulnerability under this workflow.

## Preserve original work and freeze the inputs

1. Read repository instructions. Record HEAD and branch; staged and unstaged state separately; untracked files; relevant ignored state; and any merge, rebase, cherry-pick, revert or existing bisect operation. Protect concurrent work as well as already dirty work.
2. Choose a preservation check that supports the promised claim. Record relevant file hashes and modes, index bytes or index entries, staged and unstaged diff digests, and operation metadata. Use read-only Git options such as `--no-optional-locks` when inspecting the original; status can otherwise refresh the index. Do not publish private file contents, personal paths or credential-bearing configuration in the report.
3. Resolve endpoint names once to full object IDs, verify they exist, and establish their ancestry and reachable range. Identify shallow history, missing objects, submodules, filters, hooks, alternate object stores and dependencies that could prevent a faithful checkout. A path-limited history may omit an important configuration or dependency change; do not restrict paths merely because the symptom appears in one file.
4. Work in an inspected, independent local clone or another expressly permitted isolation mechanism. A local clone with `--no-hardlinks` copies object files; it does not incorporate dirty work. A linked worktree has separate working files and index but shares repository state and refs. Explain that distinction before promising original-repository preservation. Check the new destination is unused and verify the checked-out ID.
5. Keep the external predicate and evidence outside the checkout that Git will move. Use separate output/cache directories per revision or an understood safe isolation scheme, so generated files cannot change classifications or prevent checkout.

Do not stash, switch branches, resolve an existing operation, clean, or reset the original checkout to make the investigation easier. Do not auto-initialize submodules, run filters/hooks, or copy unknown configuration. If safe isolation is unavailable, stop execution and report the concrete blocker while continuing useful read-only analysis. Never “repair” the original merely to satisfy preservation verification.

## Make the predicate trustworthy before searching

Write down the fixed question in executable terms. For example, “with occupied interval [10,20), availability for [20,25) must be true.” The test must reach the relevant product behavior; a successful import or a green unrelated suite is insufficient.

Use the same external test logic, input fixture and intended environment contract across revisions. If an older revision needs an adapter or temporary compatibility change, inspect and identify it explicitly. Establish that the adapter does not implement the answer being tested. Record its digest and affected revisions. If that cannot be justified, leave those revisions untestable rather than silently changing the predicate.

Define the outcomes before seeing midpoint results:

| Predicate outcome | Treatment in this workflow |
|---|---|
| Target behavior evaluated and satisfied | `0`, good |
| Target behavior evaluated and contradicted | `1`, bad; retain the expected and actual result |
| Known unrelated prerequisite or unsupported historical adapter prevents evaluation | `125`, skipped, with the specific reason |
| Repeated outcomes contradict one another under the declared experiment | Record every attempt; pause to stabilize the experiment, or explicitly skip that revision with `125` and retain the ambiguity |
| Harness fault, unexpected exception, missing executable, signal, cancellation, timeout or a new unsafe side effect | Abort; do not automatically call the product bad |

For `git bisect run`, Git accepts `0` as good, `1` through `127` except `125` as bad, and `125` as skip. Other exit statuses abort. In particular, shell `126`/`127` errors can look like bad revisions. Use an explicit wrapper that maps only a demonstrated target assertion failure to `1` and an infrastructure fault to an abort such as `128`. A Python child terminated by a POSIX signal has a negative `returncode`; do not blindly forward it. These semantics and the relevant isolation details are linked in [SOURCES.md](SOURCES.md).

Skipping is a loss of information, not a way to obtain a cleaner result. An API deletion is bad if API availability is part of the target contract; it may be an adapter limitation only when the investigation explicitly concerns another behavior and cannot test that behavior through the historical API. Likewise, a build failure is the answer if buildability is the selected predicate, not an automatic skip.

Run both endpoints with the exact wrapper. When variability is plausible, predeclare a small repetition or seed/configuration matrix and retain all attempts, including failures after passes. A majority vote or “retry until green” produces an unreliable binary label. If the fixed run budget cannot discriminate the states, report that limitation or route the variability investigation separately.

## Choose a search that matches the history

Check the assumption that the selected property changes from good to bad once along the history being searched. Look for reverts, fixes followed by reintroductions, toggled feature flags, test migrations and dependency/environment discontinuities. A few passing samples do not prove monotonicity.

- **Plausibly monotonic bounded history:** use bisection, then verify its candidate and neighbors
- **Known or suspected bad→good→bad history:** split into justified intervals or perform an ordered scan within a finite budget; report each observed transition. A binary search alone cannot establish the earliest historical failure
- **Small history:** an ordered scan may be simpler and provide stronger coverage than a binary search
- **Merge graph:** define whether the question concerns first appearance on an integration line or introduction anywhere in ancestry. A first-parent search can identify a merge as the integration boundary; it does not prove which side-branch commit caused the behavior. Check the relevant parents when feasible

Do not order a DAG by author timestamp and call that a causal sequence. If supplied endpoints are not in the required relationship, inspect the graph and find a justified interval instead of pretending the range is linear.

## Run and retain the investigation

With verified full IDs and the inspected predicate, the core sequence in the isolated checkout is:

```sh
git bisect start BAD_ID GOOD_ID
git bisect run python3 /approved/external/predicate.py
git bisect log > /approved/evidence/bisect.log
```

Substitute the actual permitted paths, wrapper and IDs. Add first-parent behavior only when that answers the specified question and is supported by the installed Git. Never run this sequence in a checkout whose existing bisect belongs to someone else.

For every evaluated revision retain its full ID, tree or relevant source digest, predicate version, inputs/environment, command, exit status, classification and diagnostic. Record skipped/unstable revisions and the entire unresolved set Git reports. The current `refs/bisect/bad` is only a known-bad boundary while skipped candidates remain; it is not automatically a uniquely identified introduction.

Save the bisect log and command output before ending the session. Then use `git bisect reset` only in the diagnostic checkout and verify it returned to that checkout's pre-search HEAD. This is the bisect subcommand, not permission to use destructive `git reset` on original work. An aborted search still needs its partial evidence and a stated reason.

If a result was mislabeled, preserve the original evidence, correct the record, and replay or restart the isolated search under the corrected predicate. Do not silently edit the history of observations. If tooling or inputs change, identify the new experiment separately.

## Verify the boundary and assess the explanation

1. Rerun the candidate, its relevant parent/predecessor and a succeeding revision under the same predicate. If the candidate's parent is untestable, keep the unresolved interval instead of claiming adjacency. For a merge, evaluate the parents relevant to the selected history question.
2. Test the original failing input and nearby functional boundaries that distinguish the proposed mechanism from a coincidental change. Repeat the declared matrix without suppressing contradictory attempts.
3. Read the actual candidate diff and the affected call/data path. State what change would explain the observed contrast and what result would disprove that explanation.
4. When safe local diagnostic edits are in scope, use a fresh disposable copy for a controlled test: isolate/reverse the suspected change at the candidate and introduce it in the predecessor, or use another appropriately targeted control. Preserve the original assertion and environment. Record dirty source digests as well as HEAD, because an edited experiment is not the named commit alone.
5. Calibrate the claim. Neighbor checks establish a behavioral boundary under this predicate. A controlled change can support a local mechanism. Neither automatically establishes the initiating organizational cause, all affected inputs, every platform, or a production fix. If the controlled test contradicts the explanation, continue within the agreed budget or report it unresolved.

Do not turn a diagnostic experiment into an unsolicited repair, commit or published patch. Return the boundary and evidence even when a repair is separately requested; that evidence remains distinct from later repair verification.

## Deliver and stop

Return a concise finding backed by a portable evidence record containing:

- The tested behavior, fixed endpoints, selected graph/range and actual environment
- The exact predicate and classifications, observed commands and search log
- A unique verified boundary, an unresolved candidate set, or the earliest observed transition only within the audited range
- Neighbor results, skip/variability evidence, and the monotonicity assumption or counterexample
- The supported explanation and its controls, clearly separated from unproved cause
- Preservation checks, output locations, work performed, unrun checks and remaining limits

Stop when the authorized boundary investigation and relevant verification are complete, or when a concrete prerequisite, safety/authority limit, persistent instability, exhausted declared budget or unresolved skipped interval prevents a stronger result. A candidate set is a useful completed bounded result when further discrimination is unavailable. State the smallest extra input or decision that would resolve it; do not substitute an invented unique culprit.

## Run the contained example

[EXAMPLE.md](EXAMPLE.md) supplies an original room-slot contract, actual commit histories and observed bisection results. The two inspected Python scripts regenerate everything using only installed Git and Python in a new directory. They preserve a real unresolved merge alongside dirty/untracked/ignored fixture work, verify a unique monotonic boundary, retain an ambiguous skipped interval, and demonstrate a reintroduced regression that changes the interpretation of Git's “first bad” output. All evidence is synthetic and local; no real repository was tested.
