import type {
  WatchConfig,
  TerminalEvent,
  WatcherEvent,
  PullRequestFacts,
  RollupState,
  MergeAssessment,
} from "./contracts.js";
export function watch(config: WatchConfig): Promise<TerminalEvent>;
export function validateEvent(value: unknown): WatcherEvent;
export function renderJson(value: WatcherEvent): string;
export function renderPretty(value: WatcherEvent): string;
export function assessMerge(
  facts: Pick<PullRequestFacts, "mergeable" | "mergeStateStatus">,
  rollup: RollupState,
): MergeAssessment;
export function backoff(interval: number, failures: number): number;
