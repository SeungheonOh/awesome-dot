# Build the change and clean the diff

Implementation starts with an observable result. Tell the assistant what happened, what should happen, and what must remain true. The playbook supplies the sequence; evidence determines whether the change worked.

## Use a brief suited to the change

**Bug fix:**

```text
The export writes a second record after a retry.
Reproduce it with the existing fixture before fixing it.
Both the first request and its retry must leave exactly one record.
```

**Feature:**

```text
Add --json to the status command.
Default text output stays byte-identical.
The new output must parse and contain the same status values.
```

**Refactoring:**

```text
Move parsing behind one module boundary with no behavior changes.
Capture existing valid and invalid input results before editing.
Compare those results after moving the callers.
```

**Performance:**

```text
Startup takes about 1.8 seconds on the attached fixture.
Establish a repeatable baseline, profile the cause, and compare the same workload.
Report variability and any memory or correctness tradeoff.
```

These route to [Bug fix](../../skills/dot-mode/playbooks/bug-fix.md), [Feature](../../skills/dot-mode/playbooks/feature.md), [Refactoring](../../skills/dot-mode/playbooks/refactoring.md), and [Perf issue](../../skills/dot-mode/playbooks/perf-issue.md). A performance claim needs comparable measurements, not a different input or a warmed cache on only one side.

For repeated optimization, [Hillclimb](../../skills/dot-mode/playbooks/hillclimb.md) fixes the metric and measurement harness, tries one hypothesis at a time, and records retained gains and rejected attempts. Bound the compute or attempt budget and preserve correctness checks. Do not let the target quietly change after several failed ideas.

## Use tdd when it creates real evidence

```text
Use tdd for the duplicate-write bug.
First show a failing behavioral assertion on the current code.
Then make the smallest fix and rerun that assertion plus nearby regressions.
```

[tdd](../../skills/tdd/SKILL.md) follows red, green, then cleanup. “Red” means the test fails for the expected defect. A missing dependency, syntax error, or unreachable fixture is not a valid reproduction. “Green” means the same assertion now passes on the changed code.

Prefer the smallest real interface that exposes the failure. If extensive mocks would only test the mocks, a command-line reproduction or existing integration harness may be stronger. Explain the substitution. If execution is unavailable, provide the test and patch as unrun proposals; never invent the red or green output.

For the duplicate-write example, assert the literal record count and identity after retry. Checking only that a helper was called once can miss the actual behavior users care about.

## Apply TypeScript guidance deliberately

[typescript-best-practices](../../skills/typescript-best-practices/SKILL.md) turns the principles into concrete review questions: validate unknown input at boundaries, represent variants with discriminated unions, make switches exhaustive, and derive types from authoritative schemas where suitable.

Host discovery may load it automatically, but the package does not promise a universal file-extension hook. If the guidance is missing from a `.ts` or `.tsx` task, ask for it by name. A rule is useful when it removes an impossible state or clarifies a boundary, not when it creates a type abstraction with no caller benefit.

## Review code, prose, and comments separately

Before considering the diff ready:

1. Remove unrelated changes, dead branches, unused adapters, and accidental generated files
2. Check that validation lives at real boundaries rather than repeated defensive checks everywhere
3. Preserve public behavior and required compatibility unless the brief authorized changing it
4. Tighten documentation and commit drafts with [unslop](../../skills/unslop/SKILL.md)
5. Examine comments with [no-comments](../../skills/no-comments/SKILL.md)

No extra cleanup plugin is required. Describe the desired cleanup directly and require the same tests afterward. “Clean the diff” is not permission to delete unfinished user work or rewrite unrelated architecture.

## Give comments a skeptical reader

```text
Use no-comments on the changed lines.
Keep legal notices and useful public API documentation.
Identify comments that compensate for confusing code before proposing removals.
```

The [comment-reviewer role](../../agents/comment-reviewer.md) is a bounded, read-only review brief. When the host supports native delegation, a fresh reviewer can inspect the comments. Otherwise, perform and label a self-review; do not claim someone independent looked at them.

A comment that explains an external constraint or links to necessary context may be valuable. A comment that repeats the next line often is not. If a comment says “this must never happen,” consider whether a type, invariant, or behavioral test can enforce the claim. Preserve required license headers and do not erase rationale before understanding it.

Finish cleanup before the final verification pass. A last-minute “cosmetic” edit can still break a string, directive, fixture, or public API example.

Next: [Verify and ship](06-verify-and-ship.md).
