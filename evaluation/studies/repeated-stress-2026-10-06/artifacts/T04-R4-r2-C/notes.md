# Repair summary

`merge_workspace.py` now keeps dirty state derived from the current merge base,
returns detached views, preserves pending reviews through renames/checkpoints,
blocks edits and additional incoming updates during review, and resolves against
the reviewed incoming version. Merging uses the specified line-level
`SequenceMatcher(autojunk=False)` hunks, including insertion boundary conflicts.

Checkpoint reads are bounded and reject nonregular files, final symlinks,
incorrect schemas, duplicate JSON fields/names, invalid documents, and
inconsistent conflicts. Saves use a bounded serialization and a same-root
temporary file followed by atomic replacement; save never updates live documents.

## Checks actually run

- The supplied `inputs/smoke_test.py`: passed
- A packet-local, standard-library unittest suite: 15 test groups passed
- The suite includes 150 deterministic constructed disjoint-edit scenarios,
  fixed merge/conflict examples, mixed line endings and missing final newlines,
  detached views, every resolution choice, invalid-operation atomicity,
  renaming/removal, and multi-document round trips
- Persistence checks cover injected replacement and partial-write failures,
  temporary-file cleanup, duplicate/malformed snapshots, document/text limits,
  exact 2,097,152-byte load/save acceptance and one-byte-over rejection,
  regular/dangling symlinks, directories, FIFOs, and a changed root symlink

All test fixtures were created beneath this packet's `tmp/` and cleaned up.

## Verification limits

The implementation uses the POSIX no-follow/directory-descriptor facilities of
the supplied scaffold; other operating systems were not tested. Local checks
are not an exhaustive proof of all filesystem failure modes or worst-case
`SequenceMatcher` performance. Simultaneous writers, adversarial directory
replacement races, and crash/power-loss durability beyond atomic replacement
remain outside the stated contract. No live or external systems were used.
