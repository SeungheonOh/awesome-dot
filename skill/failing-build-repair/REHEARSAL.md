# Fresh-input repair rehearsal: independent preference values

This is a fictional local correctness fixture. The repaired implementation was not supplied as part of the input. The exercise produced a minimal patch and regression tests; the same tests were run before and after the patch, followed by independent combination checks. No account, service or real application was involved.

## Input contract and report

The complete input implementation is below. The requested result was a minimal local repair and evidence, using only Python's standard library.

- `prepare_preferences(None)` uses defaults
- A supplied dictionary replaces named top-level fields; it does not recursively merge them
- Valid fixture inputs contain a string layout, a unique panel-name list and a filter-flag mapping; empty values and explicit zero/false are meaningful
- Preserve panel order and add `help` once only if absent
- Do not modify defaults or caller inputs
- Every returned nested list and mapping must be independent, so editing one result cannot change input, defaults or another result
- Do not add validation, supported types, persistence or other features outside the contract

Reported symptoms were repeated default calls adding another `help`, and a caller's custom panel list gaining `help` after the function ran. These reports were reproduced locally before changing the fixture.

### Original implementation

```python
"""Fictional local view-preference fixture. No I/O or external dependencies."""

DEFAULT_PREFERENCES = {
    "layout": "compact",
    "panels": ["summary"],
    "filters": {"archived": False},
}


def prepare_preferences(overrides=None):
    result = DEFAULT_PREFERENCES.copy()
    if overrides:
        result.update(overrides)
    result["panels"].append("help")
    return result
```

## Observed repair

The outer dictionary copy left nested containers shared. Inserting caller-owned overrides also retained their nested references. The repair deep-copies the selected result after top-level replacement and adds a membership guard. It preserves existing replacement behavior and introduces no external dependency.

```python
"""Fictional local view-preference fixture. No I/O or external dependencies."""

from copy import deepcopy

DEFAULT_PREFERENCES = {
    "layout": "compact",
    "panels": ["summary"],
    "filters": {"archived": False},
}


def prepare_preferences(overrides=None):
    result = DEFAULT_PREFERENCES.copy()
    if overrides:
        result.update(overrides)
    result = deepcopy(result)
    if "help" not in result["panels"]:
        result["panels"].append("help")
    return result
```

## Regression tests produced for the contract

Each test loads a fresh module state so one failure cannot contaminate the next. The same assertions are used against both implementations; none were weakened to make the repair pass.

```python
"""Offline regression checks for the supplied synthetic preference contract."""

from copy import deepcopy
from pathlib import Path
import runpy
import unittest


class PreparePreferencesTests(unittest.TestCase):
    def setUp(self):
        # Load a fresh fixture per test so one mutation cannot mask another.
        namespace = runpy.run_path(str(Path(__file__).with_name("preferences.py")))
        self.prepare = namespace["prepare_preferences"]
        self.defaults = namespace["DEFAULT_PREFERENCES"]
        self.original_defaults = deepcopy(self.defaults)

    def test_none_uses_defaults_and_appends_help(self):
        self.assertEqual(
            self.prepare(None),
            {
                "layout": "compact",
                "panels": ["summary", "help"],
                "filters": {"archived": False},
            },
        )

    def test_default_call_does_not_mutate_defaults(self):
        self.prepare()
        self.assertEqual(self.defaults, self.original_defaults)

    def test_repeated_default_calls_remain_stable(self):
        first = self.prepare()
        second = self.prepare()
        self.assertEqual(first["panels"], ["summary", "help"])
        self.assertEqual(second["panels"], ["summary", "help"])

    def test_custom_panels_keep_order_without_mutating_input(self):
        overrides = {"panels": ["chart", "details"]}
        before = deepcopy(overrides)
        result = self.prepare(overrides)
        self.assertEqual(result["panels"], ["chart", "details", "help"])
        self.assertEqual(overrides, before)

    def test_existing_help_is_not_duplicated_or_reordered(self):
        for panels in (["help"], ["help", "chart"], ["chart", "help", "details"]):
            with self.subTest(panels=panels):
                overrides = {"panels": list(panels)}
                result = self.prepare(overrides)
                self.assertEqual(result["panels"], panels)
                self.assertEqual(overrides["panels"], panels)

    def test_empty_panels_are_selected_and_help_is_added(self):
        overrides = {"panels": []}
        result = self.prepare(overrides)
        self.assertEqual(result["panels"], ["help"])
        self.assertEqual(overrides["panels"], [])

    def test_top_level_filters_replace_rather_than_merge(self):
        result = self.prepare({"filters": {"starred": True}})
        self.assertEqual(result["filters"], {"starred": True})

    def test_explicit_empty_and_false_like_values_survive(self):
        result = self.prepare(
            {"layout": "", "panels": [], "filters": {"archived": False, "count": 0}}
        )
        self.assertEqual(result["layout"], "")
        self.assertEqual(result["panels"], ["help"])
        self.assertIs(result["filters"]["archived"], False)
        self.assertEqual(result["filters"]["count"], 0)
        self.assertEqual(self.prepare({"filters": {}})["filters"], {})

    def test_empty_override_dictionary_uses_defaults(self):
        self.assertEqual(self.prepare({}), self.prepare(None))

    def test_default_results_have_independent_nested_containers(self):
        first = self.prepare()
        second = self.prepare()
        self.assertIsNot(first, second)
        self.assertIsNot(first["panels"], second["panels"])
        self.assertIsNot(first["filters"], second["filters"])
        self.assertIsNot(first["panels"], self.defaults["panels"])
        self.assertIsNot(first["filters"], self.defaults["filters"])

    def test_editing_default_result_leaves_defaults_and_later_results_unchanged(self):
        first = self.prepare()
        first["panels"].append("custom")
        first["filters"]["archived"] = True
        first["layout"] = "wide"
        self.assertEqual(self.defaults, self.original_defaults)
        self.assertEqual(
            self.prepare(),
            {
                "layout": "compact",
                "panels": ["summary", "help"],
                "filters": {"archived": False},
            },
        )

    def test_editing_custom_result_leaves_input_and_other_results_unchanged(self):
        overrides = {
            "layout": "wide",
            "panels": ["chart"],
            "filters": {"archived": False, "starred": True},
        }
        before = deepcopy(overrides)
        first = self.prepare(overrides)
        second = self.prepare(overrides)
        first["panels"].append("custom")
        first["filters"]["starred"] = False
        first["layout"] = "compact"
        self.assertEqual(overrides, before)
        expected = {
            "layout": "wide",
            "panels": ["chart", "help"],
            "filters": {"archived": False, "starred": True},
        }
        self.assertEqual(second, expected)
        self.assertEqual(self.prepare(overrides), expected)
        self.assertEqual(self.defaults, self.original_defaults)


if __name__ == "__main__":
    unittest.main()
```

