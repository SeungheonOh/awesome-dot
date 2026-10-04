import test from "node:test";
import assert from "node:assert/strict";
import { mkdtemp, rm, writeFile, readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { execFileSync } from "node:child_process";
import { main } from "../dot-stack.mjs";
import { fakeReader, fakeClock, HEAD, graph } from "./support/fakes.mjs";

async function call(args, extra = {}) {
  let out = "",
    err = "";
  const code = await main(args, {
    stdout: (s) => (out += s),
    stderr: (s) => (err += s),
    clock: fakeClock(),
    ...extra,
  });
  return { code, out, err };
}
async function fixture(t) {
  const dir = await mkdtemp(join(tmpdir(), "dot-stack-cli-"));
  t.after(() => rm(dir, { recursive: true, force: true }));
  return dir;
}
test("help for every command is side-effect free without GitHub reader", async () => {
  for (const command of [
    "",
    "orch",
    "watch-pr",
    "check-plan",
    "worktree-audit",
    "log",
    "doctor",
  ]) {
    const r = fakeReader();
    const result = await call([...(command ? [command] : []), "--help"], {
      reader: r,
    });
    assert.equal(result.code, 0);
    assert.match(result.out, /Node >=22/);
    assert.deepEqual(r.calls, []);
  }
});
test("orch CLI lifecycle complete JSON and NOT-VERIFIED exit", async (t) => {
  const dir = await fixture(t);
  const cmd = (...args) => call(["orch", "--store", dir, "--json", ...args]);
  assert.equal((await cmd("init")).code, 0);
  const added = await cmd("unit", "add", "u", "--track", "build");
  assert.equal(JSON.parse(added.out).state, "pending");
  assert.equal(
    (await cmd("unit", "set", "u", "--state", "done", "--sha", HEAD)).code,
    0,
  );
  assert.equal((await cmd("unit", "get", "missing")).code, 2);
  const missing = await cmd("ledger", "check", "1", HEAD);
  assert.equal(missing.code, 2);
  assert.equal(JSON.parse(missing.out).verdict, "NOT-VERIFIED");
  assert.equal(missing.err, "");
});
test("orch CLI graph inbox gates exports and status", async (t) => {
  const dir = await fixture(t),
    input = join(dir, "graph.json");
  await writeFile(input, JSON.stringify(graph()));
  const cmd = (...args) => call(["orch", "--store", dir, ...args]);
  await cmd("init");
  assert.equal(
    (await cmd("frontier", "set", "--graph", input, "--prs", "1,2")).code,
    0,
  );
  await cmd("inbox", "push", "agent", "unit", "done");
  const drain = JSON.parse((await cmd("inbox", "drain")).out);
  assert.equal((await cmd("inbox", "ack", drain.id)).code, 0);
  await cmd(
    "gate",
    "park",
    "q",
    "--question",
    "Ship?",
    "--options",
    "yes,no",
    "--default",
    "no",
  );
  assert.match((await cmd("status")).out, /gates open: 1/);
  await cmd("gate", "resolve", "q", "--answer", "yes");
  assert.equal((await cmd("export")).code, 0);
  assert.ok(
    (await readFile(join(dir, "frontier.json"), "utf8")).includes("generation"),
  );
});
test("watch CLI rejects conflicting modes unknown flags and nonpositive intervals", async () => {
  for (const args of [
    ["--unknown"],
    ["--interval", "0"],
    ["--sweep-interval", "-1"],
    ["--timeout", "-1"],
    ["--stack", "--queued-stack"],
    ["--stack-prs", "1,2"],
    ["--queued-stack", "--stack-prs", "1,1"],
  ]) {
    const result = await call(["watch-pr", ...args], { reader: fakeReader() });
    assert.equal(result.code, 64, args.join(" "));
    assert.equal(result.out, "");
    assert.ok(result.err);
  }
});
test("watch CLI status-only bypasses queue and emits one terminal status", async () => {
  const result = await call(
    [
      "watch-pr",
      "--owner",
      "o",
      "--repo",
      "r",
      "--queued-stack",
      "--stack-prs",
      "1",
      "--status-only",
    ],
    { reader: fakeReader() },
  );
  assert.equal(result.code, 0);
  const row = JSON.parse(result.out);
  assert.equal(row.kind, "STATUS");
  assert.equal(row.mode, "queued-stack");
});
test("watch CLI hidden CI refusal is exit4 and unresolved review exit3", async () => {
  const failed = await call(
    ["watch-pr", "--owner", "o", "--repo", "r", "--pr", "1"],
    { reader: fakeReader({ rollupState: "FAILURE" }) },
  );
  assert.equal(failed.code, 4);
  const review = await call(
    ["watch-pr", "--owner", "o", "--repo", "r", "--pr", "1"],
    { reader: fakeReader({ threads: [{ id: "thread", firstComment: null }] }) },
  );
  assert.equal(review.code, 3);
});
test("doctor only reports capabilities and never installs or authenticates", async () => {
  const calls = [];
  const result = await call(["doctor"], {
    runner: async (exe, args) => {
      calls.push([exe, args]);
      return { code: 0, stdout: "version\n", stderr: "" };
    },
  });
  assert.equal(JSON.parse(result.out).installsPerformed, false);
  assert.deepEqual(calls, [
    ["git", ["--version"]],
    ["gh", ["--version"]],
  ]);
});
test("actual process entrypoint runs without third-party packages", () => {
  const output = execFileSync(
    process.execPath,
    [new URL("../dot-stack.mjs", import.meta.url).pathname, "--help"],
    { encoding: "utf8", env: { ...process.env, NODE_PATH: "" } },
  );
  assert.match(output, /dot-stack tools/);
});
