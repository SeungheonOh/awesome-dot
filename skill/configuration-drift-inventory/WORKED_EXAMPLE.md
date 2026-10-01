# Worked example: Larch renderer snapshots

This is a fictional, offline comparison. Every input needed for this example is below; the labels identify supplied exports, not connected services. In an actual task, read authorized sanitized exports and produce the inventory using their real provenance. This fixture grants no access and does not authorize remediation.

## Request and bounded inputs

> Compare Larch's approved preview baseline with the east test renderer at 2026-10-01T09:15:00Z. Use the supplied template, override and field contract. Explain meaningful differences and route unresolved decisions to their owners. Do not contact either environment or change a setting.

The baseline owner approved `preview-template-v8` for these nine fields. A snapshot consists of that template plus a shallow, **field-level** override: an override replaces the entire value at a dotted path. An absent override inherits the template; explicit null replaces it. This is not recursive merging of `render.labels`. Both exports are complete for this bounded scope. The optional annotation field can be absent in an otherwise complete export.

Field contract supplied by the rendering team:

- `render.timeout`: positive duration, accepting only seconds (`s`) or milliseconds (`ms`); compare in milliseconds
- `render.labels`: string map; JSON object key order is immaterial
- `render.fallbacks`: ordered list; the first available encoder wins, so list order is material
- `render.locale`: case-sensitive locale string
- `render.watermark`: empty string is a valid empty text layer; null disables that layer, a different behavior
- `render.retry_limit` and `render.concurrency`: integers, with no unit conversion
- `render.dpi`: integer or profile interpolation; no profile export was supplied, so interpolation cannot be resolved
- `render.annotation`: absent omits annotation metadata; explicit null emits a null annotation property; no inherited application default

These are application rendering settings. Credential material and security settings are outside scope; no secret values or secret-derived hashes are in the fixture.

```json
{
  "comparison_time": "2026-10-01T09:15:00Z",
  "baseline": {"id": "preview-template-v8", "owner": "Rendering lead", "captured_at": "2026-10-01T09:00:00Z", "source": "supplied/baseline.json", "complete": true},
  "target": {"id": "east-test-export-41", "template": "preview-template-v8", "captured_at": "2026-10-01T09:02:00Z", "source": "supplied/east-overrides.json", "complete": true},
  "template": {
    "render.timeout": {"value": 2, "unit": "s"},
    "render.labels": {"engine": "larch", "tier": "preview"},
    "render.fallbacks": ["svg", "png"],
    "render.locale": "en-GB",
    "render.watermark": "",
    "render.retry_limit": 2,
    "render.concurrency": 4,
    "render.dpi": 144
  },
  "east_overrides": {
    "render.timeout": {"unit": "ms", "value": 2000},
    "render.labels": {"tier": "preview", "engine": "larch"},
    "render.fallbacks": ["png", "svg"],
    "render.retry_limit": 4,
    "render.concurrency": 2,
    "render.dpi": "${profile.dpi}",
    "render.annotation": null
  },
  "exceptions": [
    {"id": "EX-17", "environment": "east-test-export-41", "field": "render.concurrency", "allowed_value": 2, "reason": "Shared preview worker allocation", "owner": "Preview platform owner", "approved_at": "2026-09-25T12:00:00Z", "expires_at": "2026-10-08T00:00:00Z"},
    {"id": "EX-09", "environment": "east-test-export-41", "field": "render.retry_limit", "allowed_value": 4, "reason": "Temporary encoder migration", "owner": "Encoder owner", "approved_at": "2026-09-20T12:00:00Z", "expires_at": "2026-09-30T00:00:00Z"}
  ]
}
```

The exception interval includes `approved_at` and excludes `expires_at`. Exception records are exact field/environment/value grants; EX-17 cannot justify another concurrency value, another environment or a reordered fallback list.

## Expected artifact: read-only inventory

Comparison: baseline `preview-template-v8` against `east-test-export-41`, as of 2026-10-01T09:15:00Z. Provenance for a field is its dotted path in the JSON block above. `T` below means `template`; `E` means `east_overrides`. A target state records both source layer and value kind, so inherited-empty is not confused with missing or null.

| Field | Baseline → target effective comparison value | Target source/state | Classification | Evidence or decision |
|---|---|---|---|---|
| render.timeout | 2000 ms → 2000 ms | E; explicit duration | equivalent | T is 2 s; E is 2000 ms |
| render.labels | same string map | E; explicit object | equivalent | Keys differ only in presentation order |
| render.fallbacks | [svg, png] → [png, svg] | E; explicit ordered list | unexplained | Encoder preference changes; Rendering lead to confirm intended order |
| render.locale | en-GB → en-GB | T; inherited string | equivalent | No E override; complete export and supplied precedence establish inheritance |
| render.watermark | empty string → empty string | T; inherited empty | equivalent | Empty remains distinct from null |
| render.retry_limit | 2 → 4 | E; explicit integer | stale exception | EX-09 expired before comparison; Encoder owner to renew or revise |
| render.concurrency | 4 → 2 | E; explicit integer | expected | EX-17 matches scope, value and validity; retain the evidenced reason |
| render.dpi | 144 → unresolved | E; explicit interpolation | unknown effective value | Need only sanitized `profile.dpi` and its source/version; don't assume 144 |
| render.annotation | absent → null | E; explicit null | unexplained | Contract distinguishes omission from null; Rendering lead to confirm intended payload |

