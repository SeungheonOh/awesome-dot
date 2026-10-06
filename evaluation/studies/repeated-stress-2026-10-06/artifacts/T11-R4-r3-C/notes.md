# MergeWorkspace repair

Implemented detached views, derived dirty state, explicit pending-review guards,
all resolution choices, state-preserving renames, and the specified line-hunk
three-way merge. Rejected mutations validate before changing documents.

Checkpoint loading validates the complete schema and all documents, rejects
nonregular files and final symlinks, and bounds reads to the stated byte limit.
Saving bounds serialization, writes a temporary file inside the owned root, and
atomically replaces the checkpoint without changing live state. Failed replacement
removes the temporary file and preserves the previous checkpoint.

## Checks actually run

- Supplied `inputs/smoke_test.py`: passed
- Local `tmp/check_contract.py`: 17 tests passed, including 1,568 constructed
  edit-pair scenarios, newline preservation, conflict retention and resolution,
  detached views, rejected-operation atomicity, rename/remove behavior,
  multi-document save/reload and subsequent merges, forced replacement failure,
  exact load-byte boundaries, text/document limits, corrupt snapshots, symlinks,
  directory/FIFO destinations, and large Unicode text

All disposable fixtures were created beneath this packet's `tmp/`. No external
sources, accounts, network, or evaluator were used.

## Limits

This implementation uses the POSIX directory/no-follow facilities already used by
the supplied scaffold. Concurrent writers, adversarial directory replacement,
and crash/power-loss durability beyond atomic replacement remain outside the
stated contract. Standard JSON Unicode decoding applies: a Python string made
from an adjacent literal high/low surrogate pair can normalize to one Unicode
character after reload; ordinary Unicode and isolated surrogates were tested.
Independent evaluator results are not available.
