"""All titles/paths/data here are INVENTED; never load the private library in CI."""
import csv
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools.editorial_pipeline_prototype import engine as e

P = Path(e.__file__).parent
CSV = P / "fixtures" / "synthetic_catalog.csv"
RIGHTS = P / "fixtures" / "synthetic_rights.json"
GOOD = "fixture/fiction/Invented River Fables.pdf"
TRANSLATION = "fixture/fiction/Indigo Lantern Translation.epub"
UNKNOWN = "fixture/fiction/Unknown Moon Notes.pdf"
ND = "fixture/fiction/Copper Birds ND.txt"
BY = "fixture/fiction/Emerald Orchard BY.txt"
NC = "fixture/fiction/Paper Mountains NC.pdf"
UNICODE = "fixture/second/Árbol Unicode Duplicate-title.pdf"


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="synthetic-only-")
        self.addCleanup(self.temp.cleanup)
        self.db = Path(self.temp.name) / "test.sqlite"
        self.cx = e.connect(self.db)
        self.addCleanup(self.cx.close)
        e.init_db(self.cx)
        e.import_catalog(self.cx, CSV)

    def rights(self):
        e.import_rights(self.cx, RIGHTS)

    def test_import_source_sha_idempotent_integrity(self):
        first = e.import_catalog(self.cx, CSV)
        self.assertTrue(first["idempotent"])
        self.assertEqual(first["snapshot_id"], e.sha256(CSV))
        self.assertEqual(e.verify(self.cx)["foreign_key_violations"], 0)
        self.assertEqual(e.verify(self.cx)["integrity_check"], ["ok"])
        self.assertEqual(e.summary(self.cx)["files"], 7)

    def test_unicode_exact_path_and_duplicate_title_safety(self):
        with self.cx:
            self.cx.execute("UPDATE files SET name='Invented River Fables.pdf' WHERE relative_path=?",
                            (UNICODE,))
        self.assertNotEqual(e.record_id(GOOD), e.record_id(UNICODE))
        self.assertEqual(self.cx.execute("SELECT count(*) FROM files WHERE name=?",
                                         ("Invented River Fables.pdf",)).fetchone()[0],2)
        self.assertEqual(e.rights_status(self.cx,UNICODE)["class"],e.FINAL_E)

    def test_import_rollback_on_duplicate_or_unsafe_catalog(self):
        bad = Path(self.temp.name) / "bad.csv"
        with bad.open("w",newline="",encoding="utf-8") as out:
            w=csv.writer(out);w.writerow(e.HEADERS)
            w.writerow(("A","txt",1,"test/x.txt","test"))
            w.writerow(("B","txt",1,"test/x.txt","test"))
        with self.assertRaises(ValueError):
            e.import_catalog(self.cx,bad)
        with bad.open("w",newline="",encoding="utf-8") as out:
            w=csv.writer(out);w.writerow(e.HEADERS)
            w.writerow(("A","txt",1,"../unsafe/x.txt","test"))
        with self.assertRaises(ValueError):
            e.import_catalog(self.cx,bad)
        self.assertEqual(e.summary(self.cx)["files"],7)

    def test_default_E_when_no_rights(self):
        self.assertEqual(e.rights_status(self.cx,GOOD)["class"],e.FINAL_E)
        with self.assertRaises(e.GateError):
            e.start_project(self.cx,GOOD,"p", "CL")

    def test_two_layers_vs_modern_translation(self):
        self.rights()
        self.assertEqual(e.rights_status(self.cx, GOOD)["class"],e.FINAL_A)
        self.assertEqual(e.rights_status(self.cx, TRANSLATION)["class"],
                         "D_RIGHTS_RESERVED_OR_PERMISSION_REQUIRED")
        self.assertEqual(e.rights_status(self.cx, UNKNOWN)["class"],e.FINAL_E)
        with self.assertRaises(e.GateError):
            e.start_project(self.cx,TRANSLATION,"blocked-translation","CL")
        with self.assertRaises(e.GateError):
            e.start_project(self.cx,UNKNOWN,"unknown","CL")

    def test_nd_but_not_adaptable_and_nc_not_commercial(self):
        self.rights()
        self.assertEqual(e.rights_status(self.cx,ND)["class"],e.FINAL_B)
        self.assertEqual(e.rights_status(self.cx,NC)["class"],"C_NONCOMMERCIAL_ONLY")
        self.assertFalse(e.eligibility(self.cx,e.record_id(ND),"CL")
                         ["derivative_adaptation_rights_verified"])
        with self.assertRaises(e.GateError):
            e.start_project(self.cx,ND,"nd","CL")
        with self.assertRaises(e.GateError):
            e.start_project(self.cx,NC,"nc","CL")

    def test_attribution_conditional_B_and_territory(self):
        self.rights()
        self.assertEqual(e.rights_status(self.cx,BY)["class"],e.FINAL_B)
        self.assertEqual(e.start_project(self.cx,BY,"cc-by","CL")
                         ["attribution_obligations"],True)
        with self.assertRaises(e.GateError):
            e.start_project(self.cx,BY,"us","US")

    def test_adaptation_requires_independent_derivative_evidence(self):
        data=json.loads(RIGHTS.read_text(encoding="utf-8"))
        data["editions"][0]["evidence"].pop("DERIVATIVE")
        patch=Path(self.temp.name)/"with-no-derivative.json"
        patch.write_text(json.dumps(data),encoding="utf-8")
        e.import_rights(self.cx,patch)
        self.assertFalse(e.eligibility(self.cx,e.record_id(GOOD),"CL")
                         ["derivative_adaptation_rights_verified"])
        with self.assertRaises(e.GateError):
            e.start_project(self.cx,GOOD,"p","CL")

    def test_territory_evidence_required_separate_from_list(self):
        data=json.loads(RIGHTS.read_text(encoding="utf-8"))
        data["editions"][0]["evidence"].pop("TERRITORY")
        patch=Path(self.temp.name)/"without-territory-proof.json"
        patch.write_text(json.dumps(data),encoding="utf-8")
        e.import_rights(self.cx,patch)
        with self.assertRaises(e.GateError):
            e.start_project(self.cx,GOOD,"p","CL")

    def test_unverified_evidence_fails_closed(self):
        data=json.loads(RIGHTS.read_text(encoding="utf-8"))
        data["editions"][0]["evidence"]["EDITION"]["status"]="UNVERIFIED"
        patch=Path(self.temp.name)/"unverified.json"
        patch.write_text(json.dumps(data),encoding="utf-8")
        e.import_rights(self.cx,patch)
        self.assertEqual(e.rights_status(self.cx,GOOD)["class"],e.FINAL_E)
        with self.assertRaises(e.GateError):
            e.start_project(self.cx,GOOD,"p","CL")

    def test_import_rights_atomic_rollback(self):
        self.rights()
        before=e.rights_status(self.cx,GOOD)
        data=json.loads(RIGHTS.read_text(encoding="utf-8"))
        data["editions"][1]["evidence"]["UNDERLYING"]["source_url"]="http://unsafe.test/"
        patch=Path(self.temp.name)/"bad-rights.json"
        patch.write_text(json.dumps(data),encoding="utf-8")
        with self.assertRaises(ValueError):
            e.import_rights(self.cx,patch)
        self.assertEqual(e.rights_status(self.cx,GOOD),before)
        self.assertEqual(e.verify(self.cx)["integrity_check"],["ok"])

    def test_human_review_and_preflight_separate(self):
        self.rights();e.start_project(self.cx,GOOD,"p","CL")
        e.simulate_editorial(self.cx,"p","AI_ASSISTED",differentiation="ORIGINAL_ANNOTATIONS")
        report=e.preflight(self.cx,"p",public_domain_free_version=True)
        self.assertNotEqual(report["state"],e.PRE_PUBLICATION)
        with self.assertRaises(e.GateError):
            e.set_review_gate(self.cx,"p","human_legal_approval",True)
        with self.assertRaises(e.GateError):
            e.authorize_publication_simulation(self.cx,"p")
        for gate in ("human_legal_approval","editorial_qa_approval","kdp_policy_preflight"):
            e.set_review_gate(self.cx,"p",gate,True,synthetic_attestation=True)
        report=e.preflight(self.cx,"p",public_domain_free_version=True)
        self.assertEqual(report["state"],e.PRE_PUBLICATION)
        self.assertFalse(report["checklist"]["human_publish_authorization"])
        self.assertFalse(report["external_kdp_publication_performed"])
        with self.assertRaises(e.GateError):
            e.authorize_publication_simulation(self.cx,"p")
        e.set_review_gate(self.cx,"p","human_publish_authorization",True,
                          synthetic_attestation=True)
        self.assertFalse(e.authorize_publication_simulation(self.cx,"p")
                         ["actual_publication_or_upload"])

    def test_kdp_PD_differentiation_preflight_gate(self):
        self.rights();e.start_project(self.cx,GOOD,"p","CL")
        e.simulate_editorial(self.cx,"p","HUMAN_CREATED",differentiation="NOT_EVALUATED")
        for gate in ("human_legal_approval","editorial_qa_approval","kdp_policy_preflight"):
            e.set_review_gate(self.cx,"p",gate,True,synthetic_attestation=True)
        status=e.preflight(self.cx,"p",public_domain_free_version=True)
        self.assertEqual(status["state"],"STOP_RIGHTS_OR_KDP_GATES")
        self.assertFalse(status["checklist"]["KDP_public_domain_differentiation"])

    def test_AI_generated_disclosure_vs_assisted(self):
        self.rights();e.start_project(self.cx,GOOD,"p","CL")
        e.simulate_editorial(self.cx,"p","AI_GENERATED",
                             differentiation="ORIGINAL_TRANSLATION")
        row=self.cx.execute("SELECT ai_generated_disclosure FROM editorial_projects "
                            "WHERE project_id='p'").fetchone()
        self.assertEqual(row[0],1)
        e.simulate_editorial(self.cx,"p","AI_ASSISTED",differentiation="NOT_REQUIRED")
        row=self.cx.execute("SELECT ai_generated_disclosure FROM editorial_projects "
                            "WHERE project_id='p'").fetchone()
        self.assertEqual(row[0],0)

    def test_rights_revalidation_before_editorial_simulation(self):
        self.rights();e.start_project(self.cx,GOOD,"p","CL")
        with self.cx:
            self.cx.execute("UPDATE rights_decisions SET commercial_class=? "
                            "WHERE edition_id=?", (e.FINAL_E,e.record_id(GOOD)))
        with self.assertRaises(e.GateError):
            e.simulate_editorial(self.cx,"p","AI_GENERATED")

    def test_report_and_cli_demo(self):
        self.rights()
        path=Path(self.temp.name)/"public-synthetic-report.json"
        r=e.export_report(self.cx,path)
        self.assertEqual(len(r["sha256"]),64)
        self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["summary"]["files"],7)
        proc=subprocess.run([sys.executable,"-m","tools.editorial_pipeline_prototype.cli","demo"],
                            capture_output=True,text=True,check=True)
        self.assertEqual(json.loads(proc.stdout)["state"],e.PRE_PUBLICATION)

    def test_mass_import_28781_invented_distinct_paths(self):
        path=Path(self.temp.name)/"synthetic-large.csv"
        with path.open("w",encoding="utf-8",newline="") as f:
            w=csv.writer(f);w.writerow(e.HEADERS)
            for idx in range(28781):
                w.writerow([f"Fiction {idx:05d}.pdf",".pdf",idx,
                            f"fixture/unreal/p_{idx:05d}.pdf","fixture/unreal"])
        other=e.connect(Path(self.temp.name)/"scale.sqlite")
        self.addCleanup(other.close)
        e.init_db(other)
        loaded=e.import_catalog(other,path)
        self.assertEqual(loaded["rows"],28781)
        self.assertTrue(e.import_catalog(other,path)["idempotent"])
        self.assertEqual(e.summary(other)["classes"],{e.FINAL_E:28781})
        self.assertEqual(e.verify(other)["integrity_check"],["ok"])


if __name__ == "__main__":
    unittest.main()
