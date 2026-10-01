# Worked evidence brief

## Brief for the reader

Transcript-only review of a fictional 84-second clip. Audio and the full recording are unavailable; supplied labels and times are unverified. Original-source times below are calculated from the supplied 03:05.500 clip offset.

### Current work

- **Speaker A: prepare and post an internal draft for review.** “Next Friday” remains unresolved because the recording date, timezone and intended Friday are unknown. This is a commitment, not evidence of completion. [S02](fixture.md#s02), [S08](fixture.md#s08); original 03:13.500–03:22.500 and 04:08.500–04:18.500
- **Check the `[cache/cash?]` figures, owner unresolved.** Speaker A accepts the check but explicitly leaves ownership open. `[Lee/Leigh?]` is only a suggested name; the proposed “next Friday” was not clearly adopted. [S04](fixture.md#s04), [S05](fixture.md#s05); original 03:30.500–03:39.500 and 03:40.500–03:48.500

### Decisions, limits and changes

- **Reported decision:** keep the rollback switch disabled pending review. This records Speaker A’s statement, not independent confirmation of group agreement or authority. [S03](fixture.md#s03); original 03:23.500–03:30.500
- **The customer-send promise was retracted.** Speaker A replaces it with an internal draft and says no customer send is authorized. Do not carry forward the original “send tomorrow” action. [S01](fixture.md#s01), [S02](fixture.md#s02); original 03:05.500–03:13.500 and 03:13.500–03:22.500
- **Launch approval remains unresolved.** Speaker B believes it is approved; Speaker A says they have not approved it and a review is still needed. Both statements could be true if another person approved the launch. The excerpt does not establish who can authorize launch or whether another approver exists. [S06](fixture.md#s06), [S07](fixture.md#s07); original 03:49.500–03:58.500 and 03:59.500–04:07.500
- **Suggestion only:** a public recap. No acceptance appears in the supplied excerpt. [S09](fixture.md#s09); original 04:19.500–04:26.500

### Clarifications that change the brief

1. What exact date did Speaker A mean by “next Friday” for the internal draft?
2. Which figures were meant by `[cache/cash?]`, and who accepted ownership of that check? Does it have an agreed deadline?
3. Who has launch approval authority, and what review or approval remains outstanding?

No transcript wording was corrected or audio-verified. The S01 → S02 change is a spoken retraction already present in the supplied text. These are questions for the reader; none was sent.

## Evidence ledger

The JSON below is a compact, machine-checkable appendix. All milliseconds are elapsed media time. Clip timestamps target the supplied excerpt; original timestamps are navigation references for the unavailable full recording, not playback links.

```json
{
  "source_id": "memo-clip-01",
  "source_revision": "Release memo excerpt, fictional transcript revision 1",
  "evidence_mode": "transcript_only",
  "audio_reviewed_intervals": [],
  "transcript_corrections": [],
  "segments": [
    {"id":"S01","clip_ms":[0,8000],"original_ms":[185500,193500],"speaker":"Speaker A","quote":"Release memo. I’ll send the customer note tomorrow after the test."},
    {"id":"S02","clip_ms":[8000,17000],"original_ms":[193500,202500],"speaker":"Speaker A","quote":"Correction: I will not send it tomorrow. I’ll prepare a draft for internal review; no customer send is authorized."},
    {"id":"S03","clip_ms":[18000,25000],"original_ms":[203500,210500],"speaker":"Speaker A","quote":"We’ve agreed to keep the rollback switch disabled until the review says otherwise."},
    {"id":"S04","clip_ms":[25000,34000],"original_ms":[210500,219500],"speaker":"Speaker B","quote":"Maybe [Lee/Leigh?] could check the [cache/cash?] figures next Friday."},
    {"id":"S05","clip_ms":[35000,43000],"original_ms":[220500,228500],"speaker":"Speaker A","quote":"Yes to checking those figures. I don’t know who will do it yet."},
    {"id":"S06","clip_ms":[44000,53000],"original_ms":[229500,238500],"speaker":"Speaker B","quote":"I think the launch is approved."},
    {"id":"S07","clip_ms":[54000,62000],"original_ms":[239500,247500],"speaker":"Speaker A","quote":"I have not approved the launch. We still need a review."},
    {"id":"S08","clip_ms":[63000,73000],"original_ms":[248500,258500],"speaker":"Speaker A","quote":"I’ll post the internal draft by next Friday. I mean the draft, not the customer note."},
    {"id":"S09","clip_ms":[74000,81000],"original_ms":[259500,266500],"speaker":"Speaker B","quote":"We could also write a public recap, if that would help."}
  ],
  "claims": [
    {"id":"C01","kind":"commitment","state":"retracted","summary":"Send the customer note tomorrow after the test","segments":["S01"],"retracted_by":"C02"},
    {"id":"C02","kind":"retraction_and_prohibition","state":"current","summary":"Retract tomorrow’s customer send; no customer send is authorized","segments":["S02"],"retracts":"C01"},
    {"id":"A01","kind":"commitment","state":"current","summary":"Prepare and post the internal draft for review","segments":["S02","S08"],"owner":"Speaker A","owner_basis":"Supplied speaker label making a first-person commitment","due_wording":"next Friday","due_date":null,"date_status":"unresolved_recording_context_and_convention","completion_evidence":"none_supplied"},
    {"id":"D01","kind":"reported_decision","state":"current","summary":"Keep the rollback switch disabled until review says otherwise","segments":["S03"]},
    {"id":"P01","kind":"suggestion","state":"partly_accepted","summary":"Suggested check, name and date; later acceptance establishes work but no owner or agreed deadline","segments":["S04"],"accepted_work":"A02"},
    {"id":"A02","kind":"agreed_unassigned_work","state":"current","summary":"Check the [cache/cash?] figures","segments":["S04","S05"],"owner":null,"suggested_owner_wording":"[Lee/Leigh?]","due_wording":null,"proposed_due_wording":"next Friday","due_date":null,"date_status":"proposal_not_clearly_adopted","completion_evidence":"none_supplied"},
    {"id":"B01","kind":"belief","state":"unresolved","summary":"Speaker B thinks the launch is approved","segments":["S06"],"related_to":"B02"},
    {"id":"B02","kind":"status_statement","state":"unresolved","summary":"Speaker A has not approved launch and says a review is needed","segments":["S07"],"related_to":"B01"},
    {"id":"P02","kind":"suggestion","state":"not_accepted_in_excerpt","summary":"Write a public recap","segments":["S09"]}
  ],
  "current_action_ids": ["A01", "A02"],
  "unresolved": ["A01 exact due date", "A02 wording, owner and due date", "Launch approval authority and status"],
  "coverage_limits": ["No actual audio reviewed", "Supplied transcript only", "Original source unavailable", "Recording date/timezone unknown", "Unrepresented intervals are not established silence"]
}
```
