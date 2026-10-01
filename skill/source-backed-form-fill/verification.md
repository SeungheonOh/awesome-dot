# Example verification

Checked on 2026-10-01. The whole scenario is fictional. The output is a non-binding enquiry draft with a real unanswered required question; it is not ready to submit. No real recipient, contact information, portal, signature, contract or payment is involved.

## Artifact identity

Open the [original blank native PDF form](room-enquiry-blank.pdf), the [separately saved filled native draft](room-enquiry-draft.pdf), and the [one-page PNG preview](preview.png) of the filled draft. Both PDFs are one Letter-size page. Each file is below 2 MiB.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| room-enquiry-blank.pdf | 18,517 | `d25a7cd2a2d1d29a45d0545d0ae808f4b28d2a3a8e86f03cecc929b870fb0aba` |
| room-enquiry-draft.pdf | 18,442 | `4205ab38e6a31b20eca0bb8287a3e8928f0032bccee3f4b571e84e50ce57ff88` |
| preview.png | 98,832 | `ec879148e1691899b8826a4d5f663e688f0a79b13d6691a7f2a9a0136266477e` |

The preview is 935 by 1210 pixels, rendered from the exact filled PDF above at 110 dpi. The PNG is a visual aid, not the editable form. It contains only resolution metadata. Rebuilding with different library or renderer versions may change file hashes and rendering; recheck any regenerated output.

## Portable reproduction

The [source brief](source-brief.md) supplies every answer and explicitly records missing information. The [field map](field-map.json) includes native identifiers, types, values, original values, source locators, branch rules and review states. All fields are on page 1. Its `required` flag means unconditionally required; `required_when_active` identifies a child requirement controlled by another answer. No form script implements those conditional rules: the filling and review workflow evaluates them.

[example.py](example.py) uses Python 3 with the public `reportlab` and `pypdf` packages already available. This example was run with ReportLab 4.4.9 and pypdf 6.10.0. It creates the original blank fixture, reads its field tree and page widgets, fills only supported answers in a clone, reopens the exact files and prints validation results and fingerprints. It will not overwrite an existing example PDF, install dependencies, access a network or submit anything. It is a narrow worked-example builder and checker, not a general form-filling engine.

From this skill folder, choose a new output directory:

```sh
python3 example.py --check .
python3 example.py --output-dir ./example-output
python3 example.py --check ./example-output
```

Use a locally available PDF renderer whose output passes visual inspection. The commands below are an example, not a guarantee about the renderer selected on a particular machine. Check its version, render and inspect both pages, then keep the filled preview:

```sh
pdftoppm -r 110 -singlefile -png ./example-output/room-enquiry-blank.pdf ./example-output/blank-review
pdftoppm -r 110 -singlefile -png ./example-output/room-enquiry-draft.pdf ./example-output/preview
```

The script's PASS result covers its explicit structural and answer checks. It does not perform rendering, visual inspection, viewer interaction or accessibility certification. If a dependency is unavailable, stop that step and use the complete mapping honestly; do not claim to have generated a native artifact. No installation is required or authorized by these instructions.

## Answers and deliberate blanks

| Fields | Saved result | Evidence and disposition |
| --- | --- | --- |
| Group, activity | Lantern Board Game Circle; Monthly board game evening | F1, two native text answers |
| Preferred date, session times | 2026-11-14; 18:30 to 20:30 | F2, exact requested room-local values; no availability or setup-time inference |
| Attendance, room, seating | 12; Small room; Tables and chairs | F3, one text answer and two native dropdown choices |
| Projector needed | No | F4, canonical `/No` value and only the No radio appearance selected |
| Projector setup details | Blank | F4, required only when projector answer is Yes; branch inactive |
| Early setup access | Blank | F5, required Yes/No trigger is unknown |
| Early-access minutes | Blank | F5, depends on the unresolved trigger; not assumed zero |
| Extra notes | Blank | F5, optional and not supplied |
| Staff-only reference | Not reviewed | F5, original value and read-only control preserved |

There are nine supplied answers, one preserved staff-only value and four intentional blanks. The smallest pending question is: Do you need early setup access? If yes, how many minutes before the 18:30 session start? No response or submission approval is inferred.

## Observed checks

- Original bytes stayed unchanged through filling. The filled PDF is a distinct saved file, not an overwrite or a flattened image
- Both files contain 14 canonical fields and 15 page widgets. The radio group has two child widgets under one canonical field. Every page widget is the same object reachable through the canonical field tree; child widgets refer back to their owning parent
- Every saved canonical value and effective widget value matches the field map, including unresolved blanks. Each radio widget's selected appearance was checked independently from the parent value
- Radio values live on the canonical group; child widgets inherit that value and retain their own On/Off appearance states. The builder removes redundant child value entries that would shadow the canonical answer
- Text and dropdown appearances are nonempty; button appearance streams exist for the selected state. This check complements the actual render
- Page size, static page content, labels, instructions, control geometry, field names/types, options, text-length limits, required flags, tooltips, default/reset values, annotation visibility flags and the staff-only read-only flag match the original. The three dropdowns remain choice controls; they are not substituted text fields
- Dates and times parse in the stated formats. The same-day end follows the start. Attendance is a positive integer. Supported answers appear at the recorded source locators. This literal source check supplements the reviewed brief; it does not establish real-world truth
- The fixture has no document/page/widget actions, named scripts, named external links, attachments, signatures or dynamic-form payload in the checked locations. This is a check of the known fixture, not a general malicious-PDF security assessment
- The final blank and filled pages were rendered with Poppler 25.03.0 and visually inspected at 935 by 1210. Labels and answers are legible, the No radio is visibly selected, required unknowns remain blank, and no clipping, overlap or missing glyphs was observed
- Negative mutation checks rejected changed group/attendance answers; removed read-only or required flags; changed choice options; a radio group with no selected appearance; a stale child-radio value; a detached same-name canonical/widget pair; a stale choice index; a hidden widget; a changed staff reset default; and missing page widgets or canonical fields. These checks exercise native structure and saved values, not just expected prose. The detached-object, visibility and reset-default cases initially exposed gaps; the checker was strengthened and all cases then rejected as intended

An initial render showed a font-substitution defect. A different already-installed renderer produced the inspected final preview. A successful structure check was not used to waive that visual failure. Only the fingerprints above identify the final checked artifacts.

## Limits and readiness

Native field data, appearances, controls and a full-page render were checked. An end-user PDF application was not used to edit, save and reopen the form, so application-specific editing and font substitution remain untested. The native structure is editable, but this is not a promise about every viewer. Screen-reader order and complete PDF accessibility were not tested or certified.

The unresolved setup-access answer intentionally blocks a submission-ready claim. This example demonstrates successful private preparation despite a missing answer. No external disclosure, reservation, approval, signature or submission occurred. Real submission would require the final answers and the applicable, separately established authorization.
