-- INVENTED schema-shaped fixture ONLY; not the real #21 SQLite DDL.
-- Design-level compatibility for documented table and key names.
PRAGMA foreign_keys=ON;

CREATE TABLE source_snapshots(
 snapshot_id TEXT PRIMARY KEY, source_sha256 TEXT NOT NULL
);
CREATE TABLE files(
 record_id TEXT PRIMARY KEY,
 snapshot_id TEXT NOT NULL REFERENCES source_snapshots(snapshot_id),
 relative_path TEXT NOT NULL UNIQUE,
 name TEXT NOT NULL,
 extension TEXT NOT NULL,
 size_bytes INTEGER NOT NULL
);
CREATE TABLE works(
 work_id TEXT PRIMARY KEY, authority_title TEXT
);
CREATE TABLE authors(
 author_id TEXT PRIMARY KEY, authority_name TEXT
);
CREATE TABLE editions(
 record_id TEXT PRIMARY KEY REFERENCES files(record_id),
 work_id TEXT REFERENCES works(work_id),
 observed_title TEXT,
 observed_author TEXT
);
CREATE TABLE evidence(
 evidence_id TEXT PRIMARY KEY, source_url TEXT NOT NULL
);
CREATE TABLE rights_layer_status(
 record_id TEXT PRIMARY KEY REFERENCES files(record_id),
 commercial_class TEXT NOT NULL DEFAULT 'E_UNCERTAIN_MANUAL_REVIEW'
);
CREATE TABLE author_file_leads(
 record_id TEXT REFERENCES files(record_id),
 proposed_author TEXT
);
CREATE TABLE missing_required_fields(
 record_id TEXT REFERENCES files(record_id),
 field_name TEXT
);
CREATE TABLE research_notes(
 record_id TEXT REFERENCES files(record_id),
 note TEXT
);
CREATE TABLE sample_assessment(
 record_id TEXT REFERENCES files(record_id),
 stratum TEXT
);
