# Worked example: hold a CSV upgrade until runtime support is resolved

This is a self-contained fictional planning exercise. Every package, source URL, release note, application excerpt and artifact below is invented. The `.invalid` URLs identify the fictional sources within the exercise; they are not live research links. All evidence is supplied, dated 2026-09-30. No package was downloaded, installed or executed, and no application or lockfile was changed.

The request is to plan a direct dependency upgrade of `@demo/rowcsv` from the version locked for release R42 to exactly `3.2.0`. Preserve existing import and audit-export behavior. Do not expand the request into upgrading the audit adapter or migrating supported runtimes.

## Supplied evidence

### [E1] R42 application manifest

The application is `ledger-reporting`. These are the relevant complete dependency declarations from `package.json`; omitted fields contain application commands, not additional dependencies or overrides.

```json
{
  "name": "ledger-reporting",
  "version": "4.2.0",
  "private": true,
  "engines": { "node": ">=18.17.0 <23.0.0" },
  "dependencies": {
    "@demo/rowcsv": "~2.4.0",
    "@demo/audit-csv": "1.6.0"
  }
}
```

### [E2] R42 lockfile excerpt

This is an npm lockfile-version-3 excerpt. Integrity and download-location fields are omitted, not unknown in the preserved R42 lockfile. The supplied dependency records below are complete for these two CSV paths; there are no overrides, optional dependencies or peers in these records.

```json
{
  "lockfileVersion": 3,
  "packages": {
    "": {
      "dependencies": {
        "@demo/rowcsv": "~2.4.0",
        "@demo/audit-csv": "1.6.0"
      }
    },
    "node_modules/@demo/rowcsv": {
      "version": "2.4.1",
      "dependencies": { "@demo/byte-text": "^1.4.0" }
    },
    "node_modules/@demo/byte-text": { "version": "1.4.3" },
    "node_modules/@demo/audit-csv": {
      "version": "1.6.0",
      "dependencies": { "@demo/rowcsv": "~2.3.0" }
    },
    "node_modules/@demo/audit-csv/node_modules/@demo/rowcsv": {
      "version": "2.3.2",
      "dependencies": { "@demo/byte-text": "~1.3.0" }
    },
    "node_modules/@demo/audit-csv/node_modules/@demo/byte-text": {
      "version": "1.3.5"
    }
  }
}
```

The supplied range convention is ordinary stable-version npm range arithmetic: `~2.4.0` admits `2.4.x`, `~2.3.0` admits `2.3.x`, `^1.4.0` admits versions from `1.4.0` below `2.0.0`, and `~1.3.0` admits `1.3.x`. These numeric facts do not promise behavioral compatibility.

### [E3] Complete usage excerpts for the supplied application scope

U1, `src/import-accounts.js`, imports the top-level `2.4.1` copy:

```javascript
import { parse, CsvError } from "@demo/rowcsv";

export function importAccounts(text) {
  try {
    const rows = parse(text, { headers: true, emptyLines: "skip" });
    if (rows.some(row => !Object.hasOwn(row, "account") ||
                         !Object.hasOwn(row, "amount"))) {
      return { status: 400, body: "Missing columns" };
    }
    return { status: 200, body: rows };
  } catch (error) {
    if (error instanceof CsvError && error.code === "CSV_BAD_QUOTE") {
      return { status: 400, body: "Invalid CSV" };
    }
    throw error;
  }
}
```

U2, `src/import-route.js`, catches otherwise unhandled failures from U1 and returns `{ status: 500, body: "Import failed" }`. It must continue to distinguish malformed CSV from unexpected faults.

U3, `src/audit-export.js`, calls `encodeAudit(rows)` from `@demo/audit-csv`. The supplied adapter implementation shows which copy and options it uses:

```javascript
// Inside @demo/audit-csv 1.6.0; resolves its nested rowcsv 2.3.2 copy.
import { stringify } from "@demo/rowcsv";
export function encodeAudit(rows) {
  return stringify(rows, { headers: ["account", "amount"], newline: "\n" });
}
```

