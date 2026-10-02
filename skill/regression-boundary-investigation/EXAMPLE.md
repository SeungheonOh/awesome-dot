# Worked example: room-slot regression boundaries

The completed investigation uses only an original synthetic Python function and local Git histories. It does not examine any real project, remote service, account or production environment. No installation, network dependency or binary bundle is needed; the scripts regenerate the committed history from text.

## Request and contract

> Find the revision that changed whether touching room bookings count as conflicts in each bounded fixture history. Use installed Git and Python, preserve the original checkout including its unfinished merge, and keep all experiments in separate local clones. Return the observed boundaries and a checked explanation. Do not repair or commit anything in the original.

Bookings and queries use integer half-open intervals: `[start,end)`. Existing booking `[10,20)` permits a new booking `[20,25)` because the old booking has ended. A query with zero or negative duration raises `ValueError`. Both compatibility modes in the experiment must obey that same interval rule.

The target property is the overlap calculation, not historical API naming. One revision renames the entrypoint during a migration. The fixed external adapter cannot exercise that revision and records it as unavailable. If the requested property were continued availability of the original API, that same rename would be a failure, not a skip.

The [external predicate](scripts/predicate.py) evaluates ten cases: touching before/after, filling an exact gap, left/right overlap, containment, identical intervals, empty bookings, touching across zero, and a zero-duration query. It uses a predeclared `standard, legacy, standard` environment matrix. A good/bad label requires consistent outcomes across that matrix. This is an explicit conservative policy for the fixture, not a statistical claim that three runs establish stability.

## The actual histories

All identifiers below refer to the generated local history. [history.json](artifacts/history.json) carries full IDs for every revision; [commit-graph.txt](artifacts/commit-graph.txt) shows their relationships. Fixed commit dates and the generic fixture author make reconstruction reproducible; the [summary](artifacts/summary.json) records the real verification time.

| History | Declared local interval | Observed result |
|---|---|---|
| Monotonic | M0 through M5 | M3 is the verified good-to-bad boundary |
| Skipped interval | M0 through S6 | S3, S4 or S5 remains unresolved by the predicate |
| Reintroduced regression | M0 through N8 | Bisection returns N7, but the complete ordered audit finds an earlier bad revision N1 |

The branches share original room-slot code but contain distinct functional histories. They are not copied logs with labels substituted.

## 1. A unique boundary and a controlled explanation

The monotonic history adds documentation, sorts bookings without changing results, changes the two contact comparisons, then adds further notes. Both endpoints were evaluated before bisection. The actual [bisect log](artifacts/monotonic-bisect.log) and [command output](artifacts/monotonic-bisect.txt) identify:

- Good predecessor M2: `9b5f41ce67e46c2773ccb96084f9831315cbfcf9`
- Failing candidate M3: `5394db61bf56f39fde8de6623e89d40b947ab4c5`
- Failing successor M4: `af6fe1dd3a9d931a381e6745ee61bc622985ec70`

All three neighbors were independently checked again after bisection with the same ten-case matrix. M2 passed; M3 and M4 failed the four cases involving touching endpoints. The overlap, containment, identical-interval, empty-bookings and invalid-query checks continued to behave as expected.

M3 changes strict overlap checks to inclusive contact checks:

```python
# M2: touching endpoints do not overlap
start < booked_end and booked_start < end

# M3: touching endpoints now count as conflicts
start <= booked_end and booked_start <= end
```

Two controlled experiments strengthen this local explanation:

1. In a fresh clone at M3, change only those comparisons back to strict comparisons. All cases pass across the declared matrix. Restore the original M3 source bytes; the four touching cases fail again
2. In another fresh clone at M2, introduce only the inclusive comparisons. The same four cases fail across the matrix

The [explanation diff](artifacts/explanation.patch) records the one-line relation change. It is evidence from the diagnostic copy, not a proposed commit in the original. Each check record includes both HEAD and the actual source SHA-256, so the modified control is not mistaken for an unmodified commit.

The supported conclusion is that this relation change causes the observed endpoint behavior in the original fixture under the tested inputs and modes. It is not evidence about real bookings, all potential input types, CI, deployment, or why someone chose the change.

## 2. Skipped and variable outcomes leave a real gap

The second history diverges after M2:

| Revision | Observed evaluation | Predicate decision |
|---|---|---|
| M2 | Pass, pass, pass | Good, `0` |
| S3 | Named API absent in all three attempts | Unavailable adapter, `125` |
| S4 | Pass in standard, fail in legacy, pass in standard | Variable across the declared matrix, `125` |
| S5 | Fail, fail, fail | Bad, `1` |
| S6 | Fail, fail, fail | Bad, `1` |

S4 deliberately makes contact behavior depend on `BOOKING_POLICY`. It is deterministic for a fixed mode. The observed pass/fail/pass is environment sensitivity, not evidence of randomness or of identical-condition flakiness. The conservative matrix classifier refuses to erase the contradictory attempts by taking a majority. In a real task, one might instead establish the actual production mode and run a separately named predicate; silently changing the policy midway would invalidate the search record.

Git actually encounters both skipped revisions and concludes that the first bad commit could be any of:

- S3: `efd58170ab13fb2bc10078c4450d1f1c68c97684`
- S4: `a501011017630f23e7ae8225af693aad62af25cd`
- S5: `37463128c968789a79c0a2468368153aaea87298`

