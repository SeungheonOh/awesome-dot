import type {
  ActionRequest,
  CommitSha,
  DependencyGraph,
  Frontier,
  NonEmpty,
  PrContext,
} from "./contracts.js";
export function repository(value: unknown): string;
export function validateGraph(
  input: DependencyGraph,
): Omit<Frontier, "generation">;
export function mutationRequest(input: {
  readonly action: ActionRequest["action"];
  readonly target: string;
  readonly headSha: CommitSha;
  readonly baseSha?: CommitSha | null;
  readonly generation: number;
  readonly evidence: NonEmpty<string>;
  readonly data?: unknown;
}): ActionRequest;
export function discoverGraph(
  seed: PrContext,
  open: readonly {
    readonly number: number;
    readonly headRefName: string;
    readonly baseRefName: string;
    readonly headRepository?: string | null;
  }[],
  options?: { readonly complete?: boolean },
): NonEmpty<PrContext>;
