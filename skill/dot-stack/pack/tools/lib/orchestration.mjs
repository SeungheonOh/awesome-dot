import { randomUUID } from "node:crypto";
import { join } from "node:path";
import { JsonStore, atomicWrite } from "./atomic-store.mjs";
import {
  ToolError,
  fail,
  record,
  nonempty,
  positive,
  sha,
  cell,
  markdown,
} from "./core.mjs";
import { validateGraph } from "./graph.mjs";

export const VERDICTS = [
  "live-ui-verified",
  "unit-test-verified",
  "type-check-only",
  "behavior-verified",
  "docs-verified",
  "verifier-blocked",
  "verifier-failed",
];
const STATES = ["pending", "claimed", "delivered"];
const initial = (now) => ({
  schemaVersion: 1,
  revision: 0,
  createdAt: now,
  updatedAt: now,
  units: [],
  ledger: [],
  inbox: [],
  batches: [],
  gates: [],
  standing: [],
  frontier: {
    generation: 0,
    nodes: [],
    eligible: [],
    blocked: [],
    lowestUnmerged: null,
  },
  statusSummary: null,
});
const unique = (rows, key, label) =>
  fail(
    new Set(rows.map(key)).size === rows.length,
    `Duplicate ${label}`,
    "CORRUPT",
  );
export function validateState(s) {
  fail(
    record(s) &&
      s.schemaVersion === 1 &&
      Number.isSafeInteger(s.revision) &&
      s.revision >= 0,
    "Unsupported or corrupt state schema",
    "CORRUPT",
  );
  for (const name of [
    "units",
    "ledger",
    "inbox",
    "batches",
    "gates",
    "standing",
  ])
    fail(Array.isArray(s[name]), `Invalid ${name}`, "CORRUPT");
  fail(
    typeof s.createdAt === "string" && typeof s.updatedAt === "string",
    "Missing state timestamp",
    "CORRUPT",
  );
  for (const u of s.units) {
    fail(record(u), "Invalid unit");
    for (const f of ["id", "track", "state"]) nonempty(u[f], f);
    if (u.pr !== "") positive(u.pr);
    if (u.sha !== "") sha(u.sha);
  }
  unique(s.units, (u) => u.id, "unit");
  for (const e of s.ledger) {
    positive(e.pr);
    sha(e.sha);
    fail(VERDICTS.includes(e.verdict), "Invalid evidence verdict", "CORRUPT");
    nonempty(e.evidence, "evidence");
    nonempty(e.id, "evidence ID");
    if (e.baseSha) sha(e.baseSha);
  }
  unique(s.ledger, (e) => e.id, "evidence ID");
  for (const e of s.inbox) {
    nonempty(e.id, "event ID");
    fail(STATES.includes(e.delivery), "Invalid event delivery", "CORRUPT");
    for (const f of ["agent", "unit", "status"]) nonempty(e[f], f);
  }
  unique(s.inbox, (e) => e.id, "event ID");
  unique(s.batches, (b) => b.id, "batch ID");
  for (const b of s.batches)
    fail(
      record(b) &&
        Array.isArray(b.ids) &&
        b.ids.every((id) => s.inbox.some((e) => e.id === id)) &&
        ["claimed", "delivered"].includes(b.state),
      "Invalid inbox batch",
      "CORRUPT",
    );
  for (const g of s.gates) {
    nonempty(g.id, "gate ID");
    fail(
      ["open", "resolved"].includes(g.kind) && Array.isArray(g.history),
      "Invalid gate",
      "CORRUPT",
    );
  }
  unique(s.gates, (g) => g.id, "gate ID");
  for (const line of s.standing) nonempty(line, "standing line");
  fail(
    record(s.frontier) &&
      Number.isSafeInteger(s.frontier.generation) &&
      s.frontier.generation >= 0,
    "Invalid frontier generation",
    "CORRUPT",
  );
  if (s.frontier.generation > 0) validateGraph(s.frontier);
}
const counts = (values) =>
  Object.fromEntries(
    [...new Set(values)]
      .sort()
      .map((v) => [v, values.filter((x) => x === v).length]),
  );
