# Production Readiness Checklist

This checklist is specific to the QA Audit Platform in this repository and should be completed before official use.

## 1. Access Control

- Confirm each account can log in only with the intended credentials.
- Verify `admin` can access Home, Tool, and Dashboard in `home.py`.
- Verify `supervisor` can access Home, Tool, and Dashboard in `home.py`.
- Verify `auditor` can log in and use the unified interface in `home.py`.
- Verify direct access to `dashboard.py` is blocked for auditor accounts.
- Verify direct access to protected pages is blocked when not authenticated.
- Verify logout clears active access and returns the user to the login screen.

## 2. Assignment Integrity

- Confirm supervisors can assign calls only from the intended source folder.
- Confirm assigned calls are written correctly to `Call_Assignments/call_assignments.xlsx`.
- Confirm assigned calls shown in Tool match the rows written to the assignment file.
- Confirm sampled calls for audit come only from assigned calls.
- Confirm completed calls no longer appear as unfinished assigned calls.
- Confirm reassignment behavior works correctly when "Allow reassigning" is off.

## 3. Audit Workflow

- Load assigned calls and verify the selected calls match the assignment list.
- Complete an audit with realistic metadata and confirm the save succeeds.
- Verify saved audit logs are written to `Audit_log_calls/audit_log_*.xlsx`.
- Verify comments, scores, and metadata persist correctly in the saved file.
- Verify `Not Applicable (N/A)` handling does not break save logic.
- Verify the dummy auto-fill test feature is not used for live production audits.

## 4. Dashboard Accuracy

- Confirm the dashboard reads all expected audit log files.
- Verify totals, averages, agent counts, comments counts, and unfinished call counts against source data.
- Confirm the quality metrics chart percentages match the underlying audit records.
- Verify date, agent, and score filters behave correctly.
- Verify direct `dashboard.py` access is limited to `admin` and `supervisor`.
- Export the Excel report and confirm all sheets open without corruption.
- Verify Sheet 5 charts are readable, correctly sized, and show percentage score axes.

## 5. Data Safety

- Back up `Call_Assignments/call_assignments.xlsx` before go-live.
- Back up the `Audit_log_calls` folder before go-live.
- Verify the app can recover cleanly if it is closed during an audit session.
- Test two simultaneous users saving data to identify Excel write conflicts.
- Confirm no dummy or test audit logs remain in live reporting folders before release.

## 6. Security Review

- Remove hardcoded production passwords from source files before official use.
- Replace hardcoded cookie keys and weak secrets with environment-managed values.
- Confirm no secrets are committed to git history.
- Review all text fields for Excel formula injection risk (`=`, `+`, `-`, `@`).
- Test unusual input in comments, caller names, phone numbers, and organization fields.
- Run dependency checks such as `pip-audit` before release.

## 7. Performance And Reliability

- Test with a realistic number of assignment rows.
- Test with a realistic number of audit log files.
- Measure time to load Home, Tool, and Dashboard views.
- Measure time to save an audit log and generate the Excel report.
- Verify the app remains responsive with large datasets and repeated filtering.

## 8. Go-Live Signoff

- Complete one full supervisor-to-auditor-to-dashboard workflow using non-test data.
- Remove dummy output files from live folders.
- Confirm backups exist and restoration steps are documented.
- Confirm only approved user accounts are present.
- Confirm stakeholders approve dashboard numbers and report exports.

## Recommended Pre-Launch Commands

Run these from the repository root:

```powershell
pip install -r requirements.txt
pip-audit
python smoke_test_core_workflow.py
git status
```

## Recommended Final Manual Test

1. Log in as supervisor.
2. Assign calls to an auditor.
3. Log in as that auditor and complete an audit.
4. Log back in as supervisor or admin.
5. Verify the dashboard and Excel export reflect that audit correctly.
