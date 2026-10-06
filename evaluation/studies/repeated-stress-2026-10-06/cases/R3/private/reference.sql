WITH eligible AS (
 SELECT l.*, i.invoice_date, i.currency, c.region, p.family
 FROM invoice_lines l JOIN invoices i ON i.invoice_id=l.invoice_id
 JOIN customers c ON c.customer_id=i.customer_id
 JOIN products p ON p.product_id=l.product_id
 WHERE i.status='issued' AND i.invoice_date>=:report_start AND i.invoice_date<:report_end AND i.posted_at<=:as_of
), a AS (
 SELECT line_id,SUM(amount_cents) AS amount FROM adjustments
 WHERE status='approved' AND effective_date<=substr(:as_of,1,10) AND posted_at<=:as_of GROUP BY line_id
), r AS (
 SELECT line_id,SUM(amount_cents) AS amount FROM receipts
 WHERE status='settled' AND effective_date<=substr(:as_of,1,10) AND posted_at<=:as_of GROUP BY line_id
), f AS (
 SELECT line_id,SUM(quantity) AS units FROM fulfillments
 WHERE status='posted' AND effective_date<=substr(:as_of,1,10) AND posted_at<=:as_of GROUP BY line_id
)
SELECT substr(e.invoice_date,1,7) report_month,e.region,e.family,e.currency,
 COUNT(*) line_count,COUNT(DISTINCT e.invoice_id) invoice_count,SUM(e.quantity) billed_units,
 SUM(e.quantity*e.unit_price_cents) gross_cents,SUM(COALESCE(a.amount,0)) adjustment_cents,
 SUM(e.quantity*e.unit_price_cents+COALESCE(a.amount,0)) net_cents,
 SUM(COALESCE(r.amount,0)) received_cents,
 SUM(e.quantity*e.unit_price_cents+COALESCE(a.amount,0)-COALESCE(r.amount,0)) balance_cents,
 SUM(COALESCE(f.units,0)) fulfilled_units
FROM eligible e LEFT JOIN a ON a.line_id=e.line_id LEFT JOIN r ON r.line_id=e.line_id LEFT JOIN f ON f.line_id=e.line_id
GROUP BY substr(e.invoice_date,1,7),e.region,e.family,e.currency;
