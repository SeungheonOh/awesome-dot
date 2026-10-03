// Self-contained teaching examples, not a project API or security boundary.
declare const userIdBrand: unique symbol;
declare const durationBrand: unique symbol;
declare const timeRangeBrand: unique symbol;

export type UserId = string & { readonly [userIdBrand]: true };
export type DurationMs = number & { readonly [durationBrand]: true };
export type TimeRange = Readonly<{
  startMs: number;
  durationMs: DurationMs;
  [timeRangeBrand]: true;
}>;

export function parseUserId(input: unknown): UserId {
  if (typeof input !== "string" || !/^usr_[a-z0-9]{1,32}$/.test(input)) {
    throw new TypeError("Invalid user ID");
  }
  return input as UserId;
}

export function parseDurationMs(input: unknown): DurationMs {
  if (typeof input !== "number" || !Number.isFinite(input) || input < 0) {
    throw new TypeError("Duration must be a finite nonnegative number");
  }
  return input as DurationMs;
}

export function makeTimeRange(startMs: number, durationMs: DurationMs): TimeRange {
  const endMs = startMs + durationMs;
  const dateLimit = 8_640_000_000_000_000;
  if (!Number.isFinite(startMs) || Math.abs(startMs) > dateLimit ||
      !Number.isFinite(durationMs) || durationMs < 0 ||
      !Number.isFinite(endMs) || Math.abs(endMs) > dateLimit) {
    throw new RangeError("Range exceeds supported timestamps");
  }
  return Object.freeze({ startMs, durationMs }) as TimeRange;
}

export function rangeEnd(range: TimeRange): number {
  return range.startMs + range.durationMs;
}

export type NonEmpty<T> = readonly [T, ...T[]];
export function isNonEmpty<T>(items: readonly T[]): items is NonEmpty<T> {
  return items.length > 0 && Object.hasOwn(items, 0);
}
export function snapshotNonEmpty<T>(items: readonly T[]): NonEmpty<T> | undefined {
  const snapshot = Object.freeze(items.slice());
  return isNonEmpty(snapshot) ? snapshot : undefined;
}
export function first<T>(items: NonEmpty<T>): T {
  return items[0];
}
export function sum(items: readonly number[]): number {
  return items.reduce((total, value) => total + value, 0);
}

export type User = Readonly<{ id: UserId; role: "admin" | "member" }>;
export function parseUser(input: unknown): User {
  if (typeof input !== "object" || input === null || Array.isArray(input) ||
      !("id" in input) || !("role" in input) ||
      !Object.hasOwn(input, "id") || !Object.hasOwn(input, "role") ||
      Object.keys(input).some(key => key !== "id" && key !== "role")) {
    throw new TypeError("Expected a user record with id and role");
  }
  const id = parseUserId(input.id);
  const role = input.role;
  if (role !== "admin" && role !== "member") {
    throw new TypeError("Invalid user role");
  }
  return Object.freeze({ id, role });
}

export type LoadState<T> =
  | { kind: "loading" }
  | { kind: "ready"; value: T }
  | { kind: "error"; message: string };

export function renderState(state: LoadState<string>): string {
  switch (state.kind) {
    case "loading": return "Loading";
    case "ready": return state.value;
    case "error": return `Error: ${state.message}`;
    default: {
      const exhaustive: never = state;
      return exhaustive;
    }
  }
}

export type ViewConfig = { theme: "dark" | "light"; columns: number };
export const viewConfig = { theme: "dark", columns: 3 } satisfies ViewConfig;
export type UserRole = User["role"];
export type ParsedUser = ReturnType<typeof parseUser>;

export function displayUser({ user, includeRole }: {
  user: User;
  includeRole: boolean;
}): string {
  return includeRole ? `${user.id} (${user.role})` : user.id;
}
