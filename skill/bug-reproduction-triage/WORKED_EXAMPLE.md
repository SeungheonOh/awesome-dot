# Two correctness reports, two different experiments

Both products and all data below are fictional. These are investigation designs derived from supplied contracts; no real application was accessed or tested.

## Case A: Cancel leaves a changed value visible

### Supplied evidence

- Contract A1: editing a display name changes a draft only; Save persists it; Cancel must leave the saved value unchanged
- Initial saved value: Cedar
- Report A2: open the editor, type Harbor, select Cancel, reopen the editor; Harbor is visible
- No code, logs, backend read, screenshot or application revision is supplied

The reported UI state does not establish that Harbor was persisted. The editor could have retained an unsaved draft. The contract also does not specify whether Cancel must erase an independently retained draft, so the brief must not invent that requirement.

### Reproduction brief

| Element | Instruction or expected evidence |
| --- | --- |
| Safe setup | Use an authorized disposable record with saved display name Cedar |
| Baseline | Read the saved value through an available authoritative application path; establish Cedar and record the source |
| Reset | Restore saved Cedar and start a fresh editor/session; state how pending work is cleared |
| Trigger | Open editor, type Harbor, Cancel, wait for the documented close/completion signal, then reopen |
| Visible-state observation | Record the editor's displayed value; A2 predicts Harbor, but this has not been observed here |
| Independent saved-state check | Read the persisted record through the same authoritative path used for baseline |
| Contract expectation | Saved value remains Cedar after Cancel |
| Neighbor | From reset, type Harbor and Save; saved value should become Harbor under A1 |
| Repeat | Repeat the Cancel sequence from reset, then inspect through a fresh session to distinguish cached draft from persisted state |

### Hypothesis branches

| Observation from a future authorized run | What it supports | What remains unknown |
| --- | --- | --- |
| Reused editor shows Harbor; saved record and fresh session show Cedar | Draft-state retention is plausible | Whether retaining a draft violates a separate UI contract |
| Saved record becomes Harbor after Cancel | A persistence-contract mismatch is reproduced | Which code path wrote it, and whether another event intervened |
| Neither repeated nor fresh views show Harbor | This attempted sequence did not reproduce A2 | The reporter's original environment, sequence or timing difference |
| Saved-state source is unavailable | Only the visible-state part can be checked | Whether the persistence contract failed |

No row totals, export files or empty-result filters are needed. The smallest missing product decision, if only the reused editor retains Harbor, is whether Cancel is also required to clear that editor's draft.

## Case B: exported rows do not match a filter

### Supplied evidence

Contract B1: export includes every record matching both the current archive filter and the active search predicate across all result pages. An off archive toggle excludes archived records; an on toggle includes them. Search matches project names without regard to letter case.

```csv
id,name,status
P-101,Cedar,active
P-102,Harbor,archived
P-103,Juniper,active
P-104,Kestrel,archived
```

Report B2: after switching the archive toggle off, the visible list has two rows but the CSV has four. No application access, captured request or actual CSV is supplied.

### Expected case matrix

| Case | Filter/search after reset | Expected exported IDs |
| --- | --- | --- |
| B-normal | Archives on; empty search | P-101, P-102, P-103, P-104 |
| B-reported | Archives off; empty search | P-101, P-103 |
| B-empty | Archives off; search Missing | No data rows; header behavior depends on the supplied CSV contract |
| B-composed | Archives off; search Harbor | No matching rows |
| B-repeat | Export with archives on, then turn off and export again | First all four; then only P-101 and P-103 |
| B-pages | Archives on; displayed page size two | All four matching IDs, not only the current page |

Reset must restore both the archive toggle and search, discard pending export work and establish the starting record set. A case should capture the selected filter, visible IDs, export request if safely available, and actual exported IDs. Derive the expected set from B1 and the supplied rows, not the visible list alone.

If the export contains the old row set, stale request state is a hypothesis. If exported IDs are correct but a summary count is wrong, investigate aggregation separately. Neither pattern establishes a root cause without further evidence.

## Check the input-derived expectations

This exact local snippet checks only the fictional matrix. It does not reproduce an application bug.

```python
rows = [("P-101", "Cedar", "active"),
        ("P-102", "Harbor", "archived"),
        ("P-103", "Juniper", "active"),
        ("P-104", "Kestrel", "archived")]

def expected(include_archived, search=""):
    return [i for i, name, status in rows
            if (include_archived or status == "active")
            and search.casefold() in name.casefold()]

assert expected(True) == ["P-101", "P-102", "P-103", "P-104"]
assert expected(False) == ["P-101", "P-103"]
assert expected(False, "Missing") == []
assert expected(False, "Harbor") == []
assert expected(True, "HARBOR") == ["P-102"]
assert len(expected(True)) == 4  # A display page size does not alter the export contract.
print("PASS: supplied filter expectations; no application behavior tested")
```

Observed on 2026-10-01 with Python 3.12.14: the snippet produced the stated PASS line. Case A received manual source-to-experiment review against A1 only; no executable state model or UI check was performed. Case B's expected IDs were reviewed against B1 and checked by the snippet. UI behavior, request construction, storage writes, CSV formatting and a real fix remain unrun.

[Return to the skill](SKILL.md)
