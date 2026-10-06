# Fictional example: September order-cohort merchandise report

## Source and owner-defined rule

All names, amounts and records below are fictional. The evidence is the inline fixture, its schema, and this fictional reporting owner's specification. It contains no actual company policy or accounting conclusion.

The owner asks: “For paid orders placed in September 2026 UTC, show recorded merchandise line amounts less refunds posted before October 1, grouped by order currency.”

- Population: `state = 'paid'`, `2026-09-01T00:00:00Z <= ordered_at < 2026-10-01T00:00:00Z`
- Final grain: one row per currency; calculation grain: one row per order
- Refunds: for this order cohort, include postings strictly before the report cutoff. A later posting is outside this report. This is not a report of all September refund activity
- Units: positive integer minor units, with 100 minor units per unit for the fictional USD and EUR data. Lines already contain the owner's merchandise amount after discounts. Taxes and shipping are outside this metric. Refunds are positive deductions. No currency conversion or cross-currency grand total is allowed
- Complete line amount: the received line count equals the owner's expected count, at least one line is expected, and every line has a known amount in its order's currency
- Complete refund amount: the owner attests coverage through this exact cutoff, all received pre-cutoff refund amounts are known and currencies match. Under that rule, complete coverage with no refund records means zero. Missing/unknown coverage is not zero
- Source completeness: the fictional owner attests that all 9 qualifying order headers are present. Child data are intentionally incomplete. The manifest gives expected line counts and refund coverage per order; it does not supply missing amounts
- Snapshot: a frozen, self-contained fixture. Header and child relations are not changing during the run. Timestamp strings all use the same canonical UTC format, making the lexical comparisons valid here; arbitrary text timestamps would not be safe

## Schema and expected relationships

`orders.order_id`, `lines.line_id`, `refunds.refund_id`, and `coverage.order_id` are primary keys. Orders have zero or more line/refund rows. Coverage has at most one row per order. Child foreign keys are intentionally not enforced in this fictional extract so detached source records can be reconciled rather than discarded. Each amount carries its currency. Counts do not prove that an actual upstream extract is complete; the source-completeness attestation above is specific to this fixture.

Cases embedded in the fixture:

- O1: two same-valued line items and two refunds; a raw join multiplies both sides
- O2: complete refund coverage with no refunds before cutoff; its October 2 refund must be excluded
- O3: one line amount is null; summing only known values would hide the gap
- O4: a complete EUR order, kept separate from USD
- O5: no refunds received, but coverage explicitly unknown
- O6: one line expected but no line received
- O7: a refund exists with a missing amount
- O8: no coverage record; received line data alone cannot establish a complete total
- O9: exactly at the inclusive start; O0 is just before start, O10 exactly at the exclusive end, and O11 is cancelled
- LX and RX: a line and refund with no matching order header. Their amounts remain unallocated; their missing header means their cohort eligibility cannot be established

## Executable fixture and query

Copy the following single block into a local Python file and run it with Python 3. It uses only the standard library and a fresh in-memory SQLite database. It reads no files, opens no network connections and installs nothing. The DDL and inserts create fictional test data only. After setup, `query_only` and a restrictive authorizer guard the analytical phase; no custom SQL functions or external tables are registered. These controls demonstrate this connection's behavior, not a production connector's guarantees.

The `REPORT_SQL` string is a shared `WITH`/CTE prefix, not a complete statement by itself. The `per_order` execution appends `SELECT * FROM reconciled ORDER BY order_id`; the `summary` execution appends the currency-aggregation `SELECT` shown below. Those combined strings are the two complete reporting statements. Their rollups are independent and reduced to one row per order before they join. Other analytical statements below perform explicit negative controls and reconciliation on this same tiny fixture. They must not be copied to a live source as testing steps.

