# MergeWorkspace repair

The repaired module retains dirty text and pending reviews through saves and
renames, blocks edits and further receives during a pending review, and resolves
against the reviewed incoming revision. Merging uses the prescribed
`SequenceMatcher(autojunk=False)` line opcodes, including exact insertion-boundary
conflicts, identical-hunk deduplication, and preservation of line endings.

Persistence validates complete schema-1 checkpoints, rejects duplicate JSON
fields and document names, derives dirty status, and enforces text/document/byte
limits. Loads are bounded and do not follow a final symlink. Saves reject
nonregular destinations and atomically replace from an owned-root temporary
file without changing live review state.

## Checks actually run

All commands used this packet as their working directory, set `TMPDIR` to its
`tmp/` directory, and disabled Python bytecode writes. Module and test sources
were inspected before execution. All disposable fixtures were under `tmp/`.

- `python inputs/smoke_test.py`: passed
- `python tmp/check_contract.py`: 10,286 assertions/checks passed, including
  manually specified merges, 10,000 deterministic differential merge cases,
  detached views, conflict blocking/resolution, rename/remove/collisions,
  multiple-document reload, subsequent operations, corrupt snapshots,
  symlink/FIFO/directory rejection, size limits, and injected save failures
- `python tmp/check_boundaries.py`: passed exact 2,097,152-byte save/reload,
  one-byte-oversize rejection without state/checkpoint changes, and Unicode
  roundtrips, including Python surrogate-containing strings

## Scope and verification limits

The code uses the local POSIX runtime's directory descriptors and `O_NOFOLLOW`.
It does not provide simultaneous-writer coordination, protection against
adversarial directory replacement, or power-loss durability; those are outside
the task's contract. JSON Unicode handling follows Python's bytes decoder,
including its surrogate handling. Merge compatibility is textual, not a claim
about the meaning or correctness of the resulting prose. The required matcher
can be expensive on highly repetitive inputs; no worst-case runtime guarantee
was established. No hidden evaluator or external-system tests were run.
