---
name: awaiting-reply-user-followup
description: "Check a specified conversation at bounded times and notify only the user when a reply remains outstanding."
---

# A Private Nudge for an Awaited Reply

Check a specified conversation at bounded times and notify only the user when a reply remains outstanding.

## When to use

A project organizer sent a routine venue question and wants to avoid forgetting it. They want a private nudge if the answer has not arrived, not an assistant that starts chasing the venue or monitoring every conversation.

## Required inputs

- The exact authorized conversation and outgoing message to check
- What counts as a sufficient reply, including partial or automated replies
- First check time, repeat cadence if any, and a final stop time
- IANA timezone and the user’s notification destination
- A maximum reminder count and duplicate-suppression rule

## Workflow

### Required scope

Record the exact conversation reference, outgoing message reference and timestamp, authorized reader account, sufficient-reply criteria, first check, optional cadence, final check boundary, maximum user notifications, suppression window, IANA timezone and personal destination. Confirm which questions remain unanswered. The correspondent's identity and the thread are scope selectors, not authorization to send anything to them.

### Procedure

1. Read the specified conversation through the connected messaging or email app. Confirm that the outgoing message exists and establish the last relevant message visible now. If a sufficient answer has already arrived, report that result and avoid starting an unnecessary watch. A failed read produces an access blocker, never an absent-reply conclusion.
2. Translate the user's criteria into a small decision table: substantive answer closes the loop; automated acknowledgment follows the supplied rule; partial answer leaves named questions open; unrelated message changes nothing. Quote or summarize only the minimum evidence needed to explain classification. Ask when a partial response could reasonably satisfy the request either way.
3. Inspect whether the available scheduling service can perform source reads at the desired bounded cadence and whether it can retain counters, suppress unchanged notices and stop future checks. Choose a supported arrangement. If those features cannot be verified, offer a one-shot reminder to review the conversation rather than claiming durable conditional monitoring. State the expected check interval; do not describe polling as instant observation.
4. Convert the first and final local timestamps using their IANA zone. For repeated local-clock checks, calculate daylight-saving behavior by date; for an elapsed interval, preserve elapsed duration. Resolve repeated or missing local hours and reject a first check beyond the final boundary. Do not backfill missed checks with a burst.
5. Match existing setup using conversation, outgoing-message reference and reply criteria. Repeated setup should return or update that same logical watch. Suppression is a separate rule: one notification for a qualifying unanswered state within the agreed window. It is not permission to hide a new partial answer or a source failure. Inspect existing state after an uncertain save before retrying.
6. Save the supported configuration and read back source scope, timing, destination, notification limit and stop boundary. Test the decision table with a partial reply, acknowledgment and read failure without contacting the correspondent.

### Output and closure

Deliver the criteria, saved reference, schedule, sample private nudge and verified limitations. At a sufficient reply, notification limit, final boundary or user cancellation, stop the remaining checks if supported and inspect that state. If automated cancellation is unavailable, disclose that before setup and use a simpler bounded design. Preserve a distinction between a completed check, delivered notice and answered question. Any follow-up draft or external outreach is a separate user decision.

## Deliverables

- A precise conversation scope and sufficient-reply definition
- A bounded check schedule with a maximum notification count
- Private nudge text containing the next user action
- A verified setup record or a manual fallback with its limits

## Verification

- An unrelated incoming message does not count as the awaited reply
- An automated acknowledgment is treated according to the explicit reply criteria
- A failed source read is distinguished from an absent reply
- No outbound message is sent to the correspondent
- Duplicate setup and unchanged results obey the agreed suppression rule
- Checks end at the stated boundary or after a verified sufficient reply

## Stop and ask

- Read access must work before monitoring is promised
- Keep the source scope to the named conversation and avoid sensitive content in alerts
- Stop if reply criteria are ambiguous enough to change whether the user is nudged
- This workflow does not authorize follow-up outreach

## Example request

```text
dot, help me remember a reply owed in [SPECIFIC AUTHORIZED CONVERSATION] after my message [MESSAGE REFERENCE]. A sufficient reply means [REPLY CRITERIA]. Check first at [FIRST DATETIME], then [CADENCE OR ONE SHOT], in [IANA TIMEZONE], and stop at [FINAL DATETIME] or after [MAXIMUM USER NOTIFICATIONS], whichever comes first. Notify only me at [DESTINATION]. Do not contact the other person or draft in their conversation.

Verify that you can read the specified source now and that supported scheduling can perform the bounded checks. Do not promise instant observation. Inspect only relevant messages after the referenced outgoing message; distinguish a substantive answer from an automated acknowledgment or unrelated update. If access fails later, report a source-access blocker rather than claiming that no reply arrived.

Before setup, look for a matching follow-up so a retry cannot create duplicates. Specify how unchanged results will avoid repeated notices within [SUPPRESSION WINDOW]. If a sufficient reply is found, stop the remaining checks when supported and verify that state; otherwise disclose the limitation and offer a simpler one-shot reminder. Return the exact schedule, reply criteria, notification text and setup evidence. If source access or scheduling is unavailable, provide a clearly unscheduled manual follow-up checklist.
```

## Focused follow-ups

### 1. Refine a partial reply

```text
The conversation now contains [AUTHORIZED PARTIAL REPLY]. Compare it with my original reply criteria and ask whether the remaining question still warrants a reminder.
```

### 2. Move the follow-up date

```text
Update the existing check to [NEW DATE AND TIME], keeping the same conversation, personal destination and final stop boundary. Flag any resulting invalid date range.
```

### 3. Close the waiting loop

```text
The reply is sufficient. Stop this conversation’s remaining checks and verify the result, without sending anything to the correspondent.
```

## Evidence status

This is an implementation guide. End-to-end execution has not been established; report actual checks and unrun steps for each use.
