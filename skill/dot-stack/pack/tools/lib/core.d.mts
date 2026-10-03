import type { CommitSha, PrNumber } from "./contracts.js";
export function sha(value: unknown, label?: string): CommitSha;
export function positive(value: unknown, label?: string): number;
export function prNumber(value: unknown): PrNumber;
