#!/usr/bin/env python3
"""Audit the supplied fictional export adapter locally. Never fetch or import."""
import argparse
import csv
from hashlib import sha256
import io
import json
from pathlib import Path
import re
import stat
import zipfile

MAX_ARCHIVE = 2 * 1024 * 1024
MAX_MEMBER = 256 * 1024
MAX_TOTAL = 1024 * 1024
MAX_MEMBERS = 32


class UnsupportedArchive(ValueError):
    pass


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def load_json(data):
    def invalid_constant(value):
        raise ValueError("non-standard JSON number")
    return json.loads(data.decode("utf-8"), object_pairs_hook=unique_object, parse_constant=invalid_constant)


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def read_archive(path):
    """Inspect a bounded ZIP in memory; do not extract paths or open content."""
    if not path.is_file() or path.is_symlink() or path.stat().st_size > MAX_ARCHIVE:
        raise UnsupportedArchive("not a regular bounded ZIP input")
    raw = path.read_bytes()
    members = {}
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        entries = archive.infolist()
        if len(entries) > MAX_MEMBERS or sum(e.file_size for e in entries) > MAX_TOTAL:
            raise UnsupportedArchive("member count or expanded byte budget exceeded")
        seen = set()
        for entry in entries:
            name = entry.filename
            allowed = name in {"manifest.json", "records.json"} or re.fullmatch(
                r"attachments/[A-Za-z0-9_-]+/[A-Za-z0-9_.-]+", name)
            mode = stat.S_IFMT(entry.external_attr >> 16)
            if (not allowed or name.rsplit("/", 1)[-1] in {".", ".."} or name.casefold() in seen or mode not in {0, stat.S_IFREG}
                    or entry.flag_bits & 1 or entry.compress_type not in {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED}
                    or entry.file_size > MAX_MEMBER
                    or entry.file_size > max(1, entry.compress_size) * 100):
                raise UnsupportedArchive("member layout, type, encryption or size is unsupported")
            seen.add(name.casefold())
            with archive.open(entry) as member:
                data = member.read(MAX_MEMBER + 1)
            if len(data) != entry.file_size:
                raise UnsupportedArchive("member byte count disagrees with ZIP directory")
            members[name] = data
    if "manifest.json" not in members or "records.json" not in members:
        raise UnsupportedArchive("required export members are absent")
    manifest = load_json(members["manifest.json"])
    records = load_json(members["records.json"])
    if not isinstance(manifest, dict) or manifest.get("schema") != "fictional-export-v1":
        raise UnsupportedArchive("unrecognized manifest schema")
    for key in ("part_number", "part_count", "declared_records", "declared_total_records"):
        if type(manifest.get(key)) is not int or manifest[key] < (1 if key in {"part_number", "part_count"} else 0):
            raise UnsupportedArchive("invalid part or count metadata")
    if any(key not in manifest or (manifest[key] is not None and not isinstance(manifest[key], str))
           for key in ("cursor", "next_cursor")):
        raise UnsupportedArchive("explicit part cursor metadata is required")
    if not isinstance(records, list) or len(records) > 1000:
        raise UnsupportedArchive("records must be a bounded JSON array")
    for record in records:
        if not isinstance(record, dict) or any(not isinstance(record.get(k), str) or not record[k]
                                             for k in ("id", "kind", "state", "revision")):
            raise UnsupportedArchive("record identity fields must be nonempty strings")
        refs = record.get("attachment_ids", [])
        if not isinstance(refs, list) or any(not isinstance(v, str) for v in refs) or len(set(refs)) != len(refs):
            raise UnsupportedArchive("attachment references must be distinct string IDs")
    if path.read_bytes() != raw:
        raise UnsupportedArchive("input changed during inspection")
    return {"name": path.name, "bytes": len(raw), "sha256": sha256(raw).hexdigest(),
            "manifest": manifest, "records": records, "members": members}


def chain_complete(pages):
    if not pages:
        return False
    cursor = None
    seen = set()
    for index, page in enumerate(pages):
        if "cursor" not in page or "next_cursor" not in page or page["cursor"] != cursor or cursor in seen:
            return False
        seen.add(cursor)
        cursor = page.get("next_cursor")
        if cursor is None and index != len(pages) - 1:
            return False
    return cursor is None


