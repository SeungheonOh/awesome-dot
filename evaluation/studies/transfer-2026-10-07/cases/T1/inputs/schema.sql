CREATE TABLE workloads(workload_id TEXT PRIMARY KEY, tenant TEXT NOT NULL, currency TEXT NOT NULL, started_on TEXT NOT NULL, posted_at TEXT NOT NULL, status TEXT NOT NULL, base_cents INTEGER NOT NULL);
CREATE TABLE charges(event_id TEXT PRIMARY KEY, workload_id TEXT, currency TEXT NOT NULL, amount_cents INTEGER, effective_on TEXT NOT NULL, posted_at TEXT NOT NULL, status TEXT NOT NULL);
CREATE TABLE credits(event_id TEXT PRIMARY KEY, workload_id TEXT, currency TEXT NOT NULL, amount_cents INTEGER, effective_on TEXT NOT NULL, posted_at TEXT NOT NULL, status TEXT NOT NULL);
CREATE TABLE coverage(workload_id TEXT NOT NULL, stream TEXT NOT NULL, state TEXT NOT NULL, PRIMARY KEY(workload_id, stream));
CREATE TABLE population_controls(tenant TEXT NOT NULL, currency TEXT NOT NULL, expected_workloads INTEGER NOT NULL, base_cents INTEGER NOT NULL, extraction_state TEXT NOT NULL, PRIMARY KEY(tenant,currency));
CREATE TABLE feed_controls(stream TEXT NOT NULL, currency TEXT NOT NULL, eligible_rows INTEGER NOT NULL, null_amount_rows INTEGER NOT NULL, known_subtotal_cents INTEGER NOT NULL, PRIMARY KEY(stream,currency));
