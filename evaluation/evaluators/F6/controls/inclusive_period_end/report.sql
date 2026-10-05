WITH
item_totals AS (
 SELECT order_id, COUNT(*) AS n, SUM(quantity * unit_minor) AS amount
 FROM line_items GROUP BY order_id
),
refund_totals AS (
 SELECT order_id, SUM(amount_minor) AS amount
 FROM refunds WHERE event_at <= :as_of GROUP BY order_id
),
cohort AS (
 SELECT o.order_id, o.channel, o.items_complete,
        COALESCE(i.n,0) AS line_n, COALESCE(i.amount,0) AS line_amount,
        COALESCE(r.amount,0) AS refund_amount
 FROM orders o
 LEFT JOIN item_totals i ON i.order_id = o.order_id
 LEFT JOIN refund_totals r ON r.order_id = o.order_id
 WHERE o.status IN ('settled','shipped')
   AND o.ordered_at >= :period_start AND o.ordered_at <= :period_end
),
channel_report AS (
 SELECT channel, COUNT(*) AS order_count, SUM(line_n) AS line_row_count,
        SUM(line_amount) AS known_gross_minor,
        SUM(CASE WHEN items_complete=0 THEN 1 ELSE 0 END) AS incomplete_order_count,
        SUM(CASE WHEN items_complete=1 AND line_amount=0 THEN 1 ELSE 0 END) AS complete_zero_order_count,
        CASE WHEN MIN(items_complete)=1 THEN SUM(line_amount) END AS gross_minor,
        SUM(refund_amount) AS refund_minor,
        CASE WHEN MIN(items_complete)=1 THEN SUM(line_amount)-SUM(refund_amount) END AS net_minor,
        0 AS unallocated_refund_count
 FROM cohort GROUP BY channel
),
unallocated AS (
 SELECT '__unallocated__' AS channel, 0 AS order_count, 0 AS line_row_count,
        0 AS known_gross_minor, 0 AS incomplete_order_count, 0 AS complete_zero_order_count,
        0 AS gross_minor, COALESCE(SUM(r.amount_minor),0) AS refund_minor,
        NULL AS net_minor, COUNT(*) AS unallocated_refund_count
 FROM refunds r
 WHERE r.event_at <= :as_of AND NOT EXISTS (SELECT 1 FROM orders o WHERE o.order_id=r.order_id)
)
SELECT * FROM channel_report UNION ALL SELECT * FROM unallocated ORDER BY channel COLLATE BINARY;
