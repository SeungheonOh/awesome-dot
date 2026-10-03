---
name: validate-dataset
description: Check a supplied dataset against agreed structural and semantic rules, returning attributable violations and explicit evaluation limits. Use for data-contract conformance and requested reusable validators, rather than exploratory profiling, data cleanup, service import or analysis of a substantive data question.
---

# Validate a Dataset

Deliver a useful conformance result for the actual selected data. Identify which declared requirements hold, which fail and which cannot be established from the available input. When requested, also deliver the reusable validator and exercise its real caller. A proposed schema, a list of generic quality concerns or a cleaned replacement is not the requested result.

Use profiling to discover a dataset's characteristics, cleanup to change its values and import rehearsal to establish destination operations. A data model decides how facts should be stored; this workflow checks an existing representation against established requirements. Software implementation and repeatable-task guidance can support building the checker without replacing the data-specific decisions below.

## Establish the contract and population

Read the actual data, supplied schema, field definitions and relevant accepted rules. Identify the selected files, tables or snapshot, the record unit, contract version and intended use. Distinguish explicit requirements from conventions inferred from current rows and from optional concerns. An unusual value is not a violation unless a governing rule makes it one.

Resolve only ambiguities that change the verdict. Exact text equality, trimmed matching and case-insensitive identity can produce different results. Likewise, a repeated event is different from a duplicated representation of one event. Ask about an unsettled material rule instead of inventing a convenient correction; continue checks whose meaning is already established. Label proposed checks separately from authoritative acceptance conditions.

Establish the evidence needed for each population claim. Is this a complete snapshot, a filtered export, a sample or a partially retrieved source? A rule may apply within each submitted record, within a group or over an entire population. Uniqueness, absence, completeness and reconciliation totals need the appropriate population; a successful sample does not validate an unseen remainder.

Identify the selected input and rules well enough to reproduce the result. File hashes, a snapshot/version reference or a stable query and retrieval boundary may be appropriate. Preserve originals and unrelated work. Do not make source changes, load a service or expand collection merely to make the dataset conform.

## Preserve meaning while reading

Use the format's real parser and inspect its behavior where it affects the contract. Quoted CSV newlines, repeated JSON member names, spreadsheet cell types and nested collections cannot be handled reliably by treating every visible line or dictionary key as an independent record. A parser's accepted syntax or default coercion is not automatically the user's accepted format.

Keep source occurrences identifiable independently of business keys. A duplicate key is itself something to report, so it cannot serve as the sole key of a dictionary that overwrites the other occurrence. Use suitable locators such as a logical record ordinal and field, a source row, or a nested path. Distinguish a logical CSV record from its physical line span when that matters for finding the issue.

Validate before a conversion can hide the relevant distinction. Preserve literal identifiers, significant whitespace, field presence and source value types. Interpret missing, null, empty, zero and Boolean values according to the contract. Check numerical syntax, units, precision and time conventions before arithmetic. A cast that rounds a value or turns a small negative quantity into zero cannot establish that the original value satisfied a range rule.

Define what can still be examined when reading fails. An unreadable whole document, one malformed JSONL record and a damaged row in an otherwise interpretable table have different effects. Retain useful independent observations when their boundaries are reliable. Do not silently omit troublesome input or call a readable prefix the complete dataset. If record boundaries themselves are uncertain, mark that scope unavailable rather than guessing how many records were skipped.

Use resource limits appropriate to the authorized input and environment. A limit reached, interrupted read or unavailable reference is an incomplete check, not a clean result or evidence that the missing records do not exist. Report that operational limit separately from a data-rule violation.

## Evaluate rules with their dependencies

Separate structural, per-value, per-record, cross-record and population checks when their evidence differs. This need not become a large framework; the purpose is to avoid letting one failure either erase unrelated checks or silently supply a default to a dependent one.

For each consequential check, know its scope, inputs and applicability:

