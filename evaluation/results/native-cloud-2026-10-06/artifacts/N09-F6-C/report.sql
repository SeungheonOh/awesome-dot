WITH
cohort AS (
    SELECT order_id, channel, items_complete
    FROM orders
    WHERE status IN ('settled', 'shipped')
      AND ordered_at >= :period_start
      AND ordered_at < :period_end
),
line_totals AS (
    SELECT l.order_id,
           COUNT(*) AS line_row_count,
           SUM(l.quantity * l.unit_minor) AS known_gross_minor
    FROM line_items AS l
    JOIN cohort AS c ON c.order_id = l.order_id
    GROUP BY l.order_id
),
refund_totals AS (
    SELECT r.order_id, SUM(r.amount_minor) AS refund_minor
    FROM refunds AS r
    JOIN cohort AS c ON c.order_id = r.order_id
    WHERE r.amount_minor > 0
      AND r.event_at <= :as_of
    GROUP BY r.order_id
),
channel_totals AS (
    SELECT c.channel,
           COUNT(*) AS order_count,
           SUM(COALESCE(l.line_row_count, 0)) AS line_row_count,
           SUM(COALESCE(l.known_gross_minor, 0)) AS known_gross_minor,
           SUM(CASE WHEN c.items_complete = 0 THEN 1 ELSE 0 END)
               AS incomplete_order_count,
           SUM(CASE WHEN c.items_complete = 1
                         AND COALESCE(l.known_gross_minor, 0) = 0
                    THEN 1 ELSE 0 END) AS complete_zero_order_count,
           SUM(COALESCE(r.refund_minor, 0)) AS refund_minor
    FROM cohort AS c
    LEFT JOIN line_totals AS l ON l.order_id = c.order_id
    LEFT JOIN refund_totals AS r ON r.order_id = c.order_id
    GROUP BY c.channel
),
report_rows AS (
    SELECT channel,
           order_count,
           line_row_count,
           known_gross_minor,
           incomplete_order_count,
           complete_zero_order_count,
           CASE WHEN incomplete_order_count > 0 THEN NULL
                ELSE known_gross_minor END AS gross_minor,
           refund_minor,
           CASE WHEN incomplete_order_count > 0 THEN NULL
                ELSE known_gross_minor - refund_minor END AS net_minor,
           0 AS unallocated_refund_count
    FROM channel_totals
    UNION ALL
    SELECT '__unallocated__',
           0, 0, 0, 0, 0, 0,
           COALESCE(SUM(r.amount_minor), 0),
           NULL,
           COUNT(*)
    FROM refunds AS r
    WHERE r.amount_minor > 0
      AND r.event_at <= :as_of
      AND NOT EXISTS (
          SELECT 1 FROM orders AS o WHERE o.order_id = r.order_id
      )
)
SELECT channel,
       order_count,
       line_row_count,
       known_gross_minor,
       incomplete_order_count,
       complete_zero_order_count,
       gross_minor,
       refund_minor,
       net_minor,
       unallocated_refund_count
FROM report_rows
ORDER BY channel COLLATE BINARY ASC;
