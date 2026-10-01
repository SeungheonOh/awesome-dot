# Worked Example: What Changed in the Evening-Hours Pilot?

This is a completed offline rehearsal using only the [fictional packet](references/fictional-source-packet.md). All sources, organizations and events are invented. The brief below is derived from the supplied passages; no live research, delivery, calendar update or recurring task occurred.

## Derived brief

**Topic:** Larkspur Quay Library Service evening-hours pilot at North and Quay

**Baseline:** `brief-2026-09-18-v1`, through September 18, 2026 at 18:00 UTC

**Update cutoff:** September 28, 2026 at 12:00 UTC

The planned first evening has moved one week later, and the earlier staffing claim needs correcting.

- **New plan:** The first pilot evening is now planned for **October 12**, replacing October 5. The service made the decision September 25 and published the amendment that afternoon, citing time for branch inspections. This is an announced plan change, not evidence the pilot has started. `[N1, amendment-v1, §change]`
- **Correction:** Replace “eight newly hired library assistants” with **“eight existing library assistants assigned to the pilot.”** The September 26 correction says the original September 16 notice misstated their employment status at the September 15 decision. This revises the account of an earlier fact; it does not announce a reduction of eight staff. `[P1, notice-v1, §staffing → P2, notice-v2, §§staffing/correction]`
- **Still holds:** The September 25 amendment reaffirms North and Quay, Monday hours of 18:00–20:00, and the planned December 14 end. This is a fresh official reaffirmation, not independent confirmation that any session has happened. `[N1, amendment-v1, §retained]`

**Implications:** For the provisional calendar, the evidence supports replacing the planned first date with October 12. It does not support publishing an exception-free session list: the branch exceptions register could not be read. Remove the prior brief's added-jobs interpretation; the correction supplies no basis for a forecast of hiring growth, job cuts or budget savings.

**Coverage limit:** The simulated register read failed at 11:08 UTC on September 28. The general plan is documented, but branch-specific exceptions remain unverified. This is a partial-coverage update, not an assurance that every possible change was found.

The recent grant recap and copied article add no separate development. The grant was already approved May 12 and covered in the baseline; the copied story repeats the superseded launch and staffing account.

## Comparison and source ledger

The bracketed references above point to source IDs, explicit fixture versions and passage keys in the packet. The packet retains the direct illustrative URL and retrieval time for every source. Those URLs are fictional locators, not live citations.

| Proposition or item | Before / newly retrieved evidence | Editorial result | Provenance and temporal basis |
| --- | --- | --- | --- |
| Pilot first date | October 5 → October 12 | New plan; amend B1 and calendar inference in B4 | P1 §plan → N1 §change; original decision September 15; follow-on decision September 25; planned effective date October 12 |
| Staff employment status | Eight newly hired → eight existing staff assigned | Correction; replace B2 and remove the added-jobs interpretation in B4 | P1 §staffing → P2 §§staffing/correction; same URL, retained v1 and v2; correction issued September 26 concerns September 15 assignment |
| Branches, Monday hours, end date | North and Quay; 18:00–20:00; December 14 | Confirmation of plan; retain those parts of B1 | N1 §retained explicitly reaffirms the original terms; official reaffirmation, no separate firsthand observation |
| Grant | $60,000 approved May 12; recap published September 22 | Unchanged; retain B3, omit from lead | G0 §decision and R1 §recap are the same decision and amount; R1 explicitly republishes G0 |
| Copied pilot story | September 24 article repeats September 16 notice | No added development; do not use to support the current staffing or start-date claims | D1 §report identifies P1 as its sole source and adds no reporting; its later publication is not a new decision |
| Exceptions register | No content returned | Unresolved coverage | X1 is a failed read; no evidence of “no exceptions” or of cancellation |
| Later withdrawal | September 29 notice rescinds the announced pilot | Outside this brief's cutoff | L1 was first available after September 28 noon; keep it outside the as-of result |

