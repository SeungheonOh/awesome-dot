# Independent fixture review

**Result:** The reviewed rehearsal and predicate behaved as declared for the original synthetic room-slot history. No blocking defect was found within that scope. The staged scripts were not modified.

## Evidence

The scripts were inspected before execution. One new temporary fixture directory was generated, and every additional execution or controlled edit stayed within that fixture. No external code, installation, credentials, network operation, real project, or remote service was used.

- Rehearsal: **36 predicate invocations**, **108 attempts**, **102 evaluated attempts**, and **1,020 case evaluations**. Six attempts were unavailable because the named API was absent.
- Monotonic history: M2 passed, M3 failed, and the search uniquely identified M3. M4 also failed.
- Skipped history: the unresolved boundary remained **S3 / S4 / S5**. The review did not treat the current bad reference as a unique culprit.
- Returning history: bisection found N7, while the ordered audit showed the earlier failure at N1 and recovery at N2. This correctly demonstrates the limit of using a monotonic search on returning behavior.

## Independent interval oracle

The independent oracle represented each integer half-open interval as a set of unit cells and compared the query set with the union of occupied cells. It did not reuse the implementation's pairwise inequality expression.

The exhaustive domain used coordinates **−3 through 3**, all **21 positive-length intervals**, all **463 ordered booking lists of length 0–2**, and all **28 zero/negative-length queries**. Duplicate bookings, overlapping bookings, negative coordinates, and both booking orders were included.

| Variant | Valid-query checks | Invalid-query checks | Mismatches |
|---|---:|---:|---:|
| M2 | 9,723 | 12,964 | 0 |
| M3 | 9,723 | 12,964 | 966 |
| M3 with the overlap comparisons repaired | 9,723 | 12,964 | 0 |

That is **68,061 checks**. All 966 M3 discrepancies were false-unavailable decisions; no false-available result or invalid-query acceptance occurred. The controlled comparison repair produced the same source bytes as M2. Its zero-mismatch result independently supports the proposed explanation within the tested domain.

## Predicate exits and environment sensitivity

All **85 combinations** of zero through three outcomes drawn from good, bad, unavailable, and abort returned the expected classifier result:

- **0**: consistently good
- **1**: consistently bad
- **125**: API unavailable, or mixed good/bad matrix outcomes
- **128**: infrastructure failure, abort outcome, or no outcomes

All **13 CLI scenarios** behaved as expected: good, bad, missing API, policy-sensitive behavior, import exception, syntax error, child exit 126, child terminated by a signal, non-JSON output, timeout, missing source, record path pointing to a directory, and execution outside a repository. Child errors were not misclassified as ordinary bad commits.

S4 was good in standard mode, bad in legacy mode, and good when standard mode was repeated. **This is controlled environment sensitivity, not evidence of random flakiness.** The literal classification `skip-unstable-matrix` should be explained that way in surrounding prose; its name alone does not establish stochastic behavior.

## Original work preservation

The rehearsal's before/after snapshots were identical. A second review check still matched the hashes and modes of all **91 files, including Git metadata**, and matched Git status. The interrupted merge remained in progress. The staged/unstaged draft, unstaged scratchpad, untracked idea, ignored cache, and merge-conflict state remained represented as:

```text
MM draft.txt
UU merge-note.txt
 M scratchpad.txt
?? ideas.txt
!! scratch.cache
```

The review also restored its controlled copy's source bytes after the CLI probes. All three searches recorded evidence before `git bisect reset` and restored their starting bad endpoint in the independent clones.

## Additional independent readback

A second review regenerated the original histories in a fresh local fixture and reproduced the saved predicate, command, history, bisection and explanation-patch evidence. It confirmed all 91 original files and modes, the unfinished merge, and refusal of an existing output directory without changes. A different finite integer grid with up to three bookings matched the good predecessor and detected the same contact-regression pattern. Separate guide-only cases kept API availability, first-parent merge interpretation and a missing compiler distinct; they did not execute another repository investigation.

## Limits

The original exhaustive oracle used at most two positive-length bookings; the additional nonuniform-grid review used at most three. Both checks cover finite integer domains. It does not establish behavior for noninteger coordinates, malformed bookings, unusual Python objects, or arbitrary repositories. Snapshot equality covers recorded file bytes, regular-file modes, HEAD, branch, Git status, and staged/unstaged diffs; it is not a timestamp/directory-metadata audit or a general backup guarantee. Isolated Python mode, empty hooks, and empty templates reduce ambient interference but do not form a security sandbox. No production workflow or real external execution was validated.

## Reproduction and artifact identity

Run `python3 scripts/rehearse.py NEW_DIRECTORY` with a nonexistent directory after inspecting both scripts. The independent oracle uses the exact finite domain and set-intersection definition above; CLI fault probes belong only in a generated disposable copy.

Exact counts, small mismatch examples, the 85-case classifier truth table, the CLI outcomes, preservation evidence, and the reviewed input hashes are recorded in [artifacts/independent-review.json](artifacts/independent-review.json).

Reviewed script SHA-256 values:

- `predicate.py`: 282ad50e90bd291798114e0028a7ede5c23819c3309d844289dcc5e4bfe48440
- `rehearse.py`: 708c848b96441f018e2136b53004130ec5649509bc2177f2a2a31ed18c9ae496
