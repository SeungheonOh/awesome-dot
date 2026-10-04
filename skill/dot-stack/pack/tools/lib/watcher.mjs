import { ToolError, fail, realClock, markdown, sha } from "./core.mjs";
import { QueryError, resolveChecks } from "./github-reader.mjs";
import { repository } from "./graph.mjs";
import { positive } from "./core.mjs";

export const defaults = {
  interval: 60,
  sweepInterval: 300,
  timeout: 0,
  maxQueryErrors: 5,
  allowDraft: false,
};
export const backoff = (interval, failures) =>
  Math.min(Math.max(interval, 60) * 2 ** (failures - 1), 300);
export function assessMerge(facts, rollup) {
  const observed = {
    mergeStateStatus: facts.mergeStateStatus,
    headRollupState: rollup,
  };
  if (["ERROR", "FAILURE"].includes(rollup))
    return { kind: "refused", reason: "head-rollup-failed", ...observed };
  if (
    facts.mergeable === "UNKNOWN" ||
    facts.mergeStateStatus === "UNKNOWN" ||
    rollup !== "SUCCESS"
  )
    return { kind: "unknown", reason: "incomplete-merge-proof", ...observed };
  if (facts.mergeable !== "MERGEABLE" || facts.mergeStateStatus !== "CLEAN")
    return { kind: "gated", reason: factGate(facts), ...observed };
  return { kind: "allowed", reason: "current-head-clean", ...observed };
}
function factGate(f) {
  if (f.reviewDecision === "CHANGES_REQUESTED") return "changes-requested";
  if (f.reviewDecision === "REVIEW_REQUIRED") return "review-required";
  if (f.mergeable === "UNKNOWN" || f.mergeStateStatus === "UNKNOWN")
    return "mergeability-unknown";
  return (
    {
      BLOCKED: "forge-blocked",
      BEHIND: "behind-base",
      DRAFT: "draft-pr",
      HAS_HOOKS: "external-hooks",
      UNSTABLE: "forge-unstable",
    }[f.mergeStateStatus] ?? "mergeability-not-clear"
  );
}
export async function readSnapshot(
  reader,
  context,
  { pendingHistory = "include" } = {},
) {
  const facts = await reader.pullRequest(context);
  sha(facts.headRefOid);
  sha(facts.baseRefOid);
  if (facts.state === "MERGED" || facts.mergedAt !== null)
    return { kind: "merged", context, facts };
  if (facts.state === "CLOSED") return { kind: "closed", context, facts };
  const threads = await reader.reviewThreads(context);
  const checks = await resolveChecks(reader, context, facts.headRefOid);
  const failed = checks.checks.filter((c) => c.kind === "failed"),
    pending = checks.checks.filter((c) => c.kind === "pending"),
    unknown = checks.checks.filter((c) => c.kind === "unknown");
  if (
    ["PENDING", "EXPECTED"].includes(checks.rollupState) &&
    pending.length === 0
  )
    pending.push({
      id: "forge-rollup",
      name: "Forge head rollup",
      kind: "pending",
      reportedState: checks.rollupState,
    });
  let history = [];
  if (
    pendingHistory === "include" &&
    typeof reader.commitRollups === "function"
  )
    history = await reader.commitRollups(context);
  const fresh = await reader.pullRequest(context);
  if (
    fresh.headRefOid !== facts.headRefOid ||
    fresh.baseRefOid !== facts.baseRefOid ||
    fresh.state !== facts.state ||
    fresh.baseRefName !== facts.baseRefName
  )
    throw new QueryError(
      "stale-observation",
      "PR head, base or state changed while status was read",
    );
  const assessment = assessMerge(
    fresh,
    checks.rollupState ??
      (checks.checks.every((c) => ["passed", "skipped"].includes(c.kind))
        ? "SUCCESS"
        : null),
  );
  const kind =
    failed.length || assessment.kind === "refused"
      ? "failing"
      : unknown.length
        ? "unknown"
        : pending.length
          ? "pending"
          : "clean";
  return {
    kind: "open",
    context,
    facts: fresh,
    threads,
    checks: {
      ...checks,
      failed,
      pending,
      unknown,
      kind,
      assessment,
      hadPreviousPassingCi: history.some(
        (c) => c.oid !== facts.headRefOid && c.state === "SUCCESS",
      ),
    },
    observedHead: facts.headRefOid,
    observedBase: facts.baseRefOid,
    reviewAutomationRunning: checks.checks.some(
      (check) =>
        check.kind === "pending" &&
        (reader.reviewerPolicy?.checkNames ?? []).includes(check.name),
    ),
  };
}
export function blockers(row, allowDraft = false) {
  if (row.kind === "merged") return [];
  if (row.kind === "closed")
    return [
      {
        kind: "merge-gate",
        pr: row.context,
        reason: "closed-without-merge",
        tier: 3,
      },
    ];
  const out = [],
    f = row.facts;
  if (
    f.mergeable === "CONFLICTING" ||
    ["DIRTY", "CONFLICTING"].includes(f.mergeStateStatus)
  )
    out.push({ kind: "merge-conflicts", pr: row.context, facts: f, tier: 0 });
  if (row.threads.length)
    out.push({
      kind: "review-threads",
      pr: row.context,
      threads: row.threads,
      tier: 1,
    });
  if (row.checks.kind === "failing")
    out.push({
      kind: "failing-checks",
      pr: row.context,
      checks: row.checks,
      tier: 2,
    });
  let reason = null;
  if (f.isDraft && !allowDraft && !row.checks.pending.length)
    reason = "draft-pr";
  else if (["CHANGES_REQUESTED", "REVIEW_REQUIRED"].includes(f.reviewDecision))
    reason = factGate(f);
  else if (row.checks.kind === "unknown") reason = "unknown-check-state";
  else if (
    !row.checks.pending.length &&
    (f.mergeable !== "MERGEABLE" || f.mergeStateStatus !== "CLEAN")
  )
    reason = factGate(f);
  if (reason)
    out.push({ kind: "merge-gate", pr: row.context, reason, tier: 3 });
  return out;
}
export function classify(rows, { allowDraft = false } = {}) {
  fail(Array.isArray(rows) && rows.length > 0, "No snapshots to classify");
  const all = rows
    .flatMap((r) => blockers(r, allowDraft))
    .sort((a, b) => a.tier - b.tier);
  if (all.length) return { kind: "blocker", blocker: all[0], allBlockers: all };
  const waiting = rows.find(
    (r) => r.kind === "open" && r.checks.pending.length,
  );
  if (waiting)
    return {
      kind: "waiting",
      frontier: waiting.context,
      pending: waiting.checks.pending,
    };
  return {
    kind: "ready",
    prs: rows.map((row) =>
      row.kind === "merged"
        ? {
            kind: "merged-pr",
            context: row.context,
            mergedAt: row.facts.mergedAt,
          }
        : {
            kind: "ready-pr",
            context: row.context,
            proof: {
              headSha: row.observedHead,
              baseSha: row.observedBase,
              mergeability: "clear",
              threads: [],
              checks: row.checks,
              reviewDecision: row.facts.reviewDecision,
              draft: row.facts.isDraft ? "draft-allowed" : "not-draft",
            },
          },
    ),
  };
}
const codeFor = (b) =>
  ({
    "merge-conflicts": 2,
    "review-threads": 3,
    "failing-checks": 4,
    "merge-gate": 6,
  })[b.kind] ?? 7;
