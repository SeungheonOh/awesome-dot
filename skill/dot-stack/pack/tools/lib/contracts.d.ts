/** Public data contracts. Runtime validators remain mandatory for external JSON. */
declare const commitShaBrand: unique symbol;
declare const prNumberBrand: unique symbol;
export type CommitSha = string & { readonly [commitShaBrand]: "CommitSha" };
export type PrNumber = number & { readonly [prNumberBrand]: "PrNumber" };
export type NonEmpty<T> = readonly [T, ...T[]];
export interface PrContext {
  readonly owner: string;
  readonly repo: string;
  readonly number: PrNumber;
}
export type MergeState =
  | "CLEAN"
  | "BLOCKED"
  | "BEHIND"
  | "DIRTY"
  | "CONFLICTING"
  | "DRAFT"
  | "HAS_HOOKS"
  | "UNKNOWN"
  | "UNSTABLE";
export type RollupState =
  | "SUCCESS"
  | "PENDING"
  | "EXPECTED"
  | "FAILURE"
  | "ERROR"
  | null;
export interface AllowedMerge {
  readonly kind: "allowed";
  readonly reason: "current-head-clean";
  readonly mergeStateStatus: "CLEAN";
  readonly headRollupState: "SUCCESS";
}
export type MergeAssessment =
  | AllowedMerge
  | {
      readonly kind: "refused" | "unknown" | "gated";
      readonly reason: string;
      readonly mergeStateStatus: MergeState;
      readonly headRollupState: RollupState;
    };
export interface Check {
  readonly kind: "passed" | "skipped" | "pending" | "failed" | "unknown";
  readonly name: string;
  readonly reportedState: string;
  readonly id?: string;
}
export interface CleanChecks {
  readonly kind: "clean";
  readonly checks: NonEmpty<Check & { readonly kind: "passed" | "skipped" }>;
  readonly failed: readonly [];
  readonly pending: readonly [];
  readonly unknown: readonly [];
  readonly assessment: AllowedMerge;
  readonly headSha: CommitSha;
  readonly complete: true;
}
export interface ReadyProof {
  readonly headSha: CommitSha;
  readonly baseSha: CommitSha;
  readonly mergeability: "clear";
  readonly threads: readonly [];
  readonly checks: CleanChecks;
  readonly reviewDecision: "APPROVED" | null;
  readonly draft: "not-draft" | "draft-allowed";
}
export interface ReadyPr {
  readonly kind: "ready-pr";
  readonly context: PrContext;
  readonly proof: ReadyProof;
}
export interface MergedPr {
  readonly kind: "merged-pr";
  readonly context: PrContext;
  readonly mergedAt: string | null;
}
export interface EventEnvelope {
  readonly schemaVersion: 2;
  readonly sequence: number;
  readonly observedAt: string;
  readonly mode: "single" | "stack" | "queued-stack";
}
export interface ReadyEvent extends EventEnvelope {
  readonly kind: "READY";
  readonly terminal: true;
  readonly exitCode: 0;
  readonly prs: NonEmpty<ReadyPr | MergedPr>;
  readonly meaning: "forge-readiness-only";
  readonly authorizesExecution: false;
}
export interface ActionRequest {
  readonly schemaVersion: 1;
  readonly kind: "ACTION_REQUEST";
  readonly authorized: false;
  readonly executable: false;
  readonly action:
    | "publish-branch"
    | "reply-thread"
    | "retarget-pr"
    | "merge-pr"
    | "remove-worktree";
  readonly target: string;
  readonly expected: {
    readonly headSha: CommitSha;
    readonly baseSha: CommitSha | null;
    readonly generation: number;
  };
  readonly evidence: NonEmpty<string>;
  readonly data: unknown;
}

