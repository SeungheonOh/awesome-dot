# Fictional Recovery Spot Check

This example executes a plain-file restore rehearsal using Python's standard library. All contents, timestamps, identities and outcomes are fictional. No real user files, archives, credentials, services, application integrations, installations or network access are involved.

## Input and selection

The approved destination is a new isolated fixture folder. The selected capture is `capture-sep28`, dated `2026-09-28T18:00:00Z`; current-source observation is fictional `2026-10-01T18:00:00Z`. The explicit selection has six items:

| Selected item | Fixture condition |
| --- | --- |
| `guide.txt` | Historical backup and current source agree |
| `plan.txt` | Historical backup contains blue; later source contains green |
| `unlisted.txt` | Selected item has no entry in the historical manifest |
| `absent.txt` | Manifest entry exists; the backup payload is missing |
| `copy-check.txt` | Deliberate fixture-only truncated copy tests byte mismatch reporting |
| `drawing.fiction` | Fictional unsupported format; bytes can be checked, usability cannot |

The manifest is generated from fixture capture bytes before a later source edit. This known fixture relationship makes the expected comparisons testable. In a real backup, a manifest kept beside the payload would not prove historical authenticity by itself. The selected list, manifest and payload set are distinct so an omitted file cannot disappear from the denominator.

The deliberate short write affects only the new synthetic restored copy. It is not a real restore mode or a diagnostic operation to run on user data.

## Reproduce the executed check

Run this command from this skill folder. It extracts only the marked fixture block below and executes it. The fixture creates its own temporary source, backup and restore folders, uses exclusive destination creation, closes and reopens files, compares SHA-256 digests, asserts outcomes, then removes only those generated temporary files.

```sh
python3 - <<'PY'
from pathlib import Path
text = Path("worked-example.md").read_text(encoding="utf-8")
code = text.split("<!-- fixture-start -->\n```python\n", 1)[1].split("\n```\n<!-- fixture-end -->", 1)[0]
exec(compile(code, "fictional-restore-check", "exec"))
PY
```

