# Decisions That Matter in a Real Handoff

These cases help decide whether the proposed package is ready for its stated recipient and use.

| Situation | Appropriate outcome |
| --- | --- |
| Two selected case-distinct filenames contain different material | Keep both; use the approved distinct destination names and repair the known references in copies |
| A destination rename rule was already explicitly approved | Apply it and its approved exact reference changes without another approval loop |
| The user asked for byte-identical files, but a necessary rename breaks links | Show the exact conflict; do not silently edit text or promise a usable unchanged project |
| A selected guide links to an excluded required keyboard shortcut reference | Hold package completion for that dependency decision; do not silently include it or delete the link |
| An approved rename produces another destination collision | Hold the affected map; never overwrite or choose one source as the winner |
| A link resolves, but to the wrong one of two guides | Fail logical-target preservation even though existence and file count pass |
| Source text changed after the map was reviewed | Refresh that source's evidence and affected references; do not apply stale replacements |
| A source-code import or native application reference is not understood | Hold its transformation or use an established supported package workflow; filename screening is insufficient |
| The package fits the transfer limit only after dropping an essential file | Return the size result and decision; do not make the package look complete by shrinking scope |
| Only Linux extraction was performed for a Windows recipient | Report actual Linux readback and name screening separately; leave Windows use untested |
| The user asks only to prepare a package for a person | Produce the package locally; actual delivery still needs audience/data/destination authority |
| A preparation or extraction destination already exists | Leave it untouched and use an authorized new destination or request the needed choice |

## Executable checks in this example

The small reproducer checks actual source-to-copy-to-archive-to-extraction bytes, explicit selection, reference targets and input preservation. The checks below use only in-memory copies of the supplied fictional source and plan; they do not write package outputs or execute project content.

Run from this skill folder after inspecting the helper:

```sh
python3 -B - <<'PY'
import copy
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location("handoff_example", "scripts/reproduce.py")
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
bundle = json.loads(Path("fixtures/source-bundle.json").read_text())
plan = json.loads(Path("fixtures/reviewed-map.json").read_text())

def rejected(label, changed_bundle, changed_plan, expected):
    try:
        helper.build_payload(changed_bundle, changed_plan)
    except ValueError as error:
        assert expected in str(error), (label, str(error))
        print("PASS:", label)
    else:
        raise AssertionError("Unexpected acceptance: " + label)

changed = copy.deepcopy(plan)
changed["rows"][2]["destination"] = "docs/SETUP-GUIDE.md"
rejected("case-colliding destination is held", bundle, changed, "naming screen failed")

changed_bundle, changed_plan = copy.deepcopy(bundle), copy.deepcopy(plan)
for row in changed_bundle["files"]:
    if row["path"] == "reference/Keyboard shortcuts.txt":
        row["selected"] = False
        row["reason"] = "Benign check: incorrectly excluded required keyboard shortcut reference"
changed_plan["rows"] = [r for r in changed_plan["rows"] if r["source"] != "reference/Keyboard shortcuts.txt"]
rejected("required excluded dependency is held", changed_bundle, changed_plan, "Missing selected dependency")

changed = copy.deepcopy(plan)
changed["rows"][0]["replacements"][0]["new"] = "(docs/troubleshooting-guide.md)"
rejected("existing but wrong guide is held", bundle, changed, "logical target")

changed = copy.deepcopy(plan)
changed["rows"][0]["replacements"][0]["new"] = "(docs/troubleshooting-guide.md)"
changed["rows"][0]["replacements"][1]["new"] = "(docs/setup-guide.md)"
rejected("swapped guide targets retain no false pass", bundle, changed, "logical target")

changed = copy.deepcopy(plan)
changed["generated_members"] = []
rejected("undeclared support members are held", bundle, changed, "exact two declared support members")

changed = copy.deepcopy(bundle)
changed["files"][0]["text"] += "\n[Another setup link](docs/Guide.md)\n"
rejected("stale reference occurrence count is held", changed, plan, "occurrence changed")

files, manifest, issues = helper.build_payload(bundle, plan)
assert len(files) == 9 and len(manifest["relative_links"]) == 12
assert files["assets/Interface Colors.txt"] == bundle["files"][4]["text"].encode("utf-8")
assert len(issues) == 2
print("PASS: original fixture remains valid; spaces and unchanged bytes survive")
PY
```

An existing-output check is separate from these in-memory checks: rerunning the reproducer against its existing destination must fail before writing there. Compare that directory's file hashes before and after the attempted rerun. Do not delete a real user's directory to make this test pass.
