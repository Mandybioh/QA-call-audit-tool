# QA Call Audit Tool Project Documentation

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

### tool.py â€” QA Audio Call Selector

- **Imports:** Loads Streamlit, pandas, OS utilities, datetime, regex, and Plotly for UI, data, and charts.
- **Session State:** Initializes variables to store uploaded files and user input.
- **Input Method:** Lets users choose between folder selection and file upload.
- **File Handling:** Saves uploaded files to a temporary directory and lists audio files for review.
- **Data Preparation:** Extracts agent and date info from filenames, prepares DataFrame with all audit fields.
- **Sampling:** Selects calls for audit using random or stratified methods.
- **Audit Form:** Displays audio playback, metadata, and audit questions (with scores) for each call.
- **Scoring:** Calculates total score per call based on benchmark weights.
- **Saving:** Exports audit results to Excel, displays summary and statistics.

### dashboard.py â€” QA Audit Dashboard

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




Project Overview
This project consists of two main components:
* tool.py: The QA Audio Call Selector, used for uploading/selecting call recordings, auditing calls, and saving audit results.
* dashboard.py: The QA Audit Dashboard, used for visualizing, analyzing, and exporting audit results.

tool.pyÿ? QA Audio Call Selector
Imports and Setup
* import streamlit as st: Loads Streamlit, the web app framework used for UI.
* import os, random, pandas as pd: Loads OS utilities, random sampling, and pandas for data manipulation.
* from datetime import datetime: For timestamping audit logs.
* import re: For regular expressions, used in filename parsing.
* import plotly.express as px: For generating charts (used in summary).
* st.set_page_config(...): Sets the page title and layout for the Streamlit app.
* st.title(...): Displays the app title


Session State Initialization
* Checks ifÿ'uploaded_files_folder'ÿexists in session state; if not, initializes it toÿNone. This is used to store the temporary directory for uploaded files.
Input Method Selection
* input_method = st.radio(...): Lets the user choose between selecting a folder or uploading files.
* If folder path is chosen, a text input is shown for the folder path.
* If upload is chosen, a file uploader is shown for audio files (MP3, WAV, M4A).
File Handling
* If files are uploaded, they are saved to a temporary directory.
* The app displays success or info messages based on the upload status.
File Discovery
* If a valid folder path is provided, the app lists all audio files in the folder.
* If no files are found, a warning is shown.
Data Preparation
* Creates a DataFrame (df) with file names.
* Extracts agent names and call dates from filenames using regular expressions.
* Initializes all columns required for the audit, including metadata and audit questions.
Audit Sampling
* Lets the user choose between pure random or stratified sampling by agent.
* Selects a sample of calls for auditing based on the chosen method.

Audit Form
* For each selected call, displays metadata and audit questions.
* Initializes session state for each field to preserve user input.
* Audit questions and their scores are aligned with the provided benchmark (e.g., "Did CCO open the call using the appropriate greetings?" ? 3 points).
* Uses selectboxes and text inputs for user responses.
Audit Log Saving
* When the user clicks "Save Audit Log":
o Updates the DataFrame with user responses.
o Calculates the total score for each call based on the benchmark weights.
o Saves the audit log as an Excel file with a timestamped filename.
o Displays a summary and statistics (average score, agent performance, etc.).
Relevance and Impact
* This tool streamlines the QA process for call audits, ensuring consistent scoring and easy data entry.
* The use of session state ensures a smooth user experience.
* The audit log format is designed for seamless integration with the dashboard.

dashboard.pyÿ? QA Audit Dashboard
Imports and Setup
* Loads Streamlit, pandas, Plotly, datetime, glob, io, and openpyxl for UI, data, charts, and Excel export.
* Sets the dashboard page title and layout.
Audit Log Loading
* load_all_audit_logs(): Loads all audit log Excel files matchingÿaudit_log_*.xlsx.
* Combines them into a single DataFrame for analysis.

Sidebar Filters
* Lets users filter by date range (using call date if available), agent, and score range.
* Ensures only relevant records are shown in the dashboard.
Main Metrics
* Displays total calls audited, average score, unique agents, and comments provided.
Tabs
* Overview: Shows score distribution and average score gauge (charts use dark green for visual consistency).
* Agent Performance: Shows agent-wise average scores and call counts.
* Timeline: Shows trends over time using call dates (not audit timestamps).
* Comments: Displays comments provided during audits.
* Raw Data: Shows the underlying audit data.

Excel Export
* Allows users to download the audit data and analytics as a multi-sheet Excel file.
* Each sheet's column headers are styled with a white background and bold dark green font for clarity.
* Includes detailed sheets:
o Audit Log
o Individual Performance
o Quality Metrics Trend (with benchmark weights)
o Team Performance Summary
Relevance and Impact
* The dashboard provides actionable insights into call quality, agent performance, and trends.
* The use of call dates ensures accurate timeline analysis.
* The export feature enables further reporting and sharing.
* Visual and stylistic enhancements improve usability and presentation.

Overall Impact
* Consistency: The audit tool and dashboard are tightly integrated, using a shared data format and scoring system.
* Efficiency: Automates sampling, scoring, and reporting, saving time for QA teams.
* Accuracy: Ensures audits are scored according to the benchmark, with clear documentation and traceability.
* Actionable Insights: The dashboard enables data-driven decisions for training, process improvement, and quality assurance.
* Professional Presentation: Visual and export enhancements make the tool suitable for both internal and external reporting.