```python
import json
import sqlite3

START = "2026-09-01T00:00:00Z"
END = "2026-10-01T00:00:00Z"
PARAMS = {"start": START, "end": END}

db = sqlite3.connect(":memory:")
db.row_factory = sqlite3.Row
db.executescript("""
CREATE TABLE orders (
  order_id TEXT PRIMARY KEY, ordered_at TEXT NOT NULL,
  state TEXT NOT NULL, currency TEXT NOT NULL
);
CREATE TABLE lines (
  line_id TEXT PRIMARY KEY, order_id TEXT NOT NULL,
  currency TEXT NOT NULL, amount_minor INTEGER
);
CREATE TABLE refunds (
  refund_id TEXT PRIMARY KEY, order_id TEXT NOT NULL,
  currency TEXT NOT NULL, amount_minor INTEGER, posted_at TEXT NOT NULL
);
CREATE TABLE coverage (
  order_id TEXT PRIMARY KEY, expected_lines INTEGER,
  refunds_complete INTEGER NOT NULL CHECK (refunds_complete IN (0, 1)),
  covered_before TEXT NOT NULL
);
""")

orders = [(f"O{i}", "2026-09-05T12:00:00Z", "paid", "USD")
          for i in range(1, 9)]
orders[3] = ("O4", "2026-09-05T12:00:00Z", "paid", "EUR")
orders += [
    ("O9", START, "paid", "USD"),
    ("O0", "2026-08-31T23:59:59Z", "paid", "USD"),
    ("O10", END, "paid", "USD"),
    ("O11", "2026-09-05T12:00:00Z", "cancelled", "USD"),
]
lines = [
    ("L1", "O1", "USD", 1500), ("L2", "O1", "USD", 1500),
    ("L3", "O2", "USD", 4000),
    ("L4", "O3", "USD", None), ("L5", "O3", "USD", 500),
    ("L6", "O4", "EUR", 5000), ("L7", "O5", "USD", 2500),
    ("L8", "O7", "USD", 700), ("L9", "O8", "USD", 900),
    ("L10", "O9", "USD", 600), ("L11", "O0", "USD", 1500),
    ("L12", "O10", "USD", 8000), ("L13", "O11", "USD", 10000),
    ("LX", "MISSING", "USD", 777),
]
refunds = [
    ("R1", "O1", "USD", 200, "2026-09-06T00:00:00Z"),
    ("R2", "O1", "USD", 300, "2026-09-07T00:00:00Z"),
    ("R3", "O3", "USD", 100, "2026-09-07T00:00:00Z"),
    ("R4", "O4", "EUR", 500, "2026-09-07T00:00:00Z"),
    ("R7", "O7", "USD", None, "2026-09-07T00:00:00Z"),
    ("RF", "O2", "USD", 999, "2026-10-02T00:00:00Z"),
    ("RX", "MISSING", "USD", 111, "2026-09-07T00:00:00Z"),
]
coverage = [(f"O{i}", 2 if i in (1, 3) else 1,
             0 if i == 5 else 1, END)
            for i in range(12) if i != 8]
db.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", orders)
db.executemany("INSERT INTO lines VALUES (?, ?, ?, ?)", lines)
db.executemany("INSERT INTO refunds VALUES (?, ?, ?, ?, ?)", refunds)
db.executemany("INSERT INTO coverage VALUES (?, ?, ?, ?)", coverage)
db.commit()
setup_changes = db.total_changes

# Analytical statements below can only read the four fixture tables and use
# the aggregate/null functions reviewed here. Unknown authorizer actions fail.
db.execute("PRAGMA query_only = ON")
tables = {"orders", "lines", "refunds", "coverage"}
def authorize(action, arg1, arg2, database, source):
    if action == sqlite3.SQLITE_SELECT:
        return sqlite3.SQLITE_OK
    if action == sqlite3.SQLITE_READ and database == "main" and arg1 in tables:
        return sqlite3.SQLITE_OK
    if action == sqlite3.SQLITE_FUNCTION and (arg2 or "").lower() in {
        "sum", "count", "coalesce"
    }:
        return sqlite3.SQLITE_OK
    return sqlite3.SQLITE_DENY
db.set_authorizer(authorize)
progress_calls = 0
def stop_large_fixture_query():
    global progress_calls
    progress_calls += 1
    return int(progress_calls > 1000)
db.set_progress_handler(stop_large_fixture_query, 1000)

REPORT_SQL = """
WITH population AS (
  SELECT order_id, currency
  FROM orders
  WHERE state = 'paid' AND ordered_at >= :start AND ordered_at < :end
), line_rollup AS (
  SELECT p.order_id, COUNT(*) AS line_rows,
         SUM(CASE WHEN l.amount_minor IS NULL THEN 1 ELSE 0 END) AS missing,
         SUM(CASE WHEN l.currency = p.currency THEN 0 ELSE 1 END) AS bad_units,
         COALESCE(SUM(CASE WHEN l.currency = p.currency
                           THEN l.amount_minor END), 0) AS observed
  FROM population p JOIN lines l ON l.order_id = p.order_id
  GROUP BY p.order_id
), refund_rollup AS (
  SELECT p.order_id, COUNT(*) AS refund_rows,
         SUM(CASE WHEN r.amount_minor IS NULL THEN 1 ELSE 0 END) AS missing,
         SUM(CASE WHEN r.currency = p.currency THEN 0 ELSE 1 END) AS bad_units,
         COALESCE(SUM(CASE WHEN r.currency = p.currency
                           THEN r.amount_minor END), 0) AS observed
  FROM population p JOIN refunds r ON r.order_id = p.order_id
  WHERE r.posted_at < :end
  GROUP BY p.order_id
), amounts AS (
  SELECT p.order_id, p.currency, c.expected_lines, c.refunds_complete,
         COALESCE(l.line_rows, 0) AS line_rows,
         COALESCE(l.missing, 0) AS missing_line_amounts,
         COALESCE(l.bad_units, 0) AS line_unit_errors,
         COALESCE(r.refund_rows, 0) AS refund_rows,
         COALESCE(r.missing, 0) AS missing_refund_amounts,
         COALESCE(r.bad_units, 0) AS refund_unit_errors,
         COALESCE(l.observed, 0) AS observed_gross_minor,
         COALESCE(r.observed, 0) AS observed_refund_minor,
         CASE WHEN c.expected_lines >= 1
                    AND COALESCE(l.line_rows, 0) = c.expected_lines
                    AND COALESCE(l.missing, 0) = 0
                    AND COALESCE(l.bad_units, 0) = 0
              THEN COALESCE(l.observed, 0) END AS gross_minor,
         CASE WHEN c.refunds_complete = 1 AND c.covered_before = :end
                    AND COALESCE(r.missing, 0) = 0
                    AND COALESCE(r.bad_units, 0) = 0
              THEN COALESCE(r.observed, 0) END AS refund_minor
  FROM population p
  LEFT JOIN line_rollup l ON l.order_id = p.order_id
  LEFT JOIN refund_rollup r ON r.order_id = p.order_id
  LEFT JOIN coverage c ON c.order_id = p.order_id
), reconciled AS (
  SELECT *, gross_minor - refund_minor AS net_minor FROM amounts
)
"""
per_order = [dict(r) for r in db.execute(
    REPORT_SQL + "SELECT * FROM reconciled ORDER BY order_id", PARAMS)]
summary = [dict(r) for r in db.execute(REPORT_SQL + """
SELECT currency, COUNT(*) AS orders,
       COUNT(net_minor) AS known_net_orders,
       COUNT(*) - COUNT(net_minor) AS unknown_net_orders,
       SUM(observed_gross_minor) AS observed_gross_components_minor,
       SUM(observed_refund_minor) AS observed_refund_components_minor,
       CASE WHEN COUNT(gross_minor) = COUNT(*)
            THEN SUM(gross_minor) END AS gross_total_minor,
       CASE WHEN COUNT(refund_minor) = COUNT(*)
            THEN SUM(refund_minor) END AS refund_total_minor,
       COALESCE(SUM(net_minor), 0) AS known_order_net_subtotal_minor,
       CASE WHEN COUNT(net_minor) = COUNT(*)
            THEN SUM(net_minor) END AS net_total_minor
FROM reconciled GROUP BY currency ORDER BY currency
""", PARAMS)]

# Intentionally wrong read-only controls, confined to this fictional order.
wrong = dict(db.execute("""
SELECT COUNT(*) AS joined_rows, SUM(l.amount_minor) AS gross_minor,
       SUM(r.amount_minor) AS refund_minor,
       SUM(l.amount_minor) - SUM(r.amount_minor) AS net_minor,
       SUM(DISTINCT l.amount_minor) AS distinct_gross_minor
FROM lines l JOIN refunds r ON r.order_id = l.order_id
WHERE l.order_id = 'O1' AND r.posted_at < :end
""", PARAMS).fetchone())

# This check spans only the fully authorized, tiny fixture. Missing parent
# timestamps cannot be used to infer that a detached record belongs to September.
unallocated = [dict(r) for r in db.execute("""
SELECT 'line' AS kind, l.line_id AS source_id, l.order_id, l.currency,
       l.amount_minor, 'missing order header; cohort unknown' AS reason
FROM lines l LEFT JOIN orders o ON o.order_id = l.order_id
WHERE o.order_id IS NULL
UNION ALL
SELECT 'refund', r.refund_id, r.order_id, r.currency, r.amount_minor,
       'missing order header; cohort unknown'
FROM refunds r LEFT JOIN orders o ON o.order_id = r.order_id
WHERE o.order_id IS NULL AND r.posted_at < :end
ORDER BY kind, source_id
""", PARAMS)]

# Independent hand-calculated expectations, not a second copy of the rollup.
expected_amounts = {
    'O1': (3000, 500, 2500), 'O2': (4000, 0, 4000),
    'O3': (None, 100, None), 'O4': (5000, 500, 4500),
    'O5': (2500, None, None), 'O6': (None, 0, None),
    'O7': (700, None, None), 'O8': (None, None, None),
    'O9': (600, 0, 600),
}
assert len(per_order) == 9 == len({r['order_id'] for r in per_order})
assert {r['order_id'] for r in per_order} == set(expected_amounts)
for row in per_order:
    assert tuple(row[k] for k in ('gross_minor', 'refund_minor', 'net_minor')) \
        == expected_amounts[row['order_id']]
by_id = {r['order_id']: r for r in per_order}
assert by_id['O3']['missing_line_amounts'] == 1
assert by_id['O6']['line_rows'] == 0 and by_id['O6']['expected_lines'] == 1
assert by_id['O7']['missing_refund_amounts'] == 1
assert by_id['O2']['refund_rows'] == 0 and by_id['O2']['refunds_complete'] == 1
assert by_id['O5']['refund_rows'] == 0 and by_id['O5']['refunds_complete'] == 0
assert by_id['O8']['expected_lines'] is None
assert wrong == {'joined_rows': 4, 'gross_minor': 6000,
                 'refund_minor': 1000, 'net_minor': 5000,
                 'distinct_gross_minor': 1500}
assert len(summary) == 2
eur, usd = summary
assert eur['currency'] == 'EUR' and eur['net_total_minor'] == 4500
assert eur['gross_total_minor'] == 5000 and eur['refund_total_minor'] == 500
assert usd['currency'] == 'USD' and usd['orders'] == 8
assert usd['known_net_orders'] == 3 and usd['unknown_net_orders'] == 5
assert usd['observed_gross_components_minor'] == 12200
assert usd['observed_refund_components_minor'] == 600
assert usd['known_order_net_subtotal_minor'] == 7100
assert all(usd[k] is None for k in
           ('gross_total_minor', 'refund_total_minor', 'net_total_minor'))
assert [(r['source_id'], r['amount_minor']) for r in unallocated] \
       == [('LX', 777), ('RX', 111)]

blocked_write = False
try:
    db.execute("DELETE FROM orders WHERE order_id = 'O1'")
except sqlite3.DatabaseError:
    blocked_write = True
assert blocked_write and db.total_changes == setup_changes
assert db.execute("SELECT COUNT(order_id) FROM orders").fetchone()[0] == 12

columns = ['order_id', 'currency', 'line_rows', 'expected_lines',
           'missing_line_amounts', 'refund_rows', 'missing_refund_amounts',
           'gross_minor', 'refund_minor', 'net_minor']
print(json.dumps({
    'sqlite_version': sqlite3.sqlite_version,
    'parameters': PARAMS,
    'owner_expected_population': 9,
    'observed_population': len(per_order),
    'per_order_columns': columns,
    'per_order_rows': [[r[k] for k in columns] for r in per_order],
    'currency_summary': summary,
    'intentionally_wrong_raw_join_O1': wrong,
    'unallocated': unallocated,
    'fixture_write_guard_blocked_delete': blocked_write,
    'analytical_changes': db.total_changes - setup_changes,
    'assertions': 'passed',
}, indent=2))
db.close()
```

