# Portable local tools

These helpers need Node 22 or newer. They have no runtime packages and never install anything. Git is required only for repository inspection; an existing authenticated GitHub CLI is required only for live GitHub reads.

In the native export, the verified package root is `dot-stack/`. In the single-entry export it is `dot-stack/pack/`, not the outer skill folder. The bundled manifest and helper must be present there.

Run from that verified library root:

```sh
node tools/dot-stack.mjs --help
node tools/dot-stack.mjs doctor
```

For a copied skill, first verify the explicitly supplied package root: its `plugin.json` must name `dot-stack` and `tools/dot-stack.mjs` must exist. Then use `node "$DOT_STACK_ROOT/tools/dot-stack.mjs" …`. Do not search private application stores or download missing tools. A helper path is separate from the target project and state directory.

## Boundaries

- GitHub observations are read-only. No login, credential configuration, comment, thread resolution, push, rebase, merge, retarget, deployment or background scheduler is implemented
- Worktree audit neither fetches nor deletes. It uses existing local remote refs and labels their freshness accordingly
- A successful plan check means structural completeness. It never runs commands embedded in a plan
- A verification receipt is local evidence bookkeeping. A gate answer or standing line does not grant execution permission
- The graph library can produce an inert action request tied to head/base/generation and evidence. It cannot execute it
- `READY` describes an observed current-head forge state. Verification sufficiency and the host's action permission checks remain separate
- `--status-only` exits 0 after obtaining a status observation even when that observation contains blockers. Never use its exit alone as a readiness gate

GitHub's public CLI fields and GraphQL shapes were checked against the [CLI reference](https://cli.github.com/manual/gh_pr_view), [commit/check schema](https://docs.github.com/en/graphql/reference/commits), and [GraphQL pagination guidance](https://cli.github.com/manual/gh_api). This is contract review, not a live account test.

## Orchestration store

```sh
node "$DOT_STACK_ROOT/tools/dot-stack.mjs" orch --store .dot-stack/state/example init
node "$DOT_STACK_ROOT/tools/dot-stack.mjs" orch --store .dot-stack/state/example unit add parser --track build --brief briefs/parser.md
node "$DOT_STACK_ROOT/tools/dot-stack.mjs" orch --store .dot-stack/state/example unit set parser --state verified --pr 42 --sha FULL_COMMIT_SHA
node "$DOT_STACK_ROOT/tools/dot-stack.mjs" orch --store .dot-stack/state/example status
```

Store selection is explicit `--store`, then `ORCH_STORE`, then the current target project's `.dot-stack/state/default`. The CLI refuses its default when run from the package root itself; choose a project store explicitly. Never put mutable state in an installed plugin cache. State is local and private by default; publishing it is a separate action.

The canonical store is versioned `state.json`. It contains units, evidence history, inbox events and delivery batches, decision gates/history, standing constraints and the current frontier. Every write takes a token-owned exclusive process lock, validates the current snapshot, applies a serialized transaction and atomically replaces the file. Concurrent operations through one instance are serialized too. Full commit identities must be 40 or 64 hexadecimal digits.

`orch export` creates readable derived TSV/Markdown/JSON views; `exports.json` identifies their state revision. Do not edit those views as inputs. `orch status --read-only` does not write a status file or change state. `status` deliberately updates the derived status snapshot. No automatic import or in-place migration of another store format is performed; preserve an old store as an archive and seed a new one through the commands.

### Commands

All orchestration commands accept `--store DIR` and `--json`. Without `--json`, status is three compact summary lines; other results are compact JSON. Full help lists the options.

