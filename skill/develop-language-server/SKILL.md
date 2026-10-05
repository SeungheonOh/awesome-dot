---
name: develop-language-server
description: Build or maintain an LSP language server around synchronized document snapshots, negotiated positions, and results the actual client can use. Use for language-service implementation and compatibility work, rather than a standalone source checker or editor installation.
---

# Develop a language server

Carry one document through its continuing lifetime: client-owned text, analysis of that snapshot, protocol coordinates, a feature result, and the client's use of it. Keep those relationships intact when the document changes. A collection of handlers that returns plausible JSON is not yet a useful language service.

## Choose one useful consumer path

Read the affected server, actual client or intended integration, project instructions, and existing language tooling. Establish the supported language and URI scope, synchronization mode, useful feature, open/closed behavior, and delivery boundary. Existing documentation and tests can hold these decisions; a separate contract format is unnecessary.

Reuse the project's suitable LSP library, compiler or language service. Check the protocol and library versions it actually supports before using a newer field. A small open-document service can be complete with full synchronization, synchronous analysis, diagnostics and navigation. Add incremental synchronization, background work, project indexing or edits only when the requested behavior needs them.

For maintenance, observe a meaningful existing client interaction before editing and identify the promise being changed. Preserve actual supported capability combinations, including omitted optional fields. LSP 3.x exchanges capabilities during initialization; it does not negotiate a protocol release number. Ignore unknown client capability properties while honoring mandatory baseline behavior. Advertise only the features and result forms the implementation can supply. See [initialization and capabilities](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#initialize).

## Make the document snapshot authoritative

Handle open, change and close together for editable documents. On open, use the supplied text and language ID; a file URI is not permission to replace an unsaved buffer with disk contents. Keep each document's text, version and derived analysis coherent. A full-text change replaces the text; process received changes in order and analyze the resulting snapshot. Versions increase on changes, including undo/redo, but need not be consecutive. See [document ownership](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#textDocument_didOpen) and [change semantics](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#textDocument_didChange).

Close ends the client's ownership of that open content. Decide whether the service then releases analysis or continues from an authorized file/project source. Closed documents are not universally unserviceable. Reopening the same URI starts a new open lifetime; do not let retained text or work from the old lifetime masquerade as the new one when versions are reused. A synchronous service that releases its state may need no extra generation field. See [close semantics](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#textDocument_didClose).

Feed analysis from that snapshot, retaining original source spans and the facts needed for the feature. Use the language's established binding/type model when meaning requires it; simple literal-reference formats need no parser framework. Keep unresolved relationships or failed analysis distinct from a successful empty result. Invalidate derived state when its inputs change. Read [changing and deferred state](references/changing-state.md) only for incremental changes, overlapping work, project dependencies, or a capability change that needs deeper treatment.

## Keep wire bytes and document positions separate

Use the selected transport's real framing. For LSP stdio, `Content-Length` counts the UTF-8 JSON body's bytes, not characters or document code units. Headers are ASCII and end with CRLF; the empty line separates headers from the body. Buffer partial frames and retain trailing frames across reads. Keep protocol stdout free of logs and handle malformed/truncated input according to an explicit implementation policy. Prefer the existing library's framing over another handwritten parser. See the [base protocol](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#baseProtocol).

Document positions use a separate session choice. UTF-16 is mandatory and is the default when position-encoding capabilities are absent. If supporting another encoding, select a supported client offer through `general.positionEncodings` and report `capabilities.positionEncoding`; use that choice in both incoming positions and outgoing ranges. UTF-8 positions count bytes within the line; UTF-16 positions count code units. Neither is generally the host language's string index. See [text document encodings](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#textDocuments).

Convert against the exact snapshot used by the analysis. Account for LF, CRLF and CR line separators, zero-based lines, and exclusive range ends. Represent a line ending by reaching the next line's start; a position cannot point into the middle of CRLF. Respect the protocol's rule that a character offset beyond the line clamps to its end. Exercise a non-BMP character before a meaningful range so code-point and UTF-16 counting cannot accidentally agree. See [Position](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#position) and [Range](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#range).

## Return the feature's actual meaning

For push diagnostics, publish a replacement set for the URI. Send an empty array when recomputation removes prior problems. `textDocument.publishDiagnostics.versionSupport` says whether the client interprets diagnostic versions; merely attaching a version cannot guarantee stale-result suppression. Choose close behavior from the service's source authority: open-document diagnostics may clear on close, while a project service may retain them. See [publishDiagnostics](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#textDocument_publishDiagnostics).

For navigation, resolve the requested position in its synchronized snapshot and return locations whose ranges select the intended source. Use a normal no-target result where appropriate; do not conceal analysis failure as no target. Respect result-shape capabilities, such as `textDocument.definition.linkSupport` before returning definition links. See [definition results](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#textDocument_definition). The client's ability to use a request result is separate from the server's responsibility for published diagnostics. A queued edit alone is not a universal reason to reject an earlier request; see [request usefulness](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#implementationConsiderations).

When implementing rename, formatting or another edit feature, read [client-applied edits](references/client-applied-edits.md). A returned edit is a proposal; correct ranges and valid JSON do not establish that a client applied it.

## Exercise the complete interaction

Run the saved server through the chosen consumer boundary. Initialize, receive its response, send `initialized`, synchronize the buffer, and use a nonempty feature result. A native protocol client can be a useful consumer when it owns its buffer and independently turns returned ranges into selections or changes. It must not call the server's own analysis or coordinate helper to manufacture the expected outcome. An actual editor is necessary only for claims about that editor's behavior.

Choose a short sequence that distinguishes the promised behavior: an unsaved buffer differing from disk, a meaningful edit that moves or repairs a result, and the relevant close/reopen boundary. Inspect the client's selected text or current problem view, including diagnostic replacement, against independent expected source. For a maintained server, retain a useful unchanged caller case. Check only the additional capability or lifecycle branches the change affects; do not build a universal test matrix.

Correlate responses by request ID, including successful null results; notifications receive no response. LSP uses separate framed messages, not JSON-RPC batch arrays. Finish the actual session: `shutdown` returns null before `exit` asks the process to stop. For an owned stdio child, drain outputs, observe exit status, and release that child. A sent notification or a parseable transcript does not establish completion. See [JSON-RPC request/response rules](https://www.jsonrpc.org/specification#request_object), [shutdown](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#shutdown) and [exit](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#exit).

Deliver the requested server changes, usable invocation/integration, supported capabilities, and observations tied to the final candidate. Distinguish core checks, actual protocol-client use, editor use and installed delivery. If only source invocation was requested, source evidence can complete the task. Preserve useful failed cases and investigate the observer as well as the server before changing an expected range.

## Existing method owners

This method reuses source-analysis and rewrite reasoning from `build-source-analysis-rule` and `build-source-migration`, consumer obligations from `design-api-contract`, and process semantics from `develop-command-line-tools`. `dot-stack` supplies boundary discipline and candidate-bound consumer verification; `reconcile-obsolete-ui-requests` supplies ownership reasoning for overlapping work. Use those methods when available and needed for depth. The document-to-client path above does not require loading the whole collection.
