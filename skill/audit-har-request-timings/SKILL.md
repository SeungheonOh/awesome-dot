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

## Output

A source-scoped timing summary, request/phase table, concurrency/idle measures and discrepancies, with source content and sensitive fields excluded as specified.

## Verification and limits

Check nested intervals, equal endpoints, missing phases, SSL/connect inclusion, invalid times and phase-total mismatches. Reconcile selected request count and explain excluded records.