- A field can fail its timestamp rule while still supplying a valid quantity to an independent total
- An unresolved reference or ambiguous duplicate can prevent a group calculation even when each quantity parses
- An observed duplicate establishes that a uniqueness rule fails; seeing only one occurrence in incomplete input does not establish that it is unique
- An empty group has a known zero count or sum only when the relevant population and membership are established. Missing data must not acquire the same value
- A conditional rule can be inapplicable when its condition is known to be false, but an invalid or unavailable condition may leave applicability unresolved

Use statuses that communicate these distinctions where needed: satisfied, violated, inapplicable and not evaluable, or an equivalent clear representation. Do not force a complicated status system onto a simple complete check, but never count an unchecked rule as a pass. Explain why a dependent rule could not run and identify the necessary missing or invalid input.

Retain all occurrences implicated by a duplicate or relationship violation. Do not choose a first, latest or most complete record unless the contract explicitly establishes that authority. Check nested identity at its defined scope; an ID unique within one parent may legitimately occur under another. Distinguish a relationship error from an invalid attribute of an otherwise identifiable record.

Check the declared invariant itself. Totals alone may miss swapped identities; matching keys alone may miss changed values; a valid schema may still permit a business-rule contradiction. Use independent controls from the contract where they matter. Do not invent a new constraint or silently relax an accepted rule because the current data violates it.

## Make the result actionable

Lead with the supported verdict and its scope. Attach each material issue to the rule, affected source occurrence or group, relevant observed value and expected condition. Include enough evidence to locate and understand the problem without dumping unrelated data. Keep unknown or conflicting values visible rather than supplying a guessed replacement.

Keep counting units explicit. Issue occurrences, distinct affected records, duplicate groups and total inspected records are different quantities. A record may fail several rules, and a single relationship issue may involve several records. State the counting convention only to the detail needed to interpret the report; do not inflate a problem count by presenting related evidence as additional independent failures.

Make coverage part of the verdict. Known violations can establish nonconformance even when other checks remain unavailable. An overall pass requires the applicable required checks and intended input scope to be covered. A ruleset that has not been finalized supports a provisional assessment, not a final acceptance decision. Conformance to declared rules does not prove real-world truth, freshness, representativeness or completeness beyond the evidence supplied.

Keep proposed corrections separate from validation. If the user also requests remediation, preserve the original verdict, apply only supported changes within scope and check the resulting data as its own version. Do not hide an original failure by replacing the source under the same result identity.

## Exercise a reusable checker when requested

Build the smallest suitable mechanism with the available tools and selected project conventions. Make the contract or rule version, inputs, output and status behavior clear. Validate through the intended entry point, not only a helper function or a success message. Keep an operational failure distinct from a completed nonconforming-data result so downstream callers cannot mistake either for a pass.

Inspect the code and its effects before execution. Use original or authorized bounded samples and preserve prior useful outputs under the chosen write policy. When reuse is requested, verify another input through the documented interface and check relevant output replacement or refusal behavior. Do not add scheduling, CI, hosted services or account access unless those are part of the task.

Choose a few meaningful checks from the contract: a conforming case, a representative violation and a dependency or parsing boundary likely to cause a false pass. Derive expected outcomes independently of the checker's own logic. Read the actual saved result and reconcile important locators, values and statuses against the source. A test that only repeats the validator's calculation cannot establish that the rule was interpreted correctly.

If a check exposes a defect, preserve the useful failed evidence, repair the implementation within scope and rerun affected checks on the final files. Keep representative exercise results separate from exhaustive guarantees. A schema library, generated validator or inspected rule file still needs evidence that the actual caller uses the intended rules and reports their outcomes correctly.

## Deliver the conformance result

Return the requested report or saved result, the actual reusable checker when requested, and concise usage and coverage limits. For a small one-time question, a direct verdict with precise issues can be sufficient; no script, ledger or test package is mandatory by default.

State unresolved contract decisions or unavailable checks where they affect the conclusion. Distinguish local validation from a live acceptance gate or successful import. Finish with the useful result and the specific next correction or evidence needed, without claiming that every possible data-quality problem has been ruled out.
