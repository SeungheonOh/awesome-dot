---
name: audit-font-character-coverage
description: "Check which Unicode code points in supplied text map to glyphs in a bounded local OpenType font, preserving mapping selection, unsupported-format limits and the distinction from shaping or visual quality."
---

# Audit Font Character Coverage

## When to use

Use this before selecting a font for a particular text sample, diagnosing missing-character reports or adding a coverage check to a typography workflow. Produce code-point evidence from the exact supplied font. Do not install fonts, upload private text, alter a design file or claim visual quality from a mapping check.

## Required inputs

- Authorized local font bytes and their filename/version context
- The exact text sample, without silent normalization or transliteration
- Supported font containers, mapping formats and input-size bounds
- The requested output and whether a separate rendered/shaping check is available

If the input is a collection, compressed webfont or unsupported mapping, report that specific limit. Do not count every character as missing because the parser could not interpret the file.

## Workflow

1. **Preserve the source and bound the read.** Check byte length before loading and keep the original unchanged. Limit tables, encoding records and text size independently. Treat user-supplied labels as text and never as HTML or executable code.
2. **Validate the binary envelope.** Identify the container before interpreting offsets. Check the directory, required tables, duplicate tags, table ranges and supported overlaps. For nested structures, validate offset plus length against the enclosing table, not only against the whole file. Reject impossible lengths before loops or allocation.
3. **Select one supported Unicode mapping consistently.** Record platform, encoding and format. Prefer a supported full-repertoire mapping over a BMP-only mapping. Do not combine unrelated subtables into optimistic coverage. The [OpenType cmap specification](https://learn.microsoft.com/en-us/typography/opentype/spec/cmap) describes selection and the missing-glyph convention; the [font-file specification](https://learn.microsoft.com/en-us/typography/opentype/spec/otff) defines the container.
4. **Enumerate Unicode code points, not UTF-16 units.** Preserve supplementary characters as one code point. Surface isolated surrogate units as invalid input rather than treating them as ordinary missing characters. Keep repeated occurrences separate from the unique-character summary when occurrence counts matter.
5. **Resolve each mapping with bounds intact.** A glyph index of zero is unmapped under this convention. Require nonzero indices to fit the recorded glyph inventory. Format 4 needs careful relative-address and delta handling, including its zero-glyph exception; format 12 needs ordered bounded groups. Unsupported variation mappings remain unexamined.
6. **Keep conclusions narrow.** Mapping evidence does not establish correct outlines, shaping, joining, ligatures or emoji-sequence presentation. Controls and spacing behavior also need interpretation beyond a simple nonzero-index count. Label any displayed character tiles as system-font previews if the uploaded font was not actually rendered.
7. **Cross-check with an independent parser.** On permitted, known fonts, compare the selected mapping with a mature implementation such as FontTools. Confirm the same subtable-selection policy before interpreting disagreements. Use hand-built fixtures for boundary cases that ordinary fonts may never exercise.
8. **Export reproducible evidence.** Include source identity, selected mapping, exact code-point values, glyph IDs, invalid/unmapped status and omitted checks. Invalidate the export after text or file changes. An obsolete asynchronous file read must not replace a newer selection.

## Worked example

A synthetic mapping contains A→1, B→2 and U+1F600→3. The text is AAB😀C.

There are five code-point occurrences but four unique code points. A, B and the supplementary character map to nonzero indices; C does not. A check that iterates UTF-16 code units would split the supplementary character and incorrectly report two missing entries.

Return the unique rows with their U+ values and glyph indices. State that the fixture has no tested outlines and that a nonzero entry for the emoji does not establish colored emoji rendering or sequence support. Do not silently remove C or substitute another font to turn the check into a pass.

For a format 4 indirect mapping, a raw glyph-array value of zero must remain missing even if the segment's delta is nonzero. A focused fixture can catch this error when an ordinary round trip cannot.

## Verification cases

- Direct-delta and indirect format 4 mappings, including zero entries and the terminal segment
- BMP and supplementary format 12 mappings, unmapped characters and isolated surrogates
- Truncated directory/table, out-of-range nested offsets, overlapping ranges and glyph IDs outside the inventory
- Unsupported container or mapping, reported as unexamined rather than empty coverage
- Changed text, canceled/obsolete file read, text-only labels and exported evidence matching the current input

The parser used to develop this workflow was cross-checked against FontTools for two known system fonts across the full code-point range and a format-4-only fixture across the BMP. Synthetic mapping and interaction checks also passed. These checks do not validate arbitrary font outlines or prove a browser's rendering behavior.

## Output and stopping point

Return the mapping coverage, exact unsupported features, source/selection evidence and checks actually performed. If the user needs typography approval, identify the remaining rendered/shaping checks rather than silently calling the font suitable for an entire language. Installation, publication and changes to the user's design remain separate authorized actions.