const waitFingerprint = (frontier, reason, head) =>
  JSON.stringify([
    frontier.number,
    head,
    reason.kind,
    reason.pending?.map((c) => [c.id ?? c.name, c.reportedState]).sort() ??
      reason.unmergedCount,
  ]);
export function validateEvent(e) {
  fail(
    e &&
      e.schemaVersion === 2 &&
      Number.isSafeInteger(e.sequence) &&
      e.sequence > 0 &&
      typeof e.observedAt === "string" &&
      Number.isFinite(Date.parse(e.observedAt)) &&
      typeof e.terminal === "boolean" &&
      ["single", "stack", "queued-stack"].includes(e.mode) &&
      [
        "QUEUE",
        "STATUS",
        "WAITING",
        "ADVANCE",
        "RETRY",
        "BLOCKER",
        "READY",
        "COMPLETE",
        "TIMEOUT",
      ].includes(e.kind) &&
      (!Object.hasOwn(e, "authorizesExecution") ||
        e.authorizesExecution === false),
    "Invalid watcher envelope",
  );
  const validateContext = (context) => {
    fail(
      context &&
        typeof context.owner === "string" &&
        typeof context.repo === "string" &&
        typeof context.number === "number",
      "Invalid PR context",
    );
    repository(`${context.owner}/${context.repo}`);
    positive(context.number);
  };
  const empty = (value) => Array.isArray(value) && value.length === 0;
  if (e.kind === "READY") {
    fail(
      e.terminal &&
        e.exitCode === 0 &&
        Array.isArray(e.prs) &&
        e.prs.length &&
        e.mode !== "queued-stack" &&
        e.meaning === "forge-readiness-only" &&
        e.authorizesExecution === false,
      "Invalid READY event",
    );
    for (const pr of e.prs) {
      fail(
        pr && ["ready-pr", "merged-pr"].includes(pr.kind),
        "Invalid readiness row",
      );
      validateContext(pr.context);
      if (pr.kind === "ready-pr") {
        const p = pr.proof;
        fail(
          p &&
            p.mergeability === "clear" &&
            empty(p.threads) &&
            p.checks?.kind === "clean" &&
            p.checks.assessment?.kind === "allowed" &&
            p.checks.assessment.reason === "current-head-clean" &&
            p.checks.assessment.mergeStateStatus === "CLEAN" &&
            p.checks.assessment.headRollupState === "SUCCESS" &&
            empty(p.checks.failed) &&
            empty(p.checks.pending) &&
            empty(p.checks.unknown) &&
            Array.isArray(p.checks.checks) &&
            p.checks.checks.length > 0 &&
            Array.from(p.checks.checks).every(
              (c) =>
                c &&
                ["passed", "skipped"].includes(c.kind) &&
                typeof c.name === "string" &&
                typeof c.reportedState === "string" &&
                (c.id === undefined || typeof c.id === "string"),
            ) &&
            ["APPROVED", null].includes(p.reviewDecision) &&
            ["not-draft", "draft-allowed"].includes(p.draft),
          "READY lacks positive proof",
        );
        sha(p.headSha);
        sha(p.baseSha);
        fail(
          p.checks.headSha === p.headSha && p.checks.complete === true,
          "READY checks are not bound to the proven head",
        );
      } else
        fail(
          pr.mergedAt === null || typeof pr.mergedAt === "string",
          "Invalid merged timestamp",
        );
    }
  }
  if (e.kind === "COMPLETE") {
    fail(
      e.terminal &&
        e.exitCode === 0 &&
        e.mode === "queued-stack" &&
        Array.isArray(e.merged) &&
        Array.isArray(e.queue) &&
        e.queue.length > 0 &&
        e.merged.length === e.queue.length,
      "Incomplete queue cannot complete",
    );
    for (const [index, c] of e.queue.entries()) {
      validateContext(c);
      validateContext(e.merged[index]?.context);
      fail(
        JSON.stringify(e.merged[index].context) === JSON.stringify(c),
        "Merged row does not match captured queue",
      );
    }
  }
  if (e.kind === "BLOCKER")
    fail(
      e.terminal && e.exitCode === codeFor(e.blocker ?? {}),
      "Invalid blocker exit",
    );
  if (e.kind === "TIMEOUT")
    fail(e.terminal && e.exitCode === 5, "Invalid timeout exit");
  if (e.kind === "STATUS")
    fail(
      Array.isArray(e.rows) &&
        e.rows.length > 0 &&
        (!e.terminal || e.exitCode === 0),
      "Invalid status event",
    );
  if (["QUEUE", "WAITING", "ADVANCE", "RETRY"].includes(e.kind))
    fail(
      !e.terminal && !Object.hasOwn(e, "exitCode"),
      "Progress event cannot be terminal",
    );
  return e;
}

