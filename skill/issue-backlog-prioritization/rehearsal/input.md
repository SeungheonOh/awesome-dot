# Fictional backlog decision packet

All records and roles are fictional. Snapshot: 2026-10-01T12:00:00Z. Prepare a private importance comparison and identify work that can start. Do not edit a tracker, assign anyone, or change dependency links.

Use this endorsed rubric exactly: score = 3 × impact + 2 × urgency − effort. Impact is an integer 1–5, urgency an integer 0–3, and effort an integer 1–8; these are ordinal rubric points, not durations. Higher final score means greater importance. No tie-breaker is approved. A missing criterion retains its full permitted scale; no other information bounds it.

Only gate=pass items are eligible for the importance comparison. gate=fail is excluded, and gate=unknown remains unresolved, regardless of apparent score. Readiness also requires gate=pass and every hard prerequisite completed. A completed issue is not a candidate for new work. Do not treat a task as complete because it has no prerequisites.

All supplied issues are open, with no additional readiness conditions. X-90 is named only as a hard prerequisite; its record is absent and there is no authority to look outside this packet. Similar names are not evidence of duplicate work.

## Source records

| Source | Issue | Short description | Version | Gate | Impact | Urgency | Effort | Hard prerequisites |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| R1 | Q-11 | Reconcile imported totals | 3 | pass | 5 | 2 | 3 | Q-12 |
| R2 | Q-12 | Record import ownership | 2 | pass | 1 | 0 | 1 | none |
| R3 | Q-13 | Explain unmatched rows | 7 | pass | 4 | 1 | unknown | none |
| R4 | Q-14 | Add export completion notice | 4 | pass | 3 | 3 | 3 | none |
| R5 | Q-15 | Preserve export selection | 2 | pass | 4 | 2 | 4 | none |
| R6 | Q-16 | Add partner-only fields | 1 | fail | 5 | 3 | 1 | none |
| R7 | Q-17 | Add optional record enrichment | 5 | unknown | 5 | 3 | 2 | none |
| R8 | Q-18 | Validate handoff naming | 2 | pass | 2 | 1 | 1 | Q-19 |
| R9 | Q-19 | Finalize naming dependencies | 2 | pass | 2 | 0 | 2 | Q-18 |
| R10 | Q-20 | Add reconciliation summary | 3 | pass | 3 | 2 | 5 | X-90 |
| R11 | Q-13 | Explain unmatched rows | 7 | pass | 4 | 1 | unknown | none |

R11 repeats R3 from a second export; it is the same issue and version, with identical content. The gate for Q-16 failed because the proposed fields are outside the approved project scope; do not broaden the project. Q-17's gate awaits a recorded source-use decision; do not infer pass or fail.

Deliver a source-linked per-issue table, known-score tiers and any unresolved comparisons, readiness separate from importance, and the smallest useful next questions. State whether a unique highest-importance item that can start is supported by this packet. A low-scoring prerequisite may be useful next work, but do not add a dependency bonus or overwrite its score.