## How to interpret the result

EUR has one complete order: EUR 50.00 gross, EUR 5.00 refund and EUR 45.00 net under this owner-defined rule. USD has eight orders but only three complete net amounts: USD 71.00 is the subtotal for those three orders. The full USD net, gross and refund totals are unknown. Subtracting observed USD refund components from observed gross components would produce 116.00, but that is not a reconciled population metric and is deliberately not returned as net.

O1 independently reconciles to 30.00 minus 5.00 = 25.00. The raw child-to-child join returns four rows and a wrong net of 50.00. `SUM(DISTINCT line amount)` returns only 15.00 because the two genuine lines have the same value.

LX's USD 7.77 and RX's USD 1.11 stay individually unallocated. They are not netted or assigned to the September population. The known EUR total and USD partial subtotal must not be added together.

## Integration boundary

This example executes only the supplied fictional SQLite fixture. It does not connect to an actual reporting system, verify actual schema cardinality, read actual data, determine actual permissions or costs, establish actual source completeness, or validate another engine's syntax and behavior.

For an actual authorized report, the missing evidence includes the target engine/version, supplied schema and definition references, source/snapshot coverage, cost bounds and full query-effects review. Real nullable or noncanonical timestamps, reversals, currency mismatches and overflow/decimal limits need explicit handling derived from that source contract; the fixture does not claim to exercise those branches. If unit mismatches exist, retain the original-currency rows in reconciliation instead of silently dropping them from observed components. No live query should be run solely to turn this fictional test into an integration claim.
