---
name: account-export-audit
description: "Audit already-downloaded account export parts against a stated migration or retention need and independent source evidence; reconcile records, relationships and attachment bytes before producing a supported snapshot copy."
---

# Find What an Account Export Actually Preserves

Answer a bounded source-side question: does this downloaded export preserve the objects and properties needed for the user's stated purpose? Return an inventory, specific gaps and the evidence supporting each coverage claim. When the evidence supports it and local copying is within scope, also produce a coherent consolidated copy that preserves identities and provenance.

Use this before depending on an export for retention or preparing a migration. An orderly archive, matching internal totals, a successful download and a file that opens are different observations; none independently establishes account completeness. This workflow does not import into a destination, test a backup restore, close an account or authorize deletion of source data.

## Establish the need and the denominator

Inspect supplied material before asking for what is missing. Resolve only choices that change the result:

- The account/workspace and selected collections, date range, object types and lifecycle states. Are archived objects, comments, deletion markers, shared objects or historical revisions required? Is the requested baseline a specific snapshot or the account as it exists now?
- The properties that matter: body text, original attachment bytes, relationships, timestamps and timezone, revisions, rich formatting, reactions or other domain-specific fields. A usable text copy may satisfy one retention need and fail another migration need.
- The downloaded files and the provider's supplied export-job, snapshot, part and format metadata. Record which archive names came from a receipt and which names merely look like a series.
- Independently supplied source evidence for that scope: a bounded authoritative listing, separately captured object IDs/revisions, a source collection view, an export-job receipt identifying its parts, or selected original attachments with hashes. Capture source, observation time, filters, pagination and access limitations for each item.
- An approved private output location and whether the task includes a consolidated local copy or only an audit. A selected export is not permission to upload it, share its contents or change the source account.

Do not manufacture an independent control by recounting the same export or treating its manifest as a second source. If only the downloaded archive exists, finish its internal inventory and structural checks. Call source coverage unconfirmed and name the smallest external evidence needed; do not invent a denominator. A user's hand-selected list can define a useful bounded check, but it does not prove the rest of the account is represented.

For a supplied-files-only request, do not access the account to fill gaps. When a user separately authorizes live source checks, use the existing supported read route within the named account and selection. Record any changed snapshot and paginate to a terminal result. If historical scope cannot be retrieved, keep the current listing separate instead of comparing today's source to an old archive as though they were simultaneous.

## 1. Preserve and inspect the delivered parts

Keep original downloads unchanged. Record each file's byte size and fresh digest, source filename, receipt reference and available snapshot/job metadata. A digest establishes a byte identity, not provider authenticity or coverage. Keep audit files separate from the original export and use a new output directory so a previous successful copy cannot be mistaken for a new held result.

Inspect container entries before opening payloads. Set bounded member-count, per-member and total expanded-byte limits appropriate to the actual small task; record when larger input needs a revised plan. Use installed standard archive, JSON and CSV tools. Do not install a converter, run bundled software or send files to an online service.

For archives, reject or hold entries whose location or type cannot be safely represented: absolute or escaping paths, link entries, duplicate/colliding names, encrypted members without an already-authorized supported route, excessive expansion, or unsupported container methods. Never extract everything into an existing directory. Read bounded regular members as data or write explicitly selected members with exclusive creation after validating their paths. Do not recurse through nested archives automatically. Preserve two distinct attachment IDs even when they share a filename.

Parse data without opening stored links, loading remote resources, executing scripts/macros or interpreting formula-like CSV cells. Decode with the evidenced encoding; retain a parse failure as an unavailable member rather than dropping it. Detect duplicate JSON object keys before they can silently overwrite a value. A familiar extension alone does not establish the schema.

An export may contain authentication-bearing URLs, signed download links or recovery material. Keep those values out of derived reports, inventories and consolidated shareable copies; retain only a source/object locator and the reason for holding that content. Leave the untouched private original in place. Ordinary non-secret query strings are data and should not be stripped merely because they contain parameters. If this makes a required item unavailable, report the exact limitation without copying the credential into the explanation.

## 2. Separate snapshot families before joining anything

Group parts using the strongest supplied combination of account identity, export request/job ID, snapshot generation/time, selected filters, format version and part membership. Filename order, filesystem modification times and similar titles are weak hints. If the provider format does not expose a snapshot generation, record that absence and use its documented consistency guarantees or hold cross-part consistency as unknown.

