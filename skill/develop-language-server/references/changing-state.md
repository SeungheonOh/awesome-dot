# Changing and deferred state

Read only the section needed by the requested change. Full synchronization and immediate analysis remain appropriate when they satisfy the consumer's needs.

## Incremental synchronization

Treat a notification's changes as an ordered replay. Given state S, apply the first change to obtain S′, then interpret the next range against S′. Process notifications in received order; the notification's document version describes the state after all its changes. A whole-document event replaces the content. See [didChange](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#textDocument_didChange).

Convert incoming ranges using the negotiated units and the current intermediate text. Update the line map or invalidate cached offsets after each effect that changes their meaning. Validate enough before publishing the resulting state that malformed input cannot leave text, version and analysis describing different documents. If synchronization becomes unusable, choose a supported recovery or failure behavior; do not quietly continue analysis against a guessed buffer or invent a standard full-resync request.

Select a distinguishing replay: an earlier insertion changes length or line structure and a later change addresses the resulting location. Compare the reconstructed text with the client's complete buffer. Include the relevant Unicode and newline boundary. A sequence of edits whose coordinates accidentally fit both the original and updated text cannot establish replay semantics.

Incremental transport does not require incremental parsing. Reanalysis of the final text may be simpler and sufficient. If introducing incremental analysis, show that cache/dependency invalidation preserves the useful result. Measure performance when a performance problem motivates the work or a performance claim is made; do not infer correctness or improved performance from receiving small changes.

## Work that outlives its starting state

Bind deferred analysis to a stable input snapshot. Include the actual dependencies that determine its result, such as document lifetime, text version and project configuration. Separate independent documents' ownership. Choose a single writer, serialized commit or other real synchronization mechanism if workers share mutable state; a convention to avoid overlap is insufficient.

Use an internal generation or equivalent identity only when retained work can cross a superseding change, close/reopen or session boundary. Guard relevant publication, failure and cleanup paths so old work cannot overwrite the new owner's state. Cancellation can save resources but does not establish ownership. These are implementation techniques, not new mandatory LSP fields.

Apply freshness by result type. The server owns push diagnostic replacement and should prevent obsolete work from republishing a superseded set. A client may ignore diagnostic versions unless it advertises `versionSupport`; do not make that your only guard. Requests differ: the client can sometimes still use or transform an older result. Preserve processing order where it affects correctness, and do not return `ContentModified` simply because another change notification is waiting. A relevant internal project-context change can invalidate a request under the protocol's rules. See [message ordering](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#messageOrdering) and [implementation considerations](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#implementationConsiderations).

When supporting cancellation, keep request identity distinct from document version and still complete the request with a response. Do not leave it hanging because a cancellation notification arrived. See [cancellation](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#cancelRequest).

Control completion order in checks rather than hoping for a race: let newer work finish before older work and observe the actual published result, including old failures or cleanup when relevant. Check a close/reopen boundary if work can survive it. Preserve request results according to the feature and client contract, rather than copying a UI's blanket stale-display rule into every server handler.

## Project sources and dependencies

Establish which sources own definitions and which parts of the authorized project are included. Overlay open client buffers on disk-backed project data; a file watcher must not replace unsaved text. A closed document may return to URI-backed authority, but reading that URI or expanding a workspace still needs to fall within the actual task and implementation scope.

Keep enough dependency identity to invalidate affected analyses when declarations, configuration or included source change. A document version alone cannot identify an entire project snapshot. A failed dependency load must not become an empty authoritative symbol set that manufactures missing-reference diagnostics. Preserve usable facts and report the unsupported or incomplete boundary honestly.

Choose how close, deletion, rename and project removal affect retained results only for events the service supports. Demonstrate the consequence through a real affected use: change a declaration or configuration, then observe navigation or diagnostics in the dependent document. A cache hit counter alone does not prove correct project behavior.

## Maintain capability combinations

Read the relevant old client and initialization exchange before changing synchronization, position encodings or result shapes. Retain the original consumer unchanged when compatibility is promised; add a separate consumer or profile for the new behavior. Test the supported combinations that can actually disagree, not every theoretical capability permutation.

For an added position encoding, use text whose UTF-8 and UTF-16 columns differ and confirm the same semantic target in each selected mode. Keep omitted-capability UTF-16 behavior working. For an edit capability, check both the new application's result and the intended behavior when the capability is absent. A newer library release or a successful initialize response establishes neither relationship.

Keep evidence tied to the changed server and the actual consumers. A core test can explain a conversion or ownership decision; only the client's use or application establishes that the corresponding boundary works. State unexercised editor, installation and project-scale behavior separately.
