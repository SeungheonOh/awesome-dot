# Worked example: delivery-list contract v1 to v2

These fictional normalized contract extracts are small enough to compare directly. They are not executable OpenAPI files. The scope is `GET /deliveries`, the consumer is C1, and the supported rollout requires old C1 to work with the new provider. New-client/old-provider compatibility is outside the supplied rollout requirement.

## Contract and consumer inputs

```json
{
  "old": {
    "version": "v1",
    "operation": "GET /deliveries",
    "request": {
      "required_query": [],
      "limit": {"type": "integer", "minimum": 1, "maximum": 100, "documented_server_default": 50}
    },
    "response_200": {
      "required_fields": ["items", "next_cursor"],
      "item_status_enum": ["ready", "sent"],
      "next_cursor": {"type": "string", "nullable": true},
      "final_page_rule": "next_cursor is explicitly null"
    }
  },
  "new": {
    "version": "v2",
    "operation": "GET /deliveries",
    "request": {
      "required_query": ["region"],
      "region_enum": ["eu", "us"],
      "limit": {"type": "integer", "minimum": 1, "maximum": 100, "documented_server_default": 25}
    },
    "response_200": {
      "required_fields": ["items"],
      "item_status_enum": ["ready", "sent", "paused"],
      "next_cursor": {"type": "string", "nullable": false},
      "final_page_rule": "next_cursor is omitted"
    }
  },
  "consumer_C1": {
    "request_query": {},
    "accepted_statuses": ["ready", "sent"],
    "requires_next_cursor_property": true,
    "terminates_when_next_cursor_is_null": true,
    "requires_page_size_50": false,
    "ignores_unknown_response_fields": true,
    "documented_region_selection_rule": null
  }
}
```

## Expected change ledger

| ID | Change and exact source paths | Direction | Expected finding |
| --- | --- | --- | --- |
| C01 | `old.request.required_query` to `new.request.required_query` | Old request to new provider | Incompatible: C1 omits the now-required region |
| C02 | `old.response_200.item_status_enum` to `new.response_200.item_status_enum` | New response to old C1 | Incompatible when `paused` occurs: C1's accepted set excludes it |
| C03 | `old.response_200.required_fields`, `next_cursor` and `final_page_rule` to their new counterparts | New response to old C1 | Incompatible at the final page: C1 requires the property and recognizes explicit null |
| C04 | `old.request.limit.documented_server_default` to `new.request.limit.documented_server_default` | Request behavior after C01 is addressed | Behavior changes from 50 to 25 items by default; no independent C1 page-size failure is established because C1 has no fixed-size requirement |

Do not invent a default region as a fix for C01. The product owner must define which region C1 should request. C04 still matters for request volume and other consumers, but these inputs do not establish those consumers' behavior or an observed performance impact.

## Distinguishing fixtures and expected outcomes

```json
{
  "request_fixtures": [
    {"id": "F01", "query": {}, "old_accepts": true, "new_accepts": false, "change_ids": ["C01"]},
    {"id": "F02", "query": {"region": "eu"}, "new_accepts": true, "new_default_limit": 25, "change_ids": ["C01", "C04"]}
  ],
  "response_fixtures": [
    {
      "id": "F03",
      "payload": {"items": [{"status": "paused"}], "next_cursor": "c2"},
      "old_shape_accepts": false,
      "new_shape_accepts": true,
      "old_C1_accepts": false,
      "change_ids": ["C02"]
    },
    {
      "id": "F04",
      "payload": {"items": []},
      "old_shape_accepts": false,
      "new_shape_accepts": true,
      "old_C1_accepts": false,
      "change_ids": ["C03"]
    },
    {
      "id": "F05",
      "payload": {"items": [], "next_cursor": null},
      "old_shape_accepts": true,
      "new_shape_accepts": false,
      "old_C1_accepts": true,
      "change_ids": ["C03"]
    }
  ],
  "expected_migration_actions": [
    "Obtain a region-selection rule, then supply region in C1 requests",
    "Define handling for paused and future unfamiliar statuses",
    "Adapt final-page handling to the supported old and new cursor shapes",
    "Decide whether to request an explicit limit; do not assume 50 is required"
  ],
  "execution_scope": "Hand-evaluation and local consistency checks of these extracts only"
}
```

F02 is a fictional fixture, not a recommendation to choose the `eu` region for real data. Its old-provider result is deliberately unspecified because the old contract extract does not define unknown-query handling. F03 and F04 isolate different response breaks; F05 shows that the new final-page rule also excludes the old explicit-null representation. The new-client/old-provider combination stays unassessed because the rollout does not require it.

## Checks to perform

Evaluate required query keys and the declared region set. For response fixtures, check required properties, allowed item statuses and nullable cursor handling independently. Check each C1 rule against the same payloads. Confirm that every fixture refers to an existing change and that no response-level success masks the missing request region. These checks do not call a provider, exercise a real client or establish a real migration result.

[verification.md](verification.md) contains the executed, standard-library check of these normalized predicates and deliberately false fixture conclusions. It leaves unspecified old-query behavior unresolved and distinguishes missing, null and empty-string cursors.
