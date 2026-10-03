// Compiler tests. The expected-error directives are intentional proof obligations.
import {
  first, isNonEmpty, snapshotNonEmpty, parseUserId, parseDurationMs, makeTimeRange, viewConfig,
  type DurationMs, type LoadState, type TimeRange, type UserId,
} from "./examples.js";

const id: UserId = parseUserId("usr_demo");
const duration: DurationMs = parseDurationMs(10);
const range: TimeRange = makeTimeRange(0, duration);
const dark: "dark" = viewConfig.theme;
const head: string = first(["a", "b"]);
void [id, range, dark, head];

// @ts-expect-error Raw strings must pass the ID constructor.
const rawId: UserId = "usr_demo";
// @ts-expect-error A number is not a validated duration.
const rawDuration: DurationMs = -1;
// @ts-expect-error The empty collection does not satisfy NonEmpty.
first([]);
// @ts-expect-error A ready state requires its value.
const invalidReady: LoadState<string> = { kind: "ready" };
// @ts-expect-error The range constructor owns the combined bounds invariant.
const rawRange: TimeRange = { startMs: 0, durationMs: duration };
// @ts-expect-error Arbitrary unknown input is not a domain value.
const unparsed: UserId = {} as unknown;
void [rawId, rawDuration, invalidReady, rawRange, unparsed];

// Sparse arrays are legal number[] values; the runtime guard must reject a missing head.
const sparseNumbers: number[] = new Array<number>(1);
if (isNonEmpty(sparseNumbers)) {
  const head: number = first(sparseNumbers);
  void head;
}
const snapshot = snapshotNonEmpty([1]);
if (snapshot) {
  const head: number = first(snapshot);
  // @ts-expect-error The snapshot has a readonly first element.
  snapshot[0] = 2;
  void head;
}
// @ts-expect-error Snapshot creation can fail and must be narrowed before use.
first(snapshotNonEmpty(sparseNumbers));
