# Fictional example: two books and a battery

All items, labels, dates and statements are invented. The assessment date is **2026-01-29**. B1 and B2 are distinct supplied borrower labels; both have the display name Alex. Their names are not a basis for merging them.

The supplied physical-item register is A1: *Field Guide*, red sticker; A2: *Field Guide*, blue sticker; A3: kit containing driver, battery and case; A4: pump; A5: drill; A6: tent. These are physical-copy labels, not model identifiers.

## Source packet and normalized events

Each line below is one bounded source. `recorded` is the entry date; `at` is the claimed event date, if known. Event IDs and cycle IDs are preserved from the fictional ledger. The source text is supplied alongside the extraction so a reader can inspect the mapping. S05 stays unassigned. S09 explicitly identifies a copy of S07, establishing a duplicate report of the same event rather than another return.

```json
[
  {"source":"S01","recorded":"2026-01-02","text":"Jan 2: C1, A1 red-sticker guide handed to B1; promised Jan 12.","event":"E01","kind":"checkout","cycle":"C1","asset":"A1","borrower":"B1","at":"2026-01-02","due":"2026-01-12","parts":["book"]},
  {"source":"S02","recorded":"2026-01-22","text":"Late entry: C1's A1 was returned on Jan 10, before its next loan.","event":"E02","kind":"return","cycle":"C1","at":"2026-01-10","parts":["book"]},
  {"source":"S03","recorded":"2026-01-15","text":"Jan 15: C2, A1 red-sticker guide handed to B2; promised Jan 25.","event":"E03","kind":"checkout","cycle":"C2","asset":"A1","borrower":"B2","at":"2026-01-15","due":"2026-01-25","parts":["book"]},
  {"source":"S04","recorded":"2026-01-16","text":"Jan 16: C3, A2 blue-sticker guide handed to B1; no return date agreed.","event":"E04","kind":"checkout","cycle":"C3","asset":"A2","borrower":"B1","at":"2026-01-16","due":null,"parts":["book"]},
  {"source":"S05","recorded":"2026-01-17","text":"Jan 17: Field Guide back from Alex. No sticker or borrower label recorded.","kind":"unresolved","at":"2026-01-17","candidates":["C2","C3"]},
  {"source":"S06","recorded":"2026-01-18","text":"Jan 18: C4, A3 driver, battery and case handed to B1; promised Jan 24.","event":"E06","kind":"checkout","cycle":"C4","asset":"A3","borrower":"B1","at":"2026-01-18","due":"2026-01-24","parts":["driver","battery","case"]},
  {"source":"S07","recorded":"2026-01-20","text":"Jan 20: received C4's driver and case; battery remains with B1.","event":"E07","kind":"return","cycle":"C4","at":"2026-01-20","parts":["driver","case"]},
  {"source":"S08","recorded":"2026-01-21","text":"Plan to collect C4's battery Jan 22. Nothing received; no new promise recorded.","event":"E08","kind":"planned_return","cycle":"C4","at":"2026-01-22","parts":["battery"]},
  {"source":"S09","recorded":"2026-01-22","text":"Copy of S07: same Jan 20 driver-and-case return, not another event.","kind":"duplicate","duplicate_of":"S07","same_event":"E07"},
  {"source":"S10","recorded":"2026-01-23","text":"Jan 23: agreed C4 battery return date changed from Jan 24 to Jan 28.","event":"E10","kind":"promise_change","cycle":"C4","at":"2026-01-23","due":"2026-01-28","replaces_due_source":"S06","parts":["battery"]},
  {"source":"S11","recorded":"2026-01-24","text":"Proposal: lend A4 pump to B2 Jan 26, back Jan 30. No handover reported.","event":"E11","kind":"proposed_loan","asset":"A4","borrower":"B2","at":"2026-01-26","due":"2026-01-30","parts":["pump"]},
  {"source":"S12","recorded":"2026-01-25","text":"Late entry: Jan 19, C5, A5 drill handed over. Borrower label and return promise absent.","event":"E12","kind":"checkout","cycle":"C5","asset":"A5","borrower":null,"at":"2026-01-19","due":null,"parts":["drill"]},
  {"source":"S13","recorded":"2026-01-25","text":"Existing C6: A6 tent reported with B2. Handover date absent. Due phrase 'next Friday' copied from an undated note.","event":"E13","kind":"reported_loan","cycle":"C6","asset":"A6","borrower":"B2","at":null,"due":null,"due_raw":"next Friday","parts":["tent"]},
  {"source":"S14","recorded":"2026-01-27","text":"Jan 27 correction: C2's promise was Jan 29, not Jan 25 in S03. Other S03 details unchanged.","event":"E14","kind":"promise_change","cycle":"C2","at":"2026-01-27","due":"2026-01-29","replaces_due_source":"S03","parts":["book"]},
  {"source":"S15","recorded":"2026-01-28","text":"Jan 27: C3's A2 blue-sticker guide specifically received back from B1.","event":"E15","kind":"return","cycle":"C3","at":"2026-01-27","parts":["book"]}
]
```

