PRAGMA foreign_keys=ON;
PRAGMA journal_mode=DELETE;

CREATE TABLE IF NOT EXISTS schema_migrations(
  version INTEGER PRIMARY KEY,
  description TEXT NOT NULL,
  applied_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS snapshots(
  snapshot_id TEXT PRIMARY KEY,
  source_sha256 TEXT NOT NULL CHECK(length(source_sha256)=64),
  rows INTEGER NOT NULL CHECK(rows >= 0),
  imported_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS files(
  record_id TEXT PRIMARY KEY CHECK(length(record_id)=64),
  snapshot_id TEXT NOT NULL REFERENCES snapshots(snapshot_id) ON DELETE RESTRICT,
  relative_path TEXT NOT NULL UNIQUE CHECK(length(relative_path)>0),
  name TEXT NOT NULL,
  extension TEXT NOT NULL,
  size_bytes INTEGER NOT NULL CHECK(size_bytes >= 0),
  directory_relative_path TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_files_snapshot ON files(snapshot_id);
CREATE INDEX IF NOT EXISTS idx_files_name ON files(name);

CREATE TABLE IF NOT EXISTS works(
  work_id TEXT PRIMARY KEY,
  canonical_title TEXT NOT NULL,
  underlying_rights_identity TEXT NOT NULL DEFAULT 'UNRESOLVED'
);
CREATE TABLE IF NOT EXISTS editions(
  edition_id TEXT PRIMARY KEY,
  record_id TEXT NOT NULL UNIQUE REFERENCES files(record_id) ON DELETE CASCADE,
  work_id TEXT REFERENCES works(work_id) ON DELETE SET NULL,
  edition_label TEXT,
  translation_status TEXT NOT NULL DEFAULT 'UNKNOWN',
  edition_provenance_status TEXT NOT NULL DEFAULT 'UNRESOLVED'
);
CREATE INDEX IF NOT EXISTS idx_edition_work ON editions(work_id);
CREATE TABLE IF NOT EXISTS agents(
  agent_id TEXT PRIMARY KEY,
  display_name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS agent_roles(
  agent_id TEXT NOT NULL REFERENCES agents(agent_id),
  work_id TEXT REFERENCES works(work_id),
  edition_id TEXT REFERENCES editions(edition_id),
  role TEXT NOT NULL CHECK(role IN ('AUTHOR','TRANSLATOR','EDITOR','PUBLISHER','ILLUSTRATOR')),
  CHECK((work_id IS NULL) <> (edition_id IS NULL)),
  PRIMARY KEY(agent_id,role,work_id,edition_id)
);
CREATE TABLE IF NOT EXISTS evidence_sources(
  evidence_id TEXT PRIMARY KEY,
  edition_id TEXT NOT NULL REFERENCES editions(edition_id) ON DELETE CASCADE,
  layer TEXT NOT NULL CHECK(layer IN ('UNDERLYING','EDITION','DERIVATIVE','TERRITORY')),
  source_url TEXT NOT NULL CHECK(source_url LIKE 'https://%'),
  claim TEXT NOT NULL,
  evidence_status TEXT NOT NULL CHECK(evidence_status IN ('VERIFIED','UNVERIFIED')),
  observed_utc TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_evidence_edition ON evidence_sources(edition_id,layer);

CREATE TABLE IF NOT EXISTS rights_decisions(
  edition_id TEXT PRIMARY KEY REFERENCES editions(edition_id) ON DELETE CASCADE,
  underlying_status TEXT NOT NULL DEFAULT 'UNCERTAIN',
  edition_status TEXT NOT NULL DEFAULT 'UNCERTAIN',
  commercial_class TEXT NOT NULL DEFAULT 'E_UNCERTAIN_MANUAL_REVIEW'
    CHECK(commercial_class IN ('A_COMMERCIAL_REUSE_CONFIRMED','B_COMMERCIAL_WITH_CONDITIONS','C_NONCOMMERCIAL_ONLY','D_RIGHTS_RESERVED_OR_PERMISSION_REQUIRED','E_UNCERTAIN_MANUAL_REVIEW')),
  license_id TEXT NOT NULL DEFAULT 'UNKNOWN',
  derivative_adaptation_permission TEXT NOT NULL DEFAULT 'UNKNOWN'
    CHECK(derivative_adaptation_permission IN ('YES','NO','UNKNOWN')),
  allowed_territories TEXT NOT NULL DEFAULT '',
  obligations TEXT NOT NULL DEFAULT '',
  underlying_evidence_id TEXT REFERENCES evidence_sources(evidence_id),
  edition_evidence_id TEXT REFERENCES evidence_sources(evidence_id),
  derivative_evidence_id TEXT REFERENCES evidence_sources(evidence_id),
  territory_evidence_id TEXT REFERENCES evidence_sources(evidence_id),
  jurisdiction TEXT NOT NULL DEFAULT 'REVIEW_REQUIRED',
  updated_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS expiry_calculations(
  edition_id TEXT PRIMARY KEY REFERENCES editions(edition_id) ON DELETE CASCADE,
  underlying_expiry TEXT,
  edition_expiry TEXT,
  combined_expiry TEXT,
  precision TEXT NOT NULL DEFAULT 'UNKNOWN',
  basis_evidence_id TEXT REFERENCES evidence_sources(evidence_id),
  additional_rights_unresolved INTEGER NOT NULL DEFAULT 1 CHECK(additional_rights_unresolved IN (0,1))
);
CREATE TABLE IF NOT EXISTS editorial_projects(
  project_id TEXT PRIMARY KEY,
  edition_id TEXT NOT NULL REFERENCES editions(edition_id) ON DELETE RESTRICT,
  territory TEXT NOT NULL,
  state TEXT NOT NULL DEFAULT 'STOP_RIGHTS_UNVERIFIED'
    CHECK(state IN ('STOP_RIGHTS_UNVERIFIED','ELIGIBLE_FOR_EDITORIAL_WORK','SIMULATED_EDITORIAL_WORK','READY_FOR_HUMAN_PUBLICATION_REVIEW','HUMAN_PUBLICATION_AUTHORIZED_SIMULATION')),
  simulated_only INTEGER NOT NULL DEFAULT 1 CHECK(simulated_only = 1),
  content_origin TEXT NOT NULL DEFAULT 'NO_CONTENT'
    CHECK(content_origin IN ('NO_CONTENT','HUMAN_CREATED','AI_ASSISTED','AI_GENERATED')),
  ai_generated_disclosure INTEGER NOT NULL DEFAULT 0 CHECK(ai_generated_disclosure IN (0,1)),
  public_domain_differentiation TEXT NOT NULL DEFAULT 'NOT_EVALUATED',
  human_legal_approval INTEGER NOT NULL DEFAULT 0 CHECK(human_legal_approval IN (0,1)),
  editorial_qa_approval INTEGER NOT NULL DEFAULT 0 CHECK(editorial_qa_approval IN (0,1)),
  kdp_policy_preflight INTEGER NOT NULL DEFAULT 0 CHECK(kdp_policy_preflight IN (0,1)),
  human_publish_authorization INTEGER NOT NULL DEFAULT 0 CHECK(human_publish_authorization IN (0,1)),
  updated_utc TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS preflight_audit(
  audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
  project_id TEXT NOT NULL REFERENCES editorial_projects(project_id),
  checklist_json TEXT NOT NULL,
  result_state TEXT NOT NULL,
  created_utc TEXT NOT NULL
);