def write_new(root, relative, data):
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("xb") as stream:
        stream.write(data)


def audit(fixtures, archives, output, incomplete_control=False):
    need_bytes = (fixtures / "need.json").read_bytes()
    control_bytes = (fixtures / "source-control.json").read_bytes()
    inventory_bytes = (fixtures / "source-inventory.csv").read_bytes()
    need, control = load_json(need_bytes), load_json(control_bytes)
    if type(need.get("consolidation_authorized")) is not bool:
        raise ValueError("consolidation_authorized must be a JSON boolean")
    rows = list(csv.DictReader(io.StringIO(inventory_bytes.decode("utf-8"), newline="")))
    for row in rows:
        if row["in_scope"] not in {"yes", "no"}:
            raise ValueError("in_scope must be exactly yes or no in the source inventory")
        if row["body_presence"] not in {"present", "not_applicable", "absent_expected", "unexamined"}:
            raise ValueError("unsupported body_presence in the source inventory")
        if row["in_scope"] == "yes":
            if row["state"] == "deleted":
                required_presence = "absent_expected"
            elif row["kind"] == "collection":
                required_presence = "not_applicable"
            elif row["kind"] in {"note", "comment"} and row["state"] in {"active", "archived"}:
                required_presence = "present"
            else:
                raise ValueError("unsupported selected object kind/lifecycle in the source inventory")
            if row["body_presence"] != required_presence:
                raise ValueError("selected object body_presence disagrees with kind/lifecycle")
    if len({r["id"] for r in rows}) != len(rows):
        raise ValueError("source control repeats an object ID")
    expected = {r["id"]: r for r in rows if r["in_scope"] == "yes"}
    exclusions = [r for r in rows if r["in_scope"] == "no"]
    if incomplete_control:
        control["listing_pages"] = control["listing_pages"][:1]
    blockers = []
    pages = control["listing_pages"]
    listed_ids = [identifier for page in pages for identifier in page["ids"]]
    control_complete = (chain_complete(pages) and len(set(listed_ids)) == len(listed_ids)
                        and set(listed_ids) == {r["id"] for r in rows})
    if not control_complete:
        blockers.append("Independent listing is not terminal and reconciled; the source denominator is unconfirmed.")
    if (any(need[key] != control[key] for key in ("account_id", "collection_id", "generation", "scope"))
            or need["snapshot_at"] != control["observed_at"]
            or need["export_request_id"] != control["expected_export_request_id"]):
        blockers.append("Independent controls do not identify the requested snapshot and selection.")

    accepted, archive_inventory = [], []
    for archive_path in archives:
        try:
            part = read_archive(archive_path)
        except (ValueError, KeyError, zipfile.BadZipFile, RuntimeError, OSError, RecursionError) as error:
            archive_inventory.append({"name": archive_path.name, "status": "held", "reason": str(error)})
            continue
        manifest = part["manifest"]
        mismatches = [key for key in ("account_id", "collection_id", "generation", "snapshot_at", "scope")
                      if manifest.get(key) != need[key]]
        if manifest.get("request_id") != need["export_request_id"]:
            mismatches.append("request_id")
        summary = {key: part[key] for key in ("name", "bytes", "sha256")}
        summary.update({"generation": manifest.get("generation"), "request_id": manifest.get("request_id"),
                        "part_number": manifest.get("part_number"), "record_ids": [r["id"] for r in part["records"]],
                        "record_versions": [{"id": r["id"], "revision": r["revision"]} for r in part["records"]],
                        "members": [{"path": name, "bytes": len(data), "sha256": sha256(data).hexdigest()}
                                    for name, data in sorted(part["members"].items())]})
        if mismatches:
            summary.update(status="held", reason="Different " + ", ".join(mismatches) + "; never used to fill this snapshot.")
        else:
            summary.update(status="selected", reason="Matches the requested snapshot identity; reconciliation still required.")
            accepted.append(part)
        archive_inventory.append(summary)

    expected_parts = control["expected_part_numbers"]
    part_numbers = [p["manifest"].get("part_number") for p in accepted]
    missing_parts = [n for n in expected_parts if n not in part_numbers]
    parts_complete = (sorted(part_numbers, key=str) == sorted(expected_parts, key=str)
                      and len(set(part_numbers)) == len(part_numbers))
    ordered = sorted(accepted, key=lambda p: str(p["manifest"].get("part_number")))
    if not parts_complete:
        blockers.append("Requested export parts are missing, repeated or unexpected.")
    if parts_complete and not chain_complete([p["manifest"] for p in ordered]):
        blockers.append("Export part cursors do not form one terminal chain.")
    for part in accepted:
        manifest = part["manifest"]
        if manifest.get("declared_records") != len(part["records"]) or manifest.get("part_count") != len(expected_parts):
            blockers.append("Archive manifest counts disagree with the supplied part evidence: " + part["name"])
    declared_totals = {p["manifest"].get("declared_total_records") for p in accepted}
    if len(declared_totals) != 1 or (parts_complete and next(iter(declared_totals), None) != sum(len(p["records"]) for p in accepted)):
        blockers.append("Archive-declared totals are inconsistent; these totals are not independent coverage evidence.")

    by_id, attachment_members, lineage = {}, {}, []
    for part in ordered:
        for index, record in enumerate(part["records"]):
            by_id.setdefault(record["id"], []).append(record)
            lineage.append({"id": record["id"], "archive": part["name"], "archive_sha256": part["sha256"],
                            "member": "records.json", "record_index": index})
        for name, data in part["members"].items():
            if name.startswith("attachments/"):
                attachment_members.setdefault(name, []).append((part, data))
    duplicate_ids = [identifier for identifier, occurrences in by_id.items() if len(occurrences) != 1]
    unexpected_ids = sorted(set(by_id) - set(expected))
    if duplicate_ids or unexpected_ids:
        blockers.append("Record IDs are repeated or outside the expected selection; no winner was chosen.")
    record_inventory = []
    for identifier, expected_row in expected.items():
        occurrences = by_id.get(identifier, [])
        issues = []
        if not occurrences:
            status, body_presence = "missing", "unavailable"
        elif len(occurrences) != 1:
            status, body_presence = "conflicting", "ambiguous"
        else:
            record = occurrences[0]
            body_presence = "absent" if "body" not in record else ("null" if record["body"] is None else ("empty" if record["body"] == "" else "present"))
            for key in ("kind", "state", "revision"):
                if record.get(key) != expected_row[key]:
                    issues.append(key + " disagrees with source control")
            if record.get("parent_id") != (expected_row["parent_id"] or None):
                issues.append("parent identity differs")
            if record.get("parent_id") is not None and record["parent_id"] not in by_id:
                issues.append("parent is unavailable in the selected set")
            if record.get("attachment_ids", []) != json.loads(expected_row["attachment_ids"]):
                issues.append("attachment reference list differs")
            if expected_row["body_presence"] == "present" and not isinstance(record.get("body"), str):
                issues.append("required text body is omitted or null")
            if expected_row["body_presence"] == "absent_expected" and ("body" in record or not isinstance(record.get("deleted_at"), str)):
                issues.append("deletion marker semantics differ")
            status = "matched" if not issues else "conflicting"
        record_inventory.append({"id": identifier, "kind": expected_row["kind"], "state": expected_row["state"],
                                 "expected_revision": expected_row["revision"], "status": status,
                                 "body_presence": body_presence, "issues": issues})
    if any(r["status"] != "matched" for r in record_inventory):
        blockers.append("Required source objects or properties are missing or conflicting.")

    attachment_inventory = []
    actual_refs = [ref for occurrences in by_id.values() for record in occurrences for ref in record.get("attachment_ids", [])]
    expected_pairs = [(row["id"], ref) for row in expected.values() for ref in json.loads(row["attachment_ids"])]
    expected_refs = [ref for owner, ref in expected_pairs]
    control_by_pair, path_counts, control_id_counts = {}, {}, {}
    for item in control["attachments"]:
        control_by_pair.setdefault((item["owner_id"], item["id"]), []).append(item)
        path_counts[item["path"]] = path_counts.get(item["path"], 0) + 1
        control_id_counts[item["id"]] = control_id_counts.get(item["id"], 0) + 1
    attachment_controls_complete = (set(control_by_pair) == set(expected_pairs)
        and len(set(expected_pairs)) == len(expected_pairs)
        and all(len(items) == 1 for items in control_by_pair.values())
        and all(count == 1 for count in path_counts.values())
        and all(count == 1 for count in control_id_counts.values()))
    unexpected_attachment_controls = [{"owner_id": owner, "id": identifier}
        for owner, identifier in sorted(set(control_by_pair) - set(expected_pairs))]
    if not attachment_controls_complete:
        blockers.append("Independent attachment controls do not uniquely cover every expected attachment ID and owner; byte coverage is unconfirmed.")
    expected_paths = {a["path"] for pair, items in control_by_pair.items() if pair in expected_pairs for a in items}
    if sorted(actual_refs) != sorted(expected_refs):
        blockers.append("Selected record attachment references do not equal the independently expected references.")
    for owner, identifier in expected_pairs:
        controls = control_by_pair.get((owner, identifier), [])
        if len(controls) != 1:
            attachment_inventory.append({"id": identifier, "owner_id": owner, "path": None, "bytes": None,
                "sha256": None, "status": "unresolved", "observed_bytes": None, "observed_sha256": None,
                "reason": "Independent attachment control is absent or repeated."})
            continue
        item = controls[0]
        matches = attachment_members.get(item["path"], [])
        result = dict(item, status="missing", observed_bytes=None, observed_sha256=None)
        if len(matches) == 1:
            part, data = matches[0]
            digest = sha256(data).hexdigest()
            owner = by_id.get(item["owner_id"], [])
            owner_matches = len(owner) == 1 and item["id"] in owner[0].get("attachment_ids", [])
            result.update(status="matched" if len(data) == item["bytes"] and digest == item["sha256"] and owner_matches else "conflicting",
                          observed_bytes=len(data), observed_sha256=digest, archive=part["name"])
        elif len(matches) > 1:
            result["status"] = "conflicting"
        if path_counts[item["path"]] != 1 or control_id_counts[item["id"]] != 1:
            result["status"] = "conflicting"
        attachment_inventory.append(result)
    unreferenced = sorted(set(attachment_members) - expected_paths)
    if any(a["status"] != "matched" for a in attachment_inventory) or unreferenced:
        blockers.append("Attachment payloads, ownership or independent byte evidence are unresolved.")

    counts = {"expected_objects": len(expected), "matched_objects": sum(r["status"] == "matched" for r in record_inventory),
              "missing_objects": sum(r["status"] == "missing" for r in record_inventory),
              "conflicting_objects": sum(r["status"] == "conflicting" for r in record_inventory),
              "unexpected_objects": len(unexpected_ids), "excluded_control_objects": len(exclusions),
              "expected_attachments": len(expected_pairs),
              "matched_attachments": sum(a["status"] == "matched" for a in attachment_inventory),
              "expected_attachment_bytes": sum(a["bytes"] for a in attachment_inventory) if attachment_controls_complete else None,
              "matched_attachment_bytes": sum(a["observed_bytes"] for a in attachment_inventory if a["status"] == "matched"),
              "observed_attachment_references": len(actual_refs), "held_archives": sum(a["status"] == "held" for a in archive_inventory)}
    supported = not blockers
    report = {"status": "supported-for-stated-snapshot-copy" if supported else "held",
              "purpose": need["purpose"], "snapshot": {key: need[key] for key in ("account_id", "collection_id", "generation", "snapshot_at", "scope")},
              "control_complete": control_complete, "control_variant": "incomplete-page-evidence" if incomplete_control else "as-supplied",
              "attachment_controls_complete": attachment_controls_complete,
              "unexpected_attachment_controls": unexpected_attachment_controls,
              "control_hashes": {"need.json": sha256(need_bytes).hexdigest(), "source-control.json": sha256(control_bytes).hexdigest(), "source-inventory.csv": sha256(inventory_bytes).hexdigest()},
              "counts": counts, "missing_parts": missing_parts, "archives": archive_inventory,
              "records": record_inventory, "attachments": attachment_inventory, "lineage": lineage,
              "excluded_control_rows": exclusions, "unexpected_ids": unexpected_ids, "duplicate_ids": duplicate_ids,
              "unreferenced_payloads": unreferenced, "blockers": blockers, "limitations": control["limitations"] + need["excluded_properties"],
              "consolidated_copy_created": supported and need["consolidation_authorized"]}
    # Exclusive new run directory prevents an older successful copy surviving a held run.
    output.mkdir(parents=True, exist_ok=False)
    if report["consolidated_copy_created"]:
        records = [record for part in ordered for record in part["records"]]
        write_new(output, "consolidated/records.json", encoded(records))
        write_new(output, "consolidated/lineage.json", encoded(lineage))
        write_new(output, "consolidated/snapshot.json", encoded(report["snapshot"]))
        for item in attachment_inventory:
            write_new(output, "consolidated/" + item["path"], attachment_members[item["path"]][0][1])
    write_new(output, "audit.json", encoded(report))
    lines = ["# Account export audit", "", "Status: " + report["status"], "", need["purpose"], "",
             "Selected snapshot: " + need["generation"] + " at " + need["snapshot_at"] + ".",
             "Independent listing terminal and reconciled: " + str(control_complete).lower() + ".", "",
             "## Reconciliation", "",
             f"Objects: {counts['expected_objects']} expected = {counts['matched_objects']} matched + {counts['missing_objects']} missing + {counts['conflicting_objects']} conflicting.",
             f"Explicit exclusions: {len(exclusions)}. Unexpected selected objects: {len(unexpected_ids)}.",
             f"Attachments: {counts['matched_attachments']}/{counts['expected_attachments']} matched; {counts['matched_attachment_bytes']}/{counts['expected_attachment_bytes'] if counts['expected_attachment_bytes'] is not None else 'unknown total'} bytes verified against separate control digests.",
             f"Missing required parts: {missing_parts or 'none'}. Held archives: {counts['held_archives']}.", "",
             "## Object inventory", ""]
    lines += [f"- {r['id']}: {r['status']}; expected {r['state']} revision {r['expected_revision']}; body {r['body_presence']}" + ("; " + "; ".join(r["issues"]) if r["issues"] else "") for r in record_inventory]
    lines += ["", "## Attachment inventory", ""]
    lines += [f"- {a['id']} owned by {a['owner_id']}: {a['status']}; expected {a['bytes'] if a['bytes'] is not None else 'unknown'} bytes; observed {a['observed_bytes'] if a['observed_bytes'] is not None else 'unavailable'}; {a['path'] or 'path unconfirmed'}" for a in attachment_inventory]
    lines += ["", "## Explicit scope exclusions", ""]
    lines += [f"- {r['id']}: {r['reason']}" for r in exclusions]
    lines += ["", "## Part decisions", ""]
    lines += [f"- {a['name']}: {a['status']}; {a['reason']}" for a in archive_inventory]
    lines += ["", "## Next action", ""]
    if blockers:
        lines += ["No consolidated copy was created.", ""] + ["- " + b for b in blockers]
        if missing_parts:
            lines += ["", "Supply the missing part from export-cobalt at generation-42. The later amber part cannot fill that gap."]
    elif report["consolidated_copy_created"]:
        lines += ["The consolidated copy preserves all five selected raw objects and both attachment payloads. Keep the held later archive separate. Destination import behavior needs a separate rehearsal."]
    else:
        lines += ["The evidence supports the stated snapshot requirement. No consolidated copy was requested, so only this audit was created."]
    lines += ["", "## What this establishes", "", "Coverage of the independently listed, filtered snapshot selection and the checked properties only. Archive totals are internal consistency checks. No live account or provider-wide completeness was checked.", ""]
    lines += ["- " + limitation for limitation in report["limitations"]]
    write_new(output, "report.md", ("\n".join(lines) + "\n").encode("utf-8"))
    # Saved-file readback and source preservation are checked before returning.
    assert load_json((output / "audit.json").read_bytes()) == report
    assert (fixtures / "need.json").read_bytes() == need_bytes
    assert (fixtures / "source-control.json").read_bytes() == control_bytes
    assert (fixtures / "source-inventory.csv").read_bytes() == inventory_bytes
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--archive", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--incomplete-control", action="store_true", help="Worked countercase: only the first independent listing page is supplied")
    args = parser.parse_args()
    result = audit(args.fixtures, args.archive, args.output, args.incomplete_control)
    print(json.dumps({"status": result["status"], "counts": result["counts"], "consolidated_copy_created": result["consolidated_copy_created"]}))
