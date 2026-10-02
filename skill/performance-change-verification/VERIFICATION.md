# Execution and evidence verification

Executed on 2026-10-02 with an existing CPython 3.12.14 interpreter and the standard library. All inputs are original fictional records. The workflow performed local source execution and file readback only; no package installation, network service, account operation, UI automation or production operation was involved.

## What was executed

1. Authored the explicit [contract and expected outputs](example/contract.json), [implementations](example/summary.py), [fixed workloads](example/workloads.json) and [harness](example/verify.py) before the first timed attempt
2. Ran `python3 -B example/verify.py --out evidence/run.json`. It executed correctness checks and all 144 measurements, then failed its final saved-object comparison because tuple permutations serialized as JSON lists. The saved evidence was preserved as [initial-run.json](evidence/initial-run.json)
3. Changed only the `design.orders` representation to lists, as recorded in [initial-harness-change.json](evidence/initial-harness-change.json), and reran the same command. Exit status was zero. The measurement/harness interval before readback was 0.874741854 s; the full command including readback took approximately 1.39 s. No performance-based acceptance threshold or sample exclusion was applied
4. Ran `python3 -B example/verify.py --readback evidence/run.json`. Exit status was zero. It checked four source/input/contract hashes, all 144 sample identities and outputs, the actual balanced order, four recomputed summaries and the correctness gates
5. Executed four evidence-mutation checks. Readback rejected a changed source identity, missing sample, changed derived median and changed output hash. These check data integrity, not report wording
6. Reconstructed the initial source using the exact reverse replacement below and verified its full-file hash. Checked all four initial source/input/contract identities, all 144 initial sample labels/order/loop counts/output hashes/dispositions, positive elapsed durations and all four recomputed summaries. Both raw attempts remain available, 288 samples in total
7. Ran the skill frontmatter/scaffold validator; it reported `Skill is valid!`. Checked public relative links and read the saved explanatory files against the raw results
8. Independently recomputed both attempts' per-call minimum, median, maximum and median matched-block ratio from raw samples. Readback also passed from a different working directory and after relocating the packet; no machine-specific source path was needed

The full initial source was retained during review and compared byte-for-byte with the reconstructed source. The portable packet uses a small exact change record rather than a second copy of the same implementation. The initial failed final comparison is not relabeled as a successful original command. Its collected samples remain useful descriptive evidence with a clearly identified harness revision.

[checks.json](evidence/checks.json) contains the machine-readable verification outcome. Readback runs correctness operations without collecting new benchmark samples. It establishes content and arithmetic consistency, not independent witnessing or cryptographic authenticity of the original execution.

## Meaningful behavior checks

For both baseline and candidate, the harness checked:

- Three separately authored cases, including empty requests and empty records
- 259 exhaustive sequences of length zero through three from six diagnostic observation types, compared with a literal independent oracle
- Both complete timing workloads against that oracle
- Six metamorphic checks: reversed record order, appended unrequested records, and repeated request sequences on each workload
- Unchanged inputs and exact required output fields/value types
- Stable last output and unchanged shared inputs after each timed batch; the deliberately wrong control remains a measured failure on both timing workloads

The negative control actually failed four rows of the diagnostic fixture. It was timed 48 times per attempt under the same workload/boundary/loop design. Its timings were never eligible to count as equivalent-work improvement. The checks do not establish behavior on invalid input, floating-point values, concurrency or an unbounded input domain.

## Reproduce the saved checks

From the skill directory:

```sh
python3 -B example/verify.py --readback evidence/run.json
```

To make a separate new measurement without overwriting the recorded attempts:

```sh
python3 -B example/verify.py --out evidence/new-run.json
```

This helper does not checkpoint partial samples: a budget failure or other exception before its final write leaves no saved measurement report. Both supplied attempts completed sampling. Before adapting it to workloads with uncertain duration or failure behavior, add partial-result persistence in a separately identified harness to meet the guide's incomplete-attempt retention requirement.

The fixed design normally finishes in seconds. It has a 10 s check between batches; that is a bound on continuing work, not a preemptive timeout for arbitrary hanging code. This example executes known bounded loops only. The run refuses an existing output filename. Keep the new samples even if they are slower or inconclusive.

The following optional read-only reconstruction check establishes the exact initial harness identity and recomputes its summaries without re-running the old benchmark:

