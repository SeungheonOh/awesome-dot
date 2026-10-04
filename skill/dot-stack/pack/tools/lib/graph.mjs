import { fail, record, positive, sha, nonempty } from "./core.mjs";

export function repository(value) {
  fail(
    typeof value === "string" &&
      /^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(value),
    "Repository must be OWNER/REPO",
  );
  return value;
}
export function validateGraph(input) {
  fail(
    record(input) && input.schemaVersion === 1 && Array.isArray(input.nodes),
    "Graph requires schemaVersion 1 and nodes array",
  );
  const repo = repository(input.repository),
    ids = new Set(),
    prs = new Set();
  const nodes = input.nodes.map((node) => {
    fail(record(node), "Graph node must be an object");
    const id = nonempty(node.id, "node id"),
      pr = positive(node.pr, "PR");
    fail(!ids.has(id) && !prs.has(pr), "Graph has duplicate node ID or PR");
    ids.add(id);
    prs.add(pr);
    fail(
      Array.isArray(node.dependsOn) &&
        node.dependsOn.every((d) => typeof d === "string"),
      `Node ${id} requires dependsOn array`,
    );
    fail(
      new Set(node.dependsOn).size === node.dependsOn.length,
      `Node ${id} has duplicate dependencies`,
    );
    fail(
      ["OPEN", "MERGED", "CLOSED", "UNKNOWN"].includes(node.state),
      `Node ${id} has unknown state`,
    );
    const branch = nonempty(node.branch, "branch");
    return {
      id,
      pr,
      branch,
      baseBranch: node.baseBranch ?? null,
      headSha: sha(node.headSha),
      baseSha: node.baseSha ? sha(node.baseSha) : null,
      dependsOn: [...node.dependsOn],
      state: node.state,
      repository: repo,
    };
  });
  for (const node of nodes)
    for (const dependency of node.dependsOn)
      fail(
        ids.has(dependency) && dependency !== node.id,
        `Node ${node.id} has missing/self dependency ${dependency}`,
      );
  const remaining = new Set(ids),
    ordered = [];
  while (remaining.size) {
    const ready = nodes.filter(
      (n) => remaining.has(n.id) && n.dependsOn.every((d) => !remaining.has(d)),
    );
    fail(ready.length > 0, "Dependency graph contains a cycle");
    for (const node of ready) {
      ordered.push(node);
      remaining.delete(node.id);
    }
  }
  const byId = new Map(ordered.map((n) => [n.id, n]));
  const blocked = ordered
    .filter((n) => n.state !== "MERGED")
    .map((n) => ({
      id: n.id,
      reasons: n.dependsOn
        .filter((d) => byId.get(d).state !== "MERGED")
        .map((d) => `${d}:${byId.get(d).state}`),
    }))
    .filter((n) => n.reasons.length);
  const eligible = ordered
    .filter(
      (n) =>
        n.state === "OPEN" &&
        n.dependsOn.every((d) => byId.get(d).state === "MERGED"),
    )
    .map((n) => n.pr);
  return {
    schemaVersion: 1,
    repository: repo,
    nodes: ordered,
    eligible,
    blocked,
    lowestUnmerged: ordered.find((n) => n.state !== "MERGED")?.pr ?? null,
  };
}

/** Branch-graph discovery is advisory; ambiguity and incomplete observations fail closed. */
export function discoverGraph(seed, open, { complete = true } = {}) {
  fail(complete, "Open PR observation is incomplete", "INCOMPLETE", 7);
  const numbers = new Set(),
    byHead = new Map();
  for (const pr of open) {
    positive(pr.number, "PR");
    fail(
      !Object.hasOwn(pr, "headRepository") || pr.headRepository !== null,
      "Head repository identity is unavailable",
      "AMBIGUOUS",
      7,
    );
    fail(!numbers.has(pr.number), "Duplicate observed PR", "AMBIGUOUS", 7);
    numbers.add(pr.number);
    const key = `${(pr.headRepository ?? `${seed.owner}/${seed.repo}`).toLowerCase()}:${pr.headRefName}`;
    fail(!byHead.has(key), "Ambiguous duplicate head ref", "AMBIGUOUS", 7);
    byHead.set(key, pr);
  }
  const parents = new Map(),
    children = new Map();
  for (const pr of open) {
    const parent = byHead.get(
      `${seed.owner.toLowerCase()}/${seed.repo.toLowerCase()}:${pr.baseRefName}`,
    );
    if (parent) {
      parents.set(pr.number, parent);
      children.set(parent.number, [...(children.get(parent.number) ?? []), pr]);
    }
  }
  const start = open.find((pr) => pr.number === seed.number);
  if (!start) return [seed];
  let root = start;
  const ancestry = new Set();
  while (parents.has(root.number)) {
    fail(
      !ancestry.has(root.number),
      "Observed stack contains a cycle",
      "CYCLE",
      7,
    );
    ancestry.add(root.number);
    root = parents.get(root.number);
  }
  const output = [],
    visited = new Set(),
    active = new Set();
  const visit = (pr) => {
    fail(!active.has(pr.number), "Observed stack contains a cycle", "CYCLE", 7);
    if (visited.has(pr.number)) return;
    active.add(pr.number);
    output.push({ ...seed, number: pr.number });
    visited.add(pr.number);
    for (const child of (children.get(pr.number) ?? []).sort(
      (a, b) => a.number - b.number,
    ))
      visit(child);
    active.delete(pr.number);
  };
  visit(root);
  return output;
}

export function mutationRequest({
  action,
  target,
  headSha,
  baseSha,
  generation,
  evidence,
  data = null,
}) {
  fail(
    [
      "publish-branch",
      "reply-thread",
      "retarget-pr",
      "merge-pr",
      "remove-worktree",
    ].includes(action),
    "Unsupported action request",
  );
  nonempty(target, "target");
  sha(headSha);
  if (baseSha) sha(baseSha);
  fail(
    Number.isSafeInteger(generation) &&
      generation >= 0 &&
      Array.isArray(evidence) &&
      evidence.length > 0,
    "Request requires generation and evidence",
  );
  return {
    schemaVersion: 1,
    kind: "ACTION_REQUEST",
    authorized: false,
    executable: false,
    action,
    target,
    expected: { headSha, baseSha: baseSha ?? null, generation },
    evidence,
    data,
  };
}
