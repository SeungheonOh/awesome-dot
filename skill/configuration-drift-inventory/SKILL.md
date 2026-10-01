---
name: configuration-drift-inventory
description: "Compare sanitized environment snapshots against an agreed baseline and separate approved differences from unresolved drift."
---

# Inventory Configuration Drift without Changing Systems

Compare sanitized environment snapshots against an agreed baseline and separate approved differences from unresolved drift.

## When to use

A service behaves differently across environments and the team needs a field-level explanation. Their configuration files look similar, but one environment has a shorter timeout and a feature flag inherited from an older template. The team needs an inventory of effective differences and their ownership, without assuming that one environment is correct or applying any changes.

## Required inputs

- Sanitized, dated configuration exports for the environments being compared
- The agreed baseline, or an explicit statement that no authoritative baseline exists
- Template and override precedence rules, plus rendered effective values if available
- Approved environment-specific differences with reasons, owners and expiration dates when applicable
- The bounded configuration paths and a definition of fields that must never be displayed

## Workflow

### Validate the snapshots

Create one snapshot record per environment: environment label, capture time with timezone, format, covered paths, completeness and source. Require sanitized inputs before comparing values. Define a redaction allowlist for safe secret metadata, such as presence and an owner-supplied version label; never compute or display secret-derived fingerprints. If a raw credential is discovered, stop processing that input, omit its value from diagnostics and request a sanitized replacement. Record baseline authority by field or namespace rather than assuming one file governs everything.

### Compute meaningful differences

1. Parse available formats using an existing permitted local parser, or manually extract the bounded fields. Preserve provenance for each layer: default, template, environment override and explicit local value. Apply precedence only when the supplied rules determine it. For unresolved interpolation or missing includes, label the effective value unknown.
2. Normalize documented equivalents, such as a timeout expressed in seconds versus milliseconds, into a comparison value while retaining the original representation. Ignore object-key order only where the format defines it as irrelevant. Preserve list order, case, numeric/string types and empty values unless the field's contract explicitly permits normalization.
3. Enumerate the explicit requested field scope rather than only keys present in the exports, so a field absent on both sides still receives a comparison. Represent each field as path, value state, normalized value, original source, effective-source layer and evidence confidence. Value states must distinguish absent, inherited, null, empty and explicit. Carry each snapshot's completeness into effective-value evaluation: a missing override or baseline value in an incomplete export is unknown, not evidence of inheritance or absence. Compare like-for-like effective values; do not label a template-versus-rendered difference as runtime drift without resolving the layers.
4. Join differences to approved exceptions by exact field, environment and allowed value or range. Evaluate exception validity at the stated comparison date. Mark a match expected, an expired match stale exception, a resolvable mismatch unexplained, and an unresolved effective value unknown. Without an authoritative baseline, report neutral pairwise differences and keep correctness undecided.
5. Attach the supplied owner and the behavior the field controls. Separate established effects from possible consequences. Group related differences into decision items only when they share a cause or approval, retaining all individual field records.

### Produce and verify the inventory

Deliver a snapshot manifest, field-difference ledger, normalization rules and decision queue. Each decision row needs evidence on both sides, classification, relevant exception, owner or owner unknown, and the smallest missing input. Check a reordered object, an order-sensitive list, an absent override and an expired exception with synthetic examples. Ensure normalization does not collapse missing into null or convert an unexplained value into an approved one. Reconcile counts of compared, excluded and unresolved fields, and inspect the report for prohibited values. If parsing is unavailable, provide a bounded manual comparison with completeness limits. Stop before synchronization or remediation; a drift inventory establishes differences, not permission to change environments.

## Deliverables

- A dated snapshot and baseline provenance record
- A field-level difference inventory with classification and normalization rules
- An effective-value uncertainty list covering inheritance and incomplete exports
- An owner decision queue with stale exceptions and likely behavioral consequences

## Verification

- A missing authoritative baseline yields neutral differences rather than unsupported correctness judgments
- Object-key reordering does not create drift when the format defines object order as irrelevant
- A list whose ordering affects behavior retains its order and flags meaningful changes
- Missing, null, empty and inherited values are not collapsed into one state
- An approved difference with an expired date is visibly distinct from an active exception
- Secret values never appear in the output, logs or proposed comparison artifacts
- Every unexplained difference cites both compared locations or explicitly identifies a missing side

## Stop and ask

- Prepare sanitized exports before use; exclude secrets, private keys and connection strings containing credentials
- Restrict work to supplied snapshots; an open dashboard does not authorize changes or additional access
- Comparison execution requires an available permitted toolchain and must not invoke networked infrastructure commands
- Stop before remediation, security-sensitive setting changes or external sharing; obtain a specific decision for that scope

## Example request

```text
dot, create a read-only configuration-drift inventory for [ENVIRONMENTS] using [SANITIZED SNAPSHOTS], [BASELINE] and [APPROVED DIFFERENCE LIST]. Limit the comparison to [CONFIGURATION SCOPE]. Do not connect to the environments, run infrastructure tooling or change any settings.

Record each snapshot's origin, date and completeness. Establish which source is authoritative for each field; if no baseline is approved, present a neutral comparison rather than labeling one side incorrect. Apply supplied inheritance and override rules only where their effective result can be established. Distinguish an absent field, an inherited default, an explicit null and an empty value.

Normalize cosmetic formatting and documented unit equivalents without erasing meaningful ordering or case differences. Never print secrets or credential values. If those values appear in an input, omit them from the report and ask for a sanitized replacement before processing them further. For approved redacted secret fields, compare only safe metadata such as presence and declared version labels.

Classify differences as expected, unexplained, stale exception or unknown effective value. Link each to evidence, an owner if supplied, the behavior it may affect and the decision needed. Validate the inventory with reordered equivalent objects, a meaningful list-order change and a missing override. Local comparison scripts require an available authorized toolchain; label unrun checks. Read relevant snapshots from already-authorized sources within scope, and save the result to a requested authorized destination with readback. Ask only for new access, installation, remediation or scope expansion that is not authorized. Return a decision queue and identify the smallest missing evidence; do not synchronize configurations as part of an inventory.
```

## Focused follow-ups

### 1. Resolve effective values

```text
Use [SANITIZED RENDERED CONFIGURATION] to resolve the unknown inherited values. Preserve the original source and precedence explanation so reviewers can see how the final value was derived.
```

### 2. Review expired exceptions

```text
Review the differences whose approved exceptions have expired. Draft a decision worksheet with the original reason, current evidence and renew-or-remove options, without changing any setting.
```

### 3. Design a narrow remediation review

```text
For [ONE APPROVED DRIFT ITEM], outline the minimal proposed change, owner approval, behavioral check and recovery step. Identify any security-sensitive setting that needs a separate explicit decision.
```

## Worked example

Read [Larch renderer snapshots](WORKED_EXAMPLE.md) for complete synthetic inputs, a field-level inventory and local assertions covering units, inheritance, ordered lists and exception validity. Use the workflow on authorized real snapshots; the example does not require live tasks to remain hypothetical.

## Evidence status

This is an implementation guide. End-to-end execution has not been established; report actual checks and unrun steps for each use.