const currentLedger = (rows) => {
  const m = new Map();
  for (const row of rows) {
    const normalized = {
      ...row,
      sha: sha(row.sha),
      baseSha: row.baseSha ? sha(row.baseSha) : null,
    };
    m.set(`${row.pr}:${normalized.sha}`, normalized);
  }
  return [...m.values()];
};
const requiredUnit = (s, id) => {
  const u = s.units.find((u) => u.id === id);
  if (!u) throw new ToolError(`Unit ${id} not found`, "NOT_FOUND", 2);
  return u;
};
export class Orchestrator {
  constructor(
    directory,
    {
      now = () => new Date().toISOString(),
      id = randomUUID,
      lockWaitMs = 5000,
    } = {},
  ) {
    this.store = new JsonStore(directory, validateState, initial, {
      now,
      lockWaitMs,
    });
    this.now = now;
    this.id = id;
  }
  init() {
    return this.store.init();
  }
  close() {
    return this.store.close();
  }
  async unitsList({ state, track } = {}) {
    return (await this.store.read()).units.filter(
      (u) => (!state || u.state === state) && (!track || u.track === track),
    );
  }
  async unitGet(id) {
    return requiredUnit(await this.store.read(), id);
  }
  async unitCounts() {
    return counts((await this.unitsList()).map((u) => u.state));
  }
  unitAdd({ id, track, brief = "" }) {
    nonempty(id, "unit ID");
    nonempty(track, "track");
    return this.store.transact((s) => {
      fail(!s.units.some((u) => u.id === id), `Unit ${id} already exists`);
      const u = {
        id,
        track,
        state: "pending",
        branch: "",
        pr: "",
        sha: "",
        brief,
      };
      s.units.push(u);
      return u;
    });
  }
  unitSet(id, { state, branch, pr, sha: head }, revision) {
    nonempty(id, "unit ID");
    nonempty(state, "state");
    if (pr !== undefined) positive(pr);
    if (head !== undefined) sha(head);
    return this.store.transact((s) => {
      const u = requiredUnit(s, id);
      u.state = state;
      if (branch !== undefined) u.branch = nonempty(branch, "branch");
      if (pr !== undefined) u.pr = String(pr);
      if (head !== undefined) u.sha = head;
      return u;
    }, revision);
  }
  ledgerRecord({
    pr,
    sha: head,
    verdict,
    evidence,
    verifier = "",
    baseSha = null,
    profile = null,
    patchId = null,
  }) {
    positive(pr);
    head = sha(head);
    if (baseSha) baseSha = sha(baseSha);
    fail(VERDICTS.includes(verdict), `Verdict must be ${VERDICTS.join(", ")}`);
    nonempty(evidence, "evidence");
    return this.store.transact((s) => {
      const prior = currentLedger(s.ledger).find(
        (e) => e.pr === String(pr) && e.sha === head,
      );
      const row = {
        id: this.id(),
        pr: String(pr),
        sha: head,
        verdict,
        evidence,
        verifier,
        ts: this.now(),
        baseSha,
        profile,
        patchId,
        supersedes: prior?.id ?? null,
      };
      s.ledger.push(row);
      return row;
    });
  }
  async ledgerCheck({ pr, sha: head, baseSha, profile, requirePass = false }) {
    positive(pr);
    head = sha(head);
    if (baseSha) baseSha = sha(baseSha);
    const row = currentLedger((await this.store.read()).ledger).find(
      (e) => e.pr === String(pr) && e.sha === head,
    );
    if (
      !row ||
      (baseSha && baseSha !== row.baseSha) ||
      (profile && profile !== row.profile) ||
      (requirePass &&
        ["verifier-blocked", "verifier-failed", "type-check-only"].includes(
          row.verdict,
        ))
    )
      throw new ToolError("NOT-VERIFIED", "NOT_VERIFIED", 2, {
        pr: String(pr),
        sha: head,
        verdict: "NOT-VERIFIED",
      });
    return row;
  }
  async ledgerSummary() {
    return counts(
      currentLedger((await this.store.read()).ledger).map((e) => e.verdict),
    );
  }
  inboxPush({ agent, unit, status, report = "", idempotencyKey = null }) {
    [agent, unit, status].forEach((v, i) =>
      nonempty(v, ["agent", "unit", "status"][i]),
    );
    return this.store.transact((s) => {
      const prior =
        idempotencyKey &&
        s.inbox.find((e) => e.idempotencyKey === idempotencyKey);
      if (prior) {
        fail(
          prior.agent === agent &&
            prior.unit === unit &&
            prior.status === status &&
            prior.report === report,
          "Idempotency key reused for different data",
        );
        return prior;
      }
      const e = {
        id: this.id(),
        ts: this.now(),
        agent,
        unit,
        status,
        report,
        idempotencyKey,
        delivery: "pending",
      };
      s.inbox.push(e);
      return e;
    });
  }
  async inboxPeek() {
    return (await this.store.read()).inbox.filter(
      (e) => e.delivery !== "delivered",
    );
  }
  async inboxCount() {
    return (await this.inboxPeek()).length;
  }
  inboxDrain() {
    return this.store.transact((s) => {
      const old = s.batches.find((b) => b.state === "claimed");
      if (old)
        return {
          ...old,
          replay: true,
          pointers: s.inbox.filter((e) => old.ids.includes(e.id)),
        };
      const pending = s.inbox.filter((e) => e.delivery === "pending");
      if (!pending.length)
        return {
          id: null,
          ids: [],
          pointers: [],
          state: "empty",
          replay: false,
        };
      const batch = {
        id: this.id(),
        ids: pending.map((e) => e.id),
        state: "claimed",
        ts: this.now(),
      };
      s.batches.push(batch);
      for (const e of pending) e.delivery = "claimed";
      return { ...batch, pointers: pending, replay: false };
    });
  }
  inboxAck(id) {
    return this.store.transact((s) => {
      const b = s.batches.find((b) => b.id === id);
      if (!b) throw new ToolError("Batch not found", "NOT_FOUND", 2);
      b.state = "delivered";
      for (const e of s.inbox.filter((e) => b.ids.includes(e.id)))
        e.delivery = "delivered";
      return b;
    });
  }
  gatePark({ id, question, options, defaultAnswer }) {
    for (const [label, v] of Object.entries({
      id,
      question,
      options,
      defaultAnswer,
    }))
      nonempty(v, label);
    return this.store.transact((s) => {
      const old = s.gates.find((g) => g.id === id);
      const next = {
        id,
        kind: "open",
        question,
        options,
        defaultAnswer,
        history: old ? [...old.history, { ...old, history: undefined }] : [],
      };
      if (old) s.gates[s.gates.indexOf(old)] = next;
      else s.gates.push(next);
      return next;
    });
  }
  async gateList() {
    return (await this.store.read()).gates.filter((g) => g.kind === "open");
  }
  gateResolve(id, answer) {
    nonempty(answer, "answer");
    return this.store.transact((s) => {
      const g = s.gates.find((g) => g.id === id);
      if (!g) throw new ToolError("Gate not found", "NOT_FOUND", 2);
      g.history.push({
        kind: g.kind,
        answer: g.answer ?? null,
        ts: this.now(),
      });
      g.kind = "resolved";
      g.answer = answer;
      return { ...g, authorizesExecution: false };
    });
  }
  async standingShow() {
    return (await this.store.read()).standing.map((line, i) => ({
      number: i + 1,
      line,
    }));
  }
  standingAdd(line) {
    nonempty(line, "standing line");
    return this.store.transact((s) => {
      s.standing.push(line);
      return { number: s.standing.length, line };
    });
  }
  async frontierShow() {
    return (await this.store.read()).frontier;
  }
  async frontierSet(graph, pin, expectedRevision) {
    const valid = validateGraph(graph);
    if (pin) {
      fail(new Set(pin).size === pin.length, "PR pin contains duplicates");
      fail(
        JSON.stringify(pin) === JSON.stringify(valid.nodes.map((n) => n.pr)),
        "Frontier pin mismatch: membership or dependency order changed",
        "STALE",
      );
    }
    return this.store.transact((s) => {
      s.frontier = {
        ...valid,
        generation: s.frontier.generation + 1,
        observedAt: this.now(),
      };
      return s.frontier;
    }, expectedRevision);
  }
  async status({ readOnly = false } = {}) {
    const render = (s) => {
      const ledger = currentLedger(s.ledger),
        summary = {
          unitStates: counts(s.units.map((u) => u.state)),
          ledgerVerdicts: counts(ledger.map((e) => e.verdict)),
          frontierGeneration: s.frontier.generation,
          openGateIds: s.gates
            .filter((g) => g.kind === "open")
            .map((g) => g.id)
            .sort(),
        };
      const before = s.statusSummary;
      const changed = !before
        ? "first render"
        : JSON.stringify(before) === JSON.stringify(summary)
          ? "no derived changes"
          : Object.keys(summary)
              .filter(
                (k) => JSON.stringify(before[k]) !== JSON.stringify(summary[k]),
              )
              .join(", ");
      const report = {
        revision: s.revision + (readOnly ? 0 : 1),
        units: s.units,
        ledger,
        frontier: s.frontier,
        gates: s.gates,
        summary,
        changed,
      };
      if (!readOnly) s.statusSummary = summary;
      return report;
    };
    const report = readOnly
      ? render(await this.store.read())
      : await this.store.transact(render, undefined, {
          afterCommit: (report) =>
            atomicWrite(
              join(this.store.directory, "status.md"),
              renderStatus(report),
            ),
        });
    return report;
  }
  async exportViews() {
    return this.store.withSnapshot(async (s) => {
      const tsv = (header, rows) =>
        `${header.join("\t")}\n${rows.map((r) => r.map(cell).join("\t")).join("\n")}${rows.length ? "\n" : ""}`;
      const units = ["id", "track", "state", "branch", "pr", "sha", "brief"],
        ledger = ["pr", "sha", "verdict", "evidence", "verifier", "ts"];
      await atomicWrite(
        join(this.store.directory, "units.tsv"),
        tsv(
          units,
          s.units.map((u) => units.map((k) => u[k])),
        ),
      );
      await atomicWrite(
        join(this.store.directory, "ledger.tsv"),
        tsv(
          ledger,
          currentLedger(s.ledger).map((e) => ledger.map((k) => e[k])),
        ),
      );
      await atomicWrite(
        join(this.store.directory, "frontier.json"),
        JSON.stringify({ ...s.frontier, stateRevision: s.revision }, null, 2) +
          "\n",
      );
      await atomicWrite(
        join(this.store.directory, "preferences.md"),
        s.standing.map((l, i) => `${i + 1}. ${l}`).join("\n") + "\n",
      );
      await atomicWrite(
        join(this.store.directory, "gates.md"),
        s.gates
          .map(
            (g) =>
              `## ${markdown(g.id)}\n\n- Status: ${g.kind}\n- Question: ${markdown(g.question)}\n- Options: ${markdown(g.options)}\n- Default (not consent): ${markdown(g.defaultAnswer)}\n${g.kind === "resolved" ? `- Answer: ${markdown(g.answer)}\n` : ""}`,
          )
          .join("\n"),
      );
      await atomicWrite(
        join(this.store.directory, "exports.json"),
        JSON.stringify(
          { schemaVersion: 1, stateRevision: s.revision, derived: true },
          null,
          2,
        ) + "\n",
      );
      return { revision: s.revision, derived: true };
    });
  }
}
export function renderStatus(r) {
  const table = (headers, rows) =>
    rows.length
      ? [
          `| ${headers.join(" | ")} |`,
          `| ${headers.map(() => "---").join(" | ")} |`,
          ...rows.map((row) => `| ${row.map(markdown).join(" | ")} |`),
        ].join("\n")
      : "(none)";
  return `# Orchestration status\n\nState revision: ${r.revision}\n\nChanged: ${r.changed}\n\n## Units\n\n${table(
    ["ID", "Track", "State", "Branch", "PR", "SHA", "Brief"],
    r.units.map((u) => [
      u.id,
      u.track,
      u.state,
      u.branch,
      u.pr,
      u.sha,
      u.brief,
    ]),
  )}\n\n## Verification ledger\n\n${table(
    ["PR", "SHA", "Verdict", "Evidence", "Verifier"],
    r.ledger.map((e) => [e.pr, e.sha, e.verdict, e.evidence, e.verifier]),
  )}\n\n## Frontier\n\nGeneration: ${r.frontier.generation}\nEligible: ${(r.frontier.eligible ?? []).join(", ") || "none"}\nLowest unmerged: ${r.frontier.lowestUnmerged ?? "none"}\n\n## Gates\n\n${table(
    ["ID", "State", "Question", "Answer"],
    r.gates.map((g) => [g.id, g.kind, g.question, g.answer ?? ""]),
  )}\n`;
}