Reconciliation: nine scoped fields; eight resolved comparisons and one unresolved; four equivalent, one expected, one stale exception, two unexplained and one unknown. No fields were silently excluded and no runtime environment was accessed.

Decision queue:

1. Rendering lead: confirm encoder preference and whether annotation should be omitted or explicit null. The snapshot proves different representations; the field contract establishes their distinct effects. No output-quality failure has been observed.
2. Encoder owner: EX-09 no longer establishes approval at the comparison time. Ask whether four retries remains intentional; expiry alone does not prove the setting is wrong.
3. Preview platform owner: EX-17 currently explains concurrency two. Record its expiry without turning a future expiry into a current violation.
4. Configuration exporter: provide the sanitized profile value for DPI plus its version/provenance. Keep the effective DPI and its correctness unknown until then.

## Ambiguous and failure branches

- **Incomplete override export:** if `target.complete` becomes false and no rendered export exists, absence of `render.locale` or `render.watermark` cannot establish inheritance. Change those target effective values to unknown; retain present fields. Ask for a complete bounded override export, not access to the system.
- **Unsupported duration:** if east timeout is `{ "value": 2, "unit": "ticks" }`, do not guess a conversion. Timeout becomes unknown pending its field contract; do not report equivalence or approved drift.
- **No baseline authority:** if approval of v8 is withdrawn, retain observed pairwise equalities/differences and exception evidence, but remove any assertion that v8 is correct. Request a field owner decision before evaluating conformity to a replacement baseline.
- **Additional evidence:** a complete, provenance-bearing profile export resolving DPI to 144 makes only that row equivalent. It does not resolve fallback order, annotation or expired EX-09.

## Independently executable assertions

From the repository root, run this local standard-library check. It reads the fixture from this document, independently derives values and exception validity, and checks semantic claims rather than matching the output table's wording. It neither connects to an environment nor writes configuration.

```python
import copy
import json
import re
from datetime import datetime
from pathlib import Path

text = Path("skill/configuration-drift-inventory/WORKED_EXAMPLE.md").read_text()
f = json.loads(re.search(r"```json\n(.*?)\n```", text, re.S).group(1))
MISSING, UNKNOWN = object(), object()
fields = set(f["template"]) | set(f["east_overrides"])

def effective(field, overrides, complete=True):
    if field in overrides:
        return overrides[field]
    return f["template"].get(field, MISSING) if complete else UNKNOWN

def normalize(field, value):
    if field == "render.timeout":
        factors = {"s": 1000, "ms": 1}
        if not isinstance(value, dict) or value.get("unit") not in factors:
            return UNKNOWN
        return value["value"] * factors[value["unit"]]
    if field == "render.dpi" and isinstance(value, str):
        return UNKNOWN
    return value

def classify(field, overrides, complete=True):
    a = normalize(field, f["template"].get(field, MISSING))
    b = normalize(field, effective(field, overrides, complete))
    if a is UNKNOWN or b is UNKNOWN:
        return "unknown"
    if a == b:
        return "equivalent"
    for ex in f["exceptions"]:
        if (ex["environment"] == f["target"]["id"] and
            ex["field"] == field and ex["allowed_value"] == b):
            now = datetime.fromisoformat(f["comparison_time"])
            start, end = map(datetime.fromisoformat, (ex["approved_at"], ex["expires_at"]))
            if start <= now < end:
                return "expected"
            if now >= end:
                return "stale exception"
    return "unexplained"

actual = {key: classify(key, f["east_overrides"]) for key in fields}
assert actual == {
    "render.timeout": "equivalent", "render.labels": "equivalent",
    "render.fallbacks": "unexplained", "render.locale": "equivalent",
    "render.watermark": "equivalent", "render.retry_limit": "stale exception",
    "render.concurrency": "expected", "render.dpi": "unknown",
    "render.annotation": "unexplained"
}
assert effective("render.annotation", {}) is MISSING
assert effective("render.annotation", f["east_overrides"]) is None
assert effective("render.watermark", f["east_overrides"]) == ""
assert "render.locale" not in f["east_overrides"]
assert classify("render.locale", f["east_overrides"], False) == "unknown"
assert classify("render.watermark", f["east_overrides"], False) == "unknown"
changed = copy.deepcopy(f["east_overrides"])
changed["render.timeout"] = {"value": 2, "unit": "ticks"}
assert classify("render.timeout", changed) == "unknown"
changed["render.concurrency"] = 3
assert classify("render.concurrency", changed) == "unexplained"
changed["render.dpi"] = 144
assert classify("render.dpi", changed) == "equivalent"
assert sum(v != "unknown" for v in actual.values()) == 8
print("PASS: value semantics, nine-field reconciliation, exception scope and ambiguity branches")
```

Observed validation: the fenced check passed with Python 3.12.14 on 2026-10-01. JSON parsing, all table classifications, missing/null/empty distinctions, object and list ordering, unit equivalence, exception scope and ambiguous-input branches were checked locally. This validates the example's comparison logic, not a general configuration parser or any live renderer.
