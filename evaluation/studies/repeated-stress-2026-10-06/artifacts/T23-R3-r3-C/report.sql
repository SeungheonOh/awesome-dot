WITH
adjustments_by_line AS (
    SELECT line_id, SUM(amount_cents) AS adjustment_cents
    FROM adjustments
    WHERE status = 'approved'
      AND effective_date <= substr(:as_of, 1, 10)
      AND posted_at <= :as_of
    GROUP BY line_id
),
receipts_by_line AS (
    SELECT line_id, SUM(amount_cents) AS received_cents
    FROM receipts
    WHERE status = 'settled'
      AND effective_date <= substr(:as_of, 1, 10)
      AND posted_at <= :as_of
    GROUP BY line_id
),
fulfillments_by_line AS (
    SELECT line_id, SUM(quantity) AS fulfilled_units
    FROM fulfillments
    WHERE status = 'posted'
      AND effective_date <= substr(:as_of, 1, 10)
      AND posted_at <= :as_of
    GROUP BY line_id
),
eligible_lines AS (
    SELECT
        substr(i.invoice_date, 1, 7) AS report_month,
        c.region,
        p.family,
        i.currency,
        i.invoice_id,
        l.quantity AS billed_units,
        l.quantity * l.unit_price_cents AS gross_cents,
        COALESCE(a.adjustment_cents, 0) AS adjustment_cents,
        COALESCE(r.received_cents, 0) AS received_cents,
        COALESCE(f.fulfilled_units, 0) AS fulfilled_units
    FROM invoices AS i
    JOIN invoice_lines AS l ON l.invoice_id = i.invoice_id
    JOIN customers AS c ON c.customer_id = i.customer_id
    JOIN products AS p ON p.product_id = l.product_id
    LEFT JOIN adjustments_by_line AS a ON a.line_id = l.line_id
    LEFT JOIN receipts_by_line AS r ON r.line_id = l.line_id
    LEFT JOIN fulfillments_by_line AS f ON f.line_id = l.line_id
    WHERE i.status = 'issued'
      AND i.invoice_date >= :report_start
      AND i.invoice_date < :report_end
      AND i.posted_at <= :as_of
)
SELECT
    report_month,
    region,
    family,
    currency,
    COUNT(*) AS line_count,
    COUNT(DISTINCT invoice_id) AS invoice_count,
    SUM(billed_units) AS billed_units,
    SUM(gross_cents) AS gross_cents,
    SUM(adjustment_cents) AS adjustment_cents,
    SUM(gross_cents + adjustment_cents) AS net_cents,
    SUM(received_cents) AS received_cents,
    SUM(gross_cents + adjustment_cents - received_cents) AS balance_cents,
    SUM(fulfilled_units) AS fulfilled_units
FROM eligible_lines
GROUP BY report_month, region, family, currency;
