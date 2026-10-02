#!/usr/bin/env python3
"""Independent deterministic response-object tests; no sockets or remote URLs."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
PAYLOAD = (
    "Fictional meadow trail card, edition 7\n"
    "Café stop: bring a paper map and a yellow pencil.\n"
    "Use the east gate at noon. No booking or real personal data.\n"
).encode("utf-8")
ETAG = '"meadow-v7"'
CUT = PAYLOAD.index("é".encode("utf-8")) + 1
SENTINEL = b"Original destination content must remain.\n"


class Responses:
    def __init__(self, reply):
        self.reply = reply
        self.requests = []

    def resource(self, _case):
        return "fixture://independent-meadow/edition-7.txt"

    def get(self, case, phase, headers):
        self.requests.append({"case": case, "phase": phase, "headers": headers})
        return self.reply


def changed_case(name, cut=CUT, status=206, change=None, tag=ETAG, expected="resumed", reason=None):
    return dict(name=name, cut=cut, status=status, change=change, tag=tag, expected=expected, reason=reason)


CASES = [
    changed_case("utf8_split_prefix"),
    changed_case("empty_prefix", cut=0),
    changed_case("one_byte_suffix", cut=len(PAYLOAD)-1),
    changed_case("range_ignored", status=200, expected="restarted_full"),
    changed_case("weak_restart", status=200, tag="W/"+ETAG, expected="restarted_full"),
    changed_case("no_validator_restart", status=200, tag=None, expected="restarted_full"),
    changed_case("different_complete_body", status=200, change="corrupt", expected="held", reason="full_digest_mismatch"),
    changed_case("different_suffix", change="corrupt", expected="held", reason="full_digest_mismatch"),
    changed_case("prefix_disagrees_with_receipt", change="prefix", expected="held", reason="partial_changed_since_receipt"),
    changed_case("existing_destination", change="destination", expected="held", reason="destination_exists"),
    changed_case("short_response", change="truncate", expected="held", reason="truncated_or_misframed_body"),
    changed_case("duplicate_content_length", change="duplicate_length", expected="held", reason="duplicate_content-length"),
    changed_case("different_validator", change="validator", expected="held", reason="response_validator_conflict"),
    changed_case("different_coding", change="coding", expected="held", reason="changed_content_encoding"),
    changed_case("transfer_encoding", change="transfer_encoding", expected="held", reason="unsupported_transfer_encoding"),
    changed_case("shorter_valid_range", change="shorter_range", expected="held", reason="range_end_or_total_conflict"),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-dir", required=True, type=Path, help="Reviewed skill directory containing scripts/rehearse_recovery.py")
    parser.add_argument("--output-parent", required=True, type=Path, help="Existing approved private directory; creates a fresh child")
    args = parser.parse_args()
    source = args.skill_dir / "scripts/rehearse_recovery.py"
    if not source.is_file():
        parser.error("skill directory must contain scripts/rehearse_recovery.py")
    if not args.output_parent.is_dir():
        parser.error("output parent must be an existing approved directory")
    source_before = hashlib.sha256(source.read_bytes()).hexdigest()
    spec = importlib.util.spec_from_file_location("download_recovery_under_review", source)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    output = Path(tempfile.mkdtemp(prefix="changed-inputs-", dir=args.output_parent))
    contract = {"identity": "fictional-meadow/edition-7/identity", "length": len(PAYLOAD), "sha256": module.digest(PAYLOAD), "digest_provenance": "Independently authored fictional bytes in review_changed_inputs.py, a byte-equivalence oracle only"}
    (output / "expected-meadow.txt").write_bytes(PAYLOAD)
    (output / "contract.json").write_text(json.dumps(contract, indent=2)+"\n")
    rows = []
    for entry in CASES:
        directory = output / entry["name"]
        directory.mkdir()
        prefix = PAYLOAD[:entry["cut"]]
        body = PAYLOAD if entry["status"] == 200 else PAYLOAD[entry["cut"]:]
        headers = [("Content-Type", "text/plain; charset=utf-8"), ("Content-Length", str(len(body))), ("ETag", ETAG)]
        if entry["status"] == 206:
            headers.append(("Content-Range", f"bytes {entry['cut']}-{len(PAYLOAD)-1}/{len(PAYLOAD)}"))
        change = entry["change"]
        if change == "corrupt":
            body = bytes([body[0] ^ 1]) + body[1:]
        elif change == "truncate":
            body = body[:-1]
        elif change == "duplicate_length":
            headers.append(("cOnTeNt-LeNgTh", str(len(body))))
        elif change == "validator":
            headers = [(k, '"meadow-v8"' if k == "ETag" else v) for k,v in headers]
        elif change == "coding":
            headers.append(("Content-Encoding", "gzip"))
        elif change == "transfer_encoding":
            headers.append(("Transfer-Encoding", "chunked"))
        elif change == "shorter_range":
            body = body[:-1]
            headers = [(k,v) for k,v in headers if k not in ("Content-Range", "Content-Length")]
            headers.extend([("Content-Range", f"bytes {entry['cut']}-{len(PAYLOAD)-2}/{len(PAYLOAD)}"), ("Content-Length", str(len(body)))])
        reply = module.Reply(entry["status"], tuple(headers), body)
        transport = Responses(reply)
        receipt = {"identity": contract["identity"], "resource": transport.resource(entry["name"]), "selectors": dict(module.SELECTORS), "etag": entry["tag"], "partial_length": len(prefix), "partial_sha256": module.digest(prefix), "seed_status": 200, "seed_declared_length": len(PAYLOAD), "seed_observed_length": len(prefix)}
        if change == "prefix":
            prefix = b"X" + prefix[1:]
        (directory / "original.part").write_bytes(prefix)
        (directory / "receipt.json").write_text(json.dumps(receipt, indent=2)+"\n")
        (directory / "input-reply.json").write_text(json.dumps({"status": reply.status, "headers": reply.headers, "actual_body_count": len(body), "actual_body_sha256": module.digest(body)}, indent=2)+"\n")
        if change == "destination":
            (directory / "visitor-card.txt").write_bytes(SENTINEL)
        try:
            outcome = module.recover(entry["name"], transport, directory, contract, receipt)
            reason = None
        except module.Hold as error:
            outcome, reason = "held", str(error)
        final = directory / "visitor-card.txt"
        final_bytes = final.read_bytes() if final.exists() else None
        checks = {"expected_outcome": outcome == entry["expected"], "expected_hold_reason": reason == entry["reason"], "partial_preserved": (directory / "original.part").read_bytes() == prefix, "final_bytes": final_bytes == (SENTINEL if change == "destination" else PAYLOAD if outcome != "held" else None)}
        if transport.requests:
            request = transport.requests[0]["headers"]
            should_resume = module.strong_etag(entry["tag"])
            checks["correct_resume_or_restart_request"] = (request.get("Range") == f"bytes={len(prefix)}-" and request.get("If-Range") == entry["tag"]) if should_resume else ("Range" not in request and "If-Range" not in request)
        else:
            checks["stopped_before_request"] = change == "prefix"
        if outcome != "held":
            checks["utf8_readable_and_exact"] = final_bytes.decode("utf-8") == PAYLOAD.decode("utf-8")
        if change in ("corrupt", "destination"):
            checks["failed_candidate_retained"] = (directory / "candidate.bin").exists()
        rows.append({"case": entry["name"], "cut": entry["cut"], "outcome": outcome, "reason": reason, "requests": transport.requests, "checks": checks})
    report = {"scope": "independent changed-input in-process response objects; no socket/HTTP framing claim", "source_sha256_before": source_before, "source_sha256_after": hashlib.sha256(source.read_bytes()).hexdigest(), "payload_bytes": len(PAYLOAD), "cut_inside_utf8_character": CUT, "fixture_source_is_distinct": PAYLOAD != module.PAYLOAD, "cases": rows, "all_passed": all(all(row["checks"].values()) for row in rows)}
    (output / "results.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"output_directory": output.name, "all_passed": report["all_passed"], "cases": len(rows), "source_unchanged": report["source_sha256_before"] == report["source_sha256_after"]}))
    return 0 if report["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
