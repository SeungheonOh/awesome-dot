---
name: release-readiness-gate
description: "Convert a bounded release candidate into a go, hold or unknown decision packet with named evidence and rollback conditions."
---

# Build an Evidence-Based Release Gate

Convert a bounded release candidate into a go, hold or unknown decision packet with named evidence and rollback conditions.

## When to use

A fictional scheduling service plans a release that changes reminder timing and adds a database column. Test results exist in several exports, but nobody can tell which results belong to the candidate being released. The release owner needs a decision packet tied to one immutable candidate, including what would make the team stop or reverse the rollout.

## Required inputs

- A candidate identifier, change summary and exact included change list
- Sanitized test, build and staging result exports with timestamps and candidate identifiers
- Release policy, required approvals and known exceptions
- Rollout stages, observable health measures and acceptable thresholds
- Rollback or recovery instructions, including any data change that cannot be reversed

## Workflow

### Reconcile candidate and policy

Create a candidate record containing immutable identifier, included changes, build artifact reference and proposed release scope. Inventory each evidence item with type, producing command or process, candidate identifier, timestamp, environment, result and completeness. Extract mandatory gates, exception authority, evidence freshness rules and required approvals from the supplied policy. If candidate identity is missing or contradictory, prepare the evidence inventory but stop the readiness recommendation until it is resolved.

### Evaluate gates and rollout decisions

1. Map each policy gate to evidence for this candidate. Assign satisfied, failed or unknown, with the reason and source. Missing, truncated, stale or wrong-candidate evidence is unknown unless a supplied policy explicitly permits reuse. Record the precise reuse rule rather than assuming unchanged files make old evidence current.
2. Inventory change-specific risks, including timing behavior, schema changes and dependencies that must coexist. Link each to a required check or an unresolved release question. A green build does not automatically satisfy a behavioral or recovery gate.
3. Build the recommendation using mandatory gates: any failed mandatory gate means hold; any unknown mandatory gate means pending evidence; all required gates satisfied permits an advisory ready-for-owner-decision result. Apply an exception only when the supplied record names the authorized approver, scope and validity. Never create an exception by inference.
4. Define preparation, first rollout group, expansion and closure rows. Each needs entry evidence, responsible role, observation window, measurement source, success threshold, stop condition and next decision. Use supplied thresholds; a blank threshold blocks that stage rather than becoming an invented safe value. If measurements have reporting delay, expose it in the window and decision limits.
5. Write recovery as a separate decision branch. Identify the preserved prior artifact, prerequisite access, changed data compatibility, recovery action described by the supplied instructions and evidence of restored behavior. For irreversible data changes, state where artifact rollback is insufficient and what recovery choice remains for an owner.

### Test the packet's logic

Walk four fictional evidence sets through the gate rules: all requirements met, one mandatory failure, stale or different-candidate results, and a release with an irreversible migration. Record the expected recommendation and blocking stage for each; this is a logic check, not release execution. Reconcile every policy requirement to a gate and every accepted result to its candidate identity.

Deliver a one-page advisory decision summary, full evidence ledger, staged checklist, recovery branch and unresolved owner decisions. Separate existing approvals in supplied evidence from approval still required. If the policy lacks exception authority, stage thresholds or recovery prerequisites, ask the release owner the smallest necessary question while completing unaffected sections. Stop before changing status in a release system, recording approval, deploying or carrying out recovery.

## Deliverables

- A gate ledger linking each release requirement to dated candidate-specific evidence
- A staged release checklist with owners, health checks and stop conditions
- A recovery readiness section covering reversibility and post-recovery verification
- A go, hold or unknown recommendation with explicit policy-based reasons

## Verification

- The candidate identifier appears in the packet and all accepted test evidence is reconciled to it
- A failed mandatory gate produces a hold recommendation, unless a supplied explicit exception is documented
- Missing or stale evidence remains unknown and cannot silently become a pass
- Each rollout stage includes an observation window and a measurable or directly observable condition
- An irreversible migration triggers a recovery decision rather than a fictitious undo step
- The recommendation is clearly advisory and no approval or deployment is claimed

## Stop and ask

- Begin with sanitized evidence exports; production dashboards and logs require separate authorized access
- Thresholds and exception authority must come from the supplied policy or a human owner
- Stop the dependent recommendation if candidate identity cannot be established
- Deployment, rollback execution, external communication and approval recording require a separate user decision

## Example request

```text
dot, prepare a release-readiness decision packet for [RELEASE CANDIDATE] of [SERVICE] using only [SUPPLIED EVIDENCE] and [RELEASE POLICY]. The reader is [RELEASE OWNER]. This is a review exercise; do not deploy, approve a release, change settings or message anybody.

Inventory the candidate's changes and map each required gate to its evidence, candidate identifier, timestamp, owner and current state: satisfied, failed or unknown. Evidence from a different build must not count unless the supplied policy explicitly allows it and the reason is recorded. Explain unfamiliar terms briefly for a first-time release coordinator.

Construct a staged checklist covering preparation, the first rollout group, wider rollout and closure. For each stage specify the observation window, numerical or clearly observable success condition, stop condition and responsible role. Use supplied thresholds; leave a visible decision blank rather than inventing a production safety limit. Treat rollback as a recovery procedure with prerequisites, data consequences and a validation step, not just a command.

Test the decision logic against a passing candidate, a failed required gate, stale evidence and a migration that cannot be reversed. Show how each changes the recommendation. Return the packet with unresolved blockers and the smallest owner decisions needed. Any command execution requires a separately authorized environment and available toolchain. Ask before obtaining additional access, taking any external action or expanding into deployment work; keep supplied operational details private.
```

## Focused follow-ups

### 1. Reconcile candidate evidence

```text
Recheck every attached result against [FINAL CANDIDATE IDENTIFIER]. Produce a short list of results that remain valid, must be rerun, or need a policy decision, with the exact reason for each.
```

### 2. Walk through a rollback

```text
Use a fictional failed first-stage rollout to walk through the recovery procedure on paper. Identify the first irreversible step, required decision maker and observation that would show recovery succeeded.
```

### 3. Prepare the meeting decision

```text
Condense the packet into a five-minute release review agenda. Put unresolved mandatory gates first and include a place to record each human decision, owner and rationale without implying approval.
```

## Evidence status

This is an implementation guide. End-to-end execution has not been established; report actual checks and unrun steps for each use.
