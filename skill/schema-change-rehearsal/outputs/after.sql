-- Inspection export; replay only into a new empty disposable database.
PRAGMA foreign_keys = OFF;
PRAGMA user_version = 2;
BEGIN TRANSACTION;
CREATE TABLE item_note (
    id TEXT NOT NULL PRIMARY KEY,
    item_id TEXT NOT NULL REFERENCES work_item(id) ON DELETE RESTRICT,
    body TEXT NOT NULL
);
INSERT INTO "item_note" VALUES('N-001','W-001','Keep the worked example.');
INSERT INTO "item_note" VALUES('N-002','W-001','Check the Unicode heading.');
INSERT INTO "item_note" VALUES('N-003','W-002','Estimate has not been supplied.');
INSERT INTO "item_note" VALUES('N-004','W-010','Zero means no remaining effort, not unknown.');
INSERT INTO "item_note" VALUES('N-005','W-900','Archived notes remain attached.');
CREATE TABLE owner (
    id TEXT NOT NULL PRIMARY KEY,
    label TEXT NOT NULL
);
INSERT INTO "owner" VALUES('team-01','Reader tools');
INSERT INTO "owner" VALUES('team-02','Export tools');
CREATE TABLE work_estimate (
    item_id TEXT NOT NULL PRIMARY KEY REFERENCES work_item(id) ON DELETE RESTRICT,
    estimated_minutes INTEGER NOT NULL
        CHECK (typeof(estimated_minutes) = 'integer' AND estimated_minutes >= 0),
    original_text TEXT NOT NULL
);
INSERT INTO "work_estimate" VALUES('W-001',90,'1h 30m');
INSERT INTO "work_estimate" VALUES('W-010',0,'0m');
INSERT INTO "work_estimate" VALUES('W-041',420,'1d');
INSERT INTO "work_estimate" VALUES('W-900',120,'2h');
CREATE TABLE work_item (
    id TEXT NOT NULL PRIMARY KEY,
    title TEXT NOT NULL,
    owner_id TEXT REFERENCES owner(id) ON DELETE RESTRICT,
    archived_at TEXT
);
INSERT INTO "work_item" VALUES('W-001','Parser documentation','team-01',NULL);
INSERT INTO "work_item" VALUES('W-002','Export checksum',NULL,NULL);
INSERT INTO "work_item" VALUES('W-010','Retry indicator','team-02',NULL);
INSERT INTO "work_item" VALUES('W-041','Batch preview','team-01',NULL);
INSERT INTO "work_item" VALUES('W-900','Legacy console — retained',NULL,'2026-09-15T10:00:00Z');
CREATE INDEX work_item_owner ON work_item(owner_id);
CREATE INDEX item_note_item ON item_note(item_id);
COMMIT;
PRAGMA foreign_keys = ON;
PRAGMA foreign_key_check;
PRAGMA integrity_check;
