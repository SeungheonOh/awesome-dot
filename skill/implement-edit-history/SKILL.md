---
name: implement-edit-history
description: Add or repair session undo and redo in an editable application or component. Define logical edit units, retained state, grouping, redo branches, restored context and saved-state meaning, then verify the real editing path. Use for local edit history rather than backup recovery, version reconciliation or distributed undo.
---

# Implement Edit History

Give a person a reliable way to reverse and reapply accepted edits. The result is working history in the actual editor or component, with understandable action boundaries and restoration behavior. A stack of values or two enabled buttons is insufficient if another editing path bypasses it.

Use this workflow when edit-history behavior is the substantive change. General project integration belongs with `implement-scoped-change`, interaction design with `design-user-interface`, and verification with `write-behavior-tests`. Reconcile competing document versions with `document-revision-reconciliation`; recover saved files with `backup-restore-spot-check`. Collaborative undo, remote compensation and durable event sourcing require their own concurrency, authority and effect contracts. Do not extend a local history mechanism to them by assumption.

## Establish what one edit means

Read the request, actual editing entry points and existing state/history facilities. Trace a normal edit from the caller through validation, model mutation, derived output and any save marker. Check whether the framework already owns undo or records native text changes. Prefer a supported existing facility when it can express the accepted semantics; avoid creating a second competing history for the same content.

Settle the decisions that change observable behavior:

- **Scope:** which document or component owns history, which changes it covers, and what happens on opening, replacing or closing that document
- **Unit:** whether one command, drag, text-input run or explicit compound action is one undo step
- **Restoration:** which content, ordering, identities and editing context must return, and which derived values should be recomputed
- **Boundaries:** what closes a group or typing run, what is a content no-op, and how a rejected or cancelled edit affects history
- **Saved state:** what clean/dirty means and which actual operation establishes the saved reference

Use concrete short sequences to expose ambiguous choices. For example, editing a title, moving selection and undoing can either restore the earlier selection or retain the current one. Neither policy follows from having an undo stack. Follow the existing contract or decide explicitly when design is delegated. Ask only when an unresolved choice materially affects the requested behavior; a small settled change does not need a separate specification ceremony.

Keep content, selection, focus, validation messages and durable storage distinct. A selection may be restored with a content edit without being independently undoable. A derived preview or success message may need invalidation rather than historical restoration. Do not report a session save marker as evidence that a file was written.

## Retain enough independent state

Choose a representation proportional to the editable model and its lifetime. Independent before/after snapshots are often clear for small state. Commands with retained inverse data, patches or persistent data structures may suit larger models. Use the application's existing architecture rather than choosing one representation universally.

Capture enough information to reverse the actual accepted edit. Deleting an item may require its stable identity, complete content, original position and relevant selection; changing a reference may require both old and new targets. For text, preserve the declared position convention, such as code points or code units, rather than mixing it with displayed characters. An inverse cannot recover information that the forward operation discarded without retaining it.

Keep retained entries independent from later mutation. Copy or immutably own nested data as needed; protecting only the outer object does not protect its arrays or children. Caller-owned arguments and returned views must not let later changes rewrite history. Redo should reproduce the accepted result, including generated identities or other material choices, rather than accidentally creating a new random result or repeating an external effect.