export interface PullRequestFacts {
  readonly context: PrContext;
  readonly state: "OPEN" | "CLOSED" | "MERGED";
  readonly isDraft: boolean;
  readonly mergeable: "MERGEABLE" | "CONFLICTING" | "UNKNOWN";
  readonly mergeStateStatus: MergeState;
  readonly reviewDecision:
    | "APPROVED"
    | "CHANGES_REQUESTED"
    | "REVIEW_REQUIRED"
    | null;
  readonly headRefOid: CommitSha;
  readonly baseRefOid: CommitSha;
  readonly headRefName: string;
  readonly baseRefName: string;
  readonly mergedAt: string | null;
}
export interface BoundChecks {
  readonly source: string;
  readonly checks: readonly Check[];
  readonly headSha: CommitSha;
  readonly complete: true;
  readonly rollupState: RollupState;
}
export interface ReviewThread {
  readonly id: string;
  readonly firstComment: {
    readonly body: string;
    readonly authorLogin: string | null;
    readonly path: string | null;
    readonly line: number | null;
    readonly createdAt: string;
  } | null;
  readonly automation?: {
    readonly author: string;
    readonly runId: string | null;
  } | null;
  readonly observedReviewPasses?: number;
}
export interface ForgeReader {
  pullRequest(context: PrContext): Promise<PullRequestFacts>;
  reviewThreads(context: PrContext): Promise<readonly ReviewThread[]>;
  checksFastPath(
    context: PrContext,
    head: CommitSha,
  ): Promise<
    | {
        readonly kind: "checks";
        readonly checks: readonly Check[];
        readonly headSha: CommitSha;
        readonly complete?: true;
      }
    | { readonly kind: "unusable"; readonly exitCode: number }
  >;
  checksAt(context: PrContext, head: CommitSha): Promise<BoundChecks>;
  commitRollups?(
    context: PrContext,
  ): Promise<
    readonly { readonly oid: CommitSha; readonly state: RollupState }[]
  >;
}
export interface AbortSignalLike {
  readonly aborted: boolean;
  readonly reason?: unknown;
  addEventListener(
    type: "abort",
    listener: () => void,
    options?: { readonly once?: boolean },
  ): void;
  removeEventListener(type: "abort", listener: () => void): void;
}
export interface WatchClock {
  now(): number;
  observedAt(): string;
  sleep(seconds: number, signal?: AbortSignalLike): Promise<void>;
}
export interface OtherTerminalEvent extends EventEnvelope {
  readonly kind: "STATUS" | "COMPLETE" | "BLOCKER" | "TIMEOUT";
  readonly terminal: true;
  readonly exitCode: 0 | 2 | 3 | 4 | 5 | 6 | 7;
  readonly [field: string]: unknown;
}
export interface ProgressEvent extends EventEnvelope {
  readonly kind: "QUEUE" | "STATUS" | "WAITING" | "ADVANCE" | "RETRY";
  readonly terminal: false;
  readonly [field: string]: unknown;
}
export type TerminalEvent = ReadyEvent | OtherTerminalEvent;
export type WatcherEvent = TerminalEvent | ProgressEvent;
export interface WatchOptions {
  readonly interval?: number;
  readonly sweepInterval?: number;
  readonly timeout?: number;
  readonly maxQueryErrors?: number;
  readonly allowDraft?: boolean;
}
export interface WatchConfig {
  readonly reader: ForgeReader;
  readonly contexts: NonEmpty<PrContext>;
  readonly mode?: EventEnvelope["mode"];
  readonly statusOnly?: boolean;
  readonly options?: WatchOptions;
  readonly clock?: WatchClock;
  readonly signal?: AbortSignalLike;
  readonly emit?: (event: ProgressEvent) => void;
  readonly checkpoint?: (state: unknown) => Promise<void>;
}
export type VerificationVerdict =
  | "live-ui-verified"
  | "unit-test-verified"
  | "type-check-only"
  | "behavior-verified"
  | "docs-verified"
  | "verifier-blocked"
  | "verifier-failed";
export interface Receipt {
  readonly id: string;
  readonly pr: string;
  readonly sha: CommitSha;
  readonly verdict: VerificationVerdict;
  readonly evidence: string;
  readonly verifier: string;
  readonly ts: string;
  readonly baseSha: CommitSha | null;
  readonly profile: string | null;
  readonly patchId: string | null;
  readonly supersedes: string | null;
}
export interface RecordReceipt {
  readonly pr: number;
  readonly sha: CommitSha;
  readonly verdict: VerificationVerdict;
  readonly evidence: string;
  readonly verifier?: string;
  readonly baseSha?: CommitSha | null;
  readonly profile?: string | null;
  readonly patchId?: string | null;
}
export interface CheckReceipt {
  readonly pr: number;
  readonly sha: CommitSha;
  readonly baseSha?: CommitSha;
  readonly profile?: string;
  readonly requirePass?: boolean;
}
export interface Unit {
  readonly id: string;
  readonly track: string;
  readonly state: string;
  readonly branch: string;
  readonly pr: string;
  readonly sha: CommitSha | "";
  readonly brief: string;
}
export interface GraphNode {
  readonly id: string;
  readonly pr: number;
  readonly branch: string;
  readonly baseBranch?: string | null;
  readonly headSha: CommitSha;
  readonly baseSha?: CommitSha | null;
  readonly state: "OPEN" | "MERGED" | "CLOSED" | "UNKNOWN";
  readonly dependsOn: readonly string[];
}
export interface DependencyGraph {
  readonly schemaVersion: 1;
  readonly repository: string;
  readonly nodes: readonly GraphNode[];
}
export interface Frontier extends DependencyGraph {
  readonly generation: number;
  readonly eligible: readonly number[];
  readonly blocked: readonly {
    readonly id: string;
    readonly reasons: readonly string[];
  }[];
  readonly lowestUnmerged: number | null;
}
export interface InboxPointer {
  readonly id: string;
  readonly ts: string;
  readonly agent: string;
  readonly unit: string;
  readonly status: string;
  readonly report: string;
  readonly idempotencyKey: string | null;
  readonly delivery: "pending" | "claimed" | "delivered";
}
export interface InboxBatch {
  readonly id: string | null;
  readonly ids: readonly string[];
  readonly state: "claimed" | "delivered" | "empty";
  readonly pointers?: readonly InboxPointer[];
  readonly replay?: boolean;
}
export interface Gate {
  readonly id: string;
  readonly kind: "open" | "resolved";
  readonly question: string;
  readonly options: string;
  readonly defaultAnswer: string;
  readonly answer?: string;
  readonly history: readonly unknown[];
}
export interface StatusReport {
  readonly revision: number;
  readonly units: readonly Unit[];
  readonly ledger: readonly Receipt[];
  readonly frontier: Frontier | { readonly generation: 0 };
  readonly gates: readonly Gate[];
  readonly summary: {
    readonly unitStates: Readonly<Record<string, number>>;
    readonly ledgerVerdicts: Readonly<Record<string, number>>;
    readonly frontierGeneration: number;
    readonly openGateIds: readonly string[];
  };
  readonly changed: string;
}