The supplied scope has no other CSV usage, dynamic imports or direct `byte-text` usage. This establishes coverage for this exercise only; it is not a claim about unseen services.

### [E4] Supported environments and existing recovery artifacts

| Environment | Supported runtime and platform | Existing R42 evidence |
|---|---|---|
| R1 production API | Node 20.11.1, Linux x64 | `ledger-R42-api.tar`, runtime image `node20.11.1-linux-x64-R42` |
| R2 scheduled import worker | Node 18.19.0, Linux x64 | `ledger-R42-worker.tar`, runtime image `node18.19.0-linux-x64-R42` |
| R3 integration CI | Node 22.4.1, Linux arm64 | `ledger-R42-ci.tar`, runtime image `node22.4.1-linux-arm64-R42` |

The supplied R42 release record ties all three application archives to the same application source, full E1 manifest and full E2 lockfile. It also includes `ledger-R42-support.tar`, containing the matching CI configuration and versioned support documentation: R1–R3 are supported, CI uses R3, and the advertised application range is E1's `>=18.17.0 <23.0.0`. Its preserved `R42-checksums.txt` verifies these archives and runtime-image records. The excerpts here are not substitutes for those full recovery files. R42's recorded checks passed; a fresh baseline has not been run in this exercise. The recorded runner is npm 10.8.2; keep that runner fixed when comparing lockfiles.

R42 is the intact historical recovery set, including its old support policy. Once an owner approves a different runtime or support policy, dependency rollback needs a new verified pre-dependency set that retains the current dependency versions while matching that approved policy. Such a set has not been created in this exercise; unchanged runtime binaries alone do not make R42's old support metadata suitable.

The importer returns data without writing it to persistent storage. Audit CSV is archived externally using U3's fixed column order and LF terminator. No database or durable row-format migration is in scope. Already delivered external files cannot be recalled by rolling back an application archive.

### [S0] Current documentation and complete fictional release index

Source: `https://rowcsv.example.invalid/docs/2.4.1-and-2.3.2`, supplied 2026-09-30. Both current versions document Node `>=18.17.0 <23.0.0`, pure JavaScript, and no install scripts, optional dependencies or peers. For the shown APIs:

- `parse(text, { headers: true, emptyLines: "skip" })` returns objects whose field values are strings and skips empty lines
- Duplicate column names default to last-column-wins; `duplicateHeaders: "last"` explicitly selects it
- A leading UTF-8 BOM is retained in the first header by default; `bom: "preserve"` explicitly selects it
- An unterminated quoted field throws `CsvError` with `code: "CSV_BAD_QUOTE"`
- `stringify` accepts `headers` and `newline`; its default terminator is LF, and it terminates the final row

The supplied complete stable release index after `2.4.1` through the target is `2.5.0`, `3.0.0`, `3.1.0`, `3.2.0`. There are no omitted releases in that fictional interval. This index, rather than the endpoint version numbers, bounds the notes that must be covered.

### [S25] Version 2.5.0, released 2025-02-12

Source: `https://rowcsv.example.invalid/releases/2.5.0`, supplied 2026-09-30.

With header parsing enabled, the default duplicate-header policy changes from `"last"` to `"error"`. Duplicates now throw `CsvDuplicateHeaderError` unless `duplicateHeaders: "last"` is specified. The explicit last-column-wins option remains supported through `3.2.0`. Other shown parser settings and the runtime requirement are unchanged in this release.

### [S30] Version 3.0.0, released 2025-06-04

Source: `https://rowcsv.example.invalid/migrate/3.0.0`, supplied 2026-09-30.

- Node support becomes `>=20.9.0 <23.0.0`
- `parse` is removed; use `parseRows`. Replace `headers: true` with `header: "first"` and `emptyLines: "skip"` with `blankRecords: "skip"`. The corresponding outputs remain strings in object rows
- `CsvError` is removed. An unterminated quoted field now throws `CsvSyntaxError` with `reason: "UNTERMINATED_QUOTE"`; it no longer carries `code: "CSV_BAD_QUOTE"`
- `duplicateHeaders`, `bom`, and `stringify`'s explicit `headers` and `newline` options remain supported