The same N1 amendment supports both a changed first date and reaffirmed conditions. These are proposition-level classifications within one decision, not separate events created to inflate a news count. P2 describes the old pilot decision and the later correction; collapsing the entire document into one date would erase that distinction.

“Unchanged” for D1 describes its lack of additional evidence. Its claims are stale in the current account; it does not override N1 or P2. The sources do not need to be tallied as votes: the copied claim has a known origin, and the applicable official records explicitly amend or correct it.

## Date and version audit

```text
G0: event May 12; original publication May 13; prior capture September 18
R1: same May 12 event; new publication September 22; capture September 28
    New publication within the update window, already-known underlying decision

P1: original pilot decision September 15; publication September 16
    Version notice-v1 retained from September 18, before the baseline cutoff
D1: article publication September 24; underlying decision September 15
    Explicitly derived from notice-v1; no additional reporting

N1: new decision September 25; publication September 25 at 14:00 UTC
    Planned start October 12; planned end December 14
    First-date difference: October 12 − October 5 = 7 calendar days
    This does not establish a shorter actual operating period or completed opening

P2: original publication September 16; correction September 26 at 10:00 UTC
    The corrected version was available within the update window
    Employment status concerns September 15; September 26 is the correction date
    A publication-date-only filter would miss this material update

X1: attempted read September 28 at 11:08 UTC; version/content unavailable
    Failed retrieval supplies a gap, not an event date or a no-change result

L1: decision and publication September 29; capture September 29
    Excluded from a September 28 as-of brief despite being supplied in the packet
```

No eligible inspected source withdraws the pilot as of this brief's cutoff. That statement is bounded to the inspected sources and does not erase the register gap. If a separate brief used a September 29 cutoff after L1's publication, L1 would support a withdrawal of the announced plan. It would not imply that the earlier plan had never existed.

## Why the classifications are defensible

- R1 and G0 explicitly concern the same council decision, date, branches and amount, with a direct republication relationship. This is stronger than headline similarity
- D1 declares P1 its sole source; two publishers therefore do not supply two independent observations. P2 preserves the original event while correcting the earlier wording
- N1 cites the old plan to amend it. That citation does not make N1 a derivative repetition: it explicitly records a follow-on decision
- N1's inspection explanation is attributed to the service. The packet contains no independent evidence that inspections will be completed or that October 12 will be achieved
- P2 expressly denies a newly announced staffing change. The old added-jobs interpretation is removed without replacing it with an unsupported jobs-loss narrative
- The historical grant is suppressed here because the baseline already covered it. An earlier event newly discovered by a different brief could be material and should be labeled newly learned historical context
- The incomplete register cannot support a claim about all branch sessions, even though the general amendment is readable

## Executed offline checks

Run from this skill's directory:

```bash
python3 scripts/check-packet.py
```

Observed output:

```text
PASS: baseline and comparison locators resolve to eligible retained passages
PASS: explicit recap/copy provenance stays with the original events
PASS: same-URL staffing correction retains both versions and the original event date
PASS: publication/update/event/retrieval boundaries preserve gaps and exclude later evidence
PASS: planned first evening moves seven calendar days; planned end is unchanged
PASS: annotated derivative coverage adds no development; amendment and correction remain separate
LIMIT: event identities and semantic labels were supplied and reviewed, not automatically established
```

The date checks include a version available exactly at the cutoff expressed in a different offset, one available a second too late, a later retrieval of an evidenced historical version, an unknown version-availability date and a failed read. The provenance checks reject missing references and cycles in declared derivative edges, and distinguish a mere citation from a declared derivative relationship. The same-URL check ensures the old and corrected passages remain separately addressable.

These checks establish internal fixture consistency and the seven-day calculation. They do not authenticate reporting, perform live search, decide general semantic equivalence, prove exhaustive coverage, or verify an actual delivery or recurring setup. The before/after classifications and implications were reviewed against the supplied passages rather than generated by a generic news aggregator.
