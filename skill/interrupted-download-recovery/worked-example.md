# A Visitor Card Recovered From an Interrupted Transfer

This example was executed on 2026-10-02 with CPython 3.12.14. The actual HTTP run and a separate in-process run both passed 25 fixture cases. Each made 48 fixture requests: two cases were held after their original receipt was found missing or inconsistent, before issuing a recovery request.

The useful output is the [recovered fictional visitor card](examples/visitor-card.recovered.txt), a 227-byte UTF-8 file. The [preserved interrupted prefix](examples/visitor-card.original.part) contains 67 bytes. These are original practice bytes with no real booking, account or personal data.

## The supplied contract

The [contract](examples/contract.json) pins revision 1, identity coding, 227 bytes and SHA-256:

```text
7d8d90b25ff4dcb10ea245210102d157bf045ca77d74e32b3e26a0346b855bfa
```

The checksum is computed from the original in-memory fixture definition, outside the transfer, and is used as the controlled test's expected byte value. It does not authenticate a real publisher. The original transfer receipt records the exact fixture resource, request selectors, response ETag, and observed prefix size/hash.

## What actually crossed HTTP

The HTTP mode used the standard-library HTTP client and a short-lived HTTP/1.1 server bound only to IPv4 loopback. Its initial GET declared the full 227 bytes, sent 67 bytes, and closed. The next GET went to the same case-specific resource with these selectors and conditions:

```text
Accept: text/plain
Accept-Encoding: identity
Range: bytes=67-
If-Range: "cedar-card-v1"
```

The successful response was 206 with the matching strong ETag, `Content-Range: bytes 67-226/227`, `Content-Length: 160`, and 160 observed body bytes. See the [captured response evidence](examples/resume-response.json).

The helper combined a copy of the 67-byte prefix with the verified 160-byte suffix in a fresh candidate. It reopened and hashed all 227 candidate bytes, confirmed the original partial stayed unchanged, published with no-overwrite hard-link creation, and reread the final. The final bytes equal the supplied contract. The successful candidate name was then removed; the original partial remained.

The server served only constants defined in the script, never files from a directory. No external service, TLS connection, browser, account, credential, proxy or install was involved. This is an actual loopback HTTP transfer test, not evidence about a production provider or internet failure behavior.

## Branches exercised

| Fixture change | Observed result |
| --- | --- |
| Valid suffix response | Recovered from the preserved prefix plus suffix |
| Range ignored with a full 200 | Restarted from the full body, without prefix duplication |
| Weak ETag or no validator on the initial receipt | Made a complete GET without Range/If-Range; recovered the matching full bytes |
| Full 200 contains revision 2 with the same length | Held on full digest mismatch |
| Incorrect start, end or total; unknown total | Held before combining |
| Different, absent or weak ETag on 206 | Held under the fixture's explicit repeated-strong-validator contract |
| Truncated 206, truncated 200, or wrong Content-Length | Held on observed body-length mismatch |
| Correct ranges but altered suffix bytes | Held on full-file digest mismatch |
| Complete partial followed by consistent 416 | Verified the complete partial and published a copy |
| Short partial followed by 416, or conflicting 416 total | Held; 416 did not establish completion |
| Changed content coding, duplicate Content-Range, multipart response | Held as unsupported/ambiguous under this narrow contract |
| Missing receipt identity or modified local partial | Held before the recovery request |
| Final filename already exists | Held; the existing sentinel file and original partial stayed byte-identical |

The complete-416 cases deliberately request past the final byte to test that branch. In ordinary work, a receipt-bound complete partial can first be verified locally without making that request. The helper is a small explicit fixture demonstration, not a generic download utility.

The full [HTTP results](examples/http-results.json) and [in-process results](examples/in-process-results.json) retain the case-by-case outcome, hold reason and preservation checks. All 25 cases passed all three recorded checks: expected outcome, preserved partial and exact expected final-file state. A held case with an existing destination is successful test behavior; it does not mean the download was recovered.

## Independent changed-input check

