---
name: reconcile-obsolete-ui-requests
description: "Diagnose and fix stale asynchronous UI results after edits, cancellation, navigation or repeated requests, with deterministic race-order tests and evidence of the current result's ownership."
---

# Reconcile Obsolete UI Requests

## When to use

Use this when an interface shows old data after the user changes an input, an earlier failure replaces a newer success, or Cancel leaves an actionable result associated with the wrong request. The task is to establish which request owns the current view and prevent obsolete completions from changing it. It applies to local files, public data retrieval, decoding and background computation as well as network requests.

## Required inputs

- The request-start, success, failure and cleanup paths
- All controls that change the request identity or dismiss its result
- The output actions that consume a result, such as export, playback or submit
- A test harness capable of controlling promise resolution and rejection order
- The scope of authorized edits and any external effects the operation can create

If a live operation can charge, publish or create a record, separate display cancellation from server-side cancellation. An aborted browser request does not prove the server did nothing; reconcile external state through an authorized read before retrying that mutation.

## Workflow

1. **Define request identity.** List the inputs that determine the result: resource, version, filters, selected file and mode as appropriate. State which user actions supersede it. A new request, changed input, loaded example, Cancel and component disposal may all invalidate the previous result.
2. **Map result consumers.** Find every place that stores data or enables dependent controls. Export should consume the same validated result shown on screen, not a separate stale cache or newly edited input fields. Clear or visibly mark results stale when inputs change; disable consequential consumers until a current result exists.
3. **Assign ownership at start.** Use a monotonically increasing generation or equivalent unique request token. Capture it before awaiting. Keep cancellation handles request-local so an old completion cannot cancel a newer operation. Increment the generation on every superseding action, not only on the next fetch.
4. **Use cancellation to release resources.** Abort supported fetches, terminate workers or cancel readers when appropriate. Keep the ownership check even when cancellation exists: some work may finish before the cancellation is processed, and test doubles or decoders may not support abort. Cancellation and stale-result suppression solve different problems.
5. **Guard every completion path.** Success, failure, progress and finally/cleanup must check that they still own the view before changing shared state. A guarded success with an unguarded catch can still replace a newer result with an old error. A stale finally must not clear the newer loading indicator or disable its Cancel button.
6. **Handle multi-part requests as one result.** For a comparison requiring two inputs, commit only when both belong to the same generation and have passed identity/shape checks. If either fails, cancel remaining work where supported and avoid displaying a new half beside an old half. Partial results are acceptable only when explicitly designed and labeled as partial.
7. **Bound work and preserve context.** Apply a deadline and response or computation size limits appropriate to the task. Show the current resource identity, observation time and a concrete error. Differentiate an explicit cancel from a timeout if the interface promises that distinction. Do not retain a successful-looking previous result behind a failed current request.
8. **Prove race behavior deterministically.** Use deferred promises rather than sleeping and hoping for a race. Start request A, supersede it with B, then resolve B before A. Repeat with A rejecting, with Cancel, and with an input edit that starts no replacement request. Assert both displayed state and dependent controls after each completion. Finally test the normal success/error paths and recovery from an invalid input.

## Worked example

A release comparison view needs manifests for old and new exact versions. Generation 7 starts requests A1 and A2. The user loads a synthetic example, advancing to generation 8 and enabling export for that example.

Resolve A1 and A2 after the example has loaded. Neither result may replace the example. Reject A2 instead: the old failure must not replace the example's status with an error. When generation 7 reaches finally, it must not change controls owned by generation 8.

A deterministic test can hold two resolver functions returned by a mock fetch, invoke the example action, then resolve the old requests. The observable checks are: the example is still labeled synthetic, the exported JSON is still the example, and no late “live data loaded” message appears. This verifies ownership, not actual network cancellation.

For a separate Cancel test, start a request, invoke Cancel, then resolve the obsolete promise. The view remains empty or explicitly canceled and export remains disabled. A subsequent valid request must still complete normally.

## Verification matrix

- A succeeds after B succeeds: B remains visible
- A fails after B succeeds: B's success and export remain intact
- A finishes after an edit without B: stale actions remain disabled
- A finishes after Cancel or unmount: no result is committed
- One half of a comparison fails: no unlabeled mixed-generation result
- Old finally runs during B: B's loading/cancel state remains correct
- Current request fails or exceeds a limit: concrete error and recoverable controls

## Deliverable and limits

Return the affected request paths, ownership/invalidation changes, the exact race orders tested and any unverified behavior. Record which operation is canceled and which effects are merely hidden. Passing mocked lifecycle tests does not verify actual transport cancellation, browser layout, production side effects or backend idempotency. Do not expand a UI fix into a service retry policy without a separately established scope.
