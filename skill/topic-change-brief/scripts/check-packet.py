#!/usr/bin/env python3
"""Offline invariants for the fictional packet; no retrieval or event matching."""
import json
import re
from copy import deepcopy
from datetime import date, datetime
from pathlib import Path

packet_path = Path(__file__).resolve().parents[1] / "references" / "fictional-source-packet.md"
blocks = re.findall(r"```json\n(.*?)\n```", packet_path.read_text(), flags=re.S)
assert len(blocks) == 1, "Expected the single supplied packet"
p = json.loads(blocks[0])
assert p["fictional"] is True


def instant(value):
    result = datetime.fromisoformat(value)
    assert result.tzinfo is not None, "Unknown timezone cannot be treated as UTC"
    return result


prior, cutoff = instant(p["prior_cutoff"]), instant(p["cutoff"])
assert prior < cutoff < instant(p["packet_assembled_at"])
sources = {s["id"]: s for s in p["sources"]}
assert len(sources) == len(p["sources"]), "Source IDs must be unique"


def eligible(source, boundary=cutoff):
    return (source["access"] == "read"
            and source["available_at"] is not None
            and instant(source["available_at"]) <= boundary)


def locator(reference):
    source_id, section = reference.split("#", 1)
    source = sources[source_id]
    assert source["access"] == "read", "Failed reads cannot support claims"
    assert source["passages"].get(section), "Missing source passage"
    return source


def origin_roots(source_id, path=()):
    assert source_id not in path, "Cyclic derivative chain"
    source = sources[source_id]
    parents = source["derived_from"]
    if not parents:
        return {source_id}
    return set().union(*(origin_roots(parent, path + (source_id,)) for parent in parents))


for s in sources.values():
    instant(s["retrieved_at"])
    for parent in s["cites"] + s["derived_from"]:
        assert parent in sources and parent != s["id"]
    origin_roots(s["id"])
    if s["access"] == "read":
        assert s["version"] and s["passages"] and s["coverage"]
        assert instant(s["published_at"]) <= instant(s["available_at"]) <= instant(s["retrieved_at"])
        if s["updated_at"]:
            assert instant(s["published_at"]) <= instant(s["updated_at"]) <= instant(s["available_at"])
        for event_date in s["events"].values():
            date.fromisoformat(event_date)  # Retain day precision; do not assign midnight.
    else:
        assert not s["passages"] and not s["events"]

baseline = {b["id"]: b for b in p["baseline"]["statements"]}
for statement in baseline.values():
    for ref in statement["supports"]:
        assert eligible(locator(ref), prior), "Baseline cites later evidence"
for change in p["editorial_assignments"]:
    assert change["status"] in {"unchanged", "confirmation", "new", "correction", "withdrawal"}
    assert change["reason"] and all(b in baseline for b in change["baseline"])
    support = [locator(ref) for ref in change["supports"]]
    assert all(eligible(s) for s in support), "Brief cites failed or out-of-cutoff evidence"
    assert any(change["event"] in s["events"] for s in support)
print("PASS: baseline and comparison locators resolve to eligible retained passages")

assert origin_roots("R1") == origin_roots("G0") == {"G0"}
assert origin_roots("D1") == origin_roots("P1") == {"P1"}
assert origin_roots("N1") == {"N1"}, "Citing the old plan does not make a new decision derivative"
assert sources["R1"]["events"] == sources["G0"]["events"]
assert sources["D1"]["events"] == sources["P1"]["events"]
print("PASS: explicit recap/copy provenance stays with the original events")

old, corrected = sources["P1"], sources["P2"]
assert old["url"] == corrected["url"] and old["version"] != corrected["version"]
assert corrected["supersedes"] == old["id"]
assert old["passages"]["staffing"] != corrected["passages"]["staffing"]
assert instant(corrected["published_at"]) <= prior < instant(corrected["updated_at"]) <= cutoff
assert corrected["events"]["pilot-decision"] == old["events"]["pilot-decision"]
print("PASS: same-URL staffing correction retains both versions and the original event date")

newly_available = {s["id"] for s in sources.values()
                   if eligible(s) and prior < instant(s["available_at"])}
assert newly_available == {"R1", "D1", "N1", "P2"}
assert date.fromisoformat(sources["R1"]["events"]["grant-decision"]) < prior.date()
assert not eligible(sources["L1"]), "Later withdrawal must not enter earlier brief"
assert eligible(sources["L1"], instant("2026-09-29T10:00:00+00:00"))
assert eligible(dict(corrected, available_at="2026-09-28T14:00:00+02:00"))
assert not eligible(dict(corrected, available_at="2026-09-28T12:00:01+00:00"))
assert not eligible(sources["X1"]), "Failed register read must not become no change"
late_capture = deepcopy(corrected)
late_capture["retrieved_at"] = "2026-09-30T10:00:00+00:00"
assert eligible(late_capture), "Retrieval date is distinct from evidenced availability"
unknown_version_date = deepcopy(late_capture)
unknown_version_date["available_at"] = None
assert not eligible(unknown_version_date), "Unknown historical availability is not eligible"
assert not eligible(dict(corrected, access="failed")), "A timestamp cannot rescue failed access"
print("PASS: publication/update/event/retrieval boundaries preserve gaps and exclude later evidence")

shift = date.fromisoformat(sources["N1"]["planned_start"]) - date.fromisoformat(old["planned_start"])
assert shift.days == 7
assert sources["N1"]["planned_end"] == old["planned_end"]
assert date.fromisoformat(sources["N1"]["events"]["schedule-change"]) < date.fromisoformat(sources["N1"]["planned_start"])
print("PASS: planned first evening moves seven calendar days; planned end is unchanged")

# These are checks of the declared editorial assignments, not inferred labels.
changes = {c["id"]: c for c in p["editorial_assignments"]}
assert changes["C2"]["status"] == "unchanged"
assert changes["C4"]["status"] == "confirmation"
assert "N1#retained" in changes["C4"]["supports"]
assert {c["event"] for c in changes.values() if c["status"] in {"new", "correction", "withdrawal"}} == {"schedule-change", "staffing-correction"}
print("PASS: annotated derivative coverage adds no development; amendment and correction remain separate")
print("LIMIT: event identities and semantic labels were supplied and reviewed, not automatically established")
