import test from "node:test";
import assert from "node:assert/strict";
import {
  mkdtemp,
  readFile,
  writeFile,
  rm,
  mkdir,
  symlink,
} from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { execFileSync } from "node:child_process";
import { parsePlan, checkPlan } from "../lib/plan-check.mjs";
import {
  parseWorktrees,
  parseStatus,
  auditWorktrees,
} from "../lib/worktree-audit.mjs";
import { appendDecision, LOG_HEADER } from "../lib/decision-log.mjs";
import { runCommand, assertReadCommand, cell } from "../lib/core.mjs";
import { atomicWrite } from "../lib/atomic-store.mjs";
import { HEAD } from "./support/fakes.mjs";

async function temporary(t) {
  const dir = await mkdtemp(join(tmpdir(), "dot-stack-helper-"));
  t.after(() => rm(dir, { recursive: true, force: true }));
  return dir;
}
export const plan = (surface = "cli") => `# Demo plan
## Inputs
Candidate ${HEAD}. Scope is the named files. Execute only when authorized.
## Phases
Run the following units in dependency order.
## Implement parser
**ID.** parser
**Surface.** ${surface}
**Depends on.** None.
**Files.**
- [ ] Edit src/parser.mjs
**Build.**
- [ ] Reject unknown input
**Accept.** Invalid input returns status 64
**Verify, unit.** Run node --test. Evidence: evidence/unit.log; Pass when assertions pass
**Verify, live.** Exercise the ${surface} scenario. Evidence: evidence/live.log; Pass when observable result matches
**Verify, perf.** Not applicable. This only changes a documentation label with no execution impact
**Review gate.** None. No external action is requested
**Delivery.** Hand off local results; request publishing permission separately
## Close
Every applicable acceptance condition has evidence
`;
test("surface-specific plans need no universal screenshots or lane quota", () => {
  for (const surface of ["docs", "cli", "service", "ui", "mixed"])
    assert.equal(parsePlan(plan(surface)).valid, true);
});
test("plan missing evidence predicate dependencies and placeholders are diagnosed", () => {
  const source = plan()
    .replace("Depends on.** None.", "Depends on.** missing.")
    .replace("Pass when assertions pass", "looks good")
    .replace("Evidence: evidence/live.log;", "")
    .replace("Reject unknown input", "TODO");
  const codes = parsePlan(source).problems.map((p) => p.code);
  for (const expected of ["DEPENDENCY", "PREDICATE", "EVIDENCE", "PLACEHOLDER"])
    assert.ok(codes.includes(expected));
});
test("UI live evidence cannot be waived while concrete non-UI rationale can", () => {
  const na = plan("ui").replace(
    "Exercise the ui scenario. Evidence: evidence/live.log; Pass when observable result matches",
    "Not applicable. There is no local browser available",
  );
  assert.ok(parsePlan(na).problems.some((p) => p.code === "UI_EVIDENCE"));
  const docs = na.replace("Surface.** ui", "Surface.** docs");
  assert.equal(parsePlan(docs).valid, true);
});
test("fences and frontmatter ignore fake headings and detect incomplete structure", () => {
  assert.equal(
    parsePlan(
      "---\nname: example\n---\n" +
        plan() +
        "\n~~~~\n## Fake\n**ID.** fake\n~~~~\n",
    ).valid,
    true,
  );
  assert.ok(
    parsePlan(plan() + "\n```\n").problems.some((p) => p.code === "FENCE"),
  );
  assert.ok(
    parsePlan("---\nname: unfinished\n").problems.some(
      (p) => p.code === "FRONTMATTER",
    ),
  );
  assert.equal(parsePlan(plan().replaceAll("\n", "\r\n")).valid, true);
});
test("duplicate phase blocks identifiers and dependency cycles fail", () => {
  const unit = plan().split("## Implement parser")[1].split("## Close")[0];
  const duplicate = plan().replace(
    "## Close",
    `## Duplicate\n${unit}\n## Close`,
  );
  assert.ok(
    parsePlan(duplicate).problems.some((p) => p.code === "DUPLICATE_ID"),
  );
  assert.ok(
    parsePlan(
      plan().replace("**Build.**", "**Build.** Duplicate\n**Build.**"),
    ).problems.some((p) => p.code === "DUPLICATE_BLOCK"),
  );
  assert.ok(
    parsePlan(plan().replace("None.", "parser.")).problems.some(
      (p) => p.code === "CYCLE",
    ),
  );
});
test("evidence verification is rooted and candidate-specific without executing commands", async (t) => {
  const dir = await temporary(t);
  await mkdir(join(dir, "evidence"));
  await writeFile(join(dir, "evidence/unit.log"), "pass");
  await writeFile(join(dir, "evidence/live.log"), "pass");
  const p = join(dir, "plan.md");
  await writeFile(p, plan());
  assert.equal(
    (await checkPlan(p, { verifyEvidence: true, root: dir, head: HEAD })).valid,
    true,
  );
  await writeFile(p, plan().replace("evidence/unit.log", "../../outside"));
  assert.ok(
    (await checkPlan(p, { verifyEvidence: true, root: dir })).problems.some(
      (p) => p.code === "OUTSIDE_ROOT",
    ),
  );
});
test("worktree NUL parser preserves spaces tabs Unicode and newline paths", () => {
  const path = "/tmp/work tree\t雪\nline";
  const rows = parseWorktrees(
    `worktree ${path}\0HEAD ${HEAD}\0branch refs/heads/feature\0locked active work\0\0worktree /tmp/bare\0bare\0\0`,
  );
  assert.equal(rows[0].path, path);
  assert.equal(rows[0].locked, true);
  assert.equal(rows[1].bare, true);
});
test("status parser distinguishes tracked untracked and consumes rename source record", () => {
  const s = parseStatus(" M file\0?? new\nfile\0R  new name\0old name\0");
  assert.equal(s.tracked.length, 2);
  assert.deepEqual(s.untracked, ["new\nfile"]);
  assert.equal(s.tracked[1].path, "new name");
});
test("local Git worktree audit preserves dirty data and never fetches or deletes", async (t) => {
  const dir = await temporary(t);
  const repo = join(dir, "repo"),
    worktree = join(dir, "work tree 雪");
  await mkdir(repo);
  const git = (...args) =>
    execFileSync("git", ["-C", repo, ...args], {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "pipe"],
    });
  git("init", "--initial-branch=main");
  git("config", "user.name", "Fixture");
  git("config", "user.email", "fixture@example.invalid");
  await writeFile(join(repo, "tracked"), "initial");
  git("add", "tracked");
  git("commit", "-m", "initial");
  git("worktree", "add", "-b", "feature", worktree);
  await writeFile(join(worktree, "tracked"), "changed");
  await writeFile(join(worktree, "untracked"), "valuable");
  const calls = [];
  const runner = async (exe, args, config) => {
    calls.push(args);
    return runCommand(exe, args, config);
  };
  const report = await auditWorktrees(repo, {
    runner,
    trunk: "main",
    active: [worktree],
  });
  const row = report.rows.find((r) => r.path === worktree);
  assert.ok(row.reasons.includes("active"));
  assert.ok(row.reasons.includes("tracked-changes"));
  assert.ok(row.reasons.includes("untracked-data"));
  assert.equal(row.deletionAuthorized, false);
  assert.equal(
    calls.some((args) =>
      args.some((a) => ["fetch", "remove", "prune"].includes(a)),
    ),
    false,
  );
  assert.equal(await readFile(join(worktree, "untracked"), "utf8"), "valuable");
});
test("audit preserves unavailable status and closed-unmerged risk", async (t) => {
  const dir = await temporary(t);
  const runner = async (exe, args) => {
    if (args.includes("list"))
      return {
        code: 0,
        stdout: `worktree ${dir}\0HEAD ${HEAD}\0branch refs/heads/f\0\0`,
        stderr: "",
      };
    return { code: 128, stdout: "", stderr: "unavailable" };
  };
  const r = await auditWorktrees(dir, {
    runner,
    prObservations: [{ headRefName: "f", state: "CLOSED" }],
  });
  assert.ok(r.rows[0].reasons.includes("inspection-incomplete"));
  assert.ok(r.rows[0].reasons.includes("closed-unmerged"));
  assert.equal(r.rows[0].merged, null);
});
test("decision log append sanitizes cells and never rewrites earlier bytes", async (t) => {
  const dir = await temporary(t),
    file = join(dir, "decisions.tsv");
  await appendDecision(file, [
    "phase",
    "=SUM(A1)",
    "why\nline",
    "@evidence",
    "done",
  ]);
  const first = await readFile(file, "utf8");
  assert.match(first, /'=SUM/);
  assert.match(first, /'@evidence/);
  await appendDecision(file, [
    "correct",
    "supersede prior row",
    "new evidence",
    "file",
    "fixed",
  ]);
  assert.ok((await readFile(file, "utf8")).startsWith(first));
  assert.equal(cell(" \t=bad"), "'  =bad");
});
test("concurrent decision log first writes produce one header and intact rows", async (t) => {
  const dir = await temporary(t),
    file = join(dir, "log.tsv");
  await Promise.all(
    Array.from({ length: 15 }, (_, i) =>
      appendDecision(file, ["work", `decision ${i}`, "why", "receipt", "done"]),
    ),
  );
  const rows = (await readFile(file, "utf8")).trimEnd().split("\n");
  assert.equal(rows.length, 16);
  assert.equal(rows.filter((r) => r === LOG_HEADER).length, 1);
  assert.ok(rows.every((r) => r.split("\t").length === 6));
});
test("log refuses wrong header and partial rows without truncation", async (t) => {
  const dir = await temporary(t),
    file = join(dir, "log.tsv");
  for (const raw of ["wrong\n", LOG_HEADER + "\npartial"]) {
    await writeFile(file, raw);
    await assert.rejects(appendDecision(file, ["p", "d", "w", "e", "r"]));
    assert.equal(await readFile(file, "utf8"), raw);
  }
});
test("log run switches add start rows with provenance", async (t) => {
  const dir = await temporary(t),
    file = join(dir, "log.tsv");
  for (const run of ["one", "one", "two", "one"])
    await appendDecision(file, ["work", "d", "w", "e", "r"], { run });
  const rows = (await readFile(file, "utf8")).split("\n");
  assert.equal(rows.filter((r) => r.split("\t")[1] === "start").length, 3);
});
test("atomic fault before rename leaves old complete content; after rename leaves new complete content", async (t) => {
  const dir = await temporary(t),
    file = join(dir, "state");
  await writeFile(file, "old");
  await assert.rejects(
    atomicWrite(file, "new", {
      beforeRename: () => {
        throw Error("crash");
      },
    }),
  );
  assert.equal(await readFile(file, "utf8"), "old");
  await assert.rejects(
    atomicWrite(file, "new", {
      afterRename: () => {
        throw Error("crash");
      },
    }),
  );
  assert.equal(await readFile(file, "utf8"), "new");
});
test("bounded runner catches missing executable oversized output timeout and cancellation", async () => {
  await assert.rejects(
    runCommand("dot-stack-nonexistent-tool-xyz", []),
    (e) => e.code === "MISSING_TOOL",
  );
  await assert.rejects(
    runCommand(
      process.execPath,
      ["-e", 'process.stdout.write("x".repeat(10000))'],
      { maxBytes: 100 },
    ),
    (e) => e.code === "OUTPUT_LIMIT",
  );
  await assert.rejects(
    runCommand(
      process.execPath,
      ["-e", 'process.on("SIGTERM",()=>{});setInterval(()=>{},1000)'],
      { timeoutMs: 50 },
    ),
    (e) => e.code === "COMMAND_TIMEOUT",
  );
  const abort = new AbortController();
  abort.abort();
  await assert.rejects(
    runCommand(process.execPath, ["--version"], { signal: abort.signal }),
    (e) => e.code === "CANCELLED",
  );
});
test("read-only allowlist rejects mutation executable classes", () => {
  for (const [exe, args] of [
    ["git", ["fetch", "origin"]],
    ["git", ["worktree", "remove", "path"]],
    ["git", ["push"]],
    ["gh", ["pr", "merge", "1"]],
    ["gh", ["auth", "login"]],
    ["npm", ["install"]],
    ["gh", ["api", "graphql", "-f", "query=mutation { a }"]],
  ])
    assert.throws(() => assertReadCommand(exe, args));
});
