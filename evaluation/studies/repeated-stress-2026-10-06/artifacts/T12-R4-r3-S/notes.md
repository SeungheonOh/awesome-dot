# MergeWorkspace repair

`merge_workspace.py` retains the public API and implements base-relative,
line-preserving merges, detached document views, protected pending reviews,
explicit resolution, full-state rename, and checkpoint-only saving.

Persistence validates the complete schema and document/conflict invariants.
Duplicate JSON keys and document names are rejected. Reads are bounded and
no-follow; saves reject nonregular destinations, incrementally enforce the
byte limit, and atomically replace from a same-root temporary file. Failed
replacement leaves the checkpoint and all live document state unchanged and
removes the temporary file.

## Checks actually run

- Supplied `inputs/smoke_test.py`: passed
- Additional standard-library test harness in `tmp/check_workspace.py`:
  14 test groups passed, covering API validation and detached views, merge
  fast paths, manually specified merge cases and line endings, pending-review
  protections, all resolutions, rename/remove, multi-document checkpointing,
  subsequent merges after reload, failed-save atomicity, corrupt snapshots,
  exact read-byte boundary, oversized saves/merges, and symlink/directory/FIFO
  rejection
- Merge sweep compared against a pairwise conflict/reverse-application oracle
  for 3,375 exhaustive short repeated-line triples and 3,000 seeded mixed-line
  triples; all agreed

All test fixtures were disposable directories beneath this packet's `tmp/`.
No external services, packages, processes launched by the module, or account
state are used.

## Limits

The specified 100-document, 100,000-character-per-text and 2,097,152-byte
snapshot limits are enforced. The POSIX no-follow/directory-descriptor APIs
match the supplied runtime. Single-process owned roots are assumed; concurrent
writers, adversarial directory replacement, and power-loss durability are
outside the contract. Worst-case repetitive-line SequenceMatcher runtime has
not been benchmarked. No functional failure was observed in the checks run.
