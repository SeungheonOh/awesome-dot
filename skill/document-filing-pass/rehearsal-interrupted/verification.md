# Verify an interrupted filing record

This fresh fictional case tests a different boundary from the [original manifest example](../example.md): a concurrent edit, a successful move whose response timed out, an explicitly failed move, and a move whose outcome cannot be read back.

Read [input.md](input.md) first. The [result](result.md) and [compact manifest](manifest.json) were produced from that closed packet using the filing workflow. The executable checks below compare the JSON manifest's recorded states with the supplied observations, replay verified metadata changes, preserve an unknown current state and reject deliberate corruptions. The human-readable result, next steps and recovery instructions were separately reviewed against the same packet; the script does not validate that prose or execute a reversal. These checks do not simulate a real connector or establish access to any service.

## Expected conclusions from the observations

- O1 changes F011's name/revision outside this filing pass. Its stale plan is held; the outside rename is not undone
- O2 holds **both** identical-byte records without selecting a representative
- O3 applies the authorized distinct-transaction suffix to F014 and verifies both metadata writes
- O4 holds F015 because the target's inherited access is broader
- O5 resolves F016's timeout through its later ID read; retrying that move is unnecessary
- O6 preserves F017's verified intermediate name in the inbox; only its move remains outstanding
- O7 leaves F018's current state unknown. The last successful inbox observation is historical; a missing readback is not a failed move
- O8 supports seven current states. The absence of create/delete calls in the journal does not prove the unreachable file's current existence or location

A later authorized recovery must start from fresh readback. For F014/F016 it would reverse move then rename; for F017 only the verified rename exists to reverse. F018 first needs its move outcome reconciled. Every recovery write receives a new revision, not an old revision restored from the journal.

## Run the fixture checks

Run the following block from this folder with Python 3. It reads the published files, changes only in-memory copies for negative controls, and makes no service calls or file writes.

