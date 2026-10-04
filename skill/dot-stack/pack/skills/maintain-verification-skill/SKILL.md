---
name: maintain-verification-skill
description: "Audit a project verification recipe and feature map against source and real app behavior, making only proven recipe or harness corrections within scope."
---


# Maintain a verification skill

Keep a verification recipe accurate as the app changes. The target is the skill directory, feature map, and helpers it owns. Product regressions are findings to report, not permission to edit product code or erase the expected behavior from the map. This invocation creates no recurring schedule.

## Identify the target and coverage

Use the named recipe or inspect the project's established skill directories for launch/doctor/drive instructions and a feature index. If multiple candidates remain ambiguous, ask which one. If none exists, use [create verification skill](../create-verification-skill/SKILL.md) only if the user wants a new recipe.

Read the entire target and list its features and entry points. Check the index for missing, duplicated, obsolete, and unlinked files. Inspect recent source changes for user-facing behavior absent from the map, citing the concrete route, command, or component before calling it missing.

## Read source, then drive

For substantial maps, assign read-only workers distinct features with exact source revision and output contract: feature summary, entry points, likely drift with citations, and one verification recipe. Workers do not drive the same app or edit files. Use sequential source review when workers are unavailable or excessive.

Reconcile every required feature before claiming coverage. Consolidate compatible recipes into a small number of app states. The coordinator or one explicit driver owns live interaction. Follow the recipe's launch model: one isolated server/UI session, or separate test-owned processes for short-lived commands. Do not double-drive a shared user session.

## Live-pass invariants

- Run doctor before the first drive, on fresh sessions where session identity changes, and after surprising behavior
- A healthy process may still contain a wedged UI; reset to a known fixture or restart only the owned instance
- Capture evidence as work proceeds, and verify it survives every cleanup
- Clean failed-attempt residue before retrying; never stop a shared process or remove user data
- Exercise every feature for a full audit. Record each mapped entry point as verified, failed, unverified, or blocked instead of implying one path proves all paths

If doctor is wrong because of recipe drift, make the smallest in-scope correction, restart only what it invalidates, and retry the same proof. On a repeated failure, diagnose the new evidence and report the real blocker; do not loop indefinitely or change safety settings. Unavailable credentials, hardware, or entitlements leave feature coverage unverified. Verifying the missing prerequisite is not a feature pass.

## Correct only proven drift

Wrong description with current intended behavior confirmed is documentation drift. A working user path that an obsolete selector cannot drive is a harness gap. Broken intended behavior is a product regression. If the distinction is unresolved, preserve the contract and ask or report uncertainty rather than silently documenting the bug as expected behavior.

After any harness or recipe edit, run that exact path again. Validate helper invocation and retain evidence. Re-read all changed files. Do not modify product code, generated global settings, or unrelated documents.

## Report accurately

Use one outcome:

- **Clean:** all required source and live coverage completed; no corrections needed
- **Changed:** scoped corrections were applied and re-proved, with any remaining coverage gaps explicitly named
- **Blocked:** required coverage or a necessary safe correction could not complete

Return coverage by feature/entry point, corrections, product gaps, evidence paths, cleanup status, and remaining prerequisites. Keep run notes local. If publication was explicitly requested, consolidate proven corrections into at most one authorized pull request; otherwise return the local diff. No changes needed means no empty branch or pull request.
