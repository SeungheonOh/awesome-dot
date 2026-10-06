# MergeWorkspace repair

The repaired module preserves merge bases and pending conflicts across saves,
renames, and reloads. It uses the specified line hunks and conservative insertion
boundary rule, blocks edits/receives during pending review, derives dirty state,
and returns detached views. Resolution advances the base to the reviewed incoming
version. Failed validation and oversized merged results leave live state unchanged.

Snapshot loading validates the complete schema, duplicate names/object fields,
conflict consistency, and all limits. It reads at most 2,097,153 bytes from a regular
file opened without following its final symlink. Saving checks the encoded byte
limit incrementally, writes a same-directory temporary file, and replaces the
checkpoint atomically without modifying live documents. Failed writes/replacement
clean up the temporary file.

## Checks actually run

All passed after reviewing the submitted source and each test's effects:

- Supplied `inputs/smoke_test.py`
- 22 local contract tests covering editing/views, merge cases and line endings,
  conflict retention and blocking, resolutions, rename/remove, all stated limits,
  multi-document save/reload and later merges, replacement/fdopen failures,
  malformed snapshots, symlink/directory/FIFO rejection, and Unicode round trips
- 18,225 constructed single-hunk cases with coordinate-derived expected results
- 10,000 deterministic randomized multi-hunk cases compared with a simple
  pairwise-conflict/reverse-splice reference using the prescribed opcodes
- An exactly 2,097,152-byte save/reload and a 2,097,153-byte rejected save,
  checking that the previous checkpoint and live state remain unchanged

All fixtures and check scripts were confined to this packet's `tmp/`, with
`TMPDIR` set there and Python bytecode generation disabled.

## Verification limits

These are local checks, not a run of the separate evaluator. POSIX directory
file descriptors and no-follow flags were tested in the supplied environment;
other operating systems were not tested. `SequenceMatcher(autojunk=False)` can
have quadratic worst-case runtime. Concurrent writers, adversarial directory
replacement, and power-loss durability are outside the requested contract.

For strings containing raw surrogate code points, snapshot encoding mirrors
Python's JSON byte-decoding surrogate-pass behavior so Python strings round-trip
without normalization; stricter non-Python UTF-8 consumers may reject those
unusual snapshots. Ordinary Unicode is encoded as UTF-8.
