"""Validate fixed local contracts and run original bounded client fixtures.

Reads only the named sibling inputs. No network, installation, or HTTP server.
Writes a JSON report to stdout; redirect it to retain the complete observations.
"""

import hashlib
import json
import platform
from copy import deepcopy
from importlib.metadata import version
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema_specifications import REGISTRY as INSTALLED_META_SCHEMAS
from referencing import Registry, Resource
from referencing.exceptions import NoSuchResource, Unresolvable

from consumers import ConsumerFailure, adapted_export, legacy_export

ROOT = Path(__file__).resolve().parent
DIALECT = "https://json-schema.org/draft/2020-12/schema"
SCHEMA_NAMES = ("common", "request-v1", "request-v2", "response-v1", "response-v2")
META_IDS = [DIALECT] + [
    "https://json-schema.org/draft/2020-12/meta/" + suffix
    for suffix in ("core", "applicator", "unevaluated", "validation", "meta-data",
                   "format-annotation", "format-assertion", "content")
]


def require(condition, detail):
    if not condition:
        raise AssertionError(detail)


def read_json(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def references(value):
    if isinstance(value, dict):
        if "$ref" in value:
            yield value["$ref"]
        for child in value.values():
            yield from references(child)
    elif isinstance(value, list):
        for child in value:
            yield from references(child)


class Schemas:
    def __init__(self, documents):
        self.documents, self.denied = documents, []

        def deny_retrieval(uri):
            self.denied.append(uri)
            raise NoSuchResource(ref=uri)

        self.registry = Registry(retrieve=deny_retrieval).with_resources(
            (uri, INSTALLED_META_SCHEMAS[uri]) for uri in META_IDS
        ).with_resources(
            (doc["$id"], Resource.from_contents(doc)) for doc in documents.values()
        )
        # Explicit local registry for meta-validation too. Format assertions are
        # disabled; the fixture schemas use type/enum/pattern/length assertions.
        meta = Draft202012Validator(
            Draft202012Validator.META_SCHEMA, registry=self.registry,
            format_checker=None,
        )
        self.meta_checks = {}
        for name, doc in documents.items():
            require(doc["$schema"] == DIALECT, "unexpected dialect: " + name)
            errors = list(meta.iter_errors(doc))
            require(not errors, "invalid schema document: " + name)
            self.meta_checks[name] = "valid"

    def missing_dependencies(self, name):
        missing, visited = set(), set()

        def visit(document):
            for ref in references(document):
                if ref in visited:
                    continue
                visited.add(ref)
                try:
                    resolved = self.registry.resolver().lookup(ref)
                except (Unresolvable, NoSuchResource):
                    missing.add(ref)
                else:
                    visit(resolved.contents)

        # Preflight even branches not reached by this particular instance.
        visit(self.documents[name])
        return sorted(missing)

    def check(self, name, value):
        missing = self.missing_dependencies(name)
        if missing:
            return {"result": "held", "missing_references": missing}
        validator = Draft202012Validator(
            self.documents[name], registry=self.registry, format_checker=None,
        )
        errors = list(validator.iter_errors(value))
        return {
            "result": "invalid" if errors else "valid",
            "errors": [{"instance_path": list(e.absolute_path),
                        "schema_path": list(e.absolute_schema_path),
                        "keyword": e.validator} for e in errors],
        }


class LocalPages:
    """In-memory provider model OR scripted pages, never a provider integration."""
    def __init__(self, schemas, behavior, provider_version, records=None, pages=None):
        self.schemas, self.behavior, self.version = schemas, behavior, provider_version
        self.records = deepcopy(behavior["records"] if records is None else records)
        self.pages, self.calls = deepcopy(pages), []
        self.expected_cursor = None

    def __call__(self, query):
        request_check = self.schemas.check("request-" + self.version, query)
        if request_check["result"] != "valid":
            raise ConsumerFailure("request-" + request_check["result"])
        rules = self.behavior["versions"][self.version]
        limit = int(query.get("limit", rules["omitted_limit"]))
        if self.pages is None:
            offsets = {"offset-" + str(i): i for i in range(1, len(self.records))}
            if "cursor" in query and query["cursor"] not in offsets:
                raise ConsumerFailure("unknown-fixture-cursor")
            start = offsets[query["cursor"]] if "cursor" in query else 0
            batch = self.records[start:start + limit]
            end = start + len(batch)
            page = {"items": batch}
            if end < len(self.records):
                page["next_cursor"] = "offset-" + str(end)
            elif rules["terminal"] == "explicit-null":
                page["next_cursor"] = None
        else:
            if query.get("cursor") != self.expected_cursor:
                raise ConsumerFailure("wrong-fixture-cursor")
            if len(self.calls) >= len(self.pages):
                raise ConsumerFailure("fixture-pages-exhausted")
            page = deepcopy(self.pages[len(self.calls)])
        response_check = self.schemas.check("response-" + self.version, page)
        trace = {"request": deepcopy(query), "effective_limit": limit,
                 "request_validation": request_check["result"], "response": page,
                 "response_validation": response_check["result"]}
        self.calls.append(trace)
        if response_check["result"] != "valid":
            raise ConsumerFailure("response-" + response_check["result"])
        if len(page["items"]) > limit:
            raise ConsumerFailure("page-exceeds-requested-limit")
        self.expected_cursor = page.get("next_cursor")
        return deepcopy(page)


def run_client(name, transport, policy, expected_ids, explicit_limit=False):
    try:
        if name == "legacy":
            rows = legacy_export(transport, policy["maximum_pages"], explicit_limit)
        else:
            rows = adapted_export(transport, policy)
    except ConsumerFailure as error:
        return {"outcome": "failed", "reason": error.code, "calls": transport.calls}
    actual = [row["id"] for row in rows]
    return {"outcome": "complete" if actual == expected_ids else "incomplete-success",
            "rows": rows, "missing_ids": [i for i in expected_ids if i not in actual],
            "calls": transport.calls}


def verify_cases(schemas, cases):
    output = []
    for kind in ("request", "response"):
        for case in cases[kind + "_cases"]:
            record = {"id": case["id"], "meaning": case["meaning"], "value": case["value"]}
            for revision in ("v1", "v2"):
                result = schemas.check(kind + "-" + revision, case["value"])
                require(result["result"] == case[revision], (case["id"], revision, result))
                record[revision] = result
            output.append(record)
    return output


def check_default_agreement(documents, behavior):
    for revision in ("v1", "v2"):
        annotation = documents["request-" + revision]["properties"]["limit"]["default"]
        require(annotation == behavior["versions"][revision]["omitted_limit"],
                "schema annotation/behavior conflict: " + revision)


def expected_rejection(action):
    try:
        action()
    except AssertionError:
        return "rejected"
    raise AssertionError("contradictory conclusion was accepted")


def main():
    documents = {name: read_json("schemas/" + name + ".json") for name in SCHEMA_NAMES}
    behavior, cases = read_json("behavior.json"), read_json("cases.json")
    schemas = Schemas(documents)
    check_default_agreement(documents, behavior)
    fixture_results = verify_cases(schemas, cases)
    policy, records = behavior["consumer_policy"], behavior["records"]
    ids = [record["id"] for record in records]

    # The two request assertion sets are identical after removing annotations/IDs.
    def assertions(document):
        value = deepcopy(document)
        value.pop("$id")
        value["properties"]["limit"].pop("default")
        return value

    require(assertions(documents["request-v1"]) == assertions(documents["request-v2"]),
            "request assertion sets differ")
    defaults = {}
    for revision in ("v1", "v2"):
        query = {}
        require(schemas.check("request-" + revision, query)["result"] == "valid", revision)
        require(query == {}, "validator inserted a default")
        provider = LocalPages(schemas, behavior, revision)
        provider(query)
        defaults[revision] = {"instance_after_validation": query,
                              "annotation": documents["request-" + revision]["properties"]["limit"]["default"],
                              "model_effective_limit": provider.calls[0]["effective_limit"],
                              "model_first_page_count": len(provider.calls[0]["response"]["items"])}

    runs = {}
    for client, revision in policy["required_overlap"]:
        key = client + "-" + revision
        runs[key] = run_client(client, LocalPages(schemas, behavior, revision), policy, ids)
    require(runs["legacy-v1"]["outcome"] == "complete", "baseline broken")
    require(runs["legacy-v2"]["outcome"] == "incomplete-success", "missing default witness")
    require(len(runs["legacy-v2"]["rows"]) == 2, "incorrect truncation witness")
    for revision in ("v1", "v2"):
        require(runs["adapted-" + revision]["outcome"] == "complete", "adaptation failed")

    scripted = {
        "sparse": [{"items": [], "next_cursor": "page-2"},
                   {"items": records[:4], "next_cursor": "page-3"}, {"items": records[4:]}],
        "held": [{"items": [{"id": "record-7", "status": "held"}]}],
        "full-final": [{"items": records[:4]}],
        "empty-final": [{"items": []}],
        "cycle": [{"items": [], "next_cursor": "same"}, {"items": [], "next_cursor": "same"}],
        "budget": [{"items": [], "next_cursor": "page-" + str(i)} for i in range(2, 7)],
        "duplicate": [{"items": records[:1], "next_cursor": "page-2"}, {"items": records[:1]}],
        "null-final": [{"items": [], "next_cursor": None}],
    }
    expected = {
        "sparse": ids, "held": ["record-7"], "full-final": ids[:4], "empty-final": [],
        "cycle": [], "budget": [], "duplicate": ids[:1], "null-final": [],
    }
    for case, pages in scripted.items():
        runs["adapted-v2-" + case] = run_client(
            "adapted", LocalPages(schemas, behavior, "v2", pages=pages), policy, expected[case])
        if case in ("sparse", "held", "full-final"):
            runs["legacy-explicit-v2-" + case] = run_client(
                "legacy", LocalPages(schemas, behavior, "v2", pages=pages), policy,
                expected[case], explicit_limit=True)
    for case in ("sparse", "held", "full-final", "empty-final"):
        require(runs["adapted-v2-" + case]["outcome"] == "complete", case)
    require(runs["adapted-v2-held"]["rows"] == [{"id": "record-7", "label": "On hold"}], "held meaning")
    require(runs["legacy-explicit-v2-sparse"]["outcome"] == "incomplete-success", "sparse witness")
    for case, reason in (("held", "unsupported-status"), ("full-final", "missing-next-cursor")):
        require(runs["legacy-explicit-v2-" + case].get("reason") == reason, case)
    for case, reason in (("cycle", "repeated-cursor"), ("budget", "page-budget-exhausted"),
                         ("duplicate", "duplicate-record"), ("null-final", "response-invalid")):
        require(runs["adapted-v2-" + case].get("reason") == reason, case)
    require(len(runs["adapted-v2-budget"]["calls"]) == 4, "budget was not bounded")

    # Missing references are held even for an empty array that would not touch
    # the missing item definition during ordinary instance validation.
    without_common = Schemas({k: v for k, v in documents.items() if k != "common"})
    missing = without_common.check("response-v2", {"items": []})
    require(missing["result"] == "held", "missing dependency guessed")
    changed = deepcopy(documents)
    changed["request-v2"]["properties"]["cursor"]["$ref"] = "urn:shelf-example:unavailable:1"
    unresolved = Schemas(changed)
    unknown_ref = unresolved.check("request-v2", {})
    require(unknown_ref["result"] == "held", "unresolved dependency guessed")
    require(unresolved.check("response-v1", {"items": [], "next_cursor": None})["result"] == "valid",
            "an unrelated result was unnecessarily blocked")

    false_cases = deepcopy(cases)
    false_cases["response_cases"][0]["v2"] = "invalid"
    changed_annotation = deepcopy(documents)
    changed_annotation["request-v2"]["properties"]["limit"]["default"] = 4
    annotation_schemas = Schemas(changed_annotation)
    model = LocalPages(annotation_schemas, behavior, "v2")
    model({})
    require(model.calls[0]["effective_limit"] == 2, "annotation incorrectly drives behavior")
    controls = {
        "false_schema_conclusion": expected_rejection(lambda: verify_cases(schemas, false_cases)),
        "annotation_behavior_conflict": expected_rejection(lambda: check_default_agreement(changed_annotation, behavior)),
        "changed_annotation_still_meta_valid": annotation_schemas.meta_checks["request-v2"],
        "changed_annotation_did_not_change_model_default": model.calls[0]["effective_limit"],
        "missing_common_resource": missing,
        "unknown_reference": unknown_ref,
        "unrelated_response_v1": "valid",
        "retrieval_callbacks_only_rejected": without_common.denied + unresolved.denied,
    }
    source_files = ["behavior.json", "cases.json", "consumers.py", "run.py"] + [
        "schemas/" + name + ".json" for name in SCHEMA_NAMES]
    report = {
        "fixture_revision": cases["revision"],
        "environment": {"python": platform.python_version(),
                        "jsonschema": version("jsonschema"), "referencing": version("referencing"),
                        "jsonschema-specifications": version("jsonschema-specifications")},
        "dialect": DIALECT, "format_assertions_enabled": False,
        "scope": "local schema validation and original consumer/model execution; no HTTP or deployed provider",
        "registered_contract_resources": sorted(doc["$id"] for doc in documents.values()),
        "registered_installed_meta_resources": META_IDS,
        "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in source_files},
        "schema_meta_validation": schemas.meta_checks,
        "request_assertion_sets_identical": True,
        "fixture_checks": fixture_results, "defaults": defaults,
        "consumer_runs": runs, "negative_controls": controls,
        "summary": {"schema_documents": len(documents), "instance_version_checks": len(fixture_results) * 2,
                    "consumer_runs": len(runs), "required_original_overlap": "fails: legacy-v2 returns incomplete success",
                    "adapted_overlap": "passes executed fixture scenarios; not universal compatibility proof"},
    }
    require(not schemas.denied, "ordinary fixture attempted unresolved retrieval")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
