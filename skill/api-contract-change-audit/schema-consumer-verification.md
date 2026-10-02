# Reproduce the schema and consumer checks

Read [the contract, policy and directional report](schema-consumer-example.md) before interpreting this run. The earlier [normalized-predicate check](verification.md) is a separate example with different consumer assumptions; none of its claims is upgraded by this supplement.

## Run locally

Inspect [run.py](schema-consumer-fixture/run.py), [consumers.py](schema-consumer-fixture/consumers.py) and the sibling JSON inputs. From this skill folder, using an environment where the named packages are already available:

```bash
(
set -eu
set -C
python3 -B schema-consumer-fixture/run.py > schema-consumer-run.json
)
```

The program reads only named sibling files and installed package resources, and prints JSON to stdout. The no-clobber subshell refuses an existing report name; choose an unused name for another run. Treat a nonzero exit as a failed run even if an empty or partial output file exists. It installs nothing, starts no server, accepts no arbitrary input path or URL, and makes no HTTP calls. Missing packages are an execution blocker; installing them is a separate action, not part of this command.

Observed on 2026-10-02: exit 0 using Python 3.12.14, `jsonschema` 4.26.0, `referencing` 0.37.0 and the already installed `jsonschema-specifications` 2025.9.1. These versions were read from the environment; they were not installed for the run. [observed.json](schema-consumer-fixture/observed.json) is the actual retained stdout.

The output identifies the dialect, packages, registered resources and SHA-256 of every executable input. It includes full request/response traces and exported rows. Compare the input hashes before treating that retained output as evidence about an edited fixture. Error message wording is not an assertion; diagnostics retain keyword and instance/schema paths instead.

## What executed

| Layer | Actual evidence | What it cannot establish |
| --- | --- | --- |
| Schema syntax | Five schema documents validated against the installed 2020-12 meta-schema through an explicit local registry | Application meaning, reference completeness by itself, or API compatibility |
| Reference closure | All authored `$ref` values resolve through registered resources; missing-resource controls return `held` | General relative-reference, dynamic-reference or arbitrary-schema support |
| Instance validation | Fifteen request and seventeen response cases, each against both versions: 64 checks | All possible inputs or temporal/provider behavior |
| Ordinary consumers | Four required client/provider combinations executed; actual rows and calls retained | HTTP serialization, version negotiation or deployed behavior |
| Additional consumers | Eleven scenario runs isolate sparse pages, added status, full/empty finals and failure bounds | A universal guarantee for every legal provider traversal |
| Contradictions and omissions | False fixture conclusion rejected; annotation/behavior conflict rejected; missing and unknown references held | Authority to resolve a genuine product-policy conflict |

The runner contains explicit checks that raise on failure, so Python's optimization flag cannot silently remove the verification assertions. It does not use output self-comparison alone: expected schema classifications, record order/completeness, error reasons, label meaning and call bounds are checked independently of the provider model's returned rows.

## Ordinary, absent, null and empty instances

The retained `fixture_checks` array contains the payload and both actual classifications for each case. Useful witnesses include:

- Q01 `{}` is valid in both versions and stays `{}` after validation. Q03 null limit and Q04 empty-string limit are invalid. Q05 boolean limit is invalid
- Q06–Q08 establish the inclusive 1–4 bounds. Q14 numeric `2.0` is valid as a JSON Schema integer; Q15 `2.5` is invalid. HTTP query-string coercion remains untested
- Q09/Q10 reject null and empty request cursors; Q11 permits a nonempty cursor structurally. Its existence in a real traversal is a different question
- P01 is a short page with a nonempty cursor and P04 is an empty page with a nonempty cursor. Both pass both response schemas. Schema validity does not give P04 the v1 full-nonfinal-page behavioral guarantee
- P02 accepts explicit-null final cursor only in v1; P03 accepts omitted final cursor only in v2; P05 rejects an empty string in both
- P07–P10 distinguish missing items, null items, an empty object in place of the array and an empty item object. All are invalid; an empty array remains valid where the cursor rule is satisfied
- P06 permits `held` only in v2. P11–P13 reject null, empty and unknown status values. P14 rejects an extra response field; P15 proves the registered item-ID constraint is applied. P17 rejects a trailing newline in the identifier, using an explicit end-of-input assertion in the pattern

## Defaults are two separate observations

`defaults.v1` and `defaults.v2` each show `instance_after_validation: {}`. The validator does not insert `limit`. The model separately reads `behavior.json`, produces effective limits 4 and 2, and returns first-page counts 4 and 2.

An in-memory negative control changes only the v2 schema annotation to 4. That schema still passes meta-validation, and the model still applies 2 from the unchanged behavior source. A separate consistency check rejects the resulting schema-annotation/behavior conflict. The conflict is evidence to resolve, not permission to choose either source silently. These are observations of the authored local model, not observations of a server default.

