#!/usr/bin/env python3
"""Read-only checks for the two bundled, hash-pinned fictional example PDFs.

Requires pypdf, PyMuPDF, Pillow, pdftoppm and pdftotext. This is deliberately
not a general-purpose PDF validator or a tool for processing arbitrary files.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from PIL import Image
from pypdf import PdfReader
import pymupdf


EXPECTED = {
    "source-mixed.pdf": "6d86638077a4b2ca7d9068f4fa7fb15a35da298b98f8f8d65602a834946f4020",
    "searchable-reviewed.pdf": "7ed5b0bc648784b5d5b39ae4cbbe3906826197422258eedd2a35ac887083ddaa",
}
DPI = 100
QUERIES = [
    ("O012-001", 1),
    ("Keep labels O012 and 0012 distinct.", 1),
    ("capture_001.csv", 1),
    ("Do not reset before saving the export.", 1),
    ("Firmware floor: 2.08", 1),
    ("native-page-B", 2),
]
BOXES = ("mediabox", "cropbox", "bleedbox", "trimbox", "artbox")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def lines(text: str) -> list[str]:
    # Preserve punctuation and internal whitespace; omit blank layout lines only.
    return [line.strip() for line in text.splitlines() if line.strip()]


def run(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(command, check=True, capture_output=True, timeout=60)


def version(binary: str) -> str:
    result = run([binary, "-v"])
    return (result.stderr or result.stdout).decode("utf-8", "replace").splitlines()[0]


def page_geometry(page) -> dict:
    return {
        "effective_boxes": {key: [float(n) for n in getattr(page, key)] for key in BOXES},
        "rotation": int(page.rotation),
        "user_unit": float(page.get("/UserUnit", 1)),
    }


def image_samples(page) -> list[dict]:
    result = []
    for item in page.images:
        pixels = item.image
        result.append({
            "size_px": list(pixels.size),
            "mode": pixels.mode,
            "decoded_samples_sha256": digest(pixels.tobytes()),
        })
    return result


def image_placement(page) -> list[dict]:
    return [
        {key: list(info[key]) if key in ("bbox", "transform") else info[key]
         for key in ("bbox", "transform", "width", "height", "bpc", "cs-name", "has-mask")}
        for info in page.get_image_info(xrefs=True)
    ]


def search(document, text: str) -> list[dict]:
    hits = []
    for number, page in enumerate(document, 1):
        for rectangle in page.search_for(text):
            require(page.rect.contains(rectangle), "Search rectangle escaped its page")
            hits.append({"page": number, "rect": [round(n, 4) for n in rectangle]})
    return hits


def pixel_data(path: Path) -> tuple[tuple[int, int], bytes]:
    with Image.open(path) as image:
        rgb = image.convert("RGB")
        return rgb.size, rgb.tobytes()


def check(example_dir: Path, temp_parent: Path | None) -> dict:
    for binary in ("pdftoppm", "pdftotext"):
        require(shutil.which(binary) is not None, f"Missing dependency: {binary}")
    paths = {name: example_dir / name for name in EXPECTED}
    files = {}
    for name, path in paths.items():
        actual = digest(path.read_bytes())
        require(actual == EXPECTED[name], f"Bundled example hash mismatch: {name}")
        files[name] = {"sha256": actual, "bytes": path.stat().st_size}

    record = json.loads((example_dir / "source-review-record.json").read_text(encoding="utf-8"))
    authored = record["authored_source"]["page_1_lines"]
    native = record["authored_source"]["page_2_lines"]
    review_lines = record["line_review"]
    require(authored == [line["reviewed_text"] for line in review_lines], "Review record and authored lines disagree")
    changed = [line for line in review_lines if line["raw_text"] != line["reviewed_text"]]
    require(len(changed) == 3, "Expected exactly three corrected lines")

    source_path, reviewed_path = paths.values()
    source, reviewed = PdfReader(source_path), PdfReader(reviewed_path)
    src_doc, out_doc = pymupdf.open(source_path), pymupdf.open(reviewed_path)
    try:
        for label, pdf in (("source", source), ("reviewed", reviewed)):
            require(not pdf.is_encrypted, f"Unexpected encrypted {label}")
            require(len(pdf.pages) == 3, f"Unexpected {label} page count")
            for key in ("/AcroForm", "/Perms", "/StructTreeRoot", "/OpenAction", "/AA", "/Names"):
                require(key not in pdf.root_object, f"Unexpected {label} document feature: {key}")
            require(all(not page.get("/Annots") for page in pdf.pages), f"Unexpected {label} annotations")

        page_checks = []
        for index, (left, right) in enumerate(zip(source.pages, reviewed.pages)):
            geom = page_geometry(left)
            require(geom == page_geometry(right), f"Page {index + 1}: geometry changed")
            require(geom["effective_boxes"]["mediabox"] == [0, 0, 612, 792], "Unexpected page dimensions")
            require(geom["rotation"] == 0 and geom["user_unit"] == 1, "Unsupported example geometry")
            samples = image_samples(left)
            require(samples == image_samples(right), f"Page {index + 1}: image samples changed")
            placement = image_placement(src_doc[index])
            require(placement == image_placement(out_doc[index]), f"Page {index + 1}: image placement changed")
            page_checks.append({
                "page": index + 1,
                **geom,
                "geometry_equal": True,
                "decoded_images_equal": True,
                "decoded_images": samples,
                "image_placement_equal": True,
            })
        require(len(source.pages[0].images) == 1, "Expected one source scan image")
        require(not source.pages[1].images and not source.pages[2].images, "Unexpected image on native or blank page")

        for label, pdf in (("pypdf", reviewed), ("PyMuPDF", out_doc)):
            extracted = [page.extract_text() or "" for page in pdf.pages] if label == "pypdf" else [page.get_text() for page in pdf]
            require(lines(extracted[0]) == authored, f"{label}: reviewed page text differs from authored lines")
            require(lines(extracted[1]) == native, f"{label}: native page text changed")
            require(not extracted[2].strip(), f"{label}: blank page has text")
        require(not source.pages[0].extract_text().strip(), "Source scan unexpectedly has stored text")
        require(not src_doc[0].get_text().strip(), "Source scan unexpectedly has searchable text")
        require(source.pages[1].extract_text() == reviewed.pages[1].extract_text(), "Native page extraction changed")
        for index in (1, 2):
            require(source.pages[index].get_contents().get_data() == reviewed.pages[index].get_contents().get_data(), "Native or blank content stream changed")

        search_checks = []
        for text, expected_page in QUERIES:
            before, after = search(src_doc, text), search(out_doc, text)
            require(len(after) == 1 and after[0]["page"] == expected_page, f"Unexpected reviewed search result for {text}")
            require((not before) if expected_page == 1 else before == after, f"Unexpected source search result for {text}")
            search_checks.append({"query": text, "source": before, "reviewed": after})

        width, height = record["scan_image"]["size_px"]
        for line in changed:
            require(not out_doc[0].search_for(line["raw_text"]), "Superseded OCR line is still searchable")
            hits = out_doc[0].search_for(line["reviewed_text"])
            require(len(hits) == 1, "Corrected full line search is missing or duplicated")
            x0, y0, x1, y1 = line["bbox_px"]
            source_region = pymupdf.Rect(x0 * 612 / width, y0 * 792 / height, x1 * 612 / width, y1 * 792 / height)
            # Allows font ascent/descent around the hOCR ink box. This is a
            # coarse full-line placement check, not word-level UI selection QA.
            expanded = source_region + (-2, -8, 2, 8)
            require(expanded.contains(hits[0]), "Corrected line is displaced from its source region")

        with tempfile.TemporaryDirectory(prefix="searchable-pdf-check-", dir=temp_parent) as temporary:
            folder = Path(temporary)
            for prefix, path in (("source", source_path), ("reviewed", reviewed_path)):
                run(["pdftoppm", "-r", str(DPI), "-png", str(path), str(folder / prefix)])
                extracted = run(["pdftotext", "-layout", str(path), "-"]).stdout.decode("utf-8")
                sections = extracted.split("\f")
                require(len(sections) == 4 and not sections[-1].strip(), "Unexpected whole-document extraction page boundaries")
                expected_first = [] if prefix == "source" else authored
                require(lines(sections[0]) == expected_first, "Poppler: first-page text differs")
                require(lines(sections[1]) == native and not sections[2].strip(), "Poppler: native or blank page differs")
            for index, entry in enumerate(page_checks, 1):
                left_size, left = pixel_data(folder / f"source-{index}.png")
                right_size, right = pixel_data(folder / f"reviewed-{index}.png")
                require(left_size == right_size and left == right, f"Page {index}: rendered pixels changed")
                if index == 3:
                    require(all(value == 255 for value in left), "Expected visually blank white page")
                entry["render_100dpi"] = {"size_px": list(left_size), "rgb_pixels_equal": True, "rgb_pixels_sha256": digest(left)}

        return {
            "status": "pass",
            "scope": "Bundled fictional three-page example only",
            "versions": {
                "pypdf": importlib.metadata.version("pypdf"),
                "PyMuPDF_VersionBind": pymupdf.VersionBind,
                "Pillow": importlib.metadata.version("Pillow"),
                "pdftoppm": version("pdftoppm"),
                "pdftotext": version("pdftotext"),
            },
            "files": files,
            "pages": page_checks,
            "whole_document_extraction": {
                "consumers": ["pypdf", "PyMuPDF", "Poppler pdftotext -layout"],
                "reviewed_page_1_matches_all_authored_lines_in_order": True,
                "native_page_2_text_and_content_stream_preserved": True,
                "blank_page_3_text_and_content_stream_preserved": True,
                "superseded_ocr_lines_absent": True,
            },
            "search": search_checks,
            "corrected_full_lines_near_source_regions": True,
            "limitations": [
                "Pixel equality is measured at 100 DPI with the recorded Poppler version.",
                "Decoded image samples were compared independently of the render.",
                "Search checks cover short single-line queries in this fixture.",
                "Viewer UI search, clipboard copying and word-level selection were not tested.",
                "No accessibility, PDF/A, signature or general security certification.",
                "No forms, annotations, protected files, rotated pages or other languages were exercised.",
            ],
        }
    finally:
        src_doc.close()
        out_doc.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--example-dir", type=Path, default=Path(__file__).resolve().parents[1] / "examples")
    parser.add_argument("--temp-parent", type=Path, help="Optional existing directory for temporary render files")
    args = parser.parse_args()
    try:
        report = check(args.example_dir, args.temp_parent)
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        print(json.dumps({"status": "fail", "reason": str(error)}, indent=2), file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
