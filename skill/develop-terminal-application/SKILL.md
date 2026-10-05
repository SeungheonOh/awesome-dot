---
name: develop-terminal-application
description: Build or maintain an interactive terminal application around a useful session, stable task state, focused input, terminal ownership and a correct saved or returned result. Use for sustained terminal interaction; ordinary command invocation and shell completion have separate workflows.
---

# Develop a terminal application

Carry one real task from entry through interaction to the result its caller can use. Native terminal facilities provide the mechanics; the application decides what a selection, edit, completion or cancellation means. Keep those meanings consistent across the model, controls, terminal session and saved effects.

## Choose the useful session

Read the request, project instructions, existing entry points and a real result consumer when available. Identify what the person needs to inspect or change repeatedly, and what completes their work. Use an existing command, prompt or dialog when it suffices. A sustained session can help when choices depend on inspecting or revising shared state; full-screen mode is still a layout choice, not the definition of a terminal application.

Settle the consequential contract in the project's existing notes or tests: starting inputs, relevant identities, allowed actions, completion and cancellation, returned data or saved destination, and meanings of process status. Distinguish producing a valid result from the business condition it reports. A caller may reject a correctly produced report. Do not make the screen's success message the only evidence of completion.

For maintenance, trace the affected input through its actual handler, state and consumer before editing. Preserve user changes, established noninteractive calls and their dependency promises. A separate optional terminal adapter may fit an existing tool better than making every batch caller import a UI framework. Use the chosen runtime and available native facilities; inspect version-specific behavior rather than assuming current online documentation matches the installed version.

## Keep task state independent of its view

Resolve actions through domain identity, not a displayed label, row number or cursor position. Preserve distinct occurrences when repeated values are meaningful. Maintain the mapping from visible rows to those identities as filtering, sorting or wrapping changes the view. When the selected item disappears, choose and show the resulting selection or absence of selection before another action can affect it. Focus identifies the control receiving input; selection identifies the task object. They need not move together.

Separate only the states the task actually has:

- The editable draft, which may be incomplete or invalid
- Accepted domain values and any result computed from them
- The state actually saved or returned successfully

A small application can hold these in ordinary fields. No reducer, event bus or history framework is required. Bind a draft to its target and settle what switching targets, accepting, cancelling and quitting retain or discard. A live-validating editor may accept each valid change; a form may wait for an explicit action. Make that choice visible and prevent one target's draft from being saved to another.

Validate according to the domain, preserving valid zero, false or empty values. Decide whether invalid or unaccepted text blocks completion or leaves an explicitly identified accepted result available. Never silently label an old result as the current draft. Recompute or invalidate derived output when its inputs change. A navigation filter changes the saved population only when that is the declared task; otherwise save from the complete relevant model.

Update the saved reference only after the real save succeeds. Cancelling later edits does not reverse an earlier save. If undo/redo is requested, first use the editor's existing facility and define which accepted edits it covers; `implement-edit-history` develops that separate concern when available.

## Connect native controls to allowed actions

Compose the framework's text buffers, controls, layout, focus and key dispatch. Keep domain operations callable without screen coordinates, and let handlers translate focused input into those operations. The [prompt_toolkit application guide](https://python-prompt-toolkit.readthedocs.io/en/stable/pages/full_screen_apps.html) illustrates native controls, layout and simpler prompt/dialog alternatives; it is one framework option, not a required dependency.

Scope navigation and action bindings to the active control or mode. Preserve normal text entry and editing; a printable quit shortcut must not consume that character in an editable field. Decide what Enter and Escape mean in each relevant context, including where focus returns after an error or overlay. Keep action availability, feedback and the handler's own checks consistent. Use native [conditional key bindings](https://python-prompt-toolkit.readthedocs.io/en/stable/pages/advanced_topics/key_bindings.html) or the chosen framework's equivalent rather than a second input parser.

Make the current target, focused control, completion action and recovery route understandable in the interface. Show useful correction messages without losing the draft. Use the framework's text and formatting APIs deliberately so data is displayed as data. Keep rendering decisions out of stored values.