```python
import json
from copy import deepcopy
from pathlib import Path

source = Path("input.md").read_text()
manifest = json.loads(Path("manifest.json").read_text())
originals = {}
for line in source.splitlines():
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    if line.startswith("| F") and len(cells) == 5:
        fid, name, revision, checksum, _ = cells
        originals[fid] = {"name": name, "parent_ids": ["inbox-a"],
                          "revision": revision, "checksum": checksum,
                          "metadata_ref": "shared_original_metadata"}
assert set(originals) == {f"F0{i}" for i in range(11, 19)}

# Page evidence in the input fixes the kind, issuer and issue/purchase date.
# F011's later due date is deliberately not used.
classification = {
    "F011": ("2026-09-28", "Alder-Studio", "Invoice", "invoices-a"),
    "F012": ("2026-09-29", "North-Paper", "Receipt", "receipts-a"),
    "F013": ("2026-09-29", "North-Paper", "Receipt", "receipts-a"),
    "F014": ("2026-10-01", "North-Paper", "Receipt", "receipts-a"),
    "F016": ("2026-09-30", "Cedar-Works", "Invoice", "invoices-a"),
    "F017": ("2026-09-30", "Meadow-Goods", "Receipt", "receipts-a"),
    "F018": ("2026-10-01", "Elm-Services", "Invoice", "invoices-a"),
}
plans = {fid: (f"{day}_{issuer}_{kind}.pdf", folder)
         for fid, (day, issuer, kind, folder) in classification.items()}
plans["F014"] = (plans["F014"][0][:-4] + "__014.pdf", "receipts-a")
plans["F015"] = ("Alder-Devices_L2_User-Manual.pdf", "manuals-a")

# Expected call responses and outcomes come directly from O3/O5/O6/O7.
trace = [
    ("F014", "rename", "success", "verified_applied", "O3"),
    ("F014", "move", "success", "verified_applied", "O3"),
    ("F016", "rename", "success", "verified_applied", "O5"),
    ("F016", "move", "timeout", "verified_applied_after_timeout", "O5"),
    ("F017", "rename", "success", "verified_applied", "O6"),
    ("F017", "move", "explicit_failure_before_state_change: move unavailable",
     "verified_not_applied", "O6"),
    ("F018", "rename", "success", "verified_applied", "O7"),
    ("F018", "move", "timeout", "unknown", "O7"),
]

def verify(m):
    rows = {r["file_id"]: r for r in m["files"]}
    assert len(rows) == len(m["files"]) == len(originals)
    assert set(rows) == set(originals) == set(m["scope"]["authorized_file_ids"])
    assert m["shared_original_metadata"] == {
        "owner_id": "owner-a", "effective_access": "private-owner-a",
        "file_type": "application/pdf"}
    for fid, row in rows.items():
        assert row["original"] == originals[fid]
        name, parent = plans[fid]
        assert (row["planned_target"]["name"], row["planned_target"]["parent_ids"]) == (name, [parent])
        assert row["planned_target"]["revision"] is None
        for field in ("last_observed", "current_state"):
            state = row[field]
            if state is not None:
                assert state["checksum"] == originals[fid]["checksum"]
                assert state["metadata_ref"] == "shared_original_metadata"
        assert row["current_state"] == (None if fid == "F018" else row["last_observed"])
        assert row["current_confidence"] == ("unknown_after_timeout" if fid == "F018" else "verified_at_O8")
        first_observation = {"F011": "O1", "F012": "O2", "F013": "O2",
                             "F014": "O3", "F015": "O4", "F016": "O5",
                             "F017": "O6", "F018": "O7"}[fid]
        assert row["last_observed_refs"] == [first_observation] + ([] if fid == "F018" else ["O8"])
        if fid in classification:
            day, issuer, kind, _ = classification[fid]
            assert (row["classification"]["date"], row["classification"]["issuer"].replace(" ", "-"),
                    row["classification"]["kind"]) == (day, issuer, kind)

    journal = m["operation_journal"]
    operations = {op["id"]: op for op in journal}
    assert len(journal) == len(operations) == len(trace)
    assert [op["order"] for op in journal] == list(range(1, 9))
    assert [(op["file_id"], op["action"], op["response"], op["outcome"], op["observation"])
            for op in journal] == trace

    def resolve(reference):
        parts = reference.split(".")
        value = (rows | operations)[parts[0]]
        for key in parts[1:]:
            value = value[key]
        return value

    state = deepcopy(originals)
    for op in journal:
        fid = op["file_id"]
        assert resolve(op["before_state_ref"]) == state[fid]
        readback = op.get("readback")
        if readback is None and op.get("readback_ref") is not None:
            readback = resolve(op["readback_ref"])
        if op["outcome"] == "unknown":
            assert readback is None and op["retried"] is False
            assert state[fid] == rows[fid]["last_observed"]
            assert rows[fid]["current_state"] is None
            continue
        assert readback is not None
        expected = deepcopy(state[fid])
        if op["outcome"] != "verified_not_applied":
            field = "name" if op["action"] == "rename" else "parent_ids"
            expected[field] = (resolve(op["requested_name_ref"]) if field == "name"
                               else op["requested_parent_ids"])
            assert readback["revision"] != state[fid]["revision"]
            expected["revision"] = readback["revision"]
        assert readback == expected
        if op["action"] == "rename":
            assert readback["revision"] == originals[fid]["revision"] + "b"
        state[fid] = deepcopy(readback)
        if op["action"] == "move":
            assert op["retried"] is False
    for fid in ("F014", "F016", "F017", "F018"):
        assert state[fid] == rows[fid]["last_observed"]
        assert rows[fid]["operation_refs"] == [op["id"] for op in journal if op["file_id"] == fid]

    # Held cases have no attempted operation in the journal.
    for fid in ("F011", "F012", "F013", "F015"):
        assert rows[fid]["disposition"] == "held" and rows[fid]["operation_refs"] == []
    for fid in ("F012", "F013", "F015"):
        assert rows[fid]["current_state"] == originals[fid]
    assert rows["F012"]["original"]["checksum"] == rows["F013"]["original"]["checksum"]
    changed = deepcopy(originals["F011"])
    changed.update(name="reviewed-by-owner.pdf", revision="r11b")
    assert rows["F011"]["current_state"] == changed
    assert m["folders"]["manuals-a_effective_access"] == "project-group"
    assert rows["F014"]["current_state"]["revision"] == "r14c"
    assert rows["F016"]["current_state"]["revision"] == "r16c"
    assert rows["F017"]["current_state"]["parent_ids"] == ["inbox-a"]
    assert rows["F017"]["current_state"]["revision"] == "r17b"
    assert rows["F018"]["last_observed"]["revision"] == "r18b"
    assert rows["F018"]["last_observed"]["parent_ids"] == ["inbox-a"]
    assert rows["F018"]["current_state"] is None
    expected_groups = {"verified_change": {"F014", "F016"},
                       "held": {"F011", "F012", "F013", "F015"},
                       "partially_applied": {"F017"}, "unresolved": {"F018"}}
    for disposition, ids in expected_groups.items():
        assert {fid for fid, r in rows.items() if r["disposition"] == disposition} == ids
        assert set(m["summary"][disposition]) == ids
    assert m["summary"]["verified_final_states"] == sum(r["current_state"] is not None for r in rows.values()) == 7
    assert m["summary"]["collection_fully_verified"] is False
    assert m["recovery_policy"]["authorized_now"] is False
    return rows

verify(manifest)

# Negative controls: each would materially misstate the supplied observations.
def row(m, fid):
    return next(r for r in m["files"] if r["file_id"] == fid)
mutations = [
    lambda m: m["files"].pop(1),  # Loses one duplicate member.
    lambda m: row(m, "F018").update(current_state=deepcopy(row(m, "F018")["last_observed"])),
    lambda m: row(m, "F017")["current_state"].update(parent_ids=["receipts-a"]),
    lambda m: row(m, "F011")["planned_target"].update(name="2026-10-30_Alder-Studio_Invoice.pdf"),
    lambda m: row(m, "F014")["planned_target"].update(name="2026-10-01_North-Paper_Receipt.pdf"),
    lambda m: m["operation_journal"][3].update(retried=True),
    lambda m: row(m, "F016")["current_state"].update(checksum="different-bytes"),
    lambda m: m["summary"].update(collection_fully_verified=True),
]
for mutate in mutations:
    corrupted = deepcopy(manifest)
    mutate(corrupted)
    try:
        verify(corrupted)
    except AssertionError:
        pass
    else:
        raise AssertionError("A corrupted manifest was accepted")
print("PASS: 8 source identities; 8 operation outcomes; verified/partial/unknown states;")
print("      duplicate and access holds; preserved bytes; 8 corruptions rejected")
```

Convenience command from this folder:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('verification.md').read_text()
code = text.split('```python\n', 1)[1].split('\n```', 1)[0]
exec(compile(code, 'interrupted-filing-check', 'exec'))
PY
```

Verified locally on 2026-10-01 with Python 3.12.14. This establishes consistency of the fictional records and the stated negative controls. No current account state, actual file move, ownership/access preservation, recovery capability or external service delivery was tested.
