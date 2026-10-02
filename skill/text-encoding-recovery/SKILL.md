---
name: text-encoding-recovery
description: "Recover an authorized text export into a separately saved, checked encoding when byte and source evidence support the interpretation; preserve originals and hold ambiguous or already-lost characters."
---

# Recover a Garbled Text Export

Use when a text file displays garbled characters, fails a decoder, or opens differently in two applications. Produce a usable copy in the requested encoding with a short record of the supported interpretation and saved-file checks. This is a byte-to-text problem before ordinary editing or dataset cleanup; translating words, correcting spellings and changing numeric values are different tasks.

## Establish the file and the intended consumer

Read the supplied file as bytes first. Resolve the exact source/version, where it came from, export settings or format declaration, a small independently known text sample if available, the receiving application or parser, and the requested output location. A request to recover a local copy authorizes that scoped transformation. It does not authorize overwriting the source, uploading it to an online converter, or changing a shared application's import defaults.

Record what the user actually observed: a decoder error with a byte offset, replacement diamonds, literal sequences such as `\u00e9`, unexpected `Ã` characters, missing glyph boxes, or only a display difference. These symptoms are leads. A font problem, escaped JSON string, delimiter error and incorrect encoding need different remedies. If only a screenshot or pasted text is available, ask for the original export bytes when they are needed; copying through chat may already have transformed the evidence.

## 1. Preserve the original bytes

- Record size, a content digest and the supported source identity; keep an unchanged original
- Work within a separate approved output path and refuse a collision unless replacement was explicitly requested
- Keep byte offsets and record locations in private diagnostics; quote only the minimum relevant text
- Do not execute scripts/macros, follow embedded URLs, or evaluate formula-like cells while inspecting data
- Check source identity again before delivering the candidate; concurrent changes invalidate a comparison tied to the earlier bytes

Read in binary mode when establishing the baseline. A text-mode read can alter line endings, strip a signature or substitute invalid characters before they are inspected. A digest proves a byte relationship to the captured file, not authenticity or completeness of the export.

## 2. Gather evidence before selecting an encoding

Separate evidence that governs the interpretation from clues that merely suggest it:

| Evidence | Use and limit |
| --- | --- |
| Format or transport contract at the captured version | Apply its actual encoding and signature rules; a filename extension alone is insufficient |
| Recorded export setting or source application's documented encoding | Supports a decoder when tied to this file; reconcile contradictory bytes or labels |
| Initial byte-order signature | Inspect the complete signature and the format's rules; UTF-32 prefixes can overlap a UTF-16 prefix |
| Independently known characters in selected source records | Compare their exact role and code points; a matching sample does not establish every record |
| Strict decoder accepts all bytes | Establishes syntactic acceptability under that decoder, not that its interpretation is intended |
| Statistical detector or readable-looking output | A candidate suggestion only; it cannot resolve two plausible meanings by itself |

Record conflicting evidence rather than allowing a preferred guess to win. Several encodings can accept the same bytes and produce different text. ASCII-only content may have the same interpretation under several compatible encodings; distinguish a safe unchanged character sequence from a claim that the original encoding was identified.

Choose only a small evidence-based set of candidate decoders. Use strict error handling. For each, record acceptance or the exact error interval, a bounded escaped/code-point view, and whether decoding then re-encoding under the **same** rules reproduces the source bytes. Account explicitly for a format-authorized leading signature in that comparison. Do not use `ignore` or `replace` to manufacture a successful recovery. A byte-preserving diagnostic such as Python's `surrogateescape` can keep unknown bytes available; its surrogate values are not recovered characters for a deliverable.

If candidates produce different plausible text and source evidence does not resolve them, return the comparison and one decision-changing question. Finish unrelated files with supported interpretations. Do not label the first decoder that succeeds as detected or confirmed.

## 3. Distinguish decoding from reversing prior damage

For a file that contains correct characters but uses a different encoding from the receiver, a justified decode and encode is sufficient. Preserve the decoded character sequence exactly unless the task explicitly authorizes another change.

