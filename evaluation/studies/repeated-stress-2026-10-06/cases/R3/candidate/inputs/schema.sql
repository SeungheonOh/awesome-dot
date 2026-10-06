
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, region TEXT NOT NULL);
CREATE TABLE products(product_id INTEGER PRIMARY KEY, family TEXT NOT NULL);
CREATE TABLE invoices(invoice_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, invoice_date TEXT NOT NULL, posted_at TEXT NOT NULL, status TEXT NOT NULL, currency TEXT NOT NULL);
CREATE TABLE invoice_lines(line_id INTEGER PRIMARY KEY, invoice_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL, unit_price_cents INTEGER NOT NULL);
CREATE TABLE adjustments(adjustment_id INTEGER PRIMARY KEY, line_id INTEGER NOT NULL, amount_cents INTEGER NOT NULL, effective_date TEXT NOT NULL, posted_at TEXT NOT NULL, status TEXT NOT NULL);
CREATE TABLE receipts(receipt_id INTEGER PRIMARY KEY, line_id INTEGER NOT NULL, amount_cents INTEGER NOT NULL, effective_date TEXT NOT NULL, posted_at TEXT NOT NULL, status TEXT NOT NULL);
CREATE TABLE fulfillments(fulfillment_id INTEGER PRIMARY KEY, line_id INTEGER NOT NULL, quantity INTEGER NOT NULL, effective_date TEXT NOT NULL, posted_at TEXT NOT NULL, status TEXT NOT NULL);
