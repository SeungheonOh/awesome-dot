"""Check this fictional worked example only; never import or run its packages."""
import json
from pathlib import Path
import re

text = Path(__file__).with_name("worked-example.md").read_text(encoding="utf-8")
manifest, lock, target = [
    json.loads(block) for block in re.findall(r"```json\n(.*?)\n```", text, re.S)
]
records = lock["packages"]
root = records["node_modules/@demo/rowcsv"]
audit = records["node_modules/@demo/audit-csv"]
nested = records["node_modules/@demo/audit-csv/node_modules/@demo/rowcsv"]
assert manifest["dependencies"] == records[""]["dependencies"]
assert lock["lockfileVersion"] == 3
assert manifest["dependencies"]["@demo/rowcsv"] == "~2.4.0"
assert root["version"] == "2.4.1"
assert audit["version"] == manifest["dependencies"]["@demo/audit-csv"] == "1.6.0"
assert audit["dependencies"]["@demo/rowcsv"] == "~2.3.0"
assert nested["version"] == "2.3.2"
assert target["version"] == "3.2.0"
assert target["dependencies"]["@demo/byte-text"] == "^2.1.0"
assert all(target[key] == {} for key in ("scripts", "peerDependencies", "optionalDependencies"))

# Deliberately only the stable three-part versions/ranges supplied in this fixture.
def version(value):
    assert re.fullmatch(r"\d+\.\d+\.\d+", value), value
    return tuple(map(int, value.split(".")))

def within(value, low, high):
    return version(low) <= version(value) < version(high)

assert within(root["version"], "2.4.0", "2.5.0")
assert within(nested["version"], "2.3.0", "2.4.0")
assert not within(target["version"], "2.3.0", "2.4.0")
assert root["dependencies"]["@demo/byte-text"] == "^1.4.0"
assert nested["dependencies"]["@demo/byte-text"] == "~1.3.0"
assert records["node_modules/@demo/byte-text"]["version"] == "1.4.3"
assert within(records["node_modules/@demo/byte-text"]["version"], "1.4.0", "2.0.0")
assert records["node_modules/@demo/audit-csv/node_modules/@demo/byte-text"]["version"] == "1.3.5"
assert within(records["node_modules/@demo/audit-csv/node_modules/@demo/byte-text"]["version"], "1.3.0", "1.4.0")
assert manifest["engines"]["node"] == ">=18.17.0 <23.0.0"
assert target["engines"]["node"] == ">=20.9.0 <23.0.0"
for runtime, target_ok in (("20.11.1", True), ("18.19.0", False), ("22.4.1", True)):
    assert within(runtime, "18.17.0", "23.0.0")
    assert within(runtime, "20.9.0", "23.0.0") == target_ok
    assert f"Node {runtime}" in text


# Even if R2 were removed, R42's advertised range would still conflict.
# This checks the supplied simple intervals, not an invented candidate policy.
current_bounds = re.fullmatch(r">=(\d+\.\d+\.\d+) <(\d+\.\d+\.\d+)", manifest["engines"]["node"])
target_bounds = re.fullmatch(r">=(\d+\.\d+\.\d+) <(\d+\.\d+\.\d+)", target["engines"]["node"])
assert current_bounds and target_bounds
assert version(current_bounds[1]) < version(target_bounds[1])
assert current_bounds[2] == target_bounds[2]
g1 = text.split("#### G1 support reconciliation\n", 1)[1].split("### Change-to-usage", 1)[0]
for required in ("owner-approved", "candidate `engines.node`", "CI and support documentation",
                 "candidate range remains UNKNOWN", "advertised range is a subset",
                 "every approved deployment/CI runtime", "both ranges",
                 "R42 recovery artifacts unchanged", "G1 remains open until both checkpoints pass"):
    assert required in g1, required
steps = {re.match(r"\| ([1-7])\.", line)[1]: line for line in text.splitlines()
         if re.match(r"\| [1-7]\.", line)}
assert "G1 decision checkpoint" in steps["1"] and "owner-approved" in steps["1"]
assert "G1 decision checkpoint passed" in steps["2"]
assert "G1 readback checkpoint" in steps["3"] and "preserved R42 metadata" in steps["3"]
assert "G1 closed" in steps["4"]
assert "recheck G1" in steps["6"] and "actual environments and advertised range" in steps["6"]
for step in ("1", "3", "6"):
    assert all(term in steps[step] for term in ("engines.node", "CI", "support documentation")), step


# Recovery must carry the approved support state even when runtimes do not change.
e4 = text.split("### [E4] Supported environments and existing recovery artifacts\n", 1)[1].split("### [S0]", 1)[0]
assert "ledger-R42-support.tar" in e4 and "matching CI configuration and versioned support documentation" in e4
assert "Such a set has not been created" in e4
assert "support-only change" in steps["2"] and "unchanged-runtime R1/R3" in steps["2"]
assert "Retain direct `rowcsv` `2.4.1`" in steps["2"]
assert "approved baseline's `engines.node`" in steps["3"]
for step in ("2", "7"):
    assert "pre-dependency" in steps[step] and "CI and support documentation" in steps[step]
for required in ("dependency rollback", "manifest/engines", "full lockfile", "runtime image",
                 "Preserve the approved support/runtime decision", "unchanged-runtime R1/R3",
                 "separate reversal authorization", "support-consistency checks"):
    assert required in steps["7"], required
assert "For unchanged R1/R3 this is the R42 set" not in text
assert "A dependency rollback does not by itself authorize undoing the separate runtime/support decision" in text

matrix = {parts[1].strip(): parts for line in text.splitlines()
          if re.match(r"\| M\d+ \|", line) for parts in [line.split("|")]}
fixtures = {re.match(r"\| (F\d+) \|", line)[1] for line in text.splitlines()
            if re.match(r"\| F\d+ \|", line)}
assert set(matrix) == {f"M{i}" for i in range(1, 9)}
assert fixtures == {f"F{i}" for i in range(1, 7)}
expected = {
    "M1": ("S30", "E1", "U1", "G1", "engines.node", "CI", "support documentation"), "M2": ("S25", "U1", "F4"),
    "M3": ("S30", "U1", "F1"), "M4": ("S30", "U1", "F2", "F6"),
    "M5": ("S31", "U1", "F3"), "M6": ("S32", "U3", "F5", "G2"),
    "M7": ("S32", "U1", "G2"), "M8": ("S0", "S32", "G2"),
}
for key, references in expected.items():
    row = "|".join(matrix[key])
    assert all(reference in row for reference in references), key
    assert len(matrix[key]) == 7, key  # Five populated Markdown columns.
    assert all(cell.strip() for cell in matrix[key][1:-1]), key
for source, release in (("S25", "2.5.0"), ("S30", "3.0.0"), ("S31", "3.1.0"), ("S32", "3.2.0")):
    assert f"### [{source}] Version {release}, released " in text
    assert any(source in "|".join(row) for row in matrix.values())
assert "No target lockfile exists" in text
assert "remain UNRUN" in text
print("PASS: fictional version/range/runtime facts, support-metadata/recovery gates, and source/matrix/fixture coverage")
print("UNRUN: package installation, resolution, compatibility, builds, deployment and recovery")
