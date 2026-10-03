---
name: implement-scoped-change
description: "Implement an accepted behavior request in a chosen software project, including a bounded new component, and verify the actual result. Use for scoped software implementation rather than requirements discovery, interface design, website creation, repository mapping, or integrating finished changes."
---

# Implement a Scoped Change

Turn a requested behavior into working software in the authorized project. Success is the requested observable result, supported by relevant checks on the final files; a plausible patch or a passing helper test alone is insufficient.

## Establish the behavior and working boundary

Read the request and applicable project instructions. Establish the chosen project or workspace and component, the observable acceptance behavior, any compatibility constraints, and the permitted environment. Use the project's existing tools and conventions rather than introducing a preferred stack or workflow.

For a bounded new component, the accepted requirements or contract can be the starting point; an existing implementation or Git repository is not required. Inspect the chosen location and preserve anything already there. Create only the structure and tooling needed for the requested result, honoring the selected language and runtime. If the behavior or public interface still needs to be decided, resolve that design work before implementing assumptions as settled requirements.

Make the acceptance behavior concrete enough to distinguish success from a nearby wrong implementation: what input or action triggers the change, what output or state should result, and what existing behavior must still hold. For a small clear task, keep this in a short working note and proceed. Do not require a design document or another approval of the same request.

- **Missing detail:** Infer reversible implementation choices from nearby patterns. Ask when plausible interpretations would produce materially different user behavior or interfaces. State the unresolved choice and continue independent work that will remain useful under either answer.
- **Conflicting evidence:** Compare the user's requirement, the applicable specification, and current tests. An explicit request to change behavior may intentionally supersede old tests; update those expectations with that reason. If intent remains incompatible or unclear, show a concrete input on which the alternatives differ and ask for that decision. Do not choose intent merely to get a green test.
- **Unclear scope:** Separate behavior required for acceptance from optional cleanup. Proceed with necessary adjacent edits that fit the request; hold work that introduces a new product decision, external action, or materially broader contract.

Inspect the project's current files before editing; in a Git repository, include staged, unstaged, and untracked work. Read existing changes in files you need to touch so they can survive the implementation. Do not discard or hide them to obtain a convenient baseline. An isolated branch or worktree can help when it preserves the original work and includes the correct inputs; a clean checkout that omits required uncommitted changes is not an equivalent starting point. Unrelated dirty work is not itself a blocker. If edits overlap so closely that ownership or intent cannot be distinguished, pause that edit and describe the conflict. Re-read a file before applying a patch when concurrent changes are possible.

Follow the user's and project's established conventions for local commits. Publishing, deployment, installation outside the local task environment, and changes to shared systems require the authority appropriate to those actions; reuse existing authorization without adding a redundant confirmation step.

## Find the smallest complete code path

Start from the actual entry point or consumer for the requested behavior, then follow its relevant calls, state, and output. For a new component, use the accepted caller contract to establish that path. Inspect nearby tests and a comparable implementation when they exist. Read enough to decide where the behavior belongs without turning the task into a full repository survey.

Identify the constraint that most affects the implementation: an existing interface, caller assumption, validation boundary, persistence format, or generation step. Check both producer and consumer when changing a data shape or default. Distinguish editable source from generated output; use the established generator when regeneration is necessary and permitted.

Choose a change that reaches the real feature path. A new utility does not fulfill the request until the intended caller uses it; a UI control must reach its actual handler and state; a stored value must still be read correctly. Prefer an existing extension point or local pattern to a new abstraction unless the current structure cannot express the required behavior cleanly.

Select useful checks now so their results can influence the implementation. Derive commands from project configuration and instructions, including their working directory and prerequisites. When effects are unclear, inspect invoked scripts and test setup before execution. Use an existing focused baseline when it helps distinguish a regression; running the entire suite before every small edit is unnecessary.

## Implement the behavior

Make the smallest coherent change, including the necessary caller, configuration, test, and documentation updates. Minimize unrelated churn rather than merely minimizing line count: a tiny special case that bypasses the established contract can be worse than a slightly broader, consistent change.

- Keep error handling, naming, dependencies, and data ownership consistent with the surrounding code. Avoid unrelated refactors, formatting, dependency upgrades, or new configuration switches.
- Add or adjust tests when they protect changed behavior or a meaningful boundary. Assert observable results and relevant invariants, not the chosen helper structure. Use existing coverage or a direct check for trivial changes when a new test adds no useful protection. Follow a required project testing practice, but do not impose a universal test-first ritual.
- Exercise the consequence most likely to be missed: an unchanged default, an empty value, a repeated operation, or a failing dependency, as relevant to this change. Do not add every category mechanically.
- If the implementation exposes a necessary migration, public interface break, or wider redesign, explain why acceptance depends on it and resolve the missing decision or authority. Preserve useful work already done; do not silently expand the assignment or ship an incomplete substitute as complete.

Review the patch while editing. Every changed region should contribute to acceptance or required verification. Preserve pre-existing changes and remove only accidental changes you introduced and can safely identify.

## Verify the actual final result

Run the focused checks that exercise the changed behavior, then applicable required project checks and adjacent checks justified by the affected contract. For interactive behavior, inspect it through the available application or browser when that is the meaningful validation. Compilation, static review, and unit tests support different claims; do not substitute one for evidence it cannot provide.

Keep verification proportional to the change and within the permitted environment. Do not run a command that would use live accounts, alter shared data, or deploy merely because it is named `test`. Use a supported local fixture or alternative when available; obtain missing authorization only for the specific consequential step that is needed.

Handle results according to what they establish:

- **Failure caused by the change:** Fix it within scope and rerun the affected checks. Do not weaken assertions, suppress errors, or skip coverage to obtain a pass.
- **Possibly pre-existing failure:** Compare the diagnostic with a recorded baseline or inspect the affected path. Label it pre-existing only with evidence; otherwise report the cause as unresolved. Avoid reverting user work just to manufacture a clean comparison.
- **Unavailable check:** Resolve routine setup issues already within scope. If a tool, dependency, service, credential, or permission remains unavailable, record the blocked command and reason. Perform other meaningful checks, and state the behavior they leave unverified. A static inspection or miniature substitute is not a passing run of the real application.

Inspect the final changes and project state, including files generated by checks; use the diff and repository status when available. Verify that the feature is connected, required companion changes are present, and unrelated user work remains intact. Results must apply to the final relevant files: after a later edit, rerun the checks it could affect. Distinguish passed, failed, blocked, and not run; timeouts and partial runs are not passes. Stop after acceptance and the justified available checks are complete, or at a concrete blocker, rather than repeatedly running unchanged checks.

## Hand off the result

Lead with what behavior now works and where to find the change. Briefly include:

- The implementation choice or tradeoff that matters to understanding it
- Checks actually run, their commands or direct observations, and outcomes
- Any acceptance behavior still incomplete, blocked check, or unresolved risk, with the smallest next step

Use source links where useful. Distinguish the local implementation from any separately requested commit, remote CI run, or release, and claim each only when verified. A partially verified change can still be useful; describe its limits instead of declaring the entire task complete.
