---
name: event-loop-teaching-simulator
description: Build a step-through JavaScript event-loop teaching app with visible task and microtask queues, immutable trace snapshots, source highlighting, and independently checked console ordering.
---

# Event-loop teaching simulator

Make callback ordering inspectable without running arbitrary user code. The worked product, Queue Theory, presents four finite examples with source, a simplified running frame, separate queues, console output, and reversible teaching steps.

## Inputs and boundaries

Choose the learning objective, runtime being explained, example programs, allowed execution environment, and delivery audience. Start with a narrow browser-oriented lesson: synchronous code finishes, then queued microtasks drain before the next timer callback. Do not casually combine browser ordering, Node-specific phases, rendering, networking, and promise rejection behavior into one supposedly universal diagram.

The teaching app should interpret a small trusted model, not evaluate pasted code. If a real debugger or arbitrary-code sandbox is requested, that is a different engineering and security task. Keep product source and tests outside a skills-only repository contribution; read current guidance and refresh main while preserving the user's explicit limits.

## Chronological build

1. **Write contrasting examples first.** Use a small set where changing one relationship changes the output: synchronous/microtask/timer order; microtasks that enqueue other microtasks; a checkpoint between two timers; and a timer created inside a microtask. Keep programs finite and readable.
2. **Specify expected output independently.** Write the console order and a sentence explaining why before implementing the visualization. Check authoritative runtime guidance, then execute these trusted snippets in an appropriate test runtime. A Node check can corroborate shared behavior for these examples, but is not proof of every browser scheduling detail.
3. **Represent instructions as data.** The worked model needs only log, enqueue-microtask, and enqueue-timer operations, with callback labels, child instructions, and source-line references. Validate or constrain this vocabulary. Do not use eval or Function on user input to animate it.
4. **Separate execution from dispatch.** A running frame executes its operations synchronously. When it returns, drain the microtask queue FIFO, including newly enqueued microtasks. Only when that queue is empty should the model dispatch the next ready timer task. For the lesson, explicitly label timers as ready tasks rather than simulating real elapsed deadlines.
5. **Record immutable snapshots.** Save the running frame, queues, logs, highlighted line, explanation, and completion state after every model action. Deep-copy the state, because later queue mutations must not rewrite the past. Add a finite-step guard so malformed teaching data cannot hang the app.
6. **Build the learning surface.** Put source alongside runtime state. Distinguish running work, queued microtasks, queued timers, and output by labels as well as colors. Keep the explanatory sentence tied to the current state, rather than displaying a generic paragraph while unrelated animation runs.
7. **Add reversible controls honestly.** Next, Back, scrub, Play/Pause, Reset, and example selection should move through the stored snapshots. Explain that Back rewinds the teaching trace, not real JavaScript execution. Preserve keyboard focus after rebuilding example buttons. Disable forward/play controls at the terminal state.
8. **Own playback lifecycle.** One timer advances the trace. Stop it before manual stepping, scrubbing, resetting, or switching examples, and when the page is hidden or exits. Repeated Play must not stack intervals. Playback speed must not change the trace or output.
9. **Test semantics and UI separately.** Compare the final model log with expected output and trusted native execution; require empty terminal queues and unchanged earlier snapshots. Use simulated-DOM tests for control wiring, then real-browser keyboard/mobile checks when possible. Keep the boundaries of each test visible.
10. **Package, publish, and contribute within scope.** A static app needs no backend or account. Validate packaging for the selected host and preserve the approved audience; a dry-run does not establish a live URL. Extract the reusable model, chronology, and verification into a skill-only change. Pull current main, avoid force-pushing over others, and verify the remote revision.

## Worked ordering checks

- Synchronous `start`, queued timer, queued microtask, synchronous `end`: `start, end, micro, timer`
- Microtask A enqueues C, while B is already queued: `script, A, B, C`
- Timer 1 queues a microtask and timer 2 is ready: `script, timer 1, micro after timer 1, timer 2`
- A microtask queues a timer after an earlier timer was scheduled: `micro, earlier timer, later timer` for this simplified zero-delay example

Preserve simultaneous conceptual distinctions: enqueueing a callback is not running it, returning a frame is not logging, and an empty stack does not imply the program has no pending work.

## Verification evidence

The original four traces passed expected log ordering, deterministic replay, immutable initial history, finite completion, and empty terminal queues. Their logs matched execution of the trusted source snippets in Node. A jsdom interaction test passed step/back, scrub-to-completion, terminal button state, example switching, and reset. Syntax checks and Wrangler static packaging dry-run passed. Live hosting and real-browser/mobile visual checks were pending at contribution time.

## Sources and limits

- [MDN microtask guide](https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API/Microtask_guide)
- [MDN runtime and microtasks in depth](https://developer.mozilla.org/en-US/docs/Web/API/HTML_DOM_API/Microtask_guide/In_depth)

Real timers have scheduling delays and clamping; browsers have multiple task sources and rendering opportunities. Promise chains, exceptions, networking, and Node-specific queues require additional modeling. If the example depends on an omitted feature, either extend and verify the model or explicitly exclude that example. Never fix a mismatch by changing the displayed expected output to whatever the simulator happens to produce.
