# Reproduce the normalized-contract checks

[example.md](example.md) supplies two fictional normalized extracts, consumer rules and five distinguishing fixtures. The code below reads those exact blocks and evaluates only their stated predicates. It is not an OpenAPI or JSON Schema validator, a server implementation, or a test of a real consumer.

The request and response directions remain separate. An allowed response does not repair C1's missing request region. The old extract does not say whether unknown query fields are allowed, so the old-provider result for F02 remains **unknown**, rather than being guessed from the new provider's behavior.

## Executable check

Run this block from this skill folder with Python 3. It reads one local Markdown file, uses the standard library, changes only in-memory copies and makes no endpoint calls.

```python
import json
import re
from copy import deepcopy
from pathlib import Path

text = Path("example.md").read_text()
contracts, fixtures = [json.loads(s) for s in re.findall(r"```json\n(.*?)\n```", text, re.S)]

# These return only the selected predicates' result: pass, fail or unknown.
# Unsupported input shapes remain unknown instead of pretending to validate them.
def request_result(spec, query):
    if not isinstance(query, dict):
        return "unknown"
    rules = spec["request"]
    if not set(rules["required_query"]) <= query.keys():
        return "fail"
    known = {"limit"}
    if "region_enum" in rules:
        known.add("region")
        if "region" in query and query["region"] not in rules["region_enum"]:
            return "fail"
    if "limit" in query:
        value, constraint = query["limit"], rules["limit"]
        if (type(value) is not int or not constraint["minimum"] <= value <= constraint["maximum"]):
            return "fail"
    return "unknown" if query.keys() - known else "pass"


def response_result(spec, payload):
    if not isinstance(payload, dict):
        return "unknown"
    rules = spec["response_200"]
    if not set(rules["required_fields"]) <= payload.keys():
        return "fail"
    if not isinstance(payload.get("items"), list):
        return "unknown"  # This bounded extract is not a full items schema.
    for item in payload["items"]:
        if not isinstance(item, dict) or "status" not in item:
            return "unknown"  # Item requiredness/other shapes were not supplied.
        if item["status"] not in rules["item_status_enum"]:
            return "fail"
    if "next_cursor" in payload:
        cursor = payload["next_cursor"]
        if cursor is None:
            if not rules["next_cursor"]["nullable"]:
                return "fail"
        elif not isinstance(cursor, str):
            return "fail"
    # Unknown response-property policy is not specified by these extracts.
    if payload.keys() - {"items", "next_cursor"}:
        return "unknown"
    return "pass"


def consumer_result(consumer, payload):
    if not isinstance(payload, dict):
        return "unknown"
    if consumer["requires_next_cursor_property"] and "next_cursor" not in payload:
        return "fail"
    if not isinstance(payload.get("items"), list):
        return "unknown"
    for item in payload["items"]:
        if not isinstance(item, dict) or "status" not in item:
            return "unknown"
        if item["status"] not in consumer["accepted_statuses"]:
            return "fail"
    if payload.keys() - {"items", "next_cursor"} and not consumer["ignores_unknown_response_fields"]:
        return "unknown"  # No unspecified decoder behavior is invented.
    return "pass"


def verify(source, cases):
    old, new, client = source["old"], source["new"], source["consumer_C1"]
    assert old["operation"] == new["operation"] == "GET /deliveries"
    seen = set()
    for fixture in cases["request_fixtures"]:
        assert fixture["id"] not in seen
        seen.add(fixture["id"])
        for version, spec in (("old", old), ("new", new)):
            expected_key = version + "_accepts"
            result = request_result(spec, fixture["query"])
            if expected_key in fixture:
                assert result == ("pass" if fixture[expected_key] else "fail"), (fixture["id"], version, result)
        if "new_default_limit" in fixture:
            assert "limit" not in fixture["query"]
            assert fixture["new_default_limit"] == new["request"]["limit"]["documented_server_default"]
    for fixture in cases["response_fixtures"]:
        assert fixture["id"] not in seen
        seen.add(fixture["id"])
        for version, spec in (("old", old), ("new", new)):
            assert response_result(spec, fixture["payload"]) == (
                "pass" if fixture[version + "_shape_accepts"] else "fail"), (fixture["id"], version)
        assert consumer_result(client, fixture["payload"]) == (
            "pass" if fixture["old_C1_accepts"] else "fail"), fixture["id"]
    assert seen == {f"F{i:02d}" for i in range(1, 6)}
    for fixture in cases["request_fixtures"] + cases["response_fixtures"]:
        assert fixture["change_ids"] and set(fixture["change_ids"]) <= {"C01", "C02", "C03", "C04"}
    return old, new, client

old, new, client = verify(contracts, fixtures)
assert request_result(old, None) == response_result(old, None) == consumer_result(client, None) == "unknown"
assert request_result(old, {"region": "eu"}) == "unknown"
assert request_result(new, {"region": None}) == "fail"
assert request_result(new, {"region": ""}) == "fail"
assert request_result(new, {"region": "eu", "limit": True}) == "fail"
assert request_result(new, {"region": "eu", "limit": 1}) == "pass"
assert request_result(new, {"region": "eu", "limit": 100}) == "pass"
assert request_result(new, {"region": "eu", "limit": 0}) == "fail"
assert request_result(new, {"region": "eu", "limit": 101}) == "fail"

# A present empty string is not the old consumer's explicit-null termination signal.
empty_cursor = {"items": [], "next_cursor": ""}
assert response_result(old, empty_cursor) == response_result(new, empty_cursor) == "pass"
assert consumer_result(client, empty_cursor) == "pass"
assert client["terminates_when_next_cursor_is_null"] and empty_cursor["next_cursor"] is not None
assert client["requires_page_size_50"] is False  # C04 does not establish its own C1 break.
assert old["request"]["limit"]["documented_server_default"] == 50
assert new["request"]["limit"]["documented_server_default"] == 25

# Each mutation creates a false published conclusion or contradicts its source.
mutations = [
    lambda c, f: c["new"]["request"].update(required_query=[]),
    lambda c, f: c["new"]["response_200"].update(item_status_enum=["ready", "sent"]),
    lambda c, f: c["old"]["response_200"].update(required_fields=["items"]),
    lambda c, f: f["response_fixtures"][2].update(payload={"items": []}),
    lambda c, f: f["request_fixtures"][1].update(old_accepts=True),
    lambda c, f: f["response_fixtures"][0].update(old_C1_accepts=True),
]
for mutate in mutations:
    changed_contracts, changed_fixtures = deepcopy(contracts), deepcopy(fixtures)
    mutate(changed_contracts, changed_fixtures)
    try:
        verify(changed_contracts, changed_fixtures)
    except AssertionError:
        pass
    else:
        raise AssertionError("A source/fixture contradiction was accepted")
print("PASS: 5 normalized fixtures; directional request/response/client predicates;")
print("      omitted/null/empty cursor distinction; unknown old-query behavior;")
print("      request bounds and 6 source/fixture corruptions rejected")
```

Convenience command from this folder:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('verification.md').read_text()
code = text.split('```python\n', 1)[1].split('\n```', 1)[0]
exec(compile(code, 'api-contract-example-check', 'exec'))
PY
```

Observed locally on 2026-10-01 with Python 3.12.14: the exact block passed. It verifies these bounded normalized predicates and expected fixture flags, including the six negative controls. It does not validate a complete API schema, execute an actual client, establish server defaults at runtime, or demonstrate a successful migration. The source-to-change explanations and proposed migration decisions also require reading the supplied evidence; a passing fixture checker cannot choose a region or approve a release.
