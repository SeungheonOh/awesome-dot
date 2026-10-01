# Second case: synthetic interval verification

This is fictional supplied availability for a find-options request. No calendars, contacts or invitation services were used. The result checks the interval reasoning on different inputs; it is not evidence of a real person's availability or a sent invitation.

## Input

Find a 30-minute meeting on October 28, 2026 for these three required participants. Each needs 15 minutes free before and after the new meeting, inside the stated window. Availability is complete for these windows. Busy intervals are raw, without added buffers.

| Participant | IANA zone | Allowed local window | Raw busy in local time |
| --- | --- | --- | --- |
| Noor | Europe/London | Oct 28, 13:00–16:00 | Oct 28, 13:30–14:00 |
| Eli | America/New_York | Oct 28, 09:00–12:00 | Oct 28, 10:00–10:30 |
| Sana | Asia/Singapore | Oct 28, 21:00 to Oct 29, 00:00 | Oct 28, 23:30 to Oct 29, 00:00 |

## Calculated result

Python's installed `datetime` and `zoneinfo` tools confirmed the conversions and interval calculations on 2026-10-01. The date-specific offsets are London +00:00, New York −04:00 and Singapore +08:00. All allowed windows become Oct 28, 13:00–16:00 UTC. Sana's midnight endpoint is on Oct 29 locally, not the start of Oct 28.

Subtract each participant's raw busy intervals, then require 15 + 30 + 15 = 60 contiguous free minutes. The resulting CLOSED feasible-start ranges in UTC are:

```text
Noor:  [14:15, 15:15]
Eli:   [13:15, 13:15] or [14:45, 15:15]
Sana:  [13:15, 14:45]
All:   [14:45, 14:45]
```

The singleton start 14:45 UTC is valid; no scheduling grid was assumed. The meeting and full buffered intervals are:

| Zone | Meeting on Oct 28 | Buffered interval on Oct 28 |
| --- | --- | --- |
| Europe/London (+00:00) | 14:45–15:15 | 14:30–15:30 |
| America/New_York (−04:00) | 10:45–11:15 | 10:30–11:30 |
| Asia/Singapore (+08:00) | 22:45–23:15 | 22:30–23:30 |

The buffered interval [14:30, 15:30) UTC fits Noor's afternoon free block, starts exactly when Eli's busy interval ends, and ends exactly when Sana's busy interval begins. Those contacts do not overlap under half-open interval semantics. Apply the buffers once to the new meeting; do not also expand the busy intervals by those same buffers.

## Unknown required availability

If Sana's availability becomes unknown and no supplied availability remains for her, no option is verified for all three. Noor and Eli still permit starts anywhere in the closed range 14:45–15:15 UTC, each lasting 30 minutes. These are only known-subset proposals awaiting Sana's availability; the earlier 14:45 result must not retain a verified label.

For this find-options request, report the result and request the missing availability if needed. Do not send an invitation, create a hold, start a poll or contact Sana. Those actions are outside the request.

Limits: this second case checks synthetic conversions, intersection, endpoint handling and scope decisions. It does not exercise calendar access, stale-source detection, identity verification, provider writes, notification delivery or concurrency.
