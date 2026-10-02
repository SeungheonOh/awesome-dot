---
name: local-har-timing-workbench
description: Build a local-only HAR timing inspector with request waterfalls, overlap-aware metrics, and allowlist-only evidence exports. Use when developing a network-recording analysis tool, rather than diagnosing a live endpoint without a capture.
---

# Local HAR timing workbench

Turn an HTTP Archive into inspectable timing evidence without requiring the user to upload a capture. The distinct challenges are overlapping intervals, incomplete timing fields, nested TLS time, and sensitive content embedded throughout HAR files.

## Inputs and boundaries

Use a synthetic HAR while building. A real capture requires the user's authorization to read it; never fetch the URLs found inside it. A HAR can contain session cookies, authorization headers, signed URLs, request bodies and private responses. Publishing the app does not authorize publishing a capture. Keep product code and fixtures outside a skills-only contribution repository.

Read the [HAR 1.2 timing specification](https://github.com/ahmadnassri/har-spec/blob/master/versions/1.2.md). The implementation must decide what to do with unavailable timings rather than silently treating every missing value as measured zero.

## Build in this order

1. Define the information boundary before the interface. Construct a small working model containing opaque request/origin aliases, timing numbers, method/status, known body size, and booleans recording presence of potentially sensitive fields. Do not retain URLs, headers, cookies or payloads in that model. Use text nodes for all dynamic labels. Do not log input data.
2. Bound parsing before JSON decoding. An example implementation caps inputs at 8 MiB and 10,000 entries. Require explicit timezone-bearing timestamps, finite nonnegative durations, and a nonempty entry array. Report the specific bad entry. Reject unsupported input without erasing the last valid capture. Skip non-HTTP(S) resources with a visible count.
3. Normalize timings into known numbers or unavailable values. Sum blocked, DNS, connect, send, wait and receive. TLS is a subset of connect, not an additional phase. Keep it as a separate detail. Preserve unknown body size and status instead of interpreting them as zero bytes or success.
4. Compare the phase sum with the recorded duration using a documented tolerance. One useful tolerance is the larger of 1 ms or 1%. On mismatch, render a neutral duration bar and show the supplied phase values separately; never manufacture a missing phase or rescale numbers to appear consistent.
5. Compute interval evidence independently of phase sums. Recorded span is latest end minus earliest start. Busy time is the union of request intervals; idle time is span minus that union. Peak concurrency is a sweep over starts and ends. Process ends before starts at equal timestamps and exclude zero-duration intervals from concurrency. Sum of durations is request-time, not elapsed page-load time.
6. Build a waterfall with relative starts and recorded durations, a phase legend, request detail, page/origin filters and a failed-status filter. Paginate large recordings; reset pagination on every filter change. Alias page labels too. Explain that origins are numbered independently in each capture, and that a long tail does not establish rendering dependency or server causation.
7. Protect asynchronous import. Give each file selection a generation number. A later example, clear action or file selection invalidates earlier reads; a slow old file cannot replace the current view. Keep parsing errors visible and preserve the valid prior state.
8. Export by building a fresh allowlisted object, never by deleting selected keys from the original HAR. Include relative offsets, numeric phases, statuses and summary evidence. Exclude original identifiers, absolute dates, headers and payloads. Call it a summary, not a sanitized HAR. Timing/status information may still be sensitive; ask the user to review before sharing.
9. Keep the app local-only: no fetches, analytics, remote fonts or persistent browser storage. A restrictive content-security policy with `connect-src 'none'` helps enforce that design. If a later feature needs network access, treat it as a separate scope change rather than quietly weakening the promise.

## Rehearsal and checks

A worked build, Trace Loom, used a 22-request synthetic capture with two origin aliases, one HTTP 503, overlapping requests, a long wait, and deliberate fake authorization/query/body strings. The example was visibly labeled synthetic; no real capture was used.

The pure model tests checked:
- TLS does not increase the phase sum twice
- Unavailable phases remain unavailable, and mismatches are flagged
- Intervals [0,10), [5,15), [30,40) give 25 ms busy and 15 ms idle
- Adjacent intervals [0,10), [10,20) have peak concurrency one
- Two hundred seeded interval sets match an independent discrete-time union/concurrency oracle
- Export contains none of the fake hostnames, paths, authorization fields, query values, response body text or absolute dates
- Malformed JSON, null entries, timezone-free timestamps, oversized files and negative durations are rejected

The simulated-DOM tests checked example labeling, request detail, filters, download contents, clear, slow-import supersession, failed import preserving prior data, and pagination across 222 requests. These passed on the worked implementation. Its real-browser visual inspection was not completed; simulated DOM tests do not establish responsive layout or accessibility quality.

For a new implementation, run its model and interaction tests, then inspect actual desktop and phone-width rendering when the authorized browser supports that workflow. Verify keyboard operation and download bytes. Do not claim these later checks passed merely because the worked example passed its own tests.

## Completion

Deliver the local artifact or an explicitly authorized deployment, with test results and remaining verification limits. Keep original captures private. A skill-only contribution should contain this reusable workflow, not the product bundle or synthetic test files. Stop at an input/access limitation rather than claiming a capture proves an endpoint or server is at fault.
