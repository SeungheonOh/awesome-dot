---
name: run-bounded-validation-batches
description: Run a known collection of independent validation programs with bounded concurrency, complete outcome accounting, and evidence tied to the tested sources. Use when speeding up a local validation batch or making its release gate reliable; not for diagnosing flaky assertions or authoring product tests.
---

# Run bounded validation batches

## When to use

Use when a project has several independently executable checks and needs a reliable batch result without starting every process at once. Deliver an ordered outcome record and a trustworthy pass/fail decision. Parallelism is optional: correctness and resource ownership come first.

## Required inputs

- Exact executable, argument arrays, working directory, and intended test inventory
- Shared files, ports, databases, external services, and other resources each check touches
- Allowed concurrency, per-program deadline and output limit appropriate to this environment
- Source and dependency inputs whose changes invalidate the result
- Whether the result will gate packaging or another authorized action

If independence is uncertain, keep affected checks serial. An authorization to run local tests does not authorize paid remote jobs, live account mutations, or new credentials.

## Workflow

### 1. Establish a finite inventory and ownership model

Resolve the checks before execution, and give each a stable identifier. Reject duplicate or malformed entries. Do not interpret an empty inventory as evidence that the product passed testing. Preserve exclusions with reasons rather than silently changing the denominator.

Inspect resource use. Give parallel checks separate temporary directories and disposable fixtures. Avoid concurrent writers to a checkout, shared evidence file, fixed port or database. A small worker count does not make shared state safe. Keep external integrations in a separately identified group when their cost or side effects differ.

Record relevant runtime, OS, dependency lock, flags and source identities. Use an allowlist for environment metadata; never dump credentials or the entire environment.

### 2. Make a started run visibly incomplete

Before launching any check, write a new run identity with `passed: false`, a running state, start time, source fingerprint and expected inventory. If the runner crashes, a previous green result must not remain current.

Use atomic replacement where supported, and one evidence writer per checkout. If overlapping runs are required, use per-run outputs and a deliberate selection rule or lock; do not let the last process to exit silently designate itself authoritative.

### 3. Execute within explicit limits

Use an executable plus an argument array, without shell interpolation. Limit active programs through a queue, not by launching all promises and hoping the machine copes. Start with serial execution; increase concurrency only for independent work and within memory/CPU constraints.

For each launched program capture:

- Start/end or duration and stable identifier
- Exit code, terminating signal, spawn/setup error, deadline or output-limit failure
- Bounded stdout and stderr, with truncation clearly indicated
- Whether the program completed, failed, timed out, was cancelled, or never started

Count bytes before decoding output; preserve split UTF-8 sequences with a streaming decoder. A combined output cap bounds retained logs, not the child process's memory. Do not reinterpret timeout, killed process, missing result or runner failure as a passing assertion.

Use a cleanup method appropriate to the runtime. On POSIX, an owned process group can help terminate ordinary descendants; on other systems use the available owned-process mechanism. This is not an operating-system sandbox. A process that changes sessions, independent services, or escaped descendants may require stronger isolation. Never kill unrelated processes by broad name matching.

### 4. Separate completion order from presentation order

Store each outcome at its original inventory position. Workers may finish in any order while the final report stays deterministic. Print grouped logs with program identifiers instead of interleaving unlabelled output.

Define whether an ordinary failed check stops the queue or allows remaining checks to finish. Either policy can be valid; retain failed and unrun outcomes explicitly. A broken reporting callback or runner infrastructure error should stop further launches, clean up owned active work, and leave the batch failed. Document whether callbacks are synchronous or awaited; do not accidentally drop rejected promises.

### 5. Close the evidence only after reconciliation

Require one reconciled outcome for every intended check. Compare the actual inventory with the expected one, and fingerprint relevant source inputs again. A passing batch whose inputs changed during execution is not evidence for a single coherent revision.

Write the final state only after all owned workers have settled and cleanup is accounted for. Record concurrency, limits, final source identity and counts by outcome. A release gate should reject running, failed, stale, incomplete or mismatched evidence, not just look for a file named “results.”

If packaging is part of the requested workflow, verify that the packaged source bytes match the tested bytes and that the required tests/dependencies are included. Testing an extracted package checks a different boundary than testing the producer checkout. Keep the claims separate.

## Validate the runner itself

Use small original fixtures in isolated temporary directories:

- Successful programs that finish in a different order from their inventory order
- A deliberate nonzero exit, a hanging program and excessive output
- A multibyte character split across output chunks
- Invalid options and an empty inventory
- A reporting failure while another owned child is active

Measure concurrency through start/completion instrumentation or explicit synchronization, rather than a fragile assumption that two processes will start within a few milliseconds. Check that failures remain failures and retained output respects the cap. When testing cleanup, verify the actual owned process boundary; do not infer it from the runner returning.

## Worked example

A local collection had 94 validation programs and a release archive gated by source fingerprints. Its runner accepted one to four concurrent programs, a 120-second per-program deadline and a 1 MiB combined output cap. The batch used the same explicit test inventory in serial and parallel modes.

From the collection root, the exercised command was:

`TEST_JOBS=4 node app-validation/run-all.mjs`

On Linux with Node 24.19, the producer run on October 2, 2026 completed from 21:58:21.911 UTC to 21:58:39.740 UTC with 94/94 programs passing. A second run from an extracted archive, in a directory containing spaces, also passed 94/94. That consumer check reused installed offline dependencies; it did not prove a fresh registry installation or cross-platform compatibility.

The runner fixtures included an exit-code-7 program, a hanging program terminated under a shorter fixture deadline, output exceeding a 100-byte fixture cap, split UTF-8, and a throwing completion callback. Start/completion hooks checked the concurrency ceiling independently of process startup timing. The release gate required the complete current-source evidence, so an interrupted new run could not reuse an earlier success.

The checks included simulated DOM and audio behavior. Neither the batch count nor the archive rerun proved real-browser rendering, subjective audio quality, hostile-process containment or production reliability. This example's paths and limits are a concrete implementation, not required defaults for another project.

## Output

Provide the command, tested source identity, actual inventory and outcome counts, worker count and limits, evidence location, and any unverified boundary. Report “94 programs passed for these sources” rather than “everything works.” Stop when the requested batch and its evidence are complete; do not keep rerunning unchanged checks to accumulate green results.