### [S31] Version 3.1.0, released 2025-08-06

Source: `https://rowcsv.example.invalid/releases/3.1.0`, supplied 2026-09-30.

The parser's default BOM handling changes from `"preserve"` to `"strip"`. `bom: "preserve"` remains available. Node requirements and the `3.0.0` API/error contract remain unchanged.

### [S32] Version 3.2.0, released 2025-10-15

Source: `https://rowcsv.example.invalid/releases/3.2.0`, supplied 2026-09-30.

`stringify`'s default row terminator becomes CRLF; an explicit `newline` still wins. The direct decoder requirement changes from `^1.4.0` to `^2.1.0`. The notes do not enumerate `byte-text`'s own dependency tree or identify the version a new lockfile will select. All earlier documented changes above remain in force.

The accompanying published metadata excerpt is:

```json
{
  "name": "@demo/rowcsv",
  "version": "3.2.0",
  "engines": { "node": ">=20.9.0 <23.0.0" },
  "dependencies": { "@demo/byte-text": "^2.1.0" },
  "optionalDependencies": {},
  "peerDependencies": {},
  "scripts": {}
}
```

S32 describes `rowcsv` itself as pure JavaScript with no native build. This metadata does not establish the installation behavior, platform support or scripts of an unresolved transitive tree.

## Derived plan

### Current versus proposed inventory

| Dependency path / support metadata | Declared now → proposed | Resolved now | Target resolution / judgment |
|---|---|---|---|
| Direct `rowcsv`, U1 import parser | `~2.4.0` → exact `3.2.0` | `2.4.1` | Exact direct target known; requires API, error and explicit-behavior edits |
| `audit-csv`, U3 export wrapper | Exact `1.6.0` → unchanged | `1.6.0` | Preserve; upgrading this adapter is outside the request |
| Nested `rowcsv` under audit adapter, U3 serializer | `~2.3.0` → unchanged | `2.3.2` | Preserve existing locked copy; `3.2.0` cannot satisfy this range |
| Direct CSV path's `byte-text` | `^1.4.0` → `^2.1.0` from S32 | `1.4.3` | Exact future version and further dependencies unknown |
| Audit CSV path's `byte-text` | `~1.3.0` → unchanged | `1.3.5` | Preserve existing locked copy; verify the eventual lock diff |
| Application `engines.node`, E1 | `>=18.17.0 <23.0.0` → owner-approved candidate range still UNKNOWN | Manifest support claim, not a locked package | Must be reconciled with target requirements and approved support/CI records at G1; retaining the old claim would falsely include Node 18 |

Do not globally override `rowcsv` to `3.2.0`, or assume that a package-manager deduplication will migrate both usages safely. Preserve the nested locked versions as the minimal plan; any unexpected movement reopens review. No target lockfile exists. The target direct version is not proof of a known complete target tree.

### Runtime compatibility grid

| Environment | Current declared requirement | Target declared requirement | Decision |
|---|---|---|---|
| R1 Node 20.11.1 / Linux x64 | Within S0 range | Within S30/S32 range | Engine-range check passes; actual application/package compatibility unrun |
| R2 Node 18.19.0 / Linux x64 | Within S0 range | Below minimum 20.9.0 | HOLD: a supported deployment cannot use the target |
| R3 Node 22.4.1 / Linux arm64 | Within S0 range | Within S30/S32 range | Engine-range check passes; actual application/package compatibility unrun |

The shown package is documented as pure JavaScript, but the unresolved target tree prevents a complete platform/build judgment for R1 and R3. No number-based compatibility guarantee is inferred.

#### G1 support reconciliation

First decision: the support owner must choose whether to keep R2 and consider a separately researched alternative target, or authorize a separate runtime/support change. Do not assume R2 can be retired or upgraded. Removing R2 from deployment alone does not fix E1: its advertised range still admits Node 18.

