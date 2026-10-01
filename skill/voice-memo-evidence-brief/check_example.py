#!/usr/bin/env python3
"""Check only this fictional fixture's text, references and time arithmetic."""
import copy
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def json_block(path):
    blocks = re.findall(r"```json\n(.*?)\n```", path.read_text(), re.S)
    require(len(blocks) == 1, f"Expected one JSON block in {path.name}")
    return json.loads(blocks[0])


def millis(stamp):
    minutes, seconds, fraction = re.fullmatch(r"(\d{2}):(\d{2})\.(\d{3})", stamp).groups()
    require(int(seconds) < 60, "Seconds outside timebase")
    return int(minutes) * 60000 + int(seconds) * 1000 + int(fraction)


def validate(manifest, ledger, supplied):
    require(ledger["source_id"] == manifest["source_id"], "Source ID mismatch")
    require(ledger["source_revision"] == manifest["title"], "Source revision mismatch")
    require(manifest["evidence_mode"] == ledger["evidence_mode"] == "transcript_only", "Wrong evidence mode")
    require(not manifest["audio_available"] and not ledger["audio_reviewed_intervals"], "Unsupported audio review")
    require(not ledger["transcript_corrections"], "Unsupported transcript correction")
    require(manifest["timebase"] == "clip_elapsed_ms", "Unexpected timebase")
    require(manifest["mapping"] == "single_contiguous_normal_speed", "Single offset not applicable")
    segments = {item["id"]: item for item in ledger["segments"]}
    require(len(segments) == len(ledger["segments"]), "Duplicate segment ID")
    require(set(segments) == set(supplied), "Missing or invented segments")
    previous_end = 0
    represented_ms = 0
    for item in ledger["segments"]:
        start, end = item["clip_ms"]
        require(all(type(t) is int for t in item["clip_ms"] + item["original_ms"]), "Noninteger time")
        require(0 <= start < end <= manifest["clip_duration_ms"], "Span outside clip")
        # This fixture has no overlapping speech; other real sources may have it.
        require(start >= previous_end, "Unexpected overlap/order in this fixture")
        previous_end = end
        represented_ms += end - start
        require(item["original_ms"] == [t + manifest["source_offset_ms"] for t in [start, end]], "Offset mismatch")
        raw = supplied[item["id"]]
        require(item["clip_ms"] == raw["clip_ms"], "Timestamp differs from supplied transcript")
        require(item["quote"] == raw["quote"], "Exact excerpt differs from source")
        require(item["speaker"] == raw["speaker"] in manifest["speaker_labels"], "Speaker label mismatch")
    claims = {item["id"]: item for item in ledger["claims"]}
    require(len(claims) == len(ledger["claims"]), "Duplicate claim ID")
    for claim in claims.values():
        require(claim["segments"] and set(claim["segments"]) <= set(segments), "Unsupported claim reference")
        for relation in ["retracted_by", "retracts", "accepted_work", "conflicts_with", "related_to"]:
            if relation in claim:
                require(claim[relation] in claims, "Broken claim relation")
    require(claims["C01"]["state"] == "retracted" and claims["C02"]["retracts"] == "C01", "Retraction lost")
    require(ledger["current_action_ids"] == ["A01", "A02"], "Wrong current actions")
    require(claims["A01"]["due_date"] is None, "Invented relative-date resolution")
    require(claims["A02"]["owner"] is None and claims["A02"]["due_date"] is None, "Invented owner or date")
    require(claims["A02"]["due_wording"] is None, "Proposed deadline promoted to agreed deadline")
    require("[cache/cash?]" in claims["A02"]["summary"], "Word uncertainty lost")
    require(claims["B01"]["state"] == claims["B02"]["state"] == "unresolved", "Approval question settled without evidence")
    require(claims["B01"].get("related_to") == "B02" and claims["B02"].get("related_to") == "B01", "Related approval statements lost")
    require("conflicts_with" not in claims["B01"] and "conflicts_with" not in claims["B02"], "Different approver scopes are not a proved contradiction")
    require(claims["P02"]["state"] == "not_accepted_in_excerpt", "Suggestion promoted")
    return len(segments), len(claims), manifest["clip_duration_ms"] - represented_ms


def main():
    fixture = (ROOT / "fixture.md").read_text()
    manifest = json_block(ROOT / "fixture.md")
    ledger = json_block(ROOT / "example.md")
    pattern = r"### (S\d+)\n\n```text\n(\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}\.\d{3}) \| ([^\n]+)\n([^\n]+)\n```"
    rows = re.findall(pattern, fixture)
    supplied = {key: {"clip_ms": [millis(start), millis(end)], "speaker": speaker, "quote": quote}
                for key, start, end, speaker, quote in rows}
    require(len(supplied) == len(rows) == 9, "Unexpected source parsing")
    segment_count, claim_count, missing_ms = validate(manifest, ledger, supplied)
    # All local file links and explicit segment targets must exist.
    link_count = 0
    for path in ROOT.glob("*.md"):
        for destination in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            target, _, anchor = destination.partition("#")
            linked = (ROOT / target).resolve()
            require(linked.is_file(), f"Missing local link: {destination}")
            if anchor:
                require(re.search(rf"^### {re.escape(anchor.upper())}$", linked.read_text(), re.M), "Missing segment anchor")
            link_count += 1
    # Verify every original-time range in the reader-facing brief matches its cited segments.
    brief = (ROOT / "example.md").read_text().split("## Evidence ledger")[0]
    for line in brief.splitlines():
        if "; original " not in line:
            continue
        cited = re.findall(r"\[(S\d+)\]\(fixture.md#s\d+\)", line)
        ranges = re.findall(r"(\d{2}:\d{2}\.\d{3})–(\d{2}:\d{2}\.\d{3})", line)
        expected = [next(s["original_ms"] for s in ledger["segments"] if s["id"] == key) for key in cited]
        require([[millis(a), millis(b)] for a, b in ranges] == expected, "Brief citation time mismatch")
    require(manifest["source_offset_ms"] + manifest["clip_duration_ms"] == millis("04:29.500"), "Clip-end mapping mismatch")
    mutations = [
        ("wrong offset", lambda d: d["segments"][0]["original_ms"].__setitem__(0, 0)),
        ("dropped negation", lambda d: d["segments"][1].__setitem__("quote", d["segments"][1]["quote"].replace("will not", "will"))),
        ("wrong source", lambda d: d.__setitem__("source_id", "other-memo")),
        ("retracted action revived", lambda d: d["current_action_ids"].append("C01")),
        ("invented date", lambda d: next(c for c in d["claims"] if c["id"] == "A01").__setitem__("due_date", "2026-10-09")),
        ("unsupported audio review", lambda d: d["audio_reviewed_intervals"].append([0, 8000])),
    ]
    for label, mutate in mutations:
        broken = copy.deepcopy(ledger)
        mutate(broken)
        try:
            validate(manifest, broken, supplied)
        except ValueError:
            pass
        else:
            raise ValueError(f"Mutation unexpectedly passed: {label}")
    print(f"PASS: {segment_count} segments, {claim_count} claims, 2 current actions")
    print(f"PASS: source/quote/time checks, {link_count} local links, brief citation ranges")
    print(f"PASS: {missing_ms} ms unrepresented; expected unresolved-date fields preserved")
    print(f"PASS: {len(mutations)} intentionally corrupted copies rejected")
    print("LIMIT: no audio, transcription, speaker identification or external action tested")


if __name__ == "__main__":
    main()
