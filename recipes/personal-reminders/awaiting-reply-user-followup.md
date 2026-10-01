---
id: awaiting-reply-user-followup
title: "A Private Nudge for an Awaited Reply"
summary: "Check a specified conversation at bounded times and notify only the user when a reply remains outstanding."
category: personal-reminders
level: intermediate
timebox_minutes: 30
capabilities: ["scheduling", "connected-apps"]
tags: ["follow-up", "reply", "bounded-checks"]
status: recipe-not-run
---

# A Private Nudge for an Awaited Reply

Check a specified conversation at bounded times and notify only the user when a reply remains outstanding.

## Scenario

A project organizer sent a routine venue question and wants to avoid forgetting it. They want a private nudge if the answer has not arrived, not an assistant that starts chasing the venue or monitoring every conversation.

## Inputs to prepare

- The exact authorized conversation and outgoing message to check
- What counts as a sufficient reply, including partial or automated replies
- First check time, repeat cadence if any, and a final stop time
- IANA timezone and the user’s notification destination
- A maximum reminder count and duplicate-suppression rule

## Copy this prompt into dot

```text
dot, help me remember a reply owed in [SPECIFIC AUTHORIZED CONVERSATION] after my message [MESSAGE REFERENCE]. A sufficient reply means [REPLY CRITERIA]. Check first at [FIRST DATETIME], then [CADENCE OR ONE SHOT], in [IANA TIMEZONE], and stop at [FINAL DATETIME] or after [MAXIMUM USER NOTIFICATIONS], whichever comes first. Notify only me at [DESTINATION]. Do not contact the other person or draft in their conversation.

Verify that you can read the specified source now and that supported scheduling can perform the bounded checks. Do not promise instant observation. Inspect only relevant messages after the referenced outgoing message; distinguish a substantive answer from an automated acknowledgment or unrelated update. If access fails later, report a source-access blocker rather than claiming that no reply arrived.

Before setup, look for a matching follow-up so a retry cannot create duplicates. Specify how unchanged results will avoid repeated notices within [SUPPRESSION WINDOW]. If a sufficient reply is found, stop the remaining checks when supported and verify that state; otherwise disclose the limitation and offer a simpler one-shot reminder. Return the exact schedule, reply criteria, notification text and setup evidence. If source access or scheduling is unavailable, provide a clearly unscheduled manual follow-up checklist.
```

## Iterate with a purpose

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

## Expected deliverables

- A precise conversation scope and sufficient-reply definition
- A bounded check schedule with a maximum notification count
- Private nudge text containing the next user action
- A verified setup record or a manual fallback with its limits

## Acceptance checks

- An unrelated incoming message does not count as the awaited reply
- An automated acknowledgment is treated according to the explicit reply criteria
- A failed source read is distinguished from an absent reply
- No outbound message is sent to the correspondent
- Duplicate setup and unchanged results obey the agreed suppression rule
- Checks end at the stated boundary or after a verified sufficient reply

## Access, privacy and stop conditions

- Read access must work before monitoring is promised
- Keep the source scope to the named conversation and avoid sensitive content in alerts
- Stop if reply criteria are ambiguous enough to change whether the user is nudged
- This recipe does not authorize follow-up outreach

## Two possible extensions

- Prepare a routine follow-up draft in the user’s private chat after a nudge
- Add a separately approved check for one other named conversation
