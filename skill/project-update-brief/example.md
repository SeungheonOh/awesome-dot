# Worked example: a mixed-state portal update

All records are fictional. Prepare a private update under 180 words for the Partner Portal project lead. The reporting window is October 2–8, 2026, with a cutoff of October 8 at 12:00 UTC. The supplied rule calls a workstream update stale after seven calendar days.

## Inputs

```json
{
  "as_of": "2026-10-08T12:00:00+00:00",
  "reporting_start": "2026-10-02",
  "reporting_end": "2026-10-08",
  "timezone": "UTC",
  "stale_after_days": 7,
  "word_limit": 180,
  "sources": [
    {"id": "P0", "recorded_at": "2026-10-01T10:00:00+00:00", "workstream": "preview", "kind": "previous brief", "text": "The preview is blocked by sample-data approval."},
    {"id": "S1", "recorded_at": "2026-10-06T10:00:00+00:00", "event_date": "2026-10-06", "workstream": "preview", "kind": "approval and demo record", "text": "Sample data approved. The preview demo is available in the approved review environment."},
    {"id": "S2", "recorded_at": "2026-10-07T11:00:00+00:00", "event_date": "2026-10-07", "workstream": "export", "kind": "change and test record", "text": "Export change r42 merged. At r42, 18 of 20 checks passed; two custom-column checks failed. No release record is supplied.", "revision": "r42", "passed": 18, "total": 20, "failed": 2},
    {"id": "S3", "recorded_at": "2026-09-29T09:00:00+00:00", "event_date": "2026-09-29", "workstream": "training guide", "kind": "owner update", "text": "First draft underway. No completed draft supplied."},
    {"id": "S4", "recorded_at": "2026-10-07T15:00:00+00:00", "event_date": "2026-10-07", "workstream": "export", "kind": "project lead decision request", "text": "Choose by October 9: a standard-only pilot export or wait for custom columns. Without the decision, the pilot scope remains unresolved."},
    {"id": "S5", "recorded_at": "2026-10-08T16:00:00+00:00", "event_date": "2026-10-08", "workstream": "export", "kind": "later update", "text": "All export checks now pass."
    }
  ]
}
```

## Expected draft and evidence decisions

```json
{
  "brief": "Partner Portal update, October 2–8; as of October 8 at 12:00 UTC.\n\nThe preview demo is available, and its earlier sample-data approval blocker is resolved [S1, P0]. The export change is merged, but validation is incomplete: 18 of 20 checks passed at r42, with two custom-column failures [S2]. No release evidence was supplied.\n\nThe training guide is last known to be in draft as of September 29. That update is stale under the seven-day rule, so current completion is unknown [S3].\n\nDecision needed by October 9: choose a standard-only pilot export or wait for custom columns. Until then, pilot scope remains unresolved [S4].",
  "accepted_current_sources": ["S1", "S2", "S4"],
  "carry_forward_source": "S3",
  "prior_comparison_source": "P0",
  "excluded_after_cutoff": ["S5"],
  "metrics": {"test_passed": 18, "test_total": 20, "test_failed": 2, "test_pass_percent": 90, "project_percent_complete": null},
  "training_guide_update_age_days": 9,
  "training_guide_current_state": "unknown",
  "old_preview_blocker": "resolved",
  "export_release_state": "unknown: no release evidence supplied",
  "decision_due_date": "2026-10-09"
}
```

## Why this wording follows the evidence

S1 resolves the old approval blocker and supports an available preview demo, but says nothing about a public release. S2 establishes a merged change and a partial test result for r42. Eighteen divided by twenty is 90% for that test set; it does not establish that the project is 90% complete. S3 is nine days old, so the current guide state is unknown. S5 is excluded because its timestamp is four hours after the cutoff, even though its wording sounds reassuring. The October 9 decision deadline and the consequence of waiting come directly from S4.

## Checks to perform

Parse the records, verify the 18 + 2 = 20 count, recalculate 90%, compute the guide's nine-day age, exclude S5 against the exact cutoff, check every brief source label and count the brief's words. No external app, release, message or approval action is executed by this example.
