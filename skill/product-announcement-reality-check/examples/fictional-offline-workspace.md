# FICTIONAL worked example: what shipped in an offline-workspace launch?

The product, vendor, publication, dates and feature behavior below are entirely invented. MOCK-P labels identify only these supplied excerpts; they are not URLs or real documentation. No live retrieval, account access, installation or functional test was performed. Real use of the skill requires retrieving applicable current primary sources and reporting what was actually inspected.

## Supplied task

Assess the fictional Threadline Notes 3.4 release for a Windows desktop team on the Standard plan in the EEA, as of 2030-05-09 12:00 UTC. The user wants a private capability matrix and has not requested signup, installation or purchasing.

Requirements:

- R1: Search the full text of previously downloaded PDF attachments while disconnected
- R2: Export annotations from one PDF to a file on Windows, without switching plans
- R3: Bulk-export an entire notebook as PDFs without an invitation or a regional exception

These are must-haves for the user's intended evaluation. Merely opening a cached note does not satisfy R1.

## Supplied mock evidence

### MOCK-P1: Vendor launch page, headline and availability paragraph

- Publisher: fictional Threadline Tools
- Publication: 2030-05-06 10:00 UTC
- Supplied capture: 2030-05-09 10:00 UTC
- Headline: “Offline Workspace and effortless PDF exports are here.”
- Paragraph: “Threadline Notes 3.4 brings Offline Workspace to desktop. Single-PDF annotation export is available today on Pro. Notebook export starts with an invitation preview; broader access is planned for June.”
- A demo shows one invited account bulk-exporting a notebook. Its region and plan are not visible

### MOCK-P2: Desktop 3.4 guide, “Offline Workspace”

- Publisher: fictional Threadline Tools
- Publication: 2030-05-06 10:00 UTC
- Supplied capture: 2030-05-09 10:05 UTC
- Excerpt: “Offline Workspace is the new name for Cached Notes. It opens previously downloaded notes and attachments. Full-text indexing and search of PDF attachments require a connection in version 3.4.”
- Scope: Windows and macOS desktop version 3.4

### MOCK-P3: Export eligibility table, release 3.4

- Publisher: fictional Threadline Tools
- Publication: 2030-05-07 09:00 UTC
- Supplied capture: 2030-05-09 10:10 UTC

```text
Single-PDF annotation export:
  Stable desktop 3.4, Windows and macOS, Pro plan
  Standard plan: not included
Notebook bulk PDF export:
  Invitation preview, Team plan, North America only
  EEA preview access: not available
  Future broader-release plan: no fixed release date in this table
```

### MOCK-P4: Independent review, method note and observation

- Publisher: fictional Desk Tools Review, separate from the vendor
- Publication: 2030-05-08 16:00 UTC
- Supplied capture: 2030-05-09 10:15 UTC
- Method excerpt: “We used desktop build 3.4.0 on Windows with a Pro account. With the connection disabled, a previously downloaded note opened. Searching for a unique word present only inside its attached PDF returned no result. The word became searchable after reconnecting.”
- The reviewer did not test Standard, notebook bulk export or other product builds

### MOCK-P5: Vendor web help, undated and unversioned

- Publisher: fictional Threadline Tools
- Supplied capture: 2030-05-09 10:20 UTC
- Excerpt: “Search across everything in your workspace.”
- It does not specify offline operation, supported attachment types, plan or release
- Accessible coverage: that paragraph only

## Expected capability matrix

**R1: Offline full-text PDF search.** Documented mismatch for desktop 3.4. MOCK-P2 explicitly requires a connection for PDF indexing and search. MOCK-P4 is independent, method-described observation consistent with that limitation on one Windows build and Pro account. The vague wording in MOCK-P5 does not resolve the missing offline condition and should not outweigh applicable version-specific documentation. Do not generalize the review into a test of every build or plan.

**R2: Single-PDF annotation export on Standard.** The feature is documented as shipped on Windows desktop 3.4 for Pro, but the user has Standard, which MOCK-P3 explicitly excludes. Record behavior as supported for the eligible product scope, access as generally available within that scope, and the user's requirement result as documented mismatch. “Not shipped” would be incorrect globally; “available to this user” would also be incorrect.

**R3: Invitation-free notebook bulk export in the EEA.** The demonstrated capability exists in an invitation preview, but the applicable access conditions exclude the requested region and require a different plan. Record access as limited preview, the current user-scope result as mismatch, and future broad availability as unestablished. The launch's June statement is a plan, not a delivery date or promise that the user's exact configuration will qualify.

## Expected bottom line

“The supplied mock documents do not establish a match for the three must-haves in the stated Windows/Standard/EEA setup. Offline PDF search is explicitly outside the documented 3.4 offline behavior; single-PDF export is restricted to Pro; and notebook export is an invitation preview outside the stated region. The broad launch wording and demo do not remove those restrictions.”

In an actual run, replace the mock evidence with inspected primary sources and attach direct citations and real retrieval times to the conclusion.

The next useful user decision is whether any requirement or supplied access condition should change before doing more evaluation. Do not recommend a paid upgrade as though it would resolve all three requirements, register for the preview, install software or contact the vendor without an applicable request and authorization.

## Expected provenance and checks

- MOCK-P1, P2 and P3 are different first-party documents, not three independent confirmations of performance
- MOCK-P2 explicitly links the new name to Cached Notes; the renaming does not establish additional offline behavior
- MOCK-P4 supplies independent observation but only for its stated build, method and account
- MOCK-P5 is less specific, not automatically false; its omitted conditions cannot establish offline search
- Publication, capture and stated future availability remain separate fields; the June plan is not a release event
- No functional test was performed by the assistant, and no file was exported during this exercise

The expected artifact contains three requirement records, five source records, one third-party observation record and the bounded bottom line. These are expected exercise results, not evidence that a real product was tested or that a live availability check passed.