Inspect the history facility's execution and ownership contract. Some stacks execute a command when it is pushed; others record an edit already applied. Applying it twice is a real integration bug. Qt's [undo framework overview](https://doc.qt.io/qt-6/qundo.html) describes a command-based implementation; its model is an available example, not a requirement to introduce Qt or command objects into every project.

## Separate new edits from traversal

Route every covered editing entry point through the chosen owner. Include programmatic operations that alter the same content, such as paste, reset or a bulk action, when they are in scope. If an external replacement cannot be reconciled with retained history, define an explicit boundary or invalidation policy instead of leaving entries that refer to a different document.

A new accepted content edit, undo and redo are different transitions. Restoring an entry must not recursively record itself as a fresh edit through the same observer or callback. Preserve the notifications and derived-state updates the application still needs; suppressing all observers can hide a broken consumer.

For ordinary linear history, a genuine new edit after undo abandons the redo future. Discard that future only when the new edit is accepted under the chosen contract. An invalid operation, a read or a content no-op should not accidentally destroy it. Handle any legitimate context-only effect of a no-op separately from whether it creates an entry. If the application deliberately supports branching history, keep that different contract explicit.

Make unavailable undo/redo behavior and availability indicators agree with actual retained entries. Restore the recorded editing context when promised, including after intervening navigation. Keep each document's history attached to that document; switching the active view must not send an undo action to an unrelated model.

## Group and merge only compatible actions

An explicit compound action and incremental coalescing solve different problems. A compound action may apply several distinct changes but reverse as one unit. Coalescing may compress adjacent low-level edits, such as typed insertions, into one meaningful action. Add either only when the requested experience needs it.

Define grouping boundaries from real interaction or command semantics. Consider changes of target, selection, edit kind, focus, composition session, explicit completion, save and history traversal as applicable. Time proximity alone does not prove that edits belong together. Test any timing or input-method behavior in the actual consumer before claiming it works.

A merged entry must undo to the state before its first constituent and redo to the final accepted state. Updating only its label or last delta can lose the earlier inverse. Preserve the required before/after context and identity. Do not merge across a boundary whose intermediate state must remain reachable, such as a separately marked saved revision. Qt's [command documentation](https://doc.qt.io/qt-6/qundocommand.html#mergeWith) states the equivalent forward/reverse behavior required of a merged command; the particular merge eligibility remains the application's decision.

If the request promises all-or-nothing compound edits, make failure atomic for both the model and history. Stage and validate a candidate, or use another proven rollback mechanism appropriate to the model. A framework macro groups history entries but does not by itself establish rollback for a failed member. Check a failure after an earlier member has succeeded. Keep the clean reference and prior redo future intact when the contract requires rejection without change.

Treat an aggregate no-op according to the accepted equality rule, including any retained selection effect. Do not manufacture a useful-looking history entry for a change that did not happen. Conversely, do not erase meaningful order, duplicate occurrences or metadata merely to classify an edit as equal.

## Preserve saved-state and retention semantics

Dirty state may compare current content with saved content, or it may track a saved revision/history identity. Those policies differ when new edits recreate identical content. Preserve the intended one. A mutable stack index reused after branching or pruning is not a stable saved-revision identity. If revisions are issued, traversal may restore an older identity while a genuinely new edit still receives a new one.

Keep the saved reference separate from ordinary history unless the contract explicitly says otherwise. Undoing an edit should not silently undo the fact that a particular revision was saved. Update a real saved reference only at the established success point of the real save operation. For asynchronous saving, bind completion to the revision actually saved rather than blindly marking whatever is current as clean.

If retention is bounded, define what the limit counts and when eviction happens. A merged or compound unit may count once; a count limit is not a bound on bytes. Eviction must leave the current model and remaining traversal valid. Handle a saved state that is no longer reachable truthfully rather than marking an unrelated position clean. Do not add persistence, a history browser or unrequested limits to a small session feature.

## Verify the actual editing path

Derive a small sequence corpus from the request and independent expected states. Check full observable content and material context, not just stack lengths. Exercise the public API or real command path, and the UI controls when interactive behavior is part of the task and an authorized consumer is available.

Useful checks, selected for the actual feature, include:

- Several edits followed by multiple undo and redo operations, with exact content and context restoration
- Undo followed by a real new edit, and separately by a no-op, observation or failure
- A compound success and a later-member failure; a merged run and a boundary that must split it
- Save, edit and traversal around the saved state, including the chosen equal-content or revision-identity distinction
- Removal and restoration of meaningful identities/order, mutable caller data, and the retention boundary when implemented

Verify existing editing behavior through its real caller as well. A helper test does not prove that an actual keyboard command, menu action or native editor uses it. Separate model/CLI checks, rendered UI inspection and exercised interaction; report an unavailable consumer specifically rather than treating static wiring as execution. Preserve a useful failing sequence when a check exposes a defect, repair the relevant path and rerun the affected checks on the final files.

Deliver the working change with a concise explanation of history units, important boundaries, verified behavior and remaining limits. Keep evidence proportional to the request. Do not require a separate ledger, generalized framework or extensive test package for every small history repair.
