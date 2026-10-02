"""Bounded checks of the fictional packet; no physical verification or network."""
import json
from pathlib import Path

data = json.loads(Path(__file__).with_name("example-data.json").read_text())
sources = data["sources"]
items = {row["id"]: row for row in data["items"]}
reports = {row["id"]: row for row in data["reported_observations"]}
boxes = data["boxes"]
assert len(items) == len(data["items"])
assert len(reports) == len(data["reported_observations"])
assert set(data["imports"]) == set(sources)  # Coverage, despite a repeated import.

def source_exists(locator):
    assert locator.split(":")[0] in sources, locator

for item in items.values():
    source_exists(item["source"])
for report in reports.values():
    source_exists(report["source"])
    assert report["item"] in items
    assert set(report["locations"]) <= set(boxes)
    assert all(type(n) is int and n > 0 for n in report["locations"].values())
    if "superseded_by" in report:
        replacement = reports[report["superseded_by"]]
        assert replacement["corrects"] == report["id"]
        assert replacement["item"] == report["item"]

def replay(import_ids):
    current = {item_id: {} for item_id in items}
    for report_id in dict.fromkeys(import_ids):  # Same stable ID contributes once.
        report = reports[report_id]
        if "superseded_by" in report:
            assert report["superseded_by"] in import_ids
            continue
        assert not current[report["item"]], "Fixture has overlapping current reports"
        current[report["item"]] = report["locations"].copy()
    return current

current = replay(data["report_imports"])
assert current == data["expected_current"]
assert replay(data["report_imports"] * 2) == current
for item_id, item in items.items():
    quantities = [item["scope"], item["reserve"], item["outside"], *item["plan"].values()]
    assert all(type(n) is int and n >= 0 for n in quantities)
    assert set(item["plan"]) <= set(boxes)
    planned = sum(item["plan"].values())
    packed = sum(current[item_id].values())
    assert planned + item["reserve"] == item["scope"]
    assert packed + item["outside"] == item["scope"]
    assert planned - packed == data["expected_plan_gap"][item_id]
    assert item["verified"] is None  # Never promote a reported count.

resolution = data["identity_resolutions"][0]
source_exists(resolution["source"])
source_exists(resolution["claim"])
assert resolution["item"] == "I03" and items["I03"]["scope"] == 1
unknown = data["unresolved"][0]
source_exists(unknown["source"])
assert all(unknown[key] is None for key in ("item", "quantity", "box"))
assert items["I05"]["contents"] == "unlisted"
assert current["I01"] == {"B01": 2, "B02": 2} and "B01" not in current["I02"]
print("PASS: source coverage, repeat imports, corrected split, quantities, reservations and unknowns")
print("LIMIT: fictional fixture only; physical contents and verification remain unestablished")
