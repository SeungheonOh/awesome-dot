#!/usr/bin/env python3
"""Small Linux-only accounting demonstration; never accepts existing data.

Create a new output folder, write five fictional paths, move one file and move
it back, and retain the observations. No deletion, cleanup scan, or network.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import stat
import subprocess


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def now():
    return datetime.now(timezone.utc).isoformat()


def command(root, args):
    result = subprocess.run(args, cwd=root, check=True, capture_output=True,
                            text=True, env={**os.environ, "LC_ALL": "C"})
    return result.stdout.strip()


def write_new(path, data):
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def row(root, relative):
    path = root / relative
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode), "Expected a generated regular file")
    data = path.read_bytes()
    after = path.lstat()
    fields = ("st_dev", "st_ino", "st_nlink", "st_size", "st_blocks", "st_mtime_ns")
    require(all(getattr(before, field) == getattr(after, field) for field in fields),
            "Generated file changed during observation")
    return {"path": relative, "device": after.st_dev, "inode": after.st_ino,
            "link_count": after.st_nlink, "logical_bytes": after.st_size,
            "allocated_512_byte_blocks": after.st_blocks,
            "reported_allocated_bytes": after.st_blocks * 512,
            "mtime_ns": after.st_mtime_ns,
            "sha256": hashlib.sha256(data).hexdigest()}


def totals(rows):
    unique = {}
    for item in rows:
        key = (item["device"], item["inode"])
        if key in unique:
            require(signature(item) == signature(unique[key]),
                    "One inode has conflicting observations")
        unique[key] = item
    return {"regular_file_paths": len(rows), "distinct_file_inodes": len(unique),
            "logical_bytes_summed_by_path": sum(r["logical_bytes"] for r in rows),
            "logical_bytes_counted_once_per_inode": sum(r["logical_bytes"] for r in unique.values()),
            "reported_allocated_bytes_summed_by_path": sum(r["reported_allocated_bytes"] for r in rows),
            "reported_allocated_bytes_counted_once_per_inode": sum(r["reported_allocated_bytes"] for r in unique.values())}


def signature(item):
    return {key: value for key, value in item.items() if key != "path"}


def snapshot(root, paths):
    observed = now()
    rows = [row(root, path) for path in sorted(paths)]
    counters = os.statvfs(root)
    du = command(root, ["du", "-B1", "-c", "--", *sorted(paths)])
    du_apparent = command(root, ["du", "--apparent-size", "-B1", "-c", "--", *sorted(paths)])
    summary = totals(rows)
    require(int(du.splitlines()[-1].split()[0]) == summary["reported_allocated_bytes_counted_once_per_inode"],
            "GNU du and inode accounting disagree")
    require(int(du_apparent.splitlines()[-1].split()[0]) == summary["logical_bytes_counted_once_per_inode"],
            "GNU apparent-size du and logical accounting disagree")
    return {"observed_at_utc": observed, "files": rows, "totals": summary,
            "volume": {"device": root.stat().st_dev,
                       "fragment_bytes": counters.f_frsize,
                       "available_fragments": counters.f_bavail,
                       "available_bytes": counters.f_bavail * counters.f_frsize},
            "gnu_du_explicit_files_bytes": du,
            "gnu_du_explicit_files_apparent_bytes": du_apparent}


def fixture_move(root, source, destination, expected):
    # This is a single-process fixture in an exclusively created directory,
    # not a general mover for directories other people or apps can change.
    src, dst = root / source, root / destination
    require(signature(row(root, source)) == signature(expected), "Source precondition changed")
    require(src.parent.stat().st_dev == dst.parent.stat().st_dev, "Different filesystem")
    require(not os.path.lexists(dst), "Destination collision; nothing overwritten")
    os.rename(src, dst)
    observed = row(root, destination)
    require(not os.path.lexists(src), "Source name still present")
    require(signature(observed) == signature(expected), "Move readback mismatch")
    return {"operation": "same-filesystem rename", "source": source,
            "destination": destination, "before": expected, "after": observed,
            "source_absent": True, "content_and_inode_preserved": True,
            "status": "verified", "observed_at_utc": now()}


def run(output):
    require(platform.system() == "Linux", "This fixture requires Linux")
    require(hasattr(os.stat_result, "st_blocks"), "Allocated-block observations unavailable")
    versions = {name: command(Path.cwd(), [name, "--version"]).splitlines()[0]
                for name in ("du", "stat")}
    require(all("GNU coreutils" in value for value in versions.values()),
            "This fixture uses GNU coreutils options")
    # Exclusive root creation is deliberate: an existing directory is rejected.
    output.mkdir(mode=0o700)
    root = output / "fictional-files"
    root.mkdir()
    for name in ("Downloads", "Projects", "Review"):
        (root / name).mkdir()
    export = (b"fictional,row\n" * 631)[:8192]
    require(len(export) == 8192, "Unexpected fixture size")
    write_new(root / "Projects/current-export.csv", export)
    write_new(root / "Downloads/export-copy.csv", export)
    os.link(root / "Projects/current-export.csv", root / "Downloads/export-linked.csv")
    write_new(root / "Projects/keep-notes.txt", b"Fictional notes: keep the current export.\n")
    with (root / "Downloads/scratch-capture.bin").open("xb") as sparse:
        sparse.seek(65535)
        sparse.write(b"!")
        sparse.flush()
        os.fsync(sparse.fileno())
    paths = ["Downloads/export-copy.csv", "Downloads/export-linked.csv",
             "Downloads/scratch-capture.bin", "Projects/current-export.csv",
             "Projects/keep-notes.txt"]
    before = snapshot(root, paths)
    indexed = {r["path"]: r for r in before["files"]}
    keeper = indexed["Projects/current-export.csv"]
    linked = indexed["Downloads/export-linked.csv"]
    copied = indexed["Downloads/export-copy.csv"]
    require((keeper["device"], keeper["inode"]) == (linked["device"], linked["inode"]),
            "Hard-link fixture did not share its inode")
    require(keeper["link_count"] == linked["link_count"] == 2, "Unexpected links")
    require(copied["inode"] != keeper["inode"] and copied["sha256"] == keeper["sha256"],
            "Equal-byte independent-copy fixture failed")
    require(indexed["Downloads/scratch-capture.bin"]["reported_allocated_bytes"] < 65536,
            "This filesystem did not expose sparse allocation; do not claim that test passed")
    source, destination = "Downloads/export-copy.csv", "Review/export-copy.csv"
    plan = {"scope": "Only the five newly generated files in fictional-files",
            "authority": "Move the separate copy to Review, verify it, then restore it; no deletion",
            "before_files": before["files"],
            "ordered_actions": [{"source": source, "destination": destination},
                                {"source": destination, "destination": source}],
            "expected_payload_bytes_freed": 0,
            "recovery": "Inspect both names and compare the saved identity and digest before any retry or reversal"}
    write_new(output / "plan.json", (json.dumps(plan, indent=2) + "\n").encode())
    # Freeze the pre-action record before taking the volume baseline so its
    # own allocation is not confused with a change caused by the move.
    before = snapshot(root, paths)
    require(before["files"] == plan["before_files"], "Pre-action inventory changed")
    first = fixture_move(root, source, destination, copied)
    after_move = snapshot(root, [destination if p == source else p for p in paths])
    second = fixture_move(root, destination, source, first["after"])
    after_restore = snapshot(root, paths)
    require(before["totals"] == after_move["totals"] == after_restore["totals"],
            "A move changed the regular-file accounting")
    require(before["files"] == after_restore["files"], "Restored inventory differs")
    for item in after_move["files"]:
        if item["path"] != destination:
            require(item == indexed[item["path"]], "Unselected generated file changed")
    # The useful collision check changes nothing: current-export already exists.
    collision_rejected = False
    try:
        fixture_move(root, source, "Projects/current-export.csv", copied)
    except RuntimeError as error:
        require(str(error) == "Destination collision; nothing overwritten", "Unexpected failure")
        collision_rejected = True
    require(collision_rejected, "Collision was not rejected")
    require([row(root, path) for path in sorted(paths)] == before["files"],
            "Collision check changed the fixture")
    evidence = {
        "scope": "Five generated regular-file paths; Linux fixture only",
        "environment": {"system": "Linux", "python": platform.python_version(),
                        "filesystem_type": command(root, ["stat", "-f", "-c", "%T", "."]),
                        "tools": versions},
        "before": before, "after_move": after_move, "after_restore": after_restore,
        "journal": [first, second],
        "verification": {"independent_copy_same_bytes": True, "hard_link_same_inode": True,
                         "sparse_allocation_observed": True, "move_readback": True,
                         "restore_readback": True, "other_files_preserved": True,
                         "collision_rejected_without_overwrite": collision_rejected,
                         "gnu_du_totals_agree": True},
        "accounting": {
            "requested_additional_available_bytes": 8192,
            "regular_file_reported_allocation_reduction_bytes":
                before["totals"]["reported_allocated_bytes_counted_once_per_inode"] - after_move["totals"]["reported_allocated_bytes_counted_once_per_inode"],
            "observed_volume_available_delta_after_move_bytes":
                after_move["volume"]["available_bytes"] - before["volume"]["available_bytes"],
            "observed_volume_available_delta_after_restore_bytes":
                after_restore["volume"]["available_bytes"] - before["volume"]["available_bytes"],
            "attributable_payload_bytes_freed_by_rename": 0,
            "target_met_by_this_action": False,
            "caution": "Volume deltas can include unrelated activity and directory metadata; they are not attributed savings. Inode-deduplicated allocation is not exclusive physical usage."}}
    dispositions = {
        source: ("move then restore", "Executed within the fictional request; no deletion", destination),
        "Downloads/export-linked.csv": ("keep", "Another name for the retained current export; zero payload reduction from removing only this link", None),
        "Downloads/scratch-capture.bin": ("hold", "Logical size overstates reported allocation; purpose unresolved", None),
        "Projects/current-export.csv": ("keep", "Retained authoritative fictional export", None),
        "Projects/keep-notes.txt": ("keep", "Explicitly retained notes", None)}
    manifest = {
        "fictional_request": "Inspect these five files to assess an 8192-byte free-space goal. Move only export-copy.csv to Review, read it back, then restore it as a rehearsal. Leave all other files alone; do not delete anything.",
        "volume_device": before["volume"]["device"], "unit": "bytes",
        "rows": [{"before": item, "action": dispositions[item["path"]][0],
                  "reason": dispositions[item["path"]][1],
                  "temporary_destination": dispositions[item["path"]][2],
                  "final_path": item["path"],
                  "verified_payload_bytes_freed": 0,
                  "status": "verified moved and restored" if item["path"] == source else "unchanged"}
                 for item in before["files"]],
        "remove_operations": [],
        "recovery": "The authorized reversal was verified. Original names and byte digests match the before inventory. No files were deleted.",
        "next_decision": "The 8192-byte goal remains unmet. A move to Review is organizational staging. Assess a separately authorized space-releasing action before changing real data."}
    for name, value in (("evidence.json", evidence), ("manifest.json", manifest)):
        write_new(output / name, (json.dumps(value, indent=2) + "\n").encode())
    print(json.dumps({"result": "PASS", "checks": evidence["verification"],
                      "accounting": evidence["accounting"]}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("new_output_directory", type=Path,
                        help="Must not already exist; its parent must exist")
    run(parser.parse_args().new_output_directory)
