# Example verification

Checked on October 1, 2026. All observations, roles and decisions in this example are fictional. The deck is an authored demonstration, not a proposal for a real organization.

## Artifact identity

- [Editable five-slide deck](intake-pilot-example.pptx): 30,974 bytes
- SHA-256: `5a6f96c48ac27b1c69da980096e12d4c0025547c2aafc99c7065a7e47eda9815`
- Five slides, 16:9 canvas, five complete speaker-note sections
- One native chart with an embedded data workbook; no full-slide raster pictures
- [Slide preview](preview.png): 363,240 bytes, SHA-256 `e6297229ac3deb0540d4ac6c53358d8a21045cc1fb800abfa616599292644a02`. This contact sheet uses renders from that exact deck. It is a visual aid, not the editable deliverable

The [source packet](source-packet.md), [full slide script](slide-script.md) and [content specification](deck-spec.json) are portable source materials. They contain the complete copy, chart values, caveats, sources, notes and design decisions. They do not depend on downloading a template or finding missing source material.

## What actually ran

An available presentation authoring capability created and exported the PPTX. The file went through package and geometry checks, then an exact-file re-import and raster render of all five slides. Each final slide was inspected individually at 1280 × 720, followed by a contact-sheet inspection for story and design consistency. This is actual rendered inspection, not a review of XML alone.

The initial export included generic software metadata and lacked the intended native title placeholders. Those metadata issues were repaired before the final package checks and final renders. The final chart includes descriptive alternative text. No visual rendering or application-editing result from an earlier version substitutes for the final-file checks reported here.

The included checker uses Python 3 and the standard library. From this folder:

```sh
python3 check_example.py
python3 check_example.py intake-pilot-example.pptx
```

Both content and package checks passed. The checker is independently runnable for the supplied example. It does not recreate or render the presentation, and its package success does not prove application compatibility. The authored specification supports reconstruction with an available presentation editor; no portable, automated rendering build is claimed.

## Evidence and source checks

| Slide | Evidence checked | Result and important boundary |
| --- | --- | --- |
| 1 | Four-workweek extension, October 5–30, one queue, existing coverage cap, no new spending | Matches S0 and S3. The visible caveat keeps the extension and staffing unapproved. Opportunity cost remains in notes |
| 2 | 18-hour and 12-hour medians, 40 and 60 completed requests, windows and unit | Matches S1. The observed difference is six hours. Both chart bars start at zero on a 0–24-hour axis. S2's nonrandom/completion-only limits remain visible. Individual durations were not supplied, so the medians were not independently reconstructed |
| 3 | Reopening counts and fractions, full seven-day follow-up | 4/40 = 10.0%; 7/60 = 11.666…%, displayed as 11.7%. Counts remain visible. The slide does not claim quality equivalence or statistical significance |
| 4 | Proposed roles, additional records, weekly coverage cap and November 6 review | Matches S2 and S3. Notes retain completion-time logging, opportunity cost and unaccepted responsibilities. The cap is not a labor-saving claim |
| 5 | Proposed 12-hour, 12% and eight-staff-hour review rules, serious-failure pause | Matches S0 and S4. Thresholds remain proposals. Separate expansion approval and the limits of threshold passing remain in notes |

Six source anchors resolve in the packet. Every slide has source locators in its notes and a source footer. The PPTX contains ten hyperlink relationships pointing only to the public repository's source-packet sections. Their exact URL strings and section existence in the supplied packet were checked. The downloaded deck does not require a local companion to follow those public links. Public URL resolution must be checked during publication; app-level clicking was not tested. The companion script retains local Markdown links for repository browsing.

The deck identifies fictional packet version 1, dated 2026-10-01, with SHA-256 `5d14e97515765e190d776989b03cc59412e6169d4ccdb714585eee78b00e799f`. The public URLs follow the repository's main branch and may change. This snapshot identity appears in every slide's speaker notes so readers can distinguish the reviewed source from a later revision.

The unapproved “every request became 33% faster,” “quality was unchanged” and “saved eight staff-hours” claims are recorded as rejected claims in the companion materials, not findings in the deck. Two negative checks passed: changing a chart value and breaking a source anchor each caused the content checker to fail.

## Native objects and file hygiene

- Slides 1–5 contain respectively 7, 5, 12, 7 and 8 native text shapes. The text and notes match the complete specification
- All five slides contain native title placeholders. Slide 2 contains a native column chart, descriptive chart alternative text, category labels and value labels
- Chart values and embedded workbook values are `[18, 12]`, with category order “Baseline: 40 requests,” then “Pilot: 60 requests.” The workbook is a snapshot of the supplied literal values, not the unavailable request-level dataset or an original formula model
- Package/chart checks verified the chart's workbook references and cached values during export. The final package checker independently compared the chart values, category order and embedded workbook values with the source specification
- The final package and geometry checks returned no findings. Encoded text uses DejaVu Sans, and the preview showed readable text without missing glyphs
- Core authorship metadata is the neutral label “Fictional workflow example.” Slide and note metadata counts are five. No personal metadata, local absolute paths, hidden slides, comments, macros, unexpected external targets or software-identifying metadata were found in the inspected XML and embedded workbook
- The contact-sheet PNG contains no personal or application metadata

## Visual and accessibility review

The final slides had no observed clipping, overlapping text, missing labels or broken glyphs at the inspected size. Slide 1 keeps the request and its unapproved status distinct. Slide 2 retains the zero baseline, readable values and sampling caveat. Slide 3 shows both fractions and denominators. Slide 4 wraps its longer logging instruction without cutting it. Slide 5 keeps the proposed thresholds and separate expansion decision visible.

The design uses a light background, dark native text and one blue chart without decorative imagery. Titles, body copy and source/caveat text have a consistent hierarchy. The chart uses labels and values so color is not the sole signal. Against the authored background, calculated text contrast ratios are 13.06:1 for the main text, 7.24:1 for the blue accent and 6.97:1 for secondary text. The source and caveat text is 18 pt, and the smallest chart labels are 18 pt. Essential chart data and interpretation also appear in notes and the companion transcript.

These are design and package checks, not an accessibility certification. Target-application reading order, font substitution, assistive-technology behavior and native chart editing were not exercised.

## Remaining limits

- PowerPoint and Google Slides were not used to edit, save and reopen this file. Native objects exist in the PPTX, but application-specific editing and import fidelity remain untested
- Public source URLs follow the main branch and may change. Their published resolution and target-application clicking were not established by this artifact check. The recorded packet version, date and SHA-256 identify the reviewed snapshot
- Rendered inspection cannot prove all presentation modes, projection sizes or screen-reader behavior
- The fixture is synthetic and the supplied summary statistics are not independently verifiable real-world evidence
- No staffing change, spending or pilot extension occurred. Sending or publishing a user's deck requires separate authority
