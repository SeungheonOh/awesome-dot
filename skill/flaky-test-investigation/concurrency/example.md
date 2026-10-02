# Controlled concurrency: repair a lost addition

This companion exercises a product defect. A fictional workshop's tally starts at seven paper cranes. Worker A adds two and worker B adds three. After both calls complete, the tally must be the integer **12**, regardless of which call started first. Each call runs once, on one event loop, through the same tally owner; no cancellation, external writer, or second owner belongs to this contract.

The earlier [unordered-record example](../example.md) repairs an unsupported test assumption. Here the original assertion is correct. The product's read/modify/write operation needs repair.

## Before, after, and the unchanged assertion

[tally_before.py](tally_before.py) reads a snapshot and later writes its sum:

```python
async def add(self, actor, amount):
    current = await self.store.read(actor)
    await self.store.write(actor, current + amount)
```

Two callers can read seven before either writes. A later write can overwrite the other completed addition. No malformed response or unsupported output order is needed.

[tally_after.py](tally_after.py) creates one `asyncio.Lock()` in the tally's constructor and holds it across the whole operation:

```python
async def add(self, actor, amount):
    async with self._lock:
        current = await self.store.read(actor)
        await self.store.write(actor, current + amount)
```

The lock belongs to this shared tally instance. A new lock per call does not coordinate callers; locking only the write cannot repair a stale read. The fixture executes both incorrect repairs as negative controls.

Every before/after case and every negative control uses exactly the same function in [check_concurrency.py](check_concurrency.py):

```python
def correctness_assertion(actual, initial, additions):
    require(type(actual) is int, "The stored total must be an integer")
    require(actual == initial + sum(additions.values()),
            f"Lost or extra addition: expected {initial + sum(additions.values())}, got {actual}")
```

`require` raises `AssertionError` explicitly, so optimized Python cannot remove this check. The repair changes the product, not the expected total, retries, or failure classification.

## Exact fixture and schedule contract

Each case creates a fresh in-memory store, owner, events, and worker tasks. The store's read captures its integer snapshot before asynchronously completing; write assigns its supplied integer when it completes. A `call_soon` callback completes a fresh future on a later event-loop turn. This supplies a tiny, original asynchronous fixture without a service, clock delay, or third-party code.

The finite plan is declared before execution: per revision, two serial cases, two controlled cases, and eight ordinary concurrent cases. The serial and controlled pairs start A first and B first respectively. Two deliberately incorrect repair cases follow. Each slot runs once. Four invalid-total controls are separate from those 26 planned concurrency comparisons.

Both revisions use the same adaptive controlled schedule:

1. Start the first worker and pause its store read after capturing the snapshot
2. Start the other worker
3. Wait for one observable condition: the second worker completes, or it attempts the held shared lock
4. Release the first worker, then await both completed calls and compare the exact total

The controlled repair uses `ObservedLock`, an `asyncio.Lock` subclass that logs public `locked`, `acquire`, and `release` operations. It delegates acquisition/release to the real lock. On this single event loop, no suspension occurs between observing the held lock and awaiting acquisition. Ordinary and serial repair runs use the unmodified `asyncio.Lock` created by the product.

The controller does **not** wait for both workers to read when the first already holds the repaired lock. That barrier would demand an impossible interleaving and manufacture a deadlock. It releases the first worker after actual contention is observed. The resulting write/read sequence is then checked separately against the declared schedule; a trace mismatch is a runner error, not a product assertion failure.

These observed traces appear in [example-results.json](example-results.json):

| Case | Recorded state operations | Result |
| --- | --- | --- |
| Before, A first | A reads 7; B reads 7; B writes 10; A writes 9 | Fails: 9 instead of 12 |
| Before, B first | B reads 7; A reads 7; A writes 9; B writes 10 | Fails: 10 instead of 12 |
| After, A first | A reads 7; B contends; A writes 9; B reads 9; B writes 12 | Passes |
| After, B first | B reads 7; A contends; B writes 10; A reads 10; A writes 12 | Passes |

The full traces also record call starts/completions, gate releases, and lock acquisitions/releases. The sequence numbers identify observed ordering on the event loop; they are not timestamps or a cross-process causal trace.

## Reproduce without changing the evidence

Use an existing Python 3.11+ interpreter. From this folder:

```sh
python3 -B check_concurrency.py
```

This prints a fresh JSON report and leaves the bundled evidence unchanged. To retain a run, choose a directory that does not already exist:

