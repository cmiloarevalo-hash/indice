"""H5 regression: accepted metadata-only SQLite *shape*, fully invented rows.

The fixture mirrors table/PK/FK contracts observed read-only in #21, but
contains no actual item, title, path, source hash, or rights conclusion.
"""
from __future__ import annotations

import hashlib
import sqlite3
from contextlib import closing
import tempfile
import unittest
from pathlib import Path

from tools.editorial_pipeline_prototype import registry

HERE = Path(__file__).resolve().parents[1]
SCHEMA = HERE / "fixtures" / "accepted_schema_h5_synthetic.sql"


class AcceptedRealShapeSyntheticTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory(prefix="h5-fictional-")
        self.addCleanup(folder.cleanup)
        self.directory = Path(folder.name)
        self.source = self.directory / "original-FAKE.sqlite"
        db = sqlite3.connect(self.source, isolation_level=None)
        try:
            db.executescript(SCHEMA.read_text(encoding="utf-8"))
            db.execute("INSERT INTO source_snapshots VALUES(?,?,?,?,?,?)", (
                "synthetic-h5", "0000000-fake-source", "0" * 64,
                3, "2026-10-17T00:00:00Z", 0))
            self.records = []
            db.execute("BEGIN IMMEDIATE")
            for i in range(3):
                path = f"fictional/items/book-{i}.pdf"
                rid = hashlib.sha256(path.encode("utf-8")).hexdigest()
                eid = f"fictional-edition-{i}"
                self.records.append((rid, eid))
                db.execute(
                    "INSERT INTO files "
                    "(record_id,source_row,snapshot_id,relative_path,name,extension,"
                    "size_bytes,directory_relative_path,actual_stat_status) "
                    "VALUES(?,?,?,?,?,?,?,?,?)",
                    (rid, i + 1, "synthetic-h5", path,
                     f"Invented Item {i}", ".pdf", i + 1, "fictional/items",
                     "NOT_CHECKED"))
                db.execute(
                    "INSERT INTO editions("
                    "edition_id,record_id,metadata_status,edition_license_verified)"
                    " VALUES(?,?,?,?)",
                    (eid, rid, "UNVERIFIED", 0))
                db.execute(
                    "INSERT INTO rights_layer_status("
                    "record_id,underlying_status,edition_status,derivative_status,"
                    "territories_status,commercial_class,"
                    "commercial_royalty_free_confirmed,jurisdiction,certainty,"
                    "blocking_reason) VALUES(?,?,?,?,?,?,?,?,?,?)",
                    (rid, "UNCERTAIN", "UNCERTAIN", "UNKNOWN",
                     "UNKNOWN", "E_UNCERTAIN_MANUAL_REVIEW", 0, "CL",
                     "LOW", "Fictional: specific edition not established"))
            db.execute("COMMIT")
        finally:
            db.close()

    def test_real_edition_pk_and_file_fk_are_distinct_from_old_mock(self):
        with closing(sqlite3.connect(self.source)) as db:
            fields = {row[1]: row[5] for row in db.execute(
                "PRAGMA table_info(editions)")}
            self.assertEqual(fields["edition_id"], 1)
            self.assertEqual(fields["record_id"], 0)
            fk = {(r[3], r[2], r[4]) for r in db.execute(
                "PRAGMA foreign_key_list(editions)")}
            self.assertIn(("record_id", "files", "record_id"), fk)
            self.assertIn(("work_id", "works", "work_id"), fk)
            self.assertEqual(registry.verify(db, expected_rows=3)["files"], 3)
            self.assertNotEqual(self.records[0][0], self.records[0][1])

    def test_real_shaped_backup_migration_idempotence_and_original_bytes(self):
        before = registry.file_sha256(self.source)
        destination = self.directory / "derived.sqlite"
        result = registry.prepare_work_copy(
            self.source, destination, expected_sha256=before,
            expected_rows=3)
        self.assertEqual(registry.file_sha256(self.source), before)
        self.assertEqual(result["files"], 3)
        self.assertEqual(result["editions"], 3)
        self.assertEqual(result["integrity_check"], "ok")
        self.assertEqual(result["foreign_key_violations"], 0)
        self.assertEqual(result["migration"], 1)
        with closing(sqlite3.connect(destination, isolation_level=None)) as db:
            self.assertEqual(
                {row[0] for row in db.execute(
                    "SELECT record_id FROM files")},
                {rid for rid, _ in self.records})
            self.assertEqual(
                {row[0] for row in db.execute(
                    "SELECT edition_id FROM editions")},
                {eid for _, eid in self.records})
            self.assertEqual(db.execute(
                "SELECT COUNT(*) FROM rights_layer_status").fetchone()[0], 3)
            self.assertTrue(
                registry.migrate(db, expected_rows=3)["already_applied"])
            self.assertEqual(registry.verify(db, expected_rows=3)
                             ["foreign_key_violations"], 0)
            self.assertEqual(registry.registry_counts(db), {
                "migrated": True, "evidence": 0,
                "licenses": 0, "reviews": 0})

    def test_atomic_failure_rollback_on_real_shaped_mock(self):
        before = registry.file_sha256(self.source)
        db = sqlite3.connect(self.source, isolation_level=None)
        try:
            old_names = {row[0] for row in db.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")}
            with self.assertRaisesRegex(
                registry.MigrationError, "Injected synthetic migration failure"
            ):
                registry.migrate(db, expected_rows=3, fail_after=6)
            new_names = {row[0] for row in db.execute(
                "SELECT name FROM sqlite_master WHERE type='table'")}
            self.assertEqual(old_names, new_names)
            self.assertEqual(registry.verify(db, expected_rows=3)
                             ["integrity_check"], "ok")
        finally:
            db.close()
        self.assertEqual(registry.file_sha256(self.source), before)

    def test_existing_editon_rights_state_remains_e(self):
        destination = self.directory / "new-workcopy.sqlite"
        registry.prepare_work_copy(
            self.source, destination,
            expected_sha256=registry.file_sha256(self.source),
            expected_rows=3)
        with closing(sqlite3.connect(destination)) as db:
            existing = db.execute(
                "SELECT COUNT(*) FROM rights_layer_status "
                "WHERE commercial_class='E_UNCERTAIN_MANUAL_REVIEW'"
            ).fetchone()[0]
            self.assertEqual(existing, 3)
            new_reviews = db.execute(
                "SELECT COUNT(*) FROM lr_rights_reviews").fetchone()[0]
            self.assertEqual(new_reviews, 0)

    def test_fk_on_realshaped_edition_id_enforced(self):
        with closing(sqlite3.connect(self.source, isolation_level=None)) as db:
            db.execute("PRAGMA foreign_keys=ON")
            with self.assertRaises(sqlite3.IntegrityError):
                db.execute(
                    "INSERT INTO editions("
                    "edition_id,record_id,metadata_status,edition_license_verified) "
                    "VALUES(?,?,?,?)",
                    ("invented-invalid-edition", "not-a-real-record-id",
                     "UNVERIFIED", 0))
            self.assertEqual(registry.verify(db, expected_rows=3)
                             ["foreign_key_violations"], 0)


if __name__ == "__main__":
    unittest.main()
