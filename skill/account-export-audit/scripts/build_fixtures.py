#!/usr/bin/env python3
"""Build tiny, deterministic fictional export ZIPs; never contact an account."""
import argparse
import json
from pathlib import Path
import stat
import zipfile


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write_zip(path, members):
    with path.open("xb") as stream, zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED) as archive:
        for name, data in sorted(members.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 9, 20, 12, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            info.compress_type = zipfile.ZIP_STORED
            archive.writestr(info, data)


def build(output):
    output.mkdir(parents=True, exist_ok=False)
    scope = {"collection_id": "collection-007", "include_archived": True,
             "include_comments": True, "include_deletion_markers": True}
    common = {"schema": "fictional-export-v1", "account_id": "account-demo",
              "collection_id": "collection-007", "generation": "generation-42",
              "snapshot_at": "2026-09-20T12:00:00Z", "request_id": "export-cobalt",
              "scope": scope, "part_count": 2, "declared_total_records": 5}
    first_records = [
        {"id": "collection-007", "kind": "collection", "state": "active", "revision": "3",
         "parent_id": None, "title": "Equipment notes", "attachment_ids": []},
        {"id": "note-0001", "kind": "note", "state": "active", "revision": "4",
         "parent_id": "collection-007", "title": "Desk kit", "body": "", "attachment_ids": ["attachment-001"]}
    ]
    second_records = [
        {"id": "note-0002", "kind": "note", "state": "archived", "revision": "7",
         "parent_id": "collection-007", "title": "Loaner bag", "body": "USB-C hub and short cable\nKeep together.",
         "color": None, "tags": ["loaner", "café"], "attachment_ids": ["attachment-002"]},
        {"id": "comment-0001", "kind": "comment", "state": "active", "revision": "1",
         "parent_id": "note-0002", "body": "Return the adapter with its pouch.", "attachment_ids": []},
        {"id": "note-0003", "kind": "note", "state": "deleted", "revision": "9",
         "parent_id": "collection-007", "deleted_at": "2026-09-19T09:30:00Z"}
    ]
    first = dict(common, part_number=1, cursor=None, next_cursor="export-page-2", declared_records=2)
    second = dict(common, part_number=2, cursor="export-page-2", next_cursor=None, declared_records=3)
    write_zip(output / "cobalt-part-1.zip", {
        "manifest.json": encoded(first), "records.json": encoded(first_records),
        "attachments/attachment-001/notes.txt": b"Cable labels\nblue = desk\namber = spare\n"})
    write_zip(output / "cobalt-part-2.zip", {
        "manifest.json": encoded(second), "records.json": encoded(second_records),
        "attachments/attachment-002/notes.txt": b"Checkout notes\nKeep the short USB-C cable with the hub.\n"})
    later = dict(second, generation="generation-43", snapshot_at="2026-09-21T12:00:00Z",
                 request_id="export-amber", declared_records=1, declared_total_records=5)
    later_record = dict(second_records[0], revision="8", title="Loaner bag after checkout",
                        body="Hub checked out; cable stays on the shelf.", attachment_ids=[])
    write_zip(output / "amber-part-2.zip", {"manifest.json": encoded(later), "records.json": encoded([later_record])})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="New directory; existing paths are never overwritten")
    build(parser.parse_args().output)
