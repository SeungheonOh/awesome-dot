"""Original small clients for a fictional local fixture, not an HTTP SDK."""


class ConsumerFailure(Exception):
    def __init__(self, code):
        super().__init__(code)
        self.code = code


def legacy_export(fetch, maximum_pages=4, explicit_limit=False):
    """C-S1: omitted limit, exhaustive statuses, short-page termination."""
    base_query = {"limit": 4} if explicit_limit else {}
    query, rows = dict(base_query), []
    labels = {"ready": "Ready", "retired": "Retired"}
    for _ in range(maximum_pages):
        page = fetch(query)
        for item in page["items"]:
            if item["status"] not in labels:
                raise ConsumerFailure("unsupported-status")
            rows.append({"id": item["id"], "label": labels[item["status"]]})
        # Valid under the v1 full-page guarantee and omitted-limit behavior.
        # This check is deliberately retained to expose the v2 regression.
        if len(page["items"]) < 4:
            return rows
        if "next_cursor" not in page:
            raise ConsumerFailure("missing-next-cursor")
        if page["next_cursor"] is None:
            return rows
        query = {**base_query, "cursor": page["next_cursor"]}
    raise ConsumerFailure("page-budget-exhausted")


def adapted_export(fetch, policy):
    """C-S2: use explicit policy; fetch validates the selected version first."""
    query = {"limit": policy["explicit_limit"]}
    rows, seen_cursors, seen_ids = [], set(), set()
    for _ in range(policy["maximum_pages"]):
        page = fetch(query)
        for item in page["items"]:
            if item["status"] not in policy["labels"]:
                raise ConsumerFailure("unsupported-status")
            if item["id"] in seen_ids:
                raise ConsumerFailure("duplicate-record")
            seen_ids.add(item["id"])
            rows.append({"id": item["id"], "label": policy["labels"][item["status"]]})
        # The boundary validates against the known provider version. Thus this
        # does not silently accept null from v2 or omission from v1.
        cursor = page.get("next_cursor")
        if cursor is None:
            return rows
        if cursor in seen_cursors:
            raise ConsumerFailure("repeated-cursor")
        seen_cursors.add(cursor)
        query = {"limit": policy["explicit_limit"], "cursor": cursor}
    # Fail closed: do not return an incomplete export as successful.
    raise ConsumerFailure("page-budget-exhausted")
