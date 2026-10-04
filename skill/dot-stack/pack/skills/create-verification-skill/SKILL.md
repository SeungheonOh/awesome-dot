---
name: create-verification-skill
description: "Create a project-local recipe and feature map for driving the real app, collecting behavioral evidence, and cleaning up only test-owned state."
---


# Create a verification skill

Build a recipe another assistant can execute cold: launch the real app, check the instance, use its public interface, capture evidence, and clean up. A generated recipe that has not been exercised is a draft. This workflow does not authorize production writes, credential setup, installations, or external publication.

## Discover the project

Inspect the repository rather than asking the user for facts already available there. Record:

- User-facing interfaces: browser, command line, terminal UI, desktop, mobile, service, or library
- The documented local run and test commands, pinned runtime, required configuration, and readiness signal
- Existing drivers: browser tests, command fixtures, HTTP clients, device simulators, or project-specific helpers
- Observable outputs: rendered state, files, response bodies, exit codes, logs, or stored values
- Isolation: ports, profiles, data directories, test tenants, fixture ownership, and concurrent-run limits
- Which actions are safe locally, and which contact a real service or change someone else's data

Prefer an existing harness. Inspect its commands and dependencies before running them. Do not invent a wrapper executable or install a new driver by default. If the app cannot start, diagnose the specific prerequisite. Fix only what is authorized; an unrelated product change is not part of skill generation. Harmless local scaffolding can be documented when necessary, reversible, and within scope, with owned paths and cleanup.

## Choose the destination

Use the requested location or the project's established skill directory. `.agents/skills/verify-<app>/` and `.claude/skills/verify-<app>/` are host-specific examples, not interchangeable discovery guarantees. Do not overwrite an existing recipe blindly. If there is no writable environment, deliver an unapplied skill draft with its resource files.

Use portable `name` and `description` frontmatter. Name the actual app, interfaces, and verification task in the description. Do not add host permission fields or claim automatic activation by file extension.

## Write the execution contract

Every generated section must use observed project facts and real commands. Include:

1. **Launch.** Exact working directory, command, test-owned configuration, readiness condition, timeout, and how the run identifies its process. Short-lived commands get an isolated process or terminal per drive; servers may use one owned session
2. **Doctor.** A read-only check for app identity, revision, expected endpoint or prompt, owned data directory, and required authentication status. A healthy port alone is insufficient
3. **Drive.** Existing driver invocation and stable selectors, routes, command arguments, or library imports. Use accessible roles and names when available. Do not replace the user path with internal setters or hidden test-only endpoints
4. **Evidence.** Input action plus resulting state, exact revision, command, time, environment, and a durable local artifact path. Confirm side effects through a second public or read-only view. Mock only the external boundary that the test cannot safely exercise, and label the coverage limit
5. **Cleanup.** Stop only processes started by this run, remove only owned scratch data, and retain proof artifacts. Never kill by process name or delete shared user state
6. **Failure handling.** Run doctor after unexpected behavior. Reset a wedged UI even if its server is healthy. On unavailable credentials or a live-service boundary, stop that step and record it unverified; continue independent local coverage

For any dry-run mode, inspect and test what it skips. “Dry run” is not proof that no network request, file write, or browser launch occurs.

## Map user-visible features

Create a feature index and an initial set of important feature recipes. Use [the example map](references/feature-map-example/README.md) for structure, not as project commands. Select features from actual routes, menus, commands, or documentation. List every supported entry point for each mapped feature and record individual coverage. One working entry point does not prove the others.

Each recipe needs sub-features, user entry points, real driver steps with preconditions and observable outcomes, and gotchas. Include cancellation, repeated actions, persistence, empty/error states, and interruption when relevant. If a selector is not observed, leave the recipe as a draft rather than manufacturing it.

## Prove one complete run

Run the generated instructions from a clean fixture: launch, doctor, drive one mapped feature, collect evidence, and clean up. Confirm the evidence still exists afterward. A failed attempt also needs cleanup before retry. Any changed helper must be invoked as documented, and its behavior checked rather than only syntax-checked.

Report the saved files, exact feature and entry point tested, checks and artifact locations, and remaining mapped features not yet exercised. If no execution tool is available, provide the complete draft and precise missing capability; do not call it verified. [Maintain verification skill](../maintain-verification-skill/SKILL.md) can keep the recipe current when requested; creation enables no schedule.
