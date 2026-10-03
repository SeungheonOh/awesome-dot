# Real-app control adapter contract

An adapter is an existing supported tool or project harness whose behavior has been verified. These are capability names, not invented tool calls. Resolve the actual interface before use. Record what is available, how it maps to this contract, and what remains blocked.

## Required operations

| Capability | Inputs | Evidence returned |
|---|---|---|
| Start | Repository and immutable revision, safe environment, fixture/account/flags, artifact directory | Session/process ID, build revision, stable app markers, startup result |
| Navigate and act | Completed feature-map path, documented user action and inputs | Actual interaction plus observed state change |
| Reset | Run-owned test state and documented reset method | Fresh equivalent state for the next independent attempt |
| Inspect | Permitted read-only view/state/log query | Value, time, scope, and proof the query does not change state |
| Screenshot | Correct app/window and run-owned destination | Readable image, app identity, capture time, discriminating state |
| Record | Correct region and full action path | Start/stop times, playable recording, final state, sensitive-overlay handling |
| Cleanup | IDs/paths created by this run and retention policy | Resources stopped/removed/retained, unresolved cleanup work |

A method returning success is not enough: check the app state. If a required operation is missing, stop the dependent reproduction/fix stage. Optional alternatives need an explicit evidence-contract change; they cannot silently turn a missing recording into a verified gate.

## Drive the user's path

Use accessible roles/names, label relationships, stable purpose-named selectors, or fresh observed coordinates when a semantic interface is unavailable. Do not rely on generated CSS classes, volatile hashes, stale screenshots, or arbitrary child indexes. Capture state after actions that can change the surface.

Cover feature-map states that apply: default, hover/focus, selected, expanded, disabled, loading, empty, validation failure, error, success, and cancellation. Use documented fixture setup or supported test controls for preconditions. The reported symptom must arise from real user interaction, not DOM injection, direct storage mutation, hidden app setters, or forced error state.

Read-only inspection may confirm what the UI showed; it cannot replace the UI path. Capture enough app chrome or a stable marker to distinguish the correct app from another build/window. Do not include tokens, personal data, or unrelated screen areas. Any authentication/permission setup remains subject to host and user rules.

## Candidate equivalence and evidence limits

Use the same relevant environment, data, flags, account role, and action sequence for baseline and candidate. Pin both identities. If an environment translation preserves the mechanism, label the exact difference and why it remains meaningful. If an operating system, device, hardware prompt, permission dialog, or account state is part of the defect, absence of that surface is a real limit; never call another platform exact proof.

Recordings must show the transition and discriminating final state, not just setup. Screenshots require actual visual inspection. Evidence files and a reviewer statement should agree about which attempt and revision they represent. Keep artifacts outside source control under the configured retention policy.

## Harmless qualification check

Before activation: start a disposable fixture; confirm app/build identity; read one completed feature-map section; navigate through the user path; exercise one safe state; inspect its result; capture screenshot and short recording; reset; repeat; clean up. Do not post to a live source channel during this local qualification.

Track every created process/profile/workspace. Cleanup must not kill unrelated processes, remove unknown worktrees, delete user data, close someone else's session, or extend into network/security changes. If an owned resource cannot be safely removed, report it for review instead of escalating scope.
