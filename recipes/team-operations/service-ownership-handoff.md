---
id: service-ownership-handoff
title: "Service Ownership Handoff"
summary: "Prepare a bounded service handoff packet with operating responsibilities, evidence gaps, receiving-team questions, and explicit acceptance criteria."
category: team-operations
level: intermediate
timebox_minutes: 60
capabilities: ["files"]
tags: ["ownership", "handoff", "operations"]
status: recipe-not-run
---

# Service Ownership Handoff

Prepare a bounded service handoff packet with operating responsibilities, evidence gaps, receiving-team questions, and explicit acceptance criteria.

## Scenario

A fictional reporting service is moving between teams. The repository has an owner, but operational duties, known limitations, and escalation responsibilities are scattered. A handoff packet helps the receiving team judge readiness without treating a document as an accepted transfer.

## Inputs to prepare

- The service scope and proposed sending and receiving team roles
- Authorized runbooks, dependency notes, incident summaries, and responsibility records
- The proposed handoff date and any fixed transition constraints
- The organization’s existing acceptance process or an explicit statement that it is unknown

## Copy this prompt into dot

```text
dot, prepare a service ownership handoff packet for [SERVICE] moving from [SENDING TEAM] to [RECEIVING TEAM]. Use [AUTHORIZED MATERIALS], [PROPOSED DATE], and [TRANSITION CONSTRAINTS]. Keep the scope to documented responsibilities and a proposed acceptance review. Ask about missing information that would change the transfer boundary.

Describe the service purpose, interfaces, dependencies, routine maintenance, operational signals, escalation roles, known limitations, and unresolved work. For every responsibility distinguish the currently documented owner, proposed future owner, and evidence needed before acceptance. Do not assume that repository ownership includes operational, data-retention, or support duties.

Build a walkthrough for one routine operation, one degraded-service scenario, and one dependency owned by neither team. Identify stale or missing runbooks and propose a safe tabletop question instead of running production actions. Record unsupported details as gaps rather than inventing commands, contacts, or recovery guarantees.

Return a concise handoff packet, a responsibility matrix, and a go-or-pause checklist with evidence locators. Label acceptance as pending until the authorized participants confirm it. Do not transfer permissions, change escalation routing, notify teams, or modify live systems. Identify the exact approval needed for any later operational action.
```

## Iterate with a purpose

### 1. Run a tabletop walkthrough

```text
Using only the packet, walk through a fictional degraded-service scenario. Record where the receiving team would lack context, authority, or a reliable next step; do not execute operations.
```

### 2. Clarify the transfer boundary

```text
Compare documented current responsibilities with proposed future responsibilities. Highlight gaps and overlaps, and draft one confirmation question per disputed responsibility.
```

### 3. Design a transition review

```text
Create a review agenda ordered by readiness risk. For each go-or-pause item name the required evidence and the role that can judge it, without declaring the transfer accepted.
```

## Expected deliverables

- A concise service handoff packet with source locators
- A current-versus-proposed responsibility matrix
- A readiness checklist with evidence requirements and pending acceptance
- A gap list surfaced by the three tabletop scenarios

## Acceptance checks

- Service boundaries include dependencies outside both participating teams
- Current ownership is separate from proposed ownership and formal acceptance
- Each readiness item specifies evidence that a reviewer could inspect
- A missing recovery runbook produces a gap, not fabricated operating commands
- The degraded-service walkthrough remains a tabletop exercise
- The packet does not claim permissions or escalation routes have changed

## Access, privacy and stop conditions

- Use sanitized operational records and omit credentials, private endpoints, and unnecessary incident details
- The packet cannot authorize access transfer, responsibility assignment, or production changes
- Pause acceptance when the approving roles or service boundary are unclear

## Two possible extensions

- Create a receiving-team question sheet for a supervised walkthrough
- Prepare a read-only comparison against a later accepted handoff record
