---
name: trace-task-and-microtask-order
description: "Explain the execution order of a bounded JavaScript example with explicit queue checkpoints and runtime-specific limits."
---

# Trace task and microtask ordering

## When to use

A callback ordering question or bug needs a trace that distinguishes enqueueing work from executing it.

## Required inputs

- The exact bounded snippet and intended runtime/version
- Relevant timer, promise and microtask behavior
- Whether executing the trusted snippet in an isolated test runtime is authorized

## Workflow

1. Identify synchronous statements, enqueued microtasks and task callbacks. Establish which runtime semantics apply; do not mix Node-only phases with browser rules.
2. Trace the current synchronous work to completion, then the applicable microtask checkpoint, including microtasks enqueued during that drain. Record queue contents and observable output after each transition.
3. Separate a ready task model from actual elapsed timer deadlines. Where multiple task sources, I/O or rendering make order nonunique, state the allowed orders or missing evidence.
4. Cross-check a trusted finite reproduction in the intended runtime when available. Do not eval untrusted pasted code just to animate it. Bound execution and avoid its external side effects.
5. Explain the first point where observed and expected behavior diverge. Do not revise the expected semantics merely to match an implementation under test.

## Output

An ordered trace with queue/checkpoint explanations, observed output if executed, and the exact runtime assumptions or unresolved orderings.

## Verification and limits

Check nested microtasks, a microtask queued by a timer, and multiple ready tasks. A Node result is not proof of all browser scheduling details.

## References

[MDN microtask guide](https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API/Microtask_guide)