## Derived current ledger

| Item / cycle | Reported custody and outstanding parts | Current promise / assessment | Evidence and uncertainty |
|---|---|---|---|
| A1 red guide / C2 | Last checkout to B2; book remains open in the ledger; possible return unresolved | Jan 29, due today **if still out** | S03, corrected promise S14; S05 might be this return |
| A2 blue guide / C3 | Reported returned Jan 27; nothing outstanding | No outstanding promise | Specific return S15; S05 remains ambiguous historical evidence |
| A3 kit / C4 | Battery reported with B1; driver and case returned | Jan 28; recorded date passed | S06–S07, extension S10; S08 is a plan, S09 duplicates S07 |
| A4 pump / no actual cycle | Proposed only; current custody not established by this packet | Jan 30 is a proposal, not an active obligation | S11 is not a checkout |
| A5 drill / C5 | Reported on loan; borrower unknown | Unknown | Handover Jan 19 in S12; do not infer a borrower |
| A6 tent / C6 | Reported with B2; handover date unknown | Unresolved | S13's undated “next Friday” cannot be anchored to its filing date |

History retains C1: A1 with B1 from Jan 2 to its reported return Jan 10; original promise Jan 12. S02 was filed Jan 22, after C2 started, but closes only C1. C2 retains its original Jan 25 promise as a corrected field, with S14 as the current date's source. For C4, the battery's promise changes to Jan 28; the already-returned driver's and case's historical promise stays Jan 24.

Useful result: three items/parts are reported outstanding without a competing return claim (A3 battery, A5 drill, A6 tent), plus A1 whose return is unresolved. The battery's recorded return date has passed. No physical possession was independently verified. Ask: which sticker and borrower label does S05 concern; who received A5; and what dated source resolves A6's promise? A2's specific later return resolves its current ledger state even while S05 remains unassigned.

## Executable reconciliation and save-readback check

This is a small checker for these supplied normalized events, not a general note parser or a live ledger integration. It derives cycle balances from the input, tests source coverage, injects invalid history and changed-source cases, and round-trips a synthetic ledger in a temporary directory beneath this skill folder. It uses Python's standard library only.

