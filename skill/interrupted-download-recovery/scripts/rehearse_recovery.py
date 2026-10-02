#!/usr/bin/env python3
"""A bounded, fictional download-recovery rehearsal; never takes a remote URL.

Python 3.12+, standard library only. The HTTP mode serves constants from memory
on 127.0.0.1. The in-process mode uses response objects and opens no sockets.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import http.client
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import re
import tempfile
import threading
import time


PAYLOAD = (
    b"Cedar Observatory visitor card\n"
    b"Fictional practice file, revision 1.\n"
    b"Bring a notebook. Meet beside the blue model telescope.\n"
    b"If clouds arrive, use the indoor star map.\n"
    b"This card contains no real booking or personal information.\n"
)
ETAG = '"cedar-card-v1"'
CUT = 67
MAX_BYTES = 4096
MAX_REQUESTS = 64
RUN_SECONDS = 20
REQUEST_SECONDS = 2
SELECTORS = {"Accept": "text/plain", "Accept-Encoding": "identity"}
CASES = (
    "resume", "ignore_range", "weak_restart", "no_validator_restart",
    "changed_200", "wrong_start", "wrong_end", "wrong_total", "unknown_total",
    "wrong_etag", "missing_etag", "weak_206", "truncated_206", "bad_length",
    "truncated_200", "corrupt_suffix", "complete_416", "short_416",
    "wrong_416_total", "encoded", "duplicate_range", "multipart",
    "missing_binding", "changed_partial", "destination_exists",
)
SUCCESS = {
    "resume": "resumed", "ignore_range": "restarted_full",
    "weak_restart": "restarted_full", "no_validator_restart": "restarted_full",
    "complete_416": "verified_complete_partial",
}


class Hold(Exception):
    """No usable final is published for this candidate."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise Hold(message)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strong_etag(value: str | None) -> bool:
    return bool(value is not None and re.fullmatch(r'"[\x21\x23-\x7e\x80-\xff]*"', value))


@dataclass(frozen=True)
class Reply:
    status: int
    headers: tuple[tuple[str, str], ...]
    body: bytes

    def one(self, name: str) -> str | None:
        values = [v for k, v in self.headers if k.lower() == name.lower()]
        require(len(values) <= 1, "duplicate_" + name.lower())
        return values[0] if values else None


def initial_etag(case: str) -> str | None:
    if case == "weak_restart":
        return "W/" + ETAG
    return None if case == "no_validator_restart" else ETAG


