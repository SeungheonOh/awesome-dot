---
name: interrupted-download-recovery
description: "Recover a bounded interrupted file download into a new verified copy by binding the partial to its HTTP representation, checking range responses, and safely restarting or holding when identity is uncertain."
---

# Recover the Right Bytes After a Download Stops

Produce a usable recovered file and a short account of which bytes were reused, what was downloaded, and why the final copy passed. Preserve the original partial and any existing destination. A progress bar reaching 100%, a matching filename, or an HTTP success status is insufficient.

Use for a selected interrupted ordinary file transfer. This checks representation continuity and transfer completeness; it does not test historical backup recovery, package project dependencies, or establish account-export coverage. Keep executable installation, account changes, bulk crawling and download-manager configuration outside the task.

## Establish the file and the acceptance contract

Resolve these from the user's request, original download receipt and available metadata:

- The exact authorized resource, requested version or “current version,” original effective URL after any redirects, and the request selectors that chose the bytes: content coding, relevant `Vary` headers, language/media type, and account context where applicable
- The existing partial's identity, actual byte count, recorded prefix digest and original response metadata, including validator and expected total size. Record what was captured during the original transfer versus learned afterward
- The approved private output directory, whether it syncs or is shared, and the intended final filename. Prepare in a fresh child on the same filesystem as the final output
- The accepted expected length and, when supplied, whole-file digest, algorithm and provenance. A provider checksum retrieved alongside the file supports consistency, not independent authenticity. A locally computed checksum identifies bytes but is not an external baseline
- A file-size ceiling, request/time budget, retry limit, free-space allowance and whether a full restart is within the requested scope. Reserve room for the preserved partial, received segment and complete candidate

An explicit request to recover this file into this destination authorizes the needed bounded reads, fresh candidate writes and verified publication there. It does not authorize replacing existing files, opening downloaded executables, uploading private data, creating credentials, changing access or installing tools. Use existing supported access. Stop on an access denial or browser security warning rather than altering settings or finding a bypass. Keep signed URLs, cookies and tokens out of reports.

Make the acceptance level explicit. If an expected checksum exists, it must match before declaring the requested bytes recovered. If none exists, a completed transfer can be reported under an agreed narrower contract with its observed digest; do not relabel that digest as publisher verification. If the requested historical version or the partial's lineage cannot be established, preserve it and hold reuse. A separately authorized full download may still be useful.

## 1. Bind the partial to the selected representation

Read and hash the actual partial without editing it. Match its length and digest to the original receipt. A newly fetched ETag, filename, URL alone, timestamp or same total size does not establish that the stored prefix came from that representation.

For resumable identity, use a valid strong ETag recorded with the partial and the same effective resource and representation selectors. Do not invent a validator or strip `W/` from a weak one. Weak ETags cannot be used in `If-Range`; an HTTP date is allowed there only under the RFC's strong-date conditions when no entity tag exists. Prefer a complete fresh retrieval if those conditions are not evidenced. See [RFC 9110 §13.1.5](https://www.rfc-editor.org/rfc/rfc9110.html#section-13.1.5).

Preserve content coding. A byte offset refers to the transferred representation, so a decompressed partial cannot be joined to an encoded response. For an identity-coded original, request `Accept-Encoding: identity` and confirm the returned coding; that request is not a guarantee. If the earlier bytes were compressed, use an existing client that preserves and validates the exact coded representation or restart under a newly recorded representation contract. Do not mix byte spaces.

Classify the starting point:

| Starting evidence | Operation |
| --- | --- |
| Bound partial, strong validator, size below expected total | Request one suffix with `Range: bytes=N-` and `If-Range: <recorded strong ETag>` |
| Bound partial, weak/no validator | Preserve it; perform an authorized complete GET into a fresh candidate without Range/If-Range |
| Missing or conflicting partial binding | Hold reuse. Obtain the missing original receipt or agree to a separately verified full restart |
| Partial already equals expected length | Verify the whole partial against the contract; no request is necessary merely to rename it |
| Partial exceeds expected size, changed since receipt, or belongs to another coding/version | Hold; do not truncate, append, or choose a same-named replacement |

`Accept-Ranges` is a hint, not evidence that a particular resume succeeded. A server may ignore a Range request. Keep all original bytes untouched while evaluating the actual response. See [RFC 9110 §14.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-14.2).

## 2. Validate the response before combining bytes

Use an installed transfer API that exposes status, response headers and raw representation bytes. Record the requested range, response status, content range, validator, coding, declared length and actual body count. For one small task, a single suffix request avoids unnecessary multipart complexity. Reject malformed or ambiguous critical metadata; do not guess which duplicate header to trust.

Apply these branches:

| Response | Required action |
| --- | --- |
| `206 Partial Content` | Confirm the same representation, the exact requested start, valid inclusive bounds, a consistent total, and a body count of `end - start + 1`. If `Content-Length` exists, it must agree with that segment length. Only then combine a copy of the preserved prefix and suffix |
| `200 OK` after Range | Treat the body as a complete replacement candidate beginning at byte zero. Never append it. Check the full contract; a changed version may require a user decision even if the new file opens |
| `416 Range Not Satisfiable` | Treat it as diagnostic, not completion. A `bytes */L` response can support a known total. Promote a copy of the partial only if its identity, complete length and full acceptance checks independently pass |
| Truncated body, invalid range, conflicting validator/coding/total | Preserve the partial and isolated received bytes; hold this candidate |
| Redirect, authentication challenge, rate limit, other error | Stop this attempt and report it. Re-evaluate any changed destination/access within authorization; do not forward credentials or silently follow a different source |

