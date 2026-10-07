# Captured fictional execution

The single Python block in [the worked example](fictional-example.md) was extracted unchanged and executed with the standard-library `sqlite3` module. This output was captured from that run; it is not a proposed result. Every assertion in the block passed.

Executed scope: create and populate one fresh in-memory fictional database; run the complete parameterized report, per-order reconciliation, wrong-join control and unmatched-key check; then verify that a write attempt is rejected and analytical data changes remain zero. The write-guard test targets only this disposable fictional connection.

Unrun scope: actual-source access, production data, other SQL dialects, source-system completeness, production permissions, live cost/plan checks and integration behavior. No network, package installation or external data-source connection was used.

Amounts below are integer minor units. JSON `null` means unknown, not zero. The USD known-order subtotal is not the full USD total. There is no cross-currency total.

```json
{
  "sqlite_version": "3.53.1",
  "parameters": {
    "start": "2026-09-01T00:00:00Z",
    "end": "2026-10-01T00:00:00Z"
  },
  "owner_expected_population": 9,
  "observed_population": 9,
  "per_order_columns": [
    "order_id",
    "currency",
    "line_rows",
    "expected_lines",
    "missing_line_amounts",
    "refund_rows",
    "missing_refund_amounts",
    "gross_minor",
    "refund_minor",
    "net_minor"
  ],
  "per_order_rows": [
    [
      "O1",
      "USD",
      2,
      2,
      0,
      2,
      0,
      3000,
      500,
      2500
    ],
    [
      "O2",
      "USD",
      1,
      1,
      0,
      0,
      0,
      4000,
      0,
      4000
    ],
    [
      "O3",
      "USD",
      2,
      2,
      1,
      1,
      0,
      null,
      100,
      null
    ],
    [
      "O4",
      "EUR",
      1,
      1,
      0,
      1,
      0,
      5000,
      500,
      4500
    ],
    [
      "O5",
      "USD",
      1,
      1,
      0,
      0,
      0,
      2500,
      null,
      null
    ],
    [
      "O6",
      "USD",
      0,
      1,
      0,
      0,
      0,
      null,
      0,
      null
    ],
    [
      "O7",
      "USD",
      1,
      1,
      0,
      1,
      1,
      700,
      null,
      null
    ],
    [
      "O8",
      "USD",
      1,
      null,
      0,
      0,
      0,
      null,
      null,
      null
    ],
    [
      "O9",
      "USD",
      1,
      1,
      0,
      0,
      0,
      600,
      0,
      600
    ]
  ],
  "currency_summary": [
    {
      "currency": "EUR",
      "orders": 1,
      "known_net_orders": 1,
      "unknown_net_orders": 0,
      "observed_gross_components_minor": 5000,
      "observed_refund_components_minor": 500,
      "gross_total_minor": 5000,
      "refund_total_minor": 500,
      "known_order_net_subtotal_minor": 4500,
      "net_total_minor": 4500
    },
    {
      "currency": "USD",
      "orders": 8,
      "known_net_orders": 3,
      "unknown_net_orders": 5,
      "observed_gross_components_minor": 12200,
      "observed_refund_components_minor": 600,
      "gross_total_minor": null,
      "refund_total_minor": null,
      "known_order_net_subtotal_minor": 7100,
      "net_total_minor": null
    }
  ],
  "intentionally_wrong_raw_join_O1": {
    "joined_rows": 4,
    "gross_minor": 6000,
    "refund_minor": 1000,
    "net_minor": 5000,
    "distinct_gross_minor": 1500
  },
  "unallocated": [
    {
      "kind": "line",
      "source_id": "LX",
      "order_id": "MISSING",
      "currency": "USD",
      "amount_minor": 777,
      "reason": "missing order header; cohort unknown"
    },
    {
      "kind": "refund",
      "source_id": "RX",
      "order_id": "MISSING",
      "currency": "USD",
      "amount_minor": 111,
      "reason": "missing order header; cohort unknown"
    }
  ],
  "fixture_write_guard_blocked_delete": true,
  "analytical_changes": 0,
  "assertions": "passed"
}
```
