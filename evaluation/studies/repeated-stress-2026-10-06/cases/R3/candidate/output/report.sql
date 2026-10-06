-- Existing report: values no longer reconcile after partial settlements and corrections.
SELECT substr(i.invoice_date,1,7) AS report_month,c.region,p.family,i.currency,
 COUNT(*) AS line_count,COUNT(i.invoice_id) AS invoice_count,SUM(l.quantity) AS billed_units,
 SUM(l.quantity*l.unit_price_cents) AS gross_cents,SUM(a.amount_cents) AS adjustment_cents,
 SUM(l.quantity*l.unit_price_cents+a.amount_cents) AS net_cents,
 SUM(r.amount_cents) AS received_cents,
 SUM(l.quantity*l.unit_price_cents+a.amount_cents-r.amount_cents) AS balance_cents,
 SUM(f.quantity) AS fulfilled_units
FROM invoices i JOIN invoice_lines l ON l.invoice_id=i.invoice_id
JOIN customers c ON c.customer_id=i.customer_id JOIN products p ON p.product_id=l.product_id
JOIN adjustments a ON a.line_id=l.line_id JOIN receipts r ON r.line_id=l.line_id
JOIN fulfillments f ON f.line_id=l.line_id
WHERE i.invoice_date>=:report_start AND i.invoice_date<:report_end
GROUP BY substr(i.invoice_date,1,7),c.region,p.family,i.currency;