For each candidate family, reconcile:

1. The independently identified required part set against supplied parts, including any manifest/index parts that have no records
2. Each part's ordinal or ID and continuation chain, including the starting boundary and an explicit terminal marker where the format provides them
3. Local declared record/member totals against parsed contents, separately from external source coverage
4. Duplicate IDs or repeated pages, missing pages, unresolved cursors and contradictory scope or format metadata

Two files named part 1 and part 2 can belong to different export attempts. A later part cannot repair an earlier snapshot merely because it has the missing object. Hold that part with its identity and the affected overlap; do not merge the newer revision into the earlier copy. Conversely, a held unrelated generation does not prevent completion of an independently supported, coherent selected family. Keep it visible as excluded evidence.

Do not call a listing complete because it contains the expected number of rows. A count can agree while one identity is missing and another duplicated or substituted. If a continuation token or part receipt remains unresolved, coverage remains unconfirmed even when the visible totals happen to match.

## 3. Inventory objects and dependencies without changing their meaning

Build one lineage record per source occurrence before deduplicating. Keep native IDs as strings, including leading zeros. Record object kind, lifecycle state, revision, parent/owner IDs, attachment references, supplied timestamps, archive digest, member and row/index location. A locally derived ordinal is a locator, not a provider object ID.

Preserve original field values and distinguish these cases:

| Observation | Meaning to retain |
| --- | --- |
| Empty string, empty list, zero or false | Present values; not missing merely because they are false-like |
| Explicit null | A supplied null, subject to the source format's meaning |
| Omitted field | Unknown, unsupported, redacted or intentionally absent only when evidence establishes which |
| Deletion marker/tombstone | Evidence of deletion at a stated revision/time; not the deleted body and not an object missing by accident |
| Object expected by an independent selection but not found | Missing from supplied evidence; not proof it was deleted or never existed |
| Object outside the requested filter | Explicit exclusion; not an export failure unless the required scope was broader |
| Same ID with different revision/body or parent | Conflict requiring snapshot or format evidence; no first/last-row winner |

An exact repeat can still be meaningful, such as an event occurrence. Collapse duplicate representations only when the real format documents that behavior or the user supplies the rule. Keep the lineage of all occurrences. Unknown fields stay in the untouched original and, when appropriate and safe, the consolidated raw object. Do not simplify IDs, flatten relationships, replace unsupported enums or synthesize missing content to make a copy look complete.

Check every required parent and attachment reference. Separate a reference to an explicitly excluded scope boundary from a missing required dependency. If the user's need requires a self-contained subtree, even a valid external parent/reference can block that requirement; do not invent a placeholder object. If a supplied stub legitimately preserves the reference, label it as a stub and identify what is unavailable.

Match attachments by stable ID plus owner/reference, not basename. For each expected attachment, record available payload, original path, content type if supplied, byte length, digest and the evidence for expected bytes. Report missing payloads, unexpected payloads, duplicate path identities, changed bytes and absent ownership separately. A URL to a remote file is a reference, not preserved attachment bytes; do not fetch it under an offline audit. Matching archive-local hashes proves internal consistency only. A separately supplied original digest can support a stronger byte-fidelity claim, with its provenance stated.

Derive the required attachment set from the selected object references, then reconcile the independent attachment-control rows to that full set. A missing control row must not erase an expected attachment. If the size/digest evidence is incomplete or duplicated, leave the total expected bytes unconfirmed and identify the affected references. Distinguish repeated references to one legitimate shared attachment from duplicate identities or contradictory owners under the actual source format.

## 4. Reconcile coverage against the independent controls

Validate the controls before trusting their denominator: same account, selected filters, object kinds, lifecycle states and snapshot/revision boundary; all required pages retrieved; no unexplained repeated or missing identities. A UI total may omit archived objects or count attachments separately, so first establish what its number means. Permission-hidden objects, delayed generation and partial enumeration remain limitations.

Compare exact identities and required properties, then use counts as a cross-check. Keep separate ledgers for expected objects, unexpected exported objects, explicitly excluded controls, attachment references and physical attachment payloads. For each expected object, assign one outcome: matched for the required properties, missing, or conflicting/unresolved. Extra exported objects do not cancel missing expected ones.

