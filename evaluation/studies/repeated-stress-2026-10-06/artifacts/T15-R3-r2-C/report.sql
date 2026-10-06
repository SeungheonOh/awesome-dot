WITH
eligible_lines AS (
    SELECT
        l.line_id,
        i.invoice_id,
        substr(i.invoice_date, 1, 7) AS report_month,
        c.region,
        p.family,
        i.currency,
        l.quantity,
        l.quantity * l.unit_price_cents AS gross_cents
    FROM invoices AS i
    JOIN invoice_lines AS l ON l.invoice_id = i.invoice_id
    JOIN customers AS c ON c.customer_id = i.customer_id
    JOIN products AS p ON p.product_id = l.product_id
    WHERE i.status = 'issued'
      AND i.invoice_date >= :report_start
      AND i.invoice_date < :report_end
      AND i.posted_at <= :as_of
),
adjustments_by_line AS (
    SELECT line_id, sum(amount_cents) AS adjustment_cents
    FROM adjustments
    WHERE status = 'approved'
      AND effective_date <= substr(:as_of, 1, 10)
      AND posted_at <= :as_of
    GROUP BY line_id
),
receipts_by_line AS (
    SELECT line_id, sum(amount_cents) AS received_cents
    FROM receipts
    WHERE status = 'settled'
      AND effective_date <= substr(:as_of, 1, 10)
      AND posted_at <= :as_of
    GROUP BY line_id
),
fulfillments_by_line AS (
    SELECT line_id, sum(quantity) AS fulfilled_units
    FROM fulfillments
    WHERE status = 'posted'
      AND effective_date <= substr(:as_of, 1, 10)
      AND posted_at <= :as_of
    GROUP BY line_id
)
SELECT
    l.report_month,
    l.region,
    l.family,
    l.currency,
    count(*) AS line_count,
    count(DISTINCT l.invoice_id) AS invoice_count,
    sum(l.quantity) AS billed_units,
    sum(l.gross_cents) AS gross_cents,
    sum(coalesce(a.adjustment_cents, 0)) AS adjustment_cents,
    sum(l.gross_cents + coalesce(a.adjustment_cents, 0)) AS net_cents,
    sum(coalesce(r.received_cents, 0)) AS received_cents,
    sum(l.gross_cents + coalesce(a.adjustment_cents, 0)
        - coalesce(r.received_cents, 0)) AS balance_cents,
    sum(coalesce(f.fulfilled_units, 0)) AS fulfilled_units
FROM eligible_lines AS l
LEFT JOIN adjustments_by_line AS a ON a.line_id = l.line_id
LEFT JOIN receipts_by_line AS r ON r.line_id = l.line_id
LEFT JOIN fulfillments_by_line AS f ON f.line_id = l.line_id
GROUP BY l.report_month, l.region, l.family, l.currency;
