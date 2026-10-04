import { lstat, readdir } from "node:fs/promises";
import { resolve, join } from "node:path";
import { runCommand, readRunner, fail } from "./core.mjs";

export function parseWorktrees(raw) {
  const entries = [];
  let row = null;
  for (const field of raw.split("\0")) {
    if (!field) {
      if (row) {
        entries.push(row);
        row = null;
      }
      continue;
    }
    const space = field.indexOf(" "),
      key = space < 0 ? field : field.slice(0, space),
      value = space < 0 ? "" : field.slice(space + 1);
    if (key === "worktree") {
      if (row) entries.push(row);
      row = {
        path: value,
        head: null,
        branch: null,
        bare: false,
        detached: false,
        locked: false,
        prunable: false,
      };
    } else if (row) {
      if (key === "HEAD") row.head = value;
      else if (key === "branch")
        row.branch = value.replace(/^refs\/heads\//, "");
      else if (["bare", "detached", "locked", "prunable"].includes(key)) {
        row[key] = true;
        if (value) row[`${key}Reason`] = value;
      }
    }
  }
  if (row) entries.push(row);
  return entries;
}
export function parseStatus(raw) {
  const records = raw.split("\0"),
    tracked = [],
    untracked = [];
  for (let i = 0; i < records.length; i++) {
    const entry = records[i];
    if (!entry) continue;
    fail(entry.length >= 3, "Malformed git status record");
    const status = entry.slice(0, 2),
      path = entry.slice(3);
    if (status === "??") untracked.push(path);
    else {
      tracked.push({ status, path });
      if (/[RC]/.test(status)) i++;
    }
  }
  return { tracked, untracked };
}
async function sizeTree(root, { maxEntries = 100000, signal } = {}) {
  let bytes = 0,
    count = 0,
    partial = false;
  const stack = [root];
  while (stack.length) {
    if (signal?.aborted) {
      partial = true;
      break;
    }
    const path = stack.pop();
    if (++count > maxEntries) {
      partial = true;
      break;
    }
    try {
      const s = await lstat(path);
      if (s.isSymbolicLink()) continue;
      if (s.isFile()) bytes += s.size;
      else if (s.isDirectory())
        for (const name of await readdir(path)) stack.push(join(path, name));
    } catch {
      partial = true;
    }
  }
  return { bytes, partial, entries: count };
}
export async function auditWorktrees(
  repo,
  {
    runner = runCommand,
    trunk,
    active = [],
    prObservations = [],
    maxEntries = 100000,
    signal,
  } = {},
) {
  const run = readRunner(runner),
    cwd = resolve(repo ?? process.cwd());
  const git = async (args) => run("git", args, { cwd, signal });
  const result = await git(["worktree", "list", "--porcelain", "-z"]);
  fail(result.code === 0, "Cannot list worktrees", "GIT", 7);
  const entries = parseWorktrees(result.stdout);
  fail(
    Array.isArray(active) &&
      active.every(
        (a) => typeof a === "string" || (a && typeof a.path === "string"),
      ),
    "Active-worktree input must be an array of paths or path records",
  );
  fail(
    Array.isArray(prObservations) &&
      prObservations.every(
        (p) =>
          p &&
          typeof p.headRefName === "string" &&
          ["OPEN", "CLOSED", "MERGED"].includes(p.state),
      ),
    "PR observations have invalid shape",
  );
  let base = trunk ?? null;
  if (!base) {
    const r = await git([
      "symbolic-ref",
      "--quiet",
      "refs/remotes/origin/HEAD",
    ]);
    if (r.code === 0) base = r.stdout.trim();
  }
  const baseRef = base;
  if (base) {
    const resolved = await git([
      "rev-parse",
      "--verify",
      "--end-of-options",
      `${base}^{commit}`,
    ]);
    base =
      resolved.code === 0 &&
      /^(?:[a-f0-9]{40}|[a-f0-9]{64})\s*$/i.test(resolved.stdout)
        ? resolved.stdout.trim()
        : null;
  }
  const rows = [];
  for (const entry of entries) {
    const errors = [],
      usage = active.find(
        (a) =>
          (typeof a === "string" ? resolve(a) : resolve(a.path)) ===
          resolve(entry.path),
      );
    const size = await sizeTree(entry.path, { maxEntries, signal });
    let status = { tracked: [], untracked: [] },
      merged = null,
      remote = { state: entry.detached ? "detached" : "unknown" },
      ageDays = null;
    if (!entry.bare) {
      const s = await git(["-C", entry.path, "status", "--porcelain=v1", "-z"]);
      if (s.code === 0) status = parseStatus(s.stdout);
      else errors.push("status unavailable");
      const t = await git([
        "-C",
        entry.path,
        "log",
        "-1",
        "--format=%ct",
        "HEAD",
      ]);
      if (t.code === 0 && /^\d+\s*$/.test(t.stdout))
        ageDays = Math.max(
          0,
          Math.floor((Date.now() / 1000 - Number(t.stdout)) / 86400),
        );
      else errors.push("commit age unavailable");
      if (base && entry.head) {
        const a = await git([
          "-C",
          entry.path,
          "merge-base",
          "--is-ancestor",
          entry.head,
          base,
        ]);
        if (a.code === 0) merged = true;
        else if (a.code === 1) merged = false;
        else errors.push("merge ancestry unavailable");
      }
      if (entry.branch) {
        const r = await git([
          "-C",
          entry.path,
          "rev-parse",
          "--verify",
          `${entry.branch}@{upstream}`,
        ]);
        if (r.code === 0) {
          const n = await git([
            "-C",
            entry.path,
            "rev-list",
            "--left-right",
            "--count",
            `HEAD...${entry.branch}@{upstream}`,
          ]);
          const m = /^(\d+)\s+(\d+)/.exec(n.stdout);
          if (n.code === 0 && m) {
            const ahead = Number(m[1]),
              behind = Number(m[2]);
            remote = {
              state:
                ahead && behind
                  ? "diverged"
                  : ahead
                    ? "ahead"
                    : behind
                      ? "behind"
                      : "equal",
              ahead,
              behind,
              head: r.stdout.trim(),
              freshness: "local-ref-only",
            };
          } else errors.push("upstream comparison unavailable");
        } else remote = { state: "no-known-upstream", freshness: "unknown" };
      }
    }
    const prs = prObservations.filter((p) => p.headRefName === entry.branch),
      prStates = prs.map((p) => p.state);
    const reasons = [];
    if (usage) reasons.push("active");
    if (entry.locked) reasons.push("locked");
    if (entry.prunable) reasons.push("prunable");
    if (entry.bare) reasons.push("bare");
    if (errors.length || size.partial) reasons.push("inspection-incomplete");
    if (status.tracked.length) reasons.push("tracked-changes");
    if (status.untracked.length) reasons.push("untracked-data");
    if (prStates.includes("OPEN")) reasons.push("open-pr");
    if (prStates.includes("CLOSED") && !prStates.includes("MERGED"))
      reasons.push("closed-unmerged");
    if (!reasons.length) {
      if (merged === true || prStates.includes("MERGED"))
        reasons.push("merged-candidate");
      else reasons.push("review-needed");
    }
    rows.push({
      ...entry,
      size,
      ageDays,
      ...status,
      merged,
      remote,
      prs,
      active: usage ?? null,
      activityKnown: Boolean(usage),
      reasons,
      errors,
      deletionAuthorized: false,
    });
  }
  rows.sort(
    (a, b) => b.size.bytes - a.size.bytes || a.path.localeCompare(b.path),
  );
  return {
    schemaVersion: 1,
    repository: cwd,
    trunk: baseRef,
    trunkSha: base,
    remoteFreshness: "not-refreshed",
    advisoryOnly: true,
    rows,
  };
}
