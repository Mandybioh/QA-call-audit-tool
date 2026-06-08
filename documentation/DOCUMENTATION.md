# QA Call Audit Tool Documentation

## Project Overview

This project consists of two main components:
- **tool.py**: The QA Audio Call Selector, used for uploading/selecting call recordings, auditing calls, and saving audit results.
- **dashboard.py**: The QA Audit Dashboard, used for visualizing, analyzing, and exporting audit results.

---

## tool.py — QA Audio Call Selector

### Imports and Setup

```python
import streamlit as st
import os, random, pandas as pd
from datetime import datetime
import re
import plotly.express as px
st.set_page_config(page_title="QA Audio Call Selector", layout="wide")
st.title("🎧 QA Audio Call Selector")
```
- Loads all necessary libraries and sets up the Streamlit app.

### Session State Initialization

```python
if 'uploaded_files_folder' not in st.session_state:
    st.session_state.uploaded_files_folder = None
```
- Ensures a session variable exists to store the temporary directory for uploaded files.

### Input Method Selection

```python
input_method = st.radio("Choose input method:", ["📁 From Folder Path", "📤 Upload Files"], horizontal=True)
folder_path = None
```
- Lets the user choose between selecting a folder or uploading files.

#### Folder Path Option

```python
if input_method == "📁 From Folder Path":
    folder_path = st.text_input("📁 Enter or select folder path containing call recordings:")
```
- If folder path is chosen, displays a text input for the user to enter/select the folder.

#### Upload Files Option

```python
else:
    st.write("**Upload recorded call files (MP3, WAV, M4A)**")
    uploaded_files = st.file_uploader(...)
    if uploaded_files:
        ...
    else:
        st.info("No files uploaded yet. Please select audio files to proceed.")
        folder_path = None
```
- Handles file uploads: saves files to a temporary directory, updates the folder path, and displays status messages.

### File Discovery

```python
if folder_path and os.path.isdir(folder_path):
    files = [f for f in os.listdir(folder_path) if f.lower().endswith((".mp3", ".wav", ".m4a"))]
    if not files:
        st.warning("No audio files found in this folder.")
    else:
        st.success(f"Found {len(files)} recordings.")
```
- Lists all audio files in the selected/uploaded folder and displays status.

### Data Preparation

```python
df = pd.DataFrame({"File_Name": files})
df["Base"] = df["File_Name"].str.rsplit(".", n=1).str[0]
df["Agent"] = df["Base"].str.split("_").str[0].fillna("Unknown").replace("", "Unknown")
# ...extract date logic...
df["Date"] = df["Base"].apply(_extract_date_from_base)
df["Contact"] = df["File_Name"].apply(lambda x: os.path.join(folder_path, x))
```
- Prepares the DataFrame with metadata extracted from filenames.

### Audit Columns Initialization

```python
df["Id"] = range(1, len(df) + 1)
df["Name"] = ""
df["Date of interaction"] = df["Date"]
df["AHT (seconds)"] = ""
df["Name of Call Centre Officer"] = df["Agent"]
# ...other columns...
df["Total Score"] = 0
df["Fatal"] = ""
df["QI Score"] = 0.0
df["Do you have any other comments you would like to share?"] = ""
```
- Initializes all columns needed for the audit, including metadata and audit questions.

### Sampling Type Selection

```python
sampling_type = st.radio("🎯 Sampling Type", ["Pure Random", "Stratified by Agent"])
sample_size = st.number_input("🔢 Number of Calls to Audit", min_value=1, value=5)
```
- Lets the user choose the sampling method and sample size.

### Call Selection

```python
if st.button("🎲 Select Random Calls"):
    ...
    st.session_state.selected = selected.copy()
```
- Selects calls for auditing based on the chosen method and stores them in session state.

### Audit Form Display

```python
if 'selected' in st.session_state:
    selected = st.session_state.selected
    st.subheader("✅ Selected Calls for QA Audit")
    quality_questions = [ ... ]
    for i in selected.index:
        ...
```
- Displays the selected calls for auditing and initializes session state for all fields.

#### Audit Form Widgets

```python
form_data = {}
for i, row in selected.iterrows():
    st.write(f"## 🎙️ Call {i+1}: {row['File_Name']}")
    st.write(f"**Agent:** {row['Agent']} | **Date:** {row['Date']}")
    st.audio(row["Contact"])
    # ...metadata widgets...
    with st.expander("⭐ Quality Metrics (Rate as Yes/No)", expanded=True):
        ...
    with st.expander("📝 Additional Info", expanded=False):
        ...
    st.divider()
```
- Displays widgets for each call, including audio playback, metadata, audit questions, and additional info.

#### Audit Log Saving

```python
if st.button("💾 Save Audit Log"):
    ...
    selected_save.to_excel(filename, index=False)
    st.success(f"Audit selections saved successfully! File: {filename}")
    # ...summary and statistics...
```
- Saves the audit log, calculates scores, displays summaries, and handles errors.

---

## dashboard.py — QA Audit Dashboard

### Imports and Setup

```python
import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import glob
import io
from openpyxl.chart import BarChart, Reference
```
- Loads all necessary libraries for UI, data, charts, and Excel export.

### Audit Log Loading

```python
def load_all_audit_logs():
    audit_files = glob.glob("audit_log_*.xlsx")
    ...
    return combined_df
```
- Loads all audit log Excel files and combines them into a single DataFrame for analysis.

### Sidebar Filters

```python
st.sidebar.header("🔍 Filters")
# ...date range, agent, score filters...
```
- Lets users filter by date range (using call date if available), agent, and score range.

### Main Metrics

```python
col1, col2, col3, col4 = st.columns(4)
# ...metrics for total calls, average score, unique agents, comments...
```
- Displays total calls audited, average score, unique agents, and comments provided.

### Tabs

```python
tab1, tab2, tab3, tab4, tab5 = st.tabs([...])
```
- Provides tabs for Overview, Agent Performance, Timeline, Comments, and Raw Data.

#### Overview Tab

```python
fig_dist = px.histogram(..., color_discrete_sequence=['#006400'])
fig_gauge = go.Figure(go.Indicator(..., bar={'color': "#006400"}))
```
- Shows score distribution and average score gauge with dark green color.

#### Timeline Tab

```python
timeline_data['TimelineDate'] = pd.to_datetime(...)
daily_stats = timeline_data.groupby('TimelineDate').agg(...)
fig_timeline = px.line(..., color_discrete_sequence=['#006400'])
fig_volume = px.bar(..., color_discrete_sequence=['#006400'])
```
- Shows trends over time using call dates and dark green charts.

#### Excel Export

```python
with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
    ...
    # Style column headers with white background and dark green font
    bright_fill = PatternFill(start_color='FFFFFF', end_color='FFFFFF', fill_type='solid')
    bright_font = Font(bold=True, color='006400')
    for col in ws_audit.iter_cols(min_row=1, max_row=1):
        for cell in col:
            cell.fill = bright_fill
            cell.font = bright_font
    # ...repeat for other sheets...
```
- Allows users to download the audit data and analytics as a multi-sheet Excel file with styled headers.

---

## How to Use This Documentation
- This file (`DOCUMENTATION.md`) should be kept in your project root for easy access.
- Update it as your code evolves.
- Use headings, code blocks, and bullet points for clarity.
- Optionally, add a table of contents, screenshots, or diagrams for further enhancement.

---

**This documentation provides a comprehensive, line-by-line reference for your QA Call Audit Tool project, ensuring future maintainability and knowledge transfer.**
