---
name: cache-policy-playground
description: Build a deterministic interactive comparison of FIFO, LRU, and optimal cache replacement with request-by-request playback, capacity curves, and independently checked examples.
---

# Cache Policy Playground

Create a small teaching instrument that makes replacement decisions visible. It models equal-size objects and equal-cost misses; do not present its miss counts as measured application latency. Keep the generated app outside this skills repository.

## Inputs and scope

Use a synthetic request stream or a user-approved local sequence of identifiers. Choose a bounded stream length and capacity range so every state can be inspected. A useful starting envelope is 1–60 requests and 1–8 cache slots. No backend is needed. Publication and third-party uploads require the user's chosen destination and authorization.

## Build sequence

1. Define the semantics before drawing the interface. Every cache starts empty. A hit finds a resident identifier; a miss loads it and, only when full, evicts one. State whether identifiers are case-sensitive. Reject an empty stream and unsupported identifiers rather than silently rewriting them.
2. Implement a pure simulator returning an initial state plus a fresh snapshot after every request. Each snapshot includes resident entries, cumulative hits and misses, current request, hit/miss status, and the evicted entry. Copy resident arrays so Back and scrubbing cannot change history.
3. Implement the policies explicitly:
   - FIFO removes the oldest arrival; hits do not change its queue.
   - LRU moves a hit to most recent and removes the least recently used entry on a full miss.
   - OPT removes the resident entry whose next use is furthest in the remaining stream; never-used-again entries rank furthest. Break ties deterministically. Label this a future-aware oracle, not an implementable online policy.
4. Prove the model independently before connecting controls. For a short alphabet and short traces, compute the minimum possible misses with a memoized exhaustive search over every eviction choice, then compare OPT. This oracle must not reuse OPT's next-use rule.
5. Build three aligned policy cards: occupied/empty slots, hit/miss event, eviction explanation, and cumulative counters. Explain queue order on FIFO/LRU and avoid implying OPT's display order determines eviction.
6. Add Next, Back, Restart, Play/Pause, and request selection. Playback reads snapshots rather than rerunning asynchronous policy mutations. Stop the timer when inputs change, at the terminal state, when the document becomes hidden, and when leaving the page.
7. Separate edited input from applied input. While a trace is dirty or invalid, stop playback and disable controls that would mix old snapshots with new capacity. Preserve the last valid comparison, show an error, and resume only after Apply succeeds. A capacity change rebuilds all policies and returns the cursor to zero.
8. Compute a second comparison over the complete stream for every supported capacity. Clearly label this chart as whole-stream results, even during partial playback. Show numeric values accessibly and use policy labels as well as colors.
9. Verify interactions in a DOM harness, then inspect a real browser at desktop and mobile sizes when available. Simulated DOM tests do not establish layout, touch usability, or actual browser rendering.

## Concrete acceptance example

Use the stream `1 2 3 4 1 2 5 1 2 3 4 5`.

- FIFO with three slots produces nine misses; four slots produces ten.
- Explain that more capacity changes FIFO's eviction sequence; do not generalize this anomaly to every replacement policy.
- At every step, hits plus misses equals requests processed, resident entries are unique, and occupancy is no greater than capacity.
- Replaying an identical input returns identical snapshots. Back then Next returns to the same state.
- With enough slots for every distinct identifier, only first occurrences miss.
- For every capacity, OPT's misses are no greater than either FIFO or LRU.

The [original Belady, Nelson, and Shedler paper summary](https://research.ibm.com/publications/an-anomaly-in-space-time-characteristics-of-certain-programs-running-in-a-paging-machine) provides context for the anomaly. State the simplified assumptions beside the visualization.

## Interaction checks and failure handling

Exercise a completed stream, Back from completion, Restart, repeated Play/Pause, and a preset change during playback. Edit to an invalid trace and try capacity/playback controls; old snapshots must never render with incompatible capacity. Restore a valid stream and verify that errors clear. Test the maximum stream and capacity boundaries, one repeated identifier, and all-distinct identifiers. Use text nodes or escaped output for user-entered labels.

If independent model checks fail, fix the simulator before polishing animation. If rendering cannot be inspected, deliver the source and precise passed checks, explicitly leaving visual QA unverified. Do not substitute a screenshot-only mockup for the interactive product.

## Evidence from the reference build

Cache Parade used a pure JavaScript model and a dependency-free static interface. The model matched an independent exhaustive minimum for all 729 six-request traces over three identifiers at capacities one through three (2,187 comparisons). Its separate simulated-DOM checks covered stepping, seeking, returning, dirty input, capacity changes, invalid input, and presets. Real-browser visual QA was not completed for that build at contribution time. These checks are a reproducible approach, not proof about a new implementation.

## Deliverable

Provide the runnable app separately, the model/interaction verification results, and a short explanation of assumptions and unverified behavior. When contributing this workflow, publish only this SKILL.md; keep product source, test programs, deployment data, and build notes outside the skill contribution.