- G1 decision checkpoint: obtain the owner-approved actual environment list and advertised application support policy, including the exact proposed candidate `engines.node` and corresponding CI and support documentation changes. The candidate range remains UNKNOWN until that decision; do not simply copy the dependency's range or invent a narrower support policy
- G1 readback checkpoint: after the candidate metadata edits, verify that its advertised range is a subset of the target's `>=20.9.0 <23.0.0` range, every approved deployment/CI runtime is admitted by both ranges, and CI and support documentation agree with the owner-approved policy. HOLD for any remaining Node 18 claim, mismatched environment, stale support claim or unknown policy. Repeat this check in release review
- Preserve E1 and the complete R42 recovery artifacts unchanged. Apply approved support-metadata changes only to newly prepared pre-dependency and candidate artifacts. Before dependency edits, verify a pre-dependency baseline retaining direct `rowcsv` `2.4.1` and the existing audit copies, but matching the approved runtime and support policy across its manifest, lockfile, CI and support documentation. This is required for a support-only change too, including unchanged-runtime R1/R3 that share the policy. A new runtime also requires its own verified build; the old R42 worker archive is not evidence for it

G1 remains open until both checkpoints pass. This is a consistency gate for advertised and actual support, not a claim that every version in an approved range has been executed. G3 still requires the agreed compatibility checks on every approved environment.

### Change-to-usage-and-check matrix

Checks F1–F6 below are specified, not executed. G1 is the actual-and-advertised runtime support gate, G2 the resolved-tree review, and G3 the authorized application test gate.

| ID | Upstream evidence and change | Affected use / consequence | Smallest required action or assessed disposition | Evidence needed |
|---|---|---|---|---|
| M1 | S30/S32: Node minimum rises; E1 still advertises Node 18 | U1 on R2 is outside target support; the application support claim also conflicts | HOLD for support-owner decision; conditionally reconcile candidate `engines.node`, CI and support documentation. A runtime migration is separate work | G1: owner-approved actual/advertised support policy, valid pre-change baseline and matching candidate readback |
| M2 | S25: duplicate headers now reject | U1 currently accepts duplicates using the last value; default target error would escape to U2's 500 | Explicitly retain `duplicateHeaders: "last"` | F4 at G3 |
| M3 | S30: `parse` removed; parser options replaced | U1 cannot import/call the old API | Import `parseRows`; map to `header: "first"`, `blankRecords: "skip"` | F1 at G3; module-load check on every approved environment |
| M4 | S30: syntax-error class and discriminator change | U1's old catch no longer maps malformed input to 400; U2 returns 500 for unexpected faults | Import `CsvSyntaxError`; catch only that class with reason `UNTERMINATED_QUOTE` | F2 and F6 at G3 |
| M5 | S31: BOM default strips | U1 would newly accept a file previously rejected for a missing `account` header | Explicitly retain `bom: "preserve"` | F3 at G3 |
| M6 | S32: serialization default becomes CRLF | Direct copy has no serializer usage; U3 uses a distinct retained copy and explicitly requests LF | Assessed, no application edit; retain U3 and its copy | F5 at G3 and nested-copy review at G2 |
| M7 | S32: decoder range becomes `^2.1.0` | U1's underlying decoder tree changes; no direct decoder use | Unknown exact resolution; inspect the later authorized lock diff and relevant metadata | G2: exact tree, integrity/source records, scripts/native/peer/optional review; F1–F4 at G3 |
| M8 | S0/S32: no direct peers, optional dependencies, install scripts or native build | All shown uses; this statement covers `rowcsv` only | No direct adjustment identified; do not extend the claim to transitive packages | G2: confirm exact resolved metadata against supplied direct metadata and inspect unresolved tree |

The minimal candidate edit set is the direct dependency declaration and resolved lockfile, U1 adaptations in M2–M5, and the owner-approved candidate `engines.node`, CI and support documentation corrections in M1. The exact support-policy edits remain undecided; they are not optional cleanup once an approved policy requires them. Every required code edit above has a versioned source and U1 usage. U2's behavior is asserted by checks rather than rewritten. U3 is deliberately unchanged. Enabling duplicate-header rejection or BOM acceptance would be an intentional product behavior change requiring a separate decision; it is not necessary for this behavior-preserving upgrade.

