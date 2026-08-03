import argparse
import glob
import os
import shutil
import tempfile
from datetime import datetime

import pandas as pd

from excel_sanitization import sanitize_dataframe_for_excel


def _ensure(condition, message):
    if not condition:
        raise AssertionError(message)


def _simulate_supervisor_assignment(base_dir):
    assignments_dir = os.path.join(base_dir, "Call_Assignments")
    os.makedirs(assignments_dir, exist_ok=True)
    assignments_file = os.path.join(assignments_dir, "call_assignments.xlsx")

    assignments = pd.DataFrame([
        {
            "Auditor": "Auditor One",
            "Auditor_Email": "auditor.one@example.com",
            "File_Name": "=dangerous_formula.mp3",
            "Agent": "Agent A",
            "Contact": "1234567890",
            "Assigned_By": "Supervisor",
            "Assigned_By_Email": "supervisor@example.com",
            "Assigned_At": datetime.now().isoformat(),
            "Status": "Assigned",
        },
        {
            "Auditor": "Auditor Two",
            "Auditor_Email": "auditor.two@example.com",
            "File_Name": "normal_call.mp3",
            "Agent": "Agent B",
            "Contact": "0987654321",
            "Assigned_By": "Supervisor",
            "Assigned_By_Email": "supervisor@example.com",
            "Assigned_At": datetime.now().isoformat(),
            "Status": "Assigned",
        },
    ])

    sanitize_dataframe_for_excel(assignments).to_excel(assignments_file, index=False)
    reloaded = pd.read_excel(assignments_file)

    _ensure(len(reloaded) == 2, "Assignment save failed: expected 2 rows.")
    _ensure(str(reloaded.loc[0, "File_Name"]).startswith("'="), "Excel sanitization failed for assignment file name.")
    return assignments_file


def _simulate_auditor_audit(base_dir):
    audit_dir = os.path.join(base_dir, "Audit_log_calls")
    os.makedirs(audit_dir, exist_ok=True)
    audit_file = os.path.join(audit_dir, f"audit_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx")

    audit_rows = pd.DataFrame([
        {
            "Agent": "Agent B",
            "File_Name": "normal_call.mp3",
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Total Score": 88,
            "QA Score": 0.88,
            "Do you have any other comments you would like to share?": "@test comment for injection check",
            "Audit_Timestamp": datetime.now().isoformat(),
        }
    ])

    sanitize_dataframe_for_excel(audit_rows).to_excel(audit_file, index=False)
    reloaded = pd.read_excel(audit_file)

    _ensure(len(reloaded) == 1, "Audit log save failed: expected 1 row.")
    _ensure(
        str(reloaded.loc[0, "Do you have any other comments you would like to share?"]).startswith("'@"),
        "Excel sanitization failed for audit comments.",
    )
    return audit_file


def _simulate_dashboard_verification(base_dir):
    assignments_file = os.path.join(base_dir, "Call_Assignments", "call_assignments.xlsx")
    audit_glob = os.path.join(base_dir, "Audit_log_calls", "audit_log_*.xlsx")

    assignments = pd.read_excel(assignments_file)
    audit_files = glob.glob(audit_glob)
    _ensure(audit_files, "Dashboard verification failed: no audit logs found.")

    audit_data = pd.concat([pd.read_excel(path) for path in audit_files], ignore_index=True)

    _ensure("Total Score" in audit_data.columns, "Dashboard verification failed: Total Score column missing.")
    avg_score = float(audit_data["Total Score"].mean())
    _ensure(0 <= avg_score <= 100, "Dashboard verification failed: average score out of bounds.")

    completed_files = set(audit_data["File_Name"].dropna().astype(str))
    unfinished_df = assignments[~assignments["File_Name"].astype(str).isin(completed_files)].copy()
    _ensure(len(unfinished_df) == 1, "Unfinished call tracking check failed.")

    return {
        "assignment_rows": len(assignments),
        "audit_rows": len(audit_data),
        "avg_score": round(avg_score, 2),
        "unfinished_rows": len(unfinished_df),
    }


def run_smoke_test(target_base_dir=None):
    if target_base_dir:
        base_dir = os.path.abspath(target_base_dir)
        os.makedirs(base_dir, exist_ok=True)
    else:
        base_dir = tempfile.mkdtemp(prefix="qa_audit_smoke_")

    try:
        _simulate_supervisor_assignment(base_dir)
        _simulate_auditor_audit(base_dir)
        summary = _simulate_dashboard_verification(base_dir)

        print("SMOKE TEST PASSED")
        print(f"Workspace: {base_dir}")
        print(f"Assignment rows: {summary['assignment_rows']}")
        print(f"Audit rows: {summary['audit_rows']}")
        print(f"Average score: {summary['avg_score']}")
        print(f"Unfinished rows: {summary['unfinished_rows']}")
        return 0
    except Exception as exc:
        print("SMOKE TEST FAILED")
        print(f"Workspace: {base_dir}")
        print(f"Reason: {exc}")
        return 1
    finally:
        if not target_base_dir and os.path.exists(base_dir):
            shutil.rmtree(base_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="Run the QA Audit Platform core workflow smoke test.")
    parser.add_argument(
        "--workspace",
        default="",
        help="Optional test workspace path. If omitted, the test runs in a temporary workspace.",
    )
    args = parser.parse_args()

    raise SystemExit(run_smoke_test(args.workspace or None))


if __name__ == "__main__":
    main()
