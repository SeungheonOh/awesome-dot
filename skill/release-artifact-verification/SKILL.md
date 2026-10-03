---
name: release-artifact-verification
description: "Verify the exact built package users receive by inspecting its contents, installing it in an isolated consumer environment, and exercising its public entry point and required resources outside the source checkout."
---

# Verify the Package Users Receive

Establish whether one identified distribution actually installs and performs the promised small user workflow. Return the artifact, its identity and contents, and separate packaging, installation and runtime evidence. A successful source test or build is supporting evidence; it does not establish that the delivered package contains everything its runtime needs.

Use this for a built wheel, package archive, application bundle, or similar bounded deliverable when the question is “does this exact thing work after a user receives it?” Keep release approval, rollout planning, general repository mapping, source-code review and broad build repair outside this workflow. Inspect source only as needed to establish the package contract or diagnose a demonstrated artifact defect.

## Establish the consumer contract

Identify from the request and available evidence:

- The exact artifact or source candidate, expected distribution name/version, permitted local workspace, and intended delivery format
- The user's installation method and target operating system, architecture, runtime and dependency expectations
- One real public workflow with a concrete input and observable result, including any required packaged resource or module-loading relationship
- Whether the request authorizes verification only, building, installing in a disposable environment, or repairing and rebuilding a copy
- Where to preserve the original and write the checked artifact and evidence

Prefer an already supplied built artifact when that is what users will receive. Rebuilding the same commit creates another candidate; it does not test the original bytes. Resolve ambiguous artifact identity before claiming a result. An intended version, release filename or Git commit alone is insufficient: record the artifact's relative name, byte size and SHA-256 digest, and pair source identity with any relevant uncommitted changes.

Use synthetic inputs where practical. Read project instructions and the package's build/install configuration before invoking executable hooks. Existing tools and an understood offline local workflow may be used within the request. Installing an artifact executes or enables code: do not treat a read-only audit as authorization to run it. If the source, installer or dependency route needs new authority, downloads, credentials or shared services, complete static inspection and identify the exact blocked step. Never contact a registry merely because the usual command would do so.

## Inspect the artifact itself

Preserve the received bytes and their original name before any repair. Inspect the archive or native package with available tools; do not trust its extension, label or a successful build log as evidence of its contents. Work from a copy when the inspection tool can write.

Check the properties relevant to the consumer contract:

1. Distribution name/version, target compatibility declarations, runtime dependencies and public entry-point registrations
2. Required modules, templates, schemas, translations, static assets or configuration defaults, including exact resource bytes when the requirement supplies them
3. Package membership and internal integrity metadata, where the format provides it
4. Whether the resource is discoverable through the package's own runtime API after installation, rather than at a development-only relative path

Compare intended content with actual members. A file present in Git, a source distribution or a build directory can still be absent from the deliverable. Conversely, an included file can be stale, placed in the wrong directory, or registered under the wrong entry point. Verify the narrow contract, rather than assuming that inclusion alone proves usable behavior.

For Python wheels, read [the packaging notes](references/packaging-notes.md) when deriving checks. Inspect `METADATA`, `WHEEL`, `entry_points.txt` when present and `RECORD`. Record whether you independently verified internal hashes. A content digest identifies bytes; it does not authenticate their publisher. Compatibility tags and `Requires-Python` are declarations to reconcile with the test environment, not empirical proof across all declared targets.

## Install as a fresh consumer

Use a new environment that cannot see an earlier installation or the source checkout through a development shortcut. Before installing, record the environment identity and verify the target package is absent. Reuse neither an editable installation nor a global package directory. Keep the preserved original and the evidence outside disposable scratch space.

For a dependency-free Python fixture, a fresh `venv`, a direct local wheel path, and pip options `--no-index --no-deps` make the intended route explicit. Disable update checks and cache use, use the already available backend when building, and inspect configuration that could add other sources. These flags alone are not an operating-system network sandbox. For a real package with dependencies, `--no-deps` does not prove that dependencies resolve or are correctly declared. Use an authorized existing offline dependency set if the request covers it; otherwise label that part blocked. Do not silently download the missing toolchain.

Record installation separately from packaging and runtime:

- Exact command and working directory, installer/runtime versions, relevant environment overrides, exit status and meaningful output
- Which artifact digest the installer consumed, using the installer report when available and a direct file hash
- Installed distribution name/version and resolved module/application location
- Any installation-generated wrapper, manifest or metadata relevant to the public invocation

Failing before installation starts is a setup result. A successful installation can still deliver a broken application. Keep those outcomes separate.

## Exercise the installed public workflow

Change to a fresh consumer directory outside all source copies. Call the installed public entry point using an unambiguous path. A helper that imports a source module directly is not an equivalent substitute for an installed CLI invocation.

Exclude development leakage deliberately. For Python:

