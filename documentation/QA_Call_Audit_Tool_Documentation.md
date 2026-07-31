# QA Call Audit Tool Project Documentation

## Executive Summary

This project delivers a role-based solution for auditing call center interactions, enabling quality assurance teams to assign work, select and review call recordings, score audits against a benchmark, and analyze results.

The platform has been consolidated into a **single Streamlit application, `home.py`**, which is the one app to run day-to-day. It combines everything that used to be split across two separate scripts:
- **QA Audio Call Selector** (formerly `tool.py`) — supervisor call assignment, auditor call selection, and the audit form.
- **QA Audit Dashboard** (formerly `dashboard.py`) — visualizing, analyzing, and exporting audit results.

`tool.py` and `dashboard.py` are kept in the repository as standalone legacy references/backups, but are no longer required for normal use — `home.py` supersedes both.

---

## Login & Role-Based Access (RBAC)

`home.py` requires login (via `streamlit-authenticator`) before any content is shown. Each account maps to one of three roles, defined in a static `role_map` in code:

| Role | Sees in Tool mode | Sees in Dashboard mode |
|---|---|---|
| **admin** | Full audio call selector (folder/upload + sampling) | Full dashboard, all 6 tabs |
| **supervisor** | "Supervisor Dashboard — Call Assignment" panel, plus the full call selector | Full dashboard, all 6 tabs |
| **auditor** | Only their own assigned, unfinished calls (see below) | Full dashboard, all 6 tabs |

A session cookie (`streamlit-authenticator` + `extra-streamlit-components`) keeps the user logged in across reruns for a limited number of days.

---

## Key Features & Workflow

### 1. Home Mode
- Landing page with quick links into Tool and Dashboard mode.
- "Quick Stats" panel: total calls, average score, agent count, and days of data, computed from all saved audit logs.

### 2. Tool Mode — Call Assignment & Audit

**Supervisor Dashboard — Call Assignment** (supervisors only):
- Select how many auditors participate and which ones.
- Set the number of calls to allocate to each auditor.
- Point at a source folder of recordings (defaults to `New call list/`) and assign calls — previously assigned calls are excluded unless "allow reassigning" is checked.
- Assignments are appended to a persistent record at `Call_Assignments/call_assignments.xlsx` (columns include `Auditor`, `Auditor_Email`, `File_Name`, `Agent`, `Contact`, `Assigned_By`, `Assigned_At`, `Status`).
- View the latest assignment batch (with an Excel download) and the full assignment history on record.

**Auditor call restriction** (auditors only):
- Auditors do **not** see the folder/upload picker — they cannot browse or pull arbitrary new calls.
- Their working set is built entirely from `Call_Assignments/call_assignments.xlsx`, filtered to their own account.
- "Unfinished" calls are determined by cross-referencing assigned `File_Name`s against every saved audit log in `Audit_log_calls/` — any assigned call that has already been audited (or marked N/A) drops off the list automatically.
- All of an auditor's unfinished assigned calls load in one step ("📝 Load My Assigned Calls") — no random sampling, since the pool is already scoped to what's actually theirs to do.

**Audio Call Selector & Audit Form** (all roles, using their respective call pool):
- Input via folder path or direct file upload (non-auditors), or the auditor's assigned pool (auditors).
- Automatic Agent/Date extraction from filenames (format: `AgentName_CallID_YYYY-MM-DD_...`).
- Sampling: Pure Random or Stratified by Agent (non-auditors).
- Structured audit form per call: caller metadata, benchmark-aligned quality questions with weighted scores, N/A handling, and free-text comments.
- **Save Audit Log** writes a timestamped Excel file to `Audit_log_calls/audit_log_YYYY-MM-DD_HH-MM-SS.xlsx`, plus an in-app summary (average score, per-agent stats, bar chart).

### 3. Dashboard Mode — Analytics & Reporting

Loads and combines every file in `Audit_log_calls/`, then offers sidebar filters (date range, agent, score range) and four top-line metrics (total calls, average score, unique agents, comments provided).