For suspected prior mis-decoding followed by re-encoding, reconstruct the proposed chain as a hypothesis. For example, UTF-8 bytes may have been decoded as a legacy encoding and then saved as UTF-8. Reverse only a chain supported by source history and independent expected text, with strict conversions and an exact reversible relationship where available. Text that happens to contain `Ã` is not permission to apply a global repair rule.

If an earlier step replaced an unknown character with `?`, U+FFFD, dropped bytes, transliterated text or normalized distinct sequences, the current bytes may not contain enough information to recover the original. Such characters can also be intentional. Identify the affected locations and request an earlier original or authoritative correction. Never infer the missing name, identifier, amount or instruction from what would look natural.

Do not assume a whole file has one encoding if the evidence indicates concatenated or mixed sources. Isolate a segment only when real boundaries and provenance support it; otherwise hold the transformation. A line-by-line decoder fallback can silently join incompatible meanings.

## 4. Specify the output contract and create a separate candidate

Establish the receiver's required encoding, signature policy and text format. UTF-8 is not synonymous with UTF-8 plus a leading signature, and a signature can become an unwanted first-field character in a consumer that does not remove it.

List each authorized transformation before writing:

```text
source identity and byte digest
chosen decoder + evidence + strict-error behavior
signature handling, if the format permits it
target encoder + required signature policy
line-ending handling (preserve unless a change is required)
format-specific readback and exact character/field expectations
unresolved regions and resulting delivery status
```

Keep Unicode normalization, case conversion, trimming, quote replacement, escape interpretation and newline conversion out of an encoding-only operation. Visually equivalent strings can have different code points, and identifiers may depend on that distinction. If the target format requires one of these transformations, record and verify it separately.

Write the complete candidate to a new path using explicit encoding and strict errors. Preserve the original even after checks pass. If output is interrupted or uncertain, inspect the new file before retrying; do not replace a partial result by silently changing the source interpretation. Hold affected output when a required character cannot be represented by the target encoding, rather than substituting a question mark.

## 5. Reopen the saved result in the declared consumer

Verify from saved bytes rather than only the in-memory string:

1. Decode using the target's actual rules and compare the entire character sequence with the supported source interpretation, accounting only for the approved signature treatment
2. Check source preservation, target size/digest, and exact source re-encoding where applicable
3. Confirm line endings, signature presence/absence and sensitive code-point distinctions specified by the contract
4. Use the relevant available parser or application on a local copy, with the intended encoding and format settings
5. Compare record identities and fields, including leading zeros, empty values, quoted delimiters and embedded newlines when those occur; a matching row count alone is insufficient
6. Inspect representative display output if a viewer is available, and name the actual viewer/version and limits

Parsing CSV with Python establishes behavior for that parser and settings. It does not establish Excel's automatic import behavior, a web service's upload behavior, glyph appearance or meaning correctness. A successful display is similarly not proof that a machine import retained every code point. Preserve those separate results.

## Deliver the useful result

Provide the recovered copy, source identity and interpretation evidence, exact transformations, saved-file/consumer results and unresolved locations. Label an ambiguous candidate as a candidate. A held file can still have a complete diagnostic report and a precise next request.

For each file distinguish: original bytes preserved; supported text interpretation; candidate saved; exact text readback; parser/application readback; and remaining gaps. Do not claim that all source information was recovered when earlier lossy conversion remains possible.

## Example and technical references

Use the [original export example](example.md) for a declared Windows-1252 file converted into a UTF-8 CSV copy, plus separate ambiguous and already-lossy cases. Its output keeps identifiers, quoted text and original line endings intact.

Python's [Unicode HOWTO](https://docs.python.org/3.12/howto/unicode.html) and [codec documentation](https://docs.python.org/3.12/library/codecs.html) describe strict decoding, error handlers and byte/text conversion. Unicode's [encoding and signature FAQ](https://www.unicode.org/faq/utf_bom.html) explains signature forms and why receiver requirements matter. Python's [CSV reader documentation](https://docs.python.org/3.12/library/csv.html#csv.reader) specifies the newline handling and string-field behavior used by the example consumer. These references support the mechanics; they do not identify an unknown file's intended text.
