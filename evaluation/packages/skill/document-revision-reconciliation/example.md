# Fictional example: two archive-guide branches

All names, revisions, messages and document content here are synthetic. The example uses a Markdown candidate with fixed section identifiers, not a native-document service.

## Request and source evidence

The fictional user says: “Use base-r4. Apply the Export wording from branch-a-r5 and Purpose wording from branch-b-r8. Make a private candidate. Keep the section headings and order, and keep Attribution exactly. Leave the cover at the baseline wording while I decide, with both choices in a separate question list.”

The common baseline has four stable section IDs:

- PURPOSE: “Prepare image entries for the archive.”
- EXPORT: “Use numbered filenames.”
- COVER: “Use a gray cover.”
- CREDIT: “Keep the supplied creator credit exactly as written.”

Branch A changes EXPORT to “Use the entry identifier as the filename.” and COVER to blue. Branch B adds descriptive alt text in PURPOSE and changes COVER to green. Branch B has the later modification timestamp. The user accepts its PURPOSE edit, not all of Branch B.

## Reconciliation and candidate

Apply E1 at EXPORT from branch-a-r5 and E2 at PURPOSE from branch-b-r8. Each accepted row names its source revision, semantic snapshot digest and fictional-user-message-21 as the acceptance basis. Keep the same heading order and exact CREDIT wording.

The candidate body becomes:

> Purpose: Prepare image entries and descriptive alt text for the archive.
>
> Export: Use the entry identifier as the filename.
>
> Cover: Use a gray cover.
>
> Attribution: Keep the supplied creator credit exactly as written.

Mark the document as a draft candidate. Its COVER sentence is retained because the user explicitly requested that temporary treatment, not because gray was newly approved. The unresolved record asks: “Should the archive guide use the blue or green cover?” and points to the two branch revisions. Do not mark the whole document approved.

## Executed local checks

From this folder, run:

```sh
python3 -B check_example.py
```

This prints a fresh result to stdout and leaves the bundled evidence file unchanged.

The checked script embeds the fictional source snapshots and decisions, exercises them, saves a candidate to a temporary folder inside this skill folder, reads that file back, then removes the temporary folder. It writes no real document or account. The checked result is in [example-results.json](example-results.json), including the actual Python version, platform, source/candidate digests and decision ledger.

Observed checks cover exact accepted edits, both unresolved alternatives, unchanged protected wording and sources, refusal of stale source approval, ambiguous anchors and a protected edit. Moving Branch A's timestamp into the distant future does not change the result. A simulated destination edit is refused without overwriting it; a subsequent explicitly current write is saved and read back.

The model accepts only whole-text edits at fixed unique section IDs and deliberately refuses remapping. It does not test native document IDs, tracked changes, formatting, concurrent remote writes or permissions. Real work requires the actual format-aware tools, authority evidence and destination checks described in the skill. The local preflight is a behavioral demonstration, not a claim of atomic concurrency protection.
