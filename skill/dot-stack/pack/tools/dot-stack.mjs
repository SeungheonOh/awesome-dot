#!/usr/bin/env node
import { readFile, mkdir } from "node:fs/promises";
import { resolve, dirname } from "node:path";
import { pathToFileURL, fileURLToPath } from "node:url";
import {
  ToolError,
  fail,
  options,
  positive,
  errorObject,
  runCommand,
} from "./lib/core.mjs";
import { Orchestrator } from "./lib/orchestration.mjs";
import { atomicWrite, recoverLock } from "./lib/atomic-store.mjs";
import {
  GitHubReader,
  resolveContext,
  discoverStack,
} from "./lib/github-reader.mjs";
import { watch, renderJson, renderPretty, defaults } from "./lib/watcher.mjs";
import { checkPlan } from "./lib/plan-check.mjs";
import { auditWorktrees } from "./lib/worktree-audit.mjs";
import { appendDecision } from "./lib/decision-log.mjs";

const boolean = { type: "boolean" },
  string = { type: "string" };
export const HELP = `dot-stack tools (Node >=22, no installation side effects)

Usage: node tools/dot-stack.mjs COMMAND [OPTIONS]
  orch --store DIR init
  orch --store DIR unit add ID --track TRACK [--brief PATH]
  orch --store DIR unit set ID --state STATE [--branch B --pr N --sha SHA]
  orch --store DIR unit get ID | unit list [--state STATE --track TRACK] | unit counts
  orch --store DIR ledger record PR SHA VERDICT --evidence PATH [--verifier NAME]
  orch --store DIR ledger check PR SHA [--base-sha SHA --profile PROFILE --require-pass]
  orch --store DIR ledger summary
  orch --store DIR inbox push AGENT UNIT STATUS [--report PATH --key KEY]
  orch --store DIR inbox drain [--peek] | inbox count | inbox ack BATCH
  orch --store DIR gate park ID --question Q --options OPTIONS --default ANSWER
  orch --store DIR gate list | gate resolve ID --answer ANSWER
  orch --store DIR frontier set --graph FILE [--prs N,... --expected-revision N]
  orch --store DIR frontier show | standing show | standing add LINE
  orch --store DIR status [--read-only] | export
  orch --store DIR recover-lock --token TOKEN
  watch-pr [--owner OWNER --repo REPO --pr N] [--stack | --queued-stack]
           [--stack-prs N,...] [--status-only] [--allow-draft] [--pretty]
           [--interval SECONDS --sweep-interval SECONDS --timeout SECONDS]
           [--max-query-errors N] [--checkpoint FILE | --resume FILE] [--reviewers FILE]
  check-plan PLAN [--json] [--verify-evidence --root DIR --head SHA]
  worktree-audit [REPO] [--json --trunk REF --active FILE --prs FILE]
  log FILE PHASE DECISION WHY EVIDENCE RESULT [--run RUN_ID]
  doctor

Orch accepts --json. Store: --store, ORCH_STORE, or project .dot-stack/state/default.
Watcher: NDJSON default; status-only exits 0 for an observation, not a readiness claim.
Queued observation never merges. A gate answer is bookkeeping, not execution permission.
Worktree audit never fetches or deletes. Missing tools are reported, never installed.
`;
const readJson = async (path) => {
  try {
    return JSON.parse(await readFile(path, "utf8"));
  } catch (error) {
    throw new ToolError(`Cannot read JSON ${path}: ${error.message}`, "INPUT");
  }
};
function arity(values, count, usage) {
  fail(values.length === count, `Usage: ${usage}`, "USAGE", 64);
}
function required(v, name) {
  fail(v !== undefined, `Required option --${name}`, "USAGE", 64);
  return v;
}
function cliPositive(value, label) {
  try {
    return positive(value, label);
  } catch (error) {
    throw new ToolError(error.message, "USAGE", 64);
  }
}
function numbers(value) {
  const parts = value
    .split(",")
    .map((v) => cliPositive(v.trim().replace(/^#/, ""), "PR"));
  fail(new Set(parts).size === parts.length, "Duplicate PR", "USAGE", 64);
  return parts;
}
function numeric(value, name, allowZero = false) {
  const n = Number(value);
  fail(
    Number.isFinite(n) && (allowZero ? n >= 0 : n > 0),
    `--${name} must be ${allowZero ? "nonnegative" : "positive"}`,
    "USAGE",
    64,
  );
  return n;
}

async function orch(args, runtime) {
  const { values: v, positionals: p } = options(args, {
    store: string,
    json: boolean,
    track: string,
    brief: string,
    state: string,
    branch: string,
    pr: string,
    sha: string,
    evidence: string,
    verifier: string,
    report: string,
    key: string,
    peek: boolean,
    question: string,
    options: string,
    default: string,
    answer: string,
    graph: string,
    prs: string,
    "expected-revision": string,
    "base-sha": string,
    profile: string,
    "patch-id": string,
    "require-pass": boolean,
    "read-only": boolean,
    token: string,
  });
  const directory =
    v.store ??
    process.env.ORCH_STORE ??
    resolve(runtime.cwd ?? process.cwd(), ".dot-stack/state/default");
  if (!v.store && !process.env.ORCH_STORE)
    fail(
      resolve(runtime.cwd ?? process.cwd()) !==
        resolve(fileURLToPath(new URL("..", import.meta.url))),
      "Choose an explicit project --store; do not write state into the plugin package",
      "USAGE",
      64,
    );
  const store = new Orchestrator(directory, runtime.storeOptions);
  let result;
  const [group, sub, ...rest] = p,
    rev =
      v["expected-revision"] === undefined
        ? undefined
        : Number(v["expected-revision"]);
  const commandOptions = {
    "unit add": ["track", "brief"],
    "unit set": ["state", "branch", "pr", "sha", "expected-revision"],
    "unit list": ["state", "track"],
    "ledger record": [
      "evidence",
      "verifier",
      "base-sha",
      "profile",
      "patch-id",
    ],
    "ledger check": ["base-sha", "profile", "require-pass"],
    "inbox push": ["report", "key"],
    "inbox drain": ["peek"],
    "gate park": ["question", "options", "default"],
    "gate resolve": ["answer"],
    "frontier set": ["graph", "prs", "expected-revision"],
    status: ["read-only"],
    "recover-lock": ["token"],
  };
  const allowed = new Set([
    "store",
    "json",
    ...(commandOptions[`${group} ${sub}`] ?? commandOptions[group] ?? []),
  ]);
  for (const key of Object.keys(v))
    fail(
      allowed.has(key),
      `Option --${key} does not apply to this command`,
      "USAGE",
      64,
    );
  if (rev !== undefined)
    fail(
      Number.isSafeInteger(rev) && rev >= 0,
      "Invalid expected revision",
      "USAGE",
      64,
    );
  try {
    if (group === "init") {
      arity(p, 1, "orch init");
      result = await store.init();
    } else if (group === "status") {
      arity(p, 1, "orch status");
      result = await store.status({ readOnly: v["read-only"] ?? false });
    } else if (group === "export") {
      arity(p, 1, "orch export");
      result = await store.exportViews();
    } else if (group === "recover-lock") {
      arity(p, 1, "orch recover-lock --token TOKEN");
      result = await recoverLock(directory, required(v.token, "token"));
    } else if (group === "unit") {
      if (sub === "add") {
        arity(rest, 1, "unit add ID --track TRACK");
        result = await store.unitAdd({
          id: rest[0],
          track: required(v.track, "track"),
          brief: v.brief,
        });
      } else if (sub === "set") {
        arity(rest, 1, "unit set ID --state STATE");
        result = await store.unitSet(
          rest[0],
          {
            state: required(v.state, "state"),
            branch: v.branch,
            pr: v.pr,
            sha: v.sha,
          },
          rev,
        );
      } else if (sub === "get") {
        arity(rest, 1, "unit get ID");
        result = await store.unitGet(rest[0]);
      } else if (sub === "list") {
        arity(rest, 0, "unit list");
        result = await store.unitsList(v);
      } else if (sub === "counts") {
        arity(rest, 0, "unit counts");
        result = await store.unitCounts();
      } else throw new ToolError("Unknown unit command", "USAGE", 64);
    } else if (group === "ledger") {
      if (sub === "record") {
        arity(rest, 3, "ledger record PR SHA VERDICT --evidence PATH");
        result = await store.ledgerRecord({
          pr: rest[0],
          sha: rest[1],
          verdict: rest[2],
          evidence: required(v.evidence, "evidence"),
          verifier: v.verifier,
          baseSha: v["base-sha"],
          profile: v.profile,
          patchId: v["patch-id"],
        });
      } else if (sub === "check") {
        arity(rest, 2, "ledger check PR SHA");
        result = await store.ledgerCheck({
          pr: rest[0],
          sha: rest[1],
          baseSha: v["base-sha"],
          profile: v.profile,
          requirePass: v["require-pass"],
        });
      } else if (sub === "summary") {
        arity(rest, 0, "ledger summary");
        result = await store.ledgerSummary();
      } else throw new ToolError("Unknown ledger command", "USAGE", 64);
    } else if (group === "inbox") {
      if (sub === "push") {
        arity(rest, 3, "inbox push AGENT UNIT STATUS");
        result = await store.inboxPush({
          agent: rest[0],
          unit: rest[1],
          status: rest[2],
          report: v.report,
          idempotencyKey: v.key,
        });
      } else if (sub === "drain") {
        arity(rest, 0, "inbox drain");
        result = v.peek ? await store.inboxPeek() : await store.inboxDrain();
      } else if (sub === "count") {
        arity(rest, 0, "inbox count");
        result = { count: await store.inboxCount() };
      } else if (sub === "ack") {
        arity(rest, 1, "inbox ack BATCH");
        result = await store.inboxAck(rest[0]);
      } else throw new ToolError("Unknown inbox command", "USAGE", 64);
    } else if (group === "gate") {
      if (sub === "park") {
        arity(rest, 1, "gate park ID");
        result = await store.gatePark({
          id: rest[0],
          question: required(v.question, "question"),
          options: required(v.options, "options"),
          defaultAnswer: required(v.default, "default"),
        });
      } else if (sub === "list") {
        arity(rest, 0, "gate list");
        result = await store.gateList();
      } else if (sub === "resolve") {
        arity(rest, 1, "gate resolve ID --answer ANSWER");
        result = await store.gateResolve(rest[0], required(v.answer, "answer"));
      } else throw new ToolError("Unknown gate command", "USAGE", 64);
    } else if (group === "frontier") {
      if (sub === "show") {
        arity(rest, 0, "frontier show");
        result = await store.frontierShow();
      } else if (sub === "set") {
        arity(rest, 0, "frontier set --graph FILE");
        result = await store.frontierSet(
          await readJson(required(v.graph, "graph")),
          v.prs ? numbers(v.prs) : undefined,
          rev,
        );
      } else throw new ToolError("Unknown frontier command", "USAGE", 64);
    } else if (group === "standing") {
      if (sub === "show") {
        arity(rest, 0, "standing show");
        result = await store.standingShow();
      } else if (sub === "add") {
        arity(rest, 1, "standing add LINE");
        result = await store.standingAdd(rest[0]);
      } else throw new ToolError("Unknown standing command", "USAGE", 64);
    } else throw new ToolError("Unknown orch command", "USAGE", 64);
    if (!v.json && group === "status")
      runtime.stdout(
        `counts: units=${result.units.length}; states=${JSON.stringify(result.summary.unitStates)}; ledger=${JSON.stringify(result.summary.ledgerVerdicts)}\nchanged: ${result.changed}\ngates open: ${result.summary.openGateIds.length}\n`,
      );
    else
      runtime.stdout(
        JSON.stringify(result, v.json ? null : null, v.json ? 2 : 0) + "\n",
      );
    return 0;
  } finally {
    await store.close();
  }
}

async function watchCli(args, runtime) {
  const { values: v, positionals: p } = options(args, {
    owner: string,
    repo: string,
    pr: string,
    stack: boolean,
    "queued-stack": boolean,
    "stack-prs": string,
    interval: string,
    "sweep-interval": string,
    timeout: string,
    "max-query-errors": string,
    "status-only": boolean,
    "allow-draft": boolean,
    pretty: boolean,
    checkpoint: string,
    resume: string,
    reviewers: string,
  });
  arity(p, 0, "watch-pr [OPTIONS]");
  fail(
    !(v.stack && v["queued-stack"]),
    "--stack and --queued-stack conflict",
    "USAGE",
    64,
  );
  fail(
    !v["stack-prs"] || v["queued-stack"],
    "--stack-prs requires --queued-stack",
    "USAGE",
    64,
  );
  fail(
    !(v.resume && v.checkpoint),
    "--resume and --checkpoint conflict",
    "USAGE",
    64,
  );
  const polling = {
    ...defaults,
    interval:
      v.interval === undefined
        ? defaults.interval
        : numeric(v.interval, "interval"),
    sweepInterval:
      v["sweep-interval"] === undefined
        ? defaults.sweepInterval
        : numeric(v["sweep-interval"], "sweep-interval"),
    timeout:
      v.timeout === undefined
        ? defaults.timeout
        : numeric(v.timeout, "timeout", true),
    maxQueryErrors:
      v["max-query-errors"] === undefined
        ? defaults.maxQueryErrors
        : cliPositive(v["max-query-errors"], "max-query-errors"),
    allowDraft: v["allow-draft"] ?? false,
  };
  const reader =
    runtime.reader ??
    new GitHubReader({
      cwd: runtime.cwd,
      signal: runtime.signal,
      reviewerPolicy: v.reviewers ? await readJson(v.reviewers) : {},
    });
  let contexts,
    mode = v["queued-stack"] ? "queued-stack" : v.stack ? "stack" : "single";
  if (v.resume) {
    const saved = await readJson(v.resume);
    fail(
      saved.schemaVersion === 1 &&
        Array.isArray(saved.queue) &&
        saved.queue.length &&
        ["single", "stack", "queued-stack"].includes(saved.mode),
      "Invalid checkpoint",
    );
    fail(
      !v.pr &&
        !v.owner &&
        !v.repo &&
        !v["stack-prs"] &&
        !v.stack &&
        !v["queued-stack"],
      "Resume uses its captured context; do not combine context options",
      "USAGE",
      64,
    );
    contexts = saved.queue;
    mode = saved.mode;
    for (const c of contexts)
      await resolveContext(reader, {
        owner: c.owner,
        repo: c.repo,
        pr: c.number,
      });
  } else {
    const pin = v["stack-prs"] ? numbers(v["stack-prs"]) : null;
    const seed = await resolveContext(reader, {
      owner: v.owner,
      repo: v.repo,
      pr: v.pr ? cliPositive(v.pr.replace(/^#/, ""), "PR") : pin?.[0],
    });
    contexts = pin
      ? pin.map((number) => ({ ...seed, number }))
      : mode === "single"
        ? [seed]
        : await discoverStack(reader, seed);
  }
  const render = v.pretty ? renderPretty : renderJson;
  const checkpointPath = v.checkpoint ?? v.resume;
  const checkpoint = checkpointPath
    ? async (value) => {
        await mkdir(dirname(resolve(checkpointPath)), { recursive: true });
        await atomicWrite(
          resolve(checkpointPath),
          JSON.stringify(value, null, 2) + "\n",
        );
      }
    : null;
  const terminal = await watch({
    reader,
    contexts,
    mode,
    statusOnly: v["status-only"] ?? false,
    options: polling,
    clock: runtime.clock,
    emit: (e) => runtime.stdout(render(e)),
    signal: runtime.signal,
    checkpoint,
  });
  runtime.stdout(render(terminal));
  return terminal.exitCode;
}
export async function main(args, runtime = {}) {
  const io = {
    stdout: (value) => process.stdout.write(value),
    stderr: (value) => process.stderr.write(value),
    ...runtime,
  };
  if (!args.length || args.includes("--help") || args.includes("-h")) {
    io.stdout(HELP);
    return 0;
  }
  const [command, ...rest] = args;
  try {
    if (command === "orch") return await orch(rest, io);
    if (command === "watch-pr") return await watchCli(rest, io);
    if (command === "check-plan") {
      const { values: v, positionals: p } = options(rest, {
        json: boolean,
        "verify-evidence": boolean,
        root: string,
        head: string,
      });
      arity(p, 1, "check-plan PLAN");
      const r = await checkPlan(p[0], {
        verifyEvidence: v["verify-evidence"],
        root: v.root,
        head: v.head,
      });
      if (v.json) io.stdout(JSON.stringify(r, null, 2) + "\n");
      else {
        for (const u of r.units) io.stdout(`${u.id} boxes=${u.boxes}\n`);
        io.stdout(`${r.units.length} units, ${r.problems.length} problems\n`);
        for (const problem of r.problems)
          io.stderr(
            `${p[0]}:${problem.line}: ${problem.code}: ${problem.message}\n`,
          );
      }
      return r.valid ? 0 : 1;
    }
    if (command === "worktree-audit") {
      const { values: v, positionals: p } = options(rest, {
        json: boolean,
        trunk: string,
        active: string,
        prs: string,
      });
      fail(p.length <= 1, "Usage: worktree-audit [REPO]", "USAGE", 64);
      const r = await auditWorktrees(p[0] ?? io.cwd, {
        runner: io.runner,
        trunk: v.trunk,
        active: v.active ? await readJson(v.active) : [],
        prObservations: v.prs ? await readJson(v.prs) : [],
        signal: io.signal,
      });
      io.stdout(JSON.stringify(r, null, 2) + "\n");
      return 0;
    }
    if (command === "log") {
      const { values: v, positionals: p } = options(rest, { run: string });
      arity(p, 6, "log FILE PHASE DECISION WHY EVIDENCE RESULT");
      const r = await appendDecision(p[0], p.slice(1), { run: v.run });
      io.stdout(JSON.stringify(r) + "\n");
      return 0;
    }
    if (command === "doctor") {
      arity(rest, 0, "doctor");
      const capabilities = { node: process.version };
      for (const exe of ["git", "gh"])
        try {
          const r = await (io.runner ?? runCommand)(exe, ["--version"], {
            timeoutMs: 5000,
          });
          capabilities[exe] =
            r.code === 0 ? r.stdout.split("\n")[0] : "unavailable";
        } catch {
          capabilities[exe] = "unavailable";
        }
      io.stdout(
        JSON.stringify(
          {
            schemaVersion: 1,
            capabilities,
            installsPerformed: false,
            authenticationChecked: false,
          },
          null,
          2,
        ) + "\n",
      );
      return 0;
    }
    throw new ToolError(`Unknown command ${command}`, "USAGE", 64);
  } catch (error) {
    if (command === "watch-pr" && error.exitCode === 7)
      io.stdout(
        JSON.stringify({
          schemaVersion: 2,
          sequence: 1,
          observedAt: new Date().toISOString(),
          mode: "single",
          kind: "BLOCKER",
          terminal: true,
          exitCode: 7,
          blocker: { kind: "status-query", failure: errorObject(error) },
        }) + "\n",
      );
    else if (command === "orch" && error.code === "NOT_VERIFIED")
      io.stdout(
        rest.includes("--json")
          ? JSON.stringify(error.detail) + "\n"
          : "NOT-VERIFIED\n",
      );
    else
      io.stderr(
        JSON.stringify({ ok: false, error: errorObject(error) }) + "\n",
      );
    return error.exitCode ?? 1;
  }
}
if (
  process.argv[1] &&
  import.meta.url === pathToFileURL(resolve(process.argv[1])).href
) {
  const abort = new AbortController();
  process.once("SIGINT", () => abort.abort());
  process.once("SIGTERM", () => abort.abort());
  process.exitCode = await main(process.argv.slice(2), {
    signal: abort.signal,
  });
}
