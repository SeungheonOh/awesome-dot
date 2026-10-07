-- Juniper Relay RX-2026-09-30: one row per observed eligible workload.
-- SQLite 3.40+, read-only; UTC dates/timestamps and signed integer cents.
-- Source definitions: inputs/schema.sql and inputs/source-policy.md.
-- The workload interval is half-open; posting and event-effective cutoffs
-- include equality. Event activity is not restricted to the start interval.
-- Each event stream is reduced before joining. Wrong-currency events do not
-- allocate, but invalidate that workload's corresponding stream total.
-- Only complete coverage with no allocated nulls or currency defects supports
-- a total, including a known zero. Feed/population control gaps are never
-- distributed to workloads, and absent workloads are never manufactured.
WITH population AS (
    SELECT workload_id, tenant, currency, base_cents
    FROM workloads
    WHERE status = 'active'
      AND started_on >= :report_start
      AND started_on < :report_end
      AND posted_at <= :as_of
), eligible_events AS (
    SELECT 'charges' AS stream, workload_id, currency, amount_cents
    FROM charges
    WHERE status = 'final'
      AND effective_on <= substr(:as_of, 1, 10)
      AND posted_at <= :as_of
    UNION ALL
    SELECT 'credits' AS stream, workload_id, currency, amount_cents
    FROM credits
    WHERE status = 'final'
      AND effective_on <= substr(:as_of, 1, 10)
      AND posted_at <= :as_of
), stream_rollup AS (
    SELECT p.workload_id, e.stream,
           COUNT(CASE WHEN e.currency = p.currency THEN 1 END) AS event_rows,
           COUNT(CASE WHEN e.currency = p.currency
                       AND e.amount_cents IS NULL THEN 1 END) AS null_rows,
           COALESCE(SUM(CASE WHEN e.currency = p.currency
                             THEN e.amount_cents END), 0) AS known_subtotal_cents,
           COUNT(CASE WHEN e.currency <> p.currency THEN 1 END) AS mismatch_rows
    FROM population AS p
    JOIN eligible_events AS e ON e.workload_id = p.workload_id
    GROUP BY p.workload_id, e.stream
), per_workload AS (
    SELECT p.workload_id, p.tenant, p.currency, p.base_cents,
           COALESCE(ch.event_rows, 0) AS charge_rows,
           COALESCE(ch.null_rows, 0) AS charge_null_rows,
           COALESCE(ch.known_subtotal_cents, 0) AS charge_known_subtotal_cents,
           CASE WHEN cc.state = 'complete'
                     AND COALESCE(ch.null_rows, 0) = 0
                     AND COALESCE(ch.mismatch_rows, 0) = 0
                THEN 1 ELSE 0 END AS charge_total_known,
           COALESCE(cr.event_rows, 0) AS credit_rows,
           COALESCE(cr.null_rows, 0) AS credit_null_rows,
           COALESCE(cr.known_subtotal_cents, 0) AS credit_known_subtotal_cents,
           CASE WHEN rc.state = 'complete'
                     AND COALESCE(cr.null_rows, 0) = 0
                     AND COALESCE(cr.mismatch_rows, 0) = 0
                THEN 1 ELSE 0 END AS credit_total_known
    FROM population AS p
    LEFT JOIN stream_rollup AS ch
      ON ch.workload_id = p.workload_id AND ch.stream = 'charges'
    LEFT JOIN stream_rollup AS cr
      ON cr.workload_id = p.workload_id AND cr.stream = 'credits'
    LEFT JOIN coverage AS cc
      ON cc.workload_id = p.workload_id AND cc.stream = 'charges'
    LEFT JOIN coverage AS rc
      ON rc.workload_id = p.workload_id AND rc.stream = 'credits'
)
SELECT workload_id, tenant, currency, base_cents,
       charge_rows, charge_null_rows, charge_known_subtotal_cents,
       CASE WHEN charge_total_known = 1
            THEN charge_known_subtotal_cents END AS charge_total_cents,
       charge_total_known,
       credit_rows, credit_null_rows, credit_known_subtotal_cents,
       CASE WHEN credit_total_known = 1
            THEN credit_known_subtotal_cents END AS credit_total_cents,
       credit_total_known,
       CASE WHEN charge_total_known = 1 AND credit_total_known = 1
            THEN base_cents + charge_known_subtotal_cents
                            + credit_known_subtotal_cents END AS net_cents
FROM per_workload
ORDER BY workload_id;