/** Stateful read-only observer. Queue identity is frozen; cached reads never authorize actions. */
export async function watch({
  reader,
  contexts,
  mode = "single",
  statusOnly = false,
  options = {},
  clock = realClock,
  emit = () => {},
  signal,
  checkpoint = null,
}) {
  const opts = { ...defaults, ...options };
  fail(
    ["single", "stack", "queued-stack"].includes(mode),
    "Invalid watch mode",
  );
  fail(
    contexts.length > 0 &&
      new Set(contexts.map((c) => `${c.owner}/${c.repo}#${c.number}`)).size ===
        contexts.length,
    "Queue is empty or has duplicates",
  );
  for (const c of contexts) {
    repository(`${c.owner}/${c.repo}`);
    positive(c.number);
    fail(
      c.owner === contexts[0].owner && c.repo === contexts[0].repo,
      "A watch queue must stay within one repository",
    );
  }
  for (const key of ["interval", "sweepInterval", "maxQueryErrors"])
    fail(Number.isFinite(opts[key]) && opts[key] > 0, `Invalid ${key}`);
  fail(
    Number.isSafeInteger(opts.maxQueryErrors) &&
      Number.isFinite(opts.timeout) &&
      opts.timeout >= 0,
    "Invalid watcher limits",
  );
  const queue = structuredClone(contexts);
  let sequence = 0,
    failures = 0,
    lastWait = null,
    frontier = null,
    nextSweep = 0;
  const snapshots = new Map();
  const start = clock.now(),
    deadline = opts.timeout > 0 ? start + opts.timeout : Infinity;
  reader.setDeadline?.(() => Math.max(0, (deadline - clock.now()) * 1000));
  const stamp = (kind, payload = {}, terminal = false, exitCode) =>
    validateEvent({
      schemaVersion: 2,
      sequence: ++sequence,
      observedAt: clock.observedAt(),
      mode,
      kind,
      terminal,
      ...(terminal ? { exitCode } : {}),
      ...payload,
    });
  const output = (e) => {
    emit(e);
    return e;
  };
  const expired = () => clock.now() >= deadline;
  const timeout = (reason) => stamp("TIMEOUT", { reason }, true, 5);
  const sleep = async (seconds) => {
    if (signal?.aborted)
      throw new ToolError("Operation cancelled", "CANCELLED", 130);
    try {
      await clock.sleep(
        Math.min(seconds, Math.max(0, deadline - clock.now())),
        signal,
      );
    } catch (error) {
      if (
        signal?.aborted ||
        error.name === "AbortError" ||
        error.code === "ABORT_ERR"
      )
        throw new ToolError("Operation cancelled", "CANCELLED", 130);
      throw error;
    }
  };
  const observe = async (c) => {
    for (;;) {
      if (signal?.aborted)
        throw new ToolError("Operation cancelled", "CANCELLED", 130);
      if (expired())
        return {
          terminal: timeout({ kind: "status-unavailable", frontier: c }),
        };
      try {
        if ("timeoutMs" in reader)
          reader.timeoutMs = Math.min(
            reader.timeoutMs,
            Math.max(1, (deadline - clock.now()) * 1000),
          );
        const row = await readSnapshot(reader, c, {
          pendingHistory: mode === "queued-stack" ? "omit" : "include",
        });
        failures = 0;
        if (expired())
          return {
            terminal: timeout({ kind: "status-unavailable", frontier: c }),
          };
        return { row };
      } catch (error) {
        if (error.code === "CANCELLED") throw error;
        const failure =
          error instanceof QueryError
            ? error.failure
            : error.exitCode === 7
              ? { kind: error.code, detail: error.message, retryable: true }
              : null;
        if (!failure) throw error;
        failures++;
        if (!failure.retryable || failures >= opts.maxQueryErrors)
          return {
            terminal: stamp(
              "BLOCKER",
              { blocker: { kind: "status-query", failure, failures } },
              true,
              7,
            ),
          };
        const seconds = backoff(opts.interval, failures);
        output(
          stamp("RETRY", {
            failure,
            consecutiveFailures: failures,
            retryInSeconds: Math.min(seconds, deadline - clock.now()),
          }),
        );
        if (expired())
          return { terminal: timeout({ kind: "status-unavailable", failure }) };
        await sleep(seconds);
      }
    }
  };
  const terminalDecision = (decision) =>
    stamp(
      "BLOCKER",
      { blocker: decision.blocker, allBlockers: decision.allBlockers },
      true,
      codeFor(decision.blocker),
    );
  if (mode === "queued-stack" && !statusOnly) output(stamp("QUEUE", { queue }));
  for (;;) {
    const sweep =
      statusOnly ||
      mode !== "queued-stack" ||
      snapshots.size === 0 ||
      clock.now() >= nextSweep;
    const targets = sweep
      ? queue.filter((c) => snapshots.get(c.number)?.kind !== "merged")
      : queue
          .filter((c) => snapshots.get(c.number)?.kind !== "merged")
          .slice(0, 1);
    for (const c of targets) {
      const result = await observe(c);
      if (result.terminal) return result.terminal;
      snapshots.set(c.number, result.row);
    }
    const rows = queue.map((c) => snapshots.get(c.number));
    if (rows.some((r) => !r))
      throw new ToolError("Incomplete queue snapshot", "INTERNAL");
    if (mode !== "single") {
      const positions = new Map(
        rows
          .filter((r) => r.kind === "open")
          .map((r, i) => [r.facts.headRefName, i]),
      );
      for (const [index, row] of rows
        .filter((r) => r.kind === "open")
        .entries()) {
        const parent = positions.get(row.facts.baseRefName);
        if (parent !== undefined && parent >= index)
          return stamp(
            "BLOCKER",
            {
              blocker: {
                kind: "status-query",
                failures: 1,
                failure: {
                  kind: "invalid-queue-order",
                  detail:
                    "Captured queue contradicts observed base/head dependency order",
                  retryable: false,
                },
              },
            },
            true,
            7,
          );
      }
    }
    if (statusOnly)
      return stamp("STATUS", { reason: "status-only", rows }, true, 0);
    if (mode !== "single" && sweep)
      output(
        stamp("STATUS", {
          reason: mode === "queued-stack" ? "whole-stack-sweep" : "poll",
          rows,
        }),
      );
    if (sweep) nextSweep = clock.now() + opts.sweepInterval;
    if (checkpoint)
      await checkpoint({
        schemaVersion: 1,
        queue,
        mode,
        observedAt: clock.observedAt(),
        snapshots: rows,
        requiresFreshReadOnResume: true,
      });
    const decision = classify(rows, opts);
    if (decision.kind === "blocker") return terminalDecision(decision);
    if (mode !== "queued-stack") {
      if (decision.kind === "ready")
        return stamp(
          "READY",
          {
            prs: decision.prs,
            meaning: "forge-readiness-only",
            authorizesExecution: false,
          },
          true,
          0,
        );
      output(
        stamp("WAITING", {
          frontier: decision.frontier,
          reason: { kind: "pending-checks", pending: decision.pending },
        }),
      );
      if (expired())
        return timeout({ kind: "pending-checks", frontier: decision.frontier });
      await sleep(opts.interval);
      continue;
    }
    const active = rows.filter((r) => r.kind !== "merged");
    if (!active.length)
      return stamp(
        "COMPLETE",
        {
          queue,
          merged: rows.map((r) => ({
            context: r.context,
            mergedAt: r.facts.mergedAt,
          })),
        },
        true,
        0,
      );
    const current = active[0];
    if (frontier && frontier.number !== current.context.number) {
      output(
        stamp("ADVANCE", {
          merged: frontier,
          frontier: current.context,
          remaining: active.length,
        }),
      );
      frontier = current.context;
      lastWait = null;
      continue;
    }
    frontier = current.context;
    const reason = current.checks.pending.length
      ? { kind: "pending-checks", pending: current.checks.pending }
      : { kind: "merge-queue", unmergedCount: active.length };
    const key = waitFingerprint(frontier, reason, current.observedHead);
    if (key !== lastWait) {
      output(stamp("WAITING", { frontier, reason }));
      lastWait = key;
    }
    if (expired())
      return timeout({
        kind: "queued-stack",
        frontier,
        unmergedCount: active.length,
      });
    await sleep(opts.interval);
  }
}
export const renderJson = (e) => JSON.stringify(e) + "\n";
export function renderPretty(e) {
  if (e.kind === "STATUS")
    return (
      [
        "| PR | CI | Review | Merge |",
        "| --- | --- | --- |",
        ...e.rows.map(
          (r) =>
            `| #${r.context.number} | ${r.kind === "open" ? markdown(r.checks.kind) : r.kind} | ${r.kind === "open" ? (r.reviewAutomationRunning ? "automation running; " : "") + r.threads.length + " open" : "none"} | ${markdown(r.facts.mergeStateStatus)} |`,
        ),
      ].join("\n") + "\n"
    );
  if (e.kind === "BLOCKER")
    return `BLOCKER: ${e.blocker.kind}${e.blocker.pr ? ` #${e.blocker.pr.number}` : ""}${e.blocker.reason ? ` (${e.blocker.reason})` : ""}${e.blocker.failure ? `: ${e.blocker.failure.detail}` : ""}\n`;
  if (e.kind === "WAITING")
    return `WAITING: #${e.frontier.number} ${e.reason.kind}${e.reason.pending ? ` (${e.reason.pending.length} checks)` : ""}\n`;
  if (e.kind === "READY")
    return "READY: current-head forge checks are clear; verification and action permission are separate\n";
  if (e.kind === "COMPLETE")
    return `COMPLETE: ${e.merged.length} captured PRs are merged\n`;
  if (e.kind === "QUEUE")
    return `QUEUE: ${e.queue.map((c) => "#" + c.number).join(", ")}\n`;
  if (e.kind === "ADVANCE")
    return `ADVANCE: #${e.merged.number} merged; frontier #${e.frontier.number}\n`;
  if (e.kind === "RETRY")
    return `RETRY: ${e.failure.detail}; ${e.retryInSeconds}s\n`;
  return `TIMEOUT: ${e.reason.kind}\n`;
}
