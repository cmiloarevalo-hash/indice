-- H5 REAL-SHAPE SYNTHETIC CONTRACT.
-- Structural fixture only: table/column/PK/FK shapes observed from an
-- authorized PRAGMA read-only inspection of the accepted SQLite #21.
-- ZERO real rows, titles, paths, identities, copyright claims, or book data.
PRAGMA foreign_keys=ON;

CREATE TABLE source_snapshots (
  snapshot_id TEXT PRIMARY KEY,
  source_commit TEXT NOT NULL,
  sha256 TEXT NOT NULL,
  record_count INTEGER NOT NULL,
  created_utc TEXT NOT NULL,
  original_modified INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE files (
  record_id TEXT PRIMARY KEY,
  source_row INTEGER NOT NULL UNIQUE,
  snapshot_id TEXT NOT NULL REFERENCES source_snapshots(snapshot_id),
  relative_path TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  extension TEXT NOT NULL,
  size_bytes INTEGER NOT NULL,
  directory_relative_path TEXT NOT NULL,
  actual_stat_status TEXT NOT NULL DEFAULT 'NOT_AVAILABLE'
);
CREATE INDEX idx_file_name ON files(name);

CREATE TABLE works (
  work_id TEXT PRIMARY KEY,
  authority_title TEXT NOT NULL,
  authority_url TEXT,
  confidence TEXT NOT NULL,
  file_identity_verified INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE authors (
  author_key TEXT PRIMARY KEY,
  display_name TEXT,
  death_date TEXT,
  death_year TEXT,
  authority_url TEXT,
  status TEXT NOT NULL
);

CREATE TABLE editions (
  edition_id TEXT PRIMARY KEY,
  record_id TEXT NOT NULL UNIQUE REFERENCES files(record_id),
  work_id TEXT REFERENCES works(work_id),
  observed_title TEXT,
  observed_author TEXT,
  observed_publisher TEXT,
  observed_language TEXT,
  observed_date TEXT,
  observed_isbn TEXT,
  observed_identifier TEXT,
  translator TEXT,
  edition_year TEXT,
  embedded_rights_statement TEXT,
  metadata_status TEXT NOT NULL,
  edition_license_verified INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX idx_edition_work ON editions(work_id);

CREATE TABLE evidence (
  evidence_id TEXT PRIMARY KEY,
  layer TEXT NOT NULL,
  entity_key TEXT,
  claim TEXT,
  source_url TEXT,
  accessed_utc TEXT,
  source_tier TEXT,
  concrete_file_proved TEXT NOT NULL
);

CREATE TABLE rights_layer_status (
  record_id TEXT PRIMARY KEY REFERENCES files(record_id),
  underlying_status TEXT NOT NULL,
  edition_status TEXT NOT NULL,
  derivative_status TEXT NOT NULL,
  territories_status TEXT NOT NULL,
  commercial_class TEXT NOT NULL,
  commercial_royalty_free_confirmed INTEGER NOT NULL DEFAULT 0,
  underlying_conditional_year TEXT,
  edition_release_year TEXT,
  combined_release_year TEXT,
  jurisdiction TEXT NOT NULL DEFAULT 'CL_REQUIRES_REVIEW',
  certainty TEXT NOT NULL,
  blocking_reason TEXT NOT NULL
);

CREATE TABLE author_file_leads (
  record_id TEXT PRIMARY KEY REFERENCES files(record_id),
  author_key TEXT,
  proposed_author TEXT,
  match_method TEXT,
  source_url TEXT,
  status TEXT NOT NULL
);

CREATE TABLE missing_required_fields (
  record_id TEXT PRIMARY KEY REFERENCES files(record_id),
  title_for_research_available INTEGER NOT NULL,
  author_for_research_available INTEGER NOT NULL,
  author_identity_verified INTEGER NOT NULL,
  edition_identity_verified INTEGER NOT NULL,
  commercial_permission_verified INTEGER NOT NULL,
  missing_json TEXT NOT NULL,
  missing_count INTEGER NOT NULL
);

CREATE TABLE research_notes (
  note_id INTEGER PRIMARY KEY,
  record_id TEXT REFERENCES files(record_id),
  note_type TEXT NOT NULL,
  status TEXT NOT NULL,
  summary TEXT NOT NULL,
  reference_url TEXT
);

CREATE TABLE sample_assessment (
  record_id TEXT PRIMARY KEY REFERENCES files(record_id),
  stratum TEXT NOT NULL,
  title_author_startable INTEGER NOT NULL,
  combined_file_use_sufficient INTEGER NOT NULL,
  missing_tested TEXT NOT NULL,
  assessment TEXT NOT NULL
);
