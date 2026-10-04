---
name: instrument-application
description: Add or repair useful application logs, metrics or timing traces by defining what the observations mean, placing them at the right lifecycle boundaries and checking the actual emitted output without changing business behavior. Use for producing diagnostic signals in application code; analyzing supplied telemetry or diagnosing an existing capture has a different outcome.
---

# Instrument Application Behavior

Deliver the requested instrumentation in the actual application, with enough observed output to show that a maintainer can answer the intended question. A logger call or a valid telemetry schema alone does not establish useful instrumentation. Keep a design-only request as a proposed observation contract and placement plan; do not silently turn it into implementation.

Use the project's existing logging, metrics, tracing and testing capabilities when they fit. A small local command can need only one structured report. Do not introduce a collector, service, dashboard, background worker or all three signal types by default. Existing implementation guidance still owns the ordinary code change; this method supplies the observation decisions.

## Start with the question and the observed unit

Read the relevant public entry point, business operation, error paths and existing instrumentation. Identify what the maintainer needs to distinguish: work received versus completed, retries versus new requests, time spent in a stage, concurrent work, or a missing terminal outcome. Define the useful answer before selecting fields or instruments.

Choose the observation unit and its lifecycle. One input occurrence, logical request, processing attempt, stored item and transport call can describe different populations. Decide what counts as a start, completion, rejection, failure or cancellation under the application's actual contract. A successful transport response can still carry a failed business result. Conversely, a failed attempt followed by a successful retry need not be a failed logical operation.

Keep the existing business contract explicit: return values, exceptions, exit status, persisted effects, retry policy, user-visible output and relevant timing constraints. Instrumentation should observe that behavior unless the user requested a behavioral change. Do not add retries, cancellation or new lifecycle states merely to exercise a generic checklist.

For a small change, a short field-and-meaning note is enough. Resolve a missing definition only when it changes the intended answer or a consequential implementation choice. Keep unresolved measurement meaning visible rather than choosing a familiar counter name and implying the question is settled.

## Choose signals and stable meanings

An event can record a particular fact, a metric can summarize a defined population, and a span can describe a timed operation and its relationships. Choose the smallest combination that answers the question. Reuse the application's established semantic conventions and the installed instrumentation version; avoid duplicating signals already emitted by a library or automatic integration.

Define names, units, outcome vocabulary, eligibility and aggregation together. Specify whether a total counts starts or terminal results, and whether a duration includes queueing, retry waits, failures or cleanup. A gauge of active work needs balanced lifecycle updates; a completion counter needs one increment at the owner of completion. A histogram needs meaningful units and boundaries for its intended question. Avoid adding an instrument whose interpretation is unknown.

Separate correlation from aggregation. Give a logical operation an identity in the correct run/process/request namespace; identify its attempts or child operations separately. Retrying within the same logical operation should preserve that relationship. Repeated identical inputs can still be different occurrences. Do not use filenames or caller labels as an accidental substitute for identity.