<!-- fixture-start -->
```python
import hashlib
import json
import platform
from pathlib import Path
from tempfile import TemporaryDirectory


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inventory(folder):
    return {p.name: digest(p.read_bytes()) for p in sorted(folder.iterdir())}


def classify_recovered(row):
    if not row["restored_matches_backup"]:
        return "copy verification failed"
    if not row["backup_matches_manifest"]:
        return "backup-versus-manifest baseline conflict"
    if not row["restored_matches_manifest"]:
        return "restored-versus-manifest baseline conflict"
    if row["readability"] != "UTF-8 reopen passed":
        return "bytes verified; usability untested"
    return "historical bytes and text readability verified"


def check_baseline_conflict():
    # Separate synthetic fixture: a faithful copy must not erase a baseline conflict.
    with TemporaryDirectory(prefix="fictional-baseline-conflict-") as temporary:
        root = Path(temporary)
        source, backup, restored = [root / name for name in ("source", "backup", "restored")]
        for folder in (source, backup, restored):
            folder.mkdir()
        historical = b"Use the ivory cover.\n"
        (source / "sample.txt").write_bytes(historical)
        (backup / "sample.txt").write_bytes(b"Use the violet cover.\n")
        reference = {"size": len(historical), "sha256": digest(historical)}
        reference_before = json.dumps(reference, sort_keys=True)
        before = {"source": inventory(source), "backup": inventory(backup)}
        payload = (backup / "sample.txt").read_bytes()
        with (restored / "sample.txt").open("xb") as destination:
            destination.write(payload)
        recovered = (restored / "sample.txt").read_bytes()
        with (restored / "sample.txt").open("r", encoding="utf-8") as reopened:
            assert reopened.read().encode("utf-8") == recovered
        result = {
            "backup_matches_manifest": (len(payload) == reference["size"]
                                        and digest(payload) == reference["sha256"]),
            "restored_matches_backup": digest(recovered) == digest(payload),
            "restored_matches_manifest": (len(recovered) == reference["size"]
                                          and digest(recovered) == reference["sha256"]),
            "readability": "UTF-8 reopen passed",
        }
        result["outcome"] = classify_recovered(result)
        assert result["restored_matches_backup"]
        assert not result["backup_matches_manifest"]
        assert not result["restored_matches_manifest"]
        assert result["outcome"] == "backup-versus-manifest baseline conflict"
        assert before == {"source": inventory(source), "backup": inventory(backup)}
        assert json.dumps(reference, sort_keys=True) == reference_before
        result["source_backup_and_manifest_preserved"] = True
        return result


captured = {
    "guide.txt": b"Read the labels before sorting.\n",
    "plan.txt": b"Use the blue cover.\n",
    "unlisted.txt": b"Keep the sample index.\n",
    "absent.txt": b"Store the paper sleeve flat.\n",
    "copy-check.txt": b"Keep all three sample lines.\nLine two.\nLine three.\n",
    "drawing.fiction": b"Fictional drawing record; no parser is provided.\n",
}
selected = list(captured)
manifest = {
    name: {"version": "capture-sep28/" + name,
           "size": len(data), "sha256": digest(data)}
    for name, data in captured.items() if name != "unlisted.txt"
}
manifest_before = json.dumps(manifest, sort_keys=True)
rows = []

with TemporaryDirectory(prefix="fictional-restore-check-") as temporary:
    root = Path(temporary)
    source, backup, restored = [root / name for name in ("source", "backup", "restored")]
    for folder in (source, backup, restored):
        folder.mkdir()
    for name, data in captured.items():
        (source / name).write_bytes(data)
        if name in manifest and name != "absent.txt":
            (backup / name).write_bytes(data)
    (source / "plan.txt").write_bytes(b"Use the green cover.\n")
    before = {"source": inventory(source), "backup": inventory(backup)}

    for name in selected:
        row = {"item": name, "manifest_entry": name in manifest,
               "payload_found": None, "restored": False}
        if name not in manifest:
            row["outcome"] = "missing historical manifest entry"
            rows.append(row)
            continue
        if not (backup / name).is_file():
            row["payload_found"] = False
            row["outcome"] = "catalogued backup payload missing"
            rows.append(row)
            continue

        expected = manifest[name]
        payload = (backup / name).read_bytes()
        row.update(payload_found=True, backup_version=expected["version"],
                   expected_size=expected["size"], expected_sha256=expected["sha256"],
                   backup_sha256=digest(payload),
                   backup_matches_manifest=(len(payload) == expected["size"]
                                            and digest(payload) == expected["sha256"]))
        # A known fixture-only short write exercises a failed restored copy.
        copied = payload[:-1] if name == "copy-check.txt" else payload
        with (restored / name).open("xb") as destination:
            destination.write(copied)
        recovered = (restored / name).read_bytes()  # closed, then reopened
        row.update(restored=True, restored_size=len(recovered),
                   restored_sha256=digest(recovered),
                   restored_matches_backup=(digest(recovered) == digest(payload)),
                   restored_matches_manifest=(len(recovered) == expected["size"]
                                              and digest(recovered) == expected["sha256"]))
        if name.endswith(".txt"):
            with (restored / name).open("r", encoding="utf-8") as reopened:
                text = reopened.read()
            assert text.encode("utf-8") == recovered
            row["readability"] = "UTF-8 reopen passed"
            row["application_consistency"] = "not assessed; plain text only"
        else:
            row["readability"] = "untested; unsupported fictional format"
            row["application_consistency"] = "untested; no compatible application"
        row["current_source"] = (
            "changed since backup; later edit is known in fixture"
            if digest((source / name).read_bytes()) != expected["sha256"]
            else "matches historical bytes"
        )
        row["outcome"] = classify_recovered(row)
        rows.append(row)

    # Collisions must not overwrite even a previously failed restored copy.
    original = (restored / "guide.txt").read_bytes()
    try:
        with (restored / "guide.txt").open("xb") as destination:
            destination.write(b"must not overwrite")
    except FileExistsError:
        pass
    else:
        raise AssertionError("Exclusive creation did not reject a collision")
    assert (restored / "guide.txt").read_bytes() == original
    preserved = before == {"source": inventory(source), "backup": inventory(backup)}
    assert preserved and json.dumps(manifest, sort_keys=True) == manifest_before
    by_name = {row["item"]: row for row in rows}
    assert len(rows) == len(selected) == 6
    assert by_name["guide.txt"]["restored_matches_manifest"]
    assert by_name["plan.txt"]["restored_matches_manifest"]
    assert by_name["plan.txt"]["current_source"].startswith("changed since backup")
    assert by_name["unlisted.txt"]["outcome"] == "missing historical manifest entry"
    assert by_name["absent.txt"]["outcome"] == "catalogued backup payload missing"
    assert by_name["copy-check.txt"]["outcome"] == "copy verification failed"
    assert by_name["copy-check.txt"]["readability"] == "UTF-8 reopen passed"
    assert by_name["drawing.fiction"]["outcome"] == "bytes verified; usability untested"
    counts = {
        "selected": len(rows),
        "manifest_entries": sum(row["manifest_entry"] for row in rows),
        "payload_found": sum(row["payload_found"] is True for row in rows),
        "restored": sum(row["restored"] for row in rows),
        "restored_bytes_match_both_baselines": sum(
            row.get("restored_matches_backup", False)
            and row.get("restored_matches_manifest", False) for row in rows),
        "text_reopen_passed": sum(row.get("readability") == "UTF-8 reopen passed" for row in rows),
        "historical_bytes_and_text_readability_verified": sum(
            row["outcome"] == "historical bytes and text readability verified" for row in rows),
    }
    assert list(counts.values()) == [6, 5, 4, 4, 3, 3, 2]
    report = {"fixture": "synthetic plain files only",
              "environment": {"python": platform.python_version(), "os": platform.system()},
              "capture": "capture-sep28", "counts": counts,
              "source_and_backup_bytes_and_membership_preserved": preserved,
              "manifest_unchanged": True, "destination_collision_rejected": True,
              "rows": rows,
              "baseline_conflict_regression": check_baseline_conflict()}
    print(json.dumps(report, indent=2))
```
<!-- fixture-end -->

