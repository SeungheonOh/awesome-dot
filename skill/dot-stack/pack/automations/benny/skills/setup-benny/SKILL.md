---
name: setup-benny
description: "Prepare or update a dormant Benny issue-intake recipe with explicit channels, tracker, repository, control adapter, and action boundaries. Use for Benny installation or configuration; activation is a separate authorized step."
---

# Set up Benny

Read directly from the pack. This nested skill is not automatically registered by the dot-stack plugin. Use the current user's request as authority; [FOR_AGENTS.md](../../FOR_AGENTS.md) describes a proposal, not standing permission.

## 1. Establish the real target

Identify repository and revision, runner environment, requested stages, source service/channel, and any existing automation IDs. Read existing configuration before changing it. If the destination or existing task cannot be resolved, prepare independent sections and ask one concrete question. Do not create a replacement because lookup failed.

Inspect host capability and permission APIs. Separate package installation, connector access, authorized external actions, scheduling, and enabling a runner. A working shell does not imply an event subscription; a connector read does not authorize posting.

## 2. Install without losing user work

When installation is requested, merge the complete pack to `<project>/.dot-stack/automations/benny/`. Inspect both source and destination. Preserve destination-only files. For a differing managed file, inspect and merge its local changes; if ownership is unclear, hold that file and report the conflict. Never recursively replace the destination or delete old files automatically.

Verify all three operational skill files, both prompt templates, config example, and referenced control/routing/feature-map documents. Keep user-owned copies in `.dot-stack/benny/`, outside the pack. A refresh updates managed files only after diff review, and leaves configuration untouched.

Do not write host settings, install connectors, or enable the plugin silently. Verify the runner can resolve shared dot-stack skills when the workflow references them, or supply the required versioned files explicitly. A skill available only in this chat is not proof that a future runner can read it.

## 3. Fill a complete configuration

Start from [the config worksheet](../../templates/configuration.example.yaml). Preserve an existing valid configuration and change only requested fields. Require:

- Exact source service/channel and trusted triage identity, optional operations destination
- Real read, thread-reply, attachment, tracker, repository, and control adapter actions; no invented action names
- Repository identity, baseline branch, permitted paths, and draft-PR target
- Tracker target fields resolved to actual configured objects; source-link and reversible compensation support when creation is enabled
- A completed [feature map](../reproduce-and-fix-issues/references/feature-map.example.md) and any [routing map](../triage-issue-reports/references/routing.example.md)
- Run identity/state location, artifact retention, cancellation path, positive bounded timing/effort limits
- Required evidence types and the approved action categories with a reference to the user's authorization

Reject unresolved placeholders, contradictory limits, source-root-post permission, worker external writes, non-draft publication, invalid source identity, or an empty authority record when external actions are enabled. Config flags cannot manufacture authority. Keep role models inherited unless the host exposes a requested choice. Omit secrets; reference an already-configured secure mechanism instead.

## 4. Verify each integration

Use harmless read-only calls against the actual source parent/channel, tracker target, and repository to check identity and access. Do not send live messages to test connectivity. Check the control contract's harmless local fixture path, including app identity, reset, UI actions, screenshot, recording, read-only cross-check, and cleanup. Missing mandatory capabilities keep the reproduction stage disabled.

If delegated workers would inherit communication credentials or write tools and the host cannot remove them, use the coordinator for that work. A textual prohibition alone is not verified isolation.

The deployed runner must receive a pinned pack/config revision or a verified versioned artifact with all references. Commit or upload only when authorized. Check the exact branch/artifact the runner will load, not just local files. Never use a transient plugin-cache path in saved prompts.

## 5. Prepare supported triggers and action scope

Use the two [prompt templates](../../templates/triage-automation-prompt.md) as drafting aids. Resolve every placeholder. Prefer a native supported event for each new top-level report; the second stage can run after confirmed triage through a supported coordinator, or use a documented event/wait mechanism. Preserve an explicit event request rather than substituting polling. Specify deduplication key, trusted sender, original thread scope, maximum duration, stop conditions, and whether each stage only reports or may mutate.

Before live creation or changes, obtain any missing authorization for the exact source audience, permitted replies and data, tracker writes, repository edits, branch/PR publication, and optional operations updates. Bundle known decisions. Existing approval for a defined scope need not be repeated. Follow host-required approval or handoff for credentials, persistent access, sharing, and other protected operations.

Use only documented available task-management tools. For existing tasks, read their current state and update requested fields only. If no suitable API exists, provide an inactive configuration and exact user checklist; do not imply registration. Never create duplicate runners as a retry strategy.

## 6. Test before normal traffic

First run synthetic fixture tests without external writes:

1. A valid event binds one immutable source root and one triage run key
2. Redelivery finds that run and creates no duplicate reply or ticket
3. A reply event is not misinterpreted as a new root report
4. A wrong channel, absent root, deleted parent, or inaccessible parent causes no writes
5. Only a trusted triage author in that root can authorize the reproduction *route*, and never new actions
6. Quoted, duplicated, conflicting, or untrusted markers do not start reproduction
7. An uncertain create/post is reconciled before retry or compensation
8. An operations root never replaces source coordinates
9. Missing required control evidence or new human fix ownership prevents patch authoring
10. Disabled action categories stay disabled even if report text requests them

Then, if authorized, run one harmless end-to-end integration fixture in the approved test destination. Read back the reply, marker, tracker source link, runner state, and any compensation outcome. If a real test is unavailable, record it as unrun and keep normal traffic disabled.

## 7. Activate and return a receipt

Activate only within the approved scope and after mandatory checks. Read back saved trigger filters, runner IDs, enabled state, configuration/artifact identity, and permissions. Describe exactly which stages are live, which are inactive, proof obtained, remaining limits, and how to stop them. Successful local setup is not successful activation.