The proposed U1 compatibility edit is limited to its import, parser call and catch predicate:

```javascript
import { parseRows, CsvSyntaxError } from "@demo/rowcsv";

// Inside the existing try block; existing column checks and return values stay.
const rows = parseRows(text, {
  header: "first",
  blankRecords: "skip",
  duplicateHeaders: "last",
  bom: "preserve"
});

// Inside the existing catch block; otherwise retain the existing throw.
if (error instanceof CsvSyntaxError && error.reason === "UNTERMINATED_QUOTE") {
  return { status: 400, body: "Invalid CSV" };
}
```

This is a proposed adaptation derived from the supplied notes, not executed code or proof that the actual package exports work.

### Synthetic regression fixtures

All strings below use escaped LF and BOM characters to make the bytes unambiguous. Unless stated otherwise, exercise U1 through U2. Predicted outcomes follow the supplied documentation and source, not observed package execution. “Default target” compares behavior after the new exports load, before explicit preservation options and completed error mapping. In F2, the hypothetical stale handler checks the legacy `error.code`; importing a removed class would fail earlier and is separately covered by the module-load checks.

| Check | Synthetic input or fault | Current expected application result | Default target expectation | Planned target expectation / acceptance |
|---|---|---|---|---|
| F1 | `account,amount\n\nA1,7\n` | 200, `[{"account":"A1","amount":"7"}]`; empty line skipped | Same with translated skip option | Same; no intentional difference |
| F2 | `account,amount\n"A1,7\n` | `CsvError/CSV_BAD_QUOTE` becomes 400 `Invalid CSV` | `CsvSyntaxError/UNTERMINATED_QUOTE`; a handler checking legacy `error.code` would yield 500 | New narrow catch yields 400 `Invalid CSV`; no intentional HTTP difference |
| F3 | `\uFEFFaccount,amount\nA1,7\n` | 400 `Missing columns` because first header includes BOM | 200 after default BOM stripping | Explicit preserve yields 400 `Missing columns`; adopting new acceptance needs product approval |
| F4 | `account,amount,amount\nA1,5,7\n` | 200, `[{"account":"A1","amount":"7"}]` | Duplicate-header exception; U2 maps it to 500 | Explicit last-column-wins preserves 200 and final value `7`; rejection needs a separate product/error-response decision |
| F5 | U3 with `[{"account":"A1","amount":"7"}]` | Exact bytes `account,amount\nA1,7\n` | Same because U3 retains its own copy and explicit LF option | Exact bytes unchanged; compare archived-format fixture |
| F6 | Unit-level parser stub throws an unrelated `Error("synthetic fault")` | U1 rethrows; U2 yields 500 `Import failed` | Same unless error handling is widened incorrectly | Same; proves the catch is not broadened to all failures |

F6 tests application classification with a stub; it does not validate a package error class. F2 must also run against the real resolved target in the later authorized environment. The source-level plan alone cannot establish its result.

### Minimal later implementation and recovery sequence

The following steps are conditional instructions for later authorized execution of the exact `3.2.0` target. They have not been performed. Choosing an alternative version returns to planning and requires a revised inventory and matrix before any implementation.