The [output](artifacts/gap-bisect.txt) ends with an unresolved skipped set; the outer `git bisect run` exits `2` in the installed Git. Its retained bad ref points to S5, which does not make S5 the uniquely established introduction. A manual post-search audit reevaluates M2 and all four following revisions and preserves the same uncertainty. Resolving it would require an explicitly justified historical adapter and/or a different, well-defined environment question.

## 3. A “first bad” answer can miss an earlier episode

The third branch deliberately contains an initial regression, a repair, several passing documentation revisions, and a later reintroduction. Bisection between verified M0 and N8 tests passing N4 and N6, then failing N7, and prints N7 as the first bad commit:

`68ee9d12f02a66b24cd764a3975f9c86dfc77ebd`

The complete, bounded ordered audit then evaluates all nine revisions:

```text
M0   N1    N2   N3   N4   N5   N6   N7    N8
good bad   good good good good good bad   bad
```

That audit changes the conclusion. N7 is a verified later recurrence boundary; the earliest observed failing revision in this fully audited linear interval is N1:

`bfcc568d238c7513eca21d8f90d49b8e35a3a785`

The audit also brackets the repair at N2. The [search output](artifacts/returning-bisect.txt), [search log](artifacts/returning-bisect.log), and [ordered audit](artifacts/history.json) retain both the initially returned candidate and the evidence that narrows its meaning. A green midpoint excluded an earlier bad episode from the remaining binary search. The phrase “first bad” in tool output does not overcome that non-monotonic history.

## Original work remained intact

Before any investigation clone was made, the original fixture contained a genuine unresolved merge between two planning-note branches, with merge conflict stages and `MERGE_HEAD`. It also held:

- A staged change to `draft.txt`, followed by a further unstaged continuation in that same file
- An unstaged `scratchpad.txt` change
- Untracked `ideas.txt`
- Ignored `scratch.cache`

The [before](artifacts/original-before.json) and [after](artifacts/original-after.json) records match exactly: HEAD, branch, status, staged and unstaged diff digests, and hashes/modes for all 91 files, including the fixture's `.git` files and operation metadata. The unresolved merge remained in progress. This stronger byte-and-mode claim is confined to this small generated repository, which has no submodules, symlinks, linked worktrees or concurrent writers.

All searches and controls ran in independent local `--no-hardlinks` clones. Source configuration was generated and inspected, hooks and templates were empty, and no external remotes or repository scripts were invoked. Each completed search saved its log, used `git bisect reset` in that clone, and verified return to its pre-search HEAD. No stash, clean, destructive reset, force push or cleanup of original work occurred. The generator intentionally leaves its new directory available for inspection.

## Executed checks and evidence

The recorded run used Git 2.52.0 and Python 3.12.14. It completed 36 predicate invocations and 108 child attempts: 52 good, 50 bad and 6 unavailable. The 102 evaluated attempts each ran ten functional cases; unavailable attempts never reached the assertions. Invocation totals are 16 good, 16 bad, 2 unavailable skips and 2 variable-matrix skips. These counts include endpoint checks, actual midpoint searches, neighbor audits, the complete returning-history scan and causal controls.

- [summary.json](artifacts/summary.json): installed versions, actual verification time, input script hashes, search results and preservation status
- [checks.jsonl](artifacts/checks.jsonl): every actual attempt, case failure, revision, source digest and classification
- [commands.json](artifacts/commands.json): performed argument lists, portable working directories and exit codes; `<fixture>`, `<skill>` and `<python>` are documented path substitutions, not literal execution paths
- [sha256.json](artifacts/sha256.json): hashes of the generated evidence files
- [SOURCES.md](SOURCES.md): current official documentation used for tool semantics

The separate [independent review](REVIEW.md) reran the fixture, checked 68,061 cases with a set-based interval oracle, and exercised 13 good/bad/skip/error CLI scenarios. The oracle found no discrepancies at M2 or after the controlled repair, and 966 expected false-unavailable results at M3. Its finite domain and other limitations are recorded with the [review evidence](artifacts/independent-review.json).

Git's own output includes only a generic synthetic author, never a real account identity. All supplied evidence uses portable paths. No binary history artifact is shipped.

## Reproduce only the original fixture

Read both [rehearse.py](scripts/rehearse.py) and [predicate.py](scripts/predicate.py) before running. From this skill directory, select a new directory whose parent already exists:

```sh
python3 -I -B scripts/rehearse.py /tmp/room-slot-boundary-new
```

The command refuses an existing destination. It creates the original repository, its histories and dirty/in-progress state, independent diagnostic clones, and `artifacts/` under that new directory. It does not accept an existing repository as input, download code, install packages, or clean up anything. The interpreter isolation flags reduce incidental Python environment influence; they are not a sandbox for untrusted source. Inspect a fresh output's evidence rather than assuming a rerun passed because this recorded run did.

Commit IDs are reproducible with the controlled fixture history. Runtime versions, verification times, some state hashes and Git's search presentation can differ on another system. The semantic assertions determine success. If a later Git implementation chooses a different midpoint in the non-monotonic case, the explicit expected-N7 assertion may fail; inspect the retained history and outputs and report the changed search behavior rather than changing the evidence to force a pass.

The broader workflow is reusable, but these scripts are deliberately a small example rather than a runner for arbitrary repositories. A real investigation still needs its own permitted inputs, inspected historical commands, relevant dependencies, graph choice, predicate, preservation scope and stopping condition.
