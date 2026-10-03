import test from "node:test";
import assert from "node:assert/strict";
import {
  mkdtemp,
  readFile,
  writeFile,
  readdir,
  rm,
  mkdir,
  symlink,
} from "node:fs/promises";
import { spawn } from "node:child_process";
import { hostname, tmpdir } from "node:os";
import { join } from "node:path";
import { recoverLock } from "../lib/atomic-store.mjs";
import {
  GitHubReader,
  annotateReviewThreads,
  resolveChecks,
  parsePullRequest,
} from "../lib/github-reader.mjs";
import {
  watch,
  readSnapshot,
  classify,
  validateEvent,
} from "../lib/watcher.mjs";
import { main } from "../dot-stack.mjs";
import { Orchestrator } from "../lib/orchestration.mjs";
import { parsePlan, checkPlan } from "../lib/plan-check.mjs";
import { discoverGraph } from "../lib/graph.mjs";
import {
  fakeReader,
  fakeClock,
  context,
  check,
  HEAD,
  BASE,
} from "./support/fakes.mjs";

test("explicit dead same-host lock recovery quarantines the original", async (t) => {
  const dir = await mkdtemp(join(tmpdir(), "dot-stack-recover-"));
  t.after(() => rm(dir, { recursive: true, force: true }));
  const child = spawn(process.execPath, ["-e", ""]);
  await new Promise((resolve) => child.once("exit", resolve));
  const owner = { token: "dead-token", pid: child.pid, host: hostname() };
  await writeFile(join(dir, ".writer.lock"), JSON.stringify(owner));
  const result = await recoverLock(dir, "dead-token");
  assert.equal(result.recovered, true);
  assert.deepEqual(
    JSON.parse(await readFile(result.quarantine, "utf8")),
    owner,
  );
  assert.equal((await readdir(dir)).includes(".writer.lock"), false);
});
test("configured review automation counts observed distinct runs including resolved threads", () => {
  const make = (id, runId, resolved = false) => ({
    id,
    resolved,
    firstComment: {
      authorLogin: "review-worker",
      body: `REVIEW_RUN: ${runId}`,
      path: null,
      line: null,
      createdAt: "now",
    },
    automation: null,
  });
  const rows = annotateReviewThreads(
    [make("1", "run-1"), make("2", "run-1"), make("3", "run-2", true)],
    { automationAuthors: ["review-worker"], runIdMarkers: ["REVIEW_RUN:"] },
  );
  assert.equal(rows.length, 2);
  assert.equal(rows[0].observedReviewPasses, 2);
  assert.equal(rows[0].automation.runId, "run-1");
  assert.equal(annotateReviewThreads([make("1", "run-1")])[0].automation, null);
});
test("commit-bound fallback survives unusable and empty PR-check fast paths", async () => {
  for (const fast of [
    { kind: "unusable", exitCode: 8 },
    { kind: "checks", checks: [] },
  ]) {
    const r = fakeReader();
    r.checksFastPath = async () => fast;
    const result = await resolveChecks(r, context(1), HEAD);
    assert.equal(result.headSha, HEAD);
    assert.equal(result.source, "fake-commit");
  }
});
test("known pending aggregate cannot be hidden behind passing visible checks", async () => {
  const snapshot = await readSnapshot(
    fakeReader({ rollupState: "PENDING" }),
    context(1),
  );
  const decision = classify([snapshot]);
  assert.equal(decision.kind, "waiting");
  assert.equal(decision.pending[0].id, "forge-rollup");
});
test("invalid remote commit identity is a structured status-query error", async () => {
  const raw = await fakeReader().pullRequest(context(1));
  assert.throws(
    () => parsePullRequest({ ...raw, headRefOid: "short" }, context(1)),
    (e) => e.exitCode === 7 && e.failure.kind === "invalid-response",
  );
});
test("GitHub commit transport paginates against one explicit SHA", async () => {
  const calls = [];
  let page = 0;
  const r = new GitHubReader({
    runner: async (exe, args) => {
      calls.push(args);
      page++;
      return {
        code: 0,
        stderr: "",
        stdout: JSON.stringify({
          data: {
            repository: {
              object: {
                oid: HEAD,
                statusCheckRollup: {
                  state: "SUCCESS",
                  contexts: {
                    nodes: [
                      {
                        __typename: "CheckRun",
                        name: "ci-" + page,
                        status: "COMPLETED",
                        conclusion: "SUCCESS",
                        detailsUrl: "",
                      },
                    ],
                    pageInfo: {
                      hasNextPage: page === 1,
                      endCursor: page === 1 ? "page-2" : null,
                    },
                  },
                },
              },
            },
          },
        }),
      };
    },
  });
  const result = await r.checksAt(context(1), HEAD);
  assert.equal(result.checks.length, 2);
  assert.ok(calls.every((args) => args.includes(`oid=${HEAD}`)));
  assert.ok(calls[1].includes("after=page-2"));
});
test("queue rejects reversed live dependency order and mixed repositories", async () => {
  const r = fakeReader({
    onRead: (c, n, f) => ({
      ...f,
      headRefName: c.number === 1 ? "bottom" : "top",
      baseRefName: c.number === 2 ? "bottom" : "main",
    }),
  });
  const invalid = await watch({
    reader: r,
    contexts: [context(2), context(1)],
    mode: "queued-stack",
    clock: fakeClock(),
  });
  assert.equal(invalid.exitCode, 7);
  assert.match(invalid.blocker.failure.detail, /dependency order/);
  await assert.rejects(
    watch({
      reader: fakeReader(),
      contexts: [context(1), { ...context(2), repo: "other" }],
      clock: fakeClock(),
    }),
    /one repository/,
  );
});
test("queue sweep cadence and wait deduplication are deterministic", async () => {
  const r = fakeReader(),
    events = [];
  const result = await watch({
    reader: r,
    contexts: [context(1)],
    mode: "queued-stack",
    clock: fakeClock(),
    options: { interval: 1, sweepInterval: 2, timeout: 3 },
    emit: (e) => events.push(e),
  });
  assert.equal(result.kind, "TIMEOUT");
  assert.equal(events.filter((e) => e.kind === "STATUS").length, 2);
  assert.equal(events.filter((e) => e.kind === "WAITING").length, 1);
});
test("CLI defaults and strict numeric and irrelevant-option parsing", async () => {
  for (const args of [
    ["watch-pr", "--max-query-errors", "1.5"],
    ["watch-pr", "--pr", "9007199254740993"],
    ["orch", "unit", "list", "--question", "ignored"],
  ]) {
    let output = "";
    const code = await main(args, {
      reader: fakeReader(),
      stdout: (s) => (output += s),
      stderr: () => {},
    });
    assert.equal(code, 64);
    assert.equal(output, "");
  }
  const r = fakeReader();
  let output = "";
  assert.equal(
    await main(["watch-pr", "--status-only"], {
      reader: r,
      clock: fakeClock(),
      stdout: (s) => (output += s),
      stderr: () => {},
    }),
    0,
  );
  assert.ok(r.calls.includes("currentPr"));
  assert.equal(JSON.parse(output).mode, "single");
});
test("ORCH_STORE selects target state without package cache writes", async (t) => {
  const dir = await mkdtemp(join(tmpdir(), "dot-stack-env-"));
  t.after(() => rm(dir, { recursive: true, force: true }));
  const old = process.env.ORCH_STORE;
  process.env.ORCH_STORE = dir;
  try {
    const code = await main(["orch", "init"], {
      stdout: () => {},
      stderr: () => {},
    });
    assert.equal(code, 0);
    assert.equal(
      JSON.parse(await readFile(join(dir, "state.json"), "utf8")).schemaVersion,
      1,
    );
  } finally {
    if (old === undefined) delete process.env.ORCH_STORE;
    else process.env.ORCH_STORE = old;
  }
});
test("forge checks timeout budget respects the observer deadline", async () => {
  let observed;
  const r = new GitHubReader({
    runner: async (exe, args, config) => {
      observed = config.timeoutMs;
      return { code: 0, stdout: "", stderr: "" };
    },
  });
  r.setDeadline(() => 42);
  await r.command("git", ["remote", "get-url", "origin"]);
  assert.equal(observed, 42);
  r.setDeadline(() => 0);
  await assert.rejects(
    r.command("git", ["remote", "get-url", "origin"]),
    /deadline/,
  );
});
test("mixed-case commit identities cannot resurrect superseded passing evidence", async (t) => {
  const dir = await mkdtemp(join(tmpdir(), "dot-stack-case-"));
  t.after(() => rm(dir, { recursive: true, force: true }));
  const store = new Orchestrator(dir);
  await store.init();
  await store.ledgerRecord({
    pr: 1,
    sha: HEAD,
    verdict: "unit-test-verified",
    evidence: "old.log",
  });
  await store.ledgerRecord({
    pr: 1,
    sha: HEAD.toUpperCase(),
    verdict: "verifier-failed",
    evidence: "new.log",
  });
  await assert.rejects(
    store.ledgerCheck({ pr: 1, sha: HEAD, requirePass: true }),
    /NOT-VERIFIED/,
  );
  const path = join(dir, "state.json"),
    state = JSON.parse(await readFile(path, "utf8"));
  state.ledger[1].sha = HEAD.toUpperCase();
  await writeFile(path, JSON.stringify(state));
  await assert.rejects(
    store.ledgerCheck({ pr: 1, sha: HEAD, requirePass: true }),
    /NOT-VERIFIED/,
  );
});
test("delayed older status return cannot overwrite a newer status file", async (t) => {
  const dir = await mkdtemp(join(tmpdir(), "dot-stack-status-"));
  t.after(() => rm(dir, { recursive: true, force: true }));
  const first = new Orchestrator(dir),
    second = new Orchestrator(dir);
  await first.init();
  const original = first.store.transact.bind(first.store);
  let reached, release;
  const entered = new Promise((r) => (reached = r)),
    held = new Promise((r) => (release = r));
  first.store.transact = async (...args) => {
    const result = await original(...args);
    reached();
    await held;
    return result;
  };
  const old = first.status();
  await entered;
  await second.unitAdd({ id: "new-work", track: "main" });
  const fresh = await second.status();
  release();
  await old;
  const text = await readFile(join(dir, "status.md"), "utf8");
  assert.match(text, /new-work/);
  assert.ok(text.includes(`State revision: ${fresh.revision}`));
});
const evidencePlan = `# Plan\n## Inputs\nsource\n## Phases\nphases\n## Unit\n**ID.** unit\n**Surface.** cli\n**Depends on.** None.\n**Files.** tool.mjs\n**Build.** Reject malformed input\n**Accept.** Invalid input fails\n**Verify, unit.** Run tests. Evidence: \`inside/evidence.log\` Pass when successful\n**Verify, live.** Not applicable. A pure syntax check has no running surface\n**Verify, perf.** Not applicable. This has no execution performance impact\n**Review gate.** Review before delivery\n**Delivery.** Local result\n## Close\nDone\n`;
test("evidence symlink outside root and empty destination never pass validation", async (t) => {
  assert.ok(
    parsePlan(
      evidencePlan.replace("Evidence: `inside/evidence.log`", "Evidence:"),
    ).problems.some((p) => p.code === "EVIDENCE"),
  );
  const dir = await mkdtemp(join(tmpdir(), "dot-stack-evidence-"));
  t.after(() => rm(dir, { recursive: true, force: true }));
  const project = join(dir, "project");
  await mkdir(join(project, "inside"), { recursive: true });
  await writeFile(join(dir, "outside.log"), "outside");
  await symlink(join(dir, "outside.log"), join(project, "inside/evidence.log"));
  await writeFile(join(project, "plan.md"), evidencePlan);
  const report = await checkPlan(join(project, "plan.md"), {
    verifyEvidence: true,
    root: project,
  });
  assert.ok(report.problems.some((p) => p.code === "OUTSIDE_ROOT"));
});
test("repository case normalization preserves discovered parent edges", () => {
  const rows = [
    {
      number: 1,
      headRefName: "parent",
      baseRefName: "main",
      headRepository: "owner/repo",
    },
    {
      number: 2,
      headRefName: "child",
      baseRefName: "parent",
      headRepository: "owner/repo",
    },
  ];
  assert.deepEqual(
    discoverGraph({ owner: "Owner", repo: "Repo", number: 2 }, rows).map(
      (r) => r.number,
    ),
    [1, 2],
  );
});
test("abort during actual sleep returns documented cancellation status", async () => {
  const signal = new AbortController();
  let output = "";
  const promise = main(
    ["watch-pr", "--owner", "o", "--repo", "r", "--pr", "1"],
    {
      reader: fakeReader({
        checks: [check("pending")],
        rollupState: "PENDING",
      }),
      signal: signal.signal,
      stdout: (s) => {
        output += s;
        if (s.includes("WAITING")) setTimeout(() => signal.abort(), 5);
      },
      stderr: () => {},
    },
  );
  assert.equal(await promise, 130);
  assert.match(output, /WAITING/);
});
test("queued terminal errors preserve mode sequence and pretty renderer", async () => {
  const reader = () =>
    fakeReader({
      onRead: (c, n, f) => ({
        ...f,
        headRefName: c.number === 1 ? "bottom" : "top",
        baseRefName: c.number === 2 ? "bottom" : "main",
      }),
    });
  let output = "";
  assert.equal(
    await main(
      [
        "watch-pr",
        "--owner",
        "o",
        "--repo",
        "r",
        "--queued-stack",
        "--stack-prs",
        "2,1",
      ],
      {
        reader: reader(),
        clock: fakeClock(),
        stdout: (s) => (output += s),
        stderr: () => {},
      },
    ),
    7,
  );
  const events = output.trim().split("\n").map(JSON.parse);
  assert.deepEqual(
    events.map((e) => e.sequence),
    [1, 2],
  );
  assert.ok(events.every((e) => e.mode === "queued-stack"));
  output = "";
  await main(
    [
      "watch-pr",
      "--owner",
      "o",
      "--repo",
      "r",
      "--queued-stack",
      "--stack-prs",
      "2,1",
      "--pretty",
    ],
    {
      reader: reader(),
      clock: fakeClock(),
      stdout: (s) => (output += s),
      stderr: () => {},
    },
  );
  assert.match(output, /BLOCKER:/);
  assert.equal(output.includes('"schemaVersion"'), false);
});
test("exported readiness validator rejects forged authority discriminants and unbound proof", async () => {
  const valid = await watch({
    reader: fakeReader(),
    contexts: [context(1)],
    clock: fakeClock(),
  });
  for (const mutate of [
    (e) => (e.authorizesExecution = true),
    (e) => (e.prs = [{ kind: "not-a-pr" }]),
    (e) => (e.mode = "queued-stack"),
    (e) => (e.meaning = "permission-to-merge"),
    (e) => (e.prs[0].proof.checks.complete = false),
    (e) => (e.prs[0].proof.checks.headSha = BASE),
    (e) => (e.prs[0].proof.reviewDecision = "MAYBE"),
    (e) => (e.prs[0].context.number = "1"),
  ]) {
    const copy = structuredClone(valid);
    mutate(copy);
    assert.throws(() => validateEvent(copy));
  }
});
test("existing store directory symlink is rejected for reads writes exports and recovery", async (t) => {
  const dir = await mkdtemp(join(tmpdir(), "dot-stack-alias-"));
  t.after(() => rm(dir, { recursive: true, force: true }));
  const real = join(dir, "real"),
    alias = join(dir, "alias");
  const store = new Orchestrator(real);
  await store.init();
  await symlink(real, alias, "dir");
  const before = await readFile(join(real, "state.json"), "utf8");
  const redirected = new Orchestrator(alias);
  await assert.rejects(redirected.unitsList(), (e) => e.code === "UNSAFE_PATH");
  await assert.rejects(
    redirected.unitAdd({ id: "bad", track: "t" }),
    (e) => e.code === "UNSAFE_PATH",
  );
  await assert.rejects(
    redirected.exportViews(),
    (e) => e.code === "UNSAFE_PATH",
  );
  await assert.rejects(
    recoverLock(alias, "token"),
    (e) => e.code === "UNSAFE_PATH",
  );
  assert.equal(await readFile(join(real, "state.json"), "utf8"), before);
});