## Successful adaptation and bounded failures

| Run key in `observed.json#/consumer_runs` | Actual result |
| --- | --- |
| `legacy-v1` | Six exported rows, two calls |
| `legacy-v2` | Two exported rows, one call; four missing IDs, incomplete success |
| `adapted-v1`, `adapted-v2` | Six exported rows, two calls each |
| `legacy-explicit-v2-sparse` | Zero exported rows, one call; six missing IDs |
| `adapted-v2-sparse` | Six exported rows across three calls, including an empty nonfinal page |
| `legacy-explicit-v2-held` | `unsupported-status` after one call |
| `adapted-v2-held` | `record-7` labeled “On hold” after one call |
| `legacy-explicit-v2-full-final` | `missing-next-cursor` after one call |
| `adapted-v2-full-final`, `adapted-v2-empty-final` | Four rows and zero rows, respectively; each terminates after one call |
| `adapted-v2-cycle` | `repeated-cursor` after two calls |
| `adapted-v2-budget` | `page-budget-exhausted` after four calls; fifth page never requested |
| `adapted-v2-duplicate` | `duplicate-record` after two calls |
| `adapted-v2-null-final` | `response-invalid` at the selected-v2 schema boundary after one call |

Cycle, budget and duplicate scenarios have schema-valid individual responses. The first two demonstrate that structure alone cannot establish termination; the duplicate scenario demonstrates a cross-page invariant. A budget failure is an explicit refusal to call the export complete, not a successful traversal. No partial rows are returned by the client when it raises an error. The trace records the pages it received.

## Reference discipline

The five application resources have URN identifiers. Their six authored `$ref` occurrences use absolute URNs with local JSON Pointer fragments. The runner explicitly preloads these resources and nine named, already installed 2020-12 meta-schema resources; python-jsonschema also retains its built-in local specification registry internally. Their HTTPS identifiers are names in in-memory registries, not downloads. Retrieval for an absent identifier raises `NoSuchResource`; it never opens a path or uses an HTTP client.

Before instance validation, the runner checks all references in the requested authored schema and its dependencies, including branches the sample would not visit. Removing `common.json` from an in-memory registry therefore holds an empty v2 response instead of calling it compatible. Replacing a request cursor reference with an unavailable URN holds even `{}`. The independent v1 response remains valid in that second control. The retained `negative_controls` section records the missing references and the rejected retrieval identifiers.

This closure walk is tailored to the supplied schemas: absolute `$ref` values, no nested `$id`, no `$dynamicRef`, no arbitrary vocabularies. It must not be advertised as a universal JSON Schema dependency analyzer.

## Primary semantics references

Read on 2026-10-02:

- [JSON Schema 2020-12 core](https://json-schema.org/draft/2020-12/json-schema-core): dialect and resource identification, references, assertions and annotations
- [JSON Schema 2020-12 validation](https://json-schema.org/draft/2020-12/json-schema-validation): `type`, `required`, bounds and the `default` metadata annotation. An integer is a number with zero fractional part; default is not a required property or a null replacement
- [python-jsonschema validation API](https://python-jsonschema.readthedocs.io/en/stable/validate/): concrete draft validator, schema validation, error iteration and optional format checking
- [python-jsonschema referencing](https://python-jsonschema.readthedocs.io/en/stable/referencing/): explicit `Registry` resources and retrieval configuration
- [python-jsonschema default FAQ](https://python-jsonschema.readthedocs.io/en/stable/faq/#why-doesn-t-my-schema-s-default-property-set-the-default-on-my-instance): ordinary validation does not populate defaults

`format` checking is **disabled** in both meta-schema and instance validation (`format_checker=None`). The application schemas contain no `format` keyword; they rely on explicit type, enum, pattern, length, bounds and object/array assertions. No result here depends on an optional format implementation.

## Independent readback

A separate review reran the inspected fixture in a private copy and reproduced the retained JSON exactly. Additional local cases completed six rows on the fourth call after two empty nonfinal pages, retained the old explicit-limit client's truncation, and rejected a duplicate within one page, an omitted v1 terminal cursor and a response exceeding the requested limit. The no-clobber report pattern separately refused an existing file without changing it. Source files, schemas and recorded output stayed unchanged; no endpoint, installation or real client was exercised.

## Release limits

This is a successful execution of an original local schema/client fixture, with an intentionally demonstrated compatibility failure. It is not production verification, a real provider test or approval to release v2. The unchanged C-S1/v2 combination still fails its required overlap. The owner decision about that overlap, real version selection, HTTP behavior and performance remain outside the completed checks.