| Group       | Operations                                                                                                                                                                                                 |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Units       | `unit add ID --track TRACK [--brief PATH]`; `unit set ID --state STATE [--branch B --pr N --sha SHA]`; `unit get ID`; `unit list [--state STATE --track TRACK]`; `unit counts`                             |
| Evidence    | `ledger record PR SHA VERDICT --evidence PATH [--verifier NAME --base-sha SHA --profile PROFILE --patch-id ID]`; `ledger check PR SHA [--base-sha SHA --profile PROFILE --require-pass]`; `ledger summary` |
| Inbox       | `inbox push AGENT UNIT STATUS [--report PATH --key KEY]`; `inbox drain [--peek]`; `inbox count`; `inbox ack BATCH`                                                                                         |
| Gates       | `gate park ID --question QUESTION --options OPTIONS --default ANSWER`; `gate list`; `gate resolve ID --answer ANSWER`                                                                                      |
| Frontier    | `frontier set --graph FILE [--prs N,... --expected-revision N]`; `frontier show`                                                                                                                           |
| Constraints | `standing add LINE`; `standing show`                                                                                                                                                                       |
| Store       | `init`; `status [--read-only]`; `export`; `recover-lock --token TOKEN`                                                                                                                                     |

`unit set --expected-revision N` can reject stale callers too. Supported verdict labels are `live-ui-verified`, `unit-test-verified`, `type-check-only`, `behavior-verified`, `docs-verified`, `verifier-blocked`, and `verifier-failed`. There is no universal UI-over-CLI evidence ranking. A profile describes what the unit needs. `--require-pass` excludes failed, blocked and type-check-only receipts; the caller must still assess that the profile covers the task.

A new receipt supersedes a previous one for the same PR/head without deleting history. `ledger check` never substitutes another head. An optional base/profile must also match. Patch IDs are recorded metadata, not an automatic permission to reuse old results. Reuse needs a reviewed, current decision; CI, reviews and mergeability must still be fresh.

### Durable completion delivery

`inbox drain` claims the current pending events and returns a batch ID. It does not erase them. Process the events, persist resulting unit/receipt updates, then `inbox ack BATCH`. An unacknowledged batch is replayed on the next drain. New arrivals wait for the next batch. Repeating an acknowledgement is harmless. An idempotency key prevents duplicate pushes and rejects conflicting payloads under the same key. Event history remains in state.

### Lock recovery and durability limits

There is no live-lock stealing option. A locked, malformed or foreign-host store stays blocked. After confirming all writers are stopped, inspect `.writer.lock` and use its exact token with `recover-lock`. Recovery additionally requires a dead same-host PID and quarantines the old lock; it does not discard it. A reused/live PID, unknown namespace, or foreign machine requires operator diagnosis rather than guessing.

Atomic writes use a same-directory exclusive temporary file, file sync, rename and directory sync where supported. Existing file permissions are preserved. The guarantees target ordinary local filesystems. Network filesystems, simultaneous external editors and power-loss behavior on untested platforms are not certified. A write failing after rename may have committed; re-read state before retrying. Never automatically delete a corrupt file.

## Dependency graph

The frontier replaces vendor stack metadata with explicit graph data. Example:

```json
{
  "schemaVersion": 1,
  "repository": "owner/repository",
  "nodes": [
    {
      "id": "base-change",
      "pr": 41,
      "branch": "base-change",
      "baseBranch": "main",
      "headSha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "baseSha": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      "state": "MERGED",
      "dependsOn": []
    },
    {
      "id": "follow-on",
      "pr": 42,
      "branch": "follow-on",
      "headSha": "cccccccccccccccccccccccccccccccccccccccc",
      "state": "OPEN",
      "dependsOn": ["base-change"]
    }
  ]
}
```

Allowed states are `OPEN`, `MERGED`, `CLOSED`, and `UNKNOWN`. Reject cycles, self/missing/duplicate dependencies, duplicate IDs/PRs, invalid identities and pin drift. A deterministic topological order supports chains and DAGs. Eligible frontier members have every dependency merged. A closed-but-unmerged predecessor blocks descendants. Failed validation leaves the prior generation unchanged.

Graph input contains declared observations; setting it does not fetch or prove them. The coordinator must supply fresh authorized forge facts and recompute after head/base/merge/topology changes. The live watcher separately queries current GitHub facts. Do not mistake a locally declared merged node for a confirmed remote merge.

## Pull-request watcher