def fixture(case: str, phase: str, request: dict[str, str]) -> Reply:
    """All server bodies are these tiny original bytes, never filesystem data."""
    require(case in CASES and phase in ("seed", "recover"), "unknown_fixture")
    require(all(request.get(k.lower()) == v for k, v in SELECTORS.items()), "selectors")
    tag = initial_etag(case)
    headers = [("Content-Type", "text/plain; charset=utf-8"), ("Connection", "close")]
    if tag is not None:
        headers.append(("ETag", tag))
    if phase == "seed":
        body = PAYLOAD if case in ("complete_416", "wrong_416_total") else PAYLOAD[:CUT]
        return Reply(200, tuple(headers + [("Content-Length", str(len(PAYLOAD)))]), body)
    offset = len(PAYLOAD) if case in ("complete_416", "wrong_416_total") else CUT
    if case in ("weak_restart", "no_validator_restart"):
        require("range" not in request and "if-range" not in request, "unsafe_weak_resume")
        return Reply(200, tuple(headers + [("Content-Length", str(len(PAYLOAD)))]), PAYLOAD)
    require(request.get("range") == f"bytes={offset}-", "wrong_request_range")
    require(request.get("if-range") == ETAG, "wrong_request_if_range")
    if case in ("ignore_range", "changed_200", "truncated_200"):
        body = PAYLOAD
        if case == "changed_200":
            body = PAYLOAD.replace(b"revision 1", b"revision 2")
            headers = [(k, '"cedar-card-v2"' if k == "ETag" else v) for k, v in headers]
        if case == "truncated_200":
            body = body[:-5]
        return Reply(200, tuple(headers + [("Content-Length", str(len(PAYLOAD)))]), body)
    if case in ("complete_416", "short_416", "wrong_416_total"):
        total = len(PAYLOAD) - 1 if case == "wrong_416_total" else len(PAYLOAD)
        return Reply(416, tuple(headers + [("Content-Range", f"bytes */{total}"), ("Content-Length", "0")]), b"")
    start, end, total = offset, len(PAYLOAD) - 1, str(len(PAYLOAD))
    body = PAYLOAD[offset:]
    if case == "wrong_start":
        start += 1
    if case == "wrong_end":
        end -= 1
    if case == "wrong_total":
        total = str(len(PAYLOAD) + 1)
    if case == "unknown_total":
        total = "*"
    if case in ("wrong_etag", "weak_206"):
        value = '"cedar-card-v2"' if case == "wrong_etag" else "W/" + ETAG
        headers = [(k, value if k == "ETag" else v) for k, v in headers]
    if case == "missing_etag":
        headers = [(k, v) for k, v in headers if k != "ETag"]
    if case == "encoded":
        headers.append(("Content-Encoding", "gzip"))
    if case == "multipart":
        headers = [(k, "multipart/byteranges; boundary=fixture" if k == "Content-Type" else v) for k, v in headers]
    headers.append(("Content-Range", f"bytes {start}-{end}/{total}"))
    if case == "duplicate_range":
        headers.append(("Content-Range", f"bytes {start}-{end}/{total}"))
    length = len(body) + (1 if case == "bad_length" else 0)
    headers.append(("Content-Length", str(length)))
    if case == "truncated_206":
        body = body[:-5]
    if case == "corrupt_suffix":
        body = bytes([body[0] ^ 1]) + body[1:]
    return Reply(206, tuple(headers), body)


