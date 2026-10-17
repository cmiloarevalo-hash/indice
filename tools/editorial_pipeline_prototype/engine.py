"""Deterministic, stdlib-only local SQLite catalog and synthetic editorial gate engine.

No IO outside explicit caller paths. No API/network, external AI, KDP publishing,
book content, or implicit permissions. Public CI operates on invented fixtures.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from .rights_phase_a import LayerAssessment, LayerStatus, classify
from .licenses import parse_license, license_conflict

SCHEMA = Path(__file__).with_name("schema.sql")
HEADERS = ("Name", "Extension", "SizeBytes", "RelativePath", "DirectoryRelativePath")
FINAL_A = "A_COMMERCIAL_REUSE_CONFIRMED"
FINAL_B = "B_COMMERCIAL_WITH_CONDITIONS"
FINAL_E = "E_UNCERTAIN_MANUAL_REVIEW"
PRE_PUBLICATION = "READY_FOR_HUMAN_PUBLICATION_REVIEW"
GATES = ("rights_underlying_verified", "rights_specific_source_edition_verified",
         "derivative_adaptation_rights_verified", "territories_verified",
         "attribution_obligations", "human_legal_approval", "editorial_QA_approval",
         "KDP_policy_preflight", "human_publish_authorization")
ISO_COUNTRY = re.compile(r"^[A-Z]{2}$")


class GateError(ValueError):
    """An explicit rights, editorial, QA or publication gate refused progress."""


def now():
    return datetime.now(timezone.utc).isoformat()


def record_id(relative_path):
    return hashlib.sha256(relative_path.encode("utf-8")).hexdigest()


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def connect(db):
    connection = sqlite3.connect(str(db), isolation_level=None)
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 5000")
    return connection


def init_db(connection):
    connection.executescript(SCHEMA.read_text(encoding="utf-8"))
    connection.execute(
        "INSERT OR IGNORE INTO schema_migrations VALUES(1, ?, ?)",
        ("initial editorial catalog, rights and gate schema", now()))
    return verify(connection)


def verify(connection):
    integrity = [r[0] for r in connection.execute("PRAGMA integrity_check")]
    foreign_keys = list(connection.execute("PRAGMA foreign_key_check"))
    result = {"integrity_check": integrity, "foreign_key_violations": len(foreign_keys)}
    if integrity != ["ok"] or foreign_keys:
        raise RuntimeError("SQLite integrity check failed")
    return result


def _validate_path(path):
    if not path or path.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", path):
        raise ValueError("Expected a nonabsolute catalog RelativePath")
    if any(part in ("..", ".", "") for part in path.replace("\\", "/").split("/")):
        raise ValueError("Unsafe RelativePath component")


def import_catalog(connection, input_csv):
    """Atomic import; exact file SHA provenance, stable path keys and idempotence."""
    path = Path(input_csv)
    digest = sha256(path)
    with path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if tuple(reader.fieldnames or ()) != HEADERS:
            raise ValueError("Catalog CSV schema mismatch")
        rows = []
        paths = set()
        for line in reader:
            if not line or None in line:
                raise ValueError("Malformed catalog row")
            relative = line["RelativePath"]
            _validate_path(relative)
            if relative in paths:
                raise ValueError("Duplicate RelativePath")
            paths.add(relative)
            size = int(line["SizeBytes"])
            if size < 0:
                raise ValueError("Negative SizeBytes")
            rows.append((record_id(relative), digest, relative, line["Name"],
                         line["Extension"], size, line["DirectoryRelativePath"]))
    connection.execute("BEGIN IMMEDIATE")
    try:
        old = connection.execute(
            "SELECT rows FROM snapshots WHERE snapshot_id=?", (digest,)).fetchone()
        if old:
            if old[0] != len(rows):
                raise RuntimeError("Existing snapshot row count mismatch")
            ids = {r[0] for r in connection.execute(
                "SELECT record_id FROM files WHERE snapshot_id=?", (digest,))}
            if ids != {r[0] for r in rows}:
                raise RuntimeError("Existing snapshot identities changed")
            connection.execute("COMMIT")
            return {"snapshot_id": digest, "rows": len(rows), "idempotent": True}
        if connection.execute("SELECT count(*) FROM snapshots").fetchone()[0]:
            raise ValueError("Use a fresh derived SQLite DB for each accepted snapshot")
        connection.execute(
            "INSERT INTO snapshots VALUES(?,?,?,?)",
            (digest, digest, len(rows), now()))
        connection.executemany("INSERT INTO files VALUES(?,?,?,?,?,?,?)", rows)
        connection.executemany(
            "INSERT INTO editions(edition_id,record_id) VALUES(?,?)",
            [(r[0], r[0]) for r in rows])
        connection.executemany(
            "INSERT INTO rights_decisions(edition_id,updated_utc) VALUES(?,?)",
            [(r[0], now()) for r in rows])
        connection.execute("COMMIT")
    except BaseException:
        connection.execute("ROLLBACK")
        raise
    return {"snapshot_id": digest, "rows": len(rows), "idempotent": False}


def _evidence_for_layer(connection, edition_id, layer):
    row = connection.execute(
        "SELECT evidence_id,source_url FROM evidence_sources "
        "WHERE edition_id=? AND layer=? AND evidence_status='VERIFIED' "
        "ORDER BY evidence_id LIMIT 1", (edition_id, layer)).fetchone()
    return row if row else (None, None)


def _validated_territories(value):
    if not isinstance(value, list) or not value:
        return ""
    codes = sorted(set(value))
    if any(not isinstance(v, str) or not ISO_COUNTRY.fullmatch(v) for v in codes):
        raise ValueError("Only explicit uppercase ISO-3166 alpha-2 territories")
    return ";".join(codes)


def import_rights(connection, input_json):
    """Synthetic evidence/rights import. Never trusts a claimed final A/B/C/D label.

    Real classifications require separate authorization and item-level verification.
    """
    data = json.loads(Path(input_json).read_text(encoding="utf-8"))
    if set(data) != {"editions"} or not isinstance(data["editions"], list):
        raise ValueError("Expected an editions array")
    connection.execute("BEGIN IMMEDIATE")
    count = 0
    try:
        for entry in data["editions"]:
            rid = record_id(entry["relative_path"])
            if not connection.execute(
                "SELECT 1 FROM editions WHERE edition_id=?", (rid,)).fetchone():
                raise ValueError("Rights entry does not match imported file identity")
            work_id = entry["work_id"]
            prior = connection.execute(
                "SELECT canonical_title FROM works WHERE work_id=?", (work_id,)).fetchone()
            if prior and prior[0] != entry["work_title"]:
                raise ValueError("Conflicting canonical work identity: same work_id, new title")
            connection.execute(
                "INSERT OR IGNORE INTO works(work_id,canonical_title) VALUES(?,?)",
                (work_id, entry["work_title"]))
            connection.execute(
                "UPDATE editions SET work_id=?,edition_label=?,translation_status=?,"
                "edition_provenance_status=? WHERE edition_id=?",
                (work_id, entry.get("edition_label"),
                 entry.get("translation_status", "UNKNOWN"),
                 entry.get("edition_provenance_status", "UNRESOLVED"), rid))
            # Clear references BEFORE replacing evidence rows; FK constraints stay ON.
            connection.execute(
                "UPDATE rights_decisions SET underlying_evidence_id=NULL,"
                "edition_evidence_id=NULL,derivative_evidence_id=NULL,"
                "territory_evidence_id=NULL WHERE edition_id=?", (rid,))
            connection.execute("DELETE FROM evidence_sources WHERE edition_id=?", (rid,))
            normalized = {}
            for layer, claim in entry.get("evidence", {}).items():
                if layer not in ("UNDERLYING", "EDITION", "DERIVATIVE", "TERRITORY"):
                    raise ValueError("Unknown evidence layer")
                if not claim.get("source_url", "").startswith("https://"):
                    raise ValueError("Evidence source URL must be HTTPS")
                evidence_id = hashlib.sha256((rid + "|" + layer + "|" +
                         claim["source_url"]).encode("utf-8")).hexdigest()
                connection.execute(
                    "INSERT INTO evidence_sources VALUES(?,?,?,?,?,?,?)",
                    (evidence_id, rid, layer, claim["source_url"],
                     claim["claim"], claim.get("status", "UNVERIFIED"), now()))
                normalized[layer] = claim
            underlying_id, underlying_url = _evidence_for_layer(connection, rid, "UNDERLYING")
            edition_id, edition_url = _evidence_for_layer(connection, rid, "EDITION")
            derivative_id, _ = _evidence_for_layer(connection, rid, "DERIVATIVE")
            territory_id, _ = _evidence_for_layer(connection, rid, "TERRITORY")
            layer_under = LayerStatus(entry.get("underlying_status", "UNCERTAIN"))
            layer_edition = LayerStatus(entry.get("edition_status", "UNCERTAIN"))
            allow = entry.get("derivative_adaptation_permission", "UNKNOWN")
            if allow not in ("YES", "NO", "UNKNOWN"):
                raise ValueError("Derivative permission must be YES/NO/UNKNOWN")
            terms = parse_license(entry.get("license_id", "UNKNOWN"))
            # Phase A is the sole layer combiner. Never feed it a claimed OPEN
            # status that contradicts the exact edition licence semantics.
            if license_conflict(
                terms, edition_status=layer_edition.value,
                derivative_permission=allow,
            ):
                layer_edition = LayerStatus.UNCERTAIN
            decision = classify(
                LayerAssessment(layer_under, (underlying_url,) if underlying_url else ()),
                LayerAssessment(layer_edition, (edition_url,) if edition_url else ()))
            territory = _validated_territories(entry.get("territories", []))
            connection.execute(
                "UPDATE rights_decisions SET underlying_status=?,edition_status=?,"
                "commercial_class=?,license_id=?,derivative_adaptation_permission=?,"
                "allowed_territories=?,obligations=?,underlying_evidence_id=?,"
                "edition_evidence_id=?,derivative_evidence_id=?,territory_evidence_id=?,"
                "jurisdiction=?,updated_utc=? WHERE edition_id=?",
                (layer_under.value, layer_edition.value, decision.commercial_use_class.value,
                 terms.identifier if terms.recognized else "UNKNOWN", allow, territory,
                 entry.get("obligations", ""), underlying_id, edition_id,
                 derivative_id, territory_id, entry.get("jurisdiction", "REVIEW_REQUIRED"),
                 now(), rid))
            count += 1
        connection.execute("COMMIT")
    except BaseException:
        connection.execute("ROLLBACK")
        raise
    return {"entries": count, "committed": True}


def summary(connection):
    total = connection.execute("SELECT count(*) FROM files").fetchone()[0]
    counts = dict(connection.execute(
        "SELECT commercial_class, count(*) FROM rights_decisions GROUP BY commercial_class"))
    return {"files": total, "classes": counts,
            "works": connection.execute("SELECT count(*) FROM works").fetchone()[0],
            "editorial_projects": connection.execute(
                "SELECT count(*) FROM editorial_projects").fetchone()[0]}


def rights_status(connection, relative_path):
    rid = record_id(relative_path)
    row = connection.execute(
        "SELECT r.commercial_class,r.underlying_status,r.edition_status,r.license_id,"
        "r.derivative_adaptation_permission,r.allowed_territories "
        "FROM rights_decisions r WHERE r.edition_id=?", (rid,)).fetchone()
    if not row:
        raise ValueError("RelativePath not imported")
    return dict(zip(("class","underlying","edition","license","adaptation","territories"),row))


def _gate_evidence(connection, edition_id, layer):
    evidence_id, _ = _evidence_for_layer(connection, edition_id, layer)
    return bool(evidence_id)


def eligibility(connection, edition_id, territory):
    row = connection.execute(
        "SELECT commercial_class,license_id,derivative_adaptation_permission,"
        "allowed_territories,obligations,jurisdiction FROM rights_decisions "
        "WHERE edition_id=?", (edition_id,)).fetchone()
    if not row:
        raise GateError("Edition not present")
    final_class, lic, derivative, codes, obligations, jurisdiction = row
    has_source = _gate_evidence(connection, edition_id, "UNDERLYING")
    has_edition = _gate_evidence(connection, edition_id, "EDITION")
    terms = parse_license(lic)
    # Query-time revalidation also blocks tampered/stale decision rows; ND/NC
    # cannot be overridden by an unscoped adaptation/commercial flag.
    licence_consistent = (
        not license_conflict(terms, edition_status={
            "A_COMMERCIAL_REUSE_CONFIRMED": "OPEN_COMMERCIAL",
            "B_COMMERCIAL_WITH_CONDITIONS": "COMMERCIAL_WITH_CONDITIONS",
            "C_NONCOMMERCIAL_ONLY": "NONCOMMERCIAL_ONLY",
            "D_RIGHTS_RESERVED_OR_PERMISSION_REQUIRED": "RIGHTS_RESERVED_OR_PERMISSION_REQUIRED",
        }.get(final_class, "UNCERTAIN"), derivative_permission=derivative)
        if final_class != FINAL_E else False
    )
    derivative_ok = (derivative == "YES" and
                     _gate_evidence(connection, edition_id, "DERIVATIVE") and
                     terms.adaptation is True and licence_consistent)
    territories_ok = (bool(ISO_COUNTRY.fullmatch(territory)) and
                      territory in codes.split(";") and
                      _gate_evidence(connection, edition_id, "TERRITORY") and
                      jurisdiction == territory)
    # Preserve attribution/SA obligations, never silently waive them.
    attr = (final_class in (FINAL_A, FINAL_B) and
            (final_class != FINAL_B or bool(obligations.strip())))
    # A separate explicit additional grant would require a reviewed, scoped
    # model. Neither NC nor ND is bypassable by caller flags.
    return {
        "rights_underlying_verified": has_source,
        "rights_specific_source_edition_verified": has_edition,
        "derivative_adaptation_rights_verified": derivative_ok,
        "territories_verified": territories_ok,
        "attribution_obligations": attr,
        "commercial_A_or_B": (final_class in (FINAL_A, FINAL_B)
                              and terms.commercial is True and licence_consistent),
        "license": lic,
        "commercial_class": final_class,
    }


def start_project(connection, relative_path, project_id, territory):
    eid = record_id(relative_path)
    eligibility_report = eligibility(connection, eid, territory)
    mandatory = ("rights_underlying_verified","rights_specific_source_edition_verified",
                 "derivative_adaptation_rights_verified","territories_verified",
                 "attribution_obligations","commercial_A_or_B")
    if not all(eligibility_report[k] for k in mandatory):
        raise GateError("STOP: original/edition/derivative/territory/obligations rights not verified")
    with connection:
        connection.execute(
            "INSERT INTO editorial_projects(project_id,edition_id,territory,"
            "state,updated_utc) VALUES(?,?,?,'ELIGIBLE_FOR_EDITORIAL_WORK',?)",
            (project_id,eid,territory,now()))
    return eligibility_report


def simulate_editorial(connection, project_id, content_origin, differentiation="NOT_EVALUATED"):
    if content_origin not in ("HUMAN_CREATED","AI_ASSISTED","AI_GENERATED"):
        raise ValueError("Invalid simulated content origin")
    if differentiation not in ("NOT_EVALUATED","NOT_REQUIRED","ORIGINAL_TRANSLATION",
                               "ORIGINAL_ANNOTATIONS","ORIGINAL_ILLUSTRATIONS"):
        raise ValueError("Unknown differentiation")
    project = connection.execute(
        "SELECT state,edition_id,territory FROM editorial_projects WHERE project_id=?",
        (project_id,)).fetchone()
    if not project or project[0] not in ("ELIGIBLE_FOR_EDITORIAL_WORK","SIMULATED_EDITORIAL_WORK"):
        raise GateError("Cannot simulate before rights eligibility")
    gates = eligibility(connection,project[1],project[2])
    if not all(gates[k] for k in ("rights_underlying_verified","rights_specific_source_edition_verified",
                                "derivative_adaptation_rights_verified","territories_verified",
                                "attribution_obligations","commercial_A_or_B")):
        raise GateError("Rights revoked or invalid")
    with connection:
        connection.execute(
            "UPDATE editorial_projects SET state='SIMULATED_EDITORIAL_WORK',"
            "content_origin=?,ai_generated_disclosure=?,public_domain_differentiation=?,"
            "human_legal_approval=0,editorial_qa_approval=0,kdp_policy_preflight=0,"
            "human_publish_authorization=0,updated_utc=? WHERE project_id=?",
            (content_origin,1 if content_origin=="AI_GENERATED" else 0,
             differentiation,now(),project_id))
    return {"project":project_id,"simulation_only":True,"content_generated":False}


def set_review_gate(connection, project_id, gate, passed, *, synthetic_attestation=False):
    if gate not in ("human_legal_approval","editorial_qa_approval",
                    "kdp_policy_preflight","human_publish_authorization"):
        raise ValueError("Only explicit human/preflight gates allowed")
    if not synthetic_attestation:
        raise GateError("Explicit synthetic attestation required; never infer human approvals")
    if type(passed) is not bool:
        raise TypeError("Approval must be boolean")
    state = connection.execute(
        "SELECT state FROM editorial_projects WHERE project_id=?", (project_id,)).fetchone()
    if not state or state[0] not in ("SIMULATED_EDITORIAL_WORK",
                                    PRE_PUBLICATION,"HUMAN_PUBLICATION_AUTHORIZED_SIMULATION"):
        raise GateError("No editorial simulation ready for review")
    if gate=="human_publish_authorization" and passed and state[0]!=PRE_PUBLICATION:
        raise GateError("Only after complete preflight; never bypass human review")
    with connection:
        connection.execute(
            "UPDATE editorial_projects SET "+gate+"=?,updated_utc=? WHERE project_id=?",
            (int(passed), now(), project_id))


def preflight(connection, project_id, *, public_domain_free_version=False):
    row = connection.execute(
        "SELECT edition_id,territory,state,content_origin,ai_generated_disclosure,"
        "public_domain_differentiation,human_legal_approval,editorial_qa_approval,"
        "kdp_policy_preflight,human_publish_authorization FROM editorial_projects "
        "WHERE project_id=?", (project_id,)).fetchone()
    if not row:
        raise ValueError("Unknown project")
    (eid,territory,state,origin,disclosure,differentiation,legal,qa,kdp,publication)=row
    checks = eligibility(connection,eid,territory)
    checks.update({
        "human_legal_approval":bool(legal),
        "editorial_QA_approval":bool(qa),
        "KDP_policy_preflight":bool(kdp),
        "human_publish_authorization":bool(publication),
        "ai_generated_disclosure": origin!="AI_GENERATED" or bool(disclosure),
        "KDP_public_domain_differentiation":not public_domain_free_version or
          differentiation in ("ORIGINAL_TRANSLATION","ORIGINAL_ANNOTATIONS","ORIGINAL_ILLUSTRATIONS"),
        "simulated_editorial_only":state in
          ("SIMULATED_EDITORIAL_WORK",PRE_PUBLICATION,"HUMAN_PUBLICATION_AUTHORIZED_SIMULATION")
    })
    prerequisites = ("rights_underlying_verified","rights_specific_source_edition_verified",
      "derivative_adaptation_rights_verified","territories_verified","attribution_obligations",
      "commercial_A_or_B","human_legal_approval","editorial_QA_approval",
      "KDP_policy_preflight","ai_generated_disclosure","KDP_public_domain_differentiation",
      "simulated_editorial_only")
    okay = all(checks[k] for k in prerequisites)
    result_state = PRE_PUBLICATION if okay else "STOP_RIGHTS_OR_KDP_GATES"
    # Producing this report DOES NOT publish or grant real legal clearance.
    with connection:
        connection.execute(
            "INSERT INTO preflight_audit(project_id,checklist_json,result_state,created_utc)"
            " VALUES(?,?,?,?)", (project_id,json.dumps(checks,sort_keys=True),result_state,now()))
        if okay and state=="SIMULATED_EDITORIAL_WORK":
            connection.execute("UPDATE editorial_projects SET state=?,updated_utc=? "
                               "WHERE project_id=?", (PRE_PUBLICATION,now(),project_id))
    return {"project_id":project_id,"state":result_state,
            "checklist":checks,"requires_human_publication_authorization":True,
            "external_kdp_publication_performed":False}


def authorize_publication_simulation(connection, project_id):
    row = connection.execute(
        "SELECT state,human_publish_authorization FROM editorial_projects WHERE project_id=?",
        (project_id,)).fetchone()
    if not row or row!=(PRE_PUBLICATION,1):
        raise GateError("Explicit human_publish_authorization required after all gates")
    with connection:
        connection.execute("UPDATE editorial_projects SET "
            "state='HUMAN_PUBLICATION_AUTHORIZED_SIMULATION',updated_utc=? WHERE project_id=?",
            (now(),project_id))
    return {"state":"HUMAN_PUBLICATION_AUTHORIZED_SIMULATION",
            "actual_publication_or_upload":False}


def export_report(connection, output):
    # Generic local report only; caller chooses output location and handles privacy.
    data={"summary":summary(connection),"verified":verify(connection),
          "projects":[dict(zip(("project_id","state","territory"),x))
            for x in connection.execute(
            "SELECT project_id,state,territory FROM editorial_projects ORDER BY project_id")]}
    Path(output).write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",
                            encoding="utf-8")
    return {"sha256":sha256(output),"path":str(output)}
