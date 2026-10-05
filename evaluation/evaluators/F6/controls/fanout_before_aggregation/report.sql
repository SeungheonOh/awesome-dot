SELECT o.channel, COUNT(*) AS order_count, COUNT(i.line_id) AS line_row_count,
SUM(i.quantity*i.unit_minor) AS known_gross_minor,
SUM(CASE WHEN o.items_complete=0 THEN 1 ELSE 0 END) AS incomplete_order_count,
0 AS complete_zero_order_count, SUM(i.quantity*i.unit_minor) AS gross_minor,
SUM(r.amount_minor) AS refund_minor, SUM(i.quantity*i.unit_minor)-SUM(r.amount_minor) AS net_minor,
0 AS unallocated_refund_count
FROM orders o LEFT JOIN line_items i ON i.order_id=o.order_id
LEFT JOIN refunds r ON r.order_id=o.order_id AND r.event_at<=:as_of
WHERE o.status IN ('settled','shipped') AND o.ordered_at>=:period_start AND o.ordered_at<:period_end
GROUP BY o.channel ORDER BY o.channel;
