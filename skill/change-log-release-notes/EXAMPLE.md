# Fictional Example: One Release, Two Audiences

All products, changes, records, dates, and source identifiers below are invented. There are no live release links or publication actions. The expected outputs show editorial transformations of this supplied packet, not a verified deployment of a real product.

## User request

“Draft the Quillroom 2.6 update for customers and a separate version for integration developers. Use the release record below, keep rollout restrictions visible, and include anything people must change. Put unconfirmed claims in an editorial list. Return both drafts here.”

## Source packet

### R-26: Release record

Snapshot: 2026-10-01 at 09:00 UTC. Version: Quillroom 2.6.

- Web changes C-202 and C-205 are included in the version deployed on 2026-10-01
- API v2 change C-203 is deployed to all API v2 clients on 2026-10-01
- C-201 is present in the build but flag-controlled; P-201 is the authority for actual availability
- C-204 and C-206 are excluded from this release
- This packet contains no mobile release record

### C-201: Saved views

Merged change: users can save a document-list filter as a named view and reopen it from the document list. The change description calls the feature “Ready for everyone.” Actual rollout is controlled separately.

### P-201: Saved views rollout record

State checked: 2026-10-01 at 08:45 UTC.

- Pilot is active only for invited Team-plan workspaces using the web app
- A workspace owner must enable Saved views under Settings → Experiments before members can use it
- Saved views are visible only to the person who created them; sharing a view is not supported in the pilot
- No date for broader availability has been approved

### C-202: CSV export correction

Acceptance evidence: CSV exports of document titles and tags now preserve commas and accented characters in the title field. The fix applies to new exports for all web plans. Previously downloaded CSV files are unchanged; users need a new export to obtain the corrected output. Export does not include document comments.

This entry does not claim that every CSV issue is fixed, that old files are repaired, or that mobile export changed.

### C-203: Bulk update request limit

API v2 contract:

- Endpoint: `POST /v2/documents/bulk`
- Previous maximum: 500 records per request
- New maximum: 100 records per request
- A request containing more than 100 records returns HTTP 422 and changes no records
- Integrations sending larger requests must split them into batches of at most 100
- No automatic client-side batching or compatibility grace period is provided by this release

### C-204: “Search is twice as fast”

An issue title contains this phrase. The associated index work is unfinished and excluded from R-26. There is no benchmark or measurement in the supplied packet.

### C-205: Internal export-module cleanup

Renames local variables and removes a duplicate internal helper. Included in R-26. The source states there is no public interface or intended behavior change.

### C-206: Download workspace archive

The implementation is merged, but R-26 explicitly excludes it. The packet provides no release date or availability claim.

## Expected customer draft

```text
Quillroom 2.6 · October 1, 2026

Action for teams using API integrations

API v2 bulk document updates now accept at most 100 records per request, down from 500. If your integration sends larger batches, update it to split them into batches of 100 or fewer. Larger requests are rejected without changing records.

CSV title exports corrected

New CSV exports preserve commas and accented characters in document titles. This fix is available on all web plans. Download a new export if you need corrected output; existing files are unchanged. Exports still do not include document comments.

Saved views pilot

Invited Team-plan workspaces can try Saved views in the web app. A workspace owner must enable it under Settings → Experiments. You can then save a document-list filter as a named view and reopen it from the document list. Views are personal and cannot be shared during the pilot. There is no approved date for broader availability.
```

## Expected developer draft

```text
Quillroom 2.6 developer notes · October 1, 2026

Breaking change: API v2 bulk updates

POST /v2/documents/bulk now accepts a maximum of 100 records per request, reduced from 500. This limit is deployed to all API v2 clients.

Requests with more than 100 records return HTTP 422 and change no records. Split larger batches into requests containing at most 100 records. The release provides no automatic client-side batching or compatibility grace period.

Web CSV export correction

New exports of document titles and tags preserve commas and accented characters in the title field on all web plans. Existing CSV files are unchanged and must be exported again to receive the correction. Document comments remain excluded from export.

Web pilot: Saved views

Saved views are available only to invited Team-plan workspaces. A workspace owner must enable the feature under Settings → Experiments. Members can then save a document-list filter as a named view and reopen it from the document list. Saved views are personal and cannot be shared in this pilot. There is no approved broader-release date.
```

The customer version keeps the integration warning because dropping it would hide a required action. The developer version preserves the exact endpoint, response status, batch contract, and rollout reach. Neither version generalizes web evidence to mobile.

## Coverage and claim ledger

| Input | Decision | Supporting evidence and retained limits |
| --- | --- | --- |
| R-26 | Establish version, release date, and inclusion | Supports shipped C-202/C-203; refers C-201 availability to P-201; does not establish a mobile release |
| C-201 + P-201 | Include as Saved views pilot | Named personal views; web only; invited Team workspaces; owner opt-in; no sharing; no approved broader-release date. Ignore the broader claim in C-201's description because the actual rollout record is narrower |
| C-202 | Include as a bounded export correction | New exports; commas and accented title characters; all web plans; old files unchanged; comments excluded |
| C-203 | Include first as a required compatibility action | 500 → 100; API v2; exact endpoint and HTTP 422 in developer copy; no records changed on oversized requests; explicit batching action; no client batching or grace period in developer copy |
| C-204 | Hold out of both drafts | Unfinished and excluded from R-26; no benchmark supports the issue-title claim |
| C-205 | Omit from both audience drafts | Internal cleanup with no public interface or intended behavior change; accounted for here so it does not become a missing source |
| C-206 | Omit from this release | Merged but explicitly excluded; no date or availability inferred |

## Editorial questions kept out of finished copy

- C-204: Do not use “twice as fast.” A future release needs both inclusion evidence and a measured result with a defined workload before making that claim
- C-206: Leave archive downloads out until an actual release record establishes inclusion and availability
- P-201: Do not promise a general-availability date. The current pilot restrictions are sufficient to describe the feature accurately

These are evidence gaps, not reasons to block the two supported drafts. The workflow can deliver the requested notes now.

## What a destination-authorized variation would do

If the request instead said, “Write the developer version into the existing draft 2.6 section of local CHANGELOG.md,” inspect that section, replace only the requested draft content, and read it back. Preserve older entries and unrelated worktree edits. Return the file path and verified draft status. Do not ask the user to approve the same local edit again, and do not create a tag or publish a release from that wording alone.

No file write to a changelog or publication is claimed in this example; the actual request above asked for two drafts in the conversation.

## Check the example by tracing meaning

- Every supplied change has a disposition, including both omitted changes and the held performance claim
- The breaking limit and batching action survive in both outputs
- The title “Ready for everyone” does not override pilot evidence
- The corrected export cases do not become an unsupported claim about all export behavior
- “Merged” is not rewritten as “shipped” for the archive feature
- No link, migration deadline, mobile availability, performance metric, or public publication is invented
