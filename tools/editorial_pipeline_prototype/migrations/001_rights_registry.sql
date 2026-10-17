-- Additive licensing research schema for a COPY of the accepted metadata SQLite.
-- Synthetic testing only in this work item. Existing accepted tables are not changed.
-- Each statement is standalone. No triggers; the Python migrator executes all
-- statements in one explicit transaction (never sqlite3.executescript()).

CREATE TABLE lr_sources (
 source_id TEXT PRIMARY KEY,
 institution TEXT NOT NULL,
 url TEXT NOT NULL CHECK(url LIKE 'https://%'),
 kind TEXT NOT NULL CHECK(kind IN ('IDENTITY','AUTHORITY','RIGHTS_CLAIM','LEGAL_RULE')),
 tier TEXT NOT NULL,
 accessed_utc TEXT NOT NULL,
 machine_access TEXT NOT NULL DEFAULT 'UNKNOWN',
 usage_constraints TEXT NOT NULL DEFAULT ''
);

CREATE TABLE lr_evidence (
 evidence_id TEXT PRIMARY KEY,
 record_id TEXT NOT NULL REFERENCES files(record_id) ON DELETE RESTRICT,
 source_id TEXT NOT NULL REFERENCES lr_sources(source_id) ON DELETE RESTRICT,
 scope TEXT NOT NULL CHECK(scope IN ('ORIGINAL_WORK','EDITION_FILE','TRANSLATION','ADAPTATION','TERRITORY','RIGHTSHOLDER')),
 claim_summary TEXT NOT NULL,
 evidence_status TEXT NOT NULL CHECK(evidence_status IN ('UNVERIFIED','CORROBORATED','CONTRADICTED','RETRACTED')),
 retrieved_utc TEXT NOT NULL,
 reviewer TEXT,
 reviewed_utc TEXT,
 contradictory_evidence_id TEXT REFERENCES lr_evidence(evidence_id)
);

CREATE TABLE lr_work_identity_claims (
 claim_id TEXT PRIMARY KEY,
 record_id TEXT NOT NULL REFERENCES files(record_id) ON DELETE RESTRICT,
 evidence_id TEXT NOT NULL REFERENCES lr_evidence(evidence_id) ON DELETE RESTRICT,
 proposed_work_id TEXT,
 original_title TEXT,
 creator_claim TEXT,
 first_publication_year INTEGER,
 original_language TEXT,
 match_status TEXT NOT NULL CHECK(match_status IN ('CANDIDATE','CORROBORATED','REJECTED')),
 confidence TEXT NOT NULL CHECK(confidence IN ('LOW','MEDIUM','HIGH'))
);

CREATE TABLE lr_authority_claims (
 claim_id TEXT PRIMARY KEY,
 record_id TEXT NOT NULL REFERENCES files(record_id) ON DELETE RESTRICT,
 evidence_id TEXT NOT NULL REFERENCES lr_evidence(evidence_id) ON DELETE RESTRICT,
 person_name TEXT NOT NULL,
 authority_identifier TEXT,
 role TEXT NOT NULL CHECK(role IN ('AUTHOR','COAUTHOR','TRANSLATOR','EDITOR','ILLUSTRATOR','PUBLISHER')),
 death_date TEXT,
 death_precision TEXT NOT NULL DEFAULT 'UNKNOWN' CHECK(death_precision IN ('EXACT','YEAR','UNKNOWN')),
 verification_status TEXT NOT NULL CHECK(verification_status IN ('CANDIDATE','CORROBORATED','REJECTED'))
);

CREATE TABLE lr_edition_match_claims (
 claim_id TEXT PRIMARY KEY,
 record_id TEXT NOT NULL REFERENCES files(record_id) ON DELETE RESTRICT,
 evidence_id TEXT NOT NULL REFERENCES lr_evidence(evidence_id) ON DELETE RESTRICT,
 work_claim_id TEXT REFERENCES lr_work_identity_claims(claim_id),
 translator TEXT,
 publisher TEXT,
 edition_year INTEGER,
 language TEXT,
 isbn TEXT,
 oclc TEXT,
 match_basis TEXT NOT NULL,
 match_status TEXT NOT NULL CHECK(match_status IN ('CANDIDATE','CORROBORATED','REJECTED'))
);

CREATE TABLE lr_rightsholders (
 holder_id TEXT PRIMARY KEY,
 display_name TEXT NOT NULL,
 holder_kind TEXT NOT NULL CHECK(holder_kind IN ('PERSON','ORGANIZATION','UNKNOWN'))
);

CREATE TABLE lr_holder_claims (
 claim_id TEXT PRIMARY KEY,
 holder_id TEXT NOT NULL REFERENCES lr_rightsholders(holder_id) ON DELETE RESTRICT,
 evidence_id TEXT NOT NULL REFERENCES lr_evidence(evidence_id) ON DELETE RESTRICT,
 record_id TEXT NOT NULL REFERENCES files(record_id) ON DELETE RESTRICT,
 scope TEXT NOT NULL CHECK(scope IN ('ORIGINAL_WORK','EDITION_FILE','TRANSLATION','ADAPTATION')),
 grantor_authority_status TEXT NOT NULL CHECK(grantor_authority_status IN ('UNVERIFIED','VERIFIED','CONFLICTED'))
);