| Step | Entry condition | Work and completion evidence | Hold condition |
|---|---|---|---|
| 1. Resolve support decision | Owner reviews R2 and E1 incompatibility | G1 decision checkpoint records owner-approved actual environments, candidate `engines.node`, CI and support documentation policy; resolve R2 through separately authorized support/runtime work. An alternative target exits this sequence and returns to planning | R2 still supports Node 18; proposed advertised range conflicts with target; owner decision or evidence missing |
| 2. Preserve and recheck baseline | G1 decision checkpoint passed; approved runtime/support work and baseline preparation authorized | Keep R42 intact. Prepare and verify a matched pre-dependency manifest/lockfile/source/runtime/deployable set plus CI and support documentation for the approved policy, including a support-only change and unchanged-runtime R1/R3 sharing that policy. Retain direct `rowcsv` `2.4.1` and existing audit resolutions; reconcile root lockfile metadata without dependency drift. Record checksums, npm 10.8.2 runner and F1–F6/existing-check results for every approved environment | Any artifact or support record is inconsistent; dependency versions drift; baseline checks fail; the newly approved policy/runtime lacks a verified matched set |
| 3. Make only required edits | Baseline passes; exact candidate support policy approved | Change direct dependency to exact `3.2.0`; adapt U1 as M2–M5 specify; carry forward and verify the approved baseline's `engines.node`, CI and support documentation as M1 requires. Close the G1 readback checkpoint against actual environments and the advertised range. Keep preserved R42 metadata, U2, U3 and audit adapter declarations unchanged | G1 readback fails; support policy is unknown; an edit lacks upstream/usage evidence; unrelated refactoring becomes necessary without explanation |
| 4. Resolve and review the tree | G1 closed; lockfile generation separately authorized in an isolated environment | Use the fixed runner with lifecycle scripts disabled and normal approved integrity/source controls; G2 captures the actual lockfile. Verify direct target, retained audit copies, all changed transitives, licenses, scripts/build needs and platform constraints before approving any newly discovered script execution | Unexpected nested drift, new access, unapproved scripts, unresolved license/platform concerns or missing metadata. Do not force a global override |
| 5. Run agreed checks | G1 and G2 satisfied; installation and tests authorized | Install from the reviewed frozen lockfile under the approved script policy. G3 contains module-load checks, F1–F6, existing application checks and build results across every approved environment, with exact versions and failures recorded | Any required check fails or remains unrun; an intentional behavior change lacks acceptance |
| 6. Review and consider release | G3 passes and consistent new artifact set exists | Review dependency/lock/U1 changes plus owner-approved candidate `engines.node`, CI and support documentation corrections; recheck G1 against the actual environments and advertised range. Obtain the applicable deployment authorization; preserve both old and candidate artifact sets and compare import error rates and audit output after any authorized release | Review, deployment authority or recovery access missing; unexplained production errors/output changes |
| 7. Recover if needed | An authorized release regresses and dependency rollback is authorized | Restore the verified pre-dependency set from step 2: application archive, manifest/engines, full lockfile, runtime image, CI and support documentation together. Preserve the approved support/runtime decision, including on unchanged-runtime R1/R3; rerun support-consistency checks plus import and audit smoke checks. Returning to R42's older support policy requires separate reversal authorization and a newly checked whole-set recovery plan | Matched artifacts/support records are missing; recovery would silently reverse the approved decision; restoring R42 would mix old engines with newer CI/support policy. Never assume its Node 18 worker artifact works on a new runtime. Investigate persistent/external effects before declaring recovery complete |

A dependency rollback does not by itself authorize undoing the separate runtime/support decision. For this target, retaining R42's original Node 18 support claim would conflict with the approved candidate policy, even on unchanged runtime binaries; use the matched step-2 set instead. There is no documented in-scope persistent import-format migration to reverse. U3's archive format is intended to remain unchanged and F5 checks that intent. If execution reveals new durable writes or emitted-file changes, stop and add an explicit data-recovery/consumer plan; reverting a version cannot undo already distributed files.

## What has and has not been verified

The accompanying `check_example.py` performs standard-library consistency checks on this fictional document: supplied range arithmetic, current and target version records, runtime-range judgments, the unresolved advertised-support mismatch and its conditional reconciliation gates, matched support-aware recovery coverage, source coverage, and matrix/fixture cross-references. It reads only this example. Its passing result does not test npm resolution, JavaScript imports, parsing, actual error classes, installation, builds, deployment or recovery.

Run the document check from this folder with `python3 check_example.py`. The checked-in example was inspected and this check passed. All actual baseline, package compatibility, lockfile-generation, platform and recovery tests remain UNRUN. The result is a decision-ready plan with a runtime HOLD and an unresolved target transitive tree, not a completed or approved upgrade.
