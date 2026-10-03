---
name: repair-document-accessibility
description: Repair the semantic accessibility of an existing document while preserving its meaning and useful native features. Use when the requested result is a repaired artifact with coherent navigation, reading order and information equivalents, rather than ordinary proofreading, visual formatting, OCR or an export-fidelity check.
---

# Repair Document Accessibility

Return the actual repaired document in the requested format, with evidence for the changes that matter to its readers. An issue list is the result only when review alone was requested. Clear appearance, searchable text, a populated description field and a clean automated report each establish different things; none alone establishes that someone can use the document with assistive technology.

Keep ordinary editing or document creation primary when accessibility is only one routine quality consideration. Use this workflow when finding and repairing barriers in an existing artifact is the main task. Website interaction, timed-media captions and narrow contrast or font-coverage questions have their own workflows.

## Establish the document and reader task

Inspect the selected original, the requested degree of change and the intended use. Identify its native format, any requested export, protected content and features that must survive: approved wording, tables, figures, links, notes, controls, review markup or editability. Preserve the original or use the authorized version-aware editing route. Do not turn an editable document into page images or plain text merely to simplify the repair.

Establish the relevant reader tasks, such as finding a section, following a procedure, comparing a table or understanding a figure's conclusion. These guide inspection; do not invent a disability profile or claim to represent every reader. Use a named standard, application or assistive-technology target when the request supplies one. Otherwise make useful repairs and scope the evidence without inventing a certification requirement.

Inspect both appearance and native structure. Extracted body text can omit a floating box, a table relationship, an image, a field or a note that changes the task. Inspect complete relevant pages and the objects behind them. Treat a checker warning as a lead to examine, and its silence as coverage limited by that checker. Do not run document macros, refresh external data or follow stored links merely to inspect the file.

Prioritize barriers that prevent the requested task or misrepresent meaning. Record the affected object and the intended repair briefly enough to keep the actual document central. A short repair does not require a compliance matrix or a separate report for every object.

## Repair meaning and structure together

Determine what an element means before assigning semantics. Bold text may be a heading, a warning or ordinary emphasis. A table may represent data relationships or merely position two independent sections. A decorative visual and an informative chart need different treatments. Do not apply one mechanical fix to every similar-looking object.

Use the requested format's supported authoring features and verify their actual saved representation. Where the available tool cannot express a needed feature, preserve useful work and identify that precise gap. A field name in an editing API does not prove how a reader consumes it. Consult applicable format or application documentation for consequential behavior rather than assuming that all document formats share the same semantics.

### Navigation and sequence

Give real sections a logical heading hierarchy and useful labels. Keep the document title distinct from section headings. Preserve or repair contents links and cross-references when they depend on the changed hierarchy. Do not add a heading to every emphasized sentence or force a contents page into a short document.

Follow the intended reading sequence through columns, positioned objects, side notes and tables. Visual position and underlying object order may differ. Rebuild a layout construction when necessary to express its actual sequence, preserving prerequisites, warnings and qualifications beside the step they constrain. Verify that moved text is neither omitted nor read twice in the saved structure.

Use native lists for genuine sequences or parallel items where supported. Preserve grouping, order, continuation and intentional restarts. A visible digit or bullet character does not by itself encode a list, and a newly numbered list must not imply an order the source never established.

### Tables and comparisons

Preserve the identity and relationship of each value, label, unit and note. Identify which rows or columns actually supply headers and express those relationships through the target format. A repeating row, a bold first row and a complete header association are not interchangeable properties. Inspect what the specific format supports instead of declaring a table accessible because one flag is present.

Simplify merged, nested or layout structures when the request allows it and the meaning can be preserved. Do not flatten a useful data table into an image or remove its relationships to silence a warning. For a complex table whose associations remain unclear, establish the intended relationship before restructuring it. Keep legitimate blank, unknown and not-applicable values distinct; never invent data to fill empty cells.

