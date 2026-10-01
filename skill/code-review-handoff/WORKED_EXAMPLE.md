# Worked example: preview metadata handoff

This fictional offline example prepares a review artifact from complete supplied source bundles. It is not a repository connection or a completed human review. In actual use, inspect the authorized immutable change and its available context, and execute permitted relevant tests when their environment and side effects are understood.

## Request and source bundle

> Prepare the review handoff for PREVIEW-14/revision-3, from preview-before-v1 to preview-after-v1. The reviewer owns the preview response contract. Use only the four supplied paths and attached result records. Do not edit the change, post the handoff, request reviewers or merge.

Each file below is represented as an array of source lines. Reconstruct its text by joining lines with `\n` and appending a final newline. Line numbers in the handoff refer to these arrays, starting at one. The scope identifiers are SHA-256 digests of each **whole bundle**, serialized as compact JSON with sorted object keys, ASCII escaping and no trailing newline. These are fixture snapshot identifiers, not claimed Git commits.

```json
{
  "scope": "supplied four-file snapshot pair; not a complete repository",
  "base": {
    "label": "preview-before-v1",
    "sha256": "e64f0a6dd7fcf35fd5afc338d6643a13c4b8e70c836a7eae50332b23cf18a667",
    "files": {
      "src/preview.py": [
        "def preview(rows, limit=2):",
        "    return {\"rows\": list(rows[:limit])}"
      ],
      "tests/test_preview.py": [
        "from preview import preview",
        "",
        "def test_default():",
        "    assert preview([\"a\", \"b\", \"c\"])[\"rows\"] == [\"a\", \"b\"]"
      ],
      "generated/preview.schema.json": [
        "{\"type\":\"object\",\"required\":[\"rows\"],\"properties\":{\"rows\":{\"type\":\"array\",\"items\":{\"type\":\"string\"}}}}"
      ],
      "docs/preview-contract.md": [
        "Preview takes a sequence of strings and returns its first two rows by default."
      ]
    }
  },
  "head": {
    "label": "preview-after-v1",
    "sha256": "aa4f85d4ec33a8e725e055c06666b40f125b524a4c790088ff88ca8a99d501bb",
    "files": {
      "src/preview.py": [
        "def preview(rows, limit=2):",
        "    if type(limit) is not int or limit < 0:",
        "        raise ValueError(\"limit must be a non-negative integer\")",
        "    selected = list(rows[:limit])",
        "    return {\"rows\": selected, \"has_more\": len(rows) > limit}"
      ],
      "tests/test_preview.py": [
        "from preview import preview",
        "",
        "def test_default():",
        "    assert preview([\"a\", \"b\", \"c\"]) == {\"rows\": [\"a\", \"b\"], \"has_more\": True}",
        "",
        "def test_zero():",
        "    assert preview([\"a\"], 0) == {\"rows\": [], \"has_more\": True}",
        "",
        "def test_empty():",
        "    assert preview([]) == {\"rows\": [], \"has_more\": False}",
        "",
        "def test_negative():",
        "    try:",
        "        preview([\"a\"], -1)",
        "    except ValueError:",
        "        return",
        "    raise AssertionError(\"negative limit accepted\")"
      ],
      "generated/preview.schema.json": [
        "{\"type\":\"object\",\"required\":[\"rows\",\"has_more\"],\"properties\":{\"rows\":{\"type\":\"array\",\"items\":{\"type\":\"string\"}},\"has_more\":{\"type\":\"boolean\"}}}"
      ],
      "docs/preview-contract.md": [
        "Preview takes a sequence of strings; limit defaults to 2.",
        "Limit must be a non-negative integer, excluding booleans.",
        "The response contains rows and has_more; zero selects no rows."
      ]
    }
  },
  "requirement": {
    "id": "PREVIEW-14/revision-3",
    "owner_rationale": "Expose whether more rows exist so the preview UI can decide whether to request another page.",
    "criteria": {
      "AC1": "Return at most limit rows in their original order; default limit is 2.",
      "AC2": "Accept only non-negative integer limits, excluding booleans; invalid limits raise ValueError.",
      "AC3": "has_more is true exactly when the input has more rows than limit; an empty input returns no rows and false.",
      "AC4": "Repeated calls with the same sequence and limit return the same result without mutating the sequence."
    }
  },
  "supplied_runs": [
    {
      "id": "RUN-118",
      "snapshot_sha256": "9999999999999999999999999999999999999999999999999999999999999999",
      "command": "python -m pytest tests/test_preview.py",
      "environment": "Python 3.12; predecessor export",
      "finished_at": "2026-10-01T08:20:00Z",
      "result": "passed",
      "complete": true,
      "reported_summary": "4 passed"
    },
    {
      "id": "RUN-123",
      "snapshot_sha256": "aa4f85d4ec33a8e725e055c06666b40f125b524a4c790088ff88ca8a99d501bb",
      "command": "python -m pytest tests/test_preview.py",
      "environment": "Python 3.12; candidate fixture",
      "finished_at": "2026-10-01T09:00:00Z",
      "result": "canceled",
      "complete": false,
      "reported_summary": "2 passed before cancellation; no final suite result"
    }
  ]
}
```

