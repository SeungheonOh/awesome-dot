import type {
  Unit,
  Receipt,
  RecordReceipt,
  CheckReceipt,
  VerificationVerdict,
  CommitSha,
  DependencyGraph,
  Frontier,
  InboxPointer,
  InboxBatch,
  Gate,
  StatusReport,
} from "./contracts.js";
export const VERDICTS: readonly VerificationVerdict[];
export class Orchestrator {
  constructor(
    directory: string,
    options?: {
      readonly now?: () => string;
      readonly id?: () => string;
      readonly lockWaitMs?: number;
    },
  );
  init(): Promise<{ readonly store: string }>;
  close(): Promise<void>;
  unitsList(filters?: {
    readonly state?: string;
    readonly track?: string;
  }): Promise<readonly Unit[]>;
  unitGet(id: string): Promise<Unit>;
  unitCounts(): Promise<Readonly<Record<string, number>>>;
  unitAdd(input: {
    readonly id: string;
    readonly track: string;
    readonly brief?: string;
  }): Promise<Unit>;
  unitSet(
    id: string,
    input: {
      readonly state: string;
      readonly branch?: string;
      readonly pr?: number;
      readonly sha?: CommitSha;
    },
    revision?: number,
  ): Promise<Unit>;
  ledgerRecord(input: RecordReceipt): Promise<Receipt>;
  ledgerCheck(input: CheckReceipt & { readonly requirePass: true }): Promise<
    Receipt & {
      readonly verdict: Exclude<
        VerificationVerdict,
        "verifier-blocked" | "verifier-failed" | "type-check-only"
      >;
    }
  >;
  ledgerCheck(input: CheckReceipt): Promise<Receipt>;
  ledgerSummary(): Promise<
    Readonly<Partial<Record<VerificationVerdict, number>>>
  >;
  frontierSet(
    graph: DependencyGraph,
    pin?: readonly number[],
    expectedRevision?: number,
  ): Promise<Frontier>;
  frontierShow(): Promise<
    | Frontier
    | {
        readonly generation: 0;
        readonly nodes: readonly [];
        readonly eligible: readonly [];
        readonly blocked: readonly [];
        readonly lowestUnmerged: null;
      }
  >;
  inboxPush(input: {
    readonly agent: string;
    readonly unit: string;
    readonly status: string;
    readonly report?: string;
    readonly idempotencyKey?: string | null;
  }): Promise<InboxPointer>;
  inboxPeek(): Promise<readonly InboxPointer[]>;
  inboxCount(): Promise<number>;
  inboxDrain(): Promise<InboxBatch>;
  inboxAck(id: string): Promise<InboxBatch>;
  gatePark(input: {
    readonly id: string;
    readonly question: string;
    readonly options: string;
    readonly defaultAnswer: string;
  }): Promise<Gate & { readonly kind: "open" }>;
  gateList(): Promise<readonly (Gate & { readonly kind: "open" })[]>;
  gateResolve(
    id: string,
    answer: string,
  ): Promise<
    Gate & {
      readonly kind: "resolved";
      readonly answer: string;
      readonly authorizesExecution: false;
    }
  >;
  standingShow(): Promise<
    readonly { readonly number: number; readonly line: string }[]
  >;
  standingAdd(
    line: string,
  ): Promise<{ readonly number: number; readonly line: string }>;
  status(options?: { readonly readOnly?: boolean }): Promise<StatusReport>;
  exportViews(): Promise<{ readonly revision: number; readonly derived: true }>;
}