```sh
# One observed status, no future polling
node "$DOT_STACK_ROOT/tools/dot-stack.mjs" watch-pr --owner OWNER --repo REPO --pr 42 --status-only

# Read-only polling until ready, blocked, timed out or cancelled
node "$DOT_STACK_ROOT/tools/dot-stack.mjs" watch-pr --owner OWNER --repo REPO --pr 42 --timeout 1800

# Captured bottom-to-top queue; completion means every member actually merged
node "$DOT_STACK_ROOT/tools/dot-stack.mjs" watch-pr --owner OWNER --repo REPO --queued-stack --stack-prs 41,42 --checkpoint .dot-stack/state/queue.json
node "$DOT_STACK_ROOT/tools/dot-stack.mjs" watch-pr --resume .dot-stack/state/queue.json
```

Defaults: interval 60 seconds, whole-stack sweep 300 seconds, no timeout, and five consecutive query errors. Query backoff has a 60-second floor and 300-second cap. Use `--pretty` for human text. `--stack` discovers the connected open branch graph; ambiguous heads, cyclic dependencies or incomplete reads fail closed. Queued membership is frozen; fresh head/base changes invalidate old observations. Checkpoints record facts but always require a fresh read on resume. They are not durable scheduling or authority.

Optional `--reviewers FILE` reads an explicit JSON policy with `automationAuthors`, `runIdMarkers`, and `checkNames` string arrays. It annotates configured automated reviewers, counts distinct observed run markers (including resolved threads), and identifies configured pending review checks. This is observed metadata, not a trust or dismissal rule; there are no built-in vendor identities. Unknown automation remains unclassified. A run without any comments cannot be counted from thread evidence.

All authoritative checks are read for an explicit commit. The PR is re-read after checks/threads to reject mixed-head/base snapshots. Review/check/open-PR/commit collections paginate with token-cycle and completeness guards. Empty checks do not establish an absence of requirements; they block observation until evidence is available. Unknown node/state values never pass. The implementation conservatively considers all observed checks; it does not silently ignore checks just because they appear optional. A named human gate remains pending or gated.

Single/stack mode emits `READY` when a complete current-head snapshot is clear. `--allow-draft` permits inspection without the local draft flag being the stopping condition; it never changes a PR. A forge-reported draft or other non-clear merge state can still prevent readiness. Queued mode never uses `READY`: it emits `WAITING` while the bottom awaits merge and `ADVANCE` after an observed merge; only confirmed merged facts for every captured member produce `COMPLETE`. An upper pending check is not attributed to the bottom. Conflicts, review threads, CI and other gates have deterministic priority.

NDJSON schema version 2 includes sequence, observation time, mode, kind, terminal flag and terminal exit status. Kinds: `QUEUE`, `STATUS`, `WAITING`, `ADVANCE`, `RETRY`, `BLOCKER`, `READY`, `COMPLETE`, `TIMEOUT`. Readiness proof includes exact head/base identities. `READY` explicitly sets `authorizesExecution: false`.

| Exit | Meaning                                                                 |
| ---: | ----------------------------------------------------------------------- |
|    0 | Successful terminal observation; inspect event kind                     |
|    2 | Merge conflict                                                          |
|    3 | Unresolved review threads                                               |
|    4 | Failing current-head CI/rollup                                          |
|    5 | Configured observation timeout                                          |
|    6 | Draft, review requirement, closed-unmerged, unknown or other merge gate |
|    7 | Status unavailable, invalid context, incomplete or stale observation    |
|   64 | CLI usage error                                                         |
|  130 | Cancelled                                                               |

A stack readiness observation is not a command to merge the whole stack. Shipping still needs sufficient candidate evidence, permission for that exact action, and a fresh check immediately before acting. Historical passing checks are display context only.

## Plan checker

```sh
node "$DOT_STACK_ROOT/tools/dot-stack.mjs" check-plan plan.md --json
node "$DOT_STACK_ROOT/tools/dot-stack.mjs" check-plan plan.md --verify-evidence --root . --head FULL_COMMIT_SHA
```

