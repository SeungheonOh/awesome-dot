# Fictional Filing Pass

Every service, person, file ID, checksum label, folder and document in this example is invented. The [manifest](manifest.json) represents a simulated completed pass. Its `verified_fixture` labels are not claims of real connector actions. Checksum labels stand for trustworthy fixture equality evidence; they are not actual cryptographic digests.

## Authorized scope and naming rules

The fictional user asks to organize the six listed PDFs in `folder-inbox`, excluding subfolders, into existing Invoices, Receipts, Manuals and Warranties folders in the same account. Names should use `YYYY-MM-DD_Issuer_Type_Reference.pdf` when those fields are evidenced. Omit the reference when none is printed. Undated manuals and warranties may use `Issuer_Model_Type.pdf`. For distinct documents whose resulting names collide, the user has already approved `__` plus the final three characters of the stable file ID, if unique. Leave duplicates and ambiguous documents untouched. Preserve identities and access; do not delete or change sharing.

The baseline listing is complete in this fixture. All source files and the Invoices, Receipts and Manuals destinations are private to the fictional owner. The existing Warranties folder is readable by a project group, so that move cannot preserve effective access. `doc-900` is an existing destination receipt inspected only to resolve the name collision; it is outside the mutation scope.

## Before and after

| Stable ID | Before: Inbox name | Observed after | Result |
|---|---|---|---|
| doc-101 | scan_21.pdf | Invoices / 2026-09-18_Marlow-Studio_Invoice_MS-104.pdf | Applied in fixture; issue date and invoice reference read from page 1 |
| doc-102 | scan_22.pdf | Inbox / scan_22.pdf | Held: duplicate group with doc-103; candidate collision suffix is not applied |
| doc-103 | scan_22_copy.pdf | Inbox / scan_22_copy.pdf | Held: same bytes as doc-102; no deletion or merge |
| doc-104 | IMG_0451.pdf | Inbox / IMG_0451.pdf | Held: issuer/type unclear and date 03/04/26 ambiguous |
| doc-105 | setup.pdf | Manuals / Marlow-Devices_M8_User-Manual.pdf | Applied in fixture; permitted undated-document naming rule |
| doc-106 | warranty.pdf | Inbox / warranty.pdf | Held: target inheritance would broaden access |

The preexisting `doc-900` remains `Receipts / 2026-09-20_Quill-Repair_Receipt.pdf`. Its page-1 time and item establish a different purchase from `doc-102`. Different checksums alone would establish different bytes, not different underlying transactions. `doc-103` shares the trustworthy fixture checksum with `doc-102`. Both remain untouched under the explicit duplicate rule. The proposed `__102` collision suffix is a reversible plan candidate only; it does not override that rule.

The four held files keep their full before state, including original names and parents. A proposed name on `doc-106` is not an applied rename. No new folder, replacement file or changed permission is part of the example.

## Recovery example

To reverse the applied changes after authorization, first inspect each current file by ID, confirm its recorded post-change name/parents and suitable access, and check that its old name is available in Inbox. Reverse the operations for `doc-105`, then `doc-101`: move each file to Inbox and restore its original name. Record new service revisions from those operations; do not attempt to reset revisions to old values.

If someone has renamed `doc-101` since the pass, its state no longer matches the manifest. Hold that row rather than blindly restoring `scan_21.pdf`. If its first move-back succeeds but the rename fails, append the intermediate state. A later recovery should start from the service's actual state, not replay the entire reversal.

## Local consistency check

Run this block from the skill folder using Python 3. It checks source coverage, stable identity, access/checksum preservation, name uniqueness in affected destinations, held states, operation replay and the metadata effect of reversal. It does not contact a service or establish real permissions.

```python
import json
from copy import deepcopy
from pathlib import Path

m = json.loads(Path("manifest.json").read_text())
rows = m["records"]
assert len({r["id"] for r in rows}) == len(rows)
assert {r["id"] for r in rows} == set(m["source_file_ids"])
by_id = {r["id"]: r for r in rows}

for row in rows:
    before = row["before"]
    after = row["observed_after"]
    assert row["id"] == before["id"] == after["id"]
    assert before["access"] == after["access"]
    assert before["checksum"] == after["checksum"]
    for parent in after["parents"]:
        assert m["folders"][parent]["access"] == after["access"]

    if row["status"].startswith("held_"):
        assert row["operations"] == []
        assert before == after
        continue

    assert row["status"] == "applied_verified_fixture"
    assert after["name"] == row["planned"]["name"]
    assert after["parents"] == row["planned"]["parents"]
    state = deepcopy(before)
    for op in row["operations"]:
        assert op["status"] == "verified_fixture"
        assert state["revision"] == op["revision_before"]
        field = {"rename": "name", "move": "parents"}[op["type"]]
        assert state[field] == op["before"]
        state[field] = deepcopy(op["after"])
        state["revision"] = op["revision_after"]
    assert state == after

    # A real reversal receives NEW service revisions; only metadata is restored.
    for op in reversed(row["operations"]):
        field = {"rename": "name", "move": "parents"}[op["type"]]
        assert state[field] == op["after"]
        state[field] = deepcopy(op["before"])
    for field in ("id", "name", "parents", "access", "checksum"):
        assert state[field] == before[field]

# The fictional service compares these ASCII names without case sensitivity.
occupied = set()
for state in m["destination_baseline"] + [r["observed_after"] for r in rows]:
    for parent in state["parents"]:
        key = (parent, state["name"].casefold())
        assert key not in occupied, key
        occupied.add(key)

assert by_id["doc-103"]["duplicate_of"] == "doc-102"
assert by_id["doc-103"]["before"]["checksum"] == by_id["doc-102"]["before"]["checksum"]
assert by_id["doc-102"]["collision"]["existing_id"] == "doc-900"
assert by_id["doc-102"]["planned"]["name"].endswith("__102.pdf")
assert all(by_id[i]["status"] == "held_duplicate" for i in ("doc-102", "doc-103"))
assert all(by_id[i]["before"] == by_id[i]["observed_after"] for i in ("doc-102", "doc-103"))
assert by_id["doc-104"]["planned"] is None
assert by_id["doc-106"]["status"] == "held_access_change"
assert m["folders"][by_id["doc-106"]["planned"]["parents"][0]]["access"] != by_id["doc-106"]["before"]["access"]
print("Fictional filing manifest checks passed")
```

Observed on 2026-10-01 in Linux, Python 3.12.14: the exact block above was executed with `python` from this skill folder, printed `Fictional filing manifest checks passed` and exited successfully. The skill frontmatter validator also reported `Skill is valid!`. Fixture replay is not a live-service test and does not prove that a service supports atomic moves, revision preconditions or unchanged inherited access.