Useful reconciliations include:

```text
expected selected objects = matched + missing + conflicting/unresolved
expected selected attachments = byte/ownership matched + missing + conflicting/unresolved
selected record attachment references ↔ expected attachment IDs and owners
physical payload paths ↔ referenced attachment identities
verified attachment bytes = sum of individually verified payload lengths
required part IDs = supplied supported part IDs + missing required part IDs
```

Report the property-level denominator: five objects can match identities while only four required bodies are present. Hashes for two attachments do not establish text fidelity for the record bodies. Missing rich formatting, history or permissions can matter even when every object ID appears. Let the stated need decide whether a gap is blocking; make tolerated exclusions explicit rather than quietly lowering the requirement.

## 5. Move from evidence to the allowed local action

| Evidence and authority | Allowed next result |
| --- | --- |
| Archive parses; independent source scope unavailable | Internal inventory and gap report; no source-completeness claim |
| Some required parts, records or dependencies unresolved | Inventory and exact missing evidence; hold the consolidated complete-copy result |
| Known filtered scope is fully reconciled; properties required by the stated need are supported | Produce the authorized local snapshot copy and its provenance |
| A missing same-generation part arrives | Re-run affected checks against immutable inputs; release only the newly supported result |
| New part conflicts in generation, scope or identity | Keep it separate; identify its overlap and hold dependent joins |
| All archive objects exist but independent pagination is incomplete | Report internal consistency; source coverage remains unconfirmed |
| User requests later upload, import, sharing, account closure or deletion | Treat that as a distinct action with its own target and authority; this audit does not establish destination behavior or authorize destructive follow-through |

A partial working copy can be useful when explicitly wanted, but label it as partial and list omitted source IDs and dependencies. Never place it where a downstream consumer expects a complete copy. When a coherent copy is supported, write exact raw records and selected attachment bytes without schema conversion, plus a separate lineage file. Preserve IDs, nesting/reference edges and distinct filenames through their original paths or an explicit reversible path mapping. Record any unavoidable representation loss before claiming suitability.

Reopen the saved output with the intended parser. Independently compare IDs, revisions, lifecycle states, parent/reference edges, required field presence and attachment byte digests to both selected parts and external controls. Check that the held generation contributed no object or payload. Rehash originals or verify their immutable versions after the read/copy. A successful audit script run is not enough if the saved copy differs from the plan.

## Deliverable and stopping condition

Return the actual inventory and gap report. Include the usable consolidated copy only when supported or the clearly labeled partial copy specifically requested. A compact report should answer:

```text
Need and scope: account, selection, snapshot, required properties, explicit exclusions
Evidence: independent controls, archive identities, filter/pagination/part limitations
Accounting: objects, states, relationships, attachments and bytes with denominators
Gaps: affected IDs/source locators, missing or conflicting property, smallest next evidence
Copy: supported/held/partial; exact contents and provenance; preserved versus untested fields
Boundary: what was checked offline and which live-source/destination behaviors remain untested
```

Stop when the stated need is supported, or when the remaining result depends on a specific missing source/control or user decision. Do not broaden a narrow retention check into an account-wide investigation. Do not describe an offline export as safe grounds to close an account or erase originals. That requires separate decisions and evidence beyond this workflow.

## Worked account export

The [worked example](example.md) contains an original fictional collection with current and archived notes, a comment, a deletion marker and two same-named attachment files. Its separately authored [source inventory](fixtures/source-inventory.csv) and [control evidence](fixtures/source-control.json) define the denominator. The downloaded ZIPs are tiny and contain data only.

The example's [adapter](scripts/audit.py) supports only its declared fictional JSON layout. Use it to reproduce the evidence transitions, not as a universal account-export parser. For a real service, first inspect its actual supplied format and establish a schema-specific adapter using the same checks. Do not rename a real manifest's schema to bypass this boundary.

Read the [partial report](outputs/partial/report.md), [resolved report](outputs/resolved/report.md) and [incomplete-control report](outputs/incomplete-control/report.md). The [verification record](verification.md) lists executed checks, exact archive identities and the offline limits. Reproduce the behavioral and saved-output checks with:

```sh
python3 -B scripts/verify.py
```
