# Code archaeology

## Useful evidence

Commit messages and diffs show the change sequence. Review discussions, architectural decisions, release notes, and comments can state motivation. Tests reveal intended contracts and edge cases, but do not automatically prove why an author added them. Co-changed files and linked tickets provide leads.

## Establish the available record

Check whether the current environment has the requested checkout, revision, history depth, and read tools. A shallow clone, supplied diff, or snapshot may lack earlier history. An authenticated review connector or existing CLI may expose discussion, but neither is guaranteed. Do not fetch credentials or change repository remotes to work around a denial.

## Search the introduction and later changes

When git is available, adapt these read-only command templates to observed paths and commits. Arguments shown in angle brackets must be replaced; they are not literal runnable values.

```sh
git log --follow --oneline -- <file>
git log -S '<exact string>' -- <file>
git log -G '<pattern>' -- <file>
git blame -L <first>,<last> -- <file>
git show <commit> -- <file>
git log <old>..<new> -p -- <file>
git log -1 --format=%B <commit>
```

Use rename-aware history and search before the last-touch commit. Formatting changes may obscure introduction; a copied pattern may originate elsewhere. Inspect actual diffs rather than trusting a vague “cleanup” message. Follow explicit review IDs through available read tools, including body, comments, decisions, and linked issues.

Search known documentation and tests for the target symbol, error string, or requirement. Avoid an unbounded repository dump. Read relevant entries fully, including superseding decisions and revert/reapply sequences.

## Interpret carefully

Squashed history may omit branch details. Automated dependency updates may carry useful compatibility context even if their own message does not state motivation. A test added with a fix supports the intended behavior; a source comment claiming a constraint needs dates and, where possible, corroboration. Current code is not direct evidence of past intent.

A merged review is not evidence of deployment. A reverted fix must stay in the history, because its failed assumption can guide the next attempt. Missing history is a source limitation, not “nothing happened.”

## Return

Provide each relevant commit/review/decision with exact ID or URL, location, author/date where available, the short motivating text or accurate summary, and whether it is direct or circumstantial. Record searched paths and ranges, shallow-history limits, useful nulls, and cross-source leads.