- Do not pass `PYTHONPATH` or `PYTHONHOME`; disable user-site imports and avoid `--system-site-packages`
- Use the environment's interpreter explicitly; use isolated interpreter mode for provenance checks
- Verify the imported package resolves inside the new environment and that import paths do not include source roots
- Check the generated public wrapper uses the expected interpreter when its format permits inspection
- Read the installed resource and compare its digest with the archive member, rather than relying on the source copy

Do not make the source unavailable by deleting, renaming or changing permissions on a real checkout. Import-path and origin evidence should establish the boundary without destructive preparation. Environment isolation reduces contamination; it does not sandbox an unknown program.

Run the consumer workflow that exercises the required resource or module-loading behavior. A `--help`, `--version` or empty-import check alone does not establish that behavior. Compare actual output, exit status and relevant installed bytes with the established contract. Add a nearby boundary only when it tests something meaningful, such as a non-ASCII input or invalid option. Keep the observation scoped: one successful Linux CLI run cannot establish Windows wrapper behavior, GUI operation, upgrade compatibility or all documented features.

## Diagnose and, only if requested, repair

Classify the first demonstrated failure without collapsing the three evidence stages:

- **Packaging:** the required resource, entry registration or correct bytes are absent or wrong in the artifact
- **Installation:** the installer rejects the artifact, creates the wrong target, or cannot satisfy the authorized environment requirements
- **Runtime:** the installed public command reaches the application but fails the consumer contract
- **Blocked or inconclusive:** missing tools, unsupported environment, timeout, incomplete evidence or an unresolved dependency prevents a conclusion

A single defect can fail both packaging and runtime while installation passes. Preserve both results. If only verification was requested, deliver the rejected candidate, diagnosis and a precise proposed packaging change without modifying it.

When a repair is explicitly authorized, change the smallest justified build declaration or implementation in a fresh copy. Keep the original source and rejected artifact. Build into a new output directory so stale generated state cannot supply a missing file. Record the patch, build environment and resulting artifact digest. Do not clean or reset someone else's working tree. Apply the project's version policy for a real release; replacing a published version's bytes is not implied by a local repair request.

Install the new artifact in another fresh environment and rerun the same consumer check. Pair every pass with that artifact's digest. A test of an earlier build does not validate a later rebuild, even when both files have the same name and version. If the repair changes the contract, needs unavailable dependencies or crosses an unapproved execution boundary, stop that branch and finish the useful diagnosis.

## Deliver the checked package and evidence

Return the requested actual artifact, not only a recommendation document. If no candidate passed, preserve the received artifact and explicitly label it rejected or unverified. Include a compact verification note with:

- Exact filename, distribution version, byte size, SHA-256 and build/source relationship
- Packaging membership, entry-point and required-resource evidence
- Installation command, environment and installed provenance
- Public invocation, input, output, exit status and stage-by-stage verdicts
- Preserved baseline failure and authorized repair, if any
- A portable reproduction route with prerequisites, actual platform coverage and unrun checks

Read back the saved artifact and evidence. Verify its final digest and the relevant installed content again if any bytes change before handoff. Ordinary saving to an already authorized destination can proceed; a request to check a package does not imply publication, release approval, upload to a registry or distribution to new recipients.

Stop when the identified artifact's scoped consumer contract has an evidenced result, or the next necessary step is specifically blocked. Do not expand a small package check into a platform certification or release-governance project.

## Worked example

[The Packet Stamp example](EXAMPLE.md) preserves an original source fixture, a wheel that omits its required JSON data, a two-line packaging repair, and the checked wheel. Both wheels install and report version `0.3.0`; only one can format a label from outside the checkout. [The verification note](VERIFICATION.md) records actual hashes, commands, contents and limits.

[The Switchboard Registry companion](javascript/README.md) tests a JavaScript package whose ESM and CommonJS branches work alone but violate an explicit shared-state contract when combined. It verifies both load orders from exact offline-installed tarballs; a one-file repair makes both entries share the same core.

The example helpers are intentionally restricted to their respective reviewed original fixtures. Read their scope in the example before running them. They create new output directories, use the existing toolchain, install only the local fixture into disposable environments, and preserve the source inputs. They are not generic installers for arbitrary supplied packages.

## Example request

```text
Check [EXACT LOCAL ARTIFACT] as a fresh user of [PUBLIC COMMAND] on [TARGET].
Verify [EXPECTED INPUT/OUTPUT] and the required [BUNDLED RESOURCE OR LOADING CONTRACT]. Preserve
the received bytes and report the artifact's exact version, size and SHA-256.
Inspect its packaging, install this reviewed package only in a new disposable
local environment with the existing permitted tools, and run outside the source
checkout with no editable or user-site imports. Use no registry or downloads.

Separate packaging, installation and runtime results. [Choose: verify only;
or repair a copied fixture and rebuild if the defect is in its packaging.]
Return the actual checked artifact, preserved failure evidence, installed
readback and portable reproduction steps. State which targets were not tested.
```

