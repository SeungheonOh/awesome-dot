---
name: product-announcement-reality-check
description: "Translate a product announcement into a versioned capability-and-availability assessment for a specific use case, separating shipped access from demonstrations and promises."
---

# Product Announcement Reality Check

Turn a launch page or product claim into an answer to “Can this documented release meet these requirements under these access conditions?” Produce a capability matrix, an evidence-backed bottom line and a short list of remaining gates. The goal is to remove practical uncertainty, not to summarize marketing or predict a company's prospects.

## Pin down the product and use case

Get the original announcement, exact product identity, capabilities of interest and intended use case. Confirm version, region, platform, plan and access type wherever they affect availability. If the user does not know the plan or version, mark them unknown and branch the result rather than guessing. Keep private workflow details out of public search queries.

Record the inputs in this shape:

```text
request:
  product_and_vendor
  announcement_locator
  target_version_or_release_channel
  cutoff_with_timezone
  region, platform, plan, user_or_org_access_conditions
  requirements: [{id, needed_behavior, acceptance_condition, must_have}]
  evidence_scope: permitted sources and any explicitly authorized testing
  output_and_delivery: format, destination, audience, authorized action
```

Turn vague requirements into observable ones. “Works offline” might mean opening previously cached notes, searching attachment contents or creating new material without a connection. Those are different capabilities. Ask which behavior matters when the distinction changes the answer; do not let a product's feature name define the user's requirement for them.

## Investigate the release

1. **Retrieve the announcement and establish its claims.** Open the original accessible source during the run. Separate what it says is available now, rolling out, invitation-only, planned or merely demonstrated. Record exact product and feature names, publication/update times, stated release or availability dates and retrieval time. Preserve an announced future date as a plan until later evidence establishes delivery. A recent article about an old launch is not a new release.

2. **Find implementation and access evidence.** Retrieve the relevant documentation, release notes, supported-platform list and plan or eligibility descriptions. Prefer a specific versioned capability page over a broad slogan. Official documentation is authoritative for the vendor's documented conditions but may itself be stale, incomplete or inconsistent. Open the actual section; search snippets and link titles do not establish support. Record blocked pages and inspected coverage instead of filling gaps from memory.

3. **Normalize product naming and versions.** Map renamed features to their documented equivalents using an explicit source. Do not merge similarly named consumer and enterprise products, desktop and web features, or stable and preview channels. If current documentation covers a later version than the requested one, find an applicable version or mark the earlier version unresolved. A redirect to a new name alone does not prove unchanged behavior.

4. **Classify capability and availability separately.** For each requirement, assess documented behavior as supported, partially supported, explicitly unsupported or unknown. Then assign access as generally available within stated scope, rolling out, limited preview, waitlist, announced future, retired or unclear. A working demo can establish an observed behavior under its visible conditions; it cannot establish broad access. A feature can be shipped for one plan and unavailable to the user's stated plan without being unshipped everywhere.

5. **Inspect independent evidence when it changes the answer.** Record a review or test's author, date, product build, platform, account conditions, inputs, method and observed result where provided. Separate hands-on observation from opinion or a republished vendor claim. Several articles using the same demonstration are one underlying observation. Do not write “tested” as your own action unless you actually performed an authorized test; distinguish documented support, another party's observation and your own observed result.

6. **Resolve mismatches through scope and chronology.** Compare conflicting sources by version, platform, plan, geography, rollout window and feature definition. A launch-wide “today” can coexist with plan-specific eligibility, but that limitation must appear in the bottom line. If documents conflict on the same scope, look for a superseding release note or explicit correction. If none resolves it, retain both claims and mark the gate unresolved; do not pick the more convenient source. Treat missing documentation as unknown unless an applicable source explicitly rules out the behavior.

7. **Evaluate the user's requirements.** Connect every must-have to the behavior and access records. Report “documented to meet,” “documented partial match,” “documented mismatch,” or “unresolved,” with the condition behind each status. Do not collapse unknown into unsupported or infer that a preview invitation is obtainable. If all must-haves have applicable support, say the sources support proceeding to the user's requested next step, while distinguishing documentation review from actual acceptance testing. Do not promise reliability merely because availability is documented.

8. **Complete the requested deliverable.** Write the matrix and brief in the requested format, retaining evidence links and the retrieval cutoff. Save to the authorized destination and perform any explicitly requested routine delivery to the specified audience. Inspect the saved content and verify the resulting reference or delivery result. Do not ask again for unchanged, already-authorized routine handoffs. If the user requested actual evaluation as well, execute only tests within the authorized environment and scope, or identify the exact missing access; never claim source research completed a functional test.

## Return a usable evidence record

```text
capability:
  requirement_id, user_needed_behavior, product_feature_name, naming_alias_evidence
  behavior_status, access_status
  version, platform, plan, region, rollout_or_invitation_conditions
  stated_availability_date, evidence_ids, limitations
  requirement_result, remaining_gate
source:
  id, title, issuer_or_author, direct_locator, exact_section, source_type
  publication_time, update_time, retrieval_time, event_or_availability_time
  applicable_version_and_scope, access_coverage, originating_evidence_id
observation:
  evidence_id, observer, method, build_and_environment, inputs, result,
  visible_limits, performed_here_or_reported_by_source
brief:
  bottom_line_for_use_case, documented_matches, material_mismatches,
  unknown_gates, next_authorized_step, cutoff, search_limits
delivery_and_checks:
  artifact_reference, actual_delivery_state,
  [{check, observed_result_or_unrun_reason}]
```

Use “not stated” for missing source fields. Do not invent dates, regions, plan mappings or probability-based confidence scores. Link precise sections and distinguish the vendor's assertion from independent confirmation.

## Check the conclusion and boundaries

Recheck every decisive requirement against a retrieved passage. Test the classification logic using an announced-but-unreleased feature, a region- or plan-limited release and a renamed feature. Confirm that a demonstration is not labeled general availability, a failed search is not labeled absence and third-party testing is not described as your own. For a historical cutoff, exclude later evidence from what was knowable then; record whether the inspected version actually existed at that boundary.

Stop when the requested capabilities have applicable evidence or clearly described gaps, and further generic coverage would not settle those gaps. Ask for a materially missing plan, region or definition. Account creation, installation, paid access, purchasing, accepting new terms, requesting invitations or sharing private requirements require the appropriate authorization; a research request alone does not grant it. Do not automatically contact a vendor or start release monitoring to compensate for incomplete evidence. Complete the supported artifact even when a capability remains uncertain.

## Worked example

[The fictional offline-workspace launch](examples/fictional-offline-workspace.md) contains supplied mock sources and expected analysis. It demonstrates a renamed feature, platform and plan restrictions, a rollout promise and independent test evidence limited to one build. The example does not establish that any actual product exists or that live research or testing ran.