Make comparisons available without a color-only or position-only code. Derive text labels or other appropriate equivalents from the source legend and facts. Preserve what the status actually describes; a readiness color must not become a claim of completion. Keep readable contrast and magnification/reflow needs in view, while distinguishing measured color properties from observed application behavior.

### Figures, links and language

Inspect the actual visual in its context. Decide whether it conveys information, performs a function or is decorative. Supply a useful supported alternative or mark genuine decoration appropriately for the format. Do not replace an informative visual with a filename, generic label or invented interpretation simply to make an alternative-text check pass.

For a chart or complex diagram, provide the information needed for the reader's task in an appropriate nearby explanation, data table or longer description, with a concise alternative pointing to it when useful. Preserve quantities, relationships, uncertainty and limits. Avoid forcing all detail into one description field or duplicating surrounding paragraphs unnecessarily. A text alternative is not independently verified evidence of the visual's underlying claim.

Give links meaningful text while preserving the intended destination and relevant context. Distinguish links with different purposes that previously shared an unhelpful label. Do not visit protected or unnecessary destinations, and do not replace the destination with a guessed correction. Repair meaningful captions, note references and their return/navigation relationships when in scope.

Set document and passage language where the source and format support it. Preserve quoted wording and technical notation. Do not silently translate text, expand an ambiguous abbreviation or change a proper name to satisfy a mechanical rule. If forms or controls are in scope, inspect their labels, instructions, requiredness and navigation through the actual available consumer; a content control's existence does not prove a usable completion path.

## Verify the exact saved repair

Reopen the final file and compare it with the source. Check supported meaning, protected content and useful native features as well as the intended repairs. Inspect a restructured procedure in sequence and a changed table by its actual cell relationships. A count of headings or nonempty alternatives can support this review but cannot replace it.

Keep distinct evidence levels visible:

- **Saved structure:** inspect the actual heading/list relationships, reading sequence, table semantics, labels, alternatives, language and references relevant to the repair. Check native editability where it matters
- **Visible rendering:** view every affected page or relevant reflowing state. Look for clipping, overlap, lost glyphs, broken tables and misleading associations introduced by the repair. After a change that affects layout, inspect the updated rendering
- **Application checks:** use an available supported native checker when appropriate. Record what it checked, unresolved warnings and the saved revision. Do not relabel a custom XML inspection as the editor's accessibility checker
- **Reader interaction:** when a suitable authorized application and assistive-technology route are available, exercise the relevant task, such as heading navigation or reading a table with its labels. State the actual app/tool combination and observed result. A screenshot, exported text or source assertion is not that interaction

Use checks proportional to the requested repair. If an important check is unavailable, state the unverified behavior and deliver the useful supported result rather than inventing a pass or installing an unrequested tool. Repeating an unchanged checker does not expand its coverage. Do not upload a private document to an external checker without the relevant authority.

Treat any requested export as a separate representation. Confirm that necessary semantics and relationships survive in that saved file; a native-document repair does not automatically validate its PDF, HTML or other export. Tag presence, successful text extraction and a matching render are useful observations with different limits.

## Deliver the repaired artifact and useful limits

Return the actual requested document and a concise account of material repairs, preserved content and checks that ran. Identify remaining barriers by their object or section and the smallest missing decision or capability. Keep routine inspection artifacts out of the handoff unless requested or needed to explain an unresolved issue.

Describe the achieved result precisely: corrected native structure, readable pages, specific checker findings resolved or a particular reader task observed. Claim conformance only when the requested applicable criteria and required evidence have actually been assessed; do not infer it from a handful of common repairs. Preparing a repaired copy does not authorize publishing it, changing its audience or replacing unrelated versions.

## Reference

[Microsoft's Word accessibility guidance](https://support.microsoft.com/en-us/accessibility/word/make-your-word-documents-accessible-to-people-with-disabilities) describes native headings, table headers, meaningful links, visual alternatives and its checker. Those application-specific features should be verified in the actual target rather than assumed for other formats.
