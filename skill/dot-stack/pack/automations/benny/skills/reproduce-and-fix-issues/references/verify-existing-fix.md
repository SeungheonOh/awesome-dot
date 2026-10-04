# Verify an existing fix without competing with it

Use when a concrete open/merged PR or immutable commit plausibly addresses the report. A tracker status, branch name, bot hypothesis, or person saying “fixed” is a lead, not a pinned artifact. Prefer the source-thread/tracker-linked candidate; explain any different selection and hold ambiguity that changes the result.

## Bind candidate and baseline

Record repository, candidate commit, artifact URL, parent/base relationship, relevant build inputs, and environment/fixture identity. Resolve moving names once to immutable IDs and recheck the candidate before reporting. For an open PR, select the actual pre-fix baseline appropriate to its diff; for a merged fix, choose a buildable preceding revision that represents reported behavior. Do not assume the current base branch still contains the defect.

Preserve existing user work. Use a separate checkout/worktree if available and appropriate. Do not change the author's branch, add commits to the fix, or produce a competing PR. Authentication, fixture writes, process startup, and cleanup remain within the existing authority.

## Paired measurement

1. Start the baseline and verify correct build/app identity
2. Drive the exact reported user path, observe the discriminating defect, reset, and reproduce it again
3. Save baseline recording, screenshot, steps, and read-only state cross-check
4. Start the pinned candidate under equivalent relevant conditions
5. Repeat the same path twice, with reset; verify expected state and absence of the defect
6. Capture the same after evidence and record any environment differences
7. Run focused neighboring/failure-path checks required by the feature map

Compilation or a passing unit test is additional evidence, not a substitute. If baseline reproduction fails, no causal claim that the candidate resolved the symptom is established. If the candidate changes while verification runs, label the tested commit and do not extend the verdict to the new head without relevant checks.

## Outcomes and communication

- **Existing fix verified:** baseline defect twice; candidate correct twice; mandatory evidence and adjacent checks pass
- **Existing fix insufficient:** same defect persists on the candidate, or a mandatory behavior regresses
- **Inconclusive:** unavailable baseline/build, missing evidence, uncertain setup, or mismatched candidate

Only the first two may use the run's single authorized unprompted source update after parent preflight. If that update was already sent, use the configured operations/run output rather than adding another unprompted reply. Inconclusive results stay in operations/run output unless a direct authorized question needs an answer. Link the actual candidate and state tested revisions and limits. Do not open a replacement PR, edit the existing fix, merge, or deploy.

Stop owned builds and disposable resources under retention and cleanup authority. Preserve user changes and return any remaining artifacts/processes in the receipt.
