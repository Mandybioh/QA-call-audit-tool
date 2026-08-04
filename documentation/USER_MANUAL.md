# QA Audit Platform User Manual

## 1. Purpose

This manual is for day-to-day users of the QA Audit Platform. It explains how to log in, navigate the app, complete audits, assign calls, and use dashboard reports.

## 2. Accessing the Platform

1. Open the app in your browser at the platform URL provided by your team.
2. Enter your username and password.
3. After login, you will land on the Home page.

If login fails, contact your supervisor or administrator to confirm your account access.

## 3. Navigation Overview

Use the left sidebar to switch between:

- Home
- Tool
- Dashboard (visible for roles with dashboard access)

The sidebar also shows your role and includes the Logout button.

## 4. Home Page

The Home page provides:

- Quick navigation cards to Tool and Dashboard
- Platform information
- Quick Stats from existing audit logs

Use this page as your starting point each session.

## 5. Tool Page

The Tool page behavior changes by role.

### 5.1 Supervisor workflow (Call Assignment)

1. Open Tool.
2. Select participating auditors.
3. Set number of calls per auditor.
4. Confirm the call source folder.
5. Click Assign Calls.
6. Review the latest assignment batch.
7. Optionally download the assignment batch Excel file.

Notes:

- Assignments are stored in Call_Assignments/call_assignments.xlsx.
- If reassigning is disabled, already assigned calls are excluded.

### 5.2 Auditor workflow (Audit assigned calls)

1. Open Tool.
2. Click Load My Assigned Calls.
3. Review each call shown in your queue.
4. Complete all required metadata and quality questions.
5. Add optional comments.
6. Click Save Audit Log.

Notes:

- Auditors only work on calls assigned to their account.
- Completed calls are removed from unfinished queues automatically.

### 5.3 Completing the audit form

For each selected call:

1. Verify call metadata.
2. Score each quality metric as instructed.
3. Fill mandatory text fields.
4. Mark N/A only where appropriate.
5. Save when all required entries are complete.

## 6. Dashboard Page

The Dashboard is used for analysis and reporting.

### 6.1 Filters

Use sidebar filters to narrow data by:

- Date range
- Agent
- Score range

### 6.2 Tabs

Main tabs include:

- Overview
- Agent Performance
- Timeline
- Comments
- Raw Data
- Unfinished Calls

### 6.3 Exporting reports

1. Open Raw Data tab.
2. Apply desired filters first.
3. Use the export button to generate the Excel report.

## 7. Saving and Data Locations

Generated and updated files are stored in:

- Audit logs: Audit_log_calls/
- Assignments: Call_Assignments/
- Unfinished call snapshots: unfinished calls/

Do not rename these folders unless your administrator updates app configuration accordingly.

## 8. Logout

Always click Logout from the sidebar before closing the browser.

This helps prevent session confusion on shared machines.

## 9. Common Issues

### 9.1 I cannot see calls in Tool

- Confirm you are logged into the correct account.
- For auditors, confirm calls are assigned to your email.
- Ask supervisor to verify assignment records.

### 9.2 Save Audit Log does not work

- Confirm all required fields are completed.
- Check for invalid date or score entries.
- Retry once after refresh.

### 9.3 Dashboard looks empty

- Ensure audit logs exist in Audit_log_calls/.
- Clear filters and check again.
- Confirm the selected date range includes available records.

## 10. Best Practices

- Complete audits in one session when possible.
- Use consistent scoring standards across auditors.
- Keep comments specific and actionable.
- Supervisors should review unfinished calls regularly.

## 11. Support

If you need help:

1. Capture a screenshot of the issue.
2. Note the time and your username.
3. Share the details with your supervisor or platform admin.

## 12. Performance Test Checklist

Use this checklist when verifying app efficiency before production or after major changes.

|Test Area|Steps|Target|Actual|Pass/Fail|Notes|
|---|---|---|---|---|---|
|Tool load time|Open Tool from Home and wait until controls are usable.|<= 3 sec||||
|Auto-fill speed|Select calls, click Auto-fill Dummy Test Data, wait for success message.|<= 2 sec for 20 calls||||
|Save audit speed|Click Save Audit Log after auto-fill and wait for success message.|<= 5 sec for 20 calls||||
|Dashboard load time|Open Dashboard and wait for charts + tabs to render.|<= 5 sec||||
|Filter response time|Change date/agent/score filters and observe update delay.|<= 2 sec per change||||
|Export generation time|Export report from Raw Data tab and wait for download readiness.|<= 10 sec||||
|Multi-user save reliability|Two users save within 1 minute of each other.|No save failure/corruption||||
|Unfinished calls accuracy|Confirm completed files drop from unfinished list.|100% accurate||||

### 12.1 Recommended Test Volumes

- Small: 10 to 20 selected calls
- Medium: 50 selected calls
- Large: 100 selected calls

### 12.2 Minimum Evidence to Keep

- Screenshot of each major test result
- Exported sample report file
- Test date, tester name, and environment (local/production)

---

Version: 1.0  
Last Updated: 2026-08-04