```python
import copy
import json
from pathlib import Path
from tempfile import TemporaryDirectory

folder = Path("skill/borrowed-item-return-ledger")
document = (folder / "example.md").read_text()
rows = json.loads(document.split("```json\n", 1)[1].split("\n```", 1)[0])

def merge_sources(existing, incoming):
    merged = {r["source"]: copy.deepcopy(r) for r in existing}
    for row in incoming:
        key = row["source"]
        if key in merged and merged[key] != row:
            raise ValueError("changed source requires review")
        merged[key] = copy.deepcopy(row)
    return list(merged.values())

def reconcile(incoming):
    sources = merge_sources([], incoming)
    by_source = {r["source"]: r for r in sources}
    events = [r for r in sources if "event" in r]
    assert len({r["event"] for r in events}) == len(events)
    disposition = {}
    cycles = {}
    for row in sources:
        kind = row["kind"]
        disposition[row["source"]] = kind
        if kind == "duplicate":
            original = by_source[row["duplicate_of"]]
            assert original["event"] == row["same_event"]
        if kind not in {"checkout", "reported_loan"}:
            continue
        assert row["cycle"] not in cycles
        assert len(row["parts"]) == len(set(row["parts"]))
        cycles[row["cycle"]] = {
            "asset": row["asset"], "borrower": row["borrower"],
            "start": row["at"], "kind": kind,
            "lent": sorted(row["parts"]), "remaining": sorted(row["parts"]),
            "due": {p: row["due"] for p in row["parts"]},
            "due_source": {p: row["source"] for p in row["parts"]},
            "closed": None, "events": [row["event"]],
        }
    # Use actual dates and explicit cycle references, never entry order.
    for row in sorted(events, key=lambda r: (r["at"] or "", r["event"])):
        if row["kind"] not in {"return", "promise_change", "planned_return"}:
            continue
        cycle = cycles[row["cycle"]]
        cycle["events"].append(row["event"])
        if row["kind"] == "planned_return":
            continue
        if cycle["start"] is not None and row["at"] < cycle["start"]:
            raise ValueError("event predates its checkout")
        if row["kind"] == "return":
            if not set(row["parts"]) <= set(cycle["remaining"]):
                raise ValueError("return exceeds outstanding parts")
            cycle["remaining"] = sorted(set(cycle["remaining"]) - set(row["parts"]))
            if not cycle["remaining"]:
                cycle["closed"] = row["at"]
        else:
            for part in row["parts"]:
                assert cycle["due_source"][part] == row["replaces_due_source"]
                cycle["due"][part] = row["due"]
                cycle["due_source"][part] = row["source"]
    for cid, cycle in cycles.items():
        returned = len(cycle["lent"]) - len(cycle["remaining"])
        assert 0 <= returned <= len(cycle["lent"])
    # Known intervals for the same physical copy must not overlap.
    for asset in {c["asset"] for c in cycles.values()}:
        known = sorted((c for c in cycles.values()
                        if c["asset"] == asset and c["start"] is not None),
                       key=lambda c: c["start"])
        for earlier, later in zip(known, known[1:]):
            if earlier["closed"] is None or earlier["closed"] >= later["start"]:
                raise ValueError("overlapping or unresolved same-day cycles")
    return {"sources": sources, "cycles": cycles, "disposition": disposition}

result = reconcile(rows)
c = result["cycles"]
assert len(rows) == len(result["disposition"]) == 15
assert len({r["event"] for r in rows if "event" in r}) == 13
assert {s for s, d in result["disposition"].items() if d == "unresolved"} == {"S05"}
assert {s for s, d in result["disposition"].items() if d == "duplicate"} == {"S09"}
assert {s for s, d in result["disposition"].items() if d.startswith("proposed")
        or d.startswith("planned")} == {"S08", "S11"}
assert len(c) == 6
assert {key: value["remaining"] for key, value in c.items()} == {
    "C1": [], "C2": ["book"], "C3": [], "C4": ["battery"],
    "C5": ["drill"], "C6": ["tent"],
}
assert c["C1"]["closed"] == "2026-01-10"
assert c["C2"]["borrower"] == "B2" and c["C2"]["asset"] == "A1"
assert c["C3"]["closed"] == "2026-01-27" and c["C3"]["asset"] == "A2"
assert not any(cycle["asset"] == "A4" for cycle in c.values())
assert c["C4"]["due"] == {
    "driver": "2026-01-24", "battery": "2026-01-28", "case": "2026-01-24"}
assert c["C2"]["due"]["book"] == "2026-01-29"
assert c["C2"]["due_source"]["book"] == "S14"
assert c["C5"]["borrower"] is None and c["C5"]["due"]["drill"] is None
assert c["C6"]["start"] is None and c["C6"]["due"]["tent"] is None

def date_state(due, as_of):
    if due is None:
        return "unknown"
    return "past" if due < as_of else "today" if due == as_of else "future"

assert date_state(c["C4"]["due"]["battery"], "2026-01-29") == "past"
assert date_state(c["C2"]["due"]["book"], "2026-01-29") == "today"
assert date_state(None, "2026-01-29") == "unknown"
assert date_state("2026-01-29", "2026-01-28") == "future"
assert date_state("2026-01-29", "2026-01-30") == "past"

# Entry order and replay do not change the derived cycle history.
assert reconcile(sorted(rows, key=lambda r: r["recorded"]))["cycles"] == c
assert reconcile(list(reversed(rows)))["cycles"] == c
assert merge_sources(rows, rows) == rows

def must_reject(operation, reason):
    try:
        operation()
    except (ValueError, AssertionError):
        return
    raise AssertionError(reason)

bad = copy.deepcopy(rows)
next(r for r in bad if r["source"] == "S02")["cycle"] = "C2"
must_reject(lambda: reconcile(bad), "old return must not close the newer cycle")
bad = copy.deepcopy(rows)
next(r for r in bad if r["source"] == "S07")["parts"].append("charger")
must_reject(lambda: reconcile(bad), "cannot return a part never lent")
bad = copy.deepcopy(rows)
next(r for r in bad if r["source"] == "S02")["at"] = "2026-01-16"
must_reject(lambda: reconcile(bad), "same physical copy cannot overlap cycles")
changed = copy.deepcopy(rows[0])
changed["borrower"] = "B2"
must_reject(lambda: merge_sources(rows, [changed]), "changed source must be reviewed")

# A narrow update preserves unaffected cycles and all original source records.
initial_rows = [r for r in rows if r["source"] not in {"S14", "S15"}]
before = reconcile(initial_rows)
updated = reconcile(merge_sources(initial_rows, rows))
for cid in {"C1", "C4", "C5", "C6"}:
    assert before["cycles"][cid] == updated["cycles"][cid]
assert before["cycles"]["C2"]["due"]["book"] == "2026-01-25"
assert updated["cycles"]["C2"]["due"]["book"] == "2026-01-29"
assert before["cycles"]["C3"]["remaining"] == ["book"]
assert updated["cycles"]["C3"]["remaining"] == []
assert {r["source"]: r for r in updated["sources"]} == {r["source"]: r for r in rows}
with TemporaryDirectory(dir=folder) as temporary:
    path = Path(temporary) / "fictional-ledger.json"
    path.write_text(json.dumps(updated, indent=2))
    reopened = json.loads(path.read_text())
    assert reopened == updated
    replay = reconcile(merge_sources(reopened["sources"], rows))
    assert replay == reopened
print("PASS: 15 sources; 13 distinct events; 6 loan cycles; 4 open cycle balances")
print("PASS: ambiguous copy, old-cycle return, partial set, proposal and unknown fields")
print("PASS: date boundaries, invalid-event rejection, idempotent update and local readback")
```

Run from the repository root:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('skill/borrowed-item-return-ledger/example.md').read_text()
code = text.split('```python\n', 1)[1].split('\n```', 1)[0]
exec(compile(code, 'borrowed-item-example', 'exec'))
PY
```

## Observed verification and limits

Executed on 2026-10-01 with Python 3.12.14. All three PASS lines above were observed. The temporary save was reopened, compared in full and replayed without duplicating sources; temporary files were removed by the check. Local frontmatter and relative-link checks also passed.

These checks validate the synthetic extraction, cycle arithmetic, specified failure cases and a local file round-trip. They do not establish physical possession, resolve S05, anchor S13's missing date, infer any person's identity, parse arbitrary messages, or verify a live app write, concurrent-edit handling, sharing or external action. The four open balances include C2's unresolved possible return; they are not four proven present-day possessions.
