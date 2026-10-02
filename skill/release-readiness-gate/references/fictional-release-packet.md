# Fictional Rivet release decision packet

**Recommendation: HOLD at preparation.** The recovery gate has a current failure. Timing behavior is unknown because its two passing exports are stale or belong to another candidate. A narrow performance exception does not resolve either blocker.

This is a worked, fictional assessment, frozen at **2026-10-01 12:00:00 UTC**. All people, evidence, policy, artifacts and measurements below are invented. `fixture:` references are local identifiers, not links to production systems. Nothing in this packet deploys, approves, changes a dashboard, verifies a real signature or performs recovery.

Raw input: [fictional-release-input.json](fictional-release-input.json). The JSON is the complete source for the policy, evidence exports and exception record. The executable checks derive gate states from its measurements, not from an export's claimed “passed” label.

## Candidate and assessment boundary

```json
{
  "release_id": "RIVET-2026-10-01.2",
  "source_commit": "36ff22950454f542a16cc9d48c109794b6bbf71b",
  "artifact_sha256": "7524852606c76187de7d0e328f26041ade14e8fa6262b06ea5c129c86737178c",
  "migration_sha256": "3c435e60e1705e95d2b4d95f2649ef1b94a4e295aed022f48f91f89e748d5be7"
}
```

The hashes identify fictional labels; no real artifact bytes were checked. Every accepted export and exception carries all four fields. A matching release label alone is insufficient.

Included changes, and no others:

- CHANGE-201: defer reminder dispatch until canonical `due_at_utc`, with daylight-saving-boundary replay coverage
- CHANGE-202: M042 adds `due_at_utc`, converts legacy local timestamps and clears their original local-time/zone fields during cutover
- CHANGE-203: measure duplicate sends, late reminders and queue age by rollout group

Candidate artifact: `fixture:rivet-build-418`. Preserved prior artifact: `fixture:rivet-build-417`.

Assessed scope: the first **2%** rollout in `fictional-prod-eu1`, proposed for **12:10–12:40 UTC on 2026-10-01**. That is a proposed observation window, not a start instruction. The packet is not ready for this window, and the window must be rescheduled if blockers remain. The recovery owner must establish the actual migration blast radius and compatibility with every old reader before any rollout; 2% application traffic must not be assumed to mean 2% database impact.

## Supplied fictional policy

`RIVET-POLICY-7`, effective 2026-09-28 00:00 UTC, is the authority for this example. It is not a recommended universal release policy.

All six gates are mandatory. No cross-candidate evidence reuse is allowed. Evidence age is measured from its completion timestamp to the assessment timestamp; exact freshness boundaries are accepted. Future timestamps, incomplete exports, absent measurements, stale results and candidate mismatches cannot establish a pass. Valid current failures are retained; a newer passing export alone does not supersede a failure.

| Gate / accountable role | Required evidence and normal acceptance rule | Maximum age |
| --- | --- | --- |
| G1 / Build owner | CI export: zero unit failures, zero contract failures, artifact attestation present | 24 h |
| G2 / Reminder QA owner | Staging replay: zero duplicates, zero reminders over 60 seconds late, all 24 DST cases pass | 6 h |
| G3 / SRE lead | Staging load: p99 ≤200 ms and error rate ≤0.1% | 2 h |
| G4 / Data owner | Recovery sandbox: new rows recover correctly, zero replay duplicates, zero lost acknowledged rows, successful snapshot drill, data-owner-approved recovery strategy and verified migration/old-reader plan | 24 h |
| G5 / On-call SRE | Staging probes: reporting delay ≤120 seconds, duplicate alert and per-cohort measurements verified | 6 h |
| G6 / Release reviewer | Candidate-scoped change review complete, signed by the Release reviewer role | 24 h |

Here p99 is the latency at or below which 99% of requests complete. Snapshot recovery alone is one G4 check, not the whole recovery gate.