## Browser-app archives: verify the launch route

For an authorized software-archive check, exercise the links the recipient will actually use, not just the files those links eventually intend to reach.

1. Identify the root launch command and whether each app is static or needs its own local service. Check documented ports, relative URLs, worker/module resources and runtime requirements from the extracted archive.
2. Start only the reviewed local code within the existing execution authority. If using a small static server, keep its serving scope explicit; an archive does not need a directory listing or arbitrary access to the surrounding checkout.
3. Follow each declared entry route through actual HTTP. A successful request for `/tool/dist/index.html` does not prove that the launcher's `/tool/dist/` URL works. Test required directory aliases and content types, and check that unsupported routes fail without exposing unrelated files.
4. For a server-backed entry, verify that the selected command starts the intended service and that the UI or bounded public workflow is served at its documented loopback address. Static HTML inspection cannot prove its backend started.
5. Repeat from the extracted consumer directory with representative path spelling, including spaces when relevant. In Node ESM code, convert file URLs through the supported path conversion rather than treating a URL pathname containing percent escapes as a filesystem path.
6. Keep evidence labels precise. Copying known installed dependencies into a disposable consumer environment tests that dependency set; it is not a fresh registry installation. Simulated DOM checks and direct HTTP checks do not establish real-browser layout or a user's completed download.

### Worked archive route check

A locally authored app archive included a searchable launcher and a bounded Node starter. The first starter draft mapped explicit `index.html` paths, while source inspection of the launcher showed directory-style links ending in `/dist/`. The mapping was repaired before the final consumer check, adding only explicit aliases for catalogued app entry points rather than enabling directory listing.

The actual HTTP tests then requested every declared static app entry route, checked JavaScript content types, rejected unrelated `README.md`, configuration and traversal-like paths, and exercised Host/Origin and method rejection. A separate command invocation, `node app-validation/start.mjs doi-desk`, started the selected local service and served its UI without triggering an upstream data request.

The full archive was extracted into a fresh Linux directory containing spaces. Its 109 test programs passed under Node 24.19 using an existing offline dependency set. This established the exercised package, route and program-test boundaries; it did not establish macOS/Windows behavior, a clean dependency install or real-browser interaction. The useful repair was the mismatch between the public entry route and the actual serving map, which a check of file existence alone would have missed.

## Recover a workspace without regressing the delivered release

When local files may have reverted or an executor has changed, resolve the most recent delivered artifact from its durable destination before treating the local checkout or same-named ZIP as the baseline. A surviving filename, cached version label or earlier green test log does not establish that the local content is current.

1. Record the durable artifact's confirmed identity/version, materialize that exact version into a separate recovery directory and verify its internal membership/hashes. Do not overwrite new local work while downloading a baseline.
2. Compare its public inventory with the current candidate. For an app collection, compare stable app IDs, not only the count. An equal count can conceal one removed app and one added app. Refuse silent loss of a previously delivered entry unless removal is explicitly part of the requested release change.
3. Preserve new edits separately, then recover missing release files and merge only the intended changes. Avoid copying private runtime state, credentials or browser profiles into a software archive. Restoring source assets and restoring authenticated sessions are different operations.
4. Rerun source checks after recovery, package the exact resulting bytes and repeat the extracted-consumer checks. Checks on the reverted candidate cannot validate the recovered release. Keep the prior artifact unchanged until the replacement is verified.
5. Use the destination's optimistic version check when replacing a shared artifact. On a conflict, resolve the newer durable version and reconcile; do not remove the guard or force an overwrite merely to finish the upload.

A useful packaging guard can accept an explicitly selected prior ZIP, reject duplicate/unsafe members and excessive expansion, verify its complete member-hash inventory, then require that every prior stable app ID remains in the new catalog. This guard catches accidental omissions relative to its supplied baseline. It cannot discover the latest remote release by itself, authenticate the publisher from self-contained hashes, or establish that unchanged IDs still behave correctly. Keep those separate checks.

### Worked recovery example

A collection had 55 apps in its verified delivered archive, but a later working directory contained only a 47-app snapshot. Adding one new app would have produced a superficially successful 48-app release while dropping eight already delivered apps. The current local ZIP was also old, so comparing only against that ZIP would not have detected the regression.

The exact delivered 55-app archive was retrieved separately and its member hashes verified. The new app and local edits were preserved, missing released files were restored, and the intended addition was merged into a 56-app inventory. All 118 test programs then passed both before packaging and in a fresh extracted consumer directory. A later packaging guard rejected a synthetic candidate missing a prior stable app ID, as well as duplicate IDs, altered baseline bytes and an incomplete hash inventory.

This verifies continuity against the selected release and the exercised consumer contract. It does not prove that the underlying workspace will persist through future resets; that needs a separate observation after the relevant reset actually occurs.