Required headings: H1, `## Inputs` (or `How to read this`), `## Phases` (or `Program checklist`), one or more H2 unit sections, and `## Close` (or `Completion` / `Close the program`). Each unit has bold blocks `ID.`, `Surface.`, `Depends on.`, `Files.`, `Build.`, `Accept.` (or `You see.`), `Verify, unit.`, `Verify, live.`, `Verify, perf.`, `Review gate.`, and `Delivery.` (or `Merge.`).

Surface is `docs`, `cli`, `service`, `ui`, or `mixed`; dependencies are comma-separated IDs or `None.`. Applicable verification names a command/scenario, `Evidence: path` and `Pass when predicate`. Prefer backticks around evidence paths. A concrete `Not applicable. reason` is allowed for genuinely irrelevant verification categories; UI/mixed live evidence cannot be waived. No screenshot count, model, worker count, slash command, prose punctuation or video duration is prescribed.

The checker detects malformed structure, duplicate/cyclic dependencies, unresolved placeholders, missing evidence destinations and missing predicates. Fenced content does not create sections. Optional local evidence inspection checks paths and the supplied candidate identity; it never fetches remote evidence or executes embedded commands. Semantic sufficiency of a scenario or non-applicability rationale still requires review.

## Worktree audit

```sh
node "$DOT_STACK_ROOT/tools/dot-stack.mjs" worktree-audit /path/to/repo --json --trunk main
```

Optional `--active FILE` accepts a JSON array of active paths or `{ "path": "…", "task": "…" }` records supplied by the host. Optional `--prs FILE` accepts already-observed `{ "headRefName": "…", "state": "OPEN|MERGED|CLOSED" }` records. These are explicit evidence inputs, not automatic activity or remote-state discovery.

Output includes numeric size, partial inspection status, tracked/untracked files, branch/head, locked/prunable/bare/detached facts, ancestry, local ahead/behind/diverged state, supplied PR facts and descriptive reasons. NUL-safe parsing preserves unusual paths. Directory symlinks are not followed. No transcript or sidebar is scanned. A merged candidate is still only a candidate: unknown activity and untracked data are never deletion permission. Main worktree is included in the report so it cannot disappear from an audit.

## Decision trail

```sh
node "$DOT_STACK_ROOT/tools/dot-stack.mjs" log .dot-stack/state/example/decisions.tsv verify "kept the parser change" "regression now passes" evidence/test.log verified --run RUN_ID
```

Columns remain timestamp, phase, decision, why, evidence, result. The helper sanitizes single-line TSV cells and spreadsheet-formula prefixes, locks concurrent writers, validates prior rows, appends once and syncs. It never rewrites history. Correct a bad row with a new superseding entry. A wrong header or partial trailing row is an integrity error that preserves the bytes. `--run` adds a start row on a run switch. It does not inspect hidden transcripts or invent missing evidence.

## Verification and platform limits

```sh
node --test tools/test/*.test.mjs
node tools/check-types.mjs /path/to/already-installed/tsc
```

The second command is optional maintainer verification and never installs a compiler. Public module declarations for the actual watcher, dependency-graph and orchestration imports link their results and inputs to `contracts.d.ts`. Positive/negative consumer fixtures import and call these modules, checking impossible-readiness, branded PR/commit identity, typed receipts and inert action-request boundaries. The declarations are public contracts checked alongside runtime validators and tests; the JavaScript implementation itself does not have whole-program TypeScript checking. This is a narrower static guarantee than a fully typed implementation.

The offline suite uses injected readers/clocks and temporary Git repositories. It covers multiprocess state writes, durable inbox replay, explicit lock behavior, interrupted atomic writes, current-head/base drift, stack progression, query budgets, pagination, conservative enum handling, plan surfaces, read-only audit, log concurrency and process limits. No live GitHub account, credential, network mutation or package install is needed.

Initial verification is Linux / Node 24. Node 22 is the declared API baseline; macOS, Windows, live authenticated GitHub, and network-filesystem durability require separate real runs. Their absence is a verification limit, not a simulated success.
