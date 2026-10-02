# Fictional permission contract: Workshop Files v1

This is an invented service contract for an offline exercise. It describes no real product or live account. Every snapshot, account, grant, observation and operation receipt is synthetic. The evaluator does not authenticate these facts.

## Scope and evidence

The snapshot describes one file, its full relevant ancestor chain, permission revision and observation time. `coverage: complete` asserts that all relevant grant routes are present; `partial` cannot prove their absence. Ancestors are identified explicitly as folder or shared drive. A grant's `source_id` must equal the file ID or a listed ancestor; unexplained provenance rejects the packet.

Recipients use exact, case-sensitive account identifiers supplied by the fictional request. No alias matching, nested groups or directory discovery occurs. Group membership is an exact per-account map with values `yes`, `no` or `unknown`; a missing entry is unknown. Only the stated intended recipients enter the delivery matrix. Other evidenced people may be inspected separately for a bounded access-persistence check.

## Effective permission

- Viewer permits view; commenter permits view and comment; editor permits view, comment and edit. An owner can inspect and open their own file but is never substituted for a recipient
- Active, unexpired person grants match exact accounts. Group grants match only known members. All direct, folder and shared-drive grants in this contract are additive; inherited grants are not removed by changing a link
- `restricted` contributes no link grant. `organization` contributes a viewer route only for known members of the snapshot's organization who possess the exact link. `anyone` contributes a viewer route for known link holders. Unknown organization membership or link possession makes an otherwise plausible route unknown
- A known route supporting the requested capability establishes a permission floor. Higher capabilities from unknown routes remain unknown. A known route to viewing cannot establish editing
- `policy: blocked` overrides all grants for that recipient. `policy: unknown` prevents a positive permission conclusion. `policy: allowed` permits evaluation of routes. This field represents organization restrictions, not a bypassable error
- With no sufficient route, unknown membership/link eligibility or partial coverage yields `unknown`; only complete coverage with no possible sufficient route yields `absent`
- An active grant may have `expires_at`. At that exact instant and thereafter it contributes no route. A pending invitation is represented by `active: false` and contributes no active route

## Session and observation

Permission and session evidence are separate. A session principal different from the intended recipient is `wrong_account`; an absent session is `untested`. Neither removes a valid grant or proves the intended recipient opened anything. An observation counts for opening only when its file ID, exact account, requested action, permission revision and session account match and its timestamp is no later than the snapshot. Its kind is either `recipient_report` or `authorized_observation`; a matching result is success or denied. More than one contradictory current result is `conflicting`.

An owner success, stale revision, wrong item or different account is excluded from recipient proof. A valid current denial contradicting otherwise sufficient configured permission is reported separately; the evaluator does not turn it into success or automatically mutate access.

## Authorized change fixture

The request permits exactly two changes on file `file-042`: set the organization link to restricted and add `dana@guest.example` as a direct viewer. The ordinary workshop content is approved for Dana. It permits no group, parent, policy, content, owner, other recipient, public-link or notification change. The delta check compares every state field except evidence-only `captured_at`, `permission_revision`, sessions, observations and the simulated receipt. It validates one new active viewer grant with no expiration, leaving all prior grants unchanged. It does not execute or authorize an external action.
