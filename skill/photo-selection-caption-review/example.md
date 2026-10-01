# Fictional example: a studio newsletter

This packet contains invented records only. No photo files, thumbnails or EXIF bytes exist in the fixture. Supplied notes are not observations; the check below validates source matching and eligibility, not visual quality, privacy clearance or publication.

## Request and evidence

**U1:** “Prepare two candidates and short captions for a public studio newsletter about glaze experiments. Use only P1–P4. Keep the review private; do not post anything. My supplied notes describe the photos, but I have not included the image files.”

**U2:** The user states that P1 and P2 are their own photos and cleared for this public newsletter. This is supplied clearance evidence, not independent legal verification. No publishing authority is granted.

| Asset / original reference | Coverage note referenced by record | Rights and audience evidence | Other supplied information |
|---|---|---|---|
| P1 / blue-tests.jpg | N1 | U2: public newsletter allowed | M1 reports GPS fields present; no metadata bytes supplied |
| P2 / amber-samples.jpg | N2 | U2: public newsletter allowed | N2 reports a parcel label may appear at the frame edge |
| P3 / guest-display.jpg | N3 | U3: permission only for a private studio recap | No metadata evidence supplied |
| P4 / kiln-overview.jpg | N2 | None supplied | The note reference conflicts with N2's asset and filename |

The note records are:

- **N1** identifies **P1 / blue-tests.jpg** and supplies the caption fact “Blue glaze tests from the September studio session”
- **N2** identifies **P2 / amber-samples.jpg** and supplies the caption fact “Amber glaze samples from the September studio session.” Its label concern is reported by the user, not observed by the assistant
- **N3** identifies **P3 / guest-display.jpg** and supplies the caption fact “Guest display at the studio.” It does not change U3's private-only permission

## Result to return

| Asset | Selection | Caption and provenance | Holds or exclusion |
|---|---|---|---|
| P1 | Provisional shortlist, first | “Blue glaze tests from the September studio session” — supplied N1, not visually confirmed | Actual image review; metadata inspection and location-exposure resolution; authority to publish |
| P2 | Provisional shortlist, second | “Amber glaze samples from the September studio session” — supplied N2, not visually confirmed | Actual image review; reported identifier concern; metadata inspection; authority to publish |
| P3 | Excluded for this audience | No public caption proposed | U3 permits only a private recap; pixels and metadata also uninspected |
| P4 | Held; not shortlisted | No caption assigned | N2 does not describe P4; clearance unknown; pixels and metadata uninspected; no publishing authority |

There are two provisional candidates and zero final-ready pictures. Their order follows the requested coverage, not a visual quality judgment. P4 must not inherit N2's caption or P2's permission because its note reference happens to point to N2. U2 does not authorize publishing P1 or P2. No files were changed or shared.

## Executable source-matching and hold check

Python 3, standard library only. The fields below encode the packet above; they do not simulate pixel inspection or connect to a photo service. The checker deliberately fails closed on ambiguous note mappings and tests that permission to publish alone would not clear missing review.

```python
from copy import deepcopy

notes = {
    "N1": {"asset": "P1", "file": "blue-tests.jpg",
           "fact": "Blue glaze tests from the September studio session"},
    "N2": {"asset": "P2", "file": "amber-samples.jpg",
           "fact": "Amber glaze samples from the September studio session"},
    "N3": {"asset": "P3", "file": "guest-display.jpg",
           "fact": "Guest display at the studio"},
}
assets = [
    {"id": "P1", "file": "blue-tests.jpg", "note": "N1",
     "clearance": "public", "gps_reported": True, "identifier_reported": False},
    {"id": "P2", "file": "amber-samples.jpg", "note": "N2",
     "clearance": "public", "gps_reported": False, "identifier_reported": True},
    {"id": "P3", "file": "guest-display.jpg", "note": "N3",
     "clearance": "private-only", "gps_reported": False, "identifier_reported": False},
    {"id": "P4", "file": "kiln-overview.jpg", "note": "N2",
     "clearance": "unknown", "gps_reported": False, "identifier_reported": False},
]

def review(rows, note_records, publish_authorized=False):
    assert len({r["id"] for r in rows}) == len(rows), "Duplicate asset ID"
    result = []
    for row in rows:
        note = note_records.get(row["note"])
        matched = bool(note and (note["asset"], note["file"]) ==
                       (row["id"], row["file"]))
        holds = {"pixels-uninspected", "metadata-uninspected"}
        if not matched:
            holds.add("source-mismatch")
        if row["clearance"] != "public":
            holds.add("audience-restricted" if row["clearance"] == "private-only"
                      else "clearance-unknown")
        if row["gps_reported"]:
            holds.add("reported-location-exposure")
        if row["identifier_reported"]:
            holds.add("reported-identifier-concern")
        if not publish_authorized:
            holds.add("publish-not-authorized")
        provisional = matched and row["clearance"] == "public"
        result.append({"asset": row["id"], "matched": matched,
                       "inspection": "uninspected", "holds": holds,
                       "provisional": provisional,
                       "caption": note["fact"] if provisional else None,
                       "caption_source": row["note"] if provisional else None,
                       "release_ready": not holds})
    return result

before = deepcopy((assets, notes))
manifest = review(assets, notes)
by_id = {r["asset"]: r for r in manifest}
assert [r["asset"] for r in manifest if r["provisional"]] == ["P1", "P2"]
assert set(by_id) == {r["id"] for r in assets}
assert all(r["inspection"] == "uninspected" and not r["release_ready"]
           for r in manifest)
for asset_id, note_id in [("P1", "N1"), ("P2", "N2")]:
    assert by_id[asset_id]["caption"] == notes[note_id]["fact"]
    assert by_id[asset_id]["caption_source"] == note_id
assert "audience-restricted" in by_id["P3"]["holds"]
assert by_id["P3"]["caption"] is None
assert not by_id["P4"]["matched"] and by_id["P4"]["caption"] is None
assert {"source-mismatch", "clearance-unknown"} <= by_id["P4"]["holds"]
assert "reported-location-exposure" in by_id["P1"]["holds"]
assert "reported-identifier-concern" in by_id["P2"]["holds"]
assert all("metadata-uninspected" in r["holds"] for r in manifest)

# A matching ID with a different filename/version must still be held.
changed_notes = deepcopy(notes)
changed_notes["N1"]["file"] = "blue-tests-different-export.jpg"
changed = review(assets, changed_notes)
assert not changed[0]["matched"] and not changed[0]["provisional"]
assert changed[0]["caption"] is None

# Publication authority resolves exactly one gate; missing review still blocks it.
authorized = review(assets, notes, publish_authorized=True)
for original, revised in zip(manifest, authorized):
    assert revised["holds"] == original["holds"] - {"publish-not-authorized"}
    assert not revised["release_ready"]
assert (assets, notes) == before
print("PASS: 4 covered assets; 2 provisional captions; 0 ready for release;")
print("      audience, source-version, privacy and publication gates remain separate")
```

Run the fenced block from the repository root:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('skill/photo-selection-caption-review/example.md').read_text()
code = text.split('```python\n', 1)[1].split('\n```', 1)[0]
exec(compile(code, 'photo-selection-example', 'exec'))
PY
```

Observed locally on 2026-10-01 with Python 3.12.14: the fenced check passed, and the skill frontmatter validator passed. The check's scope is synthetic record matching, hold preservation and input immutability. It cannot establish that any real picture is safe, cleared, accessible or visually suitable.
