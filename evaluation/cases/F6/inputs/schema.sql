CREATE TABLE orders (order_id TEXT PRIMARY KEY, channel TEXT NOT NULL, status TEXT NOT NULL, ordered_at TEXT NOT NULL, items_complete INTEGER NOT NULL CHECK (items_complete IN (0,1)));
CREATE TABLE line_items (line_id TEXT PRIMARY KEY, order_id TEXT NOT NULL, quantity INTEGER NOT NULL, unit_minor INTEGER NOT NULL);
CREATE TABLE refunds (refund_id TEXT PRIMARY KEY, order_id TEXT NOT NULL, event_at TEXT NOT NULL, amount_minor INTEGER NOT NULL);
