# Worked example: one checklist mentioned twice

All people, documents and statements below are fictional. The required outcome is a private handoff as of October 7, 2026 in Europe/London. The document body supplied as D1 can be inspected; no messaging or task-management app is involved.

## Inputs

```json
{
  "as_of": "2026-10-07T12:00:00+01:00",
  "timezone": "Europe/London",
  "sources": [
    {
      "id": "M1",
      "date": "2026-10-05",
      "lines": {
        "L1": "Mara: I'll send the v2 English partner checklist tomorrow.",
        "L2": "Jon: Could someone shorten the welcome guide?",
        "L3": "Facilitator: Agreed, prepare a French partner checklist too. Owner and date are still open."
      }
    },
    {
      "id": "M2",
      "date": "2026-10-06",
      "lines": {
        "L1": "Facilitator: The v2 English partner checklist is the same action from yesterday, still due today."
      }
    },
    {
      "id": "U1",
      "date": "2026-10-06",
      "lines": {"L1": "Mara: Checklist sent; done."}
    },
    {
      "id": "D1",
      "date": "2026-10-07",
      "lines": {
        "L1": "Title: English partner checklist v2",
        "L2": "Content: all agreed checklist sections are present.",
        "L3": "No delivery record is supplied."
      }
    }
  ]
}
```

## Expected ledger

```json
{
  "actions": [
    {
      "action_id": "A1",
      "deliverable": "Send the v2 English partner checklist",
      "completion_condition": "The v2 checklist is sent to the intended partners",
      "owner": "Mara",
      "owner_basis": "Explicit commitment at M1:L1",
      "due_wording": "tomorrow",
      "due_reference_date": "2026-10-05",
      "due_date": "2026-10-06",
      "due_time": null,
      "dependencies": [],
      "reported_status": "reported complete",
      "evidence_status": "partial result",
      "due_date_passed": true,
      "overdue_confirmed": false,
      "sources": ["M1:L1", "M2:L1", "U1:L1", "D1:L1", "D1:L2", "D1:L3"],
      "next_decision": "Confirm delivery evidence or retain completion as self-reported"
    },
    {
      "action_id": "A2",
      "deliverable": "Prepare a French partner checklist",
      "completion_condition": "A French partner checklist is prepared",
      "owner": null,
      "owner_basis": "Ownership was explicitly left open at M1:L3",
      "due_wording": null,
      "due_date": null,
      "due_time": null,
      "dependencies": [],
      "reported_status": "open",
      "evidence_status": "no result supplied",
      "due_date_passed": null,
      "overdue_confirmed": false,
      "sources": ["M1:L3"],
      "next_decision": "Agree an owner, completion detail and due date if needed"
    }
  ],
  "merged_mentions": [{"sources": ["M1:L1", "M2:L1"], "action_id": "A1"}],
  "not_agreed": [{"source": "M1:L2", "reason": "Suggestion with no acceptance or owner commitment"}]
}
```

## Expected handoff

- Mara reports the English checklist sent. The supplied v2 document supports preparation, but delivery evidence is absent. Its original October 6 deadline has passed; lateness is not established
- The agreed French checklist still needs an owner and a completion agreement. It is separate work, even though both deliverables are checklists
- Shortening the welcome guide was suggested, not assigned

## Checks to perform

October 5 plus one calendar day is October 6. The two English-checklist mentions yield one action; the French checklist yields a second action. M1:L2 yields no commitment. Every output source locator exists. No due time, recipient identity, French-checklist owner or proof of delivery has been invented. These are fixture consistency checks, not evidence that any checklist was actually sent.
