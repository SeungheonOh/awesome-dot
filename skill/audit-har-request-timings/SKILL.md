---
name: audit-har-request-timings
description: "Analyze an authorized HAR locally for request phases, overlaps and idle intervals while minimizing sensitive request content."
---

# Audit HAR request timings

## When to use

A page-load investigation needs timing evidence without sending browser headers, cookies, URLs or bodies to another service.

## Required inputs

- The bounded authorized HAR and relevant page/request scope
- Which identifiers may be retained or replaced by local aliases
- The performance question and output audience

## Workflow

1. Preserve the original. Parse bounded HAR entries and validate dates/durations. Keep missing phase values unknown rather than zero. Avoid carrying headers, cookies, query strings and bodies into the timing model when unnecessary.
2. Alias request, origin and page identifiers consistently within the selected file. Aliases preserve correlation but do not make timing metadata anonymous.
3. Interpret HAR phases carefully: SSL commonly sits inside connect and must not be added twice. Compare phase totals with reported duration; disclose inconsistencies rather than scaling them away.
4. Calculate interval unions for busy time and gaps, and sweep starts/ends for peak concurrency under a declared endpoint convention. Sum of request durations is not elapsed page-load time.
5. Report slow phases, concurrent clusters and gaps with exact request aliases and times. Do not infer server causality or user-perceived completion from timing alone. Export only approved metadata.

### Reconcile phases and elapsed time

Create a timing-only projection before analysis, retaining an occurrence identifier for each selected entry. Keep unknown phases distinct from measured zero and count records excluded for invalid intervals. If a request contains duplicate-looking URLs, retain each occurrence; retries are separate timing evidence.

For a request from 0 to 120 ms with connect 40 ms including SSL 20 ms, do not sum connect and SSL as independent durations. When phase totals still disagree with reported duration, preserve both and mark the mismatch. Avoid deriving a server bottleneck solely from a client waiting phase without corroboration.

## Output

A source-scoped timing summary, request/phase table, concurrency/idle measures and discrepancies, with source content and sensitive fields excluded as specified.

## Verification and limits

Check nested intervals, equal endpoints, missing phases, SSL/connect inclusion, invalid times and phase-total mismatches. Reconcile selected request count and explain excluded records.

## Privacy review before export

Request aliases can still reveal a sequence of user activity when combined with times. Keep the approved audience and correlation scope explicit. A timing report is minimized evidence, not anonymous data by definition.

## Worked example

Three fictional request intervals are R1=[0, 100)ms, R2=[20, 60)ms and R3=[150, 200)ms. Their duration sum is 190 ms, but the interval union is 150 ms and the enclosing elapsed window is 200 ms. The gap is 50 ms from 100 to 150; peak concurrency is 2.

R2 is nested inside R1, so adding durations would overstate busy elapsed time. A start exactly when another request ends does not overlap under the stated half-open convention.

The report uses aliases and includes intervals/phase evidence only. It does not export original query strings, headers or bodies, and does not identify the 50 ms gap as server failure without additional evidence.

## Evidence status

The worked example illustrates the stated inputs and reasoning. Unless an execution result is explicitly identified, it is not a claim that external services, real devices or user data were tested. Report actual checks and unrun stages on each use.
