# Runtime forensics

Use to diagnose a live runtime symptom. The deliverable is a diagnosis, not a source fix. Read the [execution contract](../references/execution-contract.md).

## Inputs

The symptom, process/environment identity, time window, available diagnostics, and permission for any instrumentation that changes runtime state. Prefer read-only observation. Profiling production, collecting sensitive memory, attaching a debugger, and injecting code may require additional authorization.

## Steps

1. Capture the signal through an observed diagnostic interface. CPU spin needs a profile or thread sample; a suspected leak needs repeated allocation/heap evidence; a rendering glitch needs frame or event timing evidence. Record capture overhead and whether it could perturb the symptom.
2. Reduce the capture without discarding its provenance. Identify hot stacks, retained objects and their GC roots, repeating timers, blocked threads, or unexpected event order. For large artifacts, use a bounded parser or delegated read-only analysis and retain queries and raw data identity.
3. Form a falsifiable mechanism. Correlate event order and state rather than inferring causation from a hot symbol alone. Compare a healthy condition, disable an isolated trigger, or add temporary instrumentation only where permitted. A live hotfix or injected expression is a mutation, not automatically a read-only diagnostic step.
4. Map the finding to the exact source version, symbol, and owner of the allocation, scheduling, or boundary behavior. Use actual symbols and source maps. Unresolved mapping remains a limit.
5. Remove temporary owned instrumentation, detach safely, and leave the process in the agreed state. Do not restart or terminate unrelated processes as cleanup.

## Failure and evidence

If capture is unavailable, state the specific prerequisite and provide the narrow capture recipe. A correlation without a discriminating observation is a hypothesis, not a confirmed cause. Avoid retaining secrets or unnecessary personal data in artifacts; use the host's approved handling.

Return the captured signal, reduced finding, causal test or confidence limit, source location, environment/revision, and artifact pointers. Hand a confirmed defect to [Bug fix](bug-fix.md) or [Perf issue](perf-issue.md) only when correction is requested.
