"""Offline interpreter for the bundled fictional permission contract only."""
from copy import deepcopy
from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path

CAPABILITIES = {
    "viewer": {"view"},
    "commenter": {"view", "comment"},
    "editor": {"view", "comment", "edit"},
}
TRISTATE = {"yes", "no", "unknown"}


def instant(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Timestamps require a timezone")
    return parsed


def validate(snapshot):
    if snapshot.get("fictional") is not True or snapshot.get("contract") != "Workshop Files v1":
        raise ValueError("Only the explicit fictional contract is supported")
    if snapshot["coverage"] not in {"complete", "partial"}:
        raise ValueError("Unknown permission coverage")
    if snapshot["link"]["audience"] not in {"restricted", "organization", "anyone"}:
        raise ValueError("Unknown link audience")
    if snapshot["link"]["role"] != "viewer":
        raise ValueError("This contract only supports viewer links")
    sources = [snapshot["file"]["id"]] + [a["id"] for a in snapshot["file"]["ancestors"]]
    if len(sources) != len(set(sources)):
        raise ValueError("Ambiguous source identity")
    if any(a["kind"] not in {"folder", "shared_drive"} for a in snapshot["file"]["ancestors"]):
        raise ValueError("Unknown ancestor type")
    ids = set()
    for grant in snapshot["grants"]:
        if grant["id"] in ids or grant["source_id"] not in sources:
            raise ValueError("Duplicate grant or unknown grant origin")
        ids.add(grant["id"])
        if grant["role"] not in CAPABILITIES or grant["principal_type"] not in {"person", "group"}:
            raise ValueError("Unsupported grant")
        if type(grant["active"]) is not bool:
            raise ValueError("Grant activation must be explicit")
        if grant.get("expires_at"):
            instant(grant["expires_at"])
    if any(v not in {"allowed", "blocked", "unknown"} for v in snapshot["policy"].values()):
        raise ValueError("Unknown policy state")
    if any(v not in TRISTATE for members in snapshot["memberships"].values() for v in members.values()):
        raise ValueError("Unknown membership state")
    instant(snapshot["captured_at"])


def opening_evidence(snapshot, recipient):
    account = recipient["account"]
    matching, excluded = [], 0
    for item in snapshot["observations"]:
        matches = (
            item["file_id"] == snapshot["file"]["id"]
            and item["account"] == account
            and item["session_account"] == account
            and item["action"] == recipient["capability"]
            and item["permission_revision"] == snapshot["permission_revision"]
            and instant(item["observed_at"]) <= instant(snapshot["captured_at"])
            and item["kind"] in {"recipient_report", "authorized_observation"}
            and item["result"] in {"success", "denied"}
        )
        if matches:
            matching.append(item)
        else:
            excluded += 1
    results = {item["result"] for item in matching}
    if len(results) > 1:
        status = "conflicting"
    elif results == {"denied"}:
        status = "failed"
    elif results == {"success"}:
        status = "observed_success" if any(i["kind"] == "authorized_observation" for i in matching) else "reported_success"
    else:
        status = "untested"
    return {"status": status, "evidence": matching, "excluded_observations": excluded}


def evaluate(snapshot, recipient):
    validate(snapshot)
    account, capability = recipient["account"], recipient["capability"]
    if capability not in {"view", "comment", "edit"}:
        raise ValueError("Unsupported requested capability")
    if any(recipient.get(k, "unknown") not in TRISTATE for k in ("organization_member", "has_link")):
        raise ValueError("Unrecognized recipient eligibility")
    confirmed, unknown = [], []
    source_types = {snapshot["file"]["id"]: "direct"}
    source_types.update({a["id"]: a["kind"] for a in snapshot["file"]["ancestors"]})
    for grant in snapshot["grants"]:
        if not grant["active"] or (grant.get("expires_at") and instant(grant["expires_at"]) <= instant(snapshot["captured_at"])):
            continue
        membership = (
            "yes" if grant["principal"] == account else "no"
        ) if grant["principal_type"] == "person" else snapshot["memberships"].get(grant["principal"], {}).get(account, "unknown")
        route = {
            "grant_id": grant["id"], "source_id": grant["source_id"],
            "origin": source_types[grant["source_id"]], "principal_type": grant["principal_type"],
            "principal": grant["principal"], "role": grant["role"],
        }
        if membership == "yes":
            confirmed.append(route)
        elif membership == "unknown":
            unknown.append(route)
    audience = snapshot["link"]["audience"]
    if audience != "restricted":
        requirements = [recipient.get("has_link", "unknown")]
        if audience == "organization":
            requirements.append(recipient.get("organization_member", "unknown"))
        route = {"grant_id": "link", "source_id": snapshot["file"]["id"], "origin": "link", "role": "viewer"}
        if "no" not in requirements:
            (confirmed if all(v == "yes" for v in requirements) else unknown).append(route)
    known_caps = set().union(*(CAPABILITIES[r["role"]] for r in confirmed))
    possible_caps = set().union(*(CAPABILITIES[r["role"]] for r in unknown))
    if snapshot["coverage"] == "partial":
        possible_caps.update({"view", "comment", "edit"})
    policy = snapshot["policy"].get(account, "unknown")
    permission = (
        "blocked" if policy == "blocked" else
        "unknown" if policy == "unknown" else
        "confirmed" if capability in known_caps else
        "unknown" if capability in possible_caps else "absent"
    )
    session = snapshot["sessions"].get(account)
    opening = opening_evidence(snapshot, recipient)
    conflict = (
        opening["status"] == "conflicting"
        or (opening["status"] in {"observed_success", "reported_success"} and permission in {"blocked", "absent"})
        or (opening["status"] == "failed" and permission == "confirmed")
    )
    return {
        "account": account, "requested_capability": capability,
        "permission": permission, "policy": policy,
        "confirmed_routes": confirmed, "unknown_routes": unknown,
        "grant_capability_floor": sorted(known_caps),
        "additional_possible_capabilities": sorted(possible_caps - known_caps),
        "session": "untested" if session is None else "matching_account" if session == account else "wrong_account",
        "recipient_opening": opening, "evidence_conflict": conflict,
    }


def matrix(snapshot, request):
    if request.get("fictional") is not True:
        raise ValueError("Only fictional requests are supported")
    if snapshot["file"]["id"] != request["file_id"] or snapshot["file"]["content_revision"] != request["content_revision"]:
        raise ValueError("Request and item identity/version differ")
    accounts = [r["account"] for r in request["recipients"]]
    if len(accounts) != len(set(accounts)):
        raise ValueError("Duplicate requested account")
    return {
        "evidence_mode": "fictional_offline_only", "file_id": snapshot["file"]["id"],
        "permission_revision": snapshot["permission_revision"], "captured_at": snapshot["captured_at"],
        "recipients": [evaluate(snapshot, r) for r in request["recipients"]],
        "incidental_access": evaluate(snapshot, request["incidental_access_check"]),
    }


def review_delta(before, after, request):
    """Check the two declared changes and reject every other state difference."""
    matrix(before, request)
    matrix(after, request)
    approved = request["approved_changes"]
    problems = []
    target = approved["add_direct"]
    if approved["link_audience"] != "restricted" or target["role"] != "viewer" or approved["notifications"] is not False:
        raise ValueError("This exercise supports only its narrow viewer-and-restricted-link correction")
    if target["account"] not in {r["account"] for r in request["recipients"]}:
        problems.append("Added account is not in the approved data audience")
    expected = deepcopy(before)
    expected["link"]["audience"] = approved["link_audience"]
    additions = [g for g in after["grants"] if g["id"] not in {b["id"] for b in before["grants"]}]
    if len(additions) != 1:
        problems.append("Expected exactly one new direct grant")
    else:
        required = {
            "id": additions[0]["id"], "source_id": request["file_id"],
            "principal_type": "person", "principal": target["account"],
            "role": target["role"], "active": True,
        }
        if additions[0] != required:
            problems.append("New grant differs from the exact approved grant")
        expected["grants"].append(required)
    expected["notifications_sent"] = approved["notifications"]
    # These fields are evidence, not permission/content changes.
    evidence_fields = {"captured_at", "permission_revision", "observations", "sessions", "simulated_receipt"}
    state = lambda value: {k: v for k, v in value.items() if k not in evidence_fields}
    if state(expected) != state(after):
        problems.append("After-state contains an unapproved state difference")
    return {
        "status": "matches_fictional_approval" if not problems else "held",
        "problems": problems, "live_actions_performed": 0,
        "evaluated_changes": ["exact direct grant addition", "link audience restriction"],
    }


def main():
    root = Path(__file__).resolve().parent.parent
    inputs = {name: (root / "fixtures" / f"{name}.json").read_bytes() for name in ("before", "after", "request")}
    packet = {name: json.loads(data) for name, data in inputs.items()}
    hashes = {name: sha256(data).hexdigest() for name, data in inputs.items()}
    outputs = {
        "before-matrix": matrix(packet["before"], packet["request"]),
        "after-matrix": matrix(packet["after"], packet["request"]),
        "change-review": review_delta(packet["before"], packet["after"], packet["request"]),
    }
    destination = root / "outputs"
    destination.mkdir(exist_ok=True)
    for name, result in outputs.items():
        result["input_sha256"] = hashes
        path = destination / f"{name}.json"
        path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        if json.loads(path.read_text()) != result:
            raise ValueError("Saved result differs from evaluated result")
    print(json.dumps({
        "change_review": outputs["change-review"]["status"],
        "before": {r["account"]: r["permission"] for r in outputs["before-matrix"]["recipients"]},
        "after": {r["account"]: r["permission"] for r in outputs["after-matrix"]["recipients"]},
        "live_actions_performed": 0,
    }, indent=2))


if __name__ == "__main__":
    main()