A separate [16-case harness](scripts/review_changed_inputs.py) uses a newly written 151-byte UTF-8 meadow card, different validators, different cut points and independently supplied response objects. All 16 cases passed; see [the result JSON](examples/changed-input-results.json). This coverage is in-process only, with no HTTP framing or network claim.

The principal prefix is 43 bytes and ends inside the two-byte character `é`. Byte-based recovery produces the [complete readable meadow card](examples/meadow-card.recovered.txt), whose SHA-256 is `2731c71e2edef5ebfe220ea5d51b800e5171e9c81588ef0304e5032ffbf3ee27`. This demonstrates why offsets must count bytes rather than decoded characters. Empty-prefix and one-byte-suffix cases also recover exactly. Corruption, receipt mismatch, duplicate Content-Length, a changed validator/coding, truncation, and an occupied final name hold the result while preserving the inputs. A shorter otherwise valid range is held under the helper's full-suffix constraint.

From this skill directory, after inspecting both scripts, reproduce the changed-input check with:

```sh
python scripts/review_changed_inputs.py --skill-dir . --output-parent /approved/existing/private/directory
```

This harness uses only tiny fictional in-memory responses and fresh local files. It imports the reviewed helper from the chosen skill directory, makes at most one recovery call per case, and does not start a listener. Its recorded helper digest before and after execution is unchanged. Neither controlled fixture's checksum is a real publisher-authenticity claim.

## Additional readback

A further inspected in-process run reproduced the saved 25-case ledger exactly. Seven new response-object cases checked suffix recovery, a full restart, an unsolicited 206 after a weak receipt, range metadata on a 200, duplicate content coding, changed 416 identity and a corrupt complete partial. Expected outcomes and original-byte preservation passed. The two saved cards and the supplied interrupted prefix were also checked against their stated identities. These added cases exercised response processing and local files; the actual HTTP evidence remains the separately recorded loopback runs above.

## Reproduce within an approved destination

From this skill directory, inspect `scripts/rehearse_recovery.py`, then choose one mode:

```sh
python scripts/rehearse_recovery.py --mode http --output-parent /approved/existing/private/directory
python scripts/rehearse_recovery.py --mode in-process --output-parent /approved/existing/private/directory
```

The output parent must already exist. A new private child receives the contract, per-case original partial, receipt, actual received body, response metadata, candidate or final file, and `results.json`. The script prints that new location. No existing parent contents are replaced. Keep the run for review; the script does not clean it up.

The fixed suite has 25 cases, a 64-request cap, a 4,096-byte response-body cap, a 20-second request-admission window, 2-second network-operation timeout and zero retries. The server closes in the helper's cleanup path. A bind/access denial produces a blocked result with no automatic retry or transport substitution. In-process mode never binds a socket and proves only the response-processing logic and local file operations.

The example requires an installed Python 3.12+ and a filesystem supporting same-filesystem hard links. It intentionally does not implement chunked encoding, compressed representations, multipart ranges, strong-date validators, redirects, automatic retries or arbitrary URLs. Full expected length, full expected digest and a repeated matching strong ETag for resumed responses are part of this supplied fixture contract. Do not treat its conservative holds as a complete HTTP conformance judgment.

## Implementation references

- [RFC 9110: If-Range](https://www.rfc-editor.org/rfc/rfc9110.html#section-13.1.5), [Content-Range](https://www.rfc-editor.org/rfc/rfc9110.html#section-14.4), and [416](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.5.17)
- [RFC 9112: message completeness](https://www.rfc-editor.org/rfc/rfc9112.html#section-8)
- [Python HTTP client response APIs](https://docs.python.org/3.12/library/http.client.html#httpresponse-objects) and [in-memory request handler base](https://docs.python.org/3.12/library/http.server.html#http.server.BaseHTTPRequestHandler)
- [Python private temporary directories](https://docs.python.org/3.12/library/tempfile.html#tempfile.mkdtemp) and [hard-link creation](https://docs.python.org/3.12/library/os.html#os.link)
