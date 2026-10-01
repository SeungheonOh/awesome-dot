---
id: new-hire-onboarding-map
title: "New-Hire Onboarding Map"
summary: "Build a role-specific onboarding map that connects safe starter tasks, prerequisites, documented resources, and evidence of readiness."
category: team-operations
level: beginner
timebox_minutes: 60
capabilities: ["files"]
tags: ["onboarding", "documentation", "readiness"]
status: recipe-not-run
---

# New-Hire Onboarding Map

Build a role-specific onboarding map that connects safe starter tasks, prerequisites, documented resources, and evidence of readiness.

## Scenario

A fictional service team has a long welcome document but no clear route from reading to useful work. A new engineer needs to understand the service, practice safely, and know who can answer which question without receiving excessive access.

## Inputs to prepare

- A fictional or sanitized role description and first-month objectives
- An authorized list of existing documents, training examples, and contact roles
- Known access prerequisites and the team’s approved request process
- Available mentor time, working hours, and an explicit list of prohibited starter tasks

## Copy this prompt into dot

```text
dot, build an onboarding map for a new [ROLE] joining [TEAM]. Use [AUTHORIZED RESOURCES] and [FIRST-MONTH OBJECTIVES], with [MENTOR TIME] available. This is a planning draft, not permission to create accounts or grant access. First identify missing information that would materially change the learning order.

Organize the map around observable milestones: understand the service purpose, trace one routine workflow, complete a safe practice task, and explain when to ask for help. For each milestone list prerequisites, the smallest useful resource, a concrete exercise, a reviewer role, and evidence that the milestone is met. Separate required learning from optional depth. Mark unavailable or outdated resources instead of filling gaps with invented team practices.

Show which tasks can proceed while access is pending. Use synthetic data and read-only or isolated practice where possible; exclude [PROHIBITED TASKS]. Check a normal arrival, a delayed-access arrival, and a mentor-absence scenario. Ensure no milestone silently depends on production privileges.

Return the milestone map, a resource gap list, and a short readiness review checklist. Keep personal details out. Do not message colleagues, enroll anyone, request permissions, or modify onboarding systems without explicit instructions for those actions.
```

## Iterate with a purpose

### 1. Make the first day independent

```text
Produce a first-day route that requires no pending system access and no live mentor. Include a useful artifact the new hire can bring to the next check-in.
```

### 2. Test one starter task

```text
Expand one safe starter task into setup assumptions, expected observations, a stopping point, and a reviewer checklist. Use only the supplied resources and synthetic examples.
```

### 3. Close resource gaps

```text
Prioritize the missing or outdated resources by how much they block the milestones. Draft a short outline for the highest-impact missing page without inventing team policy.
```

## Expected deliverables

- A role-specific milestone map with prerequisites and observable readiness evidence
- An access-independent starter route
- A resource gap list with the affected milestone
- A mentor review checklist and stated assumptions

## Acceptance checks

- Each milestone ends with an observable output rather than merely “read the docs”
- Required resources have supplied locators or are explicitly marked missing
- Delayed access still leaves a useful, safe path forward
- Mentor absence has a bounded fallback rather than invented approval
- No starter task assumes production privileges or authorizes an access request
- Required and optional material are visibly separated

## Access, privacy and stop conditions

- Use role names instead of employee personal information unless it is necessary and authorized
- Respect the existing access request process; this map cannot grant permissions
- Stop a practice task at any step that would affect real systems or expose customer data

## Two possible extensions

- Create a sanitized sample artifact showing what one completed milestone looks like
- Adapt the map for an internal transfer with prior product knowledge