Policy decision order: any unexcepted mandatory failure or failed first-rollout plan → `hold`; otherwise any mandatory gate or required first-rollout planning value unknown → `unknown`; otherwise → `ready_for_owner_decision`. The last result is advisory and applies only to the assessed scope. The release owner must separately authorize an actual deployment.

For this fictional policy, first-rollout planning requires the exact environment, stage and 2% cohort; at least 30 continuous observation minutes; complete finite numerical thresholds and reporting delay; and a proposed start at or after the assessment time. A shorter window, wrong scope or past start fails planning and must be corrected. A blank or invalid planning value remains unknown. The non-past-start rule is supplied by this case, not assumed to be universal.

## Full evidence ledger

Every completion time is UTC. “Accepted” means eligible for this assessment, not proof that the claimed real-world event occurred.

| Export / source | Producer; environment | Completed | Candidate binding; completeness | Measurement and disposition |
| --- | --- | --- | --- | --- |
| E-BUILD-418 / `fixture:E-BUILD-418` | CI build 418; fictional-ci | Sep 30 23:10 | All four fields match; complete | 0 unit / 0 contract failures; attestation present. Age 12 h 50 m; accepted |
| E-BHV-OLD / `fixture:E-BHV-OLD` | Timing replay, 24 cases; fictional-staging | Oct 1 04:30 | All four fields match; complete | 0 duplicates, 0 late, 24 DST passed. Age 7 h 30 m; **rejected as stale** |
| E-BHV-OTHER / `fixture:E-BHV-OTHER` | Timing replay, 24 cases; fictional-staging | Oct 1 10:45 | Release .1, different commit and artifact; complete | 0 duplicates, 0 late, 24 DST passed. **Rejected as wrong candidate**, despite being fresh |
| E-LOAD-218 / `fixture:E-LOAD-218` | Fixed-load replay; fictional-staging | Oct 1 11:00 | All four fields match; complete | p99 218 ms; error rate 0.04%. Accepted: normal p99 fails, error rate passes |
| E-RECOVERY-FAIL / `fixture:E-RECOVERY-FAIL` | Recovery rehearsal; fictional-recovery-sandbox | Oct 1 11:25 | All four fields match; complete | Snapshot restore succeeds, replay duplicates/lost acknowledged rows both 0 in that isolated drill. Prior binary skips new canonical rows; no approved complete recovery strategy or verified migration/old-reader plan. Accepted: G4 fails |
| E-METRICS-120 / `fixture:E-METRICS-120` | Measurement probes; fictional-staging | Oct 1 11:35 | All four fields match; complete | 120-second reporting delay; duplicate alert and per-cohort metrics verified. Accepted |
| E-REVIEW-9 / `fixture:E-REVIEW-9` | Rowan's scope review; fictional-review | Oct 1 11:45 | All four fields match; complete | Review complete, correct reviewer role. Accepted for G6; not deployment authorization |

## Exception record and gate result

`EX-P99-007` (`fixture:EX-P99-007`) was approved by **Mira Chen, fictional SRE lead**, at **11:30 UTC**, valid **11:30 ≤ assessment time < 13:00 UTC on Oct 1**.

It is bound to this candidate, `RIVET-POLICY-7`, G3's `p99_ms` check, the exact proposed 2% first-rollout scope and a maximum p99 of **225 ms**. The prepared queue-stop and duplicate-stop guards must both be present. The exception must cover the observation window plus reporting delay; proposed final measurements arrive at 12:42, before expiry. The operator still must verify actual guards before any authorized start.

The exception does not waive the 0.1% error ceiling, missing evidence, G4, a different candidate, a larger group, a later stage or a later time. There is no inferred extension. The original 218 > 200 ms failure stays visible.