Missing surrounding context is explicit: no HTTP handler, consumer code, schema generator, dependency lockfile, CI definition or paging state is supplied. An imported module named `preview` in the test file refers to the supplied `src/preview.py`. The allowed input rows are a finite sequence of strings; generator support is not part of this requirement.

## Expected artifact: review handoff draft

Subject: PREVIEW-14/revision-3, preview-before-v1 → preview-after-v1

Immutable manifest: use the full base and head bundle SHA-256 identifiers from the fixture above. Both digests must verify before using this draft. All four paths changed; there are no renames or claimed hidden files. Test evidence is attached to those identifiers rather than an interchangeable branch label.

Intent, attributed to the requirement owner: expose whether more rows exist so the preview UI can decide whether to request another page. The supplied code establishes metadata production; it does not establish that the UI uses it correctly.

Behavioral summary:

- Before, `src/preview.py:1–2` returned only `rows`, used Python slicing for the limit and accepted negative and boolean limits through that operation
- After, `src/preview.py:2–3` rejects limits outside the explicit non-negative-integer contract; lines 4–5 retain ordered slicing and return `has_more`
- A zero limit on a nonempty input returns no rows and `has_more=true`; an empty input returns no rows and `has_more=false`. Repeated calls do not mutate the supplied sequence in the fixture
- The generated schema makes `has_more` a required response field. This is contract-bearing output and needs review even though it is generated

Reading order and path classification:

| Order | Path | Classification and review purpose |
|---|---|---|
| 1 | docs/preview-contract.md:1–3 | Interface documentation: input contract, default and response shape |
| 2 | src/preview.py:1–5 | Behavior: validation, selected rows and remaining-row predicate |
| 3 | generated/preview.schema.json:1 | Generated interface: new required boolean; affects schema consumers |
| 4 | tests/test_preview.py:3–17 | Tests: default, zero, empty and negative cases; supplied logs are not a complete current pass |

Acceptance-criterion evidence map:

| Criterion | Implementation/diff evidence | Test evidence and limit |
|---|---|---|
| AC1 | Base line 2 → head lines 1 and 4 retains ordered slicing and default 2 | `test_default`, head test lines 3–4; supplied full pass is stale |
| AC2 | Head source lines 2–3 adds strict type and range checks | `test_negative`, lines 12–17; committed tests do not explicitly cover bool, float, string or null |
| AC3 | Head source line 5 adds `len(rows) > limit`; generated schema line 1 requires the boolean | `test_default`, `test_zero`, `test_empty`, lines 3–10; exact-boundary behavior lacks a committed assertion |
| AC4 | Head lines 4–5 create a selected list and do not assign into rows | No committed repeated-operation test; local example assertion checks repeated calls and unchanged input |

Revision-specific verification ledger:

| Evidence | Revision match | Observed result | What it establishes |
|---|---|---|---|
| RUN-118, pytest command and environment from fixture | Different digest; predecessor content unavailable | Reported complete pass, 4 passed | Stale result; neither final-head verification nor proof of which tests existed at predecessor |
| RUN-123, same command on exact head | Current | Canceled after reported 2 passes | Partial observation only; current suite completion unknown |
| Local example replay, Python 3.12.14 on 2026-10-01 | Reconstructed source verified against exact head bundle digest | Supplied four test functions and independent boundary/invalid/repeat assertions pass | Offline source behavior for this fixture only; no pytest collection, project dependencies, schema generation or CI validation |

Highest-value reviewer questions:

