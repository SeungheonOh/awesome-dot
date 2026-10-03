import test from "node:test";
import assert from "node:assert/strict";
import {
  mkdtemp,
  readFile,
  writeFile,
  rm,
  readdir,
  symlink,
  chmod,
  stat,
} from "node:fs/promises";
import { tmpdir, hostname } from "node:os";
import { join } from "node:path";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";
import { Orchestrator, validateState } from "../lib/orchestration.mjs";
import { atomicWrite, withLock, recoverLock } from "../lib/atomic-store.mjs";
import {
  validateGraph,
  discoverGraph,
  mutationRequest,
} from "../lib/graph.mjs";
import { HEAD, BASE, NEXT, graph, context } from "./support/fakes.mjs";

async function setup(t) {
  const dir = await mkdtemp(join(tmpdir(), "dot-stack-store-"));
  t.after(() => rm(dir, { recursive: true, force: true }));
  const store = new Orchestrator(dir);
  await store.init();
  t.after(() => store.close());
  return { dir, store };
}
test("init is idempotent and reads do not change revision", async (t) => {
  const { dir, store } = await setup(t);
  const first = await readFile(join(dir, "state.json"), "utf8");
  await store.init();
  await store.unitsList();
  assert.equal(await readFile(join(dir, "state.json"), "utf8"), first);
  assert.deepEqual(await readdir(dir), ["state.json"]);
});
test("units preserve raw identifiers and compose add set get filters counts", async (t) => {
  const { store } = await setup(t);
  await store.unitAdd({ id: "=SUM(A1)", track: "+build" });
  await store.unitAdd({ id: "u1", track: "build", brief: "brief.md" });
  await store.unitSet("u1", {
    state: "done",
    pr: 3,
    sha: HEAD,
    branch: "feature",
  });
  assert.equal((await store.unitGet("u1")).sha, HEAD);
  assert.equal(
    (await store.unitsList({ state: "done", track: "build" })).length,
    1,
  );
  assert.deepEqual(await store.unitCounts(), { done: 1, pending: 1 });
  assert.equal((await store.unitGet("=SUM(A1)")).id, "=SUM(A1)");
  await assert.rejects(
    store.unitAdd({ id: "u1", track: "build" }),
    /already exists/,
  );
  await assert.rejects(
    store.unitSet("missing", { state: "done" }),
    (e) => e.exitCode === 2,
  );
});
test("ledger exact head, supersession, history and typed verdicts", async (t) => {
  const { store } = await setup(t);
  await assert.rejects(
    store.ledgerCheck({ pr: 1, sha: HEAD }),
    (e) => e.code === "NOT_VERIFIED",
  );
  await store.ledgerRecord({
    pr: 1,
    sha: HEAD,
    verdict: "unit-test-verified",
    evidence: "test.log",
  });
  await store.ledgerRecord({
    pr: 1,
    sha: HEAD,
    verdict: "behavior-verified",
    evidence: "live.log",
    baseSha: BASE,
    profile: "cli",
  });
  assert.equal(
    (
      await store.ledgerCheck({
        pr: 1,
        sha: HEAD,
        baseSha: BASE,
        profile: "cli",
        requirePass: true,
      })
    ).verdict,
    "behavior-verified",
  );
  assert.equal((await store.store.read()).ledger.length, 2);
  assert.deepEqual(await store.ledgerSummary(), { "behavior-verified": 1 });
  await assert.rejects(store.ledgerCheck({ pr: 1, sha: NEXT }), /NOT-VERIFIED/);
  await assert.rejects(
    store.ledgerCheck({ pr: 1, sha: HEAD, baseSha: NEXT }),
    /NOT-VERIFIED/,
  );
  assert.throws(
    () =>
      store.ledgerRecord({ pr: 1, sha: HEAD, verdict: "fine", evidence: "x" }),
    /Verdict/,
  );
});
test("failed blocked and type-only evidence cannot meet a passing predicate", async (t) => {
  const { store } = await setup(t);
  for (const verdict of [
    "verifier-blocked",
    "verifier-failed",
    "type-check-only",
  ]) {
    await store.ledgerRecord({ pr: 1, sha: HEAD, verdict, evidence: "r" });
    await assert.rejects(
      store.ledgerCheck({ pr: 1, sha: HEAD, requirePass: true }),
      /NOT-VERIFIED/,
    );
  }
});
test("inbox claims durably, replays before ack and keeps arrivals for next batch", async (t) => {
  const { store } = await setup(t);
  await store.inboxPush({
    agent: "a",
    unit: "u",
    status: "done",
    idempotencyKey: "one",
  });
  const batch = await store.inboxDrain();
  assert.equal(batch.pointers.length, 1);
  await store.inboxPush({ agent: "b", unit: "v", status: "done" });
  assert.equal((await store.inboxDrain()).id, batch.id);
  assert.equal((await store.inboxDrain()).replay, true);
  await store.inboxAck(batch.id);
  await store.inboxAck(batch.id);
  assert.equal((await store.inboxDrain()).pointers[0].agent, "b");
  assert.equal((await store.store.read()).inbox.length, 2);
});
test("inbox idempotency rejects conflicting payload and unknown ack", async (t) => {
  const { store } = await setup(t);
  const params = { agent: "a", unit: "u", status: "done", idempotencyKey: "k" };
  const a = await store.inboxPush(params),
    b = await store.inboxPush(params);
  assert.equal(a.id, b.id);
  await assert.rejects(
    store.inboxPush({ ...params, status: "bad" }),
    /different data/,
  );
  await assert.rejects(store.inboxAck("missing"), (e) => e.exitCode === 2);
});
test("gates are reversible bookkeeping with history and no implied execution", async (t) => {
  const { store } = await setup(t);
  await store.gatePark({
    id: "ship",
    question: "Ship?",
    options: "yes,no",
    defaultAnswer: "no",
  });
  assert.equal((await store.gateList()).length, 1);
  const answer = await store.gateResolve("ship", "yes");
  assert.equal(answer.authorizesExecution, false);
  await store.gatePark({
    id: "ship",
    question: "Again?",
    options: "yes,no",
    defaultAnswer: "no",
  });
  assert.equal((await store.gateList())[0].history.length, 2);
});
test("standing lines status deltas and derived exports retain spreadsheet safety", async (t) => {
  const { dir, store } = await setup(t);
  await store.standingAdd("Keep scope bounded");
  await store.unitAdd({ id: "=formula", track: "t" });
  assert.equal((await store.standingShow())[0].number, 1);
  assert.equal((await store.status()).changed, "first render");
  assert.equal((await store.status()).changed, "no derived changes");
  await store.exportViews();
  assert.match(await readFile(join(dir, "units.tsv"), "utf8"), /'=formula/);
  assert.equal((await store.unitGet("=formula")).id, "=formula");
  assert.match(
    await readFile(join(dir, "status.md"), "utf8"),
    /Orchestration status/,
  );
});
test("frontier generation pin and state revision reject stale writes", async (t) => {
  const { store } = await setup(t);
  const first = await store.frontierSet(graph(), [1, 2]);
  assert.equal(first.generation, 1);
  assert.deepEqual(first.eligible, [2]);
  await assert.rejects(store.frontierSet(graph(), [2, 1]), /pin mismatch/);
  await assert.rejects(
    store.frontierSet(graph(), undefined, 0),
    /revision changed/,
  );
  assert.equal((await store.frontierShow()).generation, 1);
});
test("graph closed predecessor blocks descendants rather than skipping it", () => {
  const g = validateGraph(graph(["CLOSED", "OPEN"]));
  assert.deepEqual(g.eligible, []);
  assert.equal(g.lowestUnmerged, 1);
  assert.equal(g.blocked[0].reasons[0], "u0:CLOSED");
});
test("graph rejects duplicate missing self and cyclic dependencies", () => {
  for (const mutate of [
    (g) => g.nodes.push(g.nodes[0]),
    (g) => (g.nodes[1].dependsOn = ["missing"]),
    (g) => (g.nodes[1].dependsOn = ["u1"]),
    (g) => (g.nodes[0].dependsOn = ["u1"]),
  ]) {
    const g = graph();
    mutate(g);
    assert.throws(() => validateGraph(g));
  }
});
test("DAG uses deterministic topological order and independent frontier", () => {
  const g = graph(["OPEN", "OPEN", "OPEN"]);
  g.nodes[1].dependsOn = [];
  g.nodes[2].dependsOn = ["u0", "u1"];
  assert.deepEqual(validateGraph(g).eligible, [1, 2]);
});
test("observed graph includes sibling dependencies and detects cycles and ambiguity", () => {
  const rows = [
    { number: 1, headRefName: "a", baseRefName: "main" },
    { number: 2, headRefName: "b", baseRefName: "a" },
    { number: 3, headRefName: "c", baseRefName: "a" },
  ];
  assert.deepEqual(
    discoverGraph(context(2), rows).map((p) => p.number),
    [1, 2, 3],
  );
  assert.throws(
    () =>
      discoverGraph(context(2), [
        ...rows,
        { ...rows[2], number: 4, headRefName: "b" },
      ]),
    /Ambiguous/,
  );
  assert.throws(
    () =>
      discoverGraph(context(1), [
        { number: 1, headRefName: "a", baseRefName: "b" },
        { number: 2, headRefName: "b", baseRefName: "a" },
      ]),
    /cycle/,
  );
});
test("action request is inert and bound to revision evidence", () => {
  const r = mutationRequest({
    action: "merge-pr",
    target: "owner/repo#1",
    headSha: HEAD,
    baseSha: BASE,
    generation: 2,
    evidence: ["receipt"],
  });
  assert.equal(r.authorized, false);
  assert.equal(r.executable, false);
  assert.equal(r.expected.headSha, HEAD);
  assert.throws(() => mutationRequest({ ...r, evidence: [] }));
});
test("malformed and future-version state fails closed without repair", async (t) => {
  const { dir, store } = await setup(t);
  const path = join(dir, "state.json");
  await writeFile(path, "{");
  await assert.rejects(store.unitsList(), /malformed/);
  await writeFile(path, JSON.stringify({ schemaVersion: 20 }));
  await assert.rejects(store.init(), /Unsupported/);
  assert.equal(JSON.parse(await readFile(path, "utf8")).schemaVersion, 20);
});
test("store validates duplicate rows and invalid SHA", async (t) => {
  const { store } = await setup(t);
  const s = await store.store.read();
  s.units = [{ id: "x", track: "t", state: "done", sha: "short", pr: "1" }];
  assert.throws(() => validateState(s), /full/);
});
test("same-instance concurrent mutations serialize without lost updates", async (t) => {
  const { store } = await setup(t);
  await Promise.all(
    Array.from({ length: 30 }, (_, i) =>
      store.unitAdd({ id: "u" + i, track: "t" }),
    ),
  );
  assert.equal((await store.unitsList()).length, 30);
});
test("two processes write the same store without loss", async (t) => {
  const { dir, store } = await setup(t);
  const module = fileURLToPath(
    new URL("../lib/orchestration.mjs", import.meta.url),
  );
  const launch = (n) =>
    new Promise((res, rej) => {
      const code = `import {Orchestrator} from ${JSON.stringify(pathToFile(module))};const s=new Orchestrator(${JSON.stringify(dir)});for(let i=0;i<10;i++)await s.unitAdd({id:'${n}-'+i,track:'t'});await s.close();`;
      const c = spawn(process.execPath, ["--input-type=module", "-e", code], {
        stdio: ["ignore", "pipe", "pipe"],
      });
      let error = "";
      c.stderr.on("data", (x) => (error += x));
      c.on("error", rej);
      c.on("exit", (code) => (code === 0 ? res() : rej(new Error(error))));
    });
  await Promise.all([launch("a"), launch("b")]);
  assert.equal((await store.unitsList()).length, 20);
});
const pathToFile = (p) => new URL("file://" + p).href;
test("live lock is never stolen and release checks token", async (t) => {
  const { dir } = await setup(t);
  await writeFile(
    join(dir, ".writer.lock"),
    JSON.stringify({ token: "other", pid: process.pid, host: hostname() }),
  );
  await assert.rejects(
    withLock(dir, () => {}, { waitMs: 0 }),
    /lock exists/,
  );
  await assert.rejects(recoverLock(dir, "other"), /alive/);
});
test("closed store rejects later reads and writes", async (t) => {
  const { store } = await setup(t);
  await store.close();
  await assert.rejects(store.unitsList(), /closed/);
  await assert.rejects(store.unitAdd({ id: "x", track: "t" }), /closed/);
});
test("atomic replacement preserves permissions and rejects symlink targets", async (t) => {
  const { dir } = await setup(t);
  const p = join(dir, "file");
  await writeFile(p, "old");
  await chmod(p, 0o640);
  await atomicWrite(p, "new");
  assert.equal((await stat(p)).mode & 0o777, 0o640);
  await symlink(p, join(dir, "link"));
  await assert.rejects(atomicWrite(join(dir, "link"), "bad"), /regular/);
  assert.equal(await readFile(p, "utf8"), "new");
  assert.equal(
    (await readdir(dir)).filter((n) => n.endsWith(".tmp")).length,
    0,
  );
});
