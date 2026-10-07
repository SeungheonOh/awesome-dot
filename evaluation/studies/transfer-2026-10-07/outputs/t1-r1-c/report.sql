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
stream_stats AS (
    SELECT
        w.workload_id,
        e.stream,
        sum(CASE WHEN e.currency = w.currency THEN 1 ELSE 0 END) AS event_rows,
        sum(CASE WHEN e.currency = w.currency AND e.amount_cents IS NULL
                 THEN 1 ELSE 0 END) AS null_rows,
        coalesce(sum(CASE WHEN e.currency = w.currency THEN e.amount_cents END), 0)
            AS known_subtotal_cents,
        max(CASE WHEN e.currency <> w.currency THEN 1 ELSE 0 END)
            AS has_currency_mismatch
    FROM cohort AS w
    JOIN eligible_events AS e ON e.workload_id = w.workload_id
    GROUP BY w.workload_id, e.stream
),
workload_totals AS (
    SELECT
        w.workload_id,
        w.tenant,
        w.currency,
        w.base_cents,
        coalesce(ch.event_rows, 0) AS charge_rows,
        coalesce(ch.null_rows, 0) AS charge_null_rows,
        coalesce(ch.known_subtotal_cents, 0) AS charge_known_subtotal_cents,
        CASE WHEN ch_cov.state = 'complete'
                   AND coalesce(ch.null_rows, 0) = 0
                   AND coalesce(ch.has_currency_mismatch, 0) = 0
             THEN 1 ELSE 0 END AS charge_total_known,
        coalesce(cr.event_rows, 0) AS credit_rows,
        coalesce(cr.null_rows, 0) AS credit_null_rows,
        coalesce(cr.known_subtotal_cents, 0) AS credit_known_subtotal_cents,
        CASE WHEN cr_cov.state = 'complete'
                   AND coalesce(cr.null_rows, 0) = 0
                   AND coalesce(cr.has_currency_mismatch, 0) = 0
             THEN 1 ELSE 0 END AS credit_total_known
    FROM cohort AS w
    LEFT JOIN stream_stats AS ch
        ON ch.workload_id = w.workload_id AND ch.stream = 'charges'
    LEFT JOIN stream_stats AS cr
        ON cr.workload_id = w.workload_id AND cr.stream = 'credits'
    LEFT JOIN coverage AS ch_cov
        ON ch_cov.workload_id = w.workload_id AND ch_cov.stream = 'charges'
    LEFT JOIN coverage AS cr_cov
        ON cr_cov.workload_id = w.workload_id AND cr_cov.stream = 'credits'
)
SELECT
    workload_id,
    tenant,
    currency,
    base_cents,
    charge_rows,
    charge_null_rows,
    charge_known_subtotal_cents,
    CASE WHEN charge_total_known = 1 THEN charge_known_subtotal_cents END
        AS charge_total_cents,
    charge_total_known,
    credit_rows,
    credit_null_rows,
    credit_known_subtotal_cents,
    CASE WHEN credit_total_known = 1 THEN credit_known_subtotal_cents END
        AS credit_total_cents,
    credit_total_known,
    CASE WHEN charge_total_known = 1 AND credit_total_known = 1
         THEN base_cents + charge_known_subtotal_cents + credit_known_subtotal_cents END
        AS net_cents
FROM workload_totals
ORDER BY workload_id;
