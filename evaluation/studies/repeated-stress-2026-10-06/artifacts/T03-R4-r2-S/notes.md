# MergeWorkspace repair

Implemented in `merge_workspace.py`:

- Detached document/conflict views and derived dirty status
- Exact `splitlines(keepends=True)` / `SequenceMatcher(autojunk=False)` hunk merging, including deduplication, adjacent edits, and conservative insertion boundaries
- Whole-review retention, blocked edits/receives during review, validated resolutions with the incoming revision retained as the new base
- State-preserving rename/remove and full multi-document checkpoints
- Strict snapshot structure/type/limit validation, including duplicate JSON keys and document names
- Bounded regular-file reads with no-follow checks; same-root temporary writes and atomic replacement, with cleanup on failures

## Checks actually run

- Supplied `inputs/smoke_test.py`: passed
- Local `tmp/check_contract.py`: all 13 test groups passed
- Those groups include 13 manually specified merge cases, 3,375 exhaustive small repeated-line triples, and 6,000 deterministic mixed-line-ending triples compared against a separate all-pairs conflict/reference assembly implementation
- Also checked invalid-operation state preservation, every resolution mode, subsequent merges, checkpoint/reload fidelity, injected write/replace failures and temporary-file cleanup, corrupt snapshots, exact/over-limit file reads, over-limit saves and merged text, symlink rejection, directory/FIFO rejection, and document/name/text limits

All fixtures were confined to this packet's `tmp/`. No network, external accounts, subprocesses within the Python component/tests, or third-party packages were used.

## Scope and verification limits

The persistence implementation uses the POSIX no-follow and directory-descriptor APIs available in this runtime. The workspace follows the stated single-process, owned-root contract; it provides neither locking nor stronger crash/power-loss durability. Textual merging does not establish semantic correctness. `SequenceMatcher` retains its standard worst-case quadratic runtime, as required by the specified correspondence rule. The local checks passed; the separate evaluator has not been run here.
