# Fictional Cleanup: Five Names Do Not Mean Five Independent Allocations

The fictional request was to assess an additional 8,192-byte capacity goal, move only `Downloads/export-copy.csv` to `Review`, read it back, and restore it as a rehearsal. Every other file was to remain untouched and no deletion was authorized. The useful result is a verified move and an honest unmet capacity goal.

## What was actually exercised

The script created a new directory containing five fictional regular-file paths. It ran on Linux with Python 3.12.14 and GNU coreutils 9.7. The available filesystem reported `overlayfs`. All files were newly generated, not selected from a person's Downloads or project folder. Nothing was downloaded, uploaded, trashed, permanently deleted, installed or changed in an application.

The [plan](plan.json) was saved before the volume baseline and move. The [observations](evidence.json) contain per-file identities, content digests, block counts, tool output, timestamps and readbacks. The [manifest](manifest.json) reconciles all five initial paths. Names below are relative to the fictional directory.

| File | Logical bytes | Reported allocated bytes | Observed relationship | Disposition |
| --- | ---: | ---: | --- | --- |
| `Downloads/export-copy.csv` | 8,192 | 8,192 | Separate inode, same bytes as current export | Move to Review and restore |
| `Downloads/export-linked.csv` | 8,192 | 8,192 | Same device/inode as current export; both have link count 2 | Keep |
| `Downloads/scratch-capture.bin` | 65,536 | 4,096 | Sparse file with one byte written at the end | Hold; purpose unresolved |
| `Projects/current-export.csv` | 8,192 | 8,192 | Retained file also named by export-linked | Keep |
| `Projects/keep-notes.txt` | 42 | 4,096 | Small ordinary file with allocation granularity | Keep |

The path-summed logical size is 90,154 bytes. Counting each file inode once gives 81,962 logical bytes and 24,576 reported allocated bytes across four inodes. A naive sum of the allocation column is 32,768 bytes because it counts the linked export twice. None of those totals is automatically reclaimable space.

The sparse file is not 65,536 reclaimable bytes merely because that is its length. The two names sharing one inode do not own separate 8,192-byte payloads. The separate same-byte copy has its own inode, but that alone does not prove exclusive physical storage on every filesystem. This example did not query shared extents, compression or snapshots.

GNU `du` on the exact file list agreed with the unique-inode totals. The tool attributed the hard-linked export to the first name encountered, so `Projects/current-export.csv` did not get another line in that invocation. It was still present and was read independently; omission from that particular `du` listing does not mean deletion. Directory overhead is excluded from this explicit regular-file comparison.

## Executed action and readback

1. The separate copy's current device, inode, size, link count, allocation, modification time and SHA-256 matched its recorded precondition
2. Source and destination parents were on the same filesystem, and the destination name was absent
3. The file was renamed to `Review/export-copy.csv`; its old name was absent and the destination had the same recorded identity and bytes
4. The authorized reversal returned it to its original name, with a second readback
5. A move attempt to the already-existing `Projects/current-export.csv` was rejected before mutation; both files remained unchanged

No record was removed. All five initial paths were present at the end with their original identities, bytes, sizes and modification times. Reads and renames can affect other timestamps; no claim is made that every filesystem metadata field stayed identical.

## Space result

| Measure | Before move | After move | After reversal |
| --- | ---: | ---: | ---: |
| Regular-file allocation, counted once per inode | 24,576 bytes | 24,576 bytes | 24,576 bytes |
| Available bytes from the same filesystem counter | 31,721,205,760 | 31,721,205,760 | 31,721,205,760 |
| Verified payload bytes freed by the move | — | 0 | 0 |

The observed available-space delta was zero in this run. The 8,192-byte additional-capacity goal was not met. Moving the copy to a review folder changed its location, not its payload allocation; returning it verified the recovery route. Moving a file into local Trash on the same filesystem would likewise retain that payload and must not be advertised as freed space.

Those large available-space values describe the containing filesystem, not a private disk allocated to this fixture. Other activity could make them differ on another run. The checker deliberately does not require a zero volume delta; it requires unchanged file accounting and reports whatever the counter actually says. It writes the final evidence files after measurement, so their allocation is not part of the move interval.

The next real-world decision would be a specific, authorized action that actually releases capacity, supported by an understood recovery route and retention needs. This rehearsal supplies no permission to delete the copy or any other data.

## Reproduce safely

Run from this example's folder on Linux with Python 3 and GNU coreutils already available:

```sh
python3 rehearse.py ./rehearsal-output
```

The output directory must not exist; its parent must exist. The script creates only that new directory and its tiny fictional files, retains them and the JSON records, and refuses to reuse an existing directory. It accepts no cleanup target, scans no real collection and deletes nothing. Do not point it at an existing directory or treat its internal rename helper as a general-purpose file mover.

New runs produce their own inodes, timestamps, volume counters and possibly different allocations. Read their generated reports rather than expecting the recorded byte totals on another filesystem. The script reports an error if required hard-link or sparse-file behavior cannot be observed; it does not replace missing support with invented results.
