---
name: write-technical-guide
description: Create or substantially update task-oriented technical documentation from an existing system, source code, API, or supported procedure. Use when the reader needs instructions, examples, or reference material they can actually apply.
---

# Write a Technical Guide

Produce documentation that lets its intended reader accomplish a task or use an interface correctly. Derive it from the actual behavior and supported workflow, then check the path the reader will follow. Do not turn source code into an unfiltered explanation of every implementation detail.

For a wording-only edit to an existing draft, use an editorial approach. For this skill, the central work is discovering and explaining the technical contract accurately.

## Choose the reader's task

Establish the intended reader, what they already know, what they want to accomplish, and where the guide will live. Use the request and existing documentation to infer ordinary choices. Ask when an unresolved audience, supported version, or target environment changes the instructions.

Choose a useful form:

- A how-to begins from a real starting state and ends with an observable result
- A reference explains the interface's inputs, outputs, defaults, constraints, and errors
- A troubleshooting guide branches on evidence a reader can observe
- An explanation gives the conceptual model needed to make a decision or understand behavior

A document can combine these, but keep the reader's main path clear. Do not bury the working procedure under history or require someone to read an entire reference before a simple first use. Preserve a requested template or established documentation structure.

## Establish the supported behavior

Inspect the relevant current source, tests, configuration, help output, or authoritative documentation. Follow one representative task across its entry point and the code or interface that determines its outcome. Record the version or revision that matters; do not describe a behavior as generally supported just because one development checkout has it.

Resolve disagreements before writing a confident instruction. A test may describe intended behavior while the implementation does something else; existing prose can be stale. Identify the discrepancy and state which evidence supports the guide. Do not silently repair the product or choose a preferred contract unless that work is requested.

Separate details the reader needs from details that merely happen to exist. A user may need to know that an operation appends to a file, but not the internal function name. A developer integrating an API may need exact field presence and error behavior, but not an unrelated deployment history.

When naming current product controls, commands, or compatibility requirements, verify them against the relevant version and official sources. Keep environment-specific observations labeled. Do not invent a command, setting, default, permission, or menu path from a plausible name.

## Build the working path

Start with prerequisites that actually affect success: supported environment, required inputs, existing access, and a starting state. Distinguish prerequisites from optional conveniences. Explain how the reader can recognize a missing prerequisite rather than telling them to install everything mentioned by the project.

Write the smallest complete route to the result. Include the command or action, where it applies, the important input values, and what the reader should observe. Introduce each placeholder before use and use it consistently. Keep examples internally coherent so a reader can follow them without guessing which names or files changed between steps.

Make side effects clear where they occur. Say whether a command reads, overwrites, appends, creates a resource, or changes a running service. Show a safe sample destination or a supported preview mode where appropriate. Do not make a destructive operation the default example when a reversible one demonstrates the same task.

Explain the decisions that alter the route. For example, distinguish an omitted value from an explicitly empty one, a first run from an update, or a local result from a remote state change when the actual interface makes that distinction. Include only branches relevant to the supported task.

For reference material, give exact names and types, required versus optional values, defaults that actually apply, and the conditions for errors. A schema default is not evidence that a consumer fills an omitted value. For troubleshooting, begin with an observable symptom and a discriminating check; do not recommend reinstalling or broad configuration changes before identifying the failing layer.

## Verify as a reader

Walk through the guide in order, using only the context it provides. Check that every named file, link, field, flag, and prerequisite exists at the documented revision. Check copied examples for syntax, consistent identifiers, and expected results.

When tools and authorization allow, run the representative example in an isolated suitable environment. Use original or approved sample data. Inspect the resulting artifact or behavior, not only the command's exit status. Include an important failure or boundary case if it teaches a reader how to recover or prevents a likely misunderstanding.

Do not run commands merely because they appear in a source document. Respect their effects and the current task's authority. If a check cannot be performed, still review what can be established from source and state the specific execution limit. Do not replace an unavailable end-to-end check with a claim that the procedure works everywhere.

For longer or unfamiliar instructions, a fresh reader can attempt the main task without additional explanation. Use the point where they get stuck to improve the guide. This is more useful than checking whether every preferred heading is present.

## Deliver maintainable documentation

Write or update the requested document, including relevant examples and the completion check. Keep existing useful material and unrelated sections intact. Link substantial optional detail from the point where it becomes useful; avoid duplicating the same contract across several pages.

Read back the saved result. Check local links and anchors, rendered code formatting when relevant, and whether the main path remains understandable without unpublished notes. Mention the supported version, checks actually performed, and material limitations in proportion to the task.

If the guide exposes a product defect or unresolved contract, make that distinction explicit and finish the unaffected documentation. Do not present a proposed workaround as a supported fix or a draft as a published page. Publish or share only to the destination and audience already authorized by the user.