CREATE TABLE lr_license_claims (
 license_claim_id TEXT PRIMARY KEY,
 record_id TEXT NOT NULL REFERENCES files(record_id) ON DELETE RESTRICT,
 evidence_id TEXT NOT NULL REFERENCES lr_evidence(evidence_id) ON DELETE RESTRICT,
 holder_claim_id TEXT REFERENCES lr_holder_claims(claim_id),
 scope TEXT NOT NULL CHECK(scope IN ('ORIGINAL_WORK','EDITION_FILE','TRANSLATION','ADAPTATION')),
 licensed_object TEXT NOT NULL,
 raw_identifier TEXT NOT NULL,
 canonical_identifier TEXT NOT NULL,
 license_version TEXT,
 grant_type TEXT NOT NULL CHECK(grant_type IN ('STANDARD_LICENSE','EXPLICIT_GRANT','RIGHTS_RESERVED','PUBLIC_DOMAIN_ASSESSMENT','UNKNOWN')),
 commercial_allowed INTEGER CHECK(commercial_allowed IN (0,1)),
 redistribution_allowed INTEGER CHECK(redistribution_allowed IN (0,1)),
 adaptation_allowed INTEGER CHECK(adaptation_allowed IN (0,1)),
 attribution_required INTEGER CHECK(attribution_required IN (0,1)),
 share_alike_required INTEGER CHECK(share_alike_required IN (0,1)),
 nc_restriction INTEGER CHECK(nc_restriction IN (0,1)),
 nd_restriction INTEGER CHECK(nd_restriction IN (0,1)),
 royalty_free INTEGER CHECK(royalty_free IN (0,1)),
 obligations TEXT NOT NULL DEFAULT '',
 valid_from TEXT,
 valid_until TEXT,
 verification_status TEXT NOT NULL CHECK(verification_status IN ('CANDIDATE','VERIFIED','CONFLICTED','REVOKED'))
);

CREATE TABLE lr_license_territories (
 license_claim_id TEXT NOT NULL REFERENCES lr_license_claims(license_claim_id) ON DELETE RESTRICT,
 country_code TEXT NOT NULL CHECK(length(country_code)=2),
 territory_status TEXT NOT NULL CHECK(territory_status IN ('ALLOWED','DENIED','UNKNOWN')),
 evidence_id TEXT NOT NULL REFERENCES lr_evidence(evidence_id),
 PRIMARY KEY(license_claim_id,country_code)
);

CREATE TABLE lr_expiry_assessments (
 expiry_id TEXT PRIMARY KEY,
 record_id TEXT NOT NULL REFERENCES files(record_id) ON DELETE RESTRICT,
 evidence_id TEXT REFERENCES lr_evidence(evidence_id),
 scope TEXT NOT NULL CHECK(scope IN ('ORIGINAL_WORK','EDITION_FILE','TRANSLATION')),
 jurisdiction TEXT NOT NULL CHECK(length(jurisdiction)=2),
 term_rule TEXT NOT NULL,
 expiry_date TEXT,
 earliest_safe_year INTEGER,
 precision TEXT NOT NULL DEFAULT 'UNKNOWN' CHECK(precision IN ('EXACT','SAFE_YEAR','APPROXIMATE','UNKNOWN')),
 as_of_date TEXT NOT NULL,
 exceptions TEXT NOT NULL DEFAULT ''
);

CREATE TABLE lr_rights_reviews (
 review_id TEXT PRIMARY KEY,
 record_id TEXT NOT NULL REFERENCES files(record_id) ON DELETE RESTRICT,
 jurisdiction TEXT NOT NULL CHECK(length(jurisdiction)=2),
 underlying_status TEXT NOT NULL DEFAULT 'UNCERTAIN',
 edition_status TEXT NOT NULL DEFAULT 'UNCERTAIN',
 adaptation_status TEXT NOT NULL DEFAULT 'UNKNOWN',
 commercial_class TEXT NOT NULL DEFAULT 'E_UNCERTAIN_MANUAL_REVIEW'
  CHECK(commercial_class IN ('A_COMMERCIAL_REUSE_CONFIRMED','B_COMMERCIAL_WITH_CONDITIONS','C_NONCOMMERCIAL_ONLY','D_RIGHTS_RESERVED_OR_PERMISSION_REQUIRED','E_UNCERTAIN_MANUAL_REVIEW')),
 royalty_free_status TEXT NOT NULL DEFAULT 'UNKNOWN' CHECK(royalty_free_status IN ('YES','NO','UNKNOWN')),
 decision_status TEXT NOT NULL CHECK(decision_status IN ('MACHINE_CANDIDATE','HUMAN_REVIEWED','REJECTED','SUPERSEDED')),
 blockers TEXT NOT NULL DEFAULT '',
 reviewer TEXT,
 reviewed_utc TEXT,
 created_utc TEXT NOT NULL
);

CREATE TABLE lr_review_evidence (
 review_id TEXT NOT NULL REFERENCES lr_rights_reviews(review_id) ON DELETE RESTRICT,
 evidence_id TEXT NOT NULL REFERENCES lr_evidence(evidence_id) ON DELETE RESTRICT,
 role TEXT NOT NULL CHECK(role IN ('WORK','EDITION','ADAPTATION','TERRITORY','HOLDER','CONTRADICTION')),
 PRIMARY KEY(review_id,evidence_id,role)
);

CREATE INDEX idx_lr_evidence_record_scope ON lr_evidence(record_id,scope);
CREATE INDEX idx_lr_work_record ON lr_work_identity_claims(record_id);
CREATE INDEX idx_lr_edition_record ON lr_edition_match_claims(record_id);
CREATE INDEX idx_lr_license_record_scope ON lr_license_claims(record_id,scope);
CREATE INDEX idx_lr_review_record_juris ON lr_rights_reviews(record_id,jurisdiction,created_utc);
