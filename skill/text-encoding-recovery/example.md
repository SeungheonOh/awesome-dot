# A checked copy of a small catalog export

**Result:** [catalog-utf8.csv](example-output/catalog-utf8.csv) is a 152-byte UTF-8 CSV without a leading signature. It was reopened with Python's `csv.reader`; its header and every field in three records match the [authored expected rows](fixtures/expected-rows.json). The [saved result record](example-output/result.json) records the byte identities and individual checks.

## The evidence and contract

This is an original synthetic example, not a captured customer file. Its source profile, `tiny-catalog-export-v1`, explicitly writes Windows-1252 with comma delimiters, doubled ASCII quotes and CRLF record separators. The [construction record and contract](fixtures/contract.json) tie that profile to this exact [source file](fixtures/catalog-windows1252.csv):

- 142 bytes
- SHA-256 `86c2754f2bf7da20dc5a1d1ff28a5f6027a2f9f95dc328f663ca6c5610a4b7e5`
- A separately authored expected note for record `0007`: `“small, blue” costs €5`, including U+201C, U+201D and U+20AC

The digest identifies the bytes under test. It does not authenticate an export. Here the profile and expected text are deliberately supplied fixture evidence; they are not facts inferred from readable output, an encoding detector, or a successful decoder.

The approved operation is strict `cp1252` decoding followed by strict `utf-8` encoding, into a separate new directory. There is no signature to remove. Every character, including CR and LF, must remain at the same character position. The helper writes encoded bytes directly rather than parsing and reserializing the CSV. Its final consumer is `csv.reader` with explicit UTF-8 strict decoding, `newline=''`, comma delimiter, ASCII double-quote quoting with doubled quotes, no escape character, `QUOTE_MINIMAL`, `skipinitialspace=False`, and `strict=True`.

## What survived the saved-file check

| Record ID, kept as a string | Label | Note, with embedded line endings shown as escapes | Quantity, kept as a string |
| --- | --- | --- | --- |
| `0007` | café | `“small, blue” costs €5` | `"0"` |
| `0012` | piñata | `first line\r\nsecond line` | `""` (empty) |
| `0030` | façade | `He said "sí".` | `"2"` |

The source and saved copy each contain five CRLF sequences: four record separators including the header, plus the embedded CRLF in record `0012`. The checker compares the entire decoded text, every CR/LF position, every parsed field, and exact re-encoding back to the source bytes. It also rereads all four source fixtures before reporting success.

The UTF-8 copy's SHA-256 is `e5320aff2bdf1a77e574130d0a5679748ce52c800296dc1428797bfc547b73c5`. The recorded run used CPython 3.12.14 on 2026-10-02. These are parser and byte checks; they do not establish Excel import behavior, a live service's ingestion, glyph appearance, or real-world meaning.

## Why the other cases stay separate

| Case | Observed result | Decision |
| --- | --- | --- |
| Decode the Windows-1252 source as UTF-8 | Strict decoding fails at byte interval `[39, 40)`. `replace` and `ignore` finish but change source information and expected fields | Reject both lossy results; neither is saved |
| Decode that source as Latin-1 | All bytes decode and roundtrip, but the known note has U+0093/U+0094/U+0080 instead of the declared quotes/euro | Reject; roundtrip alone does not establish the intended text |
| [ambiguous.csv](fixtures/ambiguous.csv) | Label bytes `C3 A9` strictly decode and roundtrip as U+00E9 in UTF-8 or U+00C3 U+00A9 in Windows-1252 | Hold; request an export setting tied to these bytes or the authoritative label for record `0040` |
| [known-lossy-utf8.csv](fixtures/known-lossy-utf8.csv) | Current text strictly accepts UTF-8, but the authored fixture history records earlier replacement in `0041/name` and `0041/title` | Hold; request an earlier original or authoritative corrections for those fields |
| [literal-unicode-utf8.csv](fixtures/literal-unicode-utf8.csv) | U+FFFD, `?` and the interior U+FEFF in `pre\ufeffpost` were authored intentionally | Preserve all bytes in [literal-unicode-preserved.csv](example-output/literal-unicode-preserved.csv), and verify its parsed fields |

The known-lossy fixture deliberately omits the record-specific pre-loss strings. The checker demonstrates that `Renée` and `Renèe` can both produce its current name through the recorded wrong decoder, and `Café` and `Cafè` can both produce its current title through ASCII replacement. These are competing witnesses to lost information, not proposed corrections. A literal U+FFFD or question mark in another file is not automatically damage.

The separate Unicode fixture is needed because Windows-1252 cannot represent U+FFFD or U+FEFF. Its contract treats the interior U+FEFF as content, so the example does not globally strip signature-shaped bytes or substitute similar-looking text. No normalization or other text editing is authorized.

## Reproduce locally

Use Python 3 and its standard library only. From this folder, inspect and run [rehearse.py](rehearse.py):

```sh
python3 rehearse.py check example-output
python3 rehearse.py rehearse my-new-output
python3 rehearse.py check my-new-output
```

`my-new-output` must not exist; its parent must exist. Repeating the rehearsal at an existing file, directory or symlink stops without replacing it. The helper never rewrites the fixtures. If a write is interrupted, it keeps any partial new output for inspection and will not overwrite it on retry. `check` writes nothing.

This helper is deliberately bound to the four adjacent fixtures and their declared byte identities. It has no arbitrary-input repair mode, detector, installation step, network access or formula evaluation. For a different export, establish its evidence and consumer contract anew rather than changing hashes until this rehearsal passes.

## Independent readback

An independent inspected run reproduced both CSV outputs and the result record byte-for-byte. Six additional checks rejected normalized line endings, an added leading signature, removal of the interior U+FEFF, replacement of the intentional U+FFFD, an unsupported ASCII output policy and an occupied destination. The policy change stopped before output creation; checks of damaged copies left their bytes intact. These checks support this captured fixture and parser contract, without identifying the encoding of an unrelated export.

## Technical basis

Python's [CSV documentation](https://docs.python.org/3.12/library/csv.html) documents string fields, explicit dialect options and `newline=''` for file objects. Its [codec error handlers](https://docs.python.org/3.12/library/codecs.html#error-handlers) explain strict failure and how replacement or ignoring discards information. Its [UTF-8 signature codec](https://docs.python.org/3.12/library/codecs.html#module-encodings.utf_8_sig) documents the leading bytes added or skipped by `utf-8-sig`; this consumer instead uses `utf-8` and forbids a leading signature. Unicode's [signature FAQ](https://www.unicode.org/faq/utf_bom.html#BOM) distinguishes an initial signature from interior U+FEFF content and explains why the receiving format governs signature handling. Consulted 2026-10-02.
