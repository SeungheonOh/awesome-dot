# Executed checks and limits

The workflow and all example data are original fictional material. Local checks ran on 2026-10-02 and verify the packet and generated files; they do not establish physical counts, placement or a real handoff.

## Count and source fixture

From this folder:

```bash
python check_example.py
```

Observed result:

```text
PASS: source coverage, repeat imports, corrected split, quantities, reservations and unknowns
LIMIT: fictional fixture only; physical contents and verification remain unestablished
```

The Python standard-library check reads `example-data.json`. It confirms all imported source IDs have dispositions, unchanged repeated imports and repeated review records do not add stock, the mug report's replacement references the original, per-item plans preserve reservations, current quantities reconcile with outside quantities, the towel allocation remains partly packed, and unknown identity/contents/direct-verification fields stay unknown. Its input is a bounded fixture with at most one active box-distribution report per item, not a general event processor or importer.

A temporary-copy probe also checked that inconsistent fixtures fail rather than merely printing success. The following was run successfully; each mutation produced an `AssertionError`, and the temporary copies were automatically removed:

```bash
python - <<'PY'
import copy, json, shutil, subprocess, sys, tempfile
from pathlib import Path

base = json.loads(Path('example-data.json').read_text())
mutations = {
    'overallocated reserve': lambda d: d['items'][0].update(reserve=3),
    'missing source disposition': lambda d: d['sources'].pop('S07'),
    'broken correction target': lambda d: d['reported_observations'][-1].update(corrects='R02'),
    'invented verified count': lambda d: d['items'][0].update(verified=4),
}
for label, mutate in mutations.items():
    data = copy.deepcopy(base)
    mutate(data)
    with tempfile.TemporaryDirectory(dir='review') as folder:
        folder = Path(folder)
        shutil.copyfile('check_example.py', folder / 'check_example.py')
        (folder / 'example-data.json').write_text(json.dumps(data))
        result = subprocess.run([sys.executable, str(folder / 'check_example.py')],
                                capture_output=True, text=True)
        assert result.returncode != 0 and 'AssertionError' in result.stderr, label
    print('REJECTED:', label)
PY
```

The checks do not establish whether any real count, identity or physical location is true. They do not validate natural-language understanding, live service writes, physical capacity, handling suitability, a home-wide inventory, or future transfers/unpacking. The example's one pouch is not a count of its contents. No aggregate number combines pouches with pieces.

## Printable example

Installed tools used: Python 3.12.14, ReportLab 4.4.9, pypdf 6.10.0 and Poppler's `pdftoppm`/`pdfinfo`. No dependencies were installed. The PDF renderer embeds the installed DejaVu Sans regular and bold fonts rather than relying on viewer substitutions. Supply the directory that holds both font files through `--font-dir` if rerunning on another machine.

Generation and rendering commands:

```bash
python review/render_labels.py --font-dir "$(dirname "$(fc-match -f '%{file}' DejaVuSans)")"
pdftoppm -scale-to 1200 -png -singlefile labels.pdf review/labels-preview
pdfinfo labels.pdf
```

`labels.pdf` is a single static US Letter page, 612 × 792 points, with four large cut-out labels. A pypdf readback confirmed each ID appears once and pairs with its expected room: B01 Kitchen, B02 Kitchen, B03 Bathroom and B04 Study. The labels contain no item descriptions, personal names, addresses or access links. No fillable fields are present.

The final rendered page in `review/labels-preview.png` was opened and inspected. All four label borders, IDs and destination rooms are visible with clean spacing and ample margins. The draft header and footer fit without clipping. An initial standard-font rendering showed poor font substitution; embedded DejaVu fonts corrected it before the final review.

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `labels.pdf` | 43,775 | `1291fa51174decd5b1123f689ca2029672f59acd50c9b55d545f8113dd2bb61a` |
| `review/labels-preview.png` | 54,658 | `2f489d0d553ca62e383c34fab970ec1a68f6d6f99a569a233346562639ac9a03` |

Both example artifacts are below 2 MiB. The PDF was not physically printed, so printer scaling, cutting and real label use remain untested. Its labels reflect only the fictional room assignments; no label was applied to a box.

## Packet readback

Local Markdown links resolve, and the item/box/source IDs in the prose, count fixture and labels were compared. The generated files are an example output; use the workflow with the user's actual authorized records and distinguish their evidence states in each new packet.
