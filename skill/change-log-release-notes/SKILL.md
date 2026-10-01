---
name: change-log-release-notes
description: "Turn supplied changes and release evidence into audience-specific release notes, preserving rollout limits, compatibility requirements, and unresolved claims, then write to the authorized destination."
---

# Write Release Notes from Verified Changes

Produce release notes someone can use to decide what is available, what changed, and whether they need to act. Transform the engineering record without turning a merged change, hopeful title, or rollout plan into a shipping claim.

Use this for a changelog, product update, developer release note, or support-facing change brief based on supplied or authorized sources. Match the destination's established format. Do not require the user to fill out a template when the necessary details are already present.

## Identify the release and readers

Read the request, supplied changes, relevant release record, and any existing destination before drafting. Establish:

- The product, version or bounded change window, and the source snapshot being summarized
- The audience and channel: customers, integration developers, support staff, or an internal team
- Whether the requested artifact is a draft, a local changelog edit, an update to a named document, or a public publication
- Evidence for actual availability, including platform, plan, region, cohort, feature flag, version, and date where applicable
- Any requested tone, length, terminology, or required sections

If the intended audience is unclear but low-risk, use a plainly stated assumption and prepare a draft. Ask when a missing fact would materially change correctness, such as whether a breaking change has shipped, or when a missing destination prevents the requested write. Continue the supported portions while an unresolved claim remains open.

## Build a compact change-to-claim ledger

Give each source item a stable identifier or retain its supplied ID. Read beyond titles: use descriptions, acceptance criteria, relevant diff context, release manifests, rollout records, and known limitations as available. A source can establish one fact without establishing another.

For each meaningful change, record:

- **Behavior:** what users could do before and can do after; distinguish a new capability from a bug fix or internal refactor
- **Release state:** implemented, merged, packaged, deployed, pilot, preview, generally available, paused, rolled back, or unknown, using the source's actual wording
- **Availability:** who can use it, where, how to enable it, and when that state was checked
- **Impact:** affected workflows, compatibility, user action, migration steps, and limits
- **Evidence:** the precise source or excerpt supporting each proposed claim
- **Disposition:** include, combine with a related item, omit as irrelevant to this audience, or hold for missing/conflicting evidence

Deduplicate commits, pull requests, and issue entries describing the same behavior. Retain distinct rollout or platform differences. Account for every supplied item, but do not force internal cleanup into customer-facing prose.

Use each source for facts it can establish. A diff may prove a code change; the release manifest may establish inclusion; an actual rollout record may establish who has it. A planned date does not prove release. If sources disagree, compare their timestamps, versions, and authority for the specific fact. Preserve the conflict when those checks do not resolve it.

## Draft for the audience

Lead with consequential changes and required action. Use concise behavior-first statements rather than commit titles or implementation chronology. Group related items when that improves comprehension, while retaining each distinct limit.

- **Customers:** explain what changed in their workflow, how to access it, and any material limitation. Translate internal terms but preserve product labels they need to find a control
- **Developers:** keep API or schema names exact, include old/new contracts, error behavior, supported versions, migration actions, and compatibility limits
- **Support or internal readers:** include rollout state, affected cohorts, known issues, a response or escalation route only if supplied, and facts needed to avoid promising unavailable behavior

For each bullet, distinguish benefit from evidence. “Export now preserves accented titles” describes an observed fix; “exports are always accurate” overclaims. Do not add performance numbers, guarantees, pricing changes, security assurances, compliance claims, removal dates, or “no action required” without specific support.

Preserve important qualifications close to the claim they qualify. Do not move a beta label, opt-in requirement, affected plan, or breaking limit to an obscure footnote. Use dates with years when ambiguity matters, and retain the supplied time zone for time-sensitive rollouts. Do not invent a date or version to make the heading look complete.

Keep future and unreleased work out of a shipped section. Include it only if the user requested a roadmap or upcoming section, with its status explicit. If a rollback supersedes a deployment, describe the current state and the relevant transition instead of claiming the earlier availability still holds.

## Check both coverage and meaning

Perform two passes before writing the final artifact:

1. **Notes to sources:** trace every factual statement, number, availability claim, and user action to evidence. Check that your paraphrase has not broadened “web pilot” to “all users,” “merged” to “available,” or one corrected case to a general reliability promise.
2. **Sources to notes:** account for every supplied change in the ledger. Confirm that removals, breaking changes, action requirements, known limits, and delayed availability have not disappeared during shortening. Omission needs an audience or release-scope reason; lack of evidence becomes an open item.

Check links against the authorized source or known destination. Public notes must not reveal private issue titles, customer names, access-restricted URLs, secrets, or internal discussion. Retain private evidence in the authorized review material; use public documentation links only when verified and suitable for the audience.

Review the draft as the reader: could they tell whether the change applies to them, how to use it, and what they need to change? If the requested space limit cannot preserve a critical warning, keep the warning and explain the length tradeoff rather than silently dropping it.

## Write, verify, and hand back

Use the destination and authority already given:

- If the user requested a local changelog edit, make that scoped edit. Preserve the file's existing headings, ordering, history, links, and unrelated edits
- If the user requested a draft in a named document, write it there using the available supported tool and keep its draft status
- If the user asked only for wording, deliver the draft in the conversation or requested file
- If publication is explicitly authorized and within the available permissions, publish the approved scope and verify the resulting content and visibility. A drafting request alone does not authorize publishing, notifying subscribers, changing sharing settings, creating a release tag, or modifying a remote release

Do not ask again to perform a write that was already requested. Ask for the exact missing approval or destination only when it is needed. Do not fabricate a successful write if a tool or permission blocks it; return the complete draft and the concrete blocker.

After a write, read the destination back. Compare the saved text with the intended notes, check headings and links, and confirm that important restrictions and existing content survived. A tool success response alone is not evidence that the right release or section was updated.

Return the notes or verified destination link, a concise statement of what was written and its publication state, and any unresolved claims or decisions. For a substantial release, include the change-to-claim ledger as review material rather than exposing internal evidence in the public notes. Label unconfirmed claims as editorial questions, not finished copy.

## Worked example

Read [EXAMPLE.md](EXAMPLE.md) for a fictional release packet, customer and developer versions, and a complete coverage ledger. The example includes a pilot feature, an API breaking limit, a held performance claim, and a merged but unreleased feature.

Example request:

```text
Use this supplied release packet to update the draft 2.6 section of our local CHANGELOG.md. The readers maintain integrations. Preserve exact API names, rollout limits, and migration actions; leave older releases untouched. Keep unsupported claims in a separate review list. The local edit is authorized; do not publish the release or notify anyone.
```
