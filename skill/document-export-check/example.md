# HarborDesk release delivery exercise

Example request:

> Export this approved R3 Word brief to a PDF for our internal pilot handoff. Keep the editable file intact, preserve its two-page structure and links, and check the final file before calling it ready. Do not send it anywhere.

Everything in this example is original fictional content. “Approved” describes the fixture contract, not a real person's approval. The `example.com` targets are deliberately fictional and were inspected as strings, not visited.

## Acceptance map

| Source location | Required result | How to verify |
| --- | --- | --- |
| Release decision, page 1 | 25-seat internal pilot only; general availability on hold pending screen-reader review | Compare complete sentence and inspect its visible paragraph |
| Test table, page 1 | Windows 18/0, macOS 14/0, Ubuntu 12/0; total 44/0 with the correct build identifier on each row | Read source table cells, compare extracted content, inspect every rendered row |
| Exact strings, page 1 | `Zoë`, `café`, `Δ latency = −12 ms`, `99.5%`, `HD-1847`, `v2.4.1+rc.03` | Exact text comparison and glyph inspection |
| Reference, page 1 | `https://example.com/harbordesk/releases/2.4.1?rev=3#checks` | Inspect PDF URI annotation and visible label |
| Explicit break before Recipient delivery checks | Two Letter portrait pages; checklist begins on page 2 | Page count, page boxes and both rendered pages |
| Header/footer, both pages | Header and `HD-0241-R3`; `Page 1 of 2` then `Page 2 of 2` | Extract and visually inspect both pages |
| Issue template, page 2 | `https://example.com/harbordesk/issues/new?template=delivery` | Inspect PDF URI annotation and visible label |
| Known unresolved work, page 2 | Screen-reader review pending; no compliance/compatibility claim | Full paragraph comparison and visual inspection |

The source contains a five-row, four-column native table, four numbered steps, one explicit page break and PAGE/NUMPAGES footer fields. It has an unused empty bibliography XML part inherited from the authoring template. That part contains no bibliography entries or external data and was inspected before export. The source checker inventories it; this is not permission to ignore unfamiliar custom XML in a real document.

## Reproduce the export with existing tools

Run these commands from this folder in a POSIX shell. They need an existing Python 3 environment with `pypdf`, LibreOffice's `soffice`, and Poppler's `pdftoppm`, `pdfinfo` and `pdffonts`. Do not install anything merely to run this example. If a dependency is missing, report it and use an authorized environment where it already exists. Font availability also matters; the observed output used Liberation Sans and Carlito variants. The verification record identifies the mixed font inventory and its limits.

The included checker is specific to this fixture. It checks package feature indicators, fixed table values, known fields, the two URLs and all 45 nonempty body/table paragraphs in order against extracted PDF text. It also requires the complete table block, including row and cell associations, on page 1. It does not render pages, execute links, validate arbitrary DOCX packages or decide visual quality.

```bash
python3 check_example.py approved-source.docx
```

After inspecting that inventory, create a fresh output and profile. The shell block stops on failure and does not write over the source or included PDF:

```bash
(
set -eu
export_run_dir="$(mktemp -d "${TMPDIR:-/tmp}/document-export-check.XXXXXX")"
export_profile_uri="$(python3 -c 'from pathlib import Path; import sys; print((Path(sys.argv[1]) / "profile").resolve().as_uri())' "$export_run_dir")"
sha256sum approved-source.docx > "$export_run_dir/source-before.sha256"
soffice --version > "$export_run_dir/converter-version.txt"
soffice "-env:UserInstallation=$export_profile_uri" --headless --norestore \
  --convert-to pdf:writer_pdf_Export --outdir "$export_run_dir" approved-source.docx \
  > "$export_run_dir/conversion.log" 2>&1
test -s "$export_run_dir/approved-source.pdf"
sha256sum -c "$export_run_dir/source-before.sha256"
python3 check_example.py approved-source.docx "$export_run_dir/approved-source.pdf" \
  > "$export_run_dir/machine-checks.json"
pdfinfo "$export_run_dir/approved-source.pdf" > "$export_run_dir/pdfinfo.txt"
pdffonts "$export_run_dir/approved-source.pdf" > "$export_run_dir/pdffonts.txt"
pdftoppm -r 144 -png "$export_run_dir/approved-source.pdf" "$export_run_dir/page"
printf 'Inspect every page image and the logs in %s\n' "$export_run_dir"
)
```

The reviewed included file is named `release-delivery.pdf`; LibreOffice's new export above is named from the input stem. Open every newly rendered page and compare it against the acceptance map. If you cannot inspect the images, the visual check remains pending. Preserve the new files and logs for diagnosis; do not substitute an old preview for the new export.

On systems without `sha256sum`, use an available SHA-256 utility and compare before/after values. Different exporter versions can change output bytes and layout, so regenerated PDF hashes are not expected to match the included file. Verify the regenerated file itself. This demonstration was run on Linux; other operating systems and Word versions were not tested.

To check the included artifacts without exporting again:

```bash
python3 check_example.py approved-source.docx release-delivery.pdf
```

Read [the observed verification and limits](verification.md) before relying on the result.
