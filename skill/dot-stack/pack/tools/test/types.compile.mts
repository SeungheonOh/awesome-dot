import { sha } from "../lib/core.mjs";
import type {
  AllowedMerge,
  CleanChecks,
  ReadyEvent,
  ReadyPr,
  PrNumber,
  ActionRequest,
} from "../lib/contracts.js";

const context = { owner: "owner", repo: "repo", number: 1 as PrNumber };
const assessment = {
  kind: "allowed",
  reason: "current-head-clean",
  mergeStateStatus: "CLEAN",
  headRollupState: "SUCCESS",
} as const satisfies AllowedMerge;
const checks = {
  kind: "clean",
  headSha: sha("a".repeat(40)),
  complete: true,
  checks: [{ kind: "passed", name: "ci", reportedState: "SUCCESS" }],
  failed: [],
  pending: [],
  unknown: [],
  assessment,
} as const satisfies CleanChecks;
const pr = {
  kind: "ready-pr",
  context,
  proof: {
    headSha: sha("a".repeat(40)),
    baseSha: sha("b".repeat(40)),
    mergeability: "clear",
    threads: [],
    checks,
    reviewDecision: "APPROVED",
    draft: "not-draft",
  },
} as const satisfies ReadyPr;
const ready = {
  schemaVersion: 2,
  sequence: 1,
  observedAt: "now",
  mode: "single",
  kind: "READY",
  terminal: true,
  exitCode: 0,
  prs: [pr],
  meaning: "forge-readiness-only",
  authorizesExecution: false,
} as const satisfies ReadyEvent;

const failureAllowed: AllowedMerge = {
  ...assessment,
  // @ts-expect-error A failing rollup cannot be an allowed merge assessment.
  headRollupState: "FAILURE",
};
const unknownAllowed: AllowedMerge = {
  ...assessment,
  // @ts-expect-error Unknown merge state is not positive proof.
  mergeStateStatus: "UNKNOWN",
};
const failedClean: CleanChecks = {
  ...checks,
  // @ts-expect-error Clean CI cannot include a failed check.
  failed: [{ kind: "failed", name: "ci", reportedState: "FAILURE" }],
};
// @ts-expect-error Missing current candidate proof cannot be READY.
const unproven: ReadyPr = { kind: "ready-pr", context };
// @ts-expect-error READY cannot carry a failure exit code.
const badExit: ReadyEvent = { ...ready, exitCode: 4 };
const badHead: ReadyPr = {
  ...pr,
  // @ts-expect-error Unvalidated arbitrary strings are not commit identities.
  proof: { ...pr.proof, headSha: "looks-like-a-sha" },
};
// @ts-expect-error A watch event never authorizes execution.
const authority: ReadyEvent = { ...ready, authorizesExecution: true };
const request = {
  schemaVersion: 1,
  kind: "ACTION_REQUEST",
  authorized: false,
  executable: false,
  action: "merge-pr",
  target: "owner/repo#1",
  expected: {
    headSha: sha("a".repeat(40)),
    baseSha: sha("b".repeat(40)),
    generation: 1,
  },
  evidence: ["receipt"],
  data: null,
} as const satisfies ActionRequest;
const { headSha: _missingHead, ...unboundChecks } = checks;
// @ts-expect-error Positive checks require the exact bound commit identity.
const unbound: CleanChecks = unboundChecks;
// @ts-expect-error An inert request cannot become executable via a stored boolean.
const unlocked: ActionRequest = { ...request, executable: true };
void [
  failureAllowed,
  unknownAllowed,
  failedClean,
  unproven,
  badExit,
  badHead,
  authority,
  unlocked,
  unbound,
];
