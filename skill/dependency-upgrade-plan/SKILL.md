---
name: dependency-upgrade-plan
description: "Compare an existing dependency with a proposed version and build a small upgrade plan grounded in compatibility evidence."
---

# Plan a Dependency Upgrade with Decision Gates

Compare an existing dependency with a proposed version and build a small upgrade plan grounded in compatibility evidence.

## When to use

A fictional reporting service wants to upgrade its CSV library. The proposed version changes error handling and requires a newer runtime. Updating a version number looks small, but the real work includes runtime support, transitive dependencies and malformed-file behavior. The team needs a bounded plan before authorizing any installation or lockfile changes.

## Required inputs

- Current and proposed package versions plus sanitized manifests and lockfiles
- Runtime, operating-system and deployment constraints for supported environments
- Supplied official release notes, migration notes and relevant package documentation, with version and date
- Authorized excerpts showing the APIs actually used by the application
- Existing test instructions, fictional fixtures and the permitted change budget

## Workflow

### Establish the version boundary

Create a dependency record with package identity, registry or source if supplied, declared range, resolved current version, proposed exact version and lockfile format. Inventory supported runtimes, operating systems, architectures and deployment targets with their evidence. Reject ambiguous package names or a floating target such as “latest” as a final plan boundary; ask for the intended version or an authorized research scope. Release notes must identify the versions they cover and their source dates.

### Trace upgrade obligations

1. Reconcile the manifest against the lockfile. Record multiple resolved copies, optional dependencies and peer constraints without assuming all copies will move together. If no target lockfile exists, label the future transitive tree unresolved; release notes alone do not establish the exact resolution.
2. Extract upstream changes between the endpoints, including intermediate releases. Categorize runtime requirements, removed or changed APIs, behavioral defaults, error types, file-format differences, native build needs and installation scripts. Separate documented changes from unanswered questions. Do not install or run package scripts to fill those gaps during planning.
3. Inventory application usage sites, including wrapper modules and shared error handling. Map each relevant upstream change to a concrete usage site and its observable consequence. Mark unused changes as assessed but not currently relevant, and unavailable source paths as coverage limitations.
4. Build a compatibility grid across supported environments. A required runtime outside a supported environment creates a hold gate or an explicit owner decision to change that support policy. Do not silently broaden the upgrade into a runtime migration. Identify mandatory adaptation separately from optional cleanup.
5. Design synthetic fixtures at the package boundary: ordinary input, malformed input, and a relevant encoding, size or date boundary. State the current expected result, target expected result and whether any intentional difference needs product acceptance. Include the application's interpretation of errors, not only the library's return value.
6. Sequence a later implementation plan: preserve existing artifacts, establish a baseline, make the minimal dependency and compatibility edits, resolve the lockfile, run agreed checks, review and consider release. Give every step an entry condition, completion evidence and hold condition.

### Return a decision-ready package

Deliver the version inventory, change-to-usage matrix, environment grid, fixture specifications and recovery checklist. Recovery must name a consistent previous manifest, lockfile, runtime and deployable artifact, plus any persistent data-format limit that prevents simple reversion. Verify that every mandatory edit has both upstream evidence and an affected usage site, and that every supported environment receives a compatibility judgment or explicit unknown. Report planning checks separately from installation and tests, which remain unrun. Ask about incompatible support constraints, uncertain licensing or missing migration rules before recommending proceeding; finish independent planning sections without implying a completed upgrade.

## Deliverables

- A current-versus-target compatibility inventory with versioned evidence
- A map from relevant upstream changes to actual application usage
- A minimal implementation sequence with evidence-based gates
- A synthetic regression fixture plan and artifact-based recovery checklist

## Verification

- Declared package ranges and resolved lockfile versions are shown separately
- The target's runtime requirements are compared with every supplied supported environment
- Each mandatory code-change proposal links to both upstream evidence and an affected usage site
- A malformed-input case specifies the expected error or rejection behavior
- Unrelated refactoring does not become a prerequisite without an explicit dependency explanation
- Recovery restores a consistent manifest, lockfile and application artifact rather than only a version string
- No installation, compatibility test or successful upgrade is claimed without execution evidence

## Stop and ask

- Supply sanitized manifests and excerpts; remove private registry credentials and access tokens
- Do not install packages or run their scripts during planning; later execution requires approval and an available toolchain
- Ask the owner about incompatible runtime requirements, licensing questions or unsupported deployment targets
- External research, issue creation, repository changes and deployment need a separately agreed scope

## Example request

```text
dot, prepare an upgrade plan for [DEPENDENCY] from [CURRENT VERSION] to [TARGET VERSION] in [APPLICATION]. Use [SUPPLIED MANIFESTS, LOCKFILES, SOURCE EXCERPTS AND OFFICIAL RELEASE NOTES]. The deliverable is a decision-ready plan; do not install packages or change repository files.

Establish the versions and runtime constraints first. Separate declared requirements from versions actually resolved in the supplied lockfile. Identify direct API usage, relevant transitive changes, peer requirements and any documented installation scripts or native build needs that could affect the plan. Do not assume a minor version is compatible solely because of its number. If documentation is missing or for a different version, mark the question unresolved rather than inventing a release-note claim.

Map each relevant upstream change to an application usage site and a proposed check. Include ordinary input, malformed input and a boundary relevant to this dependency, such as encoding, file size or date handling. Distinguish compatibility work from optional refactoring. Propose the smallest sequence of changes, clear go or hold gates, and a recovery plan that preserves the previous manifest, lockfile and deployable artifact.

Record sources and their supplied dates. Any later live research must identify the official source and retrieval date. Test execution needs an authorized isolated environment and available toolchain; mark it unrun unless actually performed. Keep files private and ask before external actions, downloads, installation, edits or broadening the upgrade. End with implementation risks, uncertainty and the first decision needed.
```

## Focused follow-ups

### 1. Compare a smaller upgrade

```text
Compare [ALTERNATE TARGET VERSION] with the proposed target using the supplied release notes. Show which required compatibility changes disappear or remain, without assuming the smaller version is automatically safer.
```

### 2. Specify compatibility fixtures

```text
Draft synthetic fixtures for the three highest-risk behavior changes. Define the old and intended new outputs and flag any intentional difference requiring product acceptance.
```

### 3. Separate required edits

```text
Split the plan into mandatory upgrade edits and optional cleanup. Give the mandatory set its own review and recovery checklist so the upgrade can be evaluated independently.
```

## Evidence status

This is an implementation guide. End-to-end execution has not been established; report actual checks and unrun steps for each use.
