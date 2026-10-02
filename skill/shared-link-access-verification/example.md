# A restricted link with different access outcomes

Everything in this example is fictional. The JSON permission snapshots and recipient report were authored for this exercise. The generated matrices are real local artifacts, but no file was shared, no person was contacted and no live application was tested.

## Request and evidence

> Check whether Priya, Dana, Morgan and Lee can view Workshop plan. The ordinary workshop content is approved for these four accounts. You may add Dana as viewer on this file and set its organization link to restricted. Do not change other permissions or contact anyone.

The [request packet](fixtures/request.json) resolves each fictional account. The target is file `file-042`, content revision `content-7`, owned by `owner@studio.example`, in folder `folder-017` under shared drive `drive-004`. The [contract](fixtures/contract.md) defines the behavior used here. These IDs and reserved `.example` addresses do not identify real items or people.

The [before snapshot](fixtures/before.json) claims complete route coverage at permission revision `perm-11`, 2026-09-18 10:00 UTC:

- The organization link grants viewer access only to known organization members who hold the link
- Priya has a direct viewer grant
- The Review Circle group has a commenter grant; Morgan's group membership and organization membership are unknown
- Lee has an inherited shared-drive editor grant, but an organization policy blocks Lee's use of this file
- Casey, an incidental former attendee, retains an editor grant from the parent folder
- The only opening observation is the owner's own success. Dana's supplied session record names a different account

“Restricted” is not a claim that only the names visible in one share panel can open the file. The full route inventory matters.

## Recipient/access matrix

The permission column concerns the requested viewing capability. Actual opening evidence is recorded separately. All account identities and observations below are synthetic.

| Intended recipient | Before | Minimal action within approval | After snapshot | Opening evidence after |
| --- | --- | --- | --- | --- |
| Priya, `priya@studio.example` | Viewing confirmed through direct viewer grant and organization link | Preserve direct grant | Viewing confirmed by unchanged direct grant after link restriction | Untested; owner success is not Priya's success |
| Dana, `dana@guest.example` | No viewing grant under complete coverage; different account in the supplied session | Add this exact account as direct viewer on this exact file | Viewing confirmed by new `grant-dana`; matching account in updated session evidence | Synthetic recipient report of successful viewing of this file at `perm-12` |
| Morgan, `morgan@studio.example` | Unknown group and organization membership; no proven viewing route | Obtain authoritative membership evidence if accessible; no new grant approved | Still unknown through Review Circle; link restriction cannot resolve membership | Untested |
| Lee, `lee@studio.example` | Inherited editor grant exists, but organization policy blocks use | Report the precise blocker; no policy or ancestor change approved | Still blocked; shared-drive grant remains | Untested |

Dana's missing permission and wrong account are independent findings. Granting `dana.personal@guest.example` would disclose the document to an unapproved account. A changed session in the fictional after snapshot is recipient evidence, not an action the helper takes.

## Exact proposed correction and simulated result

The authorized plan has two item-local changes: add Dana's direct viewer grant and change the organization link to restricted. It leaves the file's contents, identity, owner, parent chain, group memberships, policy, existing grants and notification state unchanged. Both changes were already specified in the fictional request, so a real equivalent would not require repeating that approval if the same preconditions still held.

The [after snapshot](fixtures/after.json), at `perm-12`, 2026-09-18 10:06 UTC, contains exactly those simulated permission changes and an explicit synthetic receipt. Readback-style evidence includes the resulting link setting, new grant ID, original unchanged grants and updated recipient observation. The [delta review](outputs/change-review.json) checks the state difference against the bounded request; it does not submit anything or validate an actual service receipt.

The intended audience still has two unresolved rows. A useful result is therefore:

> In this fictional readback, Dana now has the approved viewer grant and reports opening the exact file. Priya's viewer permission remains present, but Priya's opening is untested. Morgan's membership is unknown, and Lee remains blocked by organization policy. The link is restricted. Casey's inherited editor access persists through the parent folder, so this change did not revoke Casey's access.

Casey is kept in the incidental-access section, not added to the intended audience. Removing Casey's folder grant could affect other files. That change is outside this request and is not performed or proposed as an automatic fix. The user would need to decide the precise broader scope if removal were desired.

## Reusable artifacts and evidence limits

- [Matrix template](matrix-template.md): use with real authorized evidence and current provider rules
- [Before matrix](outputs/before-matrix.json) and [after matrix](outputs/after-matrix.json): one row per intended account, plus a separately labeled incidental route check
- [Change review](outputs/change-review.json): exact simulated delta, source hashes and zero live actions
- [Verification record](verification.md): executed behavioral checks and what they do not establish

The helper's `grant_capability_floor` means capabilities supported by known grants before policy is applied. It is not a claim of usable access for a policy-blocked account. `additional_possible_capabilities` preserves uncertainty about higher roles; it must not be presented as a granted role.

For a real task, permission and membership observations must come from the actual supported provider views, and opening evidence must come from an authorized recipient-side check or report. Neither this example's invented contract nor a local passing test can replace those observations.
