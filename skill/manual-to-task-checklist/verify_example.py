"""Check this fixed example's structure, not the safety of arbitrary manuals.

Run with Python 3 from any directory. Reads adjacent files; writes nothing.
The semantic source-to-step review is recorded in WORKED-EXAMPLE.md.
"""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
SOURCE = (ROOT / "example-source.md").read_text(encoding="utf-8")
EXAMPLE = (ROOT / "WORKED-EXAMPLE.md").read_text(encoding="utf-8")


def require(condition, message):
    if not condition:
        raise SystemExit(f"FAIL {message}")


for path in ROOT.glob("*.md"):
    text = path.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        require("://" not in target, f"unexpected external target: {target}")
        name, _, anchor = target.partition("#")
        linked = path.parent / name if name else path
        require(linked.is_file(), f"missing local link: {path.name} → {target}")
        if anchor:
            # These fixtures deliberately use simple M01/Q01 headings.
            headings = re.findall(r"^#{1,6} ([A-Za-z0-9]+)$",
                                  linked.read_text(encoding="utf-8"), re.M)
            require(anchor in {h.lower() for h in headings}, f"missing anchor: {target}")
print("PASS local links and anchors")

clauses = re.findall(r"^### (M\d{2})$", SOURCE, re.M)
coverage_rows = re.findall(r"^\| (M\d{2}) \| ([^|]+) \|", EXAMPLE, re.M)
coverage = [clause for clause, _ in coverage_rows]
require(len(clauses) == len(set(clauses)), "duplicate source clause")
require(len(coverage) == len(set(coverage)), "duplicate coverage row")
require(set(clauses) == set(coverage), "coverage must account for every D1 clause")
expected_locations = {
    "M01": "Applicability", "M02": "P1", "M03": "P2", "M04": "C1, C2",
    "M05": "C2", "M06": "C3, C4", "M07": "C5", "M08": "C6",
    "M09": "C7, Done when", "M10": "C8, Done when", "M11": "C7, C8, Gap",
}
require({clause: location.strip() for clause, location in coverage_rows} == expected_locations,
        "coverage location differs from the reviewed mapping")

expected = {
    "P1": {"M02"}, "P2": {"M03"}, "C1": {"M04"}, "C2": {"M05"},
    "C3": {"M06"}, "C4": {"M06"}, "C5": {"M07"}, "C6": {"M08"},
    "C7": {"M09", "M11"}, "C8": {"M10", "M11"},
}
steps = re.findall(r"^- \[ \] \*\*([A-Za-z][A-Za-z0-9_-]*) — (.+)$", EXAMPLE, re.M)
require(len(re.findall(r"^- \[ \] ", EXAMPLE, re.M)) == len(steps),
        "unrecognized checklist line")
require(len(steps) == len(expected), "unexpected or missing checklist step")
require(len({label for label, _ in steps}) == len(steps), "duplicate checklist step")
for label, line in steps:
    require(label in expected, f"unexpected step {label}")
    links = set(re.findall(r"\[(M\d{2})\]\(example-source\.md#m\d{2}\)", line))
    require(links == expected[label], f"source links differ for {label}")
for label, anchor in re.findall(r"\[(M\d{2}|Q01)\]\(example-source\.md#([mq]\d{2})\)", EXAMPLE):
    require(label.lower() == anchor, f"link label/target mismatch: {label}")
print("PASS D1 coverage and checklist source links")

require([label for label, _ in steps] == list(expected), "checklist order changed")
require("- [x]" not in EXAMPLE.lower(), "prepared task marked completed")
lines = dict(steps)
require("Do not press Feed" in lines["C1"], "opening warning absent")
require("before C7" in lines["C6"], "size gate absent")
require("Continue to C8 only if" in lines["C7"], "Feed outcome gate absent")
for label in ("C7", "C8"):
    require("Otherwise stop" in lines[label] and "page 12" in lines[label],
            f"failure stop or missing-page dependency absent at {label}")
print("PASS checklist order and unchecked status")

for phrase in ("Device label says L20 Plus", "firmware reported as “2.x”",
               "Size already 40 × 25 mm", "Label does not reach tear line",
               "Sample border is clipped", "D2 is added to the source set"):
    require(phrase in EXAMPLE, f"boundary case missing: {phrase}")
require("no explicit supersession" in EXAMPLE, "conflict basis absent")
print("PASS boundary-case coverage")
