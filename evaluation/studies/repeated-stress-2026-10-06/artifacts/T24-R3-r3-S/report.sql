-- Invoice cohort, with each event relation independently reduced to one row per line.
WITH eligible_lines AS (
    SELECT
        l.line_id,
        i.invoice_id,
        substr(i.invoice_date, 1, 7) AS report_month,
        c.region,
        p.family,
        i.currency,
        l.quantity AS billed_units,
        l.quantity * l.unit_price_cents AS gross_cents
    FROM invoices AS i
    JOIN invoice_lines AS l ON l.invoice_id = i.invoice_id
    JOIN customers AS c ON c.customer_id = i.customer_id
    JOIN products AS p ON p.product_id = l.product_id
    WHERE i.status = 'issued'
      AND i.invoice_date >= :report_start
      AND i.invoice_date < :report_end
      AND i.posted_at <= :as_of
), adjustment_totals AS (
    SELECT line_id, sum(amount_cents) AS adjustment_cents
    FROM adjustments
    WHERE status = 'approved'
      AND effective_date <= substr(:as_of, 1, 10)
      AND posted_at <= :as_of
    GROUP BY line_id
), receipt_totals AS (
    SELECT line_id, sum(amount_cents) AS received_cents
    FROM receipts
    WHERE status = 'settled'
      AND effective_date <= substr(:as_of, 1, 10)
      AND posted_at <= :as_of
    GROUP BY line_id
), fulfillment_totals AS (
    SELECT line_id, sum(quantity) AS fulfilled_units
    FROM fulfillments
    WHERE status = 'posted'
      AND effective_date <= substr(:as_of, 1, 10)
      AND posted_at <= :as_of
    GROUP BY line_id
), reconciled_lines AS (
    SELECT
        l.*,
        coalesce(a.adjustment_cents, 0) AS adjustment_cents,
        coalesce(r.received_cents, 0) AS received_cents,
        coalesce(f.fulfilled_units, 0) AS fulfilled_units
    FROM eligible_lines AS l
    LEFT JOIN adjustment_totals AS a ON a.line_id = l.line_id
    LEFT JOIN receipt_totals AS r ON r.line_id = l.line_id
    LEFT JOIN fulfillment_totals AS f ON f.line_id = l.line_id
)
SELECT
    report_month,
    region,
    family,
    currency,
    count(*) AS line_count,
    count(DISTINCT invoice_id) AS invoice_count,
    sum(billed_units) AS billed_units,
    sum(gross_cents) AS gross_cents,
    sum(adjustment_cents) AS adjustment_cents,
    sum(gross_cents + adjustment_cents) AS net_cents,
    sum(received_cents) AS received_cents,
    sum(gross_cents + adjustment_cents - received_cents) AS balance_cents,
    sum(fulfilled_units) AS fulfilled_units
FROM reconciled_lines
GROUP BY report_month, region, family, currency;
