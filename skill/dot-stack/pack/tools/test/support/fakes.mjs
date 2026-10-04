export const HEAD = "a".repeat(40),
  BASE = "b".repeat(40),
  NEXT = "c".repeat(40);
export const context = (number) => ({ owner: "owner", repo: "repo", number });
export const check = (kind = "passed", name = "ci") => ({
  kind,
  name,
  id: name,
  reportedState: kind === "passed" ? "SUCCESS" : kind.toUpperCase(),
  description: "",
  link: "",
  workflow: "",
});
export function fakeReader({
  facts = {},
  checks = [check()],
  threads = [],
  rollupState = "SUCCESS",
  history = [],
  open = [],
  onRead,
} = {}) {
  const calls = [];
  let reads = 0;
  return {
    calls,
    async originRepo() {
      calls.push("originRepo");
      return { owner: "owner", repo: "repo" };
    },
    async currentPr(n) {
      calls.push("currentPr");
      return context(n ?? 1);
    },
    async openPullRequests() {
      calls.push("openPullRequests");
      return open;
    },
    async pullRequest(c) {
      calls.push(`pr:${c.number}`);
      const defaults = {
        context: c,
        state: "OPEN",
        isDraft: false,
        mergeable: "MERGEABLE",
        mergeStateStatus: "CLEAN",
        reviewDecision: "APPROVED",
        headRefOid: HEAD,
        baseRefOid: BASE,
        headRefName: `branch-${c.number}`,
        baseRefName: "main",
        mergedAt: null,
        ...facts,
      };
      return onRead ? onRead(c, ++reads, defaults) : defaults;
    },
    async checksFastPath(c, head) {
      calls.push(`fast:${c.number}`);
      return { kind: "checks", checks, headSha: head };
    },
    async checksAt(c, head) {
      calls.push(`checks:${c.number}`);
      return {
        source: "fake-commit",
        checks,
        headSha: head,
        rollupState,
        complete: true,
      };
    },
    async reviewThreads(c) {
      calls.push(`threads:${c.number}`);
      return threads;
    },
    async commitRollups(c) {
      calls.push(`history:${c.number}`);
      return history;
    },
  };
}
export function fakeClock({ onSleep } = {}) {
  let time = 0;
  return {
    now: () => time,
    observedAt: () => new Date(1700000000000 + time * 1000).toISOString(),
    async sleep(seconds) {
      time += seconds;
      await onSleep?.(seconds, time);
    },
    advance: (seconds) => {
      time += seconds;
    },
  };
}
export function graph(states = ["MERGED", "OPEN"]) {
  return {
    schemaVersion: 1,
    repository: "owner/repo",
    nodes: states.map((state, i) => ({
      id: `u${i}`,
      pr: i + 1,
      branch: `branch-${i}`,
      headSha: HEAD,
      baseSha: BASE,
      state,
      dependsOn: i ? [`u${i - 1}`] : [],
    })),
  };
}