When size or lengthy content affects the task, choose wrapping, scrolling, a compact layout or a clear minimum-size state that preserves work and leaves a way to proceed or exit. Keep logical selection stable during reflow. Use native measurement and layout; string length is not terminal cell width. If a promise depends on particular Unicode text, inspect that text in the intended terminal and font. [Unicode's width specification](https://www.unicode.org/reports/tr11/) itself requires terminal-specific tailoring; a width calculation alone is not visual proof.

## Give the session one terminal owner

Use the framework's entry, exit and cleanup facilities for input modes, redraw and cursor/screen state. Python's [curses wrapper](https://docs.python.org/3.12/library/curses.html#curses.wrapper) is another native lifecycle option. Avoid a competing raw-mode or rendering layer, and do not change global shell or terminal settings to make a shortcut work.

Keep other writers from corrupting the active display. Route progress and errors through the UI, defer them until exit, or use a supported temporary handoff such as [prompt_toolkit's run_in_terminal](https://python-prompt-toolkit.readthedocs.io/en/stable/pages/reference.html#prompt_toolkit.application.run_in_terminal). Sending a debug print to stderr is insufficient when stderr shares the same terminal. Coordinate an external command through that owner if the task requires one.

Define how the interactive entry point behaves when its required input or output terminal is absent. Choose a supported noninteractive path, explicit I/O routing, or a clear early error; do not silently send screen updates into a machine-result stream. Keep ordinary CLI output, diagnostics and statuses consistent with existing callers.

Provide a reachable normal exit and the relevant cancellation/error paths through the lifecycle owner. Cleanup covers resources this run owns. Add paste, mouse, suspend/resume, asynchronous work or special interruption handling only when the actual experience needs it. For background work, use the framework's scheduling facilities, keep the interface responsive, and bind results or save completion to the target and revision they belong to. A late completion must not replace a newer draft or mark unrelated work saved.

## Finish the actual result

Connect completion to the agreed target, accepted values and population. Return the promised value or perform the real save; a preview is not the result unless that was the task. Preserve the established schema, ordering, occurrence identity and exit meanings used by downstream callers.

If saving promises replacement of a complete file, finish and validate a private staged result on the destination filesystem, close it successfully, then publish with the appropriate replacement operation. Preserve the prior destination on failures before publication and remove only owned staging resources. Python's [os.replace contract](https://docs.python.org/3.12/library/os.html#os.replace) is one runtime example; a single-path replacement does not establish multi-file transactions, concurrent-writer safety or crash durability. Use the storage system's own semantics when those are required.

A failure after publication may leave the new result saved. Report the state reached and inspect an uncertain effect before retrying. Caller-owned shell redirection can truncate a destination before the application starts; delayed output does not protect it. Deeper argument, stream and delivery design belongs to the command-line workflow, while this session must still deliver the correct complete effect.

## Verify the layer you changed

Choose a small task sequence with independent expected results that distinguishes the intended behavior from a plausible mistake. Drive the real entry point through the relevant controls, complete the task, and reopen or consume its actual result. Include the nearest consequential recovery or cancellation and a nearby existing caller during maintenance. Select cases from the changed promises rather than testing every input, signal, size and platform mechanically.

Use existing tests and drivers where they fit, with owned processes and data. Keep these evidence boundaries clear:

- **Model checks** establish the exercised identities, transitions and result values, not that keys reach them
- **Framework input** exercises decoding and bindings; non-rendering output cannot establish visible layout or terminal restoration. The [prompt_toolkit testing guide](https://python-prompt-toolkit.readthedocs.io/en/stable/pages/advanced_topics/unit_testing.html) explicitly uses this approach
- **An owned PTY** exercises the real process under its recorded terminal conditions. To support a restoration claim, compare relevant attributes on that same tty and check that its caller can continue normally after the exercised exit. Captured bytes or a screen model do not establish emulator pixels
- **An observed terminal surface** supports visible focus, clipping and layout claims for the actions and actual dimensions inspected. Changing a child tty's reported size alone is not a visible window-resize check
- **The real consumer** establishes that the saved or returned result is usable. It does not prove an interactive path that was bypassed to create that result

Use the evidence needed for the claim; a tiny prompt or model repair does not require every layer. If visual inspection or another required capability is unavailable, finish the supported checks and identify the remaining gap. Source cleanup code, static wiring and old passing runs are not fresh execution evidence.

After a repair, rerun affected checks on the final files and preserve a useful distinguishing failure when available. If packaged delivery is requested, exercise the installed public entry point and the same meaningful task outside the source tree; a source-only request needs no installation project. Report the usable entry point, consequential session/result choices, checks actually performed and material limits. Do not infer other terminals, operating systems or accessibility behavior from one successful environment.

This method integrates responsibilities already handled by `design-user-interface`, `implement-scoped-change`, ordinary command-line development and project verification recipes. They remain useful for deeper work in their scopes; using this terminal method does not require a chain of separately installed skills.