These branches follow [RFC 9110 §§14.4, 15.3.7 and 15.5.17](https://www.rfc-editor.org/rfc/rfc9110.html#section-14.4). The conservative single-suffix example below additionally requires a known total, the suffix through the final byte, a repeated matching strong ETag on resumed responses, and ordinary Content-Length framing. These are its acceptance constraints, not claims that other RFC-valid responses are invalid. A shorter valid segment needs a separately bounded continuation plan; it is not a completed download.

Count bytes actually returned. EOF, a timeout or an exception can leave a shorter body than advertised. An HTTP/1.1 message cut short under its framing is incomplete; saving its partial bytes does not make it complete. See [RFC 9112 §§6.3 and 8](https://www.rfc-editor.org/rfc/rfc9112.html#section-6.3). Do not assume a chunked read API will always raise for every truncation. Verify the observed count and final contract yourself.

## 3. Verify and publish one candidate

Write the candidate exclusively in the fresh run directory. For a successful resume, copy the preserved prefix and append only the validated suffix to that new file. For a 200 restart, write only the full response. Keep candidates separate from any previous final result.

Before publication:

1. Close/flush the completed candidate, reopen it, and read the entire file to calculate its size and whole-file digest
2. Compare these with the accepted expected values and with the download-time count/digest where available. A valid suffix cannot repair an already-corrupt prefix
3. Re-read the original partial's size/digest and confirm it remained unchanged during recovery
4. Check the final destination is still in scope. Use an atomic no-overwrite publication primitive supported on that filesystem. A prior “does not exist” check alone leaves a race
5. Reopen the published final and confirm the same full size/digest. Only now call the copy recovered

Do not use `os.replace` casually: it can silently replace an existing file. The bundled POSIX-oriented rehearsal instead creates the final directory entry using `os.link(candidate, final)` on the same filesystem, which fails when the name already exists, verifies readback, and removes only its generated candidate name. It retains the original partial and failed candidates. This is atomic visibility of an already-written file, not a claim of universal crash durability or support on every filesystem. See [Python `os.link` and `os.replace`](https://docs.python.org/3.12/library/os.html#os.link).

If the platform lacks a suitable no-overwrite primitive, retain the verified candidate and report publication pending. Do not switch to a weaker overwrite-prone method. Ordinary file reading should not execute the download; a simple UTF-8 decode can establish readability for a text fixture but not truth or completeness of its subject matter.

## 4. Stop conditions and the handoff

Set limits before the first request. A sensible small-file recovery might allow one resume plus one authorized full restart, a short per-request timeout and a fixed overall budget. Do not reset the budget on each retry. After a timeout or uncertain publication, inspect the exact candidate and destination before repeating anything. A changed representation, repeated failure, authorization problem, exhausted budget or unverified final is a reason to stop and return evidence.

Return:

```text
Requested resource/version and acceptance contract; checksum provenance
Original partial length/digest and representation binding
Action: resumed / restarted full / verified existing complete / held
Transfer: status; requested and received byte intervals; actual body count
Final: destination; full readback length/digest; contract comparison
Preservation: original partial and any existing destination unchanged
Limits used; retries; failed candidates; exact unresolved decision
Scope: actual HTTP exchange or in-process test, and untested properties
```

Keep failed copies visibly distinct from usable output. Do not delete real partials or leftovers automatically. A report that merely says “retry with resume” is not the completed operation.

## Reproducible fictional example

Read [the worked example](worked-example.md) for actual evidence and the recovered visitor card. The [standard-library rehearsal](scripts/rehearse_recovery.py) accepts no URLs, account data, external endpoints or file-serving roots. It has two explicit modes:

```sh
python scripts/rehearse_recovery.py --mode http --output-parent /approved/existing/private/directory
python scripts/rehearse_recovery.py --mode in-process --output-parent /approved/existing/private/directory
```

Inspect the helper before running it. HTTP mode temporarily binds only `127.0.0.1` and serves tiny original in-memory fixtures; no directory is exposed. In-process mode uses response objects and opens no socket. Neither silently substitutes for the other. If a listener is denied, honor that denial, report HTTP untested, and use in-process testing only when that separate local simulation is permitted. Do not escalate or expose the listener.

Each mode creates a fresh private child directory, uses 25 fixed cases, at most 64 requests, at most 4,096 body bytes per response, a 20-second request-admission window, a 2-second network timeout per operation and no automatic retries. Its fixed fixtures finish promptly; the timeout is not a general absolute wall-clock deadline against an untrusted slow server. It leaves all generated evidence for review. No installs, accounts, browser actions or network/security changes are required.

## Example request

```text
Recover this interrupted visitor-card download into a new private folder.
Use the original receipt and supplied full-file size/checksum as the acceptance
contract. Reuse the partial only if its representation is still identifiable.
A full restart is okay within the stated size and request budget. Preserve
the partial and any existing file; show the verified final copy and any holds.
```
