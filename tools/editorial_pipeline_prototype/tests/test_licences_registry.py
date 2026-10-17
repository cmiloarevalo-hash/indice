"""Synthetic-only adversarial licensing and SQLite migration regressions.

No real names/paths/catalog data, external APIs, OCR or publishing.
"""
import copy
import hashlib
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from tools.editorial_pipeline_prototype import engine as e
from tools.editorial_pipeline_prototype import registry
from tools.editorial_pipeline_prototype.licenses import parse_license

BASE = Path(e.__file__).parent
RIGHTS = BASE / "fixtures" / "synthetic_rights.json"
SOURCE_SCHEMA = BASE / "fixtures" / "accepted_schema_synthetic.sql"
CATALOG = BASE / "fixtures" / "synthetic_catalog.csv"
BY = "fixture/fiction/Emerald Orchard BY.txt"
ND = "fixture/fiction/Copper Birds ND.txt"
NC = "fixture/fiction/Paper Mountains NC.pdf"
GOOD = "fixture/fiction/Invented River Fables.pdf"


class LicenseSemanticsTests(unittest.TestCase):
    def test_cc_versions_forms_and_urls(self):
        cases = (
            ("CC-BY-ND-4.0", "CC-BY-ND-4.0", True, False),
            ("cc_by_nc_4.0", "CC-BY-NC-4.0", False, True),
            ("https://creativecommons.org/licenses/by-nc-nd/4.0/",
             "CC-BY-NC-ND-4.0", False, False),
            ("https://creativecommons.org/licenses/by-sa/3.0/",
             "CC-BY-SA-3.0", True, True),
            ("CC BY 4.0", "CC-BY-4.0", True, True),
            ("https://creativecommons.org/publicdomain/zero/1.0/",
             "CC0-1.0", True, True),
        )
        for raw, canonical, commercial, adaptation in cases:
            with self.subTest(raw=raw):
                terms = parse_license(raw)
                self.assertTrue(terms.recognized)
                self.assertEqual(terms.identifier, canonical)
                self.assertEqual(terms.commercial, commercial)
                self.assertEqual(terms.adaptation, adaptation)

    def test_unknown_and_versioned_do_not_fail_open(self):
        for raw in (
            "CC-BY-NC-9.0", "CC-BY-UNKNOWN-4.0",
            "https://untrusted.example/licenses/by/4.0/",
            "CC-BY-NC-ND-SA-4.0", "", "CC-BY-ND-4.0-commercial-ok"
        ):
            with self.subTest(raw=raw):
                self.assertFalse(parse_license(raw).recognized)
                self.assertIsNone(parse_license(raw).commercial)

    def test_nd_verbatim_commercial_distinct_from_adaptation(self):
        terms = parse_license("CC-BY-ND-4.0")
        self.assertTrue(terms.commercial)
        self.assertFalse(terms.adaptation)
        self.assertTrue(terms.no_derivatives)

    def test_nc_sa_no_commercial_but_allows_noncommercial_adaptation(self):
        terms = parse_license("CC-BY-NC-SA-4.0")
        self.assertFalse(terms.commercial)
        self.assertTrue(terms.adaptation)
        self.assertTrue(terms.share_alike)


class BadClaimsFailClosedTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix="fictional-license-")
        self.addCleanup(tmp.cleanup)
        self.directory = Path(tmp.name)
        self.connection = e.connect(self.directory / "prototype.sqlite")
        self.addCleanup(self.connection.close)
        e.init_db(self.connection)
        e.import_catalog(self.connection, CATALOG)
        self.data = json.loads(RIGHTS.read_text(encoding="utf-8"))

    def change(self, fragment, **overrides):
        data = copy.deepcopy(self.data)
        for entry in data["editions"]:
            if fragment in entry["relative_path"]:
                entry.update(overrides)
                if overrides.get("add_derivative_evidence"):
                    entry.pop("add_derivative_evidence", None)
                    entry["evidence"]["DERIVATIVE"] = {
                        "source_url": "https://example.invalid/synthetic-derivative",
                        "claim": "Invented derivative statement",
                        "status": "VERIFIED",
                    }
                break
        # Do not write any real book title or path: the fixture is invented.
        artifact = self.directory / "synthetic-claims.json"
        artifact.write_text(json.dumps(data), encoding="utf-8")
        e.import_rights(self.connection, artifact)

    def test_regression_versioned_nd_conflicting_yes_blocks(self):
        self.change("Copper Birds", license_id="CC-BY-ND-4.0",
                    derivative_adaptation_permission="YES",
                    add_derivative_evidence=True)
        self.assertEqual(e.rights_status(self.connection, ND)["class"], e.FINAL_E)
        gate = e.eligibility(self.connection, e.record_id(ND), "CL")
        self.assertFalse(gate["derivative_adaptation_rights_verified"])
        with self.assertRaises(e.GateError):
            e.start_project(self.connection, ND, "invalid-nd", "CL")

    def test_regression_versioned_nc_conflicting_open_blocks(self):
        self.change("Paper Mountains", license_id="CC-BY-NC-4.0",
                    edition_status="OPEN_COMMERCIAL",
                    derivative_adaptation_permission="YES",
                    add_derivative_evidence=True)
        self.assertEqual(e.rights_status(self.connection, NC)["class"], e.FINAL_E)
        gate = e.eligibility(self.connection, e.record_id(NC), "CL")
        self.assertFalse(gate["commercial_A_or_B"])
        with self.assertRaises(e.GateError):
            e.start_project(self.connection, NC, "invalid-nc", "CL")

    def test_nc_direct_db_tampering_cannot_make_license_commercial(self):
        self.change("Paper Mountains", license_id="CC-BY-NC-4.0")
        self.connection.execute("UPDATE rights_decisions SET commercial_class=? WHERE edition_id=?",
                                (e.FINAL_B, e.record_id(NC)))
        self.assertFalse(e.eligibility(self.connection, e.record_id(NC), "CL")
                         ["commercial_A_or_B"])
        with self.assertRaises(e.GateError):
            e.start_project(self.connection, NC, "tampered-nc", "CL")

    def test_nd_direct_db_tampering_cannot_authorize_adaptation(self):
        self.change("Copper Birds", license_id="CC-BY-ND-4.0")
        self.connection.execute(
            "UPDATE rights_decisions SET derivative_adaptation_permission='YES' "
            "WHERE edition_id=?", (e.record_id(ND),))
        self.assertFalse(e.eligibility(self.connection, e.record_id(ND), "CL")
                         ["derivative_adaptation_rights_verified"])

    def test_versioned_by_sa_positive_with_fictional_evidence(self):
        self.change("Emerald Orchard", license_id="CC-BY-SA-4.0")
        self.assertEqual(e.rights_status(self.connection, BY)["class"], e.FINAL_B)
        self.assertTrue(e.eligibility(self.connection, e.record_id(BY), "CL")
                        ["commercial_A_or_B"])
        e.start_project(self.connection, BY, "positive-by-sa", "CL")

    def test_by_claimed_unconditional_a_fails_closed(self):
        self.change("Emerald Orchard", license_id="CC-BY-4.0",
                    edition_status="OPEN_COMMERCIAL")
        self.assertEqual(e.rights_status(self.connection, BY)["class"], e.FINAL_E)
        with self.assertRaises(e.GateError):
            e.start_project(self.connection, BY, "false-a", "CL")

    def test_nd_with_no_adaptation_stays_conditional_for_verbatim(self):
        self.change("Copper Birds", license_id="CC-BY-ND-4.0")
        self.assertEqual(e.rights_status(self.connection, ND)["class"], e.FINAL_B)
        self.assertFalse(e.eligibility(self.connection, e.record_id(ND), "CL")
                         ["derivative_adaptation_rights_verified"])

    def test_revoke_after_preflight_blocks_last_authorization(self):
        self.change("Invented River", license_id="PUBLIC-DOMAIN")
        e.start_project(self.connection, GOOD, "revocation", "CL")
        e.simulate_editorial(self.connection, "revocation", "AI_ASSISTED")
        for gate in ("human_legal_approval", "editorial_qa_approval",
                     "kdp_policy_preflight"):
            e.set_review_gate(self.connection, "revocation", gate, True,
                              synthetic_attestation=True)
        self.assertEqual(
            e.preflight(self.connection, "revocation",
                        public_domain_free_version=False)["state"],
            e.PRE_PUBLICATION)
        e.set_review_gate(self.connection, "revocation",
                          "human_publish_authorization", True,
                          synthetic_attestation=True)
        # Rights revocation after a positive preflight must STOP.
        self.connection.execute(
            "UPDATE rights_decisions SET commercial_class=? WHERE edition_id=?",
            (e.FINAL_E, e.record_id(GOOD)))
        with self.assertRaises(e.GateError):
            e.authorize_publication_simulation(self.connection, "revocation")


class MigrationContractTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="invented-accepted-shape-")
        self.addCleanup(temp.cleanup)
        self.dir = Path(temp.name)
        self.source = self.dir / "source-fictional.sqlite"
        connection = sqlite3.connect(self.source, isolation_level=None)
        connection.executescript(SOURCE_SCHEMA.read_text(encoding="utf-8"))
        connection.execute("INSERT INTO source_snapshots VALUES(?,?)",
                           ("synthetic", hashlib.sha256(b"fiction").hexdigest()))
        self.rows = []
        for idx in range(17):
            name = f"Invented Reference {idx:03d}.pdf"
            relative = f"fixture-only/record-{idx:03d}.pdf"
            self.rows.append((e.record_id(relative), "synthetic", relative,
                              name, ".pdf", idx))
        connection.executemany(
            "INSERT INTO files VALUES(?,?,?,?,?,?)", self.rows)
        connection.executemany(
            "INSERT INTO editions(record_id) VALUES(?)", [(x[0],) for x in self.rows])
        connection.executemany(
            "INSERT INTO rights_layer_status(record_id) VALUES(?)",
            [(x[0],) for x in self.rows])
        connection.close()

    def open_copy(self):
        path = self.dir / "derived-fictional.sqlite"
        original = self.source.read_bytes()
        result = registry.prepare_work_copy(
            self.source, path,
            expected_sha256=hashlib.sha256(original).hexdigest(),
            expected_rows=len(self.rows))
        self.assertEqual(original, self.source.read_bytes())
        return sqlite3.connect(path, isolation_level=None), result

    def test_synthetic_copy_migrate_preserves_source_counts_and_keys(self):
        conn, receipt = self.open_copy()
        self.addCleanup(conn.close)
        self.assertEqual(receipt["files"], 17)
        self.assertEqual(receipt["editions"], 17)
        self.assertEqual(receipt["foreign_key_violations"], 0)
        self.assertEqual(receipt["integrity_check"], "ok")
        self.assertEqual(
            {r[0] for r in conn.execute("SELECT record_id FROM files")},
            {x[0] for x in self.rows})
        self.assertEqual(registry.registry_counts(conn),
                         {"migrated": True, "evidence": 0, "licenses": 0, "reviews": 0})
        self.assertEqual(len(registry.find_records(conn, "Reference 01", limit=10)), 7)

    def test_provenance_writes_are_relational_and_pending_by_default(self):
        conn, _ = self.open_copy()
        self.addCleanup(conn.close)
        record_id = self.rows[0][0]
        stamp = "2026-10-16T21:00:00Z"
        registry.record_source(
            conn, source_id="src-1", institution="Fictional Authority",
            url="https://example.invalid/registry", kind="AUTHORITY",
            tier="INVENTED_SYNTHETIC", accessed_utc=stamp)
        registry.record_unverified_evidence(
            conn, evidence_id="ev-1", record_id=record_id,
            source_id="src-1", scope="ORIGINAL_WORK",
            claim_summary="Fictional creator attribution; not a license",
            retrieved_utc=stamp)
        registry.record_pending_review(
            conn, review_id="review-1", record_id=record_id,
            jurisdiction="CL", blockers="Concrete edition not evidenced",
            created_utc=stamp)
        self.assertEqual(registry.registry_counts(conn),
                         {"migrated": True, "evidence": 1, "licenses": 0, "reviews": 1})
        self.assertEqual(conn.execute(
            "SELECT evidence_status FROM lr_evidence WHERE evidence_id='ev-1'"
        ).fetchone()[0], "UNVERIFIED")
        self.assertEqual(conn.execute(
            "SELECT commercial_class FROM lr_rights_reviews "
            "WHERE review_id='review-1'"
        ).fetchone()[0], "E_UNCERTAIN_MANUAL_REVIEW")
        self.assertEqual(registry.verify(conn, expected_rows=17)
                         ["foreign_key_violations"], 0)

    def test_28781_synthetic_accepted_shape_migration_preserves_ids(self):
        conn = sqlite3.connect(self.source, isolation_level=None)
        more = []
        for idx in range(17, 28781):
            name = f"Invented Reference {idx:05d}.pdf"
            relative = f"fixture-only/record-{idx:05d}.pdf"
            more.append((e.record_id(relative), "synthetic", relative,
                         name, ".pdf", idx))
        conn.executemany("INSERT INTO files VALUES(?,?,?,?,?,?)", more)
        conn.executemany("INSERT INTO editions(record_id) VALUES(?)",
                         [(x[0],) for x in more])
        conn.executemany("INSERT INTO rights_layer_status(record_id) VALUES(?)",
                         [(x[0],) for x in more])
        conn.close()
        target = self.dir / "large-fictional-derived.sqlite"
        original_hash = registry.file_sha256(self.source)
        receipt = registry.prepare_work_copy(
            self.source, target,
            expected_sha256=original_hash,
            expected_rows=28781)
        self.assertEqual(receipt["files"], 28781)
        self.assertEqual(receipt["editions"], 28781)
        self.assertEqual(registry.file_sha256(self.source), original_hash)
        restored = sqlite3.connect(target, isolation_level=None)
        try:
            self.assertEqual(registry.verify(restored, expected_rows=28781)
                             ["foreign_key_violations"], 0)
            self.assertEqual(restored.execute(
                "SELECT COUNT(*) FROM lr_rights_reviews").fetchone()[0], 0)
        finally:
            restored.close()

    def test_migration_idempotent_and_digest_locked(self):
        conn, original = self.open_copy()
        self.addCleanup(conn.close)
        second = registry.migrate(conn, expected_rows=17)
        self.assertTrue(second["already_applied"])
        self.assertEqual(second["sql_sha256"], original["sql_sha256"])
        self.assertEqual(
            conn.execute("SELECT COUNT(*) FROM lr_schema_migrations").fetchone()[0],
            1)

    def test_migration_failure_rolls_back_all_additions(self):
        conn = sqlite3.connect(self.source, isolation_level=None)
        self.addCleanup(conn.close)
        with self.assertRaises(registry.MigrationError):
            registry.migrate(conn, expected_rows=17, fail_after=4)
        self.assertEqual(conn.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE name LIKE 'lr_%'"
        ).fetchone()[0], 0)
        self.assertEqual(registry.verify(conn, expected_rows=17)
                         ["integrity_check"], "ok")

    def test_fk_and_not_null_enforced(self):
        conn, _ = self.open_copy()
        self.addCleanup(conn.close)
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("INSERT INTO lr_sources "
                     "(source_id,institution,url,kind,tier,accessed_utc)"
                     "VALUES(?,?,?,?,?,?)",
                     ("source", "Invented Library",
                      "https://example.invalid/source",
                      "IDENTITY", "LIBRARY", "2026-10-16T00:00:00Z"))
        with self.assertRaises(sqlite3.IntegrityError):
            conn.execute(
                "INSERT INTO lr_evidence "
                "(evidence_id,record_id,source_id,scope,claim_summary,"
                "evidence_status,retrieved_utc) VALUES(?,?,?,?,?,?,?)",
                ("missing-record", "not-a-real-id", "source",
                 "ORIGINAL_WORK", "Invented factual claim",
                 "UNVERIFIED", "2026-10-16T00:00:00Z"))
        self.assertEqual(registry.verify(conn, expected_rows=17)
                         ["foreign_key_violations"], 0)

    def test_wrong_source_hash_and_existing_target_are_rejected(self):
        with self.assertRaises(registry.MigrationError):
            registry.prepare_work_copy(
                self.source, self.dir / "invalid.sqlite",
                expected_sha256="0" * 64, expected_rows=17)
        self.assertFalse((self.dir / "invalid.sqlite").exists())
        with self.assertRaises(registry.MigrationError):
            registry.prepare_work_copy(
                self.source, self.source,
                expected_rows=17)

    def test_public_cli_synthetic_compatibility_and_source_readonly(self):
        import subprocess
        import sys

        conn, _ = self.open_copy()
        conn.close()
        target = self.dir / "derived-fictional.sqlite"
        args = [sys.executable, "-m", "tools.editorial_pipeline_prototype.cli",
                "--db", str(target), "rights-registry-summary"]
        result = subprocess.run(args, check=True, capture_output=True, text=True)
        self.assertEqual(json.loads(result.stdout)["migrated"], True)
        args = [sys.executable, "-m", "tools.editorial_pipeline_prototype.cli",
                "--db", str(self.source), "rights-verify",
                "--expected-rows", "17"]
        result = subprocess.run(args, check=True, capture_output=True, text=True)
        self.assertEqual(json.loads(result.stdout)["files"], 17)
        # The legacy CSV -> brand-new DB CLI is synthetic-only.
        prohibited = subprocess.run(
            [sys.executable, "-m", "tools.editorial_pipeline_prototype.cli",
             "--db", str(self.source), "init"],
            capture_output=True, text=True)
        self.assertNotEqual(prohibited.returncode, 0)
        self.assertIn("--synthetic-fixture", prohibited.stderr)

    def test_wrong_counts_cannot_migrate(self):
        conn = sqlite3.connect(self.source, isolation_level=None)
        self.addCleanup(conn.close)
        with self.assertRaises(registry.MigrationError):
            registry.migrate(conn, expected_rows=28781)


if __name__ == "__main__":
    unittest.main()
