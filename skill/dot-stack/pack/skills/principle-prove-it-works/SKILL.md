---
name: principle-prove-it-works
description: "Match each completion claim to a direct, candidate-bound observation of the requested behavior and distinguish executed checks from proxies or unrun plans."
---

# Prove it works

Use this before claiming a task, fix, migration, or generated artifact is complete. Define what would falsify the claim, then observe the relevant surface against the actual candidate.

## Match proof to the claim

- A type check establishes certain static properties, not successful user interaction.
- A unit test establishes the exercised isolated behavior, not the real service integration.
- A saved screenshot establishes an observed rendering at a particular time, not current state or a functioning control.
- A worker's report is a lead to evidence, not independent confirmation that the integrated result still works.
- An exit code or file timestamp can support diagnosis but does not replace inspecting the promised output.

Choose the direct check: execute the user flow, read the authoritative stored value, inspect the generated artifact, query the real process state, or compare the requested transformation against known inputs. Use synthetic fixtures for unsafe effects; label their scope rather than implying a live action occurred.

For a reusable or complex check, prefer an existing harness or a small deterministic script with an independent expected result. Test the verifier with a known failure when practical. If observation disagrees with expectations, investigate both the system and the observer; do not assume either is correct or weaken the assertion to match the output.

## Keep a useful receipt

Record the candidate revision or content identity, environment, exact check or interaction, expected behavior, observed result, and relevant artifact or log location. Re-run affected checks after integration changes. Keep evidence concise and free of secrets; retain or commit it only in the agreed location and scope.

Use clear evidence states:

- **Verified:** the named check ran on the named candidate and passed
- **Failed:** observation contradicted the acceptance condition
- **Unverified:** required proof was not obtained or is stale
- **Blocked:** a required next action needs access, authority, information, or a decision

## Example and counterexample

Applies: after a CSV export fix, run the real exporter with a comma, quote, and newline in input, parse the output independently, and compare the recovered records with expected values.

Does not apply: declaring the export correct because the file exists or the function compiles. Likewise, text-only review without execution tools may establish a reasoned patch, but cannot be reported as a passed runtime test.

Stop short of the unsupported claim. State the remaining proof gap and smallest next check instead of inventing successful execution.