Keep metric dimensions bounded by the question, such as a finite operation kind and outcome. Unique request IDs, raw URLs, arbitrary exception strings or input contents can create a new series for each value. Put necessary correlation in the appropriate event/span context instead, and still apply the allowed-data policy. The [OpenTelemetry metrics documentation](https://opentelemetry.io/docs/concepts/signals/metrics/) explains how distinct attribute combinations affect aggregation state; its particular SDK limits are not a universal application budget.

Choose an explicit field allowlist. Prefer finite reason codes and approved context over copying whole input objects, exception messages or environment values. Formatting something as JSON does not make it appropriate to retain. Keep diagnostic output separate from a CLI's data stream or an application's machine protocol.

## Place observations at their real owners

Instrument the boundary that knows the fact being claimed. A wrapper may know a call began while a repository or worker owns durable completion. Do not report saved, delivered or successful merely because an intermediate function returned. When only an intermediate stage is observable, name that narrower fact.

Use elapsed-clock differences for durations, and distinguish them from human-readable event timestamps. A system clock adjustment should not create a negative elapsed duration. CPU time, wall time and queue residence answer different questions. Nested or overlapping durations are not independent values to add into total application time; record the endpoints and scope that support the interpretation.

For concurrent or asynchronous work, preserve parent and causal relationships deliberately. A shared mutable current-operation variable can attach one task's events to another. Use the runtime's supported context propagation or explicit context arguments, restore prior context when leaving a scope, and check error and cancellation exits. A later independent call must not inherit a completed operation accidentally. For example, Python's [context variables](https://docs.python.org/3/library/contextvars.html) provide task-compatible context and token-based restoration; available syntax still depends on the actual runtime version.

End each timed scope at the correct boundary and record its actual terminal outcome. Keep a child's failure distinct from the enclosing operation's eventual result. A detached task or a batch assembled from several causes may need an explicit link rather than an invented single parent. Do not keep a span open solely to make unrelated later work look nested.

## Contain observation costs and failures

Establish whether the records are optional diagnostics or a mandatory part of the business transaction. Their failure policies can differ. For optional diagnostics, observation or exporter failures should not replace the application's result, swallow its original error, cause business retries or leave unrelated work running. Keep observation-error handling narrow enough that it does not catch and misclassify business exceptions or cancellation.

Inspect construction, emission, buffering and finalization, including callbacks supplied by the instrumentation system. Prefer the existing provider/exporter lifecycle; a library should not unexpectedly replace global configuration or shut down a caller-owned provider. If a failure is suppressed, use a bounded, appropriate diagnostic status or warning when useful, without recursively invoking the same broken sink or leaking its payload.

The [OpenTelemetry error-handling specification](https://opentelemetry.io/docs/specs/otel/error-handling/) provides one concrete runtime failure-isolation contract, with separate initialization and explicit strict-handler behavior. It does not make every custom diagnostic format OpenTelemetry-compatible or decide a mandatory audit record's policy.

State the relevant resource behavior. A synchronous writer may delay return; a background queue needs a bound, overflow policy and owned shutdown; an in-memory run report grows with its retained records. Choose only what the actual task requires. A successful small run does not establish negligible overhead, arbitrary writer timeouts or crash durability. If overhead matters, measure matched work through the real application and separate diagnostic export cost from the measured business interval.

## Make incomplete observation recognizable

Record the scope and limitations needed to interpret the output: run identity, selected versus observed population, sampling or dropped-record behavior, and the meaning of any completion marker. Missing data is not an observed zero. A start without a terminal record remains unfinished or unobserved under the contract, rather than automatically failed or successful.

If detailed records are sampled or capped, do not reconstruct exact totals from that subset. Derive exact totals independently from the complete execution only when the implementation actually does so. Keep counter epochs, resets, aggregation windows and retained history clear where relevant; a local one-shot report does not need a monitoring framework.

For file output, preserve existing destinations as required and distinguish a partially written artifact from an accepted complete one. For an exporter, distinguish acceptance into a local queue from confirmed downstream receipt. An artifact written before process exit does not by itself prove later shutdown or delivery of buffered user output. Do not claim stronger completion than the producer can observe.

## Verify the application and the signal together

Exercise the actual requested boundary with instrumentation disabled and enabled, then inspect the saved or received observations. Compare the business results, errors and effects against the original contract. Use source-derived expected facts, rather than rebuilding the producer's counting logic inside its checker. Schema validation is useful but cannot establish that a signal was emitted at the right moment.

Choose the nearby cases that could disprove the proposed meaning: a retry when attempts and operations differ, an error that skips a normal return, overlapping calls when context is shared, or cancellation during a timed stage. Include an unavailable or failed observation sink when optional failure isolation is promised. Verify the concrete adapter or exported artifact as well as any callback seam. Keep faults local and bounded; an ordinary instrumentation task does not authorize a production disruption.

Reconcile identities, terminal outcomes, counts, units and relationships in the actual output. Check that protected payload fields are absent. If incomplete captures matter, retain one partial copy and show that its reader does not promote it to a complete successful run. A controlled clock can check duration boundaries; a real-clock example supports only its observed timing, not an exact scheduling guarantee.

Deliver the changed source/configuration and requested example or operational instructions, with a concise statement of what the observations mean and which checks ran. Keep detailed evidence proportional to the task. Separate implemented emission, local readback, real backend receipt and production coverage. A useful local result can be complete while an unrequested remote exporter or dashboard remains outside its scope.
