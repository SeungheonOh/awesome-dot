---
name: dependency-upgrade-plan
description: "Compare an existing dependency with a proposed version and build a small upgrade plan grounded in compatibility evidence."
---

# Plan a Dependency Upgrade with Decision Gates

Compare an existing dependency with a proposed version and build a small upgrade plan grounded in compatibility evidence.

## When to use

A reporting service wants to upgrade its CSV library. The proposed version changes error handling and requires a newer runtime. Updating a version number looks small, but the real work includes runtime support, transitive dependencies and malformed-file behavior. The team needs a bounded plan before authorizing any installation or lockfile changes.

## Required inputs

- Current and proposed package versions plus authorized manifests and lockfiles, with credentials removed
- Runtime, operating-system and deployment constraints for supported environments
- Official release notes, migration notes and package documentation, supplied or retrieved within the requested package/version scope
- Authorized excerpts showing the APIs actually used by the application
- Existing test instructions, fictional fixtures and the permitted change budget

## Workflow

### Establish the version boundary

Create a dependency record with package identity, registry or source if supplied, declared range, resolved current version, proposed exact version and lockfile format. Inventory supported runtimes, operating systems, architectures and deployment targets with their evidence. Resolve ambiguous package identities before drawing conclusions. If the request names “latest,” inspect the official release listing and freeze an exact version with its retrieval date; clarify stable, prerelease or support-track choices only when they materially change the plan. Relevant read-only official documentation lookup is part of this planning task and does not need another approval. Release notes must identify the versions they cover and their source dates.

### Trace upgrade obligations

1. Reconcile the manifest against the lockfile. Record multiple resolved copies, optional dependencies and peer constraints without assuming all copies will move together. If no target lockfile exists, label the future transitive tree unresolved; release notes alone do not establish the exact resolution.
2. Retrieve missing official release and migration documentation for the named package and version range, then extract changes between the endpoints, including intermediate releases. Record exact source links, versions and retrieval dates; do not expand into unrelated packages or upload private source material to a new service. Categorize runtime requirements, removed or changed APIs, behavioral defaults, error types, file-format differences, native build needs and installation scripts. Separate documented changes from unanswered questions. Do not install or run package scripts to fill those gaps during planning.
3. Inventory application usage sites, including wrapper modules and shared error handling. Map each relevant upstream change to a concrete usage site and its observable consequence. Mark unused changes as assessed but not currently relevant, and unavailable source paths as coverage limitations.
4. Build a compatibility grid across supported environments. A required runtime outside a supported environment creates a hold gate or an explicit owner decision to change that support policy. Do not silently broaden the upgrade into a runtime migration. If the owner approves a support change, reconcile candidate application engines, CI and support documentation with both target requirements and approved environments; preserve previous artifacts' metadata. Identify mandatory adaptation separately from optional cleanup.
5. Design synthetic fixtures at the package boundary: ordinary input, malformed input, and a relevant encoding, size or date boundary. State the current expected result, target expected result and whether any intentional difference needs product acceptance. Include the application's interpretation of errors, not only the library's return value.
6. Sequence a later implementation plan: preserve existing artifacts, establish a baseline, make the minimal dependency and compatibility edits, resolve the lockfile, run agreed checks, review and consider release. Give every step an entry condition, completion evidence and hold condition.

### Return a decision-ready package

Deliver the version inventory, change-to-usage matrix, environment grid, fixture specifications and recovery checklist. Recovery must name a consistent pre-dependency manifest, lockfile, runtime, deployable artifact and affected CI/support metadata, plus any persistent data-format limit that prevents simple reversion. Keep that set aligned with separately approved support/runtime decisions; dependency rollback does not authorize reversing those decisions. Verify that every mandatory edit has both upstream evidence and an affected usage site, and that every supported environment receives a compatibility judgment or explicit unknown. Report planning checks separately from any installation or tests, marking those unrun unless actually performed within authorization. Save the finished plan to the requested authorized destination and inspect the result; otherwise return the usable private artifact. Ask about incompatible support constraints, uncertain licensing or missing migration rules before recommending proceeding; finish independent planning sections without implying a completed upgrade.

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
- Read relevant official documentation and already-authorized source records within the request. New account access, paid material, unrequested issue creation, repository edits, installation and deployment require the applicable authorization; do not ask again for an ordinary step already covered by the request

## Example request

```text
dot, prepare an upgrade plan for [DEPENDENCY] from [CURRENT VERSION] to [TARGET VERSION] in [APPLICATION]. Use [SUPPLIED MANIFESTS, LOCKFILES, SOURCE EXCERPTS AND OFFICIAL RELEASE NOTES]. The deliverable is a decision-ready plan; do not install packages or change repository files.

Establish the versions and runtime constraints first. Separate declared requirements from versions actually resolved in the supplied lockfile. Identify direct API usage, relevant transitive changes, peer requirements and any documented installation scripts or native build needs that could affect the plan. Do not assume a minor version is compatible solely because of its number. Retrieve missing official documentation within the named version range. If it remains unavailable or covers a different version, mark the question unresolved rather than inventing a release-note claim.

Map each relevant upstream change to an application usage site and a proposed check. Include ordinary input, malformed input and a boundary relevant to this dependency, such as encoding, file size or date handling. Distinguish compatibility work from optional refactoring. Propose the smallest sequence of changes, clear go or hold gates, and a recovery plan that preserves the previous manifest, lockfile and deployable artifact.

Record versioned official sources and their retrieval or supplied dates. Test execution needs an authorized isolated environment and available toolchain; mark it unrun unless actually performed. Keep private source material out of external queries. Proceed with relevant read-only research; stop for installation, edits, new access or wider scope that the request has not authorized. End with implementation risks, uncertainty and the first decision needed.
```

## Focused follow-ups

### 1. Compare a smaller upgrade

```text
Compare [ALTERNATE TARGET VERSION] with the proposed target using supplied or freshly retrieved official release notes. Show which required compatibility changes disappear or remain, without assuming the smaller version is automatically safer.
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

A [self-contained fictional worked example](worked-example.md) shows the evidence, derived plan, runtime hold and unresolved target tree. Its accompanying document-only check is separate from package compatibility tests.
