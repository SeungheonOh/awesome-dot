# Worked example: combine reading-queue changes

The requested artifact is a new local `integration/accepted` branch plus a patch and history bundle. The two accepted contributions add independent summary fields. A proposal to change the default order has no acceptance and remains held. All code, decisions, identities and commit history are fictional.

Read the complete [request and contract](fixtures/decisions.md). The initial function returns titles in the caller's reading order. COUNT-1 adds the number of entries; MINUTES-1 adds the total reading minutes. Neither changes ordering. Both branches passed their own relevant tests before integration.

## Immutable inputs and result

| Role | Git commit |
|---|---|
| Common base | `f20646ab6a56bf20eda49e07f74ebcd297d82aec` |
| Accepted COUNT-1 | `95051401442196992e61067cdd905dfdfb495ce2` |
| Accepted MINUTES-1 | `176122e5beb1a6ba2f1d5efe6074f518fb79caed` |
| Held ORDER-2 proposal | `e926c3eed439ccdf5f2ac22ae85867b3eb1bcb50` |
| Later count successor, outside accepted input | `3463535adbd93b9b05f84385f040003074d8aa7f` |
| Final local integration | `9e82fb830d86f350a5cd079936e6b968a949e14e` |
| Final tree | `f616d5f3bfec66a1d08c950199ad521e3fd7694d` |

The first merge retains COUNT-1's history. The second merge has that integration commit and MINUTES-1 as parents. Both accepted commits are ancestors of the final result; ORDER-2 and the later count successor are not. The [actual commit graph](artifacts/commit-graph.txt) records the branches. Commit timestamps are fixed fixture data for reproducibility; verification timestamps in the [ledger](artifacts/verification.json) are actual run times.

## Preserved work

Before creating the contributor and integration copies, the original checkout contained:

- `notes.txt`: one staged version plus a further unstaged paragraph
- `queue_summary.py`: an unstaged local experiment comment
- `ideas.txt`: untracked work
- `scratch.cache`: an ignored file

Independent local clones started from the committed base, so none of those edits entered the integrated artifact. The original [before](artifacts/original-before.json) and [after](artifacts/original-after.json) snapshots match exactly for HEAD, current branch, refs, index bytes, staged and unstaged diff digests, status, and every working-file hash and mode. This check includes the untracked and ignored files. It is not a byte comparison of the entire `.git` directory.

While integration was underway, the count contributor added a documentation commit. The frozen COUNT-1 ID stayed the selected input. That contributor's [before](artifacts/concurrent-before.json) and [after](artifacts/concurrent-after.json) snapshots also match. The later commit remains inspectable in the bundle under `observed/count-successor`, without being part of the integrated history.

## A mechanical conflict actually occurred

COUNT-1 and MINUTES-1 both replaced the original one-line return statement. Git reported one unmerged path, `queue_summary.py`; the [captured conflict](artifacts/mechanical-conflict.txt) contains both sides. The recorded stage-1, stage-2 and stage-3 content digests match the supplied base, count and minutes source files respectively.

The accepted contracts support retaining the title expression and adding both distinct fields. The resolution is the checked-in [combined implementation](fixtures/integrated/queue_summary.py):

```python
def summarize(entries):
    return {
        "titles": [entry["title"] for entry in entries],
        "count": len(entries),
        "total_minutes": sum(entry["minutes"] for entry in entries),
    }
```

No contributor assertion was removed or changed. Two [joint assertions](fixtures/integrated/test_integration.py) add the behavior that neither branch checked alone: all three fields agree for duplicate titles and zero minutes, and repeated calls produce independent outputs without changing the input. The empty result must also contain all three fields with their correct empty values.

## A genuine intent conflict stays held

ORDER-2 proposes alphabetical titles by default. With the same input `Zebra, Apple`, the existing accepted contract requires `Zebra, Apple`, while ORDER-2's assertion requires `Apple, Zebra`. The proposal's local suite ran four tests: its new alphabetical assertion passed, but the existing input-order assertion failed. That [failure remains recorded](artifacts/proposed-order.log).

The proposal was inspected and preserved as a [separate patch](artifacts/held-order-proposal.patch) and bundle ref. It was not merged, and no assertion was weakened. The unresolved question for the queue contract owner is: should the default preserve the reading plan or sort alphabetically? Adding an ordering option would be a third interface choice that also needs a decision.

The requested two-contribution integration is complete locally. ORDER-2 is a separately held proposal, so this result does not claim it was integrated or rejected permanently.

## Checked artifacts

- [integration.bundle](artifacts/integration.bundle) contains the final branch, complete fixture history, immutable input refs, held proposal and observed successor. A fresh clone restored the exact final commit and tree, then passed all 10 tests
- [integration.patch](artifacts/integration.patch) is a tree patch from the recorded base to the final result. It applied cleanly with an index update to a fresh base checkout, produced the identical final tree, and passed all 10 tests. It does not preserve merge history or claim a new commit in that checkout
- [artifact checksums](artifacts/artifact-sha256.json) cover the delivered artifacts, logs and ledger. Inspect bundle refs before choosing what to use; inclusion in the bundle does not mean inclusion in the integration

## Bare local delivery and readback

The request also authorizes one offline delivery simulation to a newly created bare repository, `delivery.git`. Before delivery it contains only `contribution/count`, pointing at the later count successor. The new `integration/accepted` ref is transferred there without a force update. A ref readback reports the exact final integration ID, while the existing contributor ref still points to its later commit.

A fresh clone of that local remote restores the final commit and tree and passes all 10 tests. The [local-remote readback record](artifacts/local-remote-readback.json) lists the before/after refs; the [test log](artifacts/local-remote-readback.log) records the run. This demonstrates a checked transfer to a local directory already named in the fictional request. It does not imply authority to push to a real service or shared repository.

No remote service, network dependency, published branch, remote CI job or release was involved.

## Repeat the local rehearsal

Read [scripts/rehearse.py](scripts/rehearse.py) and the fixture files first. From this example's directory, select a new directory that does not already exist:

```sh
python scripts/rehearse.py /tmp/reading-queue-integration-new
```

The script uses only the installed Git executable and Python standard library. It creates its own original checkout, contributor copies, integration copy, bundle-restoration copy, patch-application copy, bare local remote and readback clone. It never accepts a real repository path as a source. Its Git configuration and empty hook/template location are scoped to the fictional run; it does not change system or user configuration. It runs only the fixture's inspected unit tests.

The script leaves all checkouts and artifacts available for inspection and refuses an existing destination. A normal successful run prints the final commit, the 10-test result and preservation result. An unexpected Git result, changed snapshot, wrong conflict, ancestry mismatch, wrong test count, dirty final checkout or artifact mismatch stops the rehearsal with an error.

The full history, source, tests and state checks make this more than a narrated merge. The [verification page](VERIFICATION.md) records what was actually executed and the remaining limits.
