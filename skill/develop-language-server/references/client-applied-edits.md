# Client-applied edits

Read this when a language feature returns changes to source. Keep the analysis, proposed edit and observed application connected to the same document assumptions.

## Establish a justified transformation

Resolve the intended symbol and supported scope before constructing replacement text. A same-spelled occurrence is not necessarily the same binding. Validate the requested new form and relevant collisions; preserve unrelated source, comments and line endings according to the accepted transformation. Use the language service or existing migration mechanism that owns those semantics. Correct LSP packaging does not prove rewrite correctness.

For rename, invalid new names require an error response. A null rename result means no changes, not successful mutation or an unexplained validation failure. Decide the supported scope honestly rather than advertising a project-wide result from a single incomplete declaration set. See [rename](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#textDocument_rename).

## Construct edits against one original snapshot

All ordinary edits in one `TextEdit[]` address the document before that edit set. They do not describe successive intermediate buffers. Convert every span using that snapshot and the negotiated position encoding, detect overlap, and preserve the specified ordering when insertions share a start position. Same-position inserts may precede one remove/replace; their array order determines the inserted text order. Do not blindly reorder them with a generic sort. See [TextEdit arrays](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#textEditArray).

This differs from incoming `didChange` events, whose ranges address successive states. A client-side applicator can build new text from the original spans or apply carefully ordered replacements, but it must implement the same-snapshot semantics. Check the complete resulting text, not only the number of edits.

Choose a `WorkspaceEdit` form supported by the client. `workspace.workspaceEdit.documentChanges` permits versioned `TextDocumentEdit` entries; use the analyzed open document's version when the feature depends on that precondition. Plain `changes` cannot carry that version. If the implementation requires version checks and the client lacks this capability, choose an honest unsupported-feature behavior instead of silently removing the check. LSP does not universally require versioned rename. See [WorkspaceEdit capabilities](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#workspaceEdit) and [TextDocumentEdit](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#textDocumentEdit).

Do not substitute a null version for an unknown open-buffer version. The optional-version identifier's null case concerns a document whose authoritative content is on disk; see [versioned identifiers](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#optionalVersionedTextDocumentIdentifier). Resource operations, annotations and snippet edits have additional capability requirements; include them only if the feature uses them. Several entries do not by themselves promise atomic application: the client's supported failure-handling strategy controls partial outcomes. These choices belong to the [WorkspaceEdit capability contract](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#workspaceEditClientCapabilities).

## Observe application at the owner

Returning a `WorkspaceEdit` from rename lets the client perform the change. Do not mutate the server's mirror as though the proposal was accepted. Let subsequent synchronization establish the resulting open content. For the separate server-initiated `workspace/applyEdit` route, check `workspace.applyEdit` and inspect its `applied` result and any reported failure; sending the request does not confirm success. See [applyEdit](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.18/specification/#workspace_applyEdit).

Use the actual consumer's application path. In a controlled client, retain the request's buffer identity and lifetime and check the edit preconditions at application time. A document changed since the request may require declining the proposal or an explicitly justified transformation; never overwrite newer text by accident. A reopened document must not inherit a pending edit merely because the URI and numeric version match again. Standard request IDs and document versions do not add a wire-level open-lifetime identifier for you.

Exercise a meaningful supported edit; when the feature supports multiple length-changing replacements, use such a case to expose shifted-offset mistakes. Read back the client's complete text, synchronize its actual result, and obtain a useful new language result. Where version/lifetime protection is promised, hold a received proposal, change or reopen the client buffer, then attempt application and inspect preservation of the newer text. That boundary can be controlled without asynchronous server analysis or timing sleeps. Keep invalid/colliding requests distinguishable from valid no-op results.

Report separately what was proposed, what the consumer applied or declined, and what subsequent synchronization established. A native applicator does not establish editor undo behavior, multi-file transactional guarantees or compatibility with an unexercised editor.