| Gate | Raw state | Effective state | Reason |
| --- | --- | --- | --- |
| G1 | satisfied | satisfied | Current candidate build evidence meets all three checks |
| G2 | unknown | unknown | Neither passing export is eligible |
| G3 | failed | satisfied by exception | Only p99 fails; 218 ≤225 and EX-P99-007 covers this exact scope/time |
| G4 | failed | failed | Cannot recover new rows with prior binary; strategy approval and migration/old-reader plan absent |
| G5 | satisfied | satisfied | Measurement delay and alerts meet policy |
| G6 | satisfied | satisfied | Scoped review exists |

Thus G4 forces **hold**, even though G2 is also unknown. Removing the G4 failure without fresh G2 evidence would leave **unknown**, not ready. The separately checked first-rollout plan is satisfied as supplied: correct scope, a future 12:10 start, 30 observation minutes and complete thresholds. That planning result does not offset either evidence blocker.

## Staged checklist for the release owner

These are policy-derived planning rows, not performed actions. Reassess candidate binding, freshness, exception validity and actual metrics at each decision. All windows require complete measurements; a missing or delayed sample never counts as green.

| Stage / owner | Entry evidence and observation window | Success / stop rule and next decision |
| --- | --- | --- |
| Preparation / Release owner + Data owner | All G1–G6 satisfied or validly excepted; recorded recovery choice and prerequisites; assess at the proposed start | **Currently blocked by G4 and G2.** Hold while either remains unresolved, while any evidence expires, or while migration blast radius is unproved. If the packet becomes ready, owner decides whether to authorize the exact first group; no authorization is recorded here |
| First group / On-call SRE | Owner authorization; actual queue/duplicate guards and cohort measurement sources verified; 2% for 30 minutes, then wait 120 seconds for the final sample | All complete one-minute per-cohort windows: p99 ≤225 ms only while EX-P99-007 applies, error ≤0.1%, 0 duplicates, 0 reminders >60 seconds late, queue age ≤60 seconds. Any breach, missing data, excess lag or expiry stops expansion and invokes the recovery decision branch. At or before expiry the exceptional rollout must end or satisfy normal policy under an authorized owner decision. Earliest full-window review for the proposed window: 12:42 UTC |
| Expansion / Release owner + SRE lead | A successful first group, fresh normal G3 pass, current mandatory gates and owner authorization for 25%; 30 minutes plus 120-second reporting delay | Normal p99 ≤200 ms; same error, duplicate, lateness and queue limits. EX-P99-007 cannot authorize this stage. On any breach or unknown sample, stop expansion and choose recovery; otherwise owner decides whether to expand to 100% |
| Closure / Release owner + Data owner | Approved 100% scope, prior-stage success and current evidence; 60 minutes plus 120-second reporting delay | Same normal thresholds, plus reconciliation proving no lost acknowledged reminders and no replay duplicates. Any discrepancy blocks closure and requires a recovery decision. Owner records closure only after evidence is complete |

The supplied fictional policy uses complete one-minute windows for live measurements. `fixture:E-METRICS-120` establishes only a synthetic measurement-readiness claim, not live monitoring. A rollout could also be blocked by missing production operator access; this packet does not grant it.

## Recovery branch: the migration changes the choice

1. **Before M042 clears legacy fields:** the preserved prior binary is a possible recovery option only if old readers still understand all written rows. The operator and data owner must verify that prerequisite rather than assume it from a green build.
2. **After cutover or any canonical-only writes:** a binary revert alone is unsafe. Build 417 requires legacy local-time/zone fields, skips new rows and cannot reconstruct cleared original timezone choices. Restoring the pre-cutover snapshot alone could discard acknowledged post-snapshot reminders.
3. **Stop and select a data-safe branch:** under actual operational authority, pause dispatch/writes as required by the approved recovery plan. The data owner must choose either a rehearsed forward-fix that can read both row forms, or an isolated snapshot restore plus a complete, deduplicated journal replay and reconciliation before switching service back. Neither branch is approved or proven by the present export. Preserve the failed rehearsal and the journal; do not invent an undo command.
4. **Required prerequisites:** preserved `fixture:rivet-build-417`, `fixture:pre-cutover-snapshot` and `fixture:append-only-dispatch-journal`; verified retention and journal completeness; authorized operator access; verified migration blast radius; a rehearsal covering migrated rows, new rows and old readers. Restoring a snapshot in isolation proves only one part.
5. **Recovery verification:** zero lost acknowledged reminders; zero duplicate sends; both migrated and post-cutover rows fire at the expected UTC instant; queue and error measurements return within policy limits with complete reporting. A restored process or successful deployment status is insufficient.

