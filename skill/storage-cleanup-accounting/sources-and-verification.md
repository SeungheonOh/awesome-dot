# Sources and Verification

## Official references checked on 2026-10-02

- [GNU coreutils: du](https://www.gnu.org/s/coreutils/manual/html_node/du-invocation.html): apparent-size and allocation modes, hard-link counting, and limitations with shared or compressed data
- [GNU coreutils: df](https://www.gnu.org/s/coreutils/manual/html_node/df-invocation.html): filesystem-level used and available capacity, including path-specific selection and explicit units
- [GNU coreutils: stat](https://www.gnu.org/s/coreutils/manual/html_node/stat-invocation.html): file/device/inode/link and block fields, and separate filesystem statistics
- [Python: filesystem stat fields](https://docs.python.org/3/library/os.html#os.stat_result) and [statvfs](https://docs.python.org/3/library/os.html#os.statvfs): platform-specific identity/allocation values and filesystem availability counters
- [Linux kernel: Overlay Filesystem](https://www.kernel.org/doc/html/latest/filesystems/overlayfs.html): overlay identity and layer behavior have configuration-dependent limits; the measured short-lived fixture is not a guarantee for existing lower-layer files
- [Microsoft: OneDrive Files On-Demand for Windows](https://support.microsoft.com/en-us/onedrive/save-disk-space-with-onedrive-files-on-demand-for-windows): local residency and online-only behavior must be distinguished from deletion
- [Apple: Time Machine local snapshots](https://support.apple.com/en-us/102154): snapshot space is managed and represented differently from ordinary removable file totals

GNU's official manual text was available through search retrieval, including the relevant option definitions and accounting cautions; direct page opens timed out. Those retrieved manuals identify coreutils 9.11. The executable example separately records the installed coreutils 9.7 version and actual results from the options it uses. It does not rely on a successful direct GNU page load as execution evidence.

These sources explain product behavior. No Windows, macOS, OneDrive account, Trash, snapshot-management interface or cloud-residency action was operated. Use current instructions for the actual client and account before proposing a product-specific operation.

## Local evidence preserved

The fixture was executed on Linux/OverlayFS with Python 3.12.14 and GNU coreutils 9.7. [evidence.json](evidence.json) is the actual recorded output, not a hand-composed sample. [plan.json](plan.json) records the pre-action state; [manifest.json](manifest.json) records all dispositions and their final paths. The script saves relative fictional paths only.

The executed checks established:

- A separate inode had the same digest as the retained export
- Two names shared the same observed device/inode and link count 2
- The sparse file's reported allocation was smaller than its logical size
- GNU `du` totals on the exact file set matched the corresponding once-per-inode calculations
- The authorized move and reversal preserved the observed file identity and bytes, with the old name absent after each rename
- The other generated files stayed unchanged in the properties checked
- An existing destination caused a pre-mutation rejection and preserved both files

A separate invocation using an already-existing output directory was rejected, and a before/after digest inventory confirmed that its existing file contents were unchanged. A separate read of the saved JSON records reconciled all five manifest rows, the plan's preconditions, both readbacks, block-unit arithmetic and zero payload reclamation. These checks did not involve real user files.

The report's capacity goal is intentionally unmet: zero payload bytes were released. A zero volume delta happened in the recorded run but is not an assertion of the checker. Final report files are written after the measured interval; the initial plan is written before the baseline.

An independent isolated run confirmed the accounting, both move readbacks, unchanged measured file properties, and refusal to reuse an existing output directory. Its own timestamps, inodes and volume counters were treated as new observations rather than expected constants.

A separate guide-only case correctly distinguished 10 GiB of path-summed logical length from 9 GiB counted once per inode. It held a reversal after the moved file changed and did not attribute an unattributed 3 GiB availability increase to a same-volume move. That case produced an assessment only; it did not move or delete files.

## Boundaries

This is a single-process demonstration in an exclusively created directory. Its existence check followed by rename is not a race-free no-overwrite primitive for a live shared directory. It does not implement a general scanner, deletion engine, recovery service or duplicate cleaner. The saved plan can help explain an interrupted run, but the demonstration does not test crash recovery or provide a durable journal after each syscall.

The comparisons cover regular-file membership, identity, logical size, reported allocation, link count, modification time and content digest. Directory allocation, ACLs, extended attributes, alternate streams, application use and all timestamp fields were not validated. Snapshot retention, open-but-unlinked files, cloud placeholders, compressed files and different-inode shared extents were discussed as limits, not created or tested.

The filesystem's available-byte counter covers more than the fixture. It cannot by itself isolate an action's effect from concurrent writes or account for every physical device layer. Once-per-inode accounting prevents the demonstrated hard-link double count but does not establish exclusive block ownership. No real free-space target, real recoverable deletion or cross-volume migration was completed.
