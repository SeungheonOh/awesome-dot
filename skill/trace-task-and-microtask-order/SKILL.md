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

### Mark checkpoints and uncertainty

Distinguish callback creation, enqueueing, dispatch and completion in the trace. Record the queue state before and after a checkpoint, including newly queued microtasks. If the snippet contains features outside the established runtime model, mark the first unresolved ordering rather than extending a simple rule by intuition.

Keep execution read-only and bounded. If a supplied snippet performs network, filesystem or account actions, extract an authorized minimal reproduction or explain why it cannot be executed as-is. Reading code for an ordering explanation does not grant its side effects.

## Output

An ordered trace with queue/checkpoint explanations, observed output if executed, and the exact runtime assumptions or unresolved orderings.

## Verification and limits

Check nested microtasks, a microtask queued by a timer, and multiple ready tasks. A Node result is not proof of all browser scheduling details.

## References

[MDN microtask guide](https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API/Microtask_guide)

## Example request

“Explain this snippet’s observable order in the named runtime. Show when callbacks are enqueued versus run, and mark anything the available evidence cannot order uniquely.”

## Worked example

A supplied finite example logs “start,” schedules a timer that logs “timer,” queues a microtask that logs “micro,” and then logs “end.” Under the stated browser task/microtask model, the order is start, end, micro, timer.

A second example begins with microtask A followed by microtask B; A queues microtask C when it runs. FIFO draining produces A, B, C, because C joins behind the already queued B. Merely saying “microtasks run immediately” would predict the wrong order.

The output is a queue trace, with the synchronous return and microtask checkpoint labeled. These supplied semantic examples do not establish exact elapsed timer delays or ordering between unrelated task sources.

## Evidence status

The worked example illustrates the stated inputs and reasoning. Unless an execution result is explicitly identified, it is not a claim that external services, real devices or user data were tested. Report actual checks and unrun stages on each use.
