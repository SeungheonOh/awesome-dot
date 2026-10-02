# Riverdesk Bookmark Transfer

## Request and result

Fictional request: “Prepare this bookmark export for a desktop browser that accepts bookmark HTML. Put it under one clearly named migration folder. Keep every folder and repeated placement. Set aside malformed addresses and non-HTTP(S) entries for my review. Give me the file and a reconciliation record; do not import it into a browser yet.”

**Result: prepared only, with exceptions.** [import-ready.html](import-ready.html) contains 8 link occurrences inside the original 7 source folders plus the new `Riverdesk migration • 2026-10-02` wrapper. Seven source link occurrences are held in [lineage.json](lineage.json) and remain unchanged in [source-bookmarks.html](source-bookmarks.html). None were deleted or silently repaired. There is no claim that these links were imported, opened, reachable or safe.

The source is an original fictional fixture, not an export captured from a real user profile. Its `.example` destinations and exporter IDs are invented. It follows the bookmark HTML structure used for this rehearsal. Native IDs shown here demonstrate lineage handling; real exports may omit them.

## Accounting and placement

| Item | In source | In prepared HTML | Held outside the import |
| --- | ---: | ---: | ---: |
| Source folders | 7 | 7 | 0 |
| Added wrapper folder | 0 | 1 | 0 |
| Link occurrences | 15 | 8 | 7 |

The wrapper contains this ordered tree. Bracketed ordinals distinguish the two identically named `Reference` folders; those annotations are not added to the actual folder names.

```text
Riverdesk migration • 2026-10-02
├── Bookmarks Bar
│   ├── Software & work
│   │   ├── Reference [first sibling]
│   │   │   ├── Riverdesk API & error guide
│   │   │   ├── Café UI — 日本語
│   │   │   └── [originally blank title]
│   │   ├── Reference [second sibling]
│   │   │   ├── Release checklist
│   │   │   └── Release checklist
│   │   └── Empty • later
│   ├── Everyday / Quotidien
│   │   ├── Montréal – accès
│   │   └── Riverdesk API & error guide
│   └── Needs review [now empty in prepared subset]
└── Archive notes
```

The same-folder checklist appears twice, with separate source IDs. The API guide appears once in each of two folders, with different metadata in each placement. Both relationships are preserved. The archive URL remains HTTP, and query strings, fragments, percent escapes and Unicode are unchanged. The slash in `Everyday / Quotidien` is part of its title, not a folder separator. Ordinal arrays in the lineage record express the actual boundaries.

The source toolbar marker is retained in the sidecar, not applied to the generated folder. This deliberately places the complete source tree inside the wrapper. Whether a browser adds its own outer import folder remains untested.

## Held occurrences

All seven entries belong to `Bookmarks Bar → Needs review`. Their original attributes, titles, source positions and URLs are preserved in the sidecar and original export. They are absent from import-ready.html.

| Source exporter ID | Original address | Disposition and decision |
| --- | --- | --- |
| fixture-no-host | `https://` | Malformed: host absent. Request the intended address; do not invent one |
| fixture-bad-escape | `https://riverdesk.example/%ZZ` | Malformed percent escape. Request the exact correction |
| fixture-internal | `about:preferences` | Browser-internal scheme. Determine the intended target feature before recreating it |
| fixture-file | `file:///fictional-notes/reading.html` | Local file reference. Verify the target-device file and requested treatment before adding |
| fixture-mail | `mailto:team@riverdesk.example` | Valid type of link, outside this HTTP(S)-only preparation rule. Ask whether to include it using supported target behavior |
| fixture-bookmarklet | `javascript:void(0)` | Inert fictional bookmarklet. Retain as data; decide target treatment without executing it |
| fixture-no-href | HREF attribute absent | Missing address. Preserve the record and request the intended URL |

The held set is a preparation choice from the fictional request, not a claim that every browser rejects these schemes. No destination was contacted to classify them.

## Preservation evidence

| Property | Offline result | Live target status |
| --- | --- | --- |
| Parent/child boundaries and sibling order | Exact match after adding one wrapper and excluding held links | Not tested |
| Same-name folders and empty folders | Both `Reference` folders remain separate; `Empty • later` and emptied `Needs review` remain | Not tested |
| Titles and URL strings | Exact decoded string match, including blank title and Unicode | Not tested; a browser may normalize a URL or generate a title |
| Duplicate placements | Two checklist occurrences and two API guide placements retained | Not tested |
| Dates, tags, keyword and description | Carried in prepared HTML where present; original values also recorded | Retention not established |
| Icon URL and toolbar marker | Preserved in sidecar; omitted from the prepared HTML | Not transferred in this artifact |
| Source IDs | All 21 supplied IDs retained in the sidecar | Destination IDs unknown |
| Missing source ID | Archive entry has an export-digest + occurrence anchor; native ID stays null | Destination ID unknown |
| Original source bytes | Recorded SHA-256 still matches | Live source coverage not established |
| Existing destination bookmarks | No destination accessed or changed | Backup, pilot and comparison not performed |

Every source item has one record with a native ID if available, an export-local lineage ID, parent lineage ID, zero-based ordinal path, title, attributes, description, source line, disposition and planned output position. Custom lineage attributes in the prepared HTML aid inspection of the file; no browser persistence of those attributes is assumed.

Source SHA-256: `ae3aa6800123ca1f4d5999e1e29024227068c97bbb2a7ebc751012e59030c7df`

Prepared SHA-256: `f850819763b29f8b1bd989be82d040c8d345080e08f1f0a4e04e3e6cef8ebfb1`

Matching these digests identifies this exact fixture and transfer; it does not authenticate an exporter or prove that a real profile was completely exported.

## Next step and recovery boundary

For an authorized live migration, identify the target browser/version and profile, inspect its existing tree and sync scope, save and read its supported backup, then pilot the prepared structure. Re-export/read back the pilot to establish actual title, hierarchy, duplicate and metadata behavior before completing the import. If a user-required field is lost, pause for that specific decision.

Record the actual new target subtree and IDs. A later authorized reversal can remove only those unchanged additions after confirming there are no new user edits, followed by a comparison with the target baseline. This is a proposed recovery method, not an executed recovery test. A native restore may replace existing data and must not be used as an automatic fallback.

The [verification record](verification.md) describes the offline tests and deliberate failure cases that were actually run. The [official browser notes](browser-methods.md) identify the supported route references checked for future live work.
