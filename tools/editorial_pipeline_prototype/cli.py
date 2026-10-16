"""Command line entry point: python -m tools.editorial_pipeline_prototype.cli ..."""
import argparse
import json
import tempfile
from pathlib import Path

from . import engine as e

HERE = Path(__file__).parent
FIXTURE_CSV = HERE / "fixtures" / "synthetic_catalog.csv"
FIXTURE_RIGHTS = HERE / "fixtures" / "synthetic_rights.json"
RIVER = "fixture/fiction/Invented River Fables.pdf"


def main(argv=None):
    p = argparse.ArgumentParser(description="Local SQLite editorial MVP; NO publication or AI calls")
    p.add_argument("--db", help="SQLite database path (local/private only)")
    commands = p.add_subparsers(dest="command", required=True)
    commands.add_parser("init")
    cmd = commands.add_parser("import-catalog")
    cmd.add_argument("--csv", required=True)
    cmd = commands.add_parser("import-rights")
    cmd.add_argument("--json", required=True)
    commands.add_parser("verify")
    commands.add_parser("summary")
    cmd = commands.add_parser("rights-status")
    cmd.add_argument("--relative-path", required=True)
    cmd = commands.add_parser("export-report")
    cmd.add_argument("--out", required=True)
    cmd = commands.add_parser("start-project")
    cmd.add_argument("--relative-path", required=True)
    cmd.add_argument("--project-id", required=True)
    cmd.add_argument("--territory", required=True)
    cmd = commands.add_parser("simulate-editorial")
    cmd.add_argument("--project-id", required=True)
    cmd.add_argument("--origin", required=True,
                     choices=("HUMAN_CREATED", "AI_ASSISTED", "AI_GENERATED"))
    cmd.add_argument("--differentiation", default="NOT_EVALUATED")
    cmd = commands.add_parser("review-gate")
    cmd.add_argument("--project-id", required=True)
    cmd.add_argument("--gate", required=True)
    cmd.add_argument("--passed", choices=("yes", "no"), required=True)
    cmd.add_argument("--synthetic-attestation", action="store_true")
    cmd = commands.add_parser("preflight")
    cmd.add_argument("--project-id", required=True)
    cmd.add_argument("--pd-free-version", action="store_true")
    cmd = commands.add_parser("authorize-publication-simulation")
    cmd.add_argument("--project-id", required=True)
    commands.add_parser("demo")
    args = p.parse_args(argv)
    if args.command == "demo":
        if args.db:
            raise SystemExit("Demo manages its own temporary synthetic DB; omit --db")
        with tempfile.TemporaryDirectory(prefix="editorial-synthetic-") as directory:
            conn = e.connect(Path(directory) / "demo.sqlite")
            try:
                e.init_db(conn)
                e.import_catalog(conn, FIXTURE_CSV)
                e.import_rights(conn, FIXTURE_RIGHTS)
                e.start_project(conn, RIVER, "invented-demo", "CL")
                e.simulate_editorial(conn, "invented-demo", "AI_GENERATED",
                                    differentiation="ORIGINAL_ANNOTATIONS")
                for gate in ("human_legal_approval","editorial_qa_approval",
                             "kdp_policy_preflight"):
                    e.set_review_gate(conn, "invented-demo", gate, True,
                                      synthetic_attestation=True)
                result = e.preflight(conn, "invented-demo", public_domain_free_version=True)
                result["catalog"] = e.summary(conn)
                result["sqlite"] = e.verify(conn)
                print(json.dumps(result, indent=2, ensure_ascii=False))
            finally:
                conn.close()
        return 0
    if not args.db:
        p.error("--db is required for persistent local operations")
    conn = e.connect(args.db)
    try:
        if args.command=="init":out=e.init_db(conn)
        elif args.command=="import-catalog":out=e.import_catalog(conn,args.csv)
        elif args.command=="import-rights":out=e.import_rights(conn,args.json)
        elif args.command=="verify":out=e.verify(conn)
        elif args.command=="summary":out=e.summary(conn)
        elif args.command=="rights-status":out=e.rights_status(conn,args.relative_path)
        elif args.command=="export-report":out=e.export_report(conn,args.out)
        elif args.command=="start-project":out=e.start_project(conn,args.relative_path,args.project_id,args.territory)
        elif args.command=="simulate-editorial":out=e.simulate_editorial(conn,args.project_id,args.origin,args.differentiation)
        elif args.command=="review-gate":
            e.set_review_gate(conn,args.project_id,args.gate,args.passed=="yes",
                              synthetic_attestation=args.synthetic_attestation)
            out={"gate":args.gate,"simulation_only":True}
        elif args.command=="preflight":out=e.preflight(conn,args.project_id,public_domain_free_version=args.pd_free_version)
        elif args.command=="authorize-publication-simulation":out=e.authorize_publication_simulation(conn,args.project_id)
        print(json.dumps(out,indent=2,ensure_ascii=False))
        return 0
    finally:
        conn.close()


if __name__=="__main__":
    raise SystemExit(main())