1. At `generated/preview.schema.json:1`, is the stricter response schema consumed by clients that can see a pre-change server during rollout? Provide a client/server compatibility check or rollout ordering. This is an unresolved compatibility question, not a demonstrated defect.
2. At `src/preview.py:2–3`, does the unavailable HTTP entry point translate `ValueError` into the established client-error response? Provide the handler and invalid-input integration assertion. The local exception behavior is proven; the external response is unknown.
3. At `tests/test_preview.py:3–17`, should committed coverage include boolean and null rejection, `len(rows) == limit`, and repeated calls? The local assertions support the current source, but do not replace repository tests or a completed exact-head run.

Reviewer decision still needed: evaluate the response-contract transition, boundary error mapping and coverage expectations against the missing context. No approval, posting, merge or deployment has occurred.

## Ambiguous and failure branches

- **Named head moves:** if another export arrives under `preview-after-v1` with different contents, recompute its digest. Treat it as a new scope, not a silent update to this draft. Request the intended immutable candidate and carry old result records as history only.
- **Mixed source bundle:** if a supplied digest does not match reconstructed files, stop review-wide conclusions. Identify the mismatched bundle and ask for an internally consistent export. Do not choose whichever source makes the tests green.
- **Green but stale:** replacing RUN-123 with another pass for RUN-118's digest still leaves final-head test completion unknown. Similar filenames do not create a reuse policy.
- **Missing generated source:** the schema can be inspected as an artifact, but without generator inputs/command it cannot be claimed reproducible. Keep it in the review path, with that specific limit.

## Independently executable assertions

Run from the repository root. This check reconstructs only the synthetic source, verifies scope, executes supplied tests in memory, independently exercises additional behavior, and classifies supplied evidence. It does not import repository code or execute a service command.

```python
import copy
import difflib
import hashlib
import json
import re
from pathlib import Path

text = Path("skill/code-review-handoff/WORKED_EXAMPLE.md").read_text()
f = json.loads(re.search(r"```json\n(.*?)\n```", text, re.S).group(1))
def digest(files):
    raw = json.dumps(files, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(raw.encode()).hexdigest()
for side in ("base", "head"):
    assert digest(f[side]["files"]) == f[side]["sha256"]
a, b = f["base"]["files"], f["head"]["files"]
changed = {p for p in set(a) | set(b) if a.get(p) != b.get(p)}
assert changed == {"src/preview.py", "tests/test_preview.py",
                   "generated/preview.schema.json", "docs/preview-contract.md"}
assert len(list(difflib.unified_diff(a["src/preview.py"], b["src/preview.py"]))) > 0
scope = {}
exec("\n".join(b["src/preview.py"]), scope)
preview = scope["preview"]
# Bind the already reconstructed function instead of importing a filesystem module.
test_lines = b["tests/test_preview.py"]
assert test_lines[0] == "from preview import preview"
exec("\n".join(test_lines[1:]), scope)
for name in sorted(scope):
    if name.startswith("test_"):
        scope[name]()
rows = ["cedar", "elm", "ash"]
before = rows.copy()
assert preview(rows) == {"rows": ["cedar", "elm"], "has_more": True}
assert preview(rows, 3) == {"rows": before, "has_more": False}
assert preview(rows, 5)["has_more"] is False
assert preview([], 0) == {"rows": [], "has_more": False}
assert preview(rows, 1) == preview(rows, 1)
assert rows == before
for bad in (-1, True, False, 1.0, "1", None):
    try:
        preview(rows, bad)
    except ValueError:
        pass
    else:
        raise AssertionError(f"accepted invalid limit: {bad!r}")
schema = json.loads(b["generated/preview.schema.json"][0])
assert set(schema["required"]) == {"rows", "has_more"}
assert schema["properties"]["has_more"]["type"] == "boolean"
statuses = []
for run in f["supplied_runs"]:
    if run["snapshot_sha256"] != f["head"]["sha256"]:
        statuses.append("stale")
    elif not run["complete"] or run["result"] != "passed":
        statuses.append("not a complete pass")
    else:
        statuses.append("current pass")
assert statuses == ["stale", "not a complete pass"]
tampered = copy.deepcopy(b)
tampered["src/preview.py"][4] = '    return {"rows": selected, "has_more": False}'
assert digest(tampered) != f["head"]["sha256"]
print("PASS: immutable scope, changed paths, supplied tests, independent behavior and stale evidence")
```

Observed validation: the fenced check passed with Python 3.12.14 on 2026-10-01. Full-bundle digests, changed-path coverage, supplied test assertions, independent edge cases, generated contract and stale/partial evidence classification were checked. These are local synthetic observations, not results retrieved from CI or an actual reviewer.
