-- Observed eligible workloads; independent event streams are aggregated before joining.
-- Coverage certifies completeness only for its individual workload/stream.
WITH
cohort AS (
    SELECT workload_id, tenant, currency, base_cents
    FROM workloads
    WHERE status = 'active'
      AND started_on >= :report_start
      AND started_on < :report_end
      AND posted_at <= :as_of
),
eligible_events AS (
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
),
event_summaries AS (
    SELECT w.workload_id, e.stream,
           sum(CASE WHEN e.currency = w.currency THEN 1 ELSE 0 END) AS allocated_rows,
           sum(CASE WHEN e.currency = w.currency AND e.amount_cents IS NULL
                    THEN 1 ELSE 0 END) AS null_rows,
           sum(CASE WHEN e.currency = w.currency
                    THEN coalesce(e.amount_cents, 0) ELSE 0 END) AS known_subtotal_cents,
           sum(CASE WHEN e.currency <> w.currency THEN 1 ELSE 0 END) AS mismatch_rows
    FROM cohort AS w
    JOIN eligible_events AS e ON e.workload_id = w.workload_id
    GROUP BY w.workload_id, e.stream
),
measures AS (
    SELECT w.workload_id, w.tenant, w.currency, w.base_cents,
           coalesce(ch.allocated_rows, 0) AS charge_rows,
           coalesce(ch.null_rows, 0) AS charge_null_rows,
           coalesce(ch.known_subtotal_cents, 0) AS charge_known_subtotal_cents,
           CASE WHEN ch_coverage.state = 'complete'
                     AND coalesce(ch.null_rows, 0) = 0
                     AND coalesce(ch.mismatch_rows, 0) = 0
                THEN 1 ELSE 0 END AS charge_total_known,
           coalesce(cr.allocated_rows, 0) AS credit_rows,
           coalesce(cr.null_rows, 0) AS credit_null_rows,
           coalesce(cr.known_subtotal_cents, 0) AS credit_known_subtotal_cents,
           CASE WHEN cr_coverage.state = 'complete'
                     AND coalesce(cr.null_rows, 0) = 0
                     AND coalesce(cr.mismatch_rows, 0) = 0
                THEN 1 ELSE 0 END AS credit_total_known
    FROM cohort AS w
    LEFT JOIN event_summaries AS ch
      ON ch.workload_id = w.workload_id AND ch.stream = 'charges'
    LEFT JOIN event_summaries AS cr
      ON cr.workload_id = w.workload_id AND cr.stream = 'credits'
    LEFT JOIN coverage AS ch_coverage
      ON ch_coverage.workload_id = w.workload_id AND ch_coverage.stream = 'charges'
    LEFT JOIN coverage AS cr_coverage
      ON cr_coverage.workload_id = w.workload_id AND cr_coverage.stream = 'credits'
)
SELECT workload_id, tenant, currency, base_cents,
       charge_rows, charge_null_rows, charge_known_subtotal_cents,
       CASE WHEN charge_total_known = 1
            THEN charge_known_subtotal_cents ELSE NULL END AS charge_total_cents,
       charge_total_known,
       credit_rows, credit_null_rows, credit_known_subtotal_cents,
       CASE WHEN credit_total_known = 1
            THEN credit_known_subtotal_cents ELSE NULL END AS credit_total_cents,
       credit_total_known,
       CASE WHEN charge_total_known = 1 AND credit_total_known = 1
            THEN base_cents + charge_known_subtotal_cents + credit_known_subtotal_cents
            ELSE NULL END AS net_cents
FROM measures
ORDER BY workload_id;
