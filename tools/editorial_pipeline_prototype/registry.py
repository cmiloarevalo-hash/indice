"""Additive research registry for a work COPY of a metadata-only SQLite.

Never opens any original book, downloads a private snapshot, fetches a URL,
or runs a migration against the immutable input. A caller must supply a
legitimately obtained local SQLite and an *absent* destination path.
"""
from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path
from urllib.parse import quote

MIGRATION = Path(__file__).with_name("migrations") / "001_rights_registry.sql"
REQUIRED_TABLES = {
    "source_snapshots", "files", "editions", "works", "authors", "evidence",
    "rights_layer_status", "author_file_leads", "missing_required_fields",
    "research_notes", "sample_assessment",
}


class MigrationError(RuntimeError):
    pass


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fd:
        for block in iter(lambda: fd.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def verify(conn: sqlite3.Connection, *, expected_rows: int | None = None) -> dict:
    """Enforce SQLite, FK and record identity invariants without title joining."""
    conn.execute("PRAGMA foreign_keys=ON")
    integrity = [row[0] for row in conn.execute("PRAGMA integrity_check")]
    violations = list(conn.execute("PRAGMA foreign_key_check"))
    if integrity != ["ok"] or violations:
        raise MigrationError(f"SQLite integrity/FK failure: {integrity}; FK count={len(violations)}")
    existing = {row[0] for row in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )}
    missing = REQUIRED_TABLES - existing
    if missing:
        raise MigrationError("Missing accepted-schema tables: " + ", ".join(sorted(missing)))
    for table in ("files", "editions"):
        columns = {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
        if "record_id" not in columns:
            raise MigrationError(f"{table}.record_id is absent")
    files = conn.execute("SELECT COUNT(*) FROM files").fetchone()[0]
    editions = conn.execute("SELECT COUNT(*) FROM editions").fetchone()[0]
    if files != editions or (expected_rows is not None and files != expected_rows):
        raise MigrationError("Accepted file/edition count mismatch")
    if conn.execute("SELECT COUNT(DISTINCT record_id) FROM files").fetchone()[0] != files:
        raise MigrationError("Duplicate file identities")
    if conn.execute("SELECT COUNT(DISTINCT record_id) FROM editions").fetchone()[0] != editions:
        raise MigrationError("Duplicate edition identities")
    if conn.execute(
        "SELECT COUNT(*) FROM editions e LEFT JOIN files f ON e.record_id=f.record_id "
        "WHERE f.record_id IS NULL"
    ).fetchone()[0]:
        raise MigrationError("Edition without source file")
    return {"integrity_check": "ok", "foreign_key_violations": 0,
            "files": files, "editions": editions}


def _statements(sql: str) -> list[str]:
    """Migration SQL deliberately avoids semicolons inside strings/triggers.

    A schema linter checks this narrow format; execute (not executescript) is
    required because executescript may commit an outer migration transaction.
    """
    source = "\n".join(
        line for line in sql.splitlines() if not line.lstrip().startswith("--")
    )
    return [statement.strip() for statement in source.split(";") if statement.strip()]


def migrate(conn: sqlite3.Connection, *, expected_rows: int | None = None,
            fail_after: int | None = None) -> dict:
    """Idempotent and atomic, ONLY on an independent work-copy connection.

    Tests use fail_after for simulated rollback. Production callers must
    never pass the baseline source connection into this function.
    """
    baseline = verify(conn, expected_rows=expected_rows)
    sql_bytes = MIGRATION.read_bytes()
    digest = hashlib.sha256(sql_bytes).hexdigest()
    statements = _statements(sql_bytes.decode("utf-8"))
    conn.execute("BEGIN IMMEDIATE")
    try:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS lr_schema_migrations("
            "version INTEGER PRIMARY KEY, sha256 TEXT NOT NULL, "
            "applied_utc TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"
        )
        previous = conn.execute(
            "SELECT sha256 FROM lr_schema_migrations WHERE version=1"
        ).fetchone()
        if previous:
            if previous[0] != digest:
                raise MigrationError("Migration v1 checksum drift")
            conn.execute("COMMIT")
            return {**baseline, "migration": 1, "already_applied": True,
                    "sql_sha256": digest}
        for index, statement in enumerate(statements):
            conn.execute(statement)
            if fail_after is not None and index + 1 >= fail_after:
                raise MigrationError("Injected synthetic migration failure")
        conn.execute(
            "INSERT INTO lr_schema_migrations(version,sha256) VALUES(1,?)",
            (digest,),
        )
        conn.execute("COMMIT")
    except BaseException:
        conn.execute("ROLLBACK")
        raise
    return {**verify(conn, expected_rows=expected_rows),
            "migration": 1, "already_applied": False, "sql_sha256": digest}


def prepare_work_copy(source: Path, target: Path, *,
                      expected_sha256: str | None = None,
                      expected_rows: int = 28781) -> dict:
    """Copy an authenticated snapshot without touching it; no CSV rebuilding.

    Fails if target already exists. Uses read-only SQLite and backup API.
    The source's byte hash is compared before/after. The caller must never
    pass the accepted snapshot path as target.
    """
    source = Path(source).resolve(strict=True)
    target = Path(target).resolve()
    if source == target or target.exists():
        raise MigrationError("Target must be a new, distinct, absent work file")
    if not target.parent.is_dir():
        raise MigrationError("Target parent does not exist")
    before = file_sha256(source)
    if expected_sha256 and before.lower() != expected_sha256.lower():
        raise MigrationError("Source SHA-256 differs from explicitly authorized snapshot")
    source_uri = "file:" + quote(source.as_posix(), safe="/:") + "?mode=ro"
    src = sqlite3.connect(source_uri, uri=True)
    try:
        verify(src, expected_rows=expected_rows)
        out = sqlite3.connect(target)
        try:
            src.backup(out)
            out.close()
            out = None
        finally:
            if out is not None:
                out.close()
    except BaseException:
        if target.exists():
            target.unlink()
        raise
    finally:
        src.close()
    if before != file_sha256(source):
        if target.exists():
            target.unlink()
        raise MigrationError("Source changed during copy")
    dst = sqlite3.connect(target, isolation_level=None)
    try:
        result = migrate(dst, expected_rows=expected_rows)
    except BaseException:
        dst.close()
        target.unlink()
        raise
    finally:
        try:
            dst.close()
        except Exception:
            pass
    result.update({"input_sha256": before, "work_copy_sha256": file_sha256(target)})
    return result


def find_records(conn: sqlite3.Connection, phrase: str, limit: int = 25) -> list[dict]:
    """Bibliographic navigation (local only; never uses public CI private data)."""
    if not isinstance(phrase, str) or not phrase.strip():
        return []
    if not 1 <= limit <= 100:
        raise ValueError("Limit must be 1..100")
    verify(conn)
    rows = conn.execute(
        "SELECT record_id,name FROM files WHERE name LIKE ? ESCAPE '\\' "
        "ORDER BY record_id LIMIT ?",
        ("%" + phrase.replace("\\", "\\\\").replace("%", "\\%")
         .replace("_", "\\_") + "%", limit),
    )
    return [{"record_id": r[0], "name": r[1]} for r in rows]


def registry_counts(conn: sqlite3.Connection) -> dict:
    verify(conn)
    have = {row[0] for row in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )}
    if "lr_schema_migrations" not in have:
        return {"migrated": False, "evidence": 0, "licenses": 0, "reviews": 0}
    return {"migrated": True,
            "evidence": conn.execute("SELECT COUNT(*) FROM lr_evidence").fetchone()[0],
            "licenses": conn.execute("SELECT COUNT(*) FROM lr_license_claims").fetchone()[0],
            "reviews": conn.execute("SELECT COUNT(*) FROM lr_rights_reviews").fetchone()[0]}
