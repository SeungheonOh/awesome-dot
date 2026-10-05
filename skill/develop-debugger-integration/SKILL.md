---
name: develop-debugger-integration
description: Build or maintain a debugger adapter, runtime bridge, or native debugger client integration that keeps real execution, stopped-state inspection, and session completion consistent. Use for debugger tooling and compatibility changes, rather than ordinary program diagnosis or analysis of an existing trace.
---

# Develop a debugger integration

A useful integration lets its client explain where the program really stopped, inspect the state at that point, and control what happens next. Develop that relationship through the selected engine and protocol. Returning well-shaped responses or displaying a scripted sequence cannot establish it.

## Choose a small, complete interaction

Read the requested client experience, affected implementation and callers, runtime requirements, and existing tests. Identify the program or runtime in scope, how the session starts, the required execution controls, and who owns its resources. For maintenance, observe a useful existing interaction and name the behavior being changed before editing.

Prefer a suitable existing adapter and engine. A client integration may need only configuration, request handling, or presentation changes; it need not introduce custom protocol handlers. Check the available versions and their actual behavior. Keep a small integration complete with one meaningful stop, useful inspection, resumption, and observed completion. Add other controls or targets only when the request needs them.

Use existing project documentation and tests to record the supported interaction. Resolve a consequential choice with a concrete example: should stepping cross this call, which source corresponds to this frame, or should ending this session leave the program alive? A separate protocol, conformance matrix, or specification document is unnecessary.

Use the chosen protocol's own initialization, transport, capability, and lifetime rules. For DAP, initialization exchanges capabilities; an absent optional capability is unsupported. Honor the client's path and line/column conventions. Configuration starts when the adapter signals readiness, with `configurationDone` used only when supported. Prefer established transport support; DAP framing counts UTF-8 body bytes. See the [DAP overview](https://microsoft.github.io/debug-adapter-protocol/overview.html).

## Connect commands to execution

Follow each required control from the client's action to the real engine and back to an observation. Define what makes a step complete at the selected granularity. A callback announcing a function return may occur before control reaches the caller; inspect the engine's semantics before translating it into a completed step-out. For example, [Python 3.12 bdb](https://docs.python.org/3.12/library/bdb.html) distinguishes line, call, and return callbacks. Its behavior is an engine-specific input to the mapping, not a universal debugger model.

Keep command responses and execution observations separate. In DAP, correlate responses with `request_seq`; a successful step response precedes the later `stopped` event. A request that implies resumption does not require a redundant `continued` event. Process events while awaiting responses, and reconcile them with the client's current state. See the [DAP specification](https://microsoft.github.io/debug-adapter-protocol/specification#Requests_StepOut).

Keep the control path usable in every supported execution state. The engine must not monopolize the only path that handles required controls or shutdown. Choose an existing event loop, engine facility, or owned worker only as needed. A single stopped-state request at a time can be sufficient; concurrency is not a prerequisite.

For source breakpoints, distinguish what the client requested, what the engine accepted, and where execution actually stopped. Preserve rejected or relocated locations in the client view. DAP `setBreakpoints` replaces one source's set, including clearing with an empty set; apply that change to the engine, not just the displayed list. Later breakpoint verification changes must reach the client. See [breakpoint configuration](https://microsoft.github.io/debug-adapter-protocol/overview.html#configuring-breakpoint-and-exception-behavior).

Treat running-state pause as a separate requirement. Establish an actual stopping mechanism and its limits before offering it. For example, bdb's `set_continue()` can remove tracing when no breakpoints remain; a pause request handler alone cannot restore control of execution. Cooperative checkpoints do not promise interruption of arbitrary blocking calls. Keep exceptions, multiple threads, value mutation, and expression evaluation conditional on the requested experience and supported engine.

## Make inspection describe the current stop

Obtain stack frames and values from the real suspension. Relate the displayed statement to when it executes: a value visible before an assignment may belong to the previous iteration. Define any filtering of runtime or library frames so the client does not mistake a teaching view for a complete stack.

Resolve source through the protocol's source authority, then check the reported location against that content. In DAP, a positive `sourceReference` requires a `source` request even when a path is present, and the reference lasts for the session. Source maps or generated-source handling are needed only when execution and the requested source view differ. See the [Source definition](https://microsoft.github.io/debug-adapter-protocol/specification#Types_Source).

Manage inspection references at their actual lifetime. DAP suspension-bound frame and variable references expire on resume; reacquire stack, scopes, and values after another stop. Numeric IDs can recur and do not identify the same object across stops. Thread and source references have different lifetimes. See [object references](https://microsoft.github.io/debug-adapter-protocol/overview.html#lifetime-of-objects-references).

Do not present retained stopped-state values as current running-state inspection. Refuse unavailable inspection clearly. If work can overlap resumption or a new stop, prevent late responses from replacing the new view; local ownership bookkeeping may help, but is not a new wire requirement. A test of running-state refusal must establish when the adapter handled the request. Absence of a client-observed stop alone cannot establish that execution is still running.

## Verify the client experience and completion

Exercise the saved integration with the actual native client and real engine. The client must use returned locations, references, values, and events rather than import the adapter's mapping helpers to construct expected answers. Derive expected program behavior independently from its inputs and semantics. Compare ordinary execution with debugged execution where preserving output, effects, or status is part of the contract.

Choose a short session that distinguishes the promised behavior. For stepping work, enter and leave a meaningful call and inspect the corresponding state. For inspection lifetime work, resume to a later stop where values change and refresh the view. For breakpoint maintenance, replace or clear a breakpoint before execution reaches it again and observe the consequence. Retain a useful unchanged caller case. These are targeted checks, not features every integration must add.

Observe program completion separately from session completion. DAP `exited` reports the debuggee's exit code; `terminated` ends debugging and does not prove program exit. Follow launch/attach ownership when disconnecting. The optional `terminateDebuggee` argument requires `supportTerminateDebuggee`. See [session termination](https://microsoft.github.io/debug-adapter-protocol/specification#Events_Terminated) and [disconnect](https://microsoft.github.io/debug-adapter-protocol/specification#Requests_Disconnect).

For processes the integration owns, drain relevant output, observe exit status, and release readers, pipes, and children. Keep successful cancellation distinct from normal program completion. A timeout or forced cleanup must not become evidence that the intended run finished. For an external runtime, report only the completion facts its supported interface establishes.

Deliver the requested reusable change and invocation or integration instructions, with supported behavior and observations tied to the final files. A native protocol client establishes that interaction; an editor claim needs an actual pass in that editor. For tasks explicitly limited to static design or source review, report runtime and client behavior as unverified. An implementation delivered as source still requires the actual native-use checks above. Recheck affected behavior after changes and preserve historical evidence under its original version. No arbitrary target runner, listener, attachment feature, expression console, installation, or public release is inherent in this method.

## Existing owners

[API contract design](../design-api-contract/SKILL.md), [CLI development](../develop-command-line-tools/SKILL.md), [scoped implementation](../implement-scoped-change/SKILL.md), and [behavior tests](../write-behavior-tests/SKILL.md) remain suitable foundations. This method concentrates on their connected engine-to-client execution and inspection decisions. [dot-stack](../dot-stack/SKILL.md) supplies general engineering boundaries; its [runtime forensics](../dot-stack/pack/skills/dot-mode/playbooks/runtime-forensics.md) and [trace forensics](../dot-stack/pack/skills/dot-mode/playbooks/trace-forensics.md) own program diagnosis. [Language-server development](../develop-language-server/SKILL.md) owns document services; do not transfer its document synchronization or position-negotiation rules into a debugger protocol.
