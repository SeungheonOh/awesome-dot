const assert = require("node:assert/strict");
if (!process.argv[2])
  throw new Error("Pass the compiled examples.js fixture path.");
const m = require(process.argv[2]);
const tests = [];
function test(name, fn) {
  fn();
  tests.push({ name, status: "passed" });
}
test("empty sum is total", () => assert.equal(m.sum([]), 0));
test("sum computes actual values", () => assert.equal(m.sum([2, -1, 3]), 4));
test("empty collection fails nonempty predicate", () =>
  assert.equal(m.isNonEmpty([]), false));
test("nonempty collection passes predicate", () =>
  assert.equal(m.isNonEmpty(["a"]), true));
test("sparse length-one array fails nonempty predicate", () =>
  assert.equal(m.isNonEmpty(new Array(1)), false));
test("deleted first element fails nonempty predicate", () => {
  const xs = [1, 2];
  delete xs[0];
  assert.equal(m.isNonEmpty(xs), false);
});
test("dense explicit undefined has a head", () =>
  assert.equal(m.isNonEmpty([undefined]), true));
test("empty snapshot is absent", () =>
  assert.equal(m.snapshotNonEmpty([]), undefined));
test("sparse snapshot is absent", () =>
  assert.equal(m.snapshotNonEmpty(new Array(1)), undefined));
test("snapshot survives source mutation", () => {
  const xs = [1, 2];
  const snapshot = m.snapshotNonEmpty(xs);
  xs.shift();
  xs.length = 0;
  assert.equal(m.first(snapshot), 1);
  assert.deepEqual(snapshot, [1, 2]);
  assert.ok(Object.isFrozen(snapshot));
});
test("snapshot cannot have its head deleted", () => {
  const snapshot = m.snapshotNonEmpty([1]);
  assert.equal(Reflect.deleteProperty(snapshot, "0"), false);
  assert.equal(m.first(snapshot), 1);
});
test("first uses guaranteed index", () =>
  assert.equal(m.first(["a", "b"]), "a"));
test("valid user id returns value", () =>
  assert.equal(m.parseUserId("usr_demo"), "usr_demo"));
for (const value of [
  "",
  "demo",
  "usr_",
  "usr_UPPER",
  "usr_" + "a".repeat(33),
  null,
  42,
])
  test("bad user id rejected: " + String(value), () =>
    assert.throws(() => m.parseUserId(value), TypeError),
  );
test("valid user is constructed frozen", () => {
  const u = m.parseUser({ id: "usr_demo", role: "member" });
  assert.deepEqual(u, { id: "usr_demo", role: "member" });
  assert.ok(Object.isFrozen(u));
});
for (const value of [
  null,
  [],
  {},
  { id: "usr_demo" },
  { id: "bad", role: "member" },
  { id: "usr_demo", role: "owner" },
  { id: "usr_demo", role: "member", extra: true },
  Object.create({ id: "usr_demo", role: "member" }),
])
  test("malformed user rejected " + tests.length, () =>
    assert.throws(() => m.parseUser(value), TypeError),
  );
for (const value of [0, 0.5, 10])
  test("valid duration " + value, () =>
    assert.equal(m.parseDurationMs(value), value),
  );
for (const value of [-1, NaN, Infinity, -Infinity, "1", null])
  test("invalid duration " + String(value), () =>
    assert.throws(() => m.parseDurationMs(value), TypeError),
  );
test("range end and freeze", () => {
  const r = m.makeTimeRange(100, m.parseDurationMs(25));
  assert.equal(m.rangeEnd(r), 125);
  assert.ok(Object.isFrozen(r));
});
test("negative epoch is supported", () =>
  assert.equal(m.rangeEnd(m.makeTimeRange(-100, m.parseDurationMs(25))), -75));
test("maximum timestamp accepted", () =>
  assert.equal(
    m.rangeEnd(m.makeTimeRange(8640000000000000, m.parseDurationMs(0))),
    8640000000000000,
  ));
for (const [start, duration] of [
  [NaN, 0],
  [Infinity, 0],
  [-8640000000000001, 0],
  [8640000000000000, 1],
  [0, -1],
  [0, Infinity],
])
  test("invalid combined range " + String(start) + "/" + String(duration), () =>
    assert.throws(() => m.makeTimeRange(start, duration), RangeError),
  );
test("loading branch", () =>
  assert.equal(m.renderState({ kind: "loading" }), "Loading"));
test("ready branch", () =>
  assert.equal(m.renderState({ kind: "ready", value: "ok" }), "ok"));
test("error branch", () =>
  assert.equal(m.renderState({ kind: "error", message: "no" }), "Error: no"));
test("object argument behavior", () =>
  assert.equal(
    m.displayUser({
      user: m.parseUser({ id: "usr_demo", role: "admin" }),
      includeRole: true,
    }),
    "usr_demo (admin)",
  ));
console.log(
  JSON.stringify(
    { checks: tests.length, passed: tests.length, tests },
    null,
    2,
  ),
);
