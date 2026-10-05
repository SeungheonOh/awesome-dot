# Identity, import authority, and read models

Read this when the app moves data across a file boundary or presents related/aggregated facts. Reuse the application contract's meanings and transaction policy. The importer, report, and export are consumers of the same stored facts.

## Distinguish three identities

Identify only the identities the task actually needs:

- **Domain identity:** which continuing object or individual occurrence is being stored
- **Source identity:** which source record or event an import represents, including its namespace
- **Operation identity:** which attempted command is being repeated, when resolving uncertain outcomes requires it

These may coincide, but do not assume so. A stable source event key can be enough for repeatable ingestion without a general request ledger. A filename and row number identify a row in one immutable file, not necessarily the same event in a later reordered export. A content digest can establish equal content, but cannot distinguish two legitimate occurrences whose values are equal. A display name need not be unique or stable.

Select a stored key or mapping that survives the user's intended edits. State deletion and identity-reuse behavior if it affects replay. Keep a source namespace when keys are only locally unique. If source identity is absent, choose an explicit append-only import, a user-approved matching rule, or a hold for ambiguity. Do not silently promise deduplication that the data cannot support.

## Choose what imported data is allowed to change

Separate the source's last accepted representation from the current editable state when their roles differ. A timestamp called `updated` does not settle who may overwrite whom.

For each relevant input situation, decide the result before choosing SQL:

| Situation | Decision needed |
| --- | --- |
| New unambiguous identity | Whether creation is allowed, required values, generated target key |
| Same identity and same accepted source content | No-op, replay receipt, or reapplication under an explicitly chosen policy |
| Same source identity but changed source content | Authorized update with guards, new revision, conflict, or held correction |
| Current local fields differ after an accepted edit | Which fields the source owns; whether to preserve, reject, or deliberately replace |
| Multiple possible target identities | Resolve from stronger evidence or hold; no accidental first match |
| Omitted, blank, or explicit-clear field | Preserve, default, clear, or reject according to create/update semantics |

For example, if the user wants local corrections to survive an unchanged source replay, retain enough accepted source content or a defined digest to distinguish that replay from changed input. Comparing solely with current edited values would misclassify it. If the source is authoritative instead, specify the permitted fields and freshness rule. Neither policy is a universal default.

When hashing content, define whether identity refers to raw file bytes or parsed semantic values, along with field order, null encoding, and any normalization. Only normalize what the contract authorizes. Retain information needed to explain a conflict; a digest is not a recoverable copy of the original content.

Apply source-identity/provenance changes and the associated domain changes in the same transaction when they form one accepted import effect. An importer can call transaction-bound domain helpers beneath its own batch owner; it should not call an independently committing public command once per row when promising whole-batch atomicity.

## Parse, classify, and commit the actual input

Use the real saved input with a format-aware parser. Preserve textual identifiers, Unicode, quotes, newlines, and significant whitespace. Define conversion for numbers, dates, nulls, missing fields, and explicit controls. A successful numeric cast is not proof that the original input was valid. Store formula-like text literally where that is the contract; a spreadsheet-facing view may need a separate presentation treatment rather than altering machine-import values.

Choose whole-batch, per-item, or another stated commit unit from the user's task. Preflight can catch shape errors and conflicting duplicate keys, but it does not replace state-dependent checks at commit time. If several input rows refer to the same identity, define a sequence or reject/hold the conflict instead of letting file order accidentally choose a winner.

Account for source records as created, updated, unchanged, rejected, or unresolved using terms the app actually supports. In a rejected atomic batch, distinguish the proposed dispositions from committed effects: earlier valid rows were not created merely because parsing reached them. For partial success, return enough per-item outcome information to retry only eligible work.

Reopen the database and inspect both domain values and the mapping/provenance the policy relies on. Challenge the consequential rule through the importer itself: a local edit followed by replay, changed content under an existing key, or a late invalid row after earlier valid work. Compare before/after identities and values, not only inserted-row counts.

If commit succeeds but the caller loses the result, resolve with the chosen stable identity and any durable evidence before submitting again. The absence of a row may be inconclusive if deletion is allowed. Define retention only when a replay promise depends on it; do not invent indefinite exactly-once semantics.

## Read at the promised population and grain

Choose what a returned row represents and which stored facts qualify. Define lifecycle filters, time boundary, ordering and tie-breaking, and whether a filter selects entities or occurrences. “Objects having a matching event, with all their history” differs from “only the matching events.” Preserve that difference in query shape and output labels.

When joining a set of matching labels to a set of events, avoid multiplying the events. Use an existence test to select qualifying entities, or reduce each relation to the needed grain before joining. `DISTINCT` across displayed fields can erase legitimate same-valued occurrences; `SUM(DISTINCT value)` can undercount them. Compare per-identity results to independent examples.

Distinguish an empty complete history from unknown values within a history. Decide whether an aggregate means a total over every qualifying fact or a known-value subtotal. Carry the relevant counts so an unknown value does not disappear inside a plausible number. A default zero is justified by the domain's complete-empty rule, not by convenience. SQLite aggregates have specific null behavior; consult [aggregate functions](https://www.sqlite.org/lang_aggfunc.html) for the selected expression.

Use stable explicit ordering where consumers depend on it. If “latest” requires tie-breaking, include an agreed stable key or sequence. Do not infer chronological order from arbitrary textual identifiers. Use the [operations reference](operations-and-connections.md) when multiple queries must share one observation boundary.

## Export a defined representation

State the export's audience and population: current view, complete domain interchange, or database recovery. Give a reusable machine format a version and explicit representations for identity, relationships, units, nulls, and ordering where required. Define whether another import should append, merge, or replace, and who owns that destination decision.

A narrow compatibility CSV may deliberately omit relationships or history. Label the omissions and provide a fuller representation only when the task needs it. Do not describe a domain export as a recovery backup if it omits schema, constraints, provenance, or other facts the recovered application requires. Backup guidance lives in [evolution and delivery](evolution-and-delivery.md).

Write the real file and reopen it with its intended parser. Compare exact identities and consequential values to independently specified records, including representative literal text and missing values. An exporter/importer round trip can share the same mistake; use it as additional evidence, not the sole oracle. When a native consumer is promised, exercise that consumer or state that only parsing was verified.