## Unresolved owner decisions

- **Data owner:** choose and approve the recovery strategy, establish migration blast radius/old-reader compatibility, and obtain a successful rehearsal covering new rows. If that requires code or migration changes, create a new immutable candidate and rebind evidence; the old results do not transfer automatically
- **Release owner:** establish the policy-approved resolution of E-RECOVERY-FAIL before same-candidate reassessment. This fixture has no rule that allows an unrelated newer pass to erase a current failure
- **Reminder QA owner:** obtain complete, fresh timing results for all four candidate identity fields. Asking whether to accept the previous build's pass is unnecessary because the supplied policy already disallows it
- **SRE lead:** if the window moves beyond EX-P99-007's scope or validity, obtain a normal G3 pass or an explicitly authorized new exception; do not extend the existing record
- **Release owner:** after the packet becomes advisory-ready, decide whether to authorize the exact release scope and later expansion separately. Existing scope review and exception approval do not answer this operational decision

## Reproduce the local logic checks

From this skill folder, with Python 3.9 or later:

```bash
python scripts/check-fictional-release.py
python scripts/check-fictional-release.py --report
```

The first command runs 21 standard-library test methods. The second prints the derived candidate-bound gate ledger and first-rollout planning checks as JSON. Both read the checked-in fixture, write no files, use no network, and run no build, migration, deployment or recovery command. The named-approver field must be nonblank text; missing, boolean, numeric or container values cannot satisfy it. This checks the supplied field's shape, not a real person's identity or authority.

| Independent synthetic evidence set | Expected recommendation | Blocking stage / decision |
| --- | --- | --- |
| Supplied input: current recovery failure, stale and wrong-candidate timing, valid narrow exception | hold | Preparation: G4 failed; G2 unknown |
| Counterfactual successful, approved recovery evidence; timing exports unchanged | unknown | Preparation: G2 still unknown |
| Same counterfactual recovery plus fresh current-candidate timing | ready_for_owner_decision | Evidence gates and the supplied 30-minute first-rollout plan pass; actual owner deployment authorization remains required |
| All normal gates pass, including p99 195 ms | ready_for_owner_decision | No exception is needed; owner still decides |
| Exception expires, covers the wrong cohort/stage, has the wrong approver/candidate, exceeds its ceiling, or does not cover reporting delay | hold | G3's raw failure remains effective |
| Additional newer passing recovery export while current failure remains unresolved | hold | A newer pass does not silently erase the current failure |
| Counterfactual successful evidence, but proposed and excepted window shortened to 12:10–12:11 | hold | First-rollout planning: one minute does not meet the 30-minute minimum |
| Counterfactual successful evidence, but first-rollout queue-age threshold is null | unknown | First-rollout planning: missing threshold blocks the stage |
| Counterfactual successful evidence and 30-minute scope starting at 11:55, before the noon assessment | hold | First-rollout planning: this policy requires a new proposed scope |

The counterfactuals modify copies in memory. They are separate hypothetical evidence sets, not instructions to edit a failed real export or proof of an actual rerun. Checks also reject missing/extra policy mappings, changed identity components, absent/non-finite measurements or planning thresholds, incomplete/future exports and attempts to waive another metric or gate. Wrong scope remains blocked even when G3 passes normally and no exception is used. The scope checks establish a complete plan only; they do not assert that the observation window ran or its live limits held.

**Verification boundary:** locally executed synthetic checks establish the described decision logic and fixture consistency. They do not establish source authenticity, production safety, live operator permissions, real guard behavior or successful end-to-end release execution.
