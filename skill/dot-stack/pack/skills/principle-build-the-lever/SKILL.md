---
name: principle-build-the-lever
description: "Choose a small rerunnable transformation or check when it makes a migration, repeated edit, or difficult one-off result cheaper to verify than manual work."
---

# Build the lever

Use a reproducible mechanism when it reduces total implementation and review effort. A lever can transform work, prove it, or give independent workers a shared recipe; it does not need to be a new framework.

## Choose by payoff

Estimate the cost of doing and checking the task manually, including mistakes and likely reruns. Compare an existing project command, a small script or query, and direct editing. Use the smallest option that preserves the needed semantics. A one-off migration can justify automation because independent verification is hard; a two-line correction usually does not.

For a transformation:

1. Work through a representative example first, including one case that must remain unchanged. Write the transformation's input, output, and do-not-touch boundaries.
2. Reuse an existing parser or codemod where syntax matters. A text replacement is appropriate only when its matching assumptions are demonstrated.
3. Provide preview or dry-run output when writes are consequential. Reject ambiguous cases instead of silently guessing. Keep writes within the authorized target.
4. Compare generated output with the reviewed example, test a nonmatching case, and rerun. Idempotence or an explicit already-applied outcome should prevent double transformations.
5. Check behavior after the edit, not just the number of replacements. Save the command, input identity, and result so someone else can repeat the check.

If independent workers are useful and the host provides them, give each the same acceptance contract and disjoint write ownership. Keep the contract under one owner's control. Do not distribute mechanical edits that one deterministic pass can perform more reliably. Sequential execution remains valid when delegation is unavailable.

## Limits and evidence

Applies: rename a structured configuration field across hundreds of files with a parser, produce a changed/skipped/error report, then validate the resulting configurations.

Does not apply: add a missing argument at one known call site with a focused regression test. Building a general migration engine would add more maintenance than confidence.

Stop extending the tool once it covers the actual input set and proof obligation. Retain a useful helper in the agreed deliverable when future reruns matter; creating a helper does not authorize committing, installing, publishing, or running it against external systems. Report a drafted or unrun tool as such.
