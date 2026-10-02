-- Original fictional work-queue fixture. No external records are used.
PRAGMA user_version = 1;
CREATE TABLE owner (
    id TEXT NOT NULL PRIMARY KEY,
    label TEXT NOT NULL
);
CREATE TABLE work_item (
    id TEXT NOT NULL PRIMARY KEY,
    title TEXT NOT NULL,
    owner_id TEXT REFERENCES owner(id) ON DELETE RESTRICT,
    estimate_text TEXT,
    archived_at TEXT
);
CREATE INDEX work_item_owner ON work_item(owner_id);
CREATE TABLE item_note (
    id TEXT NOT NULL PRIMARY KEY,
    item_id TEXT NOT NULL REFERENCES work_item(id) ON DELETE RESTRICT,
    body TEXT NOT NULL
);
CREATE INDEX item_note_item ON item_note(item_id);
INSERT INTO owner VALUES ('team-01', 'Reader tools'), ('team-02', 'Export tools');
INSERT INTO work_item VALUES
    ('W-001', 'Parser documentation', 'team-01', '1h 30m', NULL),
    ('W-002', 'Export checksum', NULL, NULL, NULL),
    ('W-010', 'Retry indicator', 'team-02', '0m', NULL),
    ('W-041', 'Batch preview', 'team-01', '1d', NULL),
    ('W-900', 'Legacy console — retained', NULL, '2h', '2026-09-15T10:00:00Z');
INSERT INTO item_note VALUES
    ('N-001', 'W-001', 'Keep the worked example.'),
    ('N-002', 'W-001', 'Check the Unicode heading.'),
    ('N-003', 'W-002', 'Estimate has not been supplied.'),
    ('N-004', 'W-010', 'Zero means no remaining effort, not unknown.'),
    ('N-005', 'W-900', 'Archived notes remain attached.');
