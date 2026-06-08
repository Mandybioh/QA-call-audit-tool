# QA Call Audit Tool — Project Documentation

## Executive Summary

This project delivers a robust solution for auditing call center interactions, enabling quality assurance teams to efficiently select, review, and analyze call recordings. The system consists of two main components:
- **QA Audio Call Selector (tool.py):** For uploading/selecting call recordings, performing audits, and saving results.
- **QA Audit Dashboard (dashboard.py):** For visualizing, analyzing, and exporting audit results.

---

## Key Features & Workflow

### 1. Call Selection & Audit (tool.py)
- **Flexible Input:** Users can select call recordings from a folder or upload files directly.
- **Metadata Extraction:** Automatically extracts agent names and call dates from filenames.
- **Sampling:** Supports pure random and stratified sampling by agent for unbiased audits.
- **Audit Form:** Presents a structured form with benchmark-aligned questions and scoring.
- **Session State:** Remembers user input for seamless experience.
- **Audit Log:** Saves results in timestamped Excel files for traceability and integration.

### 2. Data Visualization & Reporting (dashboard.py)
- **Audit Log Loading:** Combines all audit logs for comprehensive analysis.
- **Filtering:** Filters by call date, agent, and score range for targeted insights.
- **Metrics:** Displays total calls, average score, agent count, and comments.
- **Charts:** Visualizes score distribution, agent performance, and trends over time (using call dates).
- **Export:** Generates a multi-sheet Excel report with styled headers for professional presentation.

---

## Detailed Code Explanation

### tool.py — QA Audio Call Selector

- **Imports:** Loads Streamlit, pandas, OS utilities, datetime, regex, and Plotly for UI, data, and charts.
- **Session State:** Initializes variables to store uploaded files and user input.
- **Input Method:** Lets users choose between folder selection and file upload.
- **File Handling:** Saves uploaded files to a temporary directory and lists audio files for review.
- **Data Preparation:** Extracts agent and date info from filenames, prepares DataFrame with all audit fields.
- **Sampling:** Selects calls for audit using random or stratified methods.
- **Audit Form:** Displays audio playback, metadata, and audit questions (with scores) for each call.
- **Scoring:** Calculates total score per call based on benchmark weights.
- **Saving:** Exports audit results to Excel, displays summary and statistics.

### dashboard.py — QA Audit Dashboard

- **Imports:** Loads Streamlit, pandas, Plotly, openpyxl, and other utilities for UI, data, charts, and Excel export.
- **Audit Log Loading:** Reads all audit logs and combines them for analysis.
- **Filtering:** Sidebar filters for date range (using call date), agent, and score range.
- **Metrics:** Shows key statistics (calls, scores, agents, comments).
- **Tabs:** Provides views for Overview, Agent Performance, Timeline, Comments, and Raw Data.
- **Charts:** Uses dark green color for all main charts for visual consistency.
- **Excel Export:** Creates a multi-sheet report with styled headers (white background, dark green font).

---

## Benchmark Alignment

- **Audit Questions:** All questions and scores match the provided benchmark, ensuring consistent and fair evaluation.
- **Scoring Logic:** Each question contributes its benchmark weight to the total score.
- **Dashboard Analysis:** All analytics and exports reflect the benchmark scoring.

---

## Impact & Value

- **Efficiency:** Automates sampling, scoring, and reporting, saving time for QA teams.
- **Accuracy:** Ensures audits are scored according to the benchmark, with clear documentation and traceability.
- **Actionable Insights:** Enables data-driven decisions for training, process improvement, and quality assurance.
- **Professional Presentation:** Visual and export enhancements make the tool suitable for both internal and external reporting.

---

## How to Present This Document

1. **Open this file in VS Code or any Markdown editor.**
2. **Copy and paste the content into Microsoft Word.**
3. **Use Word's formatting tools to add a cover page, table of contents, or images if desired.**
4. **Save and share the document as a .docx file for your boss.**

---

## Appendix: File Locations
- **Source Code:**
  - tool.py
  - dashboard.py
- **Documentation:**
  - QA_Call_Audit_Tool_Documentation.md (this file)
  - DOCUMENTATION.md (detailed technical reference)

---

**For further details, see the DOCUMENTATION.md file for line-by-line explanations.**