## Repeatable verification

From the repository root, run this block with Python. It copies only the fictional source into a temporary directory. Expected failures in the original are part of the check; a repaired failure makes verification fail. The final input matrix is derived separately from the stated contract and checks repeated calls, order, empty values, type-sensitive false/zero values and nested mutation isolation.

```python
from pathlib import Path
from copy import deepcopy
import itertools
import json
import re
import runpy
import subprocess
import sys
import tempfile

page = Path("skill/failing-build-repair/REHEARSAL.md").read_text()
blocks = re.findall(r"```python\n(.*?)\n```", page, re.S)
assert len(blocks) == 4, "Expected original, repaired, tests and verifier blocks"
before, after, tests = blocks[:3]
with tempfile.TemporaryDirectory(prefix="preference-fixture-") as folder:
    work = Path(folder)
    (work / "test_preferences.py").write_text(tests + "\n")
    (work / "preferences.py").write_text(before + "\n")
    baseline = subprocess.run([sys.executable, "-m", "unittest", "-q"],
                              cwd=work, capture_output=True, text=True)
    assert baseline.returncode == 1
    assert "Ran 12 tests" in baseline.stderr and "failures=10" in baseline.stderr
    (work / "preferences.py").write_text(after + "\n")
    repaired = subprocess.run([sys.executable, "-m", "unittest", "-q"],
                              cwd=work, capture_output=True, text=True)
    assert repaired.returncode == 0 and "Ran 12 tests" in repaired.stderr
    namespace = runpy.run_path(str(work / "preferences.py"))
    prepare = namespace["prepare_preferences"]
    defaults = deepcopy(namespace["DEFAULT_PREFERENCES"])
    absent = object()
    layouts = [absent, "", "wide"]
    panels = [absent, [], ["summary"], ["help"], ["help", "chart"],
              ["chart", "help", "details"], ["chart"]]
    filters = [absent, {}, {"archived": False}, {"archived": True},
               {"archived": False, "count": 0}]
    requests = [None] + [
        {key: deepcopy(value) for key, value in
         zip(("layout", "panels", "filters"), values) if value is not absent}
        for values in itertools.product(layouts, panels, filters)
    ]
    assert len(requests) == 106
    for request in requests:
        original = deepcopy(request)
        expected = deepcopy(defaults)
        if request is not None:
            expected.update(deepcopy(request))
        if "help" not in expected["panels"]:
            expected["panels"].append("help")
        first, second = prepare(request), prepare(request)
        # JSON distinguishes false from zero as well as preserving values and order.
        assert json.dumps(first, sort_keys=True) == json.dumps(expected, sort_keys=True)
        assert json.dumps(second, sort_keys=True) == json.dumps(expected, sort_keys=True)
        assert first is not second
        assert first["panels"] is not second["panels"]
        assert first["filters"] is not second["filters"]
        first["panels"].append("scratch")
        first["filters"]["scratch"] = True
        first["layout"] = "changed"
        assert request == original and namespace["DEFAULT_PREFERENCES"] == defaults
        assert json.dumps(prepare(request), sort_keys=True) == json.dumps(expected, sort_keys=True)
print("PASS: expected baseline failures, repaired regression suite and independent input matrix")
```

## What was verified

On 2026-10-01 with Python 3.12.14:

- The reported default-list and caller-list mutations were reproduced
- Before repair, 12 test methods ran: four passed and eight contained failures; the runner counted ten failures because one method had three failing subtests
- After repair, the identical 12 methods passed; discovery found the same suite, and both files compiled
- Independent checks passed for 106 permitted combinations, including an omitted override, explicit empty structures, existing `help` positions, false/zero values and later mutation of a returned object
- The exact verifier above was rerun successfully, and the original source input remained unchanged

These results establish the documented synthetic fixture behavior. They do not establish remote CI, a deployed fix, performance under large inputs or compatibility with types outside this contract. No publishing, account access, installation or production change occurred as part of the rehearsal.

[Return to the skill](SKILL.md)
