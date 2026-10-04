import {
  ToolError,
  fail,
  record,
  positive,
  sha,
  redact,
  runCommand,
  readRunner,
} from "./core.mjs";
import { discoverGraph, repository } from "./graph.mjs";

export class QueryError extends ToolError {
  constructor(kind, detail, retryable = true) {
    super(detail, kind, 7);
    this.failure = { kind, detail, retryable };
  }
}
const missing = (path) => {
  throw new QueryError("invalid-response", `Missing or invalid ${path}`);
};
const obj = (v, p) => (record(v) ? v : missing(p));
const arr = (v, p) => (Array.isArray(v) ? v : missing(p));
const str = (v, p) => (typeof v === "string" ? v : missing(p));
const bool = (v, p) => (typeof v === "boolean" ? v : missing(p));
const enumeration = (v, values, p) => (values.includes(v) ? v : missing(p));
const at = (v, keys) => keys.reduce((o, k) => obj(o, keys.join("."))[k], v);
const commitIdentity = (value, path) => {
  try {
    return sha(value);
  } catch {
    return missing(path);
  }
};
export function parseRepositoryRemote(value) {
  let url = value
    .trim()
    .replace(/^git@github\.com:/, "https://github.com/")
    .replace(/^ssh:\/\/git@github\.com\//, "https://github.com/");
  try {
    const u = new URL(url);
    const parts = u.pathname
      .replace(/\.git$/, "")
      .split("/")
      .filter(Boolean);
    if (
      u.protocol !== "https:" ||
      u.hostname !== "github.com" ||
      u.port ||
      u.username ||
      u.password ||
      u.search ||
      u.hash ||
      parts.length !== 2
    )
      return null;
    repository(parts.join("/"));
    return { owner: parts[0], repo: parts[1] };
  } catch {
    return null;
  }
}
export function parsePrUrl(value) {
  try {
    const u = new URL(value),
      p = u.pathname.split("/").filter(Boolean);
    fail(
      u.protocol === "https:" &&
        u.hostname === "github.com" &&
        !u.username &&
        !u.password &&
        !u.port &&
        !u.search &&
        !u.hash &&
        p.length === 4 &&
        p[2] === "pull",
      "Invalid PR URL",
    );
    repository(`${p[0]}/${p[1]}`);
    return { owner: p[0], repo: p[1], number: positive(p[3]) };
  } catch {
    throw new QueryError(
      "invalid-context",
      "Expected a canonical https://github.com/OWNER/REPO/pull/NUMBER URL",
      false,
    );
  }
}
export function parsePullRequest(v, context) {
  const p = obj(v, "pull request");
  return {
    context,
    state: enumeration(p.state, ["OPEN", "CLOSED", "MERGED"], "state"),
    isDraft: bool(p.isDraft, "isDraft"),
    mergeable: enumeration(
      p.mergeable,
      ["MERGEABLE", "CONFLICTING", "UNKNOWN"],
      "mergeable",
    ),
    mergeStateStatus: enumeration(
      p.mergeStateStatus,
      [
        "CLEAN",
        "BLOCKED",
        "BEHIND",
        "DIRTY",
        "CONFLICTING",
        "DRAFT",
        "HAS_HOOKS",
        "UNKNOWN",
        "UNSTABLE",
      ],
      "mergeStateStatus",
    ),
    reviewDecision:
      p.reviewDecision === "" || p.reviewDecision === null
        ? null
        : enumeration(
            p.reviewDecision,
            ["APPROVED", "CHANGES_REQUESTED", "REVIEW_REQUIRED"],
            "reviewDecision",
          ),
    headRefOid: commitIdentity(p.headRefOid, "remote head"),
    baseRefOid: commitIdentity(p.baseRefOid, "remote base"),
    headRefName: str(p.headRefName, "headRefName"),
    baseRefName: str(p.baseRefName, "baseRefName"),
    mergedAt: p.mergedAt === null ? null : str(p.mergedAt, "mergedAt"),
  };
}
export function parseCheck(v, source = "rollup") {
  const p = obj(v, "check");
  let name, state, kind, link;
  if (source === "fast") {
    name = str(p.name, "check.name");
    state = str(p.state, "check.state").toUpperCase();
    link = typeof p.link === "string" ? p.link : "";
    const bucket = str(p.bucket, "check.bucket");
    kind =
      bucket === "fail" ||
      [
        "FAILURE",
        "ERROR",
        "ACTION_REQUIRED",
        "CANCELLED",
        "TIMED_OUT",
      ].includes(state)
        ? "failed"
        : bucket === "pending"
          ? "pending"
          : bucket === "pass"
            ? "passed"
            : bucket === "skipping"
              ? "skipped"
              : "unknown";
  } else if (p.__typename === "CheckRun") {
    name = str(p.name, "check.name");
    link = typeof p.detailsUrl === "string" ? p.detailsUrl : "";
    const status = str(p.status, "check.status").toUpperCase();
    state = typeof p.conclusion === "string" ? p.conclusion.toUpperCase() : "";
    if (
      ["QUEUED", "IN_PROGRESS", "WAITING", "REQUESTED", "PENDING"].includes(
        status,
      )
    ) {
      kind = "pending";
      state = status;
    } else if (status !== "COMPLETED") kind = "unknown";
    else
      kind =
        state === "SUCCESS"
          ? "passed"
          : ["NEUTRAL", "SKIPPED"].includes(state)
            ? "skipped"
            : [
                  "FAILURE",
                  "CANCELLED",
                  "TIMED_OUT",
                  "ACTION_REQUIRED",
                  "STARTUP_FAILURE",
                  "STALE",
                  "ERROR",
                ].includes(state)
              ? "failed"
              : "unknown";
  } else if (p.__typename === "StatusContext") {
    name = str(p.context, "check.context");
    state = str(p.state, "check.state").toUpperCase();
    link = typeof p.targetUrl === "string" ? p.targetUrl : "";
    kind =
      state === "SUCCESS"
        ? "passed"
        : ["PENDING", "EXPECTED"].includes(state)
          ? "pending"
          : ["ERROR", "FAILURE"].includes(state)
            ? "failed"
            : "unknown";
  } else
    return {
      kind: "unknown",
      name: "unknown-check-type",
      reportedState: String(p.__typename ?? "missing"),
      link: "",
      description: "Unrecognized check node",
      workflow: "",
    };
  return {
    kind,
    name,
    reportedState: state,
    link,
    description: typeof p.description === "string" ? p.description : "",
    workflow: typeof p.workflow === "string" ? p.workflow : "",
    id: p.id ?? `${name}:${link}`,
  };
}
export function parseThread(v) {
  const t = obj(v, "review thread");
  bool(t.isResolved, "thread.isResolved");
  const comments = arr(at(t, ["comments", "nodes"]), "comments.nodes");
  const first =
    comments[0] === undefined ? null : obj(comments[0], "first comment");
  return {
    id: str(t.id, "thread.id"),
    resolved: t.isResolved,
    firstComment:
      first === null
        ? null
        : {
            body: str(first.body, "comment.body"),
            authorLogin:
              first.author === null
                ? null
                : str(obj(first.author, "author").login, "author.login"),
            path: first.path === null ? null : str(first.path, "path"),
            line:
              first.line === null
                ? null
                : Number.isSafeInteger(first.line)
                  ? first.line
                  : missing("line"),
            createdAt: str(first.createdAt, "createdAt"),
          },
    automation: null,
  };
}
export function annotateReviewThreads(threads, policy = {}) {
  const authors = policy.automationAuthors ?? [];
  const markers = policy.runIdMarkers ?? [];
  fail(
    Array.isArray(authors) &&
      authors.every((a) => typeof a === "string" && a.length > 0),
    "Invalid review automation authors",
  );
  fail(
    Array.isArray(markers) &&
      markers.every((m) => typeof m === "string" && m.length > 0),
    "Invalid review run markers",
  );
  const observedRuns = new Set();
  let hasUnidentifiedRun = false;
  const annotated = threads.map((thread) => {
    const first = thread.firstComment;
    if (
      !first ||
      !authors.some((a) => a.toLowerCase() === first.authorLogin?.toLowerCase())
    )
      return thread;
    let runId = null;
    for (const marker of markers) {
      const start = first.body.indexOf(marker);
      if (start >= 0) {
        const candidate = /^[A-Za-z0-9_.:-]+/.exec(
          first.body.slice(start + marker.length).trimStart(),
        );
        if (candidate) {
          runId = candidate[0];
          break;
        }
      }
    }
    if (runId) observedRuns.add(runId);
    else hasUnidentifiedRun = true;
    return { ...thread, automation: { author: first.authorLogin, runId } };
  });
  const observedReviewPasses =
    observedRuns.size || (hasUnidentifiedRun ? 1 : 0);
  return annotated
    .filter((thread) => !thread.resolved)
    .map((thread) => ({ ...thread, observedReviewPasses }));
}
export async function paginate(fetchPage, { maxPages = 1000 } = {}) {
  const rows = [],
    seen = new Set();
  let pageToken = null;
  for (let page = 0; page < maxPages; page++) {
    const result = await fetchPage(pageToken);
    arr(result.nodes, "page nodes");
    rows.push(...result.nodes);
    bool(result.hasNextPage, "hasNextPage");
    if (!result.hasNextPage) return rows;
    fail(
      typeof result.endCursor === "string" &&
        result.endCursor &&
        !seen.has(result.endCursor),
      "Pagination pageToken missing or repeated",
      "INCOMPLETE",
      7,
    );
    seen.add(result.endCursor);
    pageToken = result.endCursor;
  }
  throw new QueryError(
    "incomplete-pagination",
    "Pagination safety limit reached",
    false,
  );
}
const contextArgs = (c) => [
  "-f",
  `owner=${c.owner}`,
  "-f",
  `repo=${c.repo}`,
  "-F",
  `pr=${c.number}`,
];
const pageInfo = "pageInfo { hasNextPage endCursor }";
export class GitHubReader {
  constructor({
    runner = runCommand,
    cwd = process.cwd(),
    signal,
    timeoutMs = 30000,
    reviewerPolicy = {},
  } = {}) {
    this.run = readRunner(runner);
    this.cwd = cwd;
    this.signal = signal;
    this.timeoutMs = timeoutMs;
    this.reviewerPolicy = reviewerPolicy;
  }
  setDeadline(remainingMs) {
    this.remainingMs = remainingMs;
  }
  async command(exe, args) {
    let result;
    const remaining = this.remainingMs?.() ?? Infinity;
    if (remaining <= 0)
      throw new QueryError("deadline", "Observation deadline reached");
    try {
      result = await this.run(exe, args, {
        cwd: this.cwd,
        signal: this.signal,
        timeoutMs: Math.min(this.timeoutMs, remaining),
      });
    } catch (error) {
      if (error.code === "CANCELLED") throw error;
      throw new QueryError(
        error.code ?? "command",
        redact(error.message),
        error.code !== "MISSING_TOOL",
      );
    }
    return result;
  }
  async json(args) {
    const r = await this.command("gh", args);
    if (r.code !== 0)
      throw new QueryError(
        "command-exit",
        `GitHub read failed (${r.code}): ${redact(r.stderr)}`,
        !/(not logged|authentication|bad credentials|resource not accessible|could not resolve)/i.test(
          r.stderr,
        ),
      );
    let value;
    try {
      value = JSON.parse(r.stdout);
    } catch {
      throw new QueryError("json-parse", "GitHub returned invalid JSON");
    }
    if (record(value) && Array.isArray(value.errors) && value.errors.length)
      throw new QueryError(
        "graphql-error",
        "GitHub GraphQL response contains errors",
      );
    return value;
  }
  async graphql(query, c, fields = []) {
    return this.json([
      "api",
      "graphql",
      "-f",
      `query=${query}`,
      ...contextArgs(c),
      ...fields,
    ]);
  }
  async originRepo() {
    const r = await this.command("git", ["remote", "get-url", "origin"]);
    return r.code === 0 ? parseRepositoryRemote(r.stdout) : null;
  }
  async currentPr(number = null) {
    const v = obj(
      await this.json([
        "pr",
        "view",
        ...(number ? [String(number)] : []),
        "--json",
        "number,url",
      ]),
      "current PR",
    );
    const c = parsePrUrl(str(v.url, "PR URL"));
    fail(
      !number || c.number === number,
      "PR context mismatch",
      "INVALID_CONTEXT",
      7,
    );
    return c;
  }
  async pullRequest(c) {
    return parsePullRequest(
      await this.json([
        "pr",
        "view",
        String(c.number),
        "--repo",
        `${c.owner}/${c.repo}`,
        "--json",
        "state,isDraft,mergeable,mergeStateStatus,reviewDecision,headRefOid,baseRefOid,headRefName,baseRefName,mergedAt",
      ]),
      c,
    );
  }
  async openPullRequests(c) {
    const query = `query OpenPullRequests($owner:String!,$repo:String!,$after:String){repository(owner:$owner,name:$repo){pullRequests(first:100,states:OPEN,after:$after){${pageInfo} nodes{number headRefName baseRefName headRepository{nameWithOwner}}}}}`;
    const rows = await paginate(async (pageToken) => {
      const value = await this.graphql(
        query,
        c,
        pageToken ? ["-f", `after=${pageToken}`] : [],
      );
      const p = obj(
        at(value, ["data", "repository", "pullRequests"]),
        "pullRequests",
      );
      return {
        nodes: arr(p.nodes, "pullRequests.nodes"),
        ...obj(p.pageInfo, "pageInfo"),
      };
    });
    return rows.map((v) => {
      const p = obj(v, "open PR");
      return {
        number: positive(p.number),
        headRefName: str(p.headRefName, "headRefName"),
        baseRefName: str(p.baseRefName, "baseRefName"),
        headRepository:
          p.headRepository === null
            ? null
            : str(
                obj(p.headRepository, "headRepository").nameWithOwner,
                "nameWithOwner",
              ),
      };
    });
  }
  async checksFastPath(c, head) {
    // This PR fast path is diagnostic; the separate commit query supplies authoritative binding.
    const r = await this.command("gh", [
      "pr",
      "checks",
      String(c.number),
      "--repo",
      `${c.owner}/${c.repo}`,
      "--json",
      "name,state,description,link,workflow,bucket",
    ]);
    if ([0, 1, 8].includes(r.code) && r.stdout.trim())
      try {
        const v = JSON.parse(r.stdout);
        if (Array.isArray(v))
          return {
            kind: "checks",
            checks: v.map((x) => parseCheck(x, "fast")),
            headSha: head,
            binding: "bracketed-pr-read",
          };
      } catch {}
    return { kind: "unusable", exitCode: r.code };
  }
  async checksAt(c, head) {
    const query = `query Checks($owner:String!,$repo:String!,$oid:GitObjectID!,$after:String){repository(owner:$owner,name:$repo){object(oid:$oid){... on Commit{oid statusCheckRollup{state contexts(first:100,after:$after){${pageInfo} nodes{__typename ... on CheckRun{id name status conclusion detailsUrl} ... on StatusContext{id context state targetUrl}}}}}}}}`;
    let rollupState = null;
    const rows = await paginate(async (pageToken) => {
      const v = await this.graphql(query, c, [
        "-f",
        `oid=${head}`,
        ...(pageToken ? ["-f", `after=${pageToken}`] : []),
      ]);
      const commit = obj(at(v, ["data", "repository", "object"]), "commit");
      fail(
        commit.oid === head,
        "Commit check query returned a different SHA",
        "STALE",
        7,
      );
      if (commit.statusCheckRollup === null)
        return { nodes: [], hasNextPage: false, endCursor: null };
      const rollup = obj(commit.statusCheckRollup, "rollup");
      rollupState = enumeration(
        rollup.state,
        ["SUCCESS", "PENDING", "EXPECTED", "FAILURE", "ERROR"],
        "rollup.state",
      );
      const p = obj(rollup.contexts, "contexts");
      return {
        nodes: arr(p.nodes, "contexts.nodes"),
        ...obj(p.pageInfo, "pageInfo"),
      };
    });
    return {
      source: "commit-rollup",
      checks: rows.map((v) => parseCheck(v)),
      headSha: head,
      rollupState,
      complete: true,
    };
  }
  async reviewThreads(c) {
    const query = `query Threads($owner:String!,$repo:String!,$pr:Int!,$after:String){repository(owner:$owner,name:$repo){pullRequest(number:$pr){reviewThreads(first:100,after:$after){${pageInfo} nodes{id isResolved comments(first:1){nodes{body path line createdAt author{login}}}}}}}}`;
    const rows = await paginate(async (pageToken) => {
      const v = await this.graphql(
        query,
        c,
        pageToken ? ["-f", `after=${pageToken}`] : [],
      );
      const p = obj(
        at(v, ["data", "repository", "pullRequest", "reviewThreads"]),
        "threads",
      );
      return {
        nodes: arr(p.nodes, "threads.nodes"),
        ...obj(p.pageInfo, "pageInfo"),
      };
    });
    return annotateReviewThreads(rows.map(parseThread), this.reviewerPolicy);
  }
  async commitRollups(c) {
    const query = `query Commits($owner:String!,$repo:String!,$pr:Int!,$after:String){repository(owner:$owner,name:$repo){pullRequest(number:$pr){commits(first:100,after:$after){${pageInfo} nodes{commit{oid statusCheckRollup{state}}}}}}}`;
    const rows = await paginate(async (pageToken) => {
      const v = await this.graphql(
        query,
        c,
        pageToken ? ["-f", `after=${pageToken}`] : [],
      );
      const p = obj(
        at(v, ["data", "repository", "pullRequest", "commits"]),
        "commits",
      );
      return {
        nodes: arr(p.nodes, "commits.nodes"),
        ...obj(p.pageInfo, "pageInfo"),
      };
    });
    return rows.map((v) => {
      const p = obj(obj(v, "commit node").commit, "commit");
      return {
        oid: sha(p.oid),
        state:
          p.statusCheckRollup === null
            ? null
            : enumeration(
                obj(p.statusCheckRollup, "rollup").state,
                ["SUCCESS", "PENDING", "EXPECTED", "FAILURE", "ERROR"],
                "rollup.state",
              ),
      };
    });
  }
}

export async function resolveContext(reader, { owner, repo, pr }) {
  if (owner && repo && pr) {
    repository(`${owner}/${repo}`);
    return { owner, repo, number: positive(pr) };
  }
  if (pr) {
    const origin = await reader.originRepo();
    if (origin) {
      const c = {
        owner: owner ?? origin.owner,
        repo: repo ?? origin.repo,
        number: positive(pr),
      };
      repository(`${c.owner}/${c.repo}`);
      return c;
    }
  }
  const c = await reader.currentPr(pr ?? null);
  const result = { ...c, owner: owner ?? c.owner, repo: repo ?? c.repo };
  repository(`${result.owner}/${result.repo}`);
  return result;
}
export const discoverStack = async (reader, seed) =>
  discoverGraph(seed, await reader.openPullRequests(seed));
export async function resolveChecks(reader, c, head) {
  // The fast path remains useful for diagnostics, but commit-bound evidence is authoritative.
  const fast = await reader.checksFastPath(c, head);
  if (typeof reader.checksAt === "function") {
    const direct = await reader.checksAt(c, head);
    if (direct.headSha !== head || !direct.complete)
      throw new QueryError(
        "stale-checks",
        "Checks are not complete for the current head",
      );
    if (direct.checks.length) return direct;
    // Empty checks do not establish absence of required checks.
    throw new QueryError(
      "checks-unavailable",
      "No commit-bound checks were available",
    );
  }
  if (
    fast.kind === "checks" &&
    fast.headSha === head &&
    fast.complete === true &&
    fast.checks.length
  )
    return { source: "provided-head-checks", ...fast };
  throw new QueryError(
    "checks-unavailable",
    "Reader did not provide complete head-bound checks",
  );
}
