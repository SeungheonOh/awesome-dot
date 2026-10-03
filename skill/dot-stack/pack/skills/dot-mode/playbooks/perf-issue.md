# Perf issue

Use for a particular slowdown to diagnose and improve. For sustained optimization use [Hillclimb](hillclimb.md). Read the [execution contract](../references/execution-contract.md).

## Inputs

A realistic workload, affected user-visible metric and unit, correctness guardrails, environment, baseline revision, and any latency/memory/cost budget. Do not choose an easy synthetic case that misses the complaint.

## Steps

1. Reproduce and capture the baseline with an available profiler or repeatable harness. Record hardware/runtime, data size, concurrency, warm/cold state, sample count, and variability. Separate end-to-end latency from CPU time, throughput, and total work.
2. Reduce the profile to a mechanism. Trace the costly path and its consumers. Source inspection can explain a trace; it cannot establish a speedup or prove the work is deletable.
3. Choose a trace-supported strategy. Eliminate unused work; divide input-dependent work; cache repeated work with an explicit invalidation rule; add an index or queue only when its overhead pays back; batch fixed-cost operations; hedge only with resource headroom and safe duplicate effects; defer unused work; or schedule necessary work away from an interactive deadline. These are alternatives, not a mandatory checklist.
4. Make one coherent change, locally or with a scoped owner. Preserve semantic and resource constraints. A lower average that increases tail latency or shifts unbounded work elsewhere is not an unqualified win.
5. Capture post-change evidence using the same workload and environment. Interleave baseline/candidate runs where drift matters. Compare distributions and relevant percentiles rather than a single lucky sample. Run correctness gates and affected integration cases.
6. Accept only a meaningful improvement beyond noise with guardrails intact. Revert owned unsuccessful changes safely. Report any tradeoff explicitly, including added state, memory, complexity, or maintenance cost.

## Failure and recovery

An insensitive harness, inconsistent workload, or unavailable profiler blocks the performance claim, not necessarily all analysis. Calibrate before optimizing. Missing source maps limit attribution. An improvement on an unlike workload is not a valid ratio. If baseline and candidate cannot both produce the metric, use a justified absolute budget and label the comparison limit.

## Evidence and completion

Return baseline and candidate numbers with units, delta, variation/sample method, exact revisions, workload and trace paths, correctness results, and the causal explanation. Publish only if authorized. Stop at the requested improvement or give a measured account of why the candidate was rejected.
