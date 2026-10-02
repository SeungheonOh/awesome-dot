---
name: shared-link-access-verification
description: "Verify who can use a specific shared file or folder link, trace direct and inherited access, and make only scoped, already-authorized sharing corrections with readback evidence."
---

# Verify a Shared Link for Its Intended Readers

Produce a recipient/access matrix for the exact item and the smallest supported correction. Distinguish configured permission from a recipient actually opening the item. An owner opening their own link establishes neither recipient access nor appropriate audience scope.

This workflow checks access to an existing item. It does not minimize document contents, file a collection, publish a document or prove that recipients have read it.

## Establish the boundary

Resolve these from the request and authorized records before asking for missing details:

- Exact link, service/account, stable item ID, owner, item type and requested version; identify shortcuts, previews and folder links separately from their targets
- Intended people or bounded group, verified account identifiers, requested capability such as view or edit, and whether delivery itself is requested
- Data approved for that audience and the permitted changes: inspection only, specific grants, specific removals or link-setting change
- Evidence available to this account: permission details, parent/shared-drive grants, membership visibility, organization rules and recipient-side observations

An existing approval naming the file/data, audience and access change remains sufficient; do not demand another approval just because verification is complete. A request to check a link does not authorize changing permissions. Resolve ambiguous recipients using authorized records; never guess an email, substitute a similarly named account or infer group membership from a display name. Do not solicit credentials or change authentication settings.

## 1. Bind the evidence to one item

Resolve the link through the service's supported interface. Record item ID, version or revision evidence, owner, parent chain, retrieval time and the account doing the inspection. A redirect, shortcut or duplicate filename can lead to a different object. Do not follow unrelated linked documents.

Capture relevant permission details with pagination and coverage limits. Record where each route originates: link audience, direct person grant, group grant, parent folder or shared-drive membership. Include role/capabilities, expiration, invitation or activation state, membership evidence and the scope on which a grant can actually be changed. Keep sensitive link tokens and unnecessary membership lists out of reports.

For real products, consult current official documentation and supported permission views for inheritance, restricted folders, group expansion, link scope, expiry and organization policy. Record sources and observation time. Some restrictions override grants; some role names omit capabilities. Do not import the fictional example's additive rules into a real service.

## 2. Build an evidence-backed recipient and capability matrix

Use the [matrix template](matrix-template.md). Evaluate the requested capability, not merely the presence of a name in a sharing panel.

When requested capabilities have different outcomes, keep separate entitlement and usability results for each. For example, confirmed viewing does not establish downloading, and a download block does not erase an otherwise valid viewing route. Use separate rows or clearly separate capability fields for the same recipient; do not collapse them into one green/red status.

| Evidence pattern | Action and conclusion |
| --- | --- |
| Applicable direct grant | Match the exact recipient account and capability; check policy, activation and expiry before calling permission confirmed |
| Folder or shared-drive grant | Trace it to the actual ancestor and applicable inheritance rules; changing this file's link may leave that access intact |
| Group grant, known membership | Record the authoritative membership evidence and freshness, including nested groups when relevant |
| Group grant, hidden or unknown membership | Leave that route unknown; do not equate hidden membership with absence or add a redundant grant merely to make the row green |
| No matching grant | Call it absent only if all relevant permission routes were inspected; incomplete lists or inaccessible ancestors leave it unknown |
| Organization or session constraint | Separate entitlement from current usability: external-sharing policy, required organization, accepted invitation, signed-in account or supported session requirement may block a valid-looking grant |
| Owner opens successfully | Record owner-only evidence; leave intended recipient usability untested |
| Recipient-side evidence | Require the exact item, intended account, action, time and relevant permission revision; distinguish a recipient report from a directly observed supported check |

Record confirmed routes and unresolved routes separately. A confirmed view grant may prove viewing entitlement while an unknown group grant still leaves the highest effective role uncertain. A missing edit control may be correct for a viewer. A screenshot of a file title or a successful preview does not necessarily establish opening the requested document or downloading it.

Expiry removes the expired entitlement route at the provider's defined boundary; it does not establish overall absence while another direct, inherited or unresolved group route remains.

Do not sign in as another person, borrow their session, manufacture a test account or bypass a restriction. Use an available authorized effective-access feature or existing recipient evidence. If neither exists, report “permission configured; recipient opening not tested.” Ask for one relevant observation only when needed; do not automatically message owners, recipients or group administrators. An anonymous test, if authorized and appropriate to the requested link audience, cannot verify a named person's access.

## 3. Choose and perform the narrow correction

Compare desired capability with observed evidence. Preserve already-correct rows.

- Missing direct access: add only the verified recipient and necessary role to the named item when that file/data/audience change is already authorized and the service permits it
- Wrong account in use: identify the mismatch and supported sign-in choice; do not grant an unintended account access as a workaround
- Group or ancestor ambiguity: request the missing evidence or decision; a direct grant is a separate sharing change and may outlive group membership
- Excess or inherited access: show the originating grant and effect of its removal. Do not remove a folder/shared-drive/group grant, move the file or alter membership to fix a file-only request
- Organization block or unsupported scope: report the exact blocker and smallest supported next step. Do not weaken policy, make a file public or create a publicly accessible copy

Before mutation, match the live item ID, data/version, recipient, capability, access boundary and any notification behavior against the existing approval. Refresh changed preconditions. Ask only for missing authority or a material scope change, with a concrete proposal. Use a supported no-notification option when available and appropriate; disclose unavoidable notifications if they materially change what was approved. Never send a separate “try it now” message without authorization.

Perform authorized ordinary changes without a redundant approval step. Record before/after permission IDs and the service result. After a timeout, inspect the current state before retrying; adding the same person twice or toggling link settings blindly is not a verification method. A successful update response alone is not readback.

## 4. Recheck effective access and return a bounded result

Re-read the exact item and all permission routes affected by the change. Verify intended grants and link audience, unchanged unrelated access, and the role the recipient can actually receive. Restricting a link does not prove every prior recipient lost access; check direct and inherited routes. For folders, verify the requested child scope and exceptions rather than treating one child's success as proof for the entire tree.

Use current authorized recipient-side evidence if available. Record the outcome as permission confirmed, absent, blocked or unknown, with recipient opening separately observed, reported, failed or untested. Propagation delays remain pending until supported readback resolves them; an old observation does not certify the new state. If the desired result conflicts with the evidence, hold the affected claim and retain the rest of the matrix.

Return the exact item link or identifier, the matrix, changes actually made, their readback evidence, unresolved rows and the smallest needed decision. Keep the access report private unless its own audience is approved; it can expose membership or access details beyond the document itself. Do not claim “everyone can open it” from configured permissions alone.

## Worked example and checks

[The example](example.md) uses wholly fictional permission snapshots and an explicit [fictional contract](fixtures/contract.md). Its [offline evaluator](scripts/evaluate_access.py) checks access routes, uncertainty and approved before/after deltas; it never contacts a service or changes permissions. Run from this folder:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/evaluate_access.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_access.py
```

Read [verification](verification.md) for actual executed checks and their limits. A passing fixture is not live access verification.
