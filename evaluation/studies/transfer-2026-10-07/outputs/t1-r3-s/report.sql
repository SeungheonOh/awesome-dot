-- Observed-extract workload cost, signed integer cents, without currency conversion.
-- Population: active workloads started in [report_start, report_end), posted by as_of.
-- Events: final, effective by the UTC as_of date, posted by as_of (inclusive).
-- Each stream is reduced separately before joining; coverage can certify empty zero.
WITH cohort AS (
  SELECT workload_id, tenant, currency, base_cents
  FROM workloads
  WHERE status = 'active'
    AND started_on >= :report_start
    AND started_on < :report_end
    AND posted_at <= :as_of
), charge_rollup AS (
  SELECT w.workload_id,
         SUM(CASE WHEN e.currency = w.currency THEN 1 ELSE 0 END) AS allocated_rows,
         SUM(CASE WHEN e.currency = w.currency AND e.amount_cents IS NULL
                  THEN 1 ELSE 0 END) AS null_rows,
         COALESCE(SUM(CASE WHEN e.currency = w.currency THEN e.amount_cents END), 0)
           AS known_subtotal_cents,
         SUM(CASE WHEN e.currency <> w.currency THEN 1 ELSE 0 END) AS mismatched_rows
  FROM cohort AS w
  JOIN charges AS e ON e.workload_id = w.workload_id
  WHERE e.status = 'final'
    AND e.effective_on <= SUBSTR(:as_of, 1, 10)
    AND e.posted_at <= :as_of
  GROUP BY w.workload_id
), credit_rollup AS (
  SELECT w.workload_id,
         SUM(CASE WHEN e.currency = w.currency THEN 1 ELSE 0 END) AS allocated_rows,
         SUM(CASE WHEN e.currency = w.currency AND e.amount_cents IS NULL
                  THEN 1 ELSE 0 END) AS null_rows,
         COALESCE(SUM(CASE WHEN e.currency = w.currency THEN e.amount_cents END), 0)
           AS known_subtotal_cents,
         SUM(CASE WHEN e.currency <> w.currency THEN 1 ELSE 0 END) AS mismatched_rows
  FROM cohort AS w
  JOIN credits AS e ON e.workload_id = w.workload_id
  WHERE e.status = 'final'
    AND e.effective_on <= SUBSTR(:as_of, 1, 10)
    AND e.posted_at <= :as_of
  GROUP BY w.workload_id
), stream_status AS (
  SELECT w.workload_id, w.tenant, w.currency, w.base_cents,
         COALESCE(c.allocated_rows, 0) AS charge_rows,
         COALESCE(c.null_rows, 0) AS charge_null_rows,
         COALESCE(c.known_subtotal_cents, 0) AS charge_known_subtotal_cents,
         CASE WHEN cc.state = 'complete'
                    AND COALESCE(c.null_rows, 0) = 0
                    AND COALESCE(c.mismatched_rows, 0) = 0
              THEN 1 ELSE 0 END AS charge_total_known,
         COALESCE(r.allocated_rows, 0) AS credit_rows,
         COALESCE(r.null_rows, 0) AS credit_null_rows,
         COALESCE(r.known_subtotal_cents, 0) AS credit_known_subtotal_cents,
         CASE WHEN rc.state = 'complete'
                    AND COALESCE(r.null_rows, 0) = 0
                    AND COALESCE(r.mismatched_rows, 0) = 0
              THEN 1 ELSE 0 END AS credit_total_known
  FROM cohort AS w
  LEFT JOIN charge_rollup AS c ON c.workload_id = w.workload_id
  LEFT JOIN credit_rollup AS r ON r.workload_id = w.workload_id
  LEFT JOIN coverage AS cc ON cc.workload_id = w.workload_id AND cc.stream = 'charges'
  LEFT JOIN coverage AS rc ON rc.workload_id = w.workload_id AND rc.stream = 'credits'
)
SELECT workload_id, tenant, currency, base_cents,
       charge_rows, charge_null_rows, charge_known_subtotal_cents,
       CASE WHEN charge_total_known = 1 THEN charge_known_subtotal_cents END
         AS charge_total_cents,
       charge_total_known,
       credit_rows, credit_null_rows, credit_known_subtotal_cents,
       CASE WHEN credit_total_known = 1 THEN credit_known_subtotal_cents END
         AS credit_total_cents,
       credit_total_known,
       CASE WHEN charge_total_known = 1 AND credit_total_known = 1
            THEN base_cents + charge_known_subtotal_cents + credit_known_subtotal_cents END
         AS net_cents
FROM stream_status
ORDER BY workload_id;