```python
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, "example")
import verify

change = json.loads(Path("evidence/initial-harness-change.json").read_text())
current = Path(change["corrected_source"]).read_text()
assert current.count(change["corrected_fragment"]) == 1
initial_source = current.replace(change["corrected_fragment"], change["original_fragment"])
assert hashlib.sha256(initial_source.encode("utf-8")).hexdigest() == change["initial_source_sha256"]
old = json.loads(Path("evidence/initial-run.json").read_text())
for name, expected_hash in old["source_sha256"].items():
    content = initial_source.encode("utf-8") if name == "example/verify.py" else Path(name).read_bytes()
    assert hashlib.sha256(content).hexdigest() == expected_hash
assert old["summaries"] == verify.summarize(old["samples"])
```

Run it with `python3 -B` to avoid writing bytecode caches. The current harness's ordinary `--readback` intentionally rejects the initial attempt's changed harness hash; use the documented reconstruction for that attempt. Do not rewrite the initial manifest to pretend it ran the corrected source.

## Independent readback

A separate review ran the relocated check-only route and all four corruption guards without collecting new benchmark samples. Independent rational-arithmetic calculations matched every sample-derived group summary and the displayed counts across both retained attempts. A fresh hand-calculated semantic case agreed with the baseline and candidate and rejected the last-record control. The source/input/output identities, balanced order and exact initial-harness reconstruction were also checked. This establishes semantic and evidence consistency; it does not independently witness the original timing or host activity.

## Exact identities

SHA-256 values of the executed source, inputs and saved evidence:

| File or reconstructed source | SHA-256 |
| --- | --- |
| `example/summary.py` | `d6edce7e5c4969a568041554a7abd44effbc0e790f101370d4f8839362e78193` |
| `example/verify.py` | `95fe27ab553c9933f5f93271aa425e5caae5e228d024ee8fd1752077442f85c8` |
| Initial `verify.py` | `d2439f913acb5c7430e232abe94a035d0612935b27bc37a6372f41cf0ce70ed0` |
| `example/contract.json` | `8dafa914132e8221cbbd9c45df6e9b3665883a61a832bd146eca894598c3d0f6` |
| `example/workloads.json` | `6d292ad889aa86f2444a8f7bc9a5a81b0db3353122e85f4c4e0c41d5520eddae` |
| `evidence/run.json` | `1be59dffb2a737adde9a9fe4096e1edb79bdad5cc89203b9bc995053a251f638` |
| `evidence/initial-run.json` | `934a0c7edc7503f33e7787c881d45b0b4ee0f83b2e571a4b7142351ea35819f4` |
| `evidence/initial-harness-change.json` | `87f0de3c61e12aa29c44cc9d820fca49b95749d2b7e7b13b806f5201596b74fc` |
| `evidence/checks.json` | `13c2040680bc331d00b1fbddb0bb29e968628cebc41403020ea3ae6e54903138` |

The function candidates share one source-file hash and are further identified by their callable names. Canonical pipeline input hashes and output hashes are recorded for each workload in the raw evidence; exact original workload-file bytes have their own hash. The explanatory documents are not executable candidate inputs.

## Reviewed material and unexecuted scopes

Reviewed current primary Python documentation on 2026-10-02. The versioned 3.12 documentation then displayed patch version 3.12.15; the installed runtime was 3.12.14. The documented APIs used here exist in the installed interpreter, and its actual clock properties were recorded at execution:

- [time.perf_counter_ns and get_clock_info](https://docs.python.org/3.12/library/time.html#time.perf_counter_ns): integer elapsed-clock values and clock metadata; reported resolution is not a measurement-error guarantee
- [timeit](https://docs.python.org/3.12/library/timeit.html): setup exclusion, default GC disabling and interference cautions. Reviewed for measurement choices; this harness does not execute `timeit`
- [statistics.median](https://docs.python.org/3.12/library/statistics.html#statistics.median): the median used to summarize batch averages
- [hashlib.sha256](https://docs.python.org/3.12/library/hashlib.html#hashlib.sha256): content hashes used to bind source and data bytes

The benchmark was run in a shared environment, with intermittent document-rendering activity reported during the broader collection period and unknown precise overlap with samples. No quiet-host, cold-cache, sustained-load, memory, concurrency, production or user-productivity validation was executed. The [worked result](EXAMPLE.md) preserves outliers, both attempts and the resulting uncertainty rather than implying those checks passed.
