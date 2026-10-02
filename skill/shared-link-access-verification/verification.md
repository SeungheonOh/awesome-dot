# Verification and limits

Executed on 2026-10-02 using Python 3.12.14. All accounts, permission snapshots, organization constraints, receipts and recipient observations in this exercise are fictional. No service connection, authentication, notification or sharing change occurred.

## Checks run

From this skill's folder:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/evaluate_access.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_access.py
```

The evaluator exited 0 and produced three JSON artifacts. Each was reopened and compared with its computed result. The test suite ran 32 behavioral tests and returned `OK`. Skill frontmatter validation also passed.

The actual evaluator result was:

```json
{
  "change_review": "matches_fictional_approval",
  "before": {
    "priya@studio.example": "confirmed",
    "dana@guest.example": "absent",
    "morgan@studio.example": "unknown",
    "lee@studio.example": "blocked"
  },
  "after": {
    "priya@studio.example": "confirmed",
    "dana@guest.example": "confirmed",
    "morgan@studio.example": "unknown",
    "lee@studio.example": "blocked"
  },
  "live_actions_performed": 0
}
```

Every output records SHA-256 hashes for the exact request and both snapshots. Rerun after fixture changes; a hash binds the report to bytes but does not establish that the supplied evidence is true.

## Meaningful distinctions exercised

| Check | Observed behavior |
| --- | --- |
| Effective-route accounting | Direct, group, folder, shared-drive and link routes are represented separately |
| Owner opens file | Priya remains untested even though the owner succeeded |
| Restricted link | Casey's folder editor grant still permits viewing and editing; no link route remains |
| Unknown or hidden group membership | Morgan remains unknown, while a known nonmember with complete route coverage is absent |
| Known group member | Membership changed to `yes` supplies the group's actual commenter capabilities |
| Unknown higher role | A direct viewer remains confirmed for viewing, while possible editing through an unknown group stays unknown |
| Requested capability | A viewer is not reported as able to edit |
| Organization policy | Known block overrides an inherited grant; unknown policy prevents confirmation |
| Session identity | A wrong current account is reported separately from the intended account's grant |
| Invitation and expiry | Inactive grants and grants at their exact expiry instant contribute no access |
| Incomplete inventory | Missing routes cannot be presented as proven absence |
| Observation applicability | Wrong item, account, session account, action, revision and future timestamp cannot verify the intended recipient |
| Conflicting evidence | A current denial with configured access and contradictory current observations remain flagged |
| External account and link audience | An organization-only link excludes a known external account under this fictional contract; unknown link possession remains unknown |
| Authorized correction | Exactly Dana's direct viewer grant plus link restriction matches; inputs are unchanged by evaluation |
| Unapproved side effects | Ancestor removal, public-link widening, substituted account, notification and audience mismatch are held |
| Identity and scope integrity | Content revision mismatch, unknown grant origin and duplicate grant ID reject the packet |
| Bounded helper | Nonfictional input and a broader correction contract are rejected |

The evaluator never modifies the fixtures. It only reads local JSON and writes the three local output files. Tests change in-memory copies, not the saved permission snapshots.

A separate guide-only fictional case used non-additive child inheritance, a download block, exact-time expiry, cached owner/preview evidence and a wrong account. It kept those distinctions and retained uncertainty where an expired direct grant coexisted with unknown group membership. This review clarified separate entitlement/usability results for each requested capability and the fact that expiry removes one route rather than proving overall absence. The bundled evaluator remains limited to its stated fictional contract; the broader case was a separate evidence review.

## What remains untested

- Real provider semantics, live permission reads, membership freshness, identity resolution, authenticated effective-access APIs, actual recipient sessions and observed file opening
- Any live correction, propagation delay, failure recovery, concurrent permission change, readback receipt or notification behavior
- Folder trees and child-specific inheritance exceptions, nested groups, deny rules beyond the explicit per-recipient policy field, expiration of links, invitation redemption or provider-specific role capabilities
- Whether a real sharing panel exposes all routes or only the inspecting account's view; `coverage` is asserted fictional evidence, not something this helper can prove
- The authenticity of a recipient report, complete privacy review of document contents, and any guarantee that an account holder actually read or understood the document

The evaluator implements only [Workshop Files v1](fixtures/contract.md). No real product documentation is cited or implied. The workflow requires current official provider rules and actual authorized evidence before applying its distinctions to a real shared item.