Six tabs:
1. **📈 Overview** — score distribution histogram and an average-score gauge.
2. **👥 Agent Performance** — average score and call count per agent, plus a summary table.
3. **📅 Timeline** — average score and audit volume trended by call date.
4. **📝 Comments** — browsable, score-filterable list of audit comments.
5. **🗂️ Raw Data** — full filtered dataset, plus a rich multi-sheet Excel export:
   - **Sheet 1 (month/year)** — full audit data with colored headers, alternating row shading, no gridlines, the company logo embedded in the top-left corner, and live formulas for Total Score / Fatal Flag / Score %.
   - **Individual performance** — average QA score and call count per agent.
   - **Trend** — quality-metric performance broken out by category (Introduction & Conclusion, Problem Solving, Soft Skills), plus fatal-call count.
   - **Team performance** — the same categorized metrics laid out for team-wide comparison.
   - **Charts & Summary** — bar charts for overall and per-category performance, color-coded by performance band.
6. **🕒 Unfinished Calls** — supervisor-facing completion tracking:
   - Cross-references `Call_Assignments/call_assignments.xlsx` against every completed audit log to compute what's still outstanding.
   - Top-line metrics: total unfinished calls, total assigned calls, overall % unfinished.
   - A per-auditor summary table (**Auditor Name | Unfinished Calls | Total Assigned Calls | % Unfinished**), sorted worst-first.
   - A detail table of every individual unfinished call.
   - Persists a snapshot (auditor name included) to `unfinished calls/unfinished_calls.xlsx` on every view.

---

## Data & Folder Layout

| Folder | Contents |
|---|---|
| `Audit_log_calls/` | One timestamped `.xlsx` per saved audit batch — the source of truth for all Dashboard analytics. |
| `Call_Assignments/` | `call_assignments.xlsx` — the full history of supervisor → auditor call assignments. |
| `unfinished calls/` | `unfinished_calls.xlsx` — latest snapshot of outstanding (unaudited) assigned calls, refreshed each time the Unfinished Calls tab is viewed. |
| `New call list/` | Default source folder supervisors assign new calls from. |
| `Logos/` | `logo.png` (and `logo_white.png`) used in the sidebar, the Home page, and embedded in the Sheet 1 Excel export. |

---

## Benchmark Alignment

- **Audit Questions:** All questions and their point weights match the provided benchmark, ensuring consistent, fair evaluation across auditors.
- **Scoring Logic:** Each "Yes" answer contributes its benchmark weight to the call's Total Score (out of 100); N/A and Fatal responses are handled explicitly, including in the live Excel formulas.
- **Dashboard Analysis:** All analytics, tabs, and exports reflect this same benchmark scoring — there is one scoring system shared across audit entry and reporting.

---

## Impact & Value

- **Single point of entry:** One login, one app (`home.py`), for supervisors, auditors, and admins — no more juggling separate scripts.
- **Accountability:** Auditors can only work their own assigned calls, and supervisors can see exactly what's outstanding and by whom, in real time.
- **Efficiency:** Automates assignment, sampling, scoring, and reporting, saving time for QA teams.
- **Accuracy:** Ensures audits are scored according to the benchmark, with clear documentation and traceability.
- **Actionable Insights:** Enables data-driven decisions for training, process improvement, and quality assurance.
- **Professional Presentation:** The multi-sheet Excel export (formulas, colors, logo, charts) is suitable for both internal and external reporting.

---

## How to Run

**Recommended — single app:**
```powershell
streamlit run home.py
```
or double-click `run_selector.bat` (already points at `home.py`).

**Legacy (kept for reference only):**
```powershell
streamlit run dashboard.py   # or run_dashboard.bat
streamlit run tool.py
```

**Install dependencies:**
```powershell
pip install -r requirements.txt
```
or double-click `install_dependencies.bat`.

---

## How to Present This Document

1. **Open this file in VS Code or any Markdown editor.**
2. **Copy and paste the content into Microsoft Word.**
3. **Use Word's formatting tools to add a cover page, table of contents, or images if desired.**
4. **Save and share the document as a .docx file for your boss.**

---

## Appendix: File Locations

- **Primary app (run this):**
  - `home.py`
- **Legacy standalone apps (reference only):**
  - `tool.py` — original QA Audio Call Selector
  - `dashboard.py` — original QA Audit Dashboard
- **Documentation:**
  - `QA_Call_Audit_Tool_Documentation.md` (this file)
  - `DOCUMENTATION.md` (detailed technical reference — pending refresh)
  - `README.md` (quick-start guide — pending refresh)

---

**For further details, see `DOCUMENTATION.md` for line-by-line explanations.**
