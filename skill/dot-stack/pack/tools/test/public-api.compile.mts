import { sha, prNumber } from "../lib/core.mjs";
import { watch, validateEvent } from "../lib/watcher.mjs";
import { mutationRequest, validateGraph } from "../lib/graph.mjs";
import { Orchestrator } from "../lib/orchestration.mjs";
import type { ForgeReader, CommitSha, ReadyEvent } from "../lib/contracts.js";

declare const reader: ForgeReader;
const context = { owner: "owner", repo: "repo", number: prNumber(1) };
const head = sha("a".repeat(40)),
  base = sha("b".repeat(40));
async function typedConsumer() {
  const event = await watch({ reader, contexts: [context] });
  // @ts-expect-error A boolean-only object is not a usable cancellation signal.
  await watch({ reader, contexts: [context], signal: { aborted: false } });
  if (event.kind === "READY") {
    const readiness: ReadyEvent = event;
    const allowed: false = event.authorizesExecution;
    // @ts-expect-error A real watch result's READY exit is not a failure code.
    const exit: 4 = event.exitCode;
    for (const pr of event.prs)
      if (pr.kind === "ready-pr") {
        const candidate: CommitSha = pr.proof.headSha;
        // @ts-expect-error Actual watch proof does not allow a failed check list.
        const failures: readonly [unknown] = pr.proof.checks.failed;
        void [candidate, failures];
      }
    void [readiness, allowed, exit];
  }
  const parsed = validateEvent(JSON.parse("{}"));
  if (parsed.kind === "READY") {
    const permission: false = parsed.authorizesExecution;
    void permission;
  }
  const request = mutationRequest({
    action: "merge-pr",
    target: "owner/repo#1",
    headSha: head,
    baseSha: base,
    generation: 1,
    evidence: ["receipt"],
  });
  // @ts-expect-error Real graph helper returns an inert action request.
  const executable: true = request.executable;
  mutationRequest({
    action: "merge-pr",
    target: "owner/repo#1",
    // @ts-expect-error Commit input to the public action helper must be validated.
    headSha: "unvalidated",
    generation: 1,
    evidence: ["receipt"],
  });
  const store = new Orchestrator("project-state");
  const receipt = await store.ledgerRecord({
    pr: 1,
    sha: head,
    verdict: "behavior-verified",
    evidence: "proof.log",
  });
  const receiptHead: CommitSha = receipt.sha;
  await store.ledgerRecord({
    pr: 1,
    sha: head,
    // @ts-expect-error The actual receipt writer rejects unknown verdict labels at the API boundary.
    verdict: "looks-good",
    evidence: "proof.log",
  });
  // @ts-expect-error Exact-head checking requires a validated commit identity.
  await store.ledgerCheck({ pr: 1, sha: "HEAD" });
  const passing = await store.ledgerCheck({
    pr: 1,
    sha: head,
    requirePass: true,
  });
  // @ts-expect-error requirePass narrows failed/blocked/type-only receipts away.
  const blocked: "verifier-blocked" = passing.verdict;
  const graph = validateGraph({
    schemaVersion: 1,
    repository: "owner/repo",
    nodes: [
      {
        id: "one",
        pr: 1,
        branch: "feature",
        headSha: head,
        state: "OPEN",
        dependsOn: [],
      },
    ],
  });
  const graphHead: CommitSha = graph.nodes[0].headSha;
  // @ts-expect-error PR numbers must use the public validating constructor.
  await watch({ reader, contexts: [{ ...context, number: 1 }] });
  void [executable, receiptHead, blocked, graphHead];
}
void typedConsumer;