class Transport:
    def __init__(self, mode: str):
        self.mode = mode
        self.count = 0
        self.deadline = time.monotonic() + RUN_SECONDS
        self.server = None
        self.thread = None
        if mode == "http":
            seen = set()
            class Handler(BaseHTTPRequestHandler):
                protocol_version = "HTTP/1.1"

                def do_GET(self):
                    parts = self.path.strip("/").split("/")
                    if len(parts) != 2 or parts[0] not in CASES or parts[1] != "visitor-card.txt":
                        self.send_error(404)
                        return
                    try:
                        phase = "recover" if parts[0] in seen else "seed"
                        seen.add(parts[0])
                        reply = fixture(parts[0], phase, {k.lower(): v for k, v in self.headers.items()})
                    except Hold:
                        self.send_error(400)
                        return
                    self.send_response(reply.status)
                    for key, value in reply.headers:
                        self.send_header(key, value)
                    self.end_headers()
                    self.wfile.write(reply.body)
                    self.wfile.flush()
                    self.close_connection = True

                def log_message(self, *_args):
                    pass

            # An access denial propagates. No escalation, alternate bind, or fallback.
            self.server = HTTPServer(("127.0.0.1", 0), Handler)
            self.server.timeout = REQUEST_SECONDS
            self.thread = threading.Thread(target=self.server.serve_forever, kwargs={"poll_interval": 0.02}, daemon=True)
            self.thread.start()

    def resource(self, case: str) -> str:
        if self.mode == "http":
            return f"http://127.0.0.1:{self.server.server_port}/{case}/visitor-card.txt"
        return f"fixture://{case}/visitor-card.txt"

    def get(self, case: str, phase: str, headers: dict[str, str]) -> Reply:
        require(self.count < MAX_REQUESTS and time.monotonic() < self.deadline, "run_limit")
        self.count += 1
        if self.mode == "in-process":
            return fixture(case, phase, {k.lower(): v for k, v in headers.items()})
        connection = http.client.HTTPConnection("127.0.0.1", self.server.server_port, timeout=min(REQUEST_SECONDS, max(0.01, self.deadline - time.monotonic())))
        try:
            connection.request("GET", f"/{case}/visitor-card.txt", headers=headers)
            response = connection.getresponse()
            try:
                body = response.read(MAX_BYTES + 1)
            except http.client.IncompleteRead as error:
                body = error.partial
            require(len(body) <= MAX_BYTES, "response_size_limit")
            return Reply(response.status, tuple(response.getheaders()), body)
        finally:
            connection.close()

    def close(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.thread.join(timeout=REQUEST_SECONDS)


def framing(reply: Reply) -> int:
    require(reply.one("Transfer-Encoding") is None, "unsupported_transfer_encoding")
    require(reply.one("Content-Encoding") in (None, "identity"), "changed_content_encoding")
    require(not (reply.one("Content-Type") or "").lower().startswith("multipart/"), "unsupported_multipart")
    value = reply.one("Content-Length")
    require(value is not None and re.fullmatch(r"[0-9]+", value) is not None, "missing_or_invalid_length")
    length = int(value)
    require(length <= MAX_BYTES and len(reply.body) <= MAX_BYTES, "response_size_limit")
    return length


def promote(candidate: Path, final: Path, contract: dict) -> None:
    actual = candidate.read_bytes()
    require(len(actual) == contract["length"], "full_length_mismatch")
    require(digest(actual) == contract["sha256"], "full_digest_mismatch")
    # Atomic no-clobber publication on this same filesystem. Never replace an
    # existing name. No fallback on unsupported filesystems.
    try:
        os.link(candidate, final)
    except FileExistsError as error:
        raise Hold("destination_exists") from error
    require(final.read_bytes() == actual, "published_readback_mismatch")
    candidate.unlink()


def recover(case: str, transport: Transport, directory: Path, contract: dict, metadata: dict) -> str:
    partial = directory / "original.part"
    before = partial.read_bytes()
    require(metadata.get("identity") == contract["identity"], "missing_or_changed_identity_binding")
    require(metadata.get("resource") == transport.resource(case), "resource_identity_conflict")
    require(metadata.get("selectors") == SELECTORS, "changed_request_selectors")
    require(metadata.get("partial_sha256") == digest(before), "partial_changed_since_receipt")
    require(metadata.get("partial_length") == len(before) <= contract["length"], "partial_length_conflict")
    headers = dict(SELECTORS)
    resumable = strong_etag(metadata.get("etag"))
    if resumable:
        headers.update({"Range": f"bytes={len(before)}-", "If-Range": metadata["etag"]})
    reply = transport.get(case, "recover", headers)
    (directory / "response.json").write_text(json.dumps({"status": reply.status, "request": headers, "headers": reply.headers, "body_length": len(reply.body)}, indent=2) + "\n")
    (directory / "received.body").write_bytes(reply.body)
    length = framing(reply)
    require(len(reply.body) == length, "truncated_or_misframed_body")
    if reply.status == 200:
        require(reply.one("Content-Range") is None, "unexpected_content_range_on_200")
        require(length == contract["length"], "full_response_length_conflict")
        candidate_bytes, outcome = reply.body, "restarted_full"
    elif reply.status == 206:
        require(resumable, "unsolicited_206")
        # This fixture contract requires a repeated strong ETag; a general client
        # can use other adequately evidenced response/selection bindings.
        require(strong_etag(reply.one("ETag")) and reply.one("ETag") == metadata["etag"], "response_validator_conflict")
        match = re.fullmatch(r"bytes ([0-9]+)-([0-9]+)/([0-9]+)", reply.one("Content-Range") or "")
        require(match is not None, "invalid_or_unknown_content_range")
        start, end, total = map(int, match.groups())
        require(start == len(before) and start <= end < total, "range_start_or_bounds_conflict")
        require(total == contract["length"] and end == total - 1, "range_end_or_total_conflict")
        require(length == end - start + 1, "range_body_length_conflict")
        candidate_bytes, outcome = before + reply.body, "resumed"
    elif reply.status == 416:
        require(resumable and reply.one("ETag") == metadata["etag"], "416_identity_conflict")
        require(reply.one("Content-Range") == f"bytes */{contract['length']}", "416_total_conflict")
        require(len(before) == contract["length"], "416_does_not_prove_completion")
        candidate_bytes, outcome = before, "verified_complete_partial"
    else:
        raise Hold("unexpected_status_" + str(reply.status))
    require(partial.read_bytes() == before, "partial_changed_during_recovery")
    candidate = directory / "candidate.bin"
    with candidate.open("xb") as stream:
        stream.write(candidate_bytes)
        stream.flush()
        os.fsync(stream.fileno())
    promote(candidate, directory / "visitor-card.txt", contract)
    return outcome


def run(mode: str, parent: Path) -> tuple[Path, dict]:
    require(parent.is_dir(), "output_parent_must_exist")
    output = Path(tempfile.mkdtemp(prefix="download-recovery-", dir=parent))
    contract = {"identity": "fictional-cedar-card/revision-1/identity", "length": len(PAYLOAD), "sha256": digest(PAYLOAD), "digest_provenance": "Original fixture bytes defined in this script; byte-equivalence control, not proof of a publisher's authenticity."}
    (output / "contract.json").write_text(json.dumps(contract, indent=2) + "\n")
    transport = Transport(mode)
    results = []
    try:
        for case in CASES:
            directory = output / case
            directory.mkdir()
            seed = transport.get(case, "seed", dict(SELECTORS))
            require(seed.status == 200 and framing(seed) == contract["length"], "bad_seed")
            partial = directory / "original.part"
            partial.write_bytes(seed.body)
            metadata = {"identity": contract["identity"], "resource": transport.resource(case), "selectors": dict(SELECTORS), "etag": seed.one("ETag"), "partial_length": len(seed.body), "partial_sha256": digest(seed.body), "seed_status": seed.status, "seed_declared_length": framing(seed), "seed_observed_length": len(seed.body)}
            if case == "missing_binding":
                metadata.pop("identity")
            if case == "changed_partial":
                partial.write_bytes(b"X" + seed.body[1:])
            (directory / "receipt.json").write_text(json.dumps(metadata, indent=2) + "\n")
            preserved = partial.read_bytes()
            final = directory / "visitor-card.txt"
            sentinel = b"Existing destination: preserve me.\n"
            if case == "destination_exists":
                final.write_bytes(sentinel)
            try:
                outcome = recover(case, transport, directory, contract, metadata)
                reason = None
            except Hold as error:
                outcome, reason = "held", str(error)
            expected = SUCCESS.get(case, "held")
            final_bytes = final.read_bytes() if final.exists() else None
            checks = {
                "expected_outcome": outcome == expected,
                "partial_preserved": partial.read_bytes() == preserved,
                "final_bytes": final_bytes == (sentinel if case == "destination_exists" else PAYLOAD if case in SUCCESS else None),
            }
            results.append({"case": case, "outcome": outcome, "reason": reason, "checks": checks})
    finally:
        transport.close()
    report = {"transport": "actual HTTP/1.1 over IPv4 loopback" if mode == "http" else "in-process response objects; no sockets or HTTP exchange", "python": __import__("sys").version.split()[0], "contract": contract, "limits": {"response_bytes": MAX_BYTES, "requests": MAX_REQUESTS, "run_seconds": RUN_SECONDS, "request_seconds": REQUEST_SECONDS, "retries": 0}, "request_count": transport.count, "case_count": len(results), "all_passed": all(all(row["checks"].values()) for row in results), "cases": results}
    (output / "results.json").write_text(json.dumps(report, indent=2) + "\n")
    return output, report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", required=True, choices=("http", "in-process"))
    parser.add_argument("--output-parent", required=True, type=Path, help="Existing approved directory; a fresh private child is created")
    args = parser.parse_args()
    try:
        output, report = run(args.mode, args.output_parent)
    except (OSError, Hold, http.client.HTTPException) as error:
        print(json.dumps({"status": "blocked", "reason": str(error), "no_automatic_fallback": True}))
        return 2
    print(json.dumps({"output": str(output), "all_passed": report["all_passed"], "cases": report["case_count"], "transport": report["transport"]}))
    return 0 if report["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
