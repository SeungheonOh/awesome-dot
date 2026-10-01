#!/usr/bin/env python3
"""Exercise a fictional anchored merge. No network or real document adapter."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import platform
import tempfile


def digest(value):
    payload = json.dumps(value, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(payload).hexdigest()


BASE = [
    {"id": "PURPOSE", "heading": "Purpose", "text": "Prepare image entries for the archive."},
    {"id": "EXPORT", "heading": "Export", "text": "Use numbered filenames."},
    {"id": "COVER", "heading": "Cover", "text": "Use a gray cover."},
    {"id": "CREDIT", "heading": "Attribution", "text": "Keep the supplied creator credit exactly as written."},
]


def fixture():
    a = deepcopy(BASE)
    a[1]["text"] = "Use the entry identifier as the filename."
    a[2]["text"] = "Use a blue cover."
    b = deepcopy(BASE)
    b[0]["text"] = "Prepare image entries and descriptive alt text for the archive."
    b[2]["text"] = "Use a green cover."
    snapshots = {
        "base-r4": {"modified": "2026-09-20T09:00:00Z", "sections": deepcopy(BASE)},
        "branch-a-r5": {"modified": "2026-09-22T10:00:00Z", "sections": a},
        "branch-b-r8": {"modified": "2026-09-24T12:00:00Z", "sections": b},
    }
    decisions = [
        {"change": "E1", "anchor": "EXPORT", "source": "branch-a-r5", "basis": "fictional-user-message-21"},
        {"change": "E2", "anchor": "PURPOSE", "source": "branch-b-r8", "basis": "fictional-user-message-21"},
    ]
    for decision in decisions:
        decision["snapshot_digest"] = digest(snapshots[decision["source"]]["sections"])
    return snapshots, decisions


def merge(snapshots, decisions):
    """Deliberately limited to fixed, unique section IDs and whole-text edits."""
    expected_shape = [(s["id"], s["heading"]) for s in BASE]
    for snapshot in snapshots.values():
        sections = snapshot["sections"]
        if [(s["id"], s["heading"]) for s in sections] != expected_shape:
            raise ValueError("Section identity, heading or order changed; remapping is required")
    baseline = snapshots["base-r4"]["sections"]
    candidate = deepcopy(baseline)
    by_id = {s["id"]: s for s in candidate}
    accepted = []
    seen = set()
    for decision in decisions:
        anchor = decision["anchor"]
        source = snapshots[decision["source"]]["sections"]
        if digest(source) != decision["snapshot_digest"]:
            raise ValueError("Acceptance refers to a different source snapshot")
        if anchor == "CREDIT":
            raise ValueError("Protected wording is outside the authorized merge scope")
        if anchor in seen:
            raise ValueError("Competing decisions require reconciliation")
        seen.add(anchor)
        before = by_id[anchor]["text"]
        after = next(s["text"] for s in source if s["id"] == anchor)
        by_id[anchor]["text"] = after
        accepted.append({**decision, "before": before, "after": after})
    unresolved = []
    for section in baseline:
        anchor = section["id"]
        proposals = [
            {"source": key, "anchor": anchor, "text": next(s["text"] for s in snapshot["sections"] if s["id"] == anchor)}
            for key, snapshot in sorted(snapshots.items()) if key != "base-r4"
        ]
        proposals = [p for p in proposals if p["text"] != section["text"]]
        if proposals and anchor not in seen:
            unresolved.append({"anchor": anchor, "alternatives": proposals,
                               "treatment": "Retain baseline in a draft candidate, as explicitly requested",
                               "question": "Should the archive guide use the blue or green cover?"})
    return candidate, {"accepted": accepted, "unresolved": unresolved}


def save_candidate(path, candidate, expected_current_digest):
    """Toy preflight check; not an atomic remote conditional-write adapter."""
    if digest(path.read_text()) != expected_current_digest:
        raise ValueError("Destination changed; rebase before saving")
    body = "# Archive guide: draft candidate\n\nCover choice unresolved; COVER retains baseline wording.\n\n"
    body += "\n\n".join(f"## {s['heading']} [{s['id']}]\n\n{s['text']}" for s in candidate) + "\n"
    path.write_text(body, encoding="utf-8")
    if path.read_text(encoding="utf-8") != body:
        raise AssertionError("Saved readback mismatch")
    return digest(body)


def expect_error(operation, error=ValueError):
    try:
        operation()
    except error:
        return
    raise AssertionError("Expected refusal did not occur")


def main():
    snapshots, decisions = fixture()
    source_before = digest(snapshots)
    candidate, ledger = merge(snapshots, decisions)
    assert candidate[0]["text"] == "Prepare image entries and descriptive alt text for the archive."
    assert candidate[1]["text"] == "Use the entry identifier as the filename."
    assert candidate[2] == BASE[2] and candidate[3] == BASE[3]
    assert [row["anchor"] for row in ledger["unresolved"]] == ["COVER"]
    assert {row["text"] for row in ledger["unresolved"][0]["alternatives"]} == {"Use a blue cover.", "Use a green cover."}
    assert digest(snapshots) == source_before
    checks = ["accepted edits and provenance", "unresolved alternatives with baseline treatment", "protected wording and source immutability"]

    changed_times = deepcopy(snapshots)
    changed_times["branch-a-r5"]["modified"] = "2099-01-01T00:00:00Z"
    assert merge(changed_times, decisions) == (candidate, ledger)
    checks.append("timestamp does not decide acceptance")

    stale = deepcopy(snapshots)
    stale["branch-a-r5"]["sections"][1]["text"] = "A later unapproved edit"
    expect_error(lambda: merge(stale, decisions))
    checks.append("stale source approval refused")

    bad_anchor = deepcopy(snapshots)
    bad_anchor["branch-b-r8"]["sections"][1]["id"] = "PURPOSE"
    expect_error(lambda: merge(bad_anchor, decisions))
    checks.append("ambiguous section identity refused")

    protected = deepcopy(decisions)
    protected[0]["anchor"] = "CREDIT"
    expect_error(lambda: merge(snapshots, protected))
    checks.append("protected target refused")

    with tempfile.TemporaryDirectory(prefix=".example-check-", dir=Path(__file__).parent) as folder:
        destination = Path(folder) / "candidate.md"
        destination.write_text("old draft", encoding="utf-8")
        old_token = digest(destination.read_text())
        destination.write_text("another editor's draft", encoding="utf-8")
        expect_error(lambda: save_candidate(destination, candidate, old_token))
        assert destination.read_text() == "another editor's draft"
        saved_digest = save_candidate(destination, candidate, digest(destination.read_text()))
        checks.extend(["changed destination refused without overwrite", "authorized candidate saved and read back"])

    print(json.dumps({"scope": "Fictional fixed-section model only; temporary local Markdown save/readback; no live documents or connector calls",
                      "command": "python3 check_example.py", "python": platform.python_version(),
                      "platform": platform.system(), "fixture_digest": source_before,
                      "candidate_digest": saved_digest, "checks": {name: "passed" for name in checks},
                      "accepted": ledger["accepted"], "unresolved": ledger["unresolved"]}, indent=2))


if __name__ == "__main__":
    main()