## Concrete result and next steps

The [recorded verification](verification.md) captures the executed environment, selected result values and limitations. The expected outcome is:

- Six selected items remain visible in the report; five have manifest entries, four payloads are present, and four copies are created
- Three restored copies match both byte baselines; two also pass the plain-text reopen check
- `plan.txt` is a correct historical restore even though today's source is different
- `unlisted.txt` needs historical catalog evidence; its payload search is not performed and is reported as unknown. `absent.txt` needs its actual backup payload located. Neither is silently dropped
- `copy-check.txt` decodes successfully but fails the restored-byte comparison. Readability does not rescue its integrity result. In a real authorized check, preserve the observation and retry a copy into a fresh destination after rechecking the baseline; do not edit the backup
- `drawing.fiction` matches the byte evidence but remains untested for usability. A compatible application or a user-performed open check is needed before saying it works
- The collision attempt is rejected; source and backup bytes and membership remain unchanged throughout the restore checks. This is file-content preservation, not proof of unchanged filesystem access times or all metadata
- A separate isolated regression copies a readable backup payload faithfully even though that payload disagrees with its historical manifest. It reports `backup-versus-manifest baseline conflict`, never historical success. It preserves its own source, backup and manifest; its item does not enter the six-case selection or counts

The fixture has no native application consistency check, independent manifest authentication, metadata/permissions restoration, encryption, provider restore, archive extraction, external dependencies or whole-backup coverage. Successful assertions verify this small rehearsal only. A real report must use the actual selected versions, observed service results and destination access checks.
