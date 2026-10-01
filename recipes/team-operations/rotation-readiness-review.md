---
id: rotation-readiness-review
title: "Rotation Readiness Review"
summary: "Prepare a role-based support rotation readiness review with coverage gaps, tabletop exercises, escalation boundaries, and evidence requirements."
category: team-operations
level: intermediate
timebox_minutes: 60
capabilities: ["files"]
tags: ["rotations", "readiness", "support"]
status: recipe-not-run
---

# Rotation Readiness Review

Prepare a role-based support rotation readiness review with coverage gaps, tabletop exercises, escalation boundaries, and evidence requirements.

## Scenario

A fictional team is preparing a new support rotation. A populated roster looks reassuring, but coverage does not prove that the right runbooks, authority, or backup paths exist. A readiness review tests the arrangement before it is treated as operational.

## Inputs to prepare

- A sanitized proposed rotation using role labels and explicit timezone information
- Authorized runbooks, escalation policy, and support scope
- Known holidays, coverage constraints, and handoff expectations
- The readiness reviewer role and any documented approval criteria

## Copy this prompt into dot

```text
dot, review readiness for [SUPPORT ROTATION] over [DATE RANGE] using [PROPOSED ROSTER], [AUTHORIZED RUNBOOKS], and [ESCALATION POLICY]. Use [TIMEZONE] for every displayed interval and retain original zones when conversion matters. This is a planning and tabletop exercise, not an instruction to activate a rotation.

Map each coverage interval to a primary role, backup role, supported scope, escalation boundary, and handoff requirement. Identify gaps, ambiguous overlaps, missing prerequisites, and assumptions about availability. A person appearing on a roster is not evidence that they accepted the duty or have the necessary access.

Create tabletop prompts for a routine support request, an unavailable primary responder, and a problem outside the team’s authority. For each, specify the expected decision path using documented guidance and the evidence a reviewer should inspect. If dates cross a clock change, check actual offsets before asserting continuous coverage; otherwise label conversion unverified.

Return a readiness checklist, a coverage issue list, and the tabletop packet. Separate proposed fixes from confirmed arrangements. Do not contact participants, alter calendars, enable alerts, grant access, or change escalation routing. Keep the roster private and stop any dependent operational step until the appropriate reviewer confirms it.
```

## Iterate with a purpose

### 1. Inspect the handoff boundary

```text
Examine each change of coverage for unanswered cases, delayed responses, and unclear responsibility. Propose a minimal handoff record that fits the documented support scope.
```

### 2. Stress-test one absence

```text
Walk through a fictional absence of the primary role during a high-volume interval. Use the documented backup path and flag any step that depends on unconfirmed availability or authority.
```

### 3. Prepare a reviewer packet

```text
Reduce the review to the evidence needed for a go-or-pause decision. Keep staffing acceptance, access readiness, and runbook adequacy as separate judgments.
```

## Expected deliverables

- A coverage map with explicit timezones and unresolved assumptions
- A readiness checklist covering authority, access, runbooks, and handoffs
- Three tabletop scenarios and expected documented decision paths
- A prioritized list of proposed fixes requiring confirmation

## Acceptance checks

- Every interval has explicit timezone treatment rather than an unexplained local time
- A missing backup or unaccepted duty remains a readiness gap
- Overlapping shifts do not hide an uncovered handoff period
- A clock-change interval is verified with actual offsets or labeled unverified
- An out-of-scope problem follows the documented escalation boundary
- No alert, calendar, roster, or permission change is represented as completed

## Access, privacy and stop conditions

- Use role labels and minimal availability data rather than unnecessary personal schedules
- Tabletop exercises must not trigger live alerts or touch production systems
- Activating coverage, messaging participants, and changing access require separate authorization

## Two possible extensions

- Create a reusable handoff note template from the identified gaps
- Review a later rotation proposal against the same readiness criteria