```sh
python3 -B check_concurrency.py --output concurrency-run-01
```

The directory's parent must exist. An existing file or directory is refused before any cases run; `results.json` is opened exclusively. No source or input file is modified. The report records source-file, product-class, fixture, and assertion SHA-256 identities, then checks source files again after execution. These are content identities, not repository commits. `-B` avoids bytecode-cache writes.

A five-second per-case deadline is a safety bound on cooperative fixture waits. It does not order writes, repair correctness, or promise product latency. All owned tasks are cancelled and awaited during cleanup; cancellation is not suppressed in worker code. Timeouts, cancellation, and runner errors are recorded outside the correctness denominator, stop the remaining planned concurrency comparisons, and produce a nonzero result. The controller also observes a first worker that fails before reaching its paused read. A product-raised `TimeoutError` is a runner error unless the harness deadline actually expired. Unrun slots retain their reason. Cancellation cleanup can exceed the nominal timeout. A forcibly terminated interpreter cannot produce a complete in-process ledger.

Exit zero means the demonstration met its declared expectations, **including** expected failures before repair and in the negative controls. Unexpected outcomes return nonzero. The raw ledger retains the actual assertion failures; it does not relabel them as passing product results.

## Recorded outcome and interpretation

The bundled CPython 3.12.14, Linux x86_64 run completed all 26 planned concurrency comparisons, with no runner errors, timeouts, cancellations, skipped slots, or retries:

| Product and mode | Passed / completed | Failed / completed |
| --- | --- | --- |
| Before, serial | 2 / 2 | 0 / 2 |
| Before, controlled | 0 / 2 | 2 / 2 |
| Before, ordinary concurrent | 0 / 8 | 8 / 8 |
| After, serial | 2 / 2 | 0 / 2 |
| After, controlled | 2 / 2 | 0 / 2 |
| After, ordinary concurrent | 8 / 8 | 0 / 8 |
| Incorrect per-call lock | 0 / 1 | 1 / 1 |
| Incorrect write-only lock | 0 / 1 | 1 / 1 |

All four invalid-total controls were rejected: a lost A addition (10), lost B addition (9), extra addition (13), and string `"12"`. Source files remained unchanged.

The controlled failures are deliberately chosen witnesses. The eight ordinary runs have no controller, gate pause, observed-lock substitution, random seed, or hidden retry, but still use the synthetic asynchronous store and the same launch order. Their observed 8/8 failure before repair is not a random sample or a real-world failure probability. Serial success and controlled failure establish schedule-sensitive behavior; the example does not claim a naturally intermittent ordinary-run failure rate.

The shared lock is sufficient for the stated one-owner, one-loop contract. It does not cover multiple tally instances sharing a store, threads, processes, external writers, retries, crash recovery, or cancellation transaction semantics. A persistent multi-writer service would need its own atomic-update or transaction contract. These checks do not establish live CI health, every possible schedule, fairness under load, or throughput.

## Independent readback

A separate inspected run reproduced the saved JSON exactly: 26 completed comparisons, 14 assertion passes and 12 expected assertion failures, with no runner faults. A changed-input check used an initial 101 with additions 11 and 17. Both controlled orientations exposed stale totals of 112 or 118 before repair and produced 129 with the shared lock; the two incorrect lock scopes still failed. Product-raised `TimeoutError`, early cancellation and a cooperative deadline remained separate outcomes, owned tasks were settled, and an existing output destination was refused unchanged. These are finite local fixture checks, not additional evidence about a deployed application.

## Primary semantics checked

- Python's [asyncio synchronization documentation](https://docs.python.org/3/library/asyncio-sync.html) describes task mutual exclusion, waiting for lock acquisition, release on leaving `async with`, and event flags. These primitives are not thread-safe. This fixture uses one loop and does not depend on waiter fairness
- Python's [task documentation](https://docs.python.org/3/library/asyncio-task.html) describes cooperative scheduling and cancellation. `wait` leaves pending tasks running; the harness settles its own tasks explicitly. The `timeout` context cancels overdue work and exposes whether its deadline expired. Cooperative cancellation does not provide a hard process-kill guarantee
- Python's [event-loop documentation](https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.call_soon) describes scheduling callbacks for a subsequent iteration. The fixture uses that completion boundary without a sleep-based repair

Documentation checked on 2026-10-02; the actual tested interpreter and event-loop class are recorded in the JSON evidence. Other Python versions and platforms were not run here.